"""Static guards for the Radar overlay frontend (SPEC-V2 §2.7; Issue #40).

Offline and browser-free, like the other ``*_frontend.py`` tests: they read the
frontend source text. The reproducible browser check is
``tests/check_radar_browser.py``. They lock:

* the control (R-V2-RAD-3, DV-12): a real button with a visible text label that
  states its state, hidden by default, only in the Now panel; no automatic
  update — the radar is fetched only by showing it or by Refresh while shown;
* the source (R-V2-RAD-2, R-V2-SEC-1/4, INV-V2-3): the image and its radar time
  come only from ``fetch("/api/radar/latest")`` (one response); the image is put
  on the map from a same-origin object URL of that response — no image overlay,
  tile layer or other request target;
* the radar time (R-V2-RAD-4, H-3): labelled "Radar Time", apart from the
  Observation Time and the Fetched Time; its own stale / unavailable state that
  never touches the observation state, and vice versa (R-V2-DEG-4, INV-V2-7);
* the drawing order (R-V2-RAD-6): backdrop < radar < county interaction layer <
  station markers, the radar pane never taking the pointer;
* the alignment (R-V2-RAD-5, AC-V2-19) as automated geometric evidence: the
  strip placement in ``createRadarLayer`` is recomputed here with the Web
  Mercator formulas for every image row at every zoom of the map (6..12) — every
  pixel within 1 km (in fact within 0.02 km) of its projected position — while
  the same computation for one strip (a plain image overlay) is off by ~3.8 km,
  so the check discriminates. The browser check measures the same thing in the
  rendered page.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import pytest

import radar
from tests.test_map_frontend import _function_body, _strip_comments

_UNIT_DIR = Path(__file__).resolve().parent.parent
_STATIC = _UNIT_DIR / "static"
_JS = (_STATIC / "app.js").read_text(encoding="utf-8")
_CSS = (_STATIC / "styles.css").read_text(encoding="utf-8")
_HTML = (_STATIC / "index.html").read_text(encoding="utf-8")
_LEAFLET_CSS = (_STATIC / "vendor" / "leaflet.css").read_text(encoding="utf-8")

EARTH_M = 40075016.686


def _body(name: str) -> str:
    return _strip_comments(_function_body(_JS, name))


def _code() -> str:
    return _strip_comments(_JS)


def _num(name: str) -> float:
    m = re.search(r"var " + name + r" = (\d+(?:\.\d+)?);", _JS)
    assert m, f"{name} not found"
    return float(m.group(1))


def _extent() -> dict[str, float]:
    m = re.search(r"var RADAR_EXTENT = \{ west: ([\d.]+), east: ([\d.]+), south: ([\d.]+), north: ([\d.]+) \};", _JS)
    assert m, "RADAR_EXTENT not found"
    return dict(zip(("west", "east", "south", "north"), map(float, m.groups())))


# --- the control (R-V2-RAD-3, DV-12) ----------------------------------------------------


def test_radar_control_is_a_labelled_button_hidden_by_default() -> None:
    m = re.search(r'<button type="button" id="radar-toggle" class="btn btn--radar" '
                  r'aria-pressed="false" aria-controls="radar-info">Radar: Off</button>', _HTML)
    assert m, "the radar control must be a real button reading 'Radar: Off'"
    assert re.search(r'<div id="radar-info" class="radar-info" data-radar-state="off" hidden>', _HTML)
    assert "var radarOn = false;" in _JS
    render = _body("renderRadar")
    assert 'setAttribute("aria-pressed", radarOn ? "true" : "false")' in render
    assert 'radarOn ? "Radar: On" : "Radar: Off"' in render
    assert "els.radarInfo.hidden = !radarOn;" in render


def test_radar_control_lives_only_in_the_now_panel() -> None:
    panel = _HTML[_HTML.index('<div id="now-panel"'):_HTML.index('<div id="forecast-panel"')]
    assert 'id="radar-toggle"' in panel and 'id="radar-info"' in panel
    assert 'data-mode="now"' in _HTML[_HTML.index('<div id="now-panel"'):][:200]
    forecast = _HTML[_HTML.index('<div id="forecast-panel"'):_HTML.index('<div id="map-frame"')]
    assert "radar" not in forecast.lower()
    assert "if (mode !== MODE_NOW) return;" in _body("toggleRadar")
    assert "mode === MODE_NOW && appliedMode === MODE_NOW && radarOn && !!radarShown" in _body("syncRadarLayer")
    assert "syncRadarLayer();" in _body("syncMap")


def test_radar_is_fetched_only_by_a_user_action_never_by_a_timer() -> None:
    code = _code()
    assert "setInterval(" not in code
    calls = re.findall(r"\bloadRadar\(\)", code)
    # the definition, showing the radar, and Refresh while it is shown
    assert len(calls) == 3, calls
    assert "if (radarOn) loadRadar();" in _body("toggleRadar")
    assert re.search(r'refreshButton\.addEventListener\("click", function \(\) \{\s*loadObservation\(\);'
                     r'\s*if \(radarOn\) loadRadar\(\);', code)
    assert 'radarToggle.addEventListener("click", toggleRadar)' in code
    assert "setTimeout(" not in _body("loadRadar")
    assert "if (radarInFlight) return;" in _body("loadRadar")


def test_client_bound_between_server_bound_and_instrument() -> None:
    bound = _num("RADAR_TIMEOUT_MS") / 1000
    assert radar.UPSTREAM_DEADLINE_SECONDS < bound < 30
    request = _body("requestRadar")
    assert "controller.abort()" in request and "RADAR_TIMEOUT_MS" in request
    assert "if (settled) return;" in request


# --- the source: only /api/, one response (R-V2-RAD-2, RAD-4, SEC-1/4) -----------------


def test_image_and_radar_time_come_from_one_api_response() -> None:
    request = _body("requestRadar")
    assert 'fetch("/api/radar/latest"' in request
    assert 'response.headers.get("X-Radar-Time")' in request
    assert "response.blob()" in request
    assert re.search(r"/\^image\\/png\\b/i\.test\(type\)", request)
    decode = _body("decodeRadar")
    assert "URL.createObjectURL(result.blob)" in decode
    assert "probe.naturalWidth === RADAR_PIXELS && probe.naturalHeight === RADAR_PIXELS" in decode
    code = _code()
    assert "L.imageOverlay(" not in code and "L.tileLayer(" not in code
    assert code.count("/api/radar/latest") == 1


def test_the_layer_only_ever_shows_the_object_url_of_that_response() -> None:
    layer = _body("createRadarLayer")
    assert re.findall(r"\.src = (\w+(?:\.\w+)?);", layer) == ["url", "this._url"]
    assert "radarLayer.setUrl(radarShown.url);" in _body("syncRadarLayer")
    assert "radarShown = { url: result.url," in _body("applyRadar")


def test_failures_show_fixed_texts_only() -> None:
    classify = _body("classifyRadarFailure")
    assert "body.reason" in classify and "body.error" not in classify and "text" not in classify.replace(
        "text ? JSON.parse(text) : null", "")
    for reason in radar.FAILURE_REASONS:
        assert re.search(r"\b" + reason + r': "', _JS[_JS.index("var RADAR_FAILURE_TEXT"):])
    assert "OBS_SERVER_REASONS.indexOf(body.reason) >= 0" in classify


# --- radar time and independent state (R-V2-RAD-4, DEG-4, H-3) -------------------------


def test_radar_time_is_labelled_apart_from_the_observation_times() -> None:
    info = _HTML[_HTML.index('<div id="radar-info"'):]
    info = info[:info.index("</div>\n          </div>")]
    assert "<dt>Radar Time</dt>" in info and 'id="radar-time"' in info
    assert "Observation Time" not in info and "Fetched Time" not in info
    times = _HTML[_HTML.index('<dl class="obs-times">'):_HTML.index("</dl>")]
    assert "Radar" not in times
    assert "els.radarTime.textContent = radarShown ? formatObsTime(radarShown.radarTime, false) : MISSING;" \
        in _body("renderRadar")


def test_radar_state_is_its_own_and_stale_keeps_the_image() -> None:
    failure = _body("applyRadarFailure")
    assert 'radarState = radarShown ? "stale" : "unavailable";' in failure
    assert "radarShown =" not in failure  # a failure never drops the image shown
    for fn in ("applyRadar", "applyRadarFailure", "loadRadar", "toggleRadar", "renderRadar", "syncRadarLayer"):
        body = _body(fn)
        assert "obsState" not in body and "obsFailure" not in body and "obs =" not in body, fn
    for fn in ("applyObservation", "applyObservationFailure", "loadObservation", "renderObsState"):
        assert "radar" not in _body(fn).lower(), fn
    render = _body("renderRadar")
    assert "Radar Stale" in render and "Radar unavailable" in render


def test_an_older_radar_time_never_replaces_the_one_shown() -> None:
    body = _body("applyRadar")
    assert "instant(result.radarTime) < instant(radarShown.radarTime)" in body
    assert body.index("URL.revokeObjectURL(result.url)") < body.index("radarShown = {")


# --- drawing order (R-V2-RAD-6) ------------------------------------------------------------


def _leaflet_z(pane: str) -> int:
    m = re.search(r"\.leaflet-" + pane + r"-pane\s*\{ z-index: (\d+); \}", _LEAFLET_CSS)
    assert m, pane
    return int(m.group(1))


def test_radar_is_above_the_backdrop_and_below_counties_and_markers() -> None:
    init = _body("initMap")
    backdrop = int(re.search(r'map\.createPane\("backdrop"\)\.style\.zIndex = (\d+);', init).group(1))
    radar_z = int(re.search(r"radarPane\.style\.zIndex = (\d+);", init).group(1))
    assert _leaflet_z("tile") < backdrop < radar_z < _leaflet_z("overlay") < _leaflet_z("marker")
    assert 'radarPane.style.pointerEvents = "none";' in init
    assert init.count('pane: "backdrop",') == 2  # the coastline context and the Taiwan polygons
    assert init.index('createPane("backdrop")') < init.index("L.geoJSON(basemap.context")
    # the county interaction layer stays in Leaflet's overlay pane, above the radar
    assert "pane:" not in _body("buildCountyLayer")
    assert 'options: { pane: "radar" }' in _body("createRadarLayer")
    assert re.search(r"\.radar-layer__img \{[^}]*pointer-events: none;", _CSS)
    assert re.search(r"\.radar-layer__img \{[^}]*max-width: none !important;", _CSS)


# --- alignment: geometric evidence for R-V2-RAD-5 / AC-V2-19 ---------------------------


def test_frontend_geometry_is_the_server_checked_product() -> None:
    assert _extent() == radar.EXTENT
    assert (_num("RADAR_PIXELS"), _num("RADAR_PIXELS")) == radar.IMAGE_SIZE


def _mercator_y(lat: float, z: int) -> float:
    s = math.sin(math.radians(lat))
    return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * 256 * 2 ** z


def _km_per_px(lat: float, z: int) -> float:
    return EARTH_M * math.cos(math.radians(lat)) / (256 * 2 ** z) / 1000


def _max_row_error_km(strips: int, z: int) -> tuple[float, float]:
    """Largest distance between where the layer draws an image row and where the
    map projects that row's latitude — the ``_reset`` placement recomputed: strip
    k spans the projected y of its edge latitudes, its rows filled linearly; each
    screen row belongs to the strip whose (rounded) box holds it, so a row may be
    drawn by its neighbour's fill for up to half a pixel. Returns (km, latitude)."""
    e = _extent()
    n_px = int(_num("RADAR_PIXELS"))
    rows = n_px / strips
    step = (e["north"] - e["south"]) / strips
    y_nw = _mercator_y(e["north"], z)
    edges = [(_mercator_y(e["north"] - k * step, z) - y_nw) for k in range(strips + 1)]
    boxes = [(round(edges[k]), round(edges[k + 1])) for k in range(strips)]
    worst = (0.0, 0.0)
    for r in range(n_px):
        lat = e["north"] - (r + 0.5) * (e["north"] - e["south"]) / n_px
        true_y = _mercator_y(lat, z) - y_nw
        for k in range(strips):
            y0, y1 = edges[k], edges[k + 1]
            drawn = y0 + (r + 0.5 - k * rows) / rows * (y1 - y0)
            top, bottom = boxes[k]
            if top - 0.5 <= drawn <= bottom + 0.5:  # this strip's box may show the row
                err = abs(drawn - true_y) * _km_per_px(lat, z)
                if err > worst[0]:
                    worst = (err, lat)
    return worst


def test_layer_uses_the_strip_placement_recomputed_here() -> None:
    reset = _function_body(_JS, "createRadarLayer")
    reset = _strip_comments(reset[reset.index("_reset: function"):reset.index("_animateZoom:")])
    for fragment in (
        "var step = (e.north - e.south) / RADAR_STRIPS;",
        "var y0 = y(e.north - k * step) - nw.y;",
        "var y1 = y(e.north - (k + 1) * step) - nw.y;",
        "var top = Math.round(y0);",
        "var bottom = Math.round(y1);",
        'strip.height = (bottom - top) + "px";',
        'img.height = ((y1 - y0) * RADAR_STRIPS) + "px";',
        'img.top = (y0 - k * (y1 - y0) - top) + "px";',
        'img.width = width + "px";',
        "var width = m.project(L.latLng(e.north, e.east), z).x - origin.x - nw.x;",
        "L.DomUtil.setPosition(this._el, nw);",
    ):
        assert fragment in reset, fragment
    assert "m.project(L.latLng(lat, e.west), z).y - origin.y" in reset


@pytest.mark.parametrize("zoom", [6, 7, 8, 9, 10, 11, 12])
def test_every_image_row_lands_within_1_km_of_its_projected_latitude(zoom) -> None:
    strips = int(_num("RADAR_STRIPS"))
    error_km, _lat = _max_row_error_km(strips, zoom)
    assert error_km <= 1.0, f"zoom {zoom}: {error_km:.3f} km"
    assert error_km <= 0.05  # the strip layer's actual margin (~0.01 km + rounding)


def test_a_plain_image_overlay_would_fail_the_oracle() -> None:
    """The DA's figure: one strip (a linear stretch between the projected corners)
    misplaces mid-image rows by ~3.8 km — the recomputation above detects it."""
    error_km, lat = _max_row_error_km(1, 10)
    assert 3.5 < error_km < 4.1 and 22.5 < lat < 24.5, (error_km, lat)


def test_longitude_is_linear_so_columns_are_exact() -> None:
    """Across, Web Mercator x is linear in longitude: the image stretched between
    the projected west and east edges puts every column where the map projects it."""
    e = _extent()
    z = 10
    def x(lon: float) -> float:
        return (lon + 180) / 360 * 256 * 2 ** z
    width = x(e["east"]) - x(e["west"])
    for c in (0, 1, 1799, 3598, 3599):
        lon = e["west"] + (c + 0.5) * (e["east"] - e["west"]) / 3600
        drawn = (c + 0.5) / 3600 * width
        assert abs(drawn - (x(lon) - x(e["west"]))) < 1e-6
