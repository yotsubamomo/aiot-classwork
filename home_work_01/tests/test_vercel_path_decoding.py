"""Regression guard for the Vercel un-decoded PATH_INFO defect (#21 F-1).

Vercel delivers ``PATH_INFO`` to the WSGI app still percent-encoded, so a Chinese
Region name reaches Flask as ``%E4%B8%AD...`` and every
``/api/regions/<Region>/series`` returned 404 on the live deployment (the page
showed "That Region is not available…" with an empty table) while the Flask test
client — which decodes the path — stayed green. See ``api/index.py``.

These tests exercise the **deployed** WSGI callable (``api/index.py``'s ``app``)
with an encoded ``PATH_INFO`` exactly as Vercel sends it, bypassing the Flask test
client on purpose. Removing the entry point's decoding middleware makes
``test_encoded_region_series_is_200`` fail, and ``test_plain_app_404s_without_fix``
shows the plain app (no middleware) still 404s — so the middleware is provably
what fixes it. Fully offline: reads only the committed ``data.db`` (R-TC-5).
"""

from __future__ import annotations

import importlib.util
import json
from io import BytesIO
from pathlib import Path
from urllib.parse import quote

import pytest

import weather_query as wq

_UNIT_DIR = Path(__file__).resolve().parent.parent
_DATA_DB = _UNIT_DIR / "data.db"


def _load_vercel_app():
    """Load ``api/index.py``'s ``app`` — the exact WSGI callable Vercel invokes."""
    path = _UNIT_DIR / "api" / "index.py"
    spec = importlib.util.spec_from_file_location("hw01_api_index", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.app


def _wsgi_get(app, path_info: str) -> tuple[int, bytes]:
    """Call a WSGI app with a raw, undecoded ``PATH_INFO`` (as Vercel delivers it).

    The Flask/Werkzeug test client decodes the path, so it cannot reproduce the
    Vercel behaviour; driving the WSGI callable directly can.
    """
    captured: dict[str, str] = {}

    def start_response(status, headers, exc_info=None):
        captured["status"] = status

    environ = {
        "REQUEST_METHOD": "GET",
        "SCRIPT_NAME": "",
        "PATH_INFO": path_info,
        "QUERY_STRING": "",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "http",
        "wsgi.input": BytesIO(b""),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
    }
    body = b"".join(app(environ, start_response))
    status_code = int(captured["status"].split(" ", 1)[0])
    return status_code, body


def _encoded_series_path(region: str) -> str:
    # The same encoding the browser's encodeURIComponent produces for these names.
    return "/api/regions/" + quote(region, safe="") + "/series"


@pytest.fixture(scope="module")
def vercel_app():
    return _load_vercel_app()


@pytest.mark.parametrize("region", list(wq.REGION_ORDER))
def test_encoded_region_series_is_200(vercel_app, region: str) -> None:
    """Every Region's encoded /series path resolves to 200 with data.db values."""
    status, body = _wsgi_get(vercel_app, _encoded_series_path(region))
    assert status == 200, f"{region}: encoded PATH_INFO must resolve (F-1)"
    payload = json.loads(body)
    assert payload["region"] == region
    series = payload["series"]
    assert len(series) == wq.DAYS_REQUIRED
    shared = wq.region_series(region, _DATA_DB)
    assert [(r["dataDate"], r["mint"], r["maxt"]) for r in series] == [
        (r["dataDate"], r["mint"], r["maxt"]) for r in shared
    ]


def test_plain_app_404s_without_fix() -> None:
    """The bug is real: the plain Flask app (no entry-point middleware) 404s on the
    encoded path, so the middleware is what makes the parametrized test pass."""
    from server import create_app

    status, body = _wsgi_get(create_app(), _encoded_series_path("中部地區"))
    assert status == 404
    assert b"%E4%B8%AD" in body  # the encoded segment reached the view undecoded


def test_ascii_and_encoded_day_paths_both_resolve(vercel_app) -> None:
    """/api/days/<date>: ASCII dates already work; an encoded date must too."""
    date = wq.forecast_days(_DATA_DB)[0]
    status_ascii, _ = _wsgi_get(vercel_app, "/api/days/" + date)
    assert status_ascii == 200
    status_encoded, body = _wsgi_get(vercel_app, "/api/days/" + quote(date, safe=""))
    assert status_encoded == 200
    assert json.loads(body)["date"] == date


def test_ascii_paths_unaffected(vercel_app) -> None:
    """The middleware leaves plain ASCII paths (no percent-escape) untouched."""
    status, body = _wsgi_get(vercel_app, "/api/health")
    assert status == 200
    assert json.loads(body)["status"] == "ok"
