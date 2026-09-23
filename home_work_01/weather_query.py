"""Shared query / domain module for the Taiwan Weather Forecast web app.

This is the single place that holds SQL and forecast business logic for the
*read* side of the product (Spec R-SHR-1). Both presentation layers — the
Streamlit Grading App (``app.py``) and, in a later ticket, the Flask dashboard —
obtain every piece of data through this module and never write their own SQL or
re-implement the Region / Forecast-Day / Derived-Map-Temperature semantics
(INV-1). The module never talks to CWA: it imports no HTTP client and contains no
CWA endpoint URL or API-key reference (R-SHR-5, high-risk H-1 static check).

It reads the prepared ``data.db`` snapshot produced by the ingestion pipeline
(Issue #18). ``TemperatureForecasts`` holds the 6 Regions x 7 Forecast Days = 42
rows; ``IngestionMetadata`` holds the acquisition time (DR-2 / DR-17).

Semantics provided (R-SHR-2, names are HOW):

* ``snapshot_status``  (a) snapshot status in {ok, missing, empty, incomplete}
* ``region_list``      (b) the six Region names in the fixed order (DR-8)
* ``region_series``    (c) one Region's seven-day series, dataDate ascending
* ``day_values``       (d) one Forecast Day's six-Region values, with the
                           Derived Map Temperature and its colour band
* ``forecast_days``    (e) the Forecast Day list, ascending
* ``last_ingestion_time`` (f) the stored acquisition time (DR-17)

The database is opened **read-only**, at a path resolved relative to *this source
file* (not the process working directory), and every entry point accepts a
test-overridable ``db_path`` (R-SHR-3).
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from pathlib import Path
from typing import Sequence

# --- Location of the snapshot (R-SHR-3) ----------------------------------------
# Resolved relative to this file so the module works regardless of the current
# working directory; ``data.db`` lives beside this module in the unit root.
_MODULE_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH: Path = _MODULE_DIR / "data.db"

# --- Contract-fixed domain constants -------------------------------------------
# The canonical Region display order (R-SHR-2(b) / DR-8), owned by this read-side
# module. It is a fixed name list, not derived from SQL ordering or alphabetical
# order. (The ingestion package defines the same order for the *write* side; this
# module keeps the read side self-contained and free of any ingestion import so
# the presentation layers depend on nothing that touches an HTTP client.)
REGION_ORDER: tuple[str, ...] = (
    "北部地區",
    "中部地區",
    "南部地區",
    "東北部地區",
    "東部地區",
    "東南部地區",
)
REGION_COUNT = len(REGION_ORDER)  # 6
DAYS_REQUIRED = 7

FORECAST_TABLE = "TemperatureForecasts"
METADATA_TABLE = "IngestionMetadata"

# --- Derived Map Temperature colour bands (R-SHR-4 / DR-4) ----------------------
# Lower-inclusive bands, keyed by the *displayed* one-decimal value:
#   < 20 blue, 20 - < 25 green, 25 - < 30 yellow, >= 30 red.
BAND_BLUE = "blue"
BAND_GREEN = "green"
BAND_YELLOW = "yellow"
BAND_RED = "red"

_ONE_DP = Decimal("0.1")
_GREEN_MIN = Decimal("20")
_YELLOW_MIN = Decimal("25")
_RED_MIN = Decimal("30")


class SnapshotStatus(str, Enum):
    """Availability of the persisted Forecast Snapshot (R-SHR-2(a))."""

    OK = "ok"
    MISSING = "missing"
    EMPTY = "empty"
    INCOMPLETE = "incomplete"


@dataclass(frozen=True)
class DayValue:
    """One Region's values on one Forecast Day, with the derived map figure."""

    region_name: str
    mint: float
    maxt: float
    derived_map_temperature: float
    colour_band: str


class SnapshotError(RuntimeError):
    """Raised when a caller asks for data from a non-``ok`` snapshot.

    Presentation layers are expected to check :func:`snapshot_status` first and
    render an explicit message; this guards the data accessors so a missing or
    empty database can never surface as an unhandled low-level SQLite error.
    """


# --- Derived Map Temperature (R-SHR-4 / DR-4, AC-28) ---------------------------


def _derived_decimal(mint: float, maxt: float) -> Decimal:
    """(MinT + MaxT) / 2, half-up to one decimal place, as a ``Decimal``.

    Inputs are converted through ``str`` so the stored one-decimal REAL values
    are treated with decimal (not binary-float) semantics, matching the
    ``ROUND_HALF_UP`` rule fixed by DR-4. Example: (20.1, 25.2) -> 22.65 -> 22.7.
    """
    mean = (Decimal(str(mint)) + Decimal(str(maxt))) / Decimal(2)
    return mean.quantize(_ONE_DP, rounding=ROUND_HALF_UP)


def derived_map_temperature(mint: float, maxt: float) -> float:
    """Derived Map Temperature = (MinT + MaxT) / 2, half-up to one decimal."""
    return float(_derived_decimal(mint, maxt))


def colour_band(mint: float, maxt: float) -> str:
    """Colour band for the Derived Map Temperature, by its *displayed* value.

    Lower-inclusive bands (R-SHR-4): ``< 20`` blue, ``20 - < 25`` green,
    ``25 - < 30`` yellow, ``>= 30`` red. Banding uses the one-decimal displayed
    value so the colour always agrees with the number shown to the user.
    """
    shown = _derived_decimal(mint, maxt)
    if shown < _GREEN_MIN:
        return BAND_BLUE
    if shown < _YELLOW_MIN:
        return BAND_GREEN
    if shown < _RED_MIN:
        return BAND_YELLOW
    return BAND_RED


# --- Connection helpers --------------------------------------------------------


def _read_only_connection(db_path: str | Path) -> sqlite3.Connection:
    """Open ``db_path`` read-only (R-SHR-3).

    The caller must have checked existence; a missing file raises
    ``sqlite3.OperationalError`` under ``mode=ro``.

    The read-only URI is built from ``Path.as_uri()`` so that every character in
    the path is percent-encoded correctly. A plain ``"file:" + path`` string
    would let SQLite treat ``#`` as a fragment marker and decode ``%XX`` escapes,
    so a real ``data.db`` under a directory whose name contains ``#`` or a space
    would be mis-resolved and reported as missing (regression guarded by the
    special-character path test).
    """
    uri = Path(db_path).resolve().as_uri() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, name: str) -> bool:
    cur = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ?", (name,)
    )
    return cur.fetchone() is not None


# --- (a) snapshot status -------------------------------------------------------


def snapshot_status(db_path: str | Path = DEFAULT_DB_PATH) -> SnapshotStatus:
    """Return the availability of the Forecast Snapshot (R-SHR-2(a), DR-9).

    ``ok`` iff the snapshot is exactly the six canonical Regions, each with seven
    distinct Forecast Days and non-null ``mint``/``maxt`` (42 complete rows).
    ``missing`` if the database file (or its forecast table) is absent,
    ``empty`` if the table exists but has no rows, ``incomplete`` otherwise.
    """
    path = Path(db_path)
    if not path.exists():
        return SnapshotStatus.MISSING
    try:
        conn = _read_only_connection(path)
    except sqlite3.OperationalError:
        return SnapshotStatus.MISSING
    try:
        if not _table_exists(conn, FORECAST_TABLE):
            return SnapshotStatus.MISSING
        rows = conn.execute(
            f"SELECT regionName, dataDate, mint, maxt FROM {FORECAST_TABLE}"
        ).fetchall()
    finally:
        conn.close()

    if not rows:
        return SnapshotStatus.EMPTY
    return _classify_rows(rows)


def _classify_rows(rows: Sequence[sqlite3.Row]) -> SnapshotStatus:
    """OK iff exactly six canonical Regions x seven *consistent* days, all valued.

    ``ok`` requires the rows to form exactly the six canonical Regions, each
    carrying the *same* seven Forecast Days with a non-null ``mint``/``maxt`` for
    every cell (R-SHR-2(a), DR-9). A snapshot that has 42 rows but whose seven
    dates differ across Regions (so more than seven distinct dates overall) is
    ``incomplete``, not ``ok`` — otherwise a hand-edited or partially-rewritten
    database would pass as complete and the Grading App would show no warning.
    """
    if len(rows) != REGION_COUNT * DAYS_REQUIRED:
        return SnapshotStatus.INCOMPLETE

    by_region: dict[str, set[str]] = {}
    all_dates: set[str] = set()
    for row in rows:
        if row["mint"] is None or row["maxt"] is None:
            return SnapshotStatus.INCOMPLETE
        by_region.setdefault(row["regionName"], set()).add(row["dataDate"])
        all_dates.add(row["dataDate"])

    if set(by_region) != set(REGION_ORDER):
        return SnapshotStatus.INCOMPLETE
    if len(all_dates) != DAYS_REQUIRED:
        return SnapshotStatus.INCOMPLETE
    # Every Region must carry exactly the same seven Forecast Days. Because each
    # Region's date set is a subset of the seven shared dates and there are 42
    # rows across six Regions, equality here also rules out duplicate dates.
    if any(dates != all_dates for dates in by_region.values()):
        return SnapshotStatus.INCOMPLETE
    return SnapshotStatus.OK


# --- (b) Region list -----------------------------------------------------------


def region_list() -> tuple[str, ...]:
    """Return the six Region names in the fixed canonical order (R-SHR-2(b))."""
    return REGION_ORDER


# --- (c) one Region's seven-day series -----------------------------------------


def region_series(
    region_name: str, db_path: str | Path = DEFAULT_DB_PATH
) -> list[dict]:
    """Return one Region's series as ``{dataDate, mint, maxt}`` dicts, ascending.

    Ordered by ``dataDate`` ascending (Spec §4.1). Returns an empty list for a
    Region that is not present in the snapshot. Raises :class:`SnapshotError` if
    the database is missing or empty so callers surface an explicit message.
    """
    path = _require_readable(db_path)
    conn = _read_only_connection(path)
    try:
        rows = conn.execute(
            f"SELECT dataDate, mint, maxt FROM {FORECAST_TABLE} "
            "WHERE regionName = ? ORDER BY dataDate ASC",
            (region_name,),
        ).fetchall()
    finally:
        conn.close()
    return [
        {"dataDate": r["dataDate"], "mint": r["mint"], "maxt": r["maxt"]}
        for r in rows
    ]


# --- (d) one Forecast Day's six-Region values ----------------------------------


def day_values(
    data_date: str, db_path: str | Path = DEFAULT_DB_PATH
) -> list[DayValue]:
    """Return the six Regions' values for one Forecast Day, in canonical order.

    Each :class:`DayValue` carries the Derived Map Temperature and its colour
    band (R-SHR-2(d), R-SHR-4). Regions are returned in :data:`REGION_ORDER`;
    Regions absent for the given date are omitted. Raises :class:`SnapshotError`
    if the database is missing or empty.
    """
    path = _require_readable(db_path)
    conn = _read_only_connection(path)
    try:
        rows = conn.execute(
            f"SELECT regionName, mint, maxt FROM {FORECAST_TABLE} "
            "WHERE dataDate = ?",
            (data_date,),
        ).fetchall()
    finally:
        conn.close()

    by_region = {r["regionName"]: r for r in rows}
    result: list[DayValue] = []
    for region in REGION_ORDER:
        row = by_region.get(region)
        if row is None:
            continue
        mint = row["mint"]
        maxt = row["maxt"]
        result.append(
            DayValue(
                region_name=region,
                mint=mint,
                maxt=maxt,
                derived_map_temperature=derived_map_temperature(mint, maxt),
                colour_band=colour_band(mint, maxt),
            )
        )
    return result


# --- (e) Forecast Day list -----------------------------------------------------


def forecast_days(db_path: str | Path = DEFAULT_DB_PATH) -> list[str]:
    """Return the distinct Forecast Day dates, ascending (R-SHR-2(e))."""
    path = _require_readable(db_path)
    conn = _read_only_connection(path)
    try:
        rows = conn.execute(
            f"SELECT DISTINCT dataDate FROM {FORECAST_TABLE} ORDER BY dataDate ASC"
        ).fetchall()
    finally:
        conn.close()
    return [r["dataDate"] for r in rows]


# --- (f) last ingestion (acquisition) time -------------------------------------


def last_ingestion_time(db_path: str | Path = DEFAULT_DB_PATH) -> str | None:
    """Return the stored acquisition time exactly, or ``None`` if unavailable.

    This is ``IngestionMetadata.ingestedAt`` — the time the snapshot's data was
    fetched from CWA (DR-17), returned verbatim. Returns ``None`` when the
    database or the metadata row is absent so callers can show a fallback rather
    than crash.
    """
    path = Path(db_path)
    if not path.exists():
        return None
    try:
        conn = _read_only_connection(path)
    except sqlite3.OperationalError:
        return None
    try:
        if not _table_exists(conn, METADATA_TABLE):
            return None
        row = conn.execute(
            f"SELECT ingestedAt FROM {METADATA_TABLE} WHERE id = 1"
        ).fetchone()
    finally:
        conn.close()
    return row["ingestedAt"] if row is not None else None


# --- internal ------------------------------------------------------------------


def _require_readable(db_path: str | Path) -> Path:
    """Return ``db_path`` as a Path with a usable snapshot table, else raise.

    Raises :class:`SnapshotError` for a missing file, a missing forecast table,
    or an empty table, so the data accessors never emit a raw SQLite error.
    """
    path = Path(db_path)
    if not path.exists():
        raise SnapshotError(f"database not found: {path}")
    try:
        conn = _read_only_connection(path)
    except sqlite3.OperationalError as exc:
        raise SnapshotError(f"database cannot be opened: {path}") from exc
    try:
        if not _table_exists(conn, FORECAST_TABLE):
            raise SnapshotError(f"database has no snapshot table: {path}")
        count = conn.execute(f"SELECT count(*) FROM {FORECAST_TABLE}").fetchone()[0]
    finally:
        conn.close()
    if count == 0:
        raise SnapshotError(f"database snapshot is empty: {path}")
    return path
