"""Reproducible browser check for Issue #40 (Radar overlay).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the convention of ``check_modes_browser.py``, whose
DevTools driver it reuses). It runs the *unmodified* ``server.create_app``
in-process on loopback (threaded), with the root logger at ``DEBUG`` captured, and
a **sentinel** ``CWA_API_KEY`` that must never reach the browser or the log (H-1).

Both CWA services are the real ``observation.LatestObservationService`` and
``radar.RadarService`` with simulated upstreams (no key, no network, R-V2-TC-3):

* observation — the committed sanitised O-A0001-001 sample (or a connection error);
* radar metadata — the committed sanitised O-A0058-006 metadata sample with its
  ``DateTime`` moved per variant, or one of the four failure classes (a
  connection error whose message carries the host and the key, HTTP 403 / 500
  with a marker in the body, non-JSON with a marker, a stall);
* radar image — by default a **synthetic test pattern**: a transparent 3600×3600
  PNG with opaque squares centred on known pixels (the product corners, edge
  midpoints and centre, points on the main island and every whole degree), so
  where each pixel is drawn can be measured; ``--real-image PATH`` adds a session
  with a real O-A0058-006 image for the screenshots.

A platform layer in front of the app can answer the radar path with an HTML 502 or
hold it past the page's own time bound. A page hook (``L.Map.addInitHook``, no app
change) exposes the Leaflet map so the check can read ``latLngToContainerPoint``.

Checks: AC-V2-18 (control, default hidden, keyboard, overlay on/off, radar time
labelled and apart from Observation Time / Fetched Time, re-fetch triggers, no
polling, failure → unavailable / stale, observation untouched, drawing order and
map still draggable / zoomable / county- and station-selectable, markers readable,
Forecast mode without radar); AC-V2-19 (every reference pixel's drawn position vs
the map's projection of its latitude / longitude at zoom 7 and 10, from the DOM
geometry of the drawn image AND from the rendered pixels, plus the same
measurement for a plain image overlay to show the instrument discriminates);
AC-V2-09(c) (radar failure changes only the radar; observation failure leaves the
radar); AC-V2-09(a) radar part (forecast snapshot 503 → Now mode radar works);
AC-V2-16 (network log: zero external requests; the image request is ``/api/``);
AC-V2-07 radar / H-1 (no key, upstream host or upstream body in the page, console,
responses or server log); 375 px (no horizontal scroll, 44×44 control).

Optional ``--coastline PATH`` (a CWA O-A0058-003 image, which draws coastlines and
county borders; public product image, obtained separately) adds (a) screenshots
of that image placed by the same layer over the app's own basemap and (b) a
numeric data-fact check that the product really is the equal-angle grid over
lon 118–124 / lat 20.5–26.5 (the border pixels vs the vendored MOI county
polygons, with trial shifts ±2.5 km).

Usage (from the unit directory, venv active, ``data.db`` present)::

    python tests/check_radar_browser.py
    python tests/check_radar_browser.py --real-image O-A0058-006.png --coastline O-A0058-003.png
    python tests/check_radar_browser.py --out <dir>

Exit code 0 means every check passed. Evidence in ``--out`` (default
``doc/acceptance/screenshots/v2/issue-40/``): PNG screenshots,
``browser-check-results.json``, ``alignment.json`` and ``network-log.json``.
"""

from __future__ import annotations

import argparse
import copy
import io
import json
import logging
import math
import re
import struct
import sys
import threading
import time
import zlib
from collections import deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

import requests  # noqa: E402
from PIL import Image  # noqa: E402

import observation as obs  # noqa: E402
import radar  # noqa: E402
from server import create_app  # noqa: E402
from tests.check_modes_browser import (  # noqa: E402
    JS_HELPERS, Browser, Checks, _QuietHandler, find_chrome, fmt_time,
)

OBS_SAMPLE = _UNIT_DIR / "tests" / "fixtures" / "O-A0001-001_sample.json"
META_SAMPLE = _UNIT_DIR / "tests" / "fixtures" / "O-A0058-006_metadata_sample.json"
DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "v2" / "issue-40"
RADAR_PATH = "/api/radar/latest"
OBS_PATH = "/api/observations/latest"
TAIPEI_TZ = timezone(timedelta(hours=8))

SENTINEL_KEY = "SENTINEL-KEY-issue40-must-never-leak"
UPSTREAM_MARKER = "UPSTREAM-BODY-MARKER-issue40"
PLATFORM_MARKER = "PLATFORM-PAGE-MARKER-issue40"
UPSTREAM_HOSTS = ("opendata.cwa.gov.tw", "cwaopendata.s3.ap-northeast-1.amazonaws.com")
LEAKS = (SENTINEL_KEY, UPSTREAM_MARKER, *UPSTREAM_HOSTS, "Authorization", "ProductURL")
FORBIDDEN_WORDS = re.compile(r"\b(real-?time|live)\b", re.IGNORECASE)

E = radar.EXTENT
P = radar.IMAGE_SIZE[0]
KM_EARTH = 40075.016686
INSTRUMENT_S = 30.0
RADAR_TIMES = {"t0": "2026-09-26T14:30:00+08:00", "t1": "2026-09-26T14:40:00+08:00",
               "t2": "2026-09-26T14:50:00+08:00", "t3": "2026-09-26T15:00:00+08:00"}

# AC-V2-19 reference points: the product's four corners, four edge midpoints and
# centre, and points on the main island (and 澎湖 / 金門).
REF_POINTS = [
    ("corner NW", 26.5, 118.0), ("corner NE", 26.5, 124.0),
    ("corner SW", 20.5, 118.0), ("corner SE", 20.5, 124.0),
    ("edge N", 26.5, 121.0), ("edge S", 20.5, 121.0),
    ("edge W", 23.5, 118.0), ("edge E", 23.5, 124.0), ("centre", 23.5, 121.0),
    ("臺北", 25.04, 121.51), ("臺中", 24.15, 120.67), ("恆春", 22.00, 120.75),
    ("花蓮", 23.98, 121.60), ("澎湖 馬公", 23.57, 119.58), ("金門", 24.43, 118.32),
]
# Whole-degree points inside the product (squares for the rendered measurement).
GRID_POINTS = [(f"{lat}N {lon}E", float(lat), float(lon)) for lat in range(21, 27) for lon in range(119, 124)]
SQUARE_HALF = 12  # the pattern squares are 25 × 25 source pixels (≈ 4.6 km)


def pixel_of(lat: float, lon: float) -> tuple[int, int]:
    """The product pixel (column, row) holding (lat, lon): equal-angle grid, edge convention."""
    c = min(P - 1, max(0, math.floor((lon - E["west"]) / (E["east"] - E["west"]) * P)))
    r = min(P - 1, max(0, math.floor((E["north"] - lat) / (E["north"] - E["south"]) * P)))
    return c, r


def km_per_px(lat: float, z: float) -> float:
    return KM_EARTH * math.cos(math.radians(lat)) / (256 * 2 ** z)


# --- the synthetic test pattern -----------------------------------------------------------


def pattern_png() -> bytes:
    """Transparent 3600×3600 RGBA PNG with opaque squares centred on the pixels of
    REF_POINTS (cyan) and GRID_POINTS (magenta); corner / edge squares are clipped
    by the image edge. Pure Python (zlib)."""
    stride = 1 + 4 * P
    buf = bytearray(stride * P)
    def square(c, r, rgba):
        x0, x1 = max(0, c - SQUARE_HALF), min(P, c + SQUARE_HALF + 1)
        fill = bytes(rgba) * (x1 - x0)
        for y in range(max(0, r - SQUARE_HALF), min(P, r + SQUARE_HALF + 1)):
            base = y * stride + 1
            buf[base + 4 * x0: base + 4 * x1] = fill
    for _n, lat, lon in GRID_POINTS:
        square(*pixel_of(lat, lon), (255, 0, 255, 255))
    for _n, lat, lon in REF_POINTS:
        square(*pixel_of(lat, lon), (0, 255, 255, 255))
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))
    ihdr = struct.pack(">IIBBBBB", P, P, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(buf), 6))
            + chunk(b"IEND", b""))


# --- simulated upstreams, clock, platform ---------------------------------------------------


class _Resp:
    def __init__(self, status: int, content: bytes) -> None:
        self.status_code, self.content = status, content

    def iter_content(self, chunk_size=65536):
        for i in range(0, len(self.content), chunk_size):
            yield self.content[i:i + chunk_size]

    def close(self) -> None:
        pass


class RadarUpstream:
    """``requests.get`` stand-in for the radar metadata + image requests."""

    def __init__(self, image: bytes) -> None:
        self.meta = json.loads(META_SAMPLE.read_text(encoding="utf-8"))
        self.image = image
        self.mode = "ok"
        self.variant = "t1"
        self.status = 200
        self.calls: list[dict] = []

    def __call__(self, url, headers=None, params=None, timeout=None, stream=False):
        self.calls.append({"url": url, "has_key": SENTINEL_KEY in json.dumps(headers or {})})
        key = (headers or {}).get("Authorization", "")
        metadata = "/fileapi/" in url
        if self.mode == "stall" and metadata:
            time.sleep(40)
        if self.mode == "unreachable" and metadata:
            raise requests.ConnectionError(
                f"HTTPSConnectionPool(host='{UPSTREAM_HOSTS[0]}', port=443): url: /fileapi/v1/opendataapi/"
                f"O-A0058-006?Authorization={key} ({UPSTREAM_MARKER})")
        if self.mode == "http" and metadata:
            return _Resp(self.status, json.dumps({"message": f"{UPSTREAM_MARKER} {key}"}).encode())
        if self.mode == "image_http" and not metadata:
            return _Resp(self.status, f"<Error>{UPSTREAM_MARKER}</Error>".encode())
        if self.mode == "nonjson" and metadata:
            return _Resp(200, f"<html>{UPSTREAM_MARKER} {key}</html>".encode())
        if metadata:
            data = copy.deepcopy(self.meta)
            data["cwaopendata"]["dataset"]["DateTime"] = RADAR_TIMES[self.variant]
            return _Resp(200, json.dumps(data, ensure_ascii=False).encode("utf-8"))
        return _Resp(200, self.image)


class ObsUpstream:
    def __init__(self) -> None:
        self.payload = OBS_SAMPLE.read_bytes()
        self.fail = False

    def __call__(self, url, headers=None, params=None, timeout=None):
        if self.fail:
            raise requests.ConnectionError(f"{UPSTREAM_HOSTS[0]} {UPSTREAM_MARKER}")
        return _Resp(200, self.payload)


class Clock:
    def __init__(self) -> None:
        self.now = datetime(2026, 9, 26, 14, 45, 0, tzinfo=TAIPEI_TZ)

    def __call__(self) -> datetime:
        return self.now

    def advance(self) -> None:
        self.now += timedelta(seconds=radar.REUSE_WINDOW_SECONDS + 1)


class Platform:
    def __init__(self, app) -> None:
        self.app, self.mode = app, None

    def __call__(self, environ, start_response):
        if environ.get("PATH_INFO") == RADAR_PATH and self.mode:
            if self.mode == "html502":
                start_response("502 Bad Gateway", [("Content-Type", "text/html; charset=utf-8")])
                return [f"<html><body>502 Bad Gateway {PLATFORM_MARKER}</body></html>".encode()]
            if self.mode == "hang":
                time.sleep(25)
        return self.app(environ, start_response)


class _ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


LOG = io.StringIO()


class Rig:
    def __init__(self, image: bytes, db_path=None) -> None:
        self.radar_up = RadarUpstream(image)
        self.obs_up = ObsUpstream()
        self.clock = Clock()
        self.obs_clock = Clock()
        self.env = {"CWA_API_KEY": SENTINEL_KEY}
        app = create_app(
            db_path=db_path,
            observation_service=obs.LatestObservationService(
                env=self.env, http_get=self.obs_up, clock=self.obs_clock, reuse_window_seconds=0),
            radar_service=radar.RadarService(env=self.env, http_get=self.radar_up, clock=self.clock),
        )
        app.debug = True
        self.platform = Platform(app)
        self.server = make_server("127.0.0.1", 0, self.platform, server_class=_ThreadingWSGIServer,
                                  handler_class=_QuietHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def radar_next(self, mode="ok", variant=None, status=200, key=True, platform=None) -> None:
        """Configure the next radar request (past the server's reuse window)."""
        self.clock.advance()
        self.radar_up.mode, self.radar_up.status = mode, status
        if variant:
            self.radar_up.variant = variant
        if key:
            self.env["CWA_API_KEY"] = SENTINEL_KEY
        else:
            self.env.pop("CWA_API_KEY", None)
        self.platform.mode = platform

    def close(self) -> None:
        self.server.shutdown()


# --- page side ----------------------------------------------------------------------------

# Installed before any page script: exposes the Leaflet map (no app change).
MAP_HOOK = r"""
Object.defineProperty(window, 'L', {configurable: true, get: function () { return undefined; },
  set: function (v) {
    Object.defineProperty(window, 'L', {value: v, writable: true, configurable: true, enumerable: true});
    if (v && v.Map && v.Map.addInitHook) v.Map.addInitHook(function () { window.__map = this; });
  }});
"""

RADAR_STATE_JS = r"""(function () {
  var t = document.getElementById('radar-toggle'), info = document.getElementById('radar-info');
  var layer = document.querySelector('.leaflet-radar-pane .radar-layer');
  var img = layer ? layer.querySelector('img') : null;
  return {
    pressed: t.getAttribute('aria-pressed'), label: t.textContent, toggleVisible: __chk.visible(t),
    state: info.getAttribute('data-radar-state'), busy: info.getAttribute('aria-busy'),
    infoVisible: __chk.visible(info),
    time: document.getElementById('radar-time').textContent,
    status: document.getElementById('radar-status').textContent,
    statusClass: document.getElementById('radar-status').className,
    layer: !!layer, layerVisible: !!layer && __chk.visible(layer.querySelector('.radar-layer__strip')),
    src: img ? img.getAttribute('src') : null,
    strips: layer ? layer.querySelectorAll('.radar-layer__strip').length : 0,
    obsState: document.getElementById('now-panel').getAttribute('data-obs-state'),
    obsTime: document.getElementById('obs-time').textContent,
    obsFetched: document.getElementById('obs-fetched').textContent,
    obsCount: document.getElementById('obs-count').textContent,
    obsStatus: document.getElementById('obs-status').textContent,
    markers: document.querySelectorAll('.station-icon').length,
    mode: document.getElementById('mode-now').getAttribute('aria-pressed') === 'true' ? 'now' : 'forecast',
    scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
  };
})()"""

# DOM geometry of every drawn reference pixel vs the map's projection of it.
MEASURE_JS = r"""(function (points, E, P, naive) {
  var map = window.__map, mr = map.getContainer().getBoundingClientRect();
  var strips = Array.from(document.querySelectorAll('.leaflet-radar-pane .radar-layer__strip'));
  var plain = document.querySelector('.leaflet-radar-pane img.leaflet-image-layer');
  var z = map.getZoom();
  return points.map(function (p) {
    var c = p.c, r = p.r, el, rect;
    if (naive) { el = plain; }  // the check's own plain image overlay (discrimination)
    else {
      var rows = P / strips.length, k = Math.floor(r / rows);
      el = strips[k].querySelector('img');  // the app's strip that draws row r
    }
    rect = el.getBoundingClientRect();
    var drawn = {x: rect.left + (c + 0.5) * rect.width / P - mr.left, y: rect.top + (r + 0.5) * rect.height / P - mr.top};
    var lat = E.north - (r + 0.5) * (E.north - E.south) / P, lon = E.west + (c + 0.5) * (E.east - E.west) / P;
    var api = map.latLngToContainerPoint([lat, lon]);  // Leaflet's API (rounds to whole px)
    var exact = map.layerPointToContainerPoint(map.project(L.latLng(lat, lon), z).subtract(map.getPixelOrigin()));
    return {name: p.name, c: c, r: r, lat: lat, lon: lon, zoom: z, drawn: drawn,
            api: {x: api.x, y: api.y}, exact: {x: exact.x, y: exact.y},
            onScreen: exact.x >= 0 && exact.y >= 0 && exact.x <= mr.width && exact.y <= mr.height};
  });
})"""


class Page:
    def __init__(self, chrome: str, rig: Rig, out: Path, checks: Checks, label: str,
                 width: int, height: int, mobile: bool) -> None:
        self.b = Browser(chrome)
        self.b.send("Page.addScriptToEvaluateOnNewDocument", {"source": MAP_HOOK})
        self.rig, self.out, self.checks, self.label = rig, out, checks, label
        self.width, self.height = width, height
        self.b.viewport(width, height, mobile)

    def open(self) -> None:
        self.b.navigate(self.rig.base + "/")
        self.b.js(JS_HELPERS)
        self.b.wait_for("document.getElementById('now-panel').getAttribute('data-obs-state') !== 'loading' "
                        "&& !!window.__map", 20)
        self.b.pump(0.8)

    def state(self) -> dict:
        return self.b.js(RADAR_STATE_JS)

    def add(self, check_id: str, ok: bool, detail) -> None:
        self.checks.add(f"{self.label} {check_id}", ok, detail)

    def shot(self, name: str) -> None:
        self.b.screenshot(self.out / f"{self.label}-{name}.png")

    def radar_requests(self) -> int:
        return sum(1 for u in self.b.request_urls() if u.endswith(RADAR_PATH))

    def obs_requests(self) -> int:
        return sum(1 for u in self.b.request_urls() if u.endswith(OBS_PATH))

    def wait_radar(self, timeout: float = INSTRUMENT_S + 5) -> dict:
        self.b.wait_for("document.getElementById('radar-info').getAttribute('aria-busy') === 'false' && "
                        "document.getElementById('radar-info').getAttribute('data-radar-state') !== 'loading'",
                        timeout)
        self.b.pump(0.4)
        return self.state()

    def toggle(self, key: str | None = None) -> dict:
        """Operate the radar control: by keyboard (Enter / Space) or a click."""
        if key:
            self.b.js("document.getElementById('radar-toggle').focus(); true")
            self.b.key(key)
        else:
            self.b.js("document.getElementById('radar-toggle').click(); true")
        self.b.pump(0.3)
        return self.wait_radar()

    def refresh(self) -> None:
        self.b.js("document.getElementById('refresh-button').click(); true")
        self.b.pump(0.3)
        self.b.wait_for("document.getElementById('now-panel').getAttribute('aria-busy') === 'false'", 35)
        self.wait_radar()

    def set_view(self, lat: float, lon: float, zoom: int) -> dict:
        self.b.js(f"window.__map.setView([{lat}, {lon}], {zoom}, {{animate: false}}); true")
        self.b.pump(0.5)
        return self.b.js("(function(){var c=__map.getCenter();return {lat:c.lat,lng:c.lng,zoom:__map.getZoom()};})()")

    def mouse(self, kind: str, x: float, y: float, buttons: int = 0) -> None:
        p = {"type": kind, "x": x, "y": y, "button": "left" if kind != "mouseMoved" or buttons else "none",
             "buttons": buttons, "clickCount": 1 if kind != "mouseMoved" else 0}
        self.b.send("Input.dispatchMouseEvent", p)

    def click(self, x: float, y: float) -> None:
        self.mouse("mouseMoved", x, y)
        self.mouse("mousePressed", x, y, 1)
        self.mouse("mouseReleased", x, y, 0)
        self.b.pump(0.6)

    def drag(self, x0: float, y0: float, dx: float, dy: float) -> None:
        self.mouse("mouseMoved", x0, y0)
        self.mouse("mousePressed", x0, y0, 1)
        for i in range(1, 9):
            self.mouse("mouseMoved", x0 + dx * i / 8, y0 + dy * i / 8, 1)
            self.b.pump(0.03)
        self.mouse("mouseReleased", x0 + dx, y0 + dy, 0)
        self.b.pump(0.9)

    def map_rect(self) -> dict:
        return self.b.js("(function(){document.getElementById('map').scrollIntoView({block:'center'});"
                         "var r=document.getElementById('map').getBoundingClientRect();"
                         "return {x:r.left,y:r.top,w:r.width,h:r.height,sx:scrollX,sy:scrollY};})()")

    def capture_map(self) -> tuple[Image.Image, float, float]:
        """The map area of a whole-viewport screenshot (device pixel ratio 1, so
        screenshot pixel (i, j) covers viewport [i, i+1] × [j, j+1]), cropped at
        whole pixels, and the map's fractional offset inside the crop — so a
        position in the crop minus the offset is a map container position."""
        import base64
        self.map_rect()
        self.b.pump(0.3)
        r = self.b.js("(function(){var r=document.getElementById('map').getBoundingClientRect();"
                      "return {x:r.left,y:r.top,w:r.width,h:r.height};})()")
        data = self.b.send("Page.captureScreenshot", {"format": "png"})["data"]
        shot = Image.open(io.BytesIO(base64.b64decode(data))).convert("RGB")
        fx, fy = math.floor(r["x"]), math.floor(r["y"])
        crop = shot.crop((fx, fy, fx + math.ceil(r["w"]), fy + math.ceil(r["h"])))
        return crop, r["x"] - fx, r["y"] - fy

    def close(self) -> None:
        self.b.close()


# --- AC-V2-19 measurement helpers -----------------------------------------------------------


def measure(pg: Page, names=None, points=REF_POINTS, naive: bool = False) -> list[dict]:
    pts = [{"name": n, "c": pixel_of(lat, lon)[0], "r": pixel_of(lat, lon)[1]}
           for n, lat, lon in points if names is None or n in names]
    rows = pg.b.js(f"({MEASURE_JS})({json.dumps(pts)}, {json.dumps(E)}, {P}, {'true' if naive else 'false'})")
    for m in rows:
        kpp = km_per_px(m["lat"], m["zoom"])
        m["kmPerPx"] = kpp
        m["errExactKm"] = math.hypot(m["drawn"]["x"] - m["exact"]["x"], m["drawn"]["y"] - m["exact"]["y"]) * kpp
        m["errApiKm"] = math.hypot(m["drawn"]["x"] - m["api"]["x"], m["drawn"]["y"] - m["api"]["y"]) * kpp
    return rows


def blobs(changed: set[tuple[int, int]]) -> list[dict]:
    """Connected components (8-neighbour) of changed pixels: centroid and size."""
    seen: set[tuple[int, int]] = set()
    out = []
    for start in changed:
        if start in seen:
            continue
        q = deque([start])
        seen.add(start)
        xs = ys = n = 0
        while q:
            x, y = q.popleft()
            xs += x
            ys += y
            n += 1
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nb = (x + dx, y + dy)
                    if nb in changed and nb not in seen:
                        seen.add(nb)
                        q.append(nb)
        out.append({"x": xs / n + 0.5, "y": ys / n + 0.5, "n": n})
    return out


def diff_pixels(on: Image.Image, off: Image.Image) -> set[tuple[int, int]]:
    a, b = on.load(), off.load()
    w, h = on.size
    changed = set()
    for y in range(h):
        for x in range(w):
            p, q = a[x, y], b[x, y]
            if abs(p[0] - q[0]) + abs(p[1] - q[1]) + abs(p[2] - q[2]) > 30:
                changed.add((x, y))
    return changed


def rendered(pg: Page, points, save: str | None = None) -> tuple[list[dict], dict]:
    """Rendered-pixel measurement in the current view: radar visible vs hidden
    (markers and tooltips hidden in both), the changed-pixel blobs' centroids vs
    the projection of each on-screen square's centre."""
    # the map controls are hidden too (WI-UI-POLISH-1): on the wider desktop map a
    # square can lie under the zoom buttons, which would hide it from the capture
    hide = ("document.querySelectorAll('.leaflet-marker-pane, .leaflet-tooltip-pane, .obs-map-state-wrap, "
            ".leaflet-control-container').forEach(function(e){e.style.visibility='hidden'}); true")
    pg.b.js(hide)
    pg.b.pump(0.3)
    on, dx, dy = pg.capture_map()
    pg.b.js("document.querySelector('.leaflet-radar-pane').style.visibility='hidden'; true")
    pg.b.pump(0.3)
    off, _, _ = pg.capture_map()
    pg.b.js("document.querySelector('.leaflet-radar-pane').style.visibility=''; "
            "document.querySelectorAll('.leaflet-marker-pane, .leaflet-tooltip-pane, .obs-map-state-wrap, "
            ".leaflet-control-container').forEach(function(e){e.style.visibility=''}); true")
    if save:
        on.save(pg.out / f"{pg.label}-{save}-radar-on.png")
        off.save(pg.out / f"{pg.label}-{save}-radar-hidden.png")
    changed = diff_pixels(on, off)
    found = blobs(changed)
    ms = measure(pg, None, points)
    # every changed pixel must belong to a square: each blob lies near some
    # square centre (on or off screen), else the image changed the backdrop
    stray = [b for b in found if not any(math.hypot(b["x"] - dx - m["exact"]["x"], b["y"] - dy - m["exact"]["y"]) < 40
                                         for m in ms)]
    out = []
    for m in ms:
        if not m["onScreen"]:
            continue
        ex = m["exact"]
        # the square's own blob: the nearest one within 3 km (a blob of another
        # square is tens of km away at every zoom used here)
        radius = max(6.0, 3.0 / m["kmPerPx"])
        near = [b for b in found if math.hypot(b["x"] - dx - ex["x"], b["y"] - dy - ex["y"]) < radius]
        if not near:
            out.append({"name": m["name"], "zoom": m["zoom"], "found": False, "expected": ex})
            continue
        best = min(near, key=lambda b: math.hypot(b["x"] - dx - ex["x"], b["y"] - dy - ex["y"]))
        cx, cy = best["x"] - dx, best["y"] - dy  # crop pixels -> map container position
        err = math.hypot(cx - ex["x"], cy - ex["y"])
        c, r = m["c"], m["r"]
        whole = SQUARE_HALF <= c < P - SQUARE_HALF and SQUARE_HALF <= r < P - SQUARE_HALF
        out.append({"name": m["name"], "zoom": m["zoom"], "found": True, "wholeSquare": whole,
                    "centroid": {"x": cx, "y": cy}, "expected": ex, "pixels": best["n"],
                    "errPx": err, "errKm": err * m["kmPerPx"]})
    # every changed pixel belongs to a square (non-echo areas leave the backdrop untouched)
    total = on.size[0] * on.size[1]
    return out, {"changed": len(changed), "blobs": len(found), "strayBlobs": len(stray),
                 "largestBlob": max((b["n"] for b in found), default=0), "mapPixels": total}


# --- scenarios ------------------------------------------------------------------------------


def expect_success(st: dict, time_text: str) -> bool:
    return (st["pressed"] == "true" and st["label"] == "Radar: On" and st["state"] == "success"
            and st["infoVisible"] and st["layer"] and st["layerVisible"] and st["time"] == time_text
            and st["strips"] == 24 and (st["src"] or "").startswith("blob:"))


def obs_same(a: dict, b: dict) -> bool:
    return all(a[k] == b[k] for k in ("obsState", "obsTime", "obsFetched", "obsCount", "markers"))


def scenario_main(chrome: str, rig: Rig, out: Path, checks: Checks, record: dict, network: dict) -> None:
    pg = Page(chrome, rig, out, checks, "1280", 1280, 900, False)
    try:
        rig.radar_next("ok", "t1")
        pg.open()
        st0 = pg.state()
        pg.add("AC-V2-18 default: the Radar control is a visible text-labelled button, hidden (Off), no radar request, no layer",
               st0["toggleVisible"] and st0["label"] == "Radar: Off" and st0["pressed"] == "false"
               and st0["state"] == "off" and not st0["infoVisible"] and not st0["layer"]
               and pg.radar_requests() == 0, st0)
        box = pg.b.js("__chk.rect(document.getElementById('radar-toggle'))")
        pg.add("RSP-3 the Radar control is at least 44 x 44", box["w"] >= 44 and box["h"] >= 44, box)
        pg.shot("radar-off")

        # keyboard: Enter shows it
        st = pg.toggle("Enter")
        want = fmt_time(RADAR_TIMES["t1"], False)
        headers = [e["params"]["response"] for e in pg.b.events
                   if e["method"] == "Network.responseReceived" and e["params"]["response"]["url"].endswith(RADAR_PATH)]
        h = {k.lower(): v for k, v in headers[-1]["headers"].items()} if headers else {}
        pg.add("AC-V2-18 Enter shows the radar: overlay drawn, Radar Time = the response's X-Radar-Time, aria-pressed true",
               expect_success(st, want) and h.get("x-radar-time") == RADAR_TIMES["t1"]
               and h.get("content-type", "").startswith("image/png") and pg.radar_requests() == 1,
               {"state": st, "header": h.get("x-radar-time"), "type": h.get("content-type")})
        labels = pg.b.js("""(function(){
          var dts = Array.from(document.querySelectorAll('#now-panel dt')).map(function(d){return d.textContent;});
          var rt = document.getElementById('radar-time'), ot = document.getElementById('obs-time'), ft = document.getElementById('obs-fetched');
          return {dts: dts, radarRow: rt.closest('.obs-times__row').querySelector('dt').textContent,
                  separate: rt !== ot && rt !== ft && !rt.closest('.obs-times__row').contains(ot),
                  radarVal: rt.textContent, obsVal: ot.textContent, fetchedVal: ft.textContent,
                  visible: __chk.visible(rt) && __chk.visible(ot) && __chk.visible(ft)};})()""")
        pg.add("AC-V2-18/H-3 the radar time is labelled 'Radar Time', visible, apart from Observation Time and Fetched Time",
               labels["radarRow"] == "Radar Time" and labels["separate"] and labels["visible"]
               and "Observation Time" in labels["dts"] and "Fetched Time" in labels["dts"]
               and labels["radarVal"] != labels["obsVal"] and labels["radarVal"] != labels["fetchedVal"], labels)
        pg.shot("radar-on")

        # drawing order and interaction with the radar shown
        order = pg.b.js("""(function(){function z(s){var e=document.querySelector(s);return e?+getComputedStyle(e).zIndex:null;}
          var rp=document.querySelector('.leaflet-radar-pane');
          return {backdrop:z('.leaflet-backdrop-pane'),radar:z('.leaflet-radar-pane'),overlay:z('.leaflet-overlay-pane'),
                  marker:z('.leaflet-marker-pane'),radarPointer:getComputedStyle(rp).pointerEvents,
                  imgPointer:getComputedStyle(rp.querySelector('img')).pointerEvents,
                  backdropPaths:document.querySelectorAll('.leaflet-backdrop-pane path').length,
                  countyPaths:document.querySelectorAll('.leaflet-overlay-pane path.leaflet-interactive').length,
                  layerInRadarPane:!!rp.querySelector('.radar-layer')};})()""")
        pg.add("AC-V2-18/RAD-6 drawing order: backdrop < radar < county interaction layer < station markers; radar takes no pointer",
               order["backdrop"] < order["radar"] < order["overlay"] < order["marker"]
               and order["radarPointer"] == "none" and order["imgPointer"] == "none"
               and order["backdropPaths"] > 0 and order["countyPaths"] == 22 and order["layerInRadarPane"], order)

        # a pattern square over land (24N 121E, 南投縣 / 花蓮縣): the county path is on top, the radar under it
        pg.set_view(23.9, 121.0, 8)
        pt = measure(pg, ["24N 121E"], GRID_POINTS)[0]
        mr = pg.map_rect()
        x, y = mr["x"] + pt["exact"]["x"], mr["y"] + pt["exact"]["y"]
        hit = pg.b.js(f"(function(){{var e=document.elementFromPoint({x},{y});return {{tag:e.tagName, "
                      f"county:e.classList.contains('leaflet-interactive')&&!!e.closest('.leaflet-overlay-pane'), "
                      f"radar:!!e.closest('.leaflet-radar-pane')}};}})()")
        pg.mouse("mouseMoved", x, y)
        pg.b.pump(0.5)
        tip = pg.b.js("(function(){var t=document.querySelector('.county-tip');return t&&__chk.visible(t)?t.textContent:null;})()")
        pg.click(x, y)
        chosen = pg.b.js("document.getElementById('county-select').value")
        st_c = pg.state()
        pg.add("AC-V2-18/RAD-6 over a radar pixel the county layer is hit (not the radar): hover shows the county name, click selects it",
               hit["county"] and not hit["radar"] and bool(tip) and chosen == tip and st_c["state"] == "success"
               and st_c["layer"], {"hit": hit, "tooltip": tip, "selected": chosen})
        pg.shot("radar-on-county-selected")
        # a station marker over the radar: click selects it; the label is readable (marker pane on top)
        mk = pg.b.js("""(function(){var el=Array.from(document.querySelectorAll('.station-icon')).find(function(e){
            return !e.classList.contains('is-culled') && __chk.visible(e);}); if(!el) return null;
            var p=el.querySelector('.spill').getBoundingClientRect();
            var hit=document.elementFromPoint(p.x+p.width/2,p.y+p.height/2);
            var cs=getComputedStyle(el.querySelector('.spill'));
            return {x:p.x+p.width/2,y:p.y+p.height/2,label:el.querySelector('.spill').getAttribute('aria-label'),
                    top:!!hit&&el.contains(hit),opacity:getComputedStyle(el).opacity,color:cs.color,bg:cs.backgroundColor};})()""")
        pg.click(mk["x"], mk["y"])
        sel = pg.b.js("(function(){var s=document.getElementById('obs-selected');return __chk.visible(s)?document.getElementById('obs-sel-name').textContent:null;})()")
        pg.add("AC-V2-18/RAD-6 station markers stay on top and readable over the radar; clicking one selects the station",
               mk is not None and mk["top"] and mk["opacity"] == "1" and bool(sel), {"marker": mk, "selected": sel})
        pg.b.js("document.getElementById('back-to-taiwan').click(); true")
        pg.b.pump(0.8)
        # drag and zoom with the radar shown; the layer follows the map. The drag
        # starts over the open sea west of Taiwan (no marker under the pointer), at
        # zoom 8 (at zoom 7 the whole fence E fits the map, so there is nothing to drag).
        pg.set_view(23.4, 119.9, 8)
        before = pg.b.js("__map.getCenter()")
        mr = pg.map_rect()
        sea = pg.b.js("(function(){var p=__map.latLngToContainerPoint([23.0,119.0]);return {x:p.x,y:p.y};})()")
        pg.drag(mr["x"] + sea["x"], mr["y"] + sea["y"], -120, 60)
        after = pg.b.js("__map.getCenter()")
        z0 = pg.b.js("__map.getZoom()")
        pg.b.js("document.querySelector('.leaflet-control-zoom-in').click(); true")
        pg.b.pump(1.0)
        z1 = pg.b.js("__map.getZoom()")
        follow = measure(pg, ["centre", "臺北", "臺中"])
        pg.add("AC-V2-18/RAD-6 with the radar shown the map still drags and zooms (animated +); the layer is re-placed (≤ 1 km)",
               math.hypot(after["lng"] - before["lng"], after["lat"] - before["lat"]) > 0.05 and z1 == z0 + 1
               and all(m["errExactKm"] <= 1.0 for m in follow),
               {"before": before, "after": after, "zoom": [z0, z1],
                "errKm": {m["name"]: round(m["errExactKm"], 4) for m in follow}})

        alignment(pg, record)
        transparency(pg, record)

        # Space hides it
        st = pg.toggle(" ")
        pg.add("AC-V2-18 Space hides the radar: overlay removed, Radar Time hidden, aria-pressed false",
               st["pressed"] == "false" and st["label"] == "Radar: Off" and not st["layer"] and not st["infoVisible"], st)
        # re-show fetches the latest image (the documented trigger)
        rig.radar_next("ok", "t2")
        n = pg.radar_requests()
        st = pg.toggle()
        pg.add("AC-V2-18/RAD-3 showing the radar again fetches the latest image (new Radar Time)",
               expect_success(st, fmt_time(RADAR_TIMES["t2"], False)) and pg.radar_requests() == n + 1, st)
        # Refresh while shown also fetches it; the observation is refreshed alongside
        rig.radar_next("ok", "t3")
        n, o = pg.radar_requests(), pg.obs_requests()
        pg.refresh()
        st = pg.state()
        pg.add("AC-V2-18/RAD-3 Refresh while the radar is shown fetches the latest radar image too",
               expect_success(st, fmt_time(RADAR_TIMES["t3"], False)) and pg.radar_requests() == n + 1
               and pg.obs_requests() == o + 1, st)
        # no polling: nothing happens by itself
        n = pg.radar_requests()
        pg.b.pump(12)
        pg.add("AC-V2-18/RAD-3 no automatic update or polling (12 s idle: no radar request)",
               pg.radar_requests() == n, {"requests": pg.radar_requests()})
        # an older radar time never replaces the one shown
        rig.radar_next("ok", "t0")
        st = pg.toggle()  # off
        st = pg.toggle()  # on -> fetch returns the older t0
        pg.add("RAD-4 an older radar image never replaces the newer one shown (kept, noted)",
               expect_success(st, fmt_time(RADAR_TIMES["t3"], False)) and "Already the latest" in st["status"], st)
        # Forecast mode: no radar control, no layer; back to Now: the radar is back
        pg.b.js("document.getElementById('mode-forecast').click(); true")
        pg.b.wait_for("document.querySelectorAll('.pill-icon').length === 6", 10)
        pg.b.pump(0.6)
        f = pg.state()
        ftext = pg.b.js("document.querySelector('.map-shell').innerText")
        pg.add("AC-V2-18/MODE-4 Forecast mode has no Radar control and no radar overlay",
               f["mode"] == "forecast" and not f["toggleVisible"] and not f["layer"] and "Radar" not in ftext,
               {"toggle": f["toggleVisible"], "layer": f["layer"]})
        pg.shot("forecast-mode-no-radar")
        pg.b.js("document.getElementById('mode-now').click(); true")
        pg.b.pump(1.0)
        st = pg.state()
        pg.add("MODE-5 back in Now mode the shown radar and its Radar Time are back",
               expect_success(st, fmt_time(RADAR_TIMES["t3"], False)), st)
        text = pg.b.js("document.body.innerText")
        pg.add("MODE-6/DOC-5 no real-time / live wording on the page", not FORBIDDEN_WORDS.search(text), "")
        record["consoleProblems1280"] = pg.b.console_problems()
        pg.add("no console errors / NaN / Invalid LatLng", not record["consoleProblems1280"], record["consoleProblems1280"])
        network["1280-main"] = pg.b.request_urls()
    finally:
        pg.close()


def alignment(pg: Page, record: dict) -> None:
    """AC-V2-19 at zoom 7 and 10: DOM geometry for the reference points (on and off
    screen), rendered pixels for the squares on screen, and the discrimination
    check with a plain image overlay."""
    dom = {}
    for z, centre in ((7, (23.5, 120.9)), (10, (24.2, 120.9))):
        pg.set_view(*centre, z)
        rows = measure(pg)
        dom[z] = rows
        worst = max(rows, key=lambda m: m["errExactKm"])
        worst_api = max(rows, key=lambda m: m["errApiKm"])
        pg.add(f"AC-V2-19 zoom {z}: all {len(rows)} reference pixels drawn within 1 km of the map's projection",
               len(rows) >= 12 and all(m["errExactKm"] <= 1.0 for m in rows),
               {"worstKm": round(worst["errExactKm"], 4), "worst": worst["name"],
                "worstVsLeafletRoundedApiKm": round(worst_api["errApiKm"], 4)})
    record["alignmentDom"] = dom

    # rendered pixels: zoom 7 (one view holds most squares) and zoom 10 at island points
    ren = []
    pg.set_view(23.6, 120.9, 7)
    r7, stats7 = rendered(pg, REF_POINTS + GRID_POINTS, save="z7")
    ren += r7
    for name, lat, lon in (("臺北", 25.04, 121.51), ("臺中", 24.15, 120.67), ("恆春", 22.00, 120.75),
                           ("花蓮", 23.98, 121.60), ("澎湖 馬公", 23.57, 119.58), ("金門", 24.43, 118.32),
                           ("centre", 23.5, 121.0), ("edge N", 26.5, 121.0), ("corner NW", 26.5, 118.0),
                           ("edge W", 23.5, 118.0)):
        pg.set_view(lat, lon, 10)
        rr, _ = rendered(pg, [p for p in REF_POINTS + GRID_POINTS if p[0] == name])
        ren += rr
        if name in ("臺北", "澎湖 馬公"):
            pg.shot(f"alignment-z10-{'taipei' if name == '臺北' else 'penghu'}")
    whole = [m for m in ren if m.get("found") and m.get("wholeSquare")]
    z10 = [m for m in whole if m["zoom"] == 10]
    z7 = [m for m in whole if m["zoom"] == 7]
    record["alignmentRendered"] = {"points": ren, "zoom7Stats": stats7}
    pg.add("AC-V2-19 rendered pixels, zoom 10: every whole square's centroid within 1 km of its projected centre",
           len(z10) >= 7 and all(m["errKm"] <= 1.0 for m in z10),
           {m["name"]: round(m["errKm"], 3) for m in z10})
    missing = [m["name"] for m in ren if not m.get("found")]
    pg.add("AC-V2-19 rendered pixels: every square on screen was found in the rendered map", not missing, missing)
    pg.add("AC-V2-19 rendered pixels, zoom 7 (coarse; 1 px ≈ 1.1 km): every whole square on screen within 1 km",
           len(z7) >= 20 and all(m["errKm"] <= 1.0 for m in z7),
           {"n": len(z7), "worstKm": round(max(m["errKm"] for m in z7), 3) if z7 else None})
    clipped = [m for m in ren if m.get("found") and not m.get("wholeSquare")]
    record["alignmentRendered"]["edgeSquaresNote"] = (
        "squares centred on the product's edge / corner pixels are clipped by the image edge, so their "
        "centroid is not the pixel centre; those points are measured by the DOM geometry above")
    record["alignmentRendered"]["clippedFound"] = len(clipped)

    # discrimination: a plain image overlay of the same image on the same map
    pg.set_view(24.2, 120.9, 10)
    pg.b.js("""(function(){var url=document.querySelector('.leaflet-radar-pane img').getAttribute('src');
        window.__naive=L.imageOverlay(url,[[20.5,118],[26.5,124]],{pane:'radar'}).addTo(__map);
        document.querySelector('.leaflet-radar-pane .radar-layer').style.display='none';})(); true""")
    pg.b.pump(0.8)
    naive = measure(pg, naive=True)
    pg.b.js("__map.removeLayer(window.__naive); document.querySelector('.leaflet-radar-pane .radar-layer').style.display=''; true")
    pg.b.pump(0.4)
    worst = max(naive, key=lambda m: m["errExactKm"])
    record["alignmentNaiveOverlay"] = naive
    pg.add("AC-V2-19 the instrument discriminates: a plain image overlay measures > 1 km off (DA: ~3.8 km)",
           worst["errExactKm"] > 1.0, {"worstKm": round(worst["errExactKm"], 3), "at": worst["name"]})


def transparency(pg: Page, record: dict) -> None:
    """RAD-6 / RAD-1: the image's non-echo area leaves the backdrop untouched —
    every pixel that changes when the radar is shown belongs to a pattern square."""
    pg.set_view(23.6, 120.9, 8)
    on_pts, stats = rendered(pg, REF_POINTS + GRID_POINTS)
    # a square at zoom 8 is 25 source px ≈ 4.6 km ≈ 8 screen px across
    record["transparency"] = stats
    pg.add("RAD-6 non-echo area is transparent: the only map pixels the radar changes are the pattern squares",
           stats["blobs"] > 0 and stats["strayBlobs"] == 0 and stats["largestBlob"] <= 12 * 12
           and stats["changed"] <= stats["blobs"] * 12 * 12, stats)


def scenario_failures(chrome: str, rig: Rig, out: Path, checks: Checks, record: dict, network: dict) -> None:
    pg = Page(chrome, rig, out, checks, "1280-fail", 1280, 900, False)
    texts = {}
    try:
        pg.open()
        base = pg.state()
        cases = [("key_not_configured", dict(mode="ok", key=False)),
                 ("upstream_unreachable", dict(mode="unreachable")),
                 ("upstream_error", dict(mode="http", status=403)),
                 ("invalid_response", dict(mode="nonjson")),
                 ("unexpected_response", dict(mode="ok", platform="html502"))]
        for i, (category, setup) in enumerate(cases):
            rig.radar_next(**setup)
            st = pg.toggle()
            texts[category] = st["status"]
            ok = (st["state"] == "unavailable" and not st["layer"] and st["time"] == "—"
                  and "Radar unavailable" in st["status"] and st["pressed"] == "true"
                  and (category in st["status"] or category == "unexpected_response")
                  and obs_same(st, base) and st["obsState"] == "success")
            pg.add(f"AC-V2-18/09(c) first radar fetch fails ({category}) → radar unavailable, no overlay, reason; observation unchanged",
                   ok, {k: st[k] for k in ("state", "layer", "time", "status", "obsState", "obsTime")})
            if i == 0:
                pg.shot("radar-unavailable")
            pg.toggle()  # off (resets nothing; the next show fetches again)
            rig.env["CWA_API_KEY"] = SENTINEL_KEY
        pg.add("R-V2-OBS-12 (radar) the failure categories are distinguishable to the user",
               len(set(texts.values())) == len(texts), texts)
        # server-side stall: bounded (classified within the instrument)
        rig.radar_next("stall")
        t0 = time.time()
        st = pg.toggle()
        secs = time.time() - t0
        pg.add("AC-V2-18 bounded time: a stalled upstream ends as radar unavailable (upstream_unreachable) within 30 s",
               st["state"] == "unavailable" and "upstream_unreachable" in st["status"] and secs < INSTRUMENT_S,
               {"seconds": round(secs, 1), "status": st["status"]})
        pg.toggle()
        # success, then a failed refetch keeps the image, marked stale
        rig.radar_next("ok", "t1")
        st = pg.toggle()
        src = st["src"]
        pg.add("recovery: the next successful show clears radar unavailable", expect_success(st, fmt_time(RADAR_TIMES["t1"], False)), st)
        rig.radar_next("http", status=500)
        pg.refresh()
        st = pg.state()
        pg.add("AC-V2-18/RAD-4 a failed refetch while an image is shown keeps the overlay and its Radar Time, marked stale with the reason",
               st["state"] == "stale" and st["layer"] and st["layerVisible"] and st["src"] == src
               and st["time"] == fmt_time(RADAR_TIMES["t1"], False) and "Radar Stale" in st["status"]
               and "upstream_error" in st["status"] and "(HTTP 500)" in st["status"], st)
        pg.add("AC-V2-09(c) the radar failure changed only the radar: observation state success, times and markers as before",
               st["obsState"] == "success" and st["obsTime"] == base["obsTime"] and st["markers"] == base["markers"],
               {k: st[k] for k in ("obsState", "obsTime", "markers")})
        pg.shot("radar-stale")
        # hang past the page's own bound: the shown image stays, stale (no_response)
        rig.radar_next("ok", "t2", platform="hang")
        t0 = time.time()
        pg.toggle()
        st = pg.toggle()
        secs = time.time() - t0
        pg.add("AC-V2-18 the page's own bound: no answer in 20 s → stale kept (no_response), within 30 s",
               st["state"] == "stale" and st["src"] == src and "did not answer" in st["status"] and secs < INSTRUMENT_S,
               {"seconds": round(secs, 1), "status": st["status"]})
        rig.platform.mode = None
        rig.radar_next("ok", "t2")
        st = pg.toggle()
        st = pg.toggle()
        pg.add("stale cleared by the next successful fetch", expect_success(st, fmt_time(RADAR_TIMES["t2"], False)), st)
        # the other direction: an observation failure leaves the radar working
        rig.obs_up.fail = True
        rig.radar_next("ok", "t3")
        pg.refresh()
        st = pg.state()
        pg.add("AC-V2-09(c) an observation failure (Refresh → observation Stale) leaves the radar working (new image, success)",
               st["obsState"] == "stale" and expect_success(st, fmt_time(RADAR_TIMES["t3"], False)), st)
        pg.shot("obs-stale-radar-ok")
        rig.obs_up.fail = False
        page_text = pg.b.js("document.body.innerText")
        pg.add("H-1 the page shows no key, upstream host, upstream body or platform page text",
               not [s for s in LEAKS + (PLATFORM_MARKER,) if s in page_text], "")
        record["consoleProblemsFail"] = pg.b.console_problems()
        network["1280-failures"] = pg.b.request_urls()
    finally:
        pg.close()
    # first load with the observation unavailable: the radar still works
    rig.obs_up.fail = True
    pg = Page(chrome, rig, out, checks, "1280-obs-down", 1280, 900, False)
    try:
        pg.open()
        rig.radar_next("ok", "t1")
        st = pg.toggle()
        pg.add("AC-V2-09(c) observation Unavailable from the first load: the radar still shows",
               st["obsState"] == "unavailable" and expect_success(st, fmt_time(RADAR_TIMES["t1"], False)), st)
        pg.shot("obs-unavailable-radar-ok")
        network["1280-obs-down"] = pg.b.request_urls()
    finally:
        pg.close()
        rig.obs_up.fail = False


def scenario_forecast_503(chrome: str, image: bytes, out: Path, checks: Checks, network: dict) -> None:
    rig = Rig(image, db_path=_UNIT_DIR / "tests" / "no-such-forecast.db")
    pg = Page(chrome, rig, out, checks, "1280-forecast503", 1280, 900, False)
    try:
        pg.open()
        rig.radar_next("ok", "t1")
        st = pg.toggle()
        err = pg.b.js("(function(){var e=document.getElementById('page-error');return __chk.visible(e)?e.innerText:null;})()")
        pg.add("AC-V2-09(a) forecast snapshot 503: Now mode radar works; the forecast section shows its own error",
               bool(err) and expect_success(st, fmt_time(RADAR_TIMES["t1"], False)) and st["obsState"] == "success",
               {"forecastError": (err or "")[:80], "radar": st["state"]})
        pg.shot("forecast503-radar-on")
        network["1280-forecast503"] = pg.b.request_urls()
    finally:
        pg.close()
        rig.close()


def scenario_375(chrome: str, rig: Rig, out: Path, checks: Checks, record: dict, network: dict,
                 label: str = "375") -> None:
    pg = Page(chrome, rig, out, checks, label, 375, 812, True)
    try:
        rig.radar_next("ok", "t1")
        pg.open()
        st = pg.state()
        box = pg.b.js("__chk.rect(document.getElementById('radar-toggle'))")
        pg.add("375 default hidden; control ≥ 44 x 44; no horizontal scroll",
               st["state"] == "off" and box["w"] >= 44 and box["h"] >= 44 and st["scrollWidth"] <= 375, box)
        pg.shot("radar-off")
        st = pg.toggle("Enter")
        pg.add("375 radar shown by keyboard; Radar Time visible; no horizontal scroll",
               expect_success(st, fmt_time(RADAR_TIMES["t1"], False)) and st["scrollWidth"] <= 375, st)
        pg.b.js("document.getElementById('map').scrollIntoView({block:'center'}); true")
        pg.b.pump(0.3)
        pg.shot("radar-on")
        if label == "375":
            rows = measure(pg)
            pg.add("375 AC-V2-19 (DOM geometry, current zoom) every reference pixel within 1 km",
                   all(m["errExactKm"] <= 1.0 for m in rows), {"worstKm": round(max(m["errExactKm"] for m in rows), 4)})
            record["alignmentDom375"] = rows
            pg.b.js("window.scrollTo(0,0); true")
            rig.radar_next("http", status=429)
            pg.refresh()
            st = pg.state()
            pg.add("375 stale: overlay kept, reason visible; no horizontal scroll",
                   st["state"] == "stale" and st["layer"] and "upstream_error" in st["status"] and st["scrollWidth"] <= 375, st)
            pg.b.js("window.scrollTo(0,0); true")
            pg.shot("radar-stale")
            pg.toggle()
            rig.radar_next("ok", key=False)
            pg.b.navigate(rig.base + "/")
            pg.b.js(JS_HELPERS)
            pg.b.wait_for("!!window.__map", 15)
            st = pg.toggle()
            pg.add("375 unavailable: no overlay, reason visible; no horizontal scroll",
                   st["state"] == "unavailable" and not st["layer"] and "key_not_configured" in st["status"]
                   and st["scrollWidth"] <= 375, st)
            pg.b.js("window.scrollTo(0,0); true")
            pg.shot("radar-unavailable")
            rig.env["CWA_API_KEY"] = SENTINEL_KEY
        network[label] = pg.b.request_urls()
    finally:
        pg.close()


def scenario_real(chrome: str, image: bytes, out: Path, checks: Checks, network: dict, label: str,
                  opacity: str | None = None) -> None:
    """The same layer with a real product image (screenshots only)."""
    rig = Rig(image)
    for width, height, mobile, tag in ((1280, 900, False, "1280"), (375, 812, True, "375")):
        pg = Page(chrome, rig, out, checks, f"{label}-{tag}", width, height, mobile)
        try:
            rig.radar_next("ok", "t1")
            pg.open()
            st = pg.toggle()
            pg.add("real image shown by the layer", st["state"] == "success" and st["layer"], st["state"])
            if opacity:
                pg.b.js(f"document.querySelector('.radar-layer').style.opacity='{opacity}'; true")
            if tag == "1280":
                pg.shot("taiwan")
                for name, lat, lon, z in (("taipei-z10", 25.05, 121.5, 10), ("kinmen-z10", 24.45, 118.35, 10),
                                          ("penghu-z10", 23.57, 119.6, 10), ("south-z9", 22.2, 120.8, 9)):
                    pg.set_view(lat, lon, z)
                    pg.b.js("document.getElementById('map').scrollIntoView({block:'center'}); true")
                    pg.b.pump(0.6)
                    pg.shot(name)
            else:
                pg.b.js("document.getElementById('map').scrollIntoView({block:'center'}); true")
                pg.b.pump(0.4)
                pg.shot("taiwan")
            network[f"{label}-{tag}"] = pg.b.request_urls()
        finally:
            pg.close()
    rig.close()


def georef_data_fact(coastline: Path) -> dict:
    """Data-fact check (not the app's oracle): the O-A0058-003 border / coastline
    pixels vs the vendored MOI county polygons under the equal-angle assumption."""
    import numpy as np

    src = (_UNIT_DIR / "static" / "data" / "basemap.js").read_text(encoding="utf-8")
    data = json.loads(re.search(r"Object\.freeze\((\{.*\})\)", src, re.S).group(1))
    verts = []
    for g in data["taiwan"]["geometries"]:
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            for ring in poly:
                verts.extend(ring)
    verts = np.array(verts)
    img = np.asarray(Image.open(coastline).convert("RGB")).astype(int)
    dark = img.sum(axis=2) < 150
    km_lat = (E["north"] - E["south"]) / P * 111.32
    inside = ((verts[:, 0] > E["west"] + 0.02) & (verts[:, 0] < E["east"] - 0.02)
              & (verts[:, 1] > E["south"] + 0.02) & (verts[:, 1] < E["north"] - 0.02))
    v = verts[inside]
    rng = np.random.default_rng(0)
    if len(v) > 4000:
        v = v[rng.choice(len(v), 4000, replace=False)]
    cos = np.cos(np.radians(v[:, 1]))
    c0 = (v[:, 0] - E["west"]) / (E["east"] - E["west"]) * P
    r0 = (E["north"] - v[:, 1]) / (E["north"] - E["south"]) * P
    ys, xs = np.nonzero(dark)
    cells: dict = {}
    for y, x in zip(ys.tolist(), xs.tolist()):
        cells.setdefault((y // 22, x // 22), []).append((x + 0.5, y + 0.5))
    ox, oy, owner = [], [], []
    for i, (c, r) in enumerate(zip(c0, r0)):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                for px, py in cells.get((int(r) // 22 + dy, int(c) // 22 + dx), ()):
                    ox.append((px - c) * km_lat * cos[i])
                    oy.append((r - py) * km_lat)
                    owner.append(i)
    ox, oy, owner = np.array(ox), np.array(oy), np.array(owner)
    order = np.argsort(owner, kind="stable")
    ox, oy, owner = ox[order], oy[order], owner[order]
    used = np.unique(owner)
    starts = np.searchsorted(owner, used)

    def score(sx, sy):
        return np.minimum.reduceat(np.hypot(ox - sx, oy - sy), starts)

    base = score(0.0, 0.0)
    best = None
    grid = np.arange(-2.5, 2.51, 0.1)
    for sx in grid:
        for sy in grid:
            m = float(np.median(score(sx, sy)))
            if best is None or m < best[0]:
                best = (m, float(sx), float(sy))
    sens = {f"{sx:+.0f}km_east": float(np.median(score(sx, 0.0))) for sx in (-1.0, 1.0)}
    sens.update({f"{sy:+.0f}km_north": float(np.median(score(0.0, sy))) for sy in (-1.0, 1.0)})
    return {"vertices": int(len(used)), "medianKm": float(np.median(base)), "p90Km": float(np.percentile(base, 90)),
            "bestShiftKm": {"east": round(best[1], 2), "north": round(best[2], 2), "medianKm": best[0]},
            "medianKmIfShifted1km": sens}


def leak_and_network(checks: Checks, network: dict, base_origin_ok) -> None:
    urls = [u for v in network.values() for u in v]
    external = [u for u in urls if not base_origin_ok(u)]
    checks.add("AC-V2-16 network log: zero external requests (the radar image comes from /api/radar/latest)",
               not external and any(u.endswith(RADAR_PATH) for u in urls), {"external": external[:5], "total": len(urls)})
    log = LOG.getvalue()
    leaks = [s for s in LEAKS if s in log or any(s in u for u in urls)]
    checks.add("AC-V2-07/H-1 server log (DEBUG) and request URLs carry no key, upstream host, upstream body or auth header",
               not leaks, leaks)


def run(chrome: str, out: Path, real: Path | None, coastline: Path | None) -> tuple[Checks, dict, dict]:
    checks, record, network = Checks(), {}, {}
    handler = logging.StreamHandler(LOG)
    handler.setLevel(logging.DEBUG)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)
    image = pattern_png()
    rig = Rig(image)
    try:
        scenario_main(chrome, rig, out, checks, record, network)
        scenario_failures(chrome, rig, out, checks, record, network)
        scenario_375(chrome, rig, out, checks, record, network)
    finally:
        rig.close()
    scenario_forecast_503(chrome, image, out, checks, network)
    if real:
        scenario_real(chrome, real.read_bytes(), out, checks, network, "real-006")
    if coastline:
        scenario_real(chrome, coastline.read_bytes(), out, checks, network, "coastline-003", opacity="0.55")
        fact = georef_data_fact(coastline)
        record["georefDataFact"] = fact
        checks.add("data fact: the O-A0058 grid is the equal-angle lon 118–124 / lat 20.5–26.5 grid "
                   "(borders within ~0.1 km; best trial shift within 0.3 km of none)",
                   fact["medianKm"] < 0.3 and abs(fact["bestShiftKm"]["east"]) <= 0.3
                   and abs(fact["bestShiftKm"]["north"]) <= 0.3, fact)

    def origin_ok(u: str) -> bool:
        return (u.startswith("http://127.0.0.1:") or u.startswith("blob:http://127.0.0.1:")
                or u.startswith("data:") or u == "about:blank")

    leak_and_network(checks, network, origin_ok)
    root.removeHandler(handler)
    return checks, record, network


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--real-image", type=Path, default=None, help="a real O-A0058-006 PNG (screenshots)")
    parser.add_argument("--coastline", type=Path, default=None, help="a real O-A0058-003 PNG (visual + data fact)")
    args = parser.parse_args()
    # check names carry non-ASCII text (≤, →, place names); never fail on a console code page
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args.out.mkdir(parents=True, exist_ok=True)
    checks, record, network = run(find_chrome(), args.out, args.real_image, args.coastline)
    (args.out / "browser-check-results.json").write_text(
        json.dumps({"checks": checks.items}, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "alignment.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "network-log.json").write_text(json.dumps(network, ensure_ascii=False, indent=2), encoding="utf-8")
    passed = sum(1 for i in checks.items if i["pass"])
    print(f"{passed}/{len(checks.items)} checks passed")
    return 0 if checks.ok else 1


if __name__ == "__main__":
    sys.exit(main())
