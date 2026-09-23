"""Persistence tests: AC-05 (DDL + verification SQL), AC-06 (idempotent replace),
AC-24 (ingestion metadata in a separate table)."""

from __future__ import annotations

import re
import sqlite3

import pytest

from ingestion.config import FORECAST_TABLE_DDL
from ingestion.derive import derive_snapshot
from ingestion.persist import persist_snapshot

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
INGESTED_AT = "2026-09-24T12:00:00+08:00"


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "data.db"


@pytest.fixture
def rows(sample_response):
    return derive_snapshot(sample_response)


# --- AC-05 ---------------------------------------------------------------------


def test_ddl_is_verbatim(rows, db_path):
    persist_snapshot(rows, INGESTED_AT, db_path=db_path)
    conn = sqlite3.connect(str(db_path))
    stored = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='TemperatureForecasts'"
    ).fetchone()[0]
    assert stored == FORECAST_TABLE_DDL.rstrip(";").rstrip()

    info = conn.execute("PRAGMA table_info(TemperatureForecasts)").fetchall()
    columns = [(c[1], c[2], c[5]) for c in info]  # (name, type, pk)
    assert columns == [
        ("id", "INTEGER", 1),
        ("regionName", "TEXT", 0),
        ("dataDate", "TEXT", 0),
        ("mint", "REAL", 0),
        ("maxt", "REAL", 0),
    ]
    conn.close()


def test_teacher_verification_sql(rows, db_path):
    persist_snapshot(rows, INGESTED_AT, db_path=db_path)
    conn = sqlite3.connect(str(db_path))
    distinct = [
        r[0]
        for r in conn.execute("SELECT DISTINCT regionName FROM TemperatureForecasts")
    ]
    assert len(distinct) == 6
    central = conn.execute(
        "SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區'"
    ).fetchall()
    assert len(central) == 7
    for row in central:
        # row = (id, regionName, dataDate, mint, maxt)
        assert DATE_RE.match(row[2])
    conn.close()


# --- AC-06 ---------------------------------------------------------------------


def test_reingest_same_snapshot_no_duplicates(rows, db_path):
    persist_snapshot(rows, INGESTED_AT, db_path=db_path)
    persist_snapshot(rows, INGESTED_AT, db_path=db_path)  # run twice
    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    dup = conn.execute(
        "SELECT regionName, dataDate, COUNT(*) c FROM TemperatureForecasts "
        "GROUP BY regionName, dataDate HAVING c > 1"
    ).fetchall()
    assert dup == []
    conn.close()


def test_date_shifted_snapshot_fully_replaces(rows, db_path):
    persist_snapshot(rows, INGESTED_AT, db_path=db_path)
    old_dates = {r["dataDate"] for r in rows}

    # A later week: shift every dataDate forward by seven days.
    shifted = []
    shift_map = {
        "2026-09-24": "2026-10-01",
        "2026-09-25": "2026-10-02",
        "2026-09-26": "2026-10-03",
        "2026-09-27": "2026-10-04",
        "2026-09-28": "2026-10-05",
        "2026-09-29": "2026-10-06",
        "2026-09-30": "2026-10-07",
    }
    for r in rows:
        shifted.append({**r, "dataDate": shift_map[r["dataDate"]]})
    persist_snapshot(shifted, INGESTED_AT, db_path=db_path)

    conn = sqlite3.connect(str(db_path))
    assert conn.execute("SELECT COUNT(*) FROM TemperatureForecasts").fetchone()[0] == 42
    present = {r[0] for r in conn.execute("SELECT DISTINCT dataDate FROM TemperatureForecasts")}
    assert present == set(shift_map.values())
    assert present.isdisjoint(old_dates)  # the old snapshot is entirely gone
    conn.close()


# --- AC-24 ---------------------------------------------------------------------


def test_metadata_stored_separately(rows, db_path):
    persist_snapshot(rows, INGESTED_AT, source_dataset_id="F-D0047-091", db_path=db_path)
    conn = sqlite3.connect(str(db_path))
    meta = conn.execute(
        "SELECT id, ingestedAt, sourceDatasetId FROM IngestionMetadata"
    ).fetchall()
    assert meta == [(1, INGESTED_AT, "F-D0047-091")]

    # Re-ingesting keeps a single metadata row (id = 1) and updates it.
    persist_snapshot(rows, "2026-09-25T09:00:00+08:00", db_path=db_path)
    meta2 = conn.execute("SELECT ingestedAt FROM IngestionMetadata").fetchall()
    assert meta2 == [("2026-09-25T09:00:00+08:00",)]

    # TemperatureForecasts DDL is untouched by the metadata table.
    stored = conn.execute(
        "SELECT sql FROM sqlite_master WHERE name='TemperatureForecasts'"
    ).fetchone()[0]
    assert stored == FORECAST_TABLE_DDL.rstrip(";").rstrip()
    conn.close()
