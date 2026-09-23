"""Pipeline / offline-rerun tests.

Covers R-ING-5 (derive+persist offline from a saved JSON) and the AC-09 integration
guarantee that a validation failure leaves the previous snapshot untouched and
exits non-zero.
"""

from __future__ import annotations

import json
import sqlite3

import pytest

from ingestion import pipeline
from ingestion.derive import derive_snapshot
from ingestion.persist import persist_snapshot
from tests.conftest import FIXTURE_PATH, remove_county


def _dates(db_path):
    conn = sqlite3.connect(str(db_path))
    try:
        return {r[0] for r in conn.execute("SELECT DISTINCT dataDate FROM TemperatureForecasts")}
    finally:
        conn.close()


def test_offline_rerun_from_saved_json(tmp_path):
    db_path = tmp_path / "data.db"
    code = pipeline.main(["--from-json", str(FIXTURE_PATH), "--db", str(db_path)])
    assert code == 0
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    conn.close()


def test_failure_leaves_previous_snapshot_unchanged(tmp_path, sample_response):
    db_path = tmp_path / "data.db"
    # Seed a valid snapshot.
    persist_snapshot(derive_snapshot(sample_response), "2026-09-24T12:00:00+08:00", db_path=db_path)
    before = _dates(db_path)
    assert len(before) == 7

    # A broken input (missing member county) written to disk.
    bad = remove_county(sample_response, "苗栗縣")
    bad_path = tmp_path / "bad.json"
    bad_path.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

    code = pipeline.main(["--from-json", str(bad_path), "--db", str(db_path)])
    assert code == 1  # non-zero exit
    assert _dates(db_path) == before  # snapshot unchanged
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    conn.close()


def test_summary_reports_counts(sample_response):
    summary = pipeline.summarize_response(sample_response)
    assert summary["county_count"] == 22
    assert "最高溫度" in summary["element_names"]
    assert "最低溫度" in summary["element_names"]
    assert summary["period_count"] >= 7
