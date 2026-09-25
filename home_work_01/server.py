"""Taiwan Weather Forecast — Flask dashboard backend (``server.py``).

This is the deployed presentation layer's server (Spec R-DS-1..R-DS-8, MVM part).
A single Flask application serves both the dashboard **page** (``GET /`` → the
static ``index.html``) and the JSON **API** (everything under the ``/api/``
prefix), plus the page's own static assets under ``/static/``. It is structured
to deploy to Vercel as one Python serverless function (brief §5.2): ``api/index.py``
imports ``app`` from here, ``vercel.json`` routes every request to that function,
and ``data.db`` is packaged beside the code and opened read-only. The forecast
path needs no environment variable or secret (R-SEC-3 for the forecast path,
INV-V2-1).

Every piece of **forecast** data comes through the shared :mod:`weather_query`
module — the single owner of SQL and forecast business logic (R-DS-5, INV-1).
This file therefore contains no SQL, imports no HTTP client, and references no
CWA URL or API key itself. The dashboard shows the same MVM
behaviour as the Streamlit Grading App (INV-2): the title ``Taiwan Weather
Forecast``, a ``Select Region`` control over the six Regions in the fixed order,
and — for the selected Region — a ``MaxT`` / ``MinT`` seven-day line chart and a
``Date`` / ``MinT`` / ``MaxT`` table equal to ``data.db``, together with the
snapshot's acquisition time (DR-17).

Availability semantics (DR-7 / DR-9): ``GET /api/health`` returns 200 when the
snapshot is a complete six-Region × seven-day snapshot and 503 otherwise; every
data endpoint returns 503 when the snapshot is unavailable (missing / empty /
incomplete) and 404 for an unknown Region or date. Error responses are JSON with
a human-readable ``error`` message so the frontend never shows a blank page
(R-DS-6).

**V2 Latest Observation** (SPEC-V2 §2.2, §2.4; Issue #35). ``GET
/api/observations/latest`` is the Now mode's observation path. It is served by
:mod:`observation`, the backend's only CWA access: it reads the key from the
``CWA_API_KEY`` process environment variable at request time and returns either
a normalised success body or a classified non-2xx failure (``reason`` /
``error``). The forecast endpoints above never touch it, so they stay CWA-free
and key-free (INV-V2-1). For a local run, ``python server.py`` copies
``CWA_API_KEY`` from the unit's untracked ``.env`` into the environment first.
"""

from __future__ import annotations

from pathlib import Path

from flask import Flask, jsonify, send_from_directory

import observation
import weather_query as wq

PAGE_TITLE = "Taiwan Weather Forecast"

# Static assets (index.html / styles.css / app.js) live beside this module so the
# whole unit deploys as one function with its files packaged next to it.
_STATIC_DIR = Path(__file__).resolve().parent / "static"

# Human-readable reasons for an unavailable snapshot, keyed by the shared
# module's status (DR-9). ``ok`` is not a reason and never appears here.
_UNAVAILABLE_REASON = {
    wq.SnapshotStatus.MISSING: (
        "The forecast database is missing. Run the ingestion pipeline to create it."
    ),
    wq.SnapshotStatus.EMPTY: (
        "The forecast database contains no snapshot yet. Run the ingestion pipeline."
    ),
    wq.SnapshotStatus.INCOMPLETE: (
        "The forecast snapshot is incomplete — it is not the full six Regions "
        "× seven Forecast Days."
    ),
}


def create_app(
    db_path: str | Path | None = None,
    observation_service: observation.LatestObservationService | None = None,
) -> Flask:
    """Build the dashboard Flask app, reading ``data.db`` through the shared module.

    ``db_path`` defaults to the snapshot beside the shared module (the packaged
    ``data.db``) and is overridable so tests can point the app at alternative
    databases for the 503 states (R-SHR-3, AC-10). The path is resolved by
    :mod:`weather_query` relative to source, never the process working directory.

    ``observation_service`` defaults to a :class:`observation.LatestObservationService`
    reading the process environment; tests inject one with a controllable clock
    and a simulated upstream.
    """
    app = Flask(
        __name__,
        static_folder=str(_STATIC_DIR),
        static_url_path="/static",
    )
    app.config["DB_PATH"] = (
        wq.DEFAULT_DB_PATH if db_path is None else Path(db_path)
    )

    latest_observation_service = (
        observation.LatestObservationService()
        if observation_service is None
        else observation_service
    )

    def _db() -> str | Path:
        return app.config["DB_PATH"]

    def _snapshot_unavailable(status: wq.SnapshotStatus):
        """Return a 503 JSON response describing why the snapshot is unavailable."""
        reason = status.value  # "missing" / "empty" / "incomplete"
        message = _UNAVAILABLE_REASON.get(status, "The forecast snapshot is unavailable.")
        return (
            jsonify(status="unavailable", reason=reason, error=message),
            503,
        )

    # --- page and static assets ------------------------------------------------

    @app.get("/")
    def index():
        """Serve the dashboard page (``Taiwan Weather Forecast``)."""
        return send_from_directory(_STATIC_DIR, "index.html")

    # --- health (DR-7 / R-DS-2) ------------------------------------------------

    @app.get("/api/health")
    def health():
        """Report snapshot availability: 200 when ok, 503 otherwise."""
        status = wq.snapshot_status(_db())
        if status is not wq.SnapshotStatus.OK:
            return _snapshot_unavailable(status)
        return jsonify(
            status="ok",
            region_count=len(wq.region_list()),
            forecast_day_count=len(wq.forecast_days(_db())),
            ingestion_time=wq.last_ingestion_time(_db()),
        )

    # --- data endpoints (R-DS-3) -----------------------------------------------

    @app.get("/api/regions")
    def regions():
        """Return the six Region names in the fixed canonical order (R-SHR-2(b))."""
        status = wq.snapshot_status(_db())
        if status is not wq.SnapshotStatus.OK:
            return _snapshot_unavailable(status)
        return jsonify(regions=list(wq.region_list()))

    @app.get("/api/regions/<region>/series")
    def region_series(region: str):
        """Return one Region's seven-day series, ascending (R-SHR-2(c))."""
        status = wq.snapshot_status(_db())
        if status is not wq.SnapshotStatus.OK:
            return _snapshot_unavailable(status)
        if region not in wq.region_list():
            return (
                jsonify(error=f"Unknown Region: {region!r} is not one of the six Regions."),
                404,
            )
        series = wq.region_series(region, _db())
        return jsonify(region=region, series=series)

    @app.get("/api/days")
    def days():
        """Return the seven Forecast Day dates, ascending (R-SHR-2(e))."""
        status = wq.snapshot_status(_db())
        if status is not wq.SnapshotStatus.OK:
            return _snapshot_unavailable(status)
        return jsonify(days=wq.forecast_days(_db()))

    @app.get("/api/days/<date>")
    def day_values(date: str):
        """Return the six Regions' values for one Forecast Day (R-SHR-2(d)).

        Each entry carries the Derived Map Temperature and its colour band
        (R-SHR-4). An unknown date yields 404.
        """
        status = wq.snapshot_status(_db())
        if status is not wq.SnapshotStatus.OK:
            return _snapshot_unavailable(status)
        if date not in wq.forecast_days(_db()):
            return (
                jsonify(error=f"Unknown Forecast Day: {date!r} is not in the snapshot."),
                404,
            )
        values = [
            {
                "regionName": v.region_name,
                "mint": v.mint,
                "maxt": v.maxt,
                "derivedMapTemperature": v.derived_map_temperature,
                "colourBand": v.colour_band,
            }
            for v in wq.day_values(date, _db())
        ]
        return jsonify(date=date, values=values)

    # --- V2 Latest Observation (SPEC-V2 R-V2-OBS-1..13, Issue #35) -------------

    @app.get("/api/observations/latest")
    def latest_observation():
        """Return the normalised Latest Observation, or a classified failure.

        Success is 200; the four failure reasons are non-2xx JSON with ``reason``
        and ``error``. ``Cache-Control: no-store`` keeps any intermediary cache
        from reusing the body beyond the server's own reuse window (R-V2-OBS-9).
        """
        status, body = latest_observation_service.latest()
        response = jsonify(body)
        response.status_code = status
        response.headers["Cache-Control"] = "no-store"
        return response

    return app


# Module-level application object for the Vercel entry point (api/index.py) and
# for ``flask run``. Tests build their own app via ``create_app(db_path=...)``.
app = create_app()


if __name__ == "__main__":
    # Local run: ``python server.py``. Vercel does not execute this block; it
    # imports ``app`` through api/index.py and gets CWA_API_KEY from the project
    # environment. Locally the key comes only from the unit's untracked .env
    # (R-V2-SEC-3(b)); the value is never printed.
    observation.load_local_env(Path(__file__).resolve().parent / ".env")
    app.run(host="127.0.0.1", port=5000, debug=False)
