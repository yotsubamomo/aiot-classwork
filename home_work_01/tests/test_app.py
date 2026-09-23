"""Streamlit ``AppTest`` coverage for the Grading App (``app.py``).

Fully offline (no network, no ``.env``; R-TC-5). Uses the committed ``data.db``
through the app's default path for the happy-path assertions, and builds
alternative databases in ``tmp_path`` for the error states (AC-10).

Coverage:
* AC-02 title text, ``Select Region`` options and their fixed order
* AC-03 chart (``MaxT`` / ``MinT`` lines over the seven days) and the
        ``Date`` / ``MinT`` / ``MaxT`` table (seven ascending rows == ``data.db``),
        verified for 中部地區 and 東南部地區
* AC-10 missing / empty / incomplete databases -> message / warning, no exception
* AC-24 the displayed ingestion time equals the database metadata value
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import weather_query as wq

_UNIT_DIR = Path(__file__).resolve().parent.parent
_APP_PATH = _UNIT_DIR / "app.py"
_DATA_DB = _UNIT_DIR / "data.db"

_TIMEOUT = 60


def _run_default() -> AppTest:
    """Run app.py against its own default (committed) data.db."""
    return AppTest.from_file(str(_APP_PATH)).run(timeout=_TIMEOUT)


def _run_with_db(db_path: Path) -> AppTest:
    """Run the app's main() against an alternative database path (AC-10)."""
    script = (
        "import app\n"
        f"app.main(db_path=r{str(db_path)!r})\n"
    )
    return AppTest.from_string(script).run(timeout=_TIMEOUT)


def _select_region(at: AppTest, region: str) -> AppTest:
    box = next(s for s in at.selectbox if s.label == "Select Region")
    return box.set_value(region).run(timeout=_TIMEOUT)


# --- AC-02 title, Select Region options and order ------------------------------


def test_title_text() -> None:
    at = _run_default()
    assert [t.value for t in at.title] == ["Taiwan Weather Forecast"]


def test_select_region_options_and_order() -> None:
    at = _run_default()
    box = next(s for s in at.selectbox if s.label == "Select Region")
    assert box.options == [
        "北部地區",
        "中部地區",
        "南部地區",
        "東北部地區",
        "東部地區",
        "東南部地區",
    ]
    # SHOULD default to the first Region (R-GA-3 / DR-15).
    assert box.value == "北部地區"


# --- AC-03 chart and table, for two Regions ------------------------------------


@pytest.mark.parametrize("region", ["中部地區", "東南部地區"])
def test_region_chart_and_table(region: str) -> None:
    at = _run_default()
    at = _select_region(at, region)
    assert not at.exception

    # SHOULD chart title (R-GA-4 / DR-15), rendered as a subheader.
    assert any(
        s.value == f"Temperature Forecast – {region}" for s in at.subheader
    )

    # Table: exactly the Date / MinT / MaxT columns, seven ascending rows, equal
    # to data.db for this Region.
    frame = at.dataframe[0].value
    assert list(frame.columns) == ["Date", "MinT", "MaxT"]
    assert len(frame) == wq.DAYS_REQUIRED
    dates = list(frame["Date"])
    assert dates == sorted(dates)

    expected = _direct_series(region)
    assert dates == [d for d, _, _ in expected]
    assert list(frame["MinT"]) == [mn for _, mn, _ in expected]
    assert list(frame["MaxT"]) == [mx for _, _, mx in expected]

    # Chart: one line chart whose spec encodes both MaxT and MinT lines, with
    # MaxT red and MinT blue (DR-15), over the Date axis. The seven-day extent is
    # covered by the table above, which is built from the same shared-module
    # series that feeds the chart.
    charts = at.get("vega_lite_chart")
    assert len(charts) == 1
    spec = json.loads(charts[0].spec)
    color = _find_color_encoding(spec)
    assert color["scale"]["domain"] == ["MaxT", "MinT"]
    assert color["scale"]["range"] == ["#d62728", "#1f77b4"]
    assert _has_x_field(spec, "Date")


# --- AC-24 displayed ingestion time equals metadata ----------------------------


def test_ingestion_time_equals_metadata() -> None:
    at = _run_default()
    stored = _direct_metadata_time()
    assert stored is not None
    captions = [c.value for c in at.caption]
    assert any(stored in text for text in captions), captions


# --- AC-10 error states: message / warning, no exception -----------------------


def test_missing_database_shows_message_no_exception(tmp_path: Path) -> None:
    at = _run_with_db(tmp_path / "nope.db")
    assert not at.exception
    assert at.error
    assert any("data.db" in e.value for e in at.error)


def test_empty_database_shows_message_no_exception(tmp_path: Path) -> None:
    path = tmp_path / "empty.db"
    _build_forecast_db(path, rows=[])
    at = _run_with_db(path)
    assert not at.exception
    assert at.error


def test_incomplete_database_shows_warning_no_exception(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.db"
    _build_forecast_db(path, rows=_full_rows()[:-1])  # 41 rows
    at = _run_with_db(path)
    assert not at.exception
    assert at.warning


# --- helpers -------------------------------------------------------------------


def _direct_series(region: str) -> list[tuple[str, float, float]]:
    conn = sqlite3.connect(str(_DATA_DB))
    try:
        rows = conn.execute(
            "SELECT dataDate, mint, maxt FROM TemperatureForecasts "
            "WHERE regionName = ? ORDER BY dataDate ASC",
            (region,),
        ).fetchall()
    finally:
        conn.close()
    return [(d, mn, mx) for d, mn, mx in rows]


def _direct_metadata_time() -> str | None:
    conn = sqlite3.connect(str(_DATA_DB))
    try:
        row = conn.execute(
            "SELECT ingestedAt FROM IngestionMetadata WHERE id = 1"
        ).fetchone()
    finally:
        conn.close()
    return row[0] if row else None


def _full_rows() -> list[tuple[str, str, float, float]]:
    rows: list[tuple[str, str, float, float]] = []
    for ri, region in enumerate(wq.REGION_ORDER):
        for d in range(wq.DAYS_REQUIRED):
            rows.append((region, f"2026-03-{d + 1:02d}", 10.0 + ri, 20.0 + ri))
    return rows


def _build_forecast_db(
    path: Path, rows: list[tuple[str, str, float, float]]
) -> None:
    conn = sqlite3.connect(str(path))
    try:
        conn.execute(
            "CREATE TABLE TemperatureForecasts (id INTEGER PRIMARY KEY, "
            "regionName TEXT, dataDate TEXT, mint REAL, maxt REAL);"
        )
        conn.executemany(
            "INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt) "
            "VALUES (?, ?, ?, ?)",
            rows,
        )
        conn.execute(
            "CREATE TABLE IngestionMetadata (id INTEGER PRIMARY KEY CHECK (id = 1), "
            "ingestedAt TEXT NOT NULL, sourceDatasetId TEXT NOT NULL);"
        )
        conn.execute(
            "INSERT INTO IngestionMetadata (id, ingestedAt, sourceDatasetId) "
            "VALUES (1, '2026-01-02T03:04:05+08:00', 'F-D0047-091')"
        )
        conn.commit()
    finally:
        conn.close()


def _find_color_encoding(spec: dict) -> dict:
    """Return the colour encoding from a streamlit line_chart vega-lite spec."""
    for layer in spec.get("layer", []):
        encoding = layer.get("encoding", {})
        if "color" in encoding and "scale" in encoding["color"]:
            return encoding["color"]
    raise AssertionError("no colour encoding with a scale found in chart spec")


def _has_x_field(spec: dict, field: str) -> bool:
    for layer in spec.get("layer", []):
        x = layer.get("encoding", {}).get("x", {})
        if x.get("field") == field:
            return True
    return False
