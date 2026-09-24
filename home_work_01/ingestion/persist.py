"""Database stage: persist the Forecast Snapshot into SQLite.

The snapshot semantics are "one current week only": ``TemperatureForecasts`` holds
either 0 rows or exactly 42, never a partial write. Each ingestion replaces the
whole snapshot inside a single transaction (DR-3 / R-DB-4), so re-running never
duplicates rows and a mid-write failure leaves the previous snapshot intact.

The teacher DDL is created verbatim (H-2). Ingestion time and source dataset id
are recorded in a separate ``IngestionMetadata`` table so ``TemperatureForecasts``
never changes (DR-2 / R-DB-5).
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Sequence

from . import config


def persist_snapshot(
    rows: Sequence[dict],
    ingested_at: str,
    source_dataset_id: str = config.RESOURCE_ID,
    db_path: str | Path = config.DB_PATH,
) -> int:
    """Create the schema if needed and atomically replace the whole snapshot.

    Returns the number of rows written. ``rows`` is expected to be the 42-row
    output of :func:`ingestion.derive.derive_snapshot`; this function does not
    re-validate the count so that the single source of the 6x7 rule stays in the
    derive stage.
    """
    conn = sqlite3.connect(str(db_path))
    try:
        _ensure_schema(conn)
        _replace_snapshot(conn, rows, ingested_at, source_dataset_id)
    finally:
        conn.close()
    return len(rows)


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """Create TemperatureForecasts (verbatim DDL) and the metadata table."""
    if not _table_exists(conn, config.FORECAST_TABLE):
        # Execute the teacher DDL exactly as specified so sqlite_master stores it
        # verbatim. Idempotence is handled by the existence check, not by editing
        # the DDL with IF NOT EXISTS.
        conn.execute(config.FORECAST_TABLE_DDL)
    conn.execute(config.METADATA_TABLE_DDL)
    conn.commit()


def _replace_snapshot(
    conn: sqlite3.Connection,
    rows: Sequence[dict],
    ingested_at: str,
    source_dataset_id: str,
) -> None:
    """Delete every existing row and insert the new snapshot in one transaction.

    ``with conn`` wraps the DELETE + INSERTs + metadata upsert in a single
    transaction that commits on success and rolls back on any exception, so a
    failure mid-write leaves the previous snapshot intact (DR-3).
    """
    with conn:
        conn.execute(f"DELETE FROM {config.FORECAST_TABLE}")
        conn.executemany(
            f"INSERT INTO {config.FORECAST_TABLE} "
            "(regionName, dataDate, mint, maxt) VALUES (?, ?, ?, ?)",
            [(r["regionName"], r["dataDate"], r["mint"], r["maxt"]) for r in rows],
        )
        conn.execute(
            f"INSERT INTO {config.METADATA_TABLE} "
            "(id, ingestedAt, sourceDatasetId) VALUES (1, ?, ?) "
            "ON CONFLICT(id) DO UPDATE SET "
            "ingestedAt = excluded.ingestedAt, "
            "sourceDatasetId = excluded.sourceDatasetId",
            (ingested_at, source_dataset_id),
        )


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
    )
    return cur.fetchone() is not None
