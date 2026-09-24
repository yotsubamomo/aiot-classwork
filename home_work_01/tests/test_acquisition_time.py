"""Acquisition-time format validation (Issue #29, #18 R2 N-1; DR-22.3).

Covers the AT-1..AT-12 acceptance rules — via the ``acquisition_time`` validator
directly and via the ``pipeline.main`` / ``run_online`` entry points — for all three
sources the single validator guards (AT-8): the CLI ``--acquired-at`` value, the
provenance sidecar ``acquiredAt`` field, and the online ``ingestion_timestamp()``
output. Fail-closed cases assert a non-zero exit, an unchanged prior snapshot
(INV-3), a source-named message, and no key leak (H-1).
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from ingestion import config, pipeline, provenance
from ingestion.acquisition_time import (
    EXAMPLE,
    REQUIRED_FORMAT,
    AcquisitionTimeError,
    is_valid_acquisition_time,
    validate_acquisition_time,
)
from ingestion.derive import derive_snapshot
from ingestion.persist import persist_snapshot
from tests.conftest import FIXTURE_PATH

SEED_TIME = "2026-09-24T12:00:00+08:00"
SENTINEL_KEY = "SENTINEL-SECRET-KEY-abc123-do-not-leak"

# --- DR-22.3.3 valid examples (OK-1..OK-6) -------------------------------------

VALID_VALUES = {
    "committed": "2026-09-24T02:24:50+08:00",   # OK-1 committed data.db / sidecar
    "dr17_e4": "2026-09-24T01:39:31+08:00",     # OK-2 DR-17 E-4 acquisition time
    "seed": "2026-09-24T12:00:00+08:00",        # OK-3 existing SEED_TIME
    "day_low": "2026-01-01T00:00:00+08:00",     # OK-4 day-boundary low
    "day_high": "2026-12-31T23:59:59+08:00",    # OK-5 day-boundary high
    "leap_day": "2028-02-29T12:00:00+08:00",    # OK-6 leap day (2028 is leap)
}

# --- DR-22.3.4 invalid string examples (NG-1..NG-13 + edges) -------------------

INVALID_STRINGS = {
    "empty": "",                                    # NG-1
    "word": "yesterday",                            # NG-2
    "date_only": "2026-09-24",                      # NG-3 (fromisoformat accepts it)
    "utc_Z": "2026-09-24T02:24:50Z",                # NG-4 (UTC marker, not +08:00)
    "sidecar_word": "not-a-time",                   # NG-5
    "naive": "2026-09-24T02:24:50",                 # NG-6 (no offset)
    "offset_no_colon": "2026-09-24T02:24:50+0800",  # NG-7
    "offset_plus9": "2026-09-24T02:24:50+09:00",    # NG-8a
    "offset_zero": "2026-09-24T02:24:50+00:00",     # NG-8b
    "fractional": "2026-09-24T02:24:50.000+08:00",  # NG-9
    "space_sep": "2026-09-24 02:24:50+08:00",       # NG-10
    "lower_t": "2026-09-24t02:24:50+08:00",         # NG-11
    "leading_ws": " 2026-09-24T02:24:50+08:00",     # NG-12a
    "trailing_nl": "2026-09-24T02:24:50+08:00\n",   # NG-12b
    "whitespace_only": "   ",                       # NG-12c
    "impossible_day": "2026-02-30T02:24:50+08:00",  # NG-13a
    "hour_24": "2026-09-24T24:00:00+08:00",         # NG-13b
    "second_60": "2026-09-24T02:24:60+08:00",       # NG-13c
    "non_leap_feb29": "2026-02-29T02:24:50+08:00",  # 2026 is not a leap year
    "month_13": "2026-13-01T02:24:50+08:00",        # month out of range
}

# --- NG-14 non-string JSON values (sidecar only) -------------------------------

INVALID_NONSTRINGS = {
    "number": 1758651890,
    "float": 1.5,
    "bool": True,
    "null": None,
    "object": {},
    "array": [],
}


# --- helpers -------------------------------------------------------------------


def _signature(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        rows = conn.execute(
            "SELECT regionName, dataDate, mint, maxt FROM TemperatureForecasts "
            "ORDER BY regionName, dataDate"
        ).fetchall()
        meta = conn.execute(
            "SELECT ingestedAt, sourceDatasetId FROM IngestionMetadata"
        ).fetchall()
        return tuple(rows), tuple(meta)
    finally:
        conn.close()


def _seed(db_path, sample_response):
    persist_snapshot(derive_snapshot(sample_response), SEED_TIME, db_path=db_path)
    return _signature(db_path)


def _write_raw(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


def _write_sidecar(raw_path, acquired_value):
    """Write a sidecar with an arbitrary (possibly malformed / non-string) value."""
    meta = provenance.provenance_path(raw_path)
    meta.write_text(
        json.dumps(
            {
                "sourceDatasetId": config.RESOURCE_ID,
                "acquiredAt": acquired_value,
                "rawJson": raw_path.name,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    return meta


def _stored_ingested_at(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        return conn.execute("SELECT ingestedAt FROM IngestionMetadata").fetchone()[0]
    finally:
        conn.close()


# --- V-8: validator unit tests -------------------------------------------------


@pytest.mark.parametrize("value", VALID_VALUES.values(), ids=list(VALID_VALUES))
def test_valid_values_accepted_and_returned_verbatim(value):
    assert is_valid_acquisition_time(value) is True
    # AT-12: valid value returned unchanged (no normalization).
    assert validate_acquisition_time(value, source="unit") == value


@pytest.mark.parametrize(
    "value", INVALID_STRINGS.values(), ids=list(INVALID_STRINGS)
)
def test_invalid_strings_rejected(value):
    assert is_valid_acquisition_time(value) is False
    with pytest.raises(AcquisitionTimeError) as excinfo:
        validate_acquisition_time(value, source="--acquired-at")
    message = str(excinfo.value)
    assert "--acquired-at" in message           # AT-11(b) source
    assert repr(value) in message               # AT-11(a) value visible
    assert REQUIRED_FORMAT in message           # AT-11(c) required format
    assert EXAMPLE in message                   # AT-11(c) example


@pytest.mark.parametrize(
    "value", INVALID_NONSTRINGS.values(), ids=list(INVALID_NONSTRINGS)
)
def test_non_string_values_rejected_with_json_type(value):
    assert is_valid_acquisition_time(value) is False
    with pytest.raises(AcquisitionTimeError) as excinfo:
        validate_acquisition_time(
            value, source="the F-D0047-091.meta.json 'acquiredAt' field"
        )
    assert "JSON" in str(excinfo.value)         # AT-11(b) names the JSON type


def test_message_has_no_key_or_header():
    # AT-11 / H-1: the message is built only from the value, source and format.
    with pytest.raises(AcquisitionTimeError) as excinfo:
        validate_acquisition_time("bad", source="--acquired-at")
    message = str(excinfo.value)
    assert "Authorization" not in message
    assert "CWA_API_KEY" not in message


# --- V-1: CLI --acquired-at fails closed ---------------------------------------

CLI_BAD = {
    k: INVALID_STRINGS[k]
    for k in (
        "empty", "word", "date_only", "utc_Z", "naive", "offset_no_colon",
        "offset_plus9", "fractional", "space_sep", "lower_t", "impossible_day",
    )
}


@pytest.mark.parametrize("bad", CLI_BAD.values(), ids=list(CLI_BAD))
def test_cli_bad_value_fails_closed(tmp_path, capsys, sample_response, bad):
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    code = pipeline.main(
        ["--from-json", str(FIXTURE_PATH), "--db", str(db_path), "--acquired-at", bad]
    )
    captured = capsys.readouterr()
    assert code == 1                                    # AT-10 non-zero exit
    assert _signature(db_path) == before                # INV-3 snapshot unchanged
    assert "--acquired-at" in captured.err              # AT-11(b) source named
    assert repr(bad) in captured.err                    # AT-11(a) value visible
    assert REQUIRED_FORMAT in captured.err              # AT-11(c)
    # AT-10: validation precedes reading the raw JSON, so no body is echoed.
    assert "WeatherElement" not in (captured.out + captured.err)


# --- V-2: sidecar acquiredAt fails closed --------------------------------------

SIDECAR_BAD_STRINGS = {
    k: INVALID_STRINGS[k]
    for k in ("sidecar_word", "empty", "date_only", "utc_Z", "naive", "fractional")
}


@pytest.mark.parametrize(
    "bad", SIDECAR_BAD_STRINGS.values(), ids=list(SIDECAR_BAD_STRINGS)
)
def test_sidecar_bad_string_fails_closed(tmp_path, capsys, sample_response, bad):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    _write_sidecar(raw_path, bad)
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before
    assert "resp.meta.json" in captured.err             # AT-11(b) sidecar file named
    assert "acquiredAt" in captured.err                 # AT-11(b) field named


@pytest.mark.parametrize(
    "bad", INVALID_NONSTRINGS.values(), ids=list(INVALID_NONSTRINGS)
)
def test_sidecar_non_string_fails_closed(tmp_path, capsys, sample_response, bad):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    _write_sidecar(raw_path, bad)
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before
    assert "resp.meta.json" in captured.err
    assert "JSON" in captured.err                       # AT-11(b) JSON type named


def test_sidecar_missing_key_keeps_provenance_message(
    tmp_path, capsys, sample_response
):
    # AT-9: a missing acquiredAt key keeps the pre-existing ProvenanceError message,
    # distinct from a present-but-malformed value (which the validator rejects).
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    meta = provenance.provenance_path(raw_path)
    meta.write_text(
        json.dumps({"sourceDatasetId": config.RESOURCE_ID, "rawJson": raw_path.name}),
        encoding="utf-8",
    )
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before
    assert "has no 'acquiredAt' value" in captured.err


# --- V-3: valid values are accepted and stored verbatim ------------------------


@pytest.mark.parametrize("good", VALID_VALUES.values(), ids=list(VALID_VALUES))
def test_valid_value_via_cli_stored_verbatim(tmp_path, good):
    db_path = tmp_path / "data.db"
    code = pipeline.main(
        ["--from-json", str(FIXTURE_PATH), "--db", str(db_path), "--acquired-at", good]
    )
    assert code == 0
    assert _stored_ingested_at(db_path) == good


@pytest.mark.parametrize("good", VALID_VALUES.values(), ids=list(VALID_VALUES))
def test_valid_value_via_sidecar_stored_verbatim(tmp_path, sample_response, good):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    provenance.write_provenance(raw_path, good)
    db_path = tmp_path / "data.db"
    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    assert code == 0
    assert _stored_ingested_at(db_path) == good


# --- V-5: CLI/sidecar priority -------------------------------------------------


def test_bad_cli_does_not_fall_back_to_valid_sidecar(
    tmp_path, capsys, sample_response
):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    provenance.write_provenance(raw_path, "2026-09-20T06:00:00+08:00")  # valid sidecar
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    code = pipeline.main(
        ["--from-json", str(raw_path), "--db", str(db_path), "--acquired-at", ""]
    )
    captured = capsys.readouterr()
    assert code == 1                                    # AT-9 no fallback
    assert _signature(db_path) == before
    assert "--acquired-at" in captured.err
    assert "sidecar" in captured.err.lower()            # hint how to fall back


def test_valid_cli_overrides_unread_bad_sidecar(tmp_path, sample_response):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    _write_sidecar(raw_path, "not-a-time")              # never read: CLI wins
    db_path = tmp_path / "data.db"
    good = "2026-09-22T18:30:00+08:00"
    code = pipeline.main(
        ["--from-json", str(raw_path), "--db", str(db_path), "--acquired-at", good]
    )
    assert code == 0
    assert _stored_ingested_at(db_path) == good


# --- V-4: online ingestion_timestamp() -----------------------------------------


def test_ingestion_timestamp_output_is_valid():
    assert is_valid_acquisition_time(pipeline.ingestion_timestamp())


def test_ingestion_timestamp_strips_subsecond_at_day_boundary(monkeypatch):
    tz = timezone(timedelta(hours=8))
    fixed = datetime(2026, 12, 31, 23, 59, 59, 654321, tzinfo=tz)

    class FakeDateTime:
        @staticmethod
        def now(_tz=None):
            return fixed

    monkeypatch.setattr(pipeline, "datetime", FakeDateTime)
    out = pipeline.ingestion_timestamp()
    assert out == "2026-12-31T23:59:59+08:00"
    assert is_valid_acquisition_time(out)


def test_online_bad_timestamp_refuses_before_writing(
    tmp_path, capsys, monkeypatch, sample_response
):
    env = tmp_path / ".env"
    env.write_text(f"CWA_API_KEY={SENTINEL_KEY}\n", encoding="utf-8")
    raw_out = tmp_path / "raw" / "resp.json"
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)

    monkeypatch.setattr(pipeline, "fetch_raw", lambda key: sample_response)
    # A regressed generator returns a UTC marker instead of +08:00 (NG-4).
    monkeypatch.setattr(
        pipeline, "ingestion_timestamp", lambda: "2026-09-24T02:24:50Z"
    )

    code = pipeline.main(
        ["--env", str(env), "--raw-out", str(raw_out), "--db", str(db_path)]
    )
    captured = capsys.readouterr()
    assert code == 1                                        # AT-10 fail-closed
    assert not raw_out.exists()                             # no raw JSON written
    assert not provenance.provenance_path(raw_out).exists() # no sidecar written
    assert _signature(db_path) == before                    # DB unchanged
    assert SENTINEL_KEY not in (captured.out + captured.err)  # H-1 no key leak
    assert "ingestion_timestamp()" in captured.err          # AT-11(b) source named


# --- V-6: the committed sidecar value is valid under the new rule --------------


def test_committed_sidecar_value_is_valid():
    sidecar = config.UNIT_DIR / "data" / "raw" / "F-D0047-091.meta.json"
    record = json.loads(sidecar.read_text(encoding="utf-8"))
    assert is_valid_acquisition_time(record["acquiredAt"])
    assert record["acquiredAt"] == "2026-09-24T02:24:50+08:00"


# --- A-4 R1 F-1: ASCII-only digits (Unicode / full-width digits rejected) ------

# Non-ASCII decimal digits: Unicode ``\d`` matches them and int()/strptime accept a
# full-width or Arabic-Indic year, so before the re.ASCII fix a year in these digits
# was accepted and stored. AT-2 is ASCII digits only, so all must fail closed.
NON_ASCII_DIGITS = {
    "fullwidth_year": "２０２６-09-24T02:24:50+08:00",
    "arabic_indic_year": "٢٠٢٦-09-24T02:24:50+08:00",
    "devanagari_year": "२०२६-09-24T02:24:50+08:00",
    "fullwidth_month": "2026-０９-24T02:24:50+08:00",
    "fullwidth_day": "2026-09-２４T02:24:50+08:00",
    "fullwidth_second": "2026-09-24T02:24:５０+08:00",
}


@pytest.mark.parametrize("bad", NON_ASCII_DIGITS.values(), ids=list(NON_ASCII_DIGITS))
def test_non_ascii_digits_rejected_by_validator(bad):
    assert is_valid_acquisition_time(bad) is False
    with pytest.raises(AcquisitionTimeError):
        validate_acquisition_time(bad, source="--acquired-at")


@pytest.mark.parametrize("bad", NON_ASCII_DIGITS.values(), ids=list(NON_ASCII_DIGITS))
def test_non_ascii_digits_fail_closed_via_cli(tmp_path, capsys, sample_response, bad):
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)
    code = pipeline.main(
        ["--from-json", str(FIXTURE_PATH), "--db", str(db_path), "--acquired-at", bad]
    )
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before                # INV-3 unchanged
    assert "--acquired-at" in captured.err              # source named


@pytest.mark.parametrize("bad", NON_ASCII_DIGITS.values(), ids=list(NON_ASCII_DIGITS))
def test_non_ascii_digits_fail_closed_via_sidecar(
    tmp_path, capsys, sample_response, bad
):
    raw_path = _write_raw(tmp_path / "resp.json", sample_response)
    _write_sidecar(raw_path, bad)
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)
    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before
    assert "resp.meta.json" in captured.err             # sidecar file named


# --- A-4 R1 F-3: the pattern itself (not just strptime) rejects a trailing NL ---


def test_pattern_rejects_trailing_newline():
    # re.fullmatch (not re.match + '$', which allows a trailing '\n') means the
    # regex, not only strptime, rejects a trailing newline (and any tail).
    from ingestion.acquisition_time import _PATTERN

    assert _PATTERN.fullmatch("2026-09-24T02:24:50+08:00\n") is None
    assert is_valid_acquisition_time("2026-09-24T02:24:50+08:00\n") is False


# --- A-4 R1 F-2: offline validation runs BEFORE the raw JSON is read ------------


def test_cli_validation_precedes_raw_json_read(tmp_path, capsys, sample_response):
    # AT-10: a bad --acquired-at is rejected before the raw JSON is read/derived.
    # With a nonexistent raw JSON the failure must still be the acquisition-time
    # error (source --acquired-at), never a "raw JSON not found" error. This test
    # FAILS if the validate call is moved after the raw-JSON read.
    db_path = tmp_path / "data.db"
    before = _seed(db_path, sample_response)
    missing = tmp_path / "does-not-exist.json"
    code = pipeline.main(
        ["--from-json", str(missing), "--db", str(db_path),
         "--acquired-at", "yesterday"]
    )
    captured = capsys.readouterr()
    assert code == 1
    assert _signature(db_path) == before
    assert "--acquired-at" in captured.err              # validated first
    assert "'yesterday'" in captured.err                # the offending value
    assert "not found" not in captured.err.lower()      # NOT the missing-file error
    assert "raw JSON" not in captured.err
