"""Pipeline / CLI tests.

Covers, through the ``pipeline.main`` entry point:
* R-ING-5 offline rebuild from a saved JSON;
* F-2 — every AC-09 negative and every AC-11 HTTP failure asserts a non-zero exit
  code, an unchanged prior snapshot, and (for AC-11) key-free output;
* F-8 — a date-shifted fixture re-ingested through the CLI fully replaces the snapshot;
* DR-17 T-1..T-4 — acquisition-time provenance semantics.
"""

from __future__ import annotations

import json
import sqlite3

import pytest
import requests

from ingestion import fetch, pipeline, provenance
from ingestion.derive import derive_snapshot
from ingestion.persist import persist_snapshot
from tests.conftest import (
    FIXTURE_PATH,
    corrupt_value,
    remove_county,
    remove_day,
    remove_half_day,
    shift_day,
)

SEED_TIME = "2026-09-24T12:00:00+08:00"
SENTINEL_KEY = "SENTINEL-SECRET-KEY-abc123-do-not-leak"


# --- helpers -------------------------------------------------------------------


def snapshot_signature(db_path):
    """A stable signature of the whole snapshot + metadata, for unchanged checks."""
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


def seed(db_path, sample_response):
    persist_snapshot(derive_snapshot(sample_response), SEED_TIME, db_path=db_path)
    return snapshot_signature(db_path)


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return path


class FakeResponse:
    def __init__(self, status_code=200, payload=None, raise_json=False):
        self.status_code = status_code
        self._payload = payload
        self.text = "" if payload is None else str(payload)
        self._raise_json = raise_json

    def json(self):
        if self._raise_json:
            raise ValueError("no JSON")
        return self._payload


# --- R-ING-5 offline rerun -----------------------------------------------------


def test_offline_rerun_from_saved_json(tmp_path):
    db_path = tmp_path / "data.db"
    code = pipeline.main(
        ["--from-json", str(FIXTURE_PATH), "--db", str(db_path),
         "--acquired-at", SEED_TIME]
    )
    assert code == 0
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    conn.close()


# --- F-2: AC-09 negatives through the CLI --------------------------------------


AC09_CASES = {
    "missing_county": lambda d: remove_county(d, "苗栗縣"),
    "missing_half_day": lambda d: remove_half_day(d, "臺北市", "2026-09-26", 18),
    "invalid_value": lambda d: corrupt_value(d, "臺北市", "2026-09-26", 6, "-"),
    "only_six_days": lambda d: remove_day(d, "2026-09-30"),
    "non_consecutive": lambda d: shift_day(d, "2026-09-30", "2026-10-02"),
}


@pytest.mark.parametrize("name", list(AC09_CASES))
def test_ac09_negative_via_cli(tmp_path, sample_response, name):
    db_path = tmp_path / "data.db"
    before = seed(db_path, sample_response)

    bad = AC09_CASES[name](sample_response)
    bad_path = write_json(tmp_path / "bad.json", bad)
    # Supply the acquisition time so the failure is the derivation, not provenance.
    code = pipeline.main(
        ["--from-json", str(bad_path), "--db", str(db_path), "--acquired-at", SEED_TIME]
    )
    assert code == 1                                    # non-zero exit
    assert snapshot_signature(db_path) == before        # prior snapshot unchanged


# --- F-2: AC-11 HTTP failures through the CLI (online, mocked) ------------------


def _run_online_with_get(monkeypatch, tmp_path, get_impl):
    """Run `main` (online) with a mocked requests.get and a seeded db; return
    (exit_code, captured_output, db_path, raw_out, before_signature)."""
    env = tmp_path / ".env"
    env.write_text(f"CWA_API_KEY={SENTINEL_KEY}\n", encoding="utf-8")
    raw_out = tmp_path / "raw" / "resp.json"
    db_path = tmp_path / "data.db"
    monkeypatch.setattr(fetch.requests, "get", get_impl)
    return env, raw_out, db_path


AC11_CASES = {
    "http_401": lambda url, **k: FakeResponse(401, {"message": "Authorization key is not correct."}),
    "http_404": lambda url, **k: FakeResponse(404, {"message": "Resource not found."}),
    "http_500": lambda url, **k: FakeResponse(500, "<html>error</html>"),
    "http_503": lambda url, **k: FakeResponse(503, {"message": "unavailable"}),
    "non_json": lambda url, **k: FakeResponse(200, raise_json=True),
}


@pytest.mark.parametrize("name", list(AC11_CASES))
def test_ac11_http_failure_via_cli(tmp_path, monkeypatch, capsys, sample_response, name):
    env, raw_out, db_path = _run_online_with_get(
        monkeypatch, tmp_path, AC11_CASES[name]
    )
    before = seed(db_path, sample_response)

    code = pipeline.main(
        ["--env", str(env), "--raw-out", str(raw_out), "--db", str(db_path)]
    )
    captured = capsys.readouterr()
    assert code == 1                                    # non-zero exit
    assert snapshot_signature(db_path) == before        # db not written
    assert not raw_out.exists()                         # no raw JSON saved on failure
    assert SENTINEL_KEY not in (captured.out + captured.err)  # key-free output


def test_ac11_timeout_via_cli(tmp_path, monkeypatch, capsys, sample_response):
    def timeout_get(url, **kwargs):
        raise requests.Timeout()

    env, raw_out, db_path = _run_online_with_get(monkeypatch, tmp_path, timeout_get)
    before = seed(db_path, sample_response)
    code = pipeline.main(
        ["--env", str(env), "--raw-out", str(raw_out), "--db", str(db_path)]
    )
    captured = capsys.readouterr()
    assert code == 1
    assert snapshot_signature(db_path) == before
    assert SENTINEL_KEY not in (captured.out + captured.err)


# --- F-8: date-shifted fixture fully replaces via the CLI ----------------------


def test_shifted_fixture_reingest_replaces_via_cli(tmp_path, sample_response):
    db_path = tmp_path / "data.db"
    seed(db_path, sample_response)
    old_dates = {r[1] for r in snapshot_signature(db_path)[0]}

    # Shift the whole fixture forward one week and re-ingest through the CLI.
    shifted = sample_response
    for old, new in [
        ("2026-09-24", "2026-10-01"), ("2026-09-25", "2026-10-02"),
        ("2026-09-26", "2026-10-03"), ("2026-09-27", "2026-10-04"),
        ("2026-09-28", "2026-10-05"), ("2026-09-29", "2026-10-06"),
        ("2026-09-30", "2026-10-07"), ("2026-10-01", "2026-10-08"),
    ]:
        shifted = shift_day(shifted, old, new)
    shifted_path = write_json(tmp_path / "shifted.json", shifted)

    code = pipeline.main(
        ["--from-json", str(shifted_path), "--db", str(db_path),
         "--acquired-at", "2026-10-01T09:00:00+08:00"]
    )
    assert code == 0
    conn = sqlite3.connect(str(db_path))
    dates = {r[0] for r in conn.execute("SELECT DISTINCT dataDate FROM TemperatureForecasts")}
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    conn.close()
    assert dates.isdisjoint(old_dates)  # old snapshot fully replaced


# --- DR-17 T-1..T-4: acquisition-time provenance -------------------------------


def test_t1_online_records_fetch_time_in_both_places(
    tmp_path, monkeypatch, sample_response
):
    fetch_time = "2026-09-24T08:15:30+08:00"
    env = tmp_path / ".env"
    env.write_text(f"CWA_API_KEY={SENTINEL_KEY}\n", encoding="utf-8")
    raw_out = tmp_path / "raw" / "resp.json"
    db_path = tmp_path / "data.db"

    monkeypatch.setattr(pipeline, "fetch_raw", lambda key: sample_response)
    monkeypatch.setattr(pipeline, "ingestion_timestamp", lambda: fetch_time)

    code = pipeline.run_online(env_path=env, raw_out=raw_out, db_path=db_path)
    assert code == 0

    # Provenance sidecar carries the fetch-time acquisition value...
    assert provenance.read_acquisition_time(raw_out) == fetch_time
    # ...and the database records the same value.
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT ingestedAt FROM IngestionMetadata").fetchone()[0] == fetch_time
    conn.close()


def test_t2_offline_uses_provenance_not_clock(tmp_path, monkeypatch, sample_response):
    acquired = "2026-09-20T06:00:00+08:00"
    clock = "2026-09-24T23:59:59+08:00"  # distinguishable, must NOT be used
    raw_path = write_json(tmp_path / "resp.json", sample_response)
    provenance.write_provenance(raw_path, acquired)
    db_path = tmp_path / "data.db"

    # If the offline path ever read the clock, this patch would make it visible.
    monkeypatch.setattr(pipeline, "ingestion_timestamp", lambda: clock)

    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    assert code == 0
    conn = sqlite3.connect(str(db_path))
    stored = conn.execute("SELECT ingestedAt FROM IngestionMetadata").fetchone()[0]
    conn.close()
    assert stored == acquired
    assert stored != clock


def test_t2b_offline_explicit_acquired_at_overrides(tmp_path, sample_response):
    raw_path = write_json(tmp_path / "resp.json", sample_response)
    provenance.write_provenance(raw_path, "2026-09-20T06:00:00+08:00")
    db_path = tmp_path / "data.db"
    explicit = "2026-09-22T18:30:00+08:00"

    code = pipeline.main(
        ["--from-json", str(raw_path), "--db", str(db_path), "--acquired-at", explicit]
    )
    assert code == 0
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT ingestedAt FROM IngestionMetadata").fetchone()[0] == explicit
    conn.close()


def test_t3_offline_without_acquisition_time_fails_closed(
    tmp_path, capsys, sample_response
):
    db_path = tmp_path / "data.db"
    before = seed(db_path, sample_response)
    # A raw JSON with NO provenance sidecar and no --acquired-at.
    raw_path = write_json(tmp_path / "orphan.json", sample_response)

    code = pipeline.main(["--from-json", str(raw_path), "--db", str(db_path)])
    captured = capsys.readouterr()
    assert code == 1                                    # non-zero exit
    assert snapshot_signature(db_path) == before        # snapshot unchanged
    assert "provenance" in captured.err.lower()         # names what is missing


def test_t4_provenance_record_is_key_free(tmp_path, sample_response):
    raw_path = write_json(tmp_path / "resp.json", sample_response)
    prov_path = provenance.write_provenance(raw_path, "2026-09-24T08:00:00+08:00")
    from ingestion.checks import scan_file

    text = prov_path.read_text(encoding="utf-8")
    assert scan_file(prov_path) == []
    assert "Authorization" not in text


# --- summary sanity ------------------------------------------------------------


def test_summary_reports_counts(sample_response):
    summary = pipeline.summarize_response(sample_response)
    assert summary["county_count"] == 22
    assert "最高溫度" in summary["element_names"]
    assert "最低溫度" in summary["element_names"]
    assert summary["period_count"] >= 7
