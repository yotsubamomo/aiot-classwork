"""Derivation tests: AC-08 (positives) and AC-09 (five negatives).

Expected Region values are hand-computed from the county values in the committed
fixture and written inline with their source numbers, so a silent change to the
denominator, the day boundary, or the rounding rule fails the suite (H-3).
"""

from __future__ import annotations

import pytest

from ingestion.config import REGION_ORDER
from ingestion.derive import DeriveError, derive_snapshot
from tests.conftest import (
    corrupt_value,
    remove_county,
    remove_day,
    remove_half_day,
    shift_day,
)

WINDOW = [
    "2026-09-24",
    "2026-09-25",
    "2026-09-26",
    "2026-09-27",
    "2026-09-28",
    "2026-09-29",
    "2026-09-30",
]


def _row(rows, region, date):
    return next(r for r in rows if r["regionName"] == region and r["dataDate"] == date)


# --- AC-08 positives -----------------------------------------------------------


def test_derive_yields_exactly_42_rows(sample_response):
    rows = derive_snapshot(sample_response)
    assert len(rows) == 42
    assert {r["regionName"] for r in rows} == set(REGION_ORDER)
    for region in REGION_ORDER:
        dates = [r["dataDate"] for r in rows if r["regionName"] == region]
        assert dates == WINDOW  # seven consecutive days, ascending


def test_retains_seven_consecutive_days_dropping_leading_partial(sample_response):
    # The capture includes a leading 00:00-06:00 partial on 2026-09-24 that is not
    # a Forecast-Day segment; the window still starts at 2026-09-24 (which has both
    # 06:00 and 18:00 periods) and ends 2026-09-30 — exactly seven consecutive days.
    rows = derive_snapshot(sample_response)
    all_dates = sorted({r["dataDate"] for r in rows})
    assert all_dates == WINDOW


def test_every_row_has_both_values(sample_response):
    rows = derive_snapshot(sample_response)
    for r in rows:
        assert isinstance(r["mint"], float)
        assert isinstance(r["maxt"], float)


@pytest.mark.parametrize(
    "region, date, expected_mint, expected_maxt, source",
    [
        # 南部地區 = 臺南市, 高雄市, 屏東縣 (3 counties)
        # 2026-09-24: mins (27, 27, 25) -> 79/3 = 26.333 -> 26.3;
        #             maxs (31, 32, 33) -> 96/3 = 32.0
        ("南部地區", "2026-09-24", 26.3, 32.0, "mins 27/27/25, maxs 31/32/33"),
        # 2026-09-29: mins (26, 26, 25) -> 77/3 = 25.666 -> 25.7 (half-up);
        #             maxs (32, 32, 32) -> 32.0
        ("南部地區", "2026-09-29", 25.7, 32.0, "mins 26/26/25, maxs 32/32/32"),
        # 中部地區 = 臺中市, 彰化縣, 南投縣, 雲林縣, 嘉義市, 嘉義縣 (6 counties)
        # 2026-09-24: mins (25,25,24,25,25,25) -> 149/6 = 24.833 -> 24.8;
        #             maxs (33,32,33,33,33,33) -> 197/6 = 32.833 -> 32.8
        ("中部地區", "2026-09-24", 24.8, 32.8, "mins 25/25/24/25/25/25, maxs 33/32/33/33/33/33"),
        # 2026-09-30: mins (25,25,24,24,24,24) -> 146/6 = 24.333 -> 24.3;
        #             maxs (30,30,30,29,30,30) -> 179/6 = 29.833 -> 29.8
        ("中部地區", "2026-09-30", 24.3, 29.8, "mins 25/25/24/24/24/24, maxs 30/30/30/29/30/30"),
    ],
)
def test_region_values_match_hand_computed(
    sample_response, region, date, expected_mint, expected_maxt, source
):
    rows = derive_snapshot(sample_response)
    row = _row(rows, region, date)
    assert row["mint"] == expected_mint, source
    assert row["maxt"] == expected_maxt, source


def test_single_county_region_equals_county_value(sample_response):
    # 東部地區 = 花蓮縣 only, so the Region value is exactly the county-day value.
    rows = derive_snapshot(sample_response)
    row = _row(rows, "東部地區", "2026-09-24")
    # 花蓮縣 2026-09-24: day/night mins -> 24; maxs -> 30 (see fixture).
    assert row["mint"] == 24.0
    assert row["maxt"] == 30.0


# --- AC-09 negatives: each fails, names the problem, and (by raising before any
# --- persist call) leaves the database untouched -------------------------------


def test_missing_member_county_names_the_county(sample_response):
    bad = remove_county(sample_response, "苗栗縣")  # a 北部地區 member
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    assert "苗栗縣" in str(exc.value)


def test_missing_half_day_names_the_date(sample_response):
    bad = remove_half_day(sample_response, "臺北市", "2026-09-26", 18)  # night gone
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    message = str(exc.value)
    assert "2026-09-26" in message
    assert "臺北市" in message


def test_invalid_value_names_county_and_date(sample_response):
    bad = corrupt_value(sample_response, "臺北市", "2026-09-26", 6, bad_value="-")
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    message = str(exc.value)
    assert "臺北市" in message
    assert "2026-09-26" in message


def test_only_six_complete_days_fails(sample_response):
    bad = remove_day(sample_response, "2026-09-30")
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    assert "seven" in str(exc.value).lower()


def test_non_consecutive_days_fail(sample_response):
    # Relabel the last day so the seven retained dates have a gap (29 -> Oct 2).
    bad = shift_day(sample_response, "2026-09-30", "2026-10-02")
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    assert "consecutive" in str(exc.value).lower()


def test_empty_string_value_is_invalid(sample_response):
    bad = corrupt_value(sample_response, "高雄市", "2026-09-25", 6, bad_value="")
    with pytest.raises(DeriveError) as exc:
        derive_snapshot(bad)
    assert "高雄市" in str(exc.value)
