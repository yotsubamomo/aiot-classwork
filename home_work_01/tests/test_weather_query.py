"""Tests for the shared query / domain module (Spec R-SHR-2, R-SHR-3, R-SHR-4).

Fully offline: builds small SQLite databases in ``tmp_path`` and also reads the
committed ``data.db`` through the source-relative default path. No network, no
``.env`` (R-TC-5).

Coverage:
* R-SHR-2 (a) snapshot status in {ok, missing, empty, incomplete}
* R-SHR-2 (b) Region list in the fixed order (DR-8)
* R-SHR-2 (c) one Region's seven-day series, dataDate ascending
* R-SHR-2 (d) one Forecast Day's six-Region values with Derived Map Temperature
* R-SHR-2 (e) Forecast Day list ascending
* R-SHR-2 (f) last ingestion (acquisition) time, returned verbatim (DR-17)
* R-SHR-3 read-only open, source-relative default path, test-overridable path
* R-SHR-4 / AC-28 Derived Map Temperature half-up and colour band by shown value
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path

import pytest

import weather_query as wq

# Schema mirrors what the ingestion pipeline writes (kept inline so the read-side
# tests stay self-contained and independent of the ingestion package).
_FORECAST_DDL = (
    "CREATE TABLE TemperatureForecasts ("
    "id INTEGER PRIMARY KEY, regionName TEXT, dataDate TEXT, mint REAL, maxt REAL);"
)
_METADATA_DDL = (
    "CREATE TABLE IngestionMetadata ("
    "id INTEGER PRIMARY KEY CHECK (id = 1), ingestedAt TEXT NOT NULL, "
    "sourceDatasetId TEXT NOT NULL);"
)

_DEFAULT_INGESTED_AT = "2026-01-02T03:04:05+08:00"


def _build_db(
    path: Path,
    rows: list[tuple[str, str, float, float]],
    *,
    ingested_at: str | None = _DEFAULT_INGESTED_AT,
    forecast_table: bool = True,
) -> None:
    """Create a snapshot database at ``path`` with the given forecast rows."""
    conn = sqlite3.connect(str(path))
    try:
        if forecast_table:
            conn.execute(_FORECAST_DDL)
            conn.executemany(
                "INSERT INTO TemperatureForecasts "
                "(regionName, dataDate, mint, maxt) VALUES (?, ?, ?, ?)",
                rows,
            )
        if ingested_at is not None:
            conn.execute(_METADATA_DDL)
            conn.execute(
                "INSERT INTO IngestionMetadata (id, ingestedAt, sourceDatasetId) "
                "VALUES (1, ?, ?)",
                (ingested_at, "F-D0047-091"),
            )
        conn.commit()
    finally:
        conn.close()


def _full_rows() -> list[tuple[str, str, float, float]]:
    """Six canonical Regions x seven consecutive days with distinct values."""
    rows: list[tuple[str, str, float, float]] = []
    for ri, region in enumerate(wq.REGION_ORDER):
        for d in range(wq.DAYS_REQUIRED):
            date = f"2026-03-{d + 1:02d}"
            rows.append((region, date, 10.0 + ri + d * 0.1, 20.0 + ri + d * 0.1))
    return rows


def _mismatched_rows() -> list[tuple[str, str, float, float]]:
    """42 rows, six Regions x seven rows each, but the dates differ across Regions.

    One Region's seven days are shifted into a different week, so there are 14
    distinct dates overall (F-1): the same six-Regions/seven-rows shape but not a
    consistent 6x7 snapshot.
    """
    out: list[tuple[str, str, float, float]] = []
    for region, date, mn, mx in _full_rows():
        if region == "東部地區":
            date = f"2026-04-{int(date[-2:]):02d}"  # shift this Region's week
        out.append((region, date, mn, mx))
    return out


@pytest.fixture
def ok_db(tmp_path: Path) -> Path:
    path = tmp_path / "ok.db"
    _build_db(path, _full_rows())
    return path


# --- R-SHR-2(a) snapshot status ------------------------------------------------


def test_status_ok(ok_db: Path) -> None:
    assert wq.snapshot_status(ok_db) is wq.SnapshotStatus.OK


def test_status_missing(tmp_path: Path) -> None:
    assert wq.snapshot_status(tmp_path / "nope.db") is wq.SnapshotStatus.MISSING


def test_status_empty(tmp_path: Path) -> None:
    path = tmp_path / "empty.db"
    _build_db(path, [])  # forecast table present, zero rows
    assert wq.snapshot_status(path) is wq.SnapshotStatus.EMPTY


def test_status_incomplete_missing_a_day(tmp_path: Path) -> None:
    path = tmp_path / "short.db"
    _build_db(path, _full_rows()[:-1])  # 41 rows
    assert wq.snapshot_status(path) is wq.SnapshotStatus.INCOMPLETE


def test_status_incomplete_null_value(tmp_path: Path) -> None:
    rows = _full_rows()
    region, date, _, maxt = rows[0]
    rows[0] = (region, date, None, maxt)  # a missing value
    path = tmp_path / "null.db"
    _build_db(path, rows)
    assert wq.snapshot_status(path) is wq.SnapshotStatus.INCOMPLETE


def test_status_incomplete_wrong_region_set(tmp_path: Path) -> None:
    rows = _full_rows()
    # Relabel every 北部地區 row to a non-canonical Region name: still 42 rows but
    # only five canonical Regions are present.
    rows = [
        (("其他地區" if r[0] == "北部地區" else r[0]), r[1], r[2], r[3])
        for r in rows
    ]
    path = tmp_path / "wrongset.db"
    _build_db(path, rows)
    assert wq.snapshot_status(path) is wq.SnapshotStatus.INCOMPLETE


def test_status_incomplete_mismatched_dates(tmp_path: Path) -> None:
    # F-1: 42 rows, six Regions x seven rows each, but the seven dates differ
    # across Regions (14 distinct overall) -> incomplete, never ok.
    path = tmp_path / "mismatch.db"
    _build_db(path, _mismatched_rows())
    assert wq.snapshot_status(path) is wq.SnapshotStatus.INCOMPLETE


def test_status_committed_data_db_is_ok() -> None:
    # The prepared, committed snapshot beside the module is a complete 6x7.
    assert wq.snapshot_status() is wq.SnapshotStatus.OK


# --- R-SHR-2(b) Region list ----------------------------------------------------


def test_region_list_fixed_order() -> None:
    assert wq.region_list() == (
        "北部地區",
        "中部地區",
        "南部地區",
        "東北部地區",
        "東部地區",
        "東南部地區",
    )


# --- R-SHR-2(c) one Region's seven-day series ----------------------------------


def test_region_series_ascending_and_values(ok_db: Path) -> None:
    series = wq.region_series("中部地區", ok_db)
    assert len(series) == wq.DAYS_REQUIRED
    dates = [row["dataDate"] for row in series]
    assert dates == sorted(dates)  # ascending
    # 中部地區 is index 1 in REGION_ORDER; values follow the _full_rows formula.
    assert series[0] == {"dataDate": "2026-03-01", "mint": 11.0, "maxt": 21.0}
    assert series[-1]["dataDate"] == "2026-03-07"


def test_region_series_unknown_region_is_empty(ok_db: Path) -> None:
    assert wq.region_series("no-such-region", ok_db) == []


def test_region_series_missing_db_raises(tmp_path: Path) -> None:
    with pytest.raises(wq.SnapshotError):
        wq.region_series("中部地區", tmp_path / "nope.db")


def test_region_series_matches_committed_data_db() -> None:
    # Values equal data.db (AC-03 support): compare against a direct read.
    series = wq.region_series("東南部地區")
    expected = _direct_series(wq.DEFAULT_DB_PATH, "東南部地區")
    assert [(s["dataDate"], s["mint"], s["maxt"]) for s in series] == expected


# --- R-SHR-2(d) one Forecast Day's six-Region values ---------------------------


def test_day_values_canonical_order_with_derived(ok_db: Path) -> None:
    values = wq.day_values("2026-03-01", ok_db)
    assert [v.region_name for v in values] == list(wq.REGION_ORDER)
    first = values[0]  # 北部地區 day 0: mint 10.0, maxt 20.0 -> mean 15.0 -> blue
    assert first.mint == 10.0 and first.maxt == 20.0
    assert first.derived_map_temperature == 15.0
    assert first.colour_band == wq.BAND_BLUE


def test_day_values_missing_db_raises(tmp_path: Path) -> None:
    with pytest.raises(wq.SnapshotError):
        wq.day_values("2026-03-01", tmp_path / "nope.db")


# --- R-SHR-2(e) Forecast Day list ----------------------------------------------


def test_forecast_days_ascending(ok_db: Path) -> None:
    days = wq.forecast_days(ok_db)
    assert days == [f"2026-03-{d + 1:02d}" for d in range(wq.DAYS_REQUIRED)]
    assert days == sorted(days)


# --- R-SHR-2(f) last ingestion (acquisition) time ------------------------------


def test_last_ingestion_time_verbatim(ok_db: Path) -> None:
    assert wq.last_ingestion_time(ok_db) == _DEFAULT_INGESTED_AT


def test_last_ingestion_time_none_without_metadata(tmp_path: Path) -> None:
    path = tmp_path / "nometa.db"
    _build_db(path, _full_rows(), ingested_at=None)
    assert wq.last_ingestion_time(path) is None


def test_last_ingestion_time_missing_db_is_none(tmp_path: Path) -> None:
    assert wq.last_ingestion_time(tmp_path / "nope.db") is None


# --- R-SHR-3 read-only, source-relative, overridable ---------------------------


def test_default_path_is_source_relative() -> None:
    expected = Path(wq.__file__).resolve().parent / "data.db"
    assert wq.DEFAULT_DB_PATH == expected


def test_default_path_independent_of_cwd(ok_db: Path, tmp_path: Path) -> None:
    # Changing the working directory must not change what the default resolves to.
    original = os.getcwd()
    os.chdir(tmp_path)
    try:
        assert wq.snapshot_status() is wq.SnapshotStatus.OK  # uses committed data.db
    finally:
        os.chdir(original)


def test_override_path_is_used(ok_db: Path) -> None:
    # An explicit db_path overrides the default (test-overridable, R-SHR-3).
    assert wq.forecast_days(ok_db) != wq.forecast_days()


def test_connection_is_read_only(ok_db: Path) -> None:
    conn = wq._read_only_connection(ok_db)
    try:
        with pytest.raises(sqlite3.OperationalError):
            conn.execute("DELETE FROM TemperatureForecasts")
    finally:
        conn.close()


def test_special_character_path_opens(tmp_path: Path) -> None:
    # F-2: a real database under a directory whose name contains '#' and a space
    # must open (the read-only URI percent-encodes the path); previously it was
    # mis-resolved and reported as missing.
    special_dir = tmp_path / "c#course dir"
    special_dir.mkdir()
    path = special_dir / "data.db"
    _build_db(path, _full_rows())

    assert wq.snapshot_status(path) is wq.SnapshotStatus.OK
    assert len(wq.region_series("中部地區", path)) == wq.DAYS_REQUIRED
    assert wq.forecast_days(path) == [
        f"2026-03-{d + 1:02d}" for d in range(wq.DAYS_REQUIRED)
    ]
    assert wq.last_ingestion_time(path) == _DEFAULT_INGESTED_AT

    # Read-only is still enforced under the encoded URI.
    conn = wq._read_only_connection(path)
    try:
        with pytest.raises(sqlite3.OperationalError):
            conn.execute("DELETE FROM TemperatureForecasts")
    finally:
        conn.close()


# --- R-SHR-4 / AC-28 Derived Map Temperature and colour bands ------------------


@pytest.mark.parametrize(
    "mint, maxt, expected_value, expected_band",
    [
        (20.1, 25.2, 22.7, wq.BAND_GREEN),  # half-up 22.65 -> 22.7
        (19.9, 20.0, 20.0, wq.BAND_GREEN),  # 19.95 -> 20.0 -> green (>=20)
        (24.9, 25.0, 25.0, wq.BAND_YELLOW),  # 24.95 -> 25.0 -> yellow (>=25)
        (29.9, 30.0, 30.0, wq.BAND_RED),  # 29.95 -> 30.0 -> red (>=30)
        (15.0, 24.8, 19.9, wq.BAND_BLUE),  # 19.9 -> blue (<20)
    ],
)
def test_derived_map_temperature_and_band(
    mint: float, maxt: float, expected_value: float, expected_band: str
) -> None:
    assert wq.derived_map_temperature(mint, maxt) == expected_value
    assert wq.colour_band(mint, maxt) == expected_band


# --- helpers -------------------------------------------------------------------


def _direct_series(db_path: Path, region: str) -> list[tuple[str, float, float]]:
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            "SELECT dataDate, mint, maxt FROM TemperatureForecasts "
            "WHERE regionName = ? ORDER BY dataDate ASC",
            (region,),
        ).fetchall()
    finally:
        conn.close()
    return [(d, mn, mx) for d, mn, mx in rows]
