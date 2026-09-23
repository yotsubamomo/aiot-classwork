"""Flask test-client coverage for the dashboard backend (``server.py``).

Fully offline (no network, no ``.env``; R-TC-4, R-TC-5). The happy-path tests use
the committed ``data.db`` through the app's default path; the 503 states build
alternative databases in ``tmp_path`` and drive ``create_app(db_path=...)``.

Coverage:
* R-DS-1 / AC-02   ``GET /`` returns 200 and the page contains the title
* R-DS-2 / AC-16   ``/api/health`` 200 (ok) and 503 (missing / empty / incomplete)
* R-DS-3 / AC-10   each data endpoint: normal, 404 (unknown Region/date), 503
* INV-2            for all six Regions the series endpoint's seven
                   ``(Date, MinT, MaxT)`` equal the shared module's (what the
                   Grading App shows) — asserted by direct comparison
* R-DS-3 / AC-10   error responses are JSON carrying a human-readable ``error``
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from urllib.parse import quote

import pytest

import weather_query as wq
from server import create_app

_UNIT_DIR = Path(__file__).resolve().parent.parent
_DATA_DB = _UNIT_DIR / "data.db"


# --- fixtures ------------------------------------------------------------------


@pytest.fixture
def client():
    """A test client bound to the committed data.db (the ok snapshot)."""
    return create_app().test_client()


def _client_for(db_path: Path):
    return create_app(db_path=db_path).test_client()


def _series_path(region: str) -> str:
    return "/api/regions/" + quote(region) + "/series"


# --- GET / (R-DS-1, AC-02) -----------------------------------------------------


def test_index_returns_page_with_title(client) -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert "Taiwan Weather Forecast" in res.get_data(as_text=True)


def test_index_page_has_visible_teacher_text(client) -> None:
    """Guard the visible page text, not just <title> (INV-4 / H-2; finding F-5).

    A mutant that changes the <h1>, the Select Region label, or a table header
    must fail here even though the <title> is untouched."""
    html = client.get("/").get_data(as_text=True)
    assert ">Taiwan Weather Forecast</h1>" in html, "visible <h1> title missing"
    assert ">Select Region</label>" in html, "Select Region label missing"
    for header in ("Date", "MinT", "MaxT"):
        assert f">{header}</th>" in html, f"table header {header} missing"


# --- /api/health ok (R-DS-2, AC-16) --------------------------------------------


def test_health_ok(client) -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.get_json()
    assert body["status"] == "ok"
    assert body["region_count"] == wq.REGION_COUNT  # 6
    assert body["forecast_day_count"] == wq.DAYS_REQUIRED  # 7
    assert body["ingestion_time"] == _stored_ingestion_time()


# --- /api/health 503 (missing / empty / incomplete) (R-DS-2, AC-16, AC-10) -----


def test_health_missing_is_503(tmp_path: Path) -> None:
    res = _client_for(tmp_path / "nope.db").get("/api/health")
    assert res.status_code == 503
    body = res.get_json()
    assert body["status"] == "unavailable"
    assert body["reason"] == "missing"
    assert body["error"]


def test_health_empty_is_503(tmp_path: Path) -> None:
    path = tmp_path / "empty.db"
    _build_db(path, rows=[])
    res = _client_for(path).get("/api/health")
    assert res.status_code == 503
    assert res.get_json()["reason"] == "empty"


def test_health_incomplete_is_503(tmp_path: Path) -> None:
    path = tmp_path / "incomplete.db"
    _build_db(path, rows=_full_rows()[:-1])  # 41 rows
    res = _client_for(path).get("/api/health")
    assert res.status_code == 503
    assert res.get_json()["reason"] == "incomplete"


def test_health_mismatched_dates_is_503(tmp_path: Path) -> None:
    # 42 rows but the seven dates differ across Regions -> incomplete, not ok
    # (guards the shared module's #19 F-1 fix from the API's side).
    path = tmp_path / "mismatch.db"
    _build_db(path, rows=_mismatched_rows())
    res = _client_for(path).get("/api/health")
    assert res.status_code == 503
    assert res.get_json()["reason"] == "incomplete"


# --- /api/regions: normal + 503 ------------------------------------------------


def test_regions_normal(client) -> None:
    res = client.get("/api/regions")
    assert res.status_code == 200
    assert res.get_json()["regions"] == list(wq.region_list())


def test_regions_503_when_unavailable(tmp_path: Path) -> None:
    res = _client_for(tmp_path / "nope.db").get("/api/regions")
    assert res.status_code == 503
    assert res.get_json()["error"]


# --- /api/days: normal + 503 ---------------------------------------------------


def test_days_normal(client) -> None:
    res = client.get("/api/days")
    assert res.status_code == 200
    days = res.get_json()["days"]
    assert days == sorted(days)
    assert len(days) == wq.DAYS_REQUIRED
    assert days == wq.forecast_days(_DATA_DB)


def test_days_503_when_unavailable(tmp_path: Path) -> None:
    res = _client_for(tmp_path / "nope.db").get("/api/days")
    assert res.status_code == 503
    assert res.get_json()["error"]


# --- /api/regions/<region>/series: normal + 404 + 503 --------------------------


@pytest.mark.parametrize("region", list(wq.REGION_ORDER))
def test_region_series_normal(client, region: str) -> None:
    res = client.get(_series_path(region))
    assert res.status_code == 200
    body = res.get_json()
    assert body["region"] == region
    series = body["series"]
    assert len(series) == wq.DAYS_REQUIRED
    dates = [row["dataDate"] for row in series]
    assert dates == sorted(dates)


def test_region_series_unknown_is_404(client) -> None:
    res = client.get(_series_path("沒有這個地區"))
    assert res.status_code == 404
    assert res.get_json()["error"]


def test_region_series_503_when_unavailable(tmp_path: Path) -> None:
    res = _client_for(tmp_path / "nope.db").get(_series_path("北部地區"))
    assert res.status_code == 503
    assert res.get_json()["error"]


# --- /api/days/<date>: normal + 404 + 503 --------------------------------------


def test_day_values_normal(client) -> None:
    date = wq.forecast_days(_DATA_DB)[0]
    res = client.get("/api/days/" + date)
    assert res.status_code == 200
    body = res.get_json()
    assert body["date"] == date
    values = body["values"]
    assert [v["regionName"] for v in values] == list(wq.region_list())
    for v in values:
        # Derived Map Temperature and its colour band are present (R-SHR-4).
        assert "derivedMapTemperature" in v
        assert v["colourBand"] in {"blue", "green", "yellow", "red"}
        expected = wq.derived_map_temperature(v["mint"], v["maxt"])
        assert v["derivedMapTemperature"] == expected


def test_day_values_unknown_is_404(client) -> None:
    res = client.get("/api/days/2099-01-01")
    assert res.status_code == 404
    assert res.get_json()["error"]


def test_day_values_503_when_unavailable(tmp_path: Path) -> None:
    res = _client_for(tmp_path / "nope.db").get("/api/days/2026-09-24")
    assert res.status_code == 503
    assert res.get_json()["error"]


# --- INV-2: dashboard series == shared module (== Grading App) -----------------


def test_inv2_series_equals_shared_module_for_all_regions(client) -> None:
    """For every Region the API's seven (Date, MinT, MaxT) equal what the shared
    module returns — i.e. exactly what the Streamlit Grading App shows (INV-2)."""
    for region in wq.region_list():
        api_series = client.get(_series_path(region)).get_json()["series"]
        shared = wq.region_series(region, _DATA_DB)
        api_triples = [(r["dataDate"], r["mint"], r["maxt"]) for r in api_series]
        shared_triples = [(r["dataDate"], r["mint"], r["maxt"]) for r in shared]
        assert api_triples == shared_triples, region
        assert len(api_triples) == wq.DAYS_REQUIRED


# --- helpers -------------------------------------------------------------------


def _stored_ingestion_time() -> str | None:
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


def _mismatched_rows() -> list[tuple[str, str, float, float]]:
    out: list[tuple[str, str, float, float]] = []
    for region, date, mn, mx in _full_rows():
        if region == "東部地區":
            date = f"2026-04-{int(date[-2:]):02d}"
        out.append((region, date, mn, mx))
    return out


def _build_db(path: Path, rows: list[tuple[str, str, float, float]]) -> None:
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
