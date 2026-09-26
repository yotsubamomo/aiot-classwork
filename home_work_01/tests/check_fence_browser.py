"""Reproducible browser check for Issue #39 (map fence and responsive usability).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the convention of ``check_modes_browser.py``, whose
DevTools driver it reuses). It runs the *unmodified* ``server.create_app``
in-process on loopback through the #37 rig (``check_refresh_browser.Rig``: the
real ``LatestObservationService`` with a controllable clock, a simulated upstream
derived from the committed sanitised sample, the four server failure classes)
with a sentinel key — no real key, no network (R-V2-TC-3). It reuses the #38
page helpers (``check_county_browser``) for the county chooser and context.

What it checks (SPEC-V2 §2.6, §5.3 instruments, AC-V2-13, AC-V2-14, AC-V2-15,
§6.3 AC-19):

* the map fence at 1280 px and 375 px — after dragging to the end in each of the
  four directions at zoom 8 and at the zoom ceiling, the map's centre is inside
  the fence range E and, on each axis, the map lies inside E or (the axis on
  which the map is wider than E) E lies wholly inside the map; 金門 and 連江 are
  reached by dragging / zooming and their stations are selected by a click;
* the zoom floor (the main island spans >= 25 % of the map height; no further
  zoom-out by button, key or wheel) and the zoom ceiling (1 km >= 20 px; a 375 px
  map spans >= 5 km; no further zoom-in); at the ceiling in 臺北市 every station on
  the map is selected by a click on its marker or, when the density rule hides it
  at that view, shown and marked on the map after choosing it from the list;
* the Now mode's initial view and the view after ``Back to Taiwan`` contain the
  whole main island and 澎湖's main island;
* the 375 px bottom info panel (peek keeps >= half the map; expand to the list;
  a visible, keyboard-operable Close; Esc; "Details" reopens; a new station or
  county updates it while open; zoom, mode switch, Refresh and Back to Taiwan
  never covered; a selected station kept clear of it, even at the fence edge);
* 44 x 44 CSS px for the controls and for every shown station marker's touch
  area; marker density (shown markers never overlap and are hit where drawn);
* no horizontal scroll at 375 px in each state; the 768 px breakage check; the
  desktop panel beside the map (never over the selection or the zoom buttons);
  tooltips inside the map;
* the non-zero-size guard (R-V2-MAP-5): no NaN / 0x0 marker after the info
  panel opens / expands / closes, after resizes (width, height only, a resize
  while the map has no size) and mode switches;
* R-EN-1's six items on the V2 page (loading / Stale / Unavailable screenshots);
* the runtime network log: zero external requests.

The map view is read from the DOM — Leaflet's zoom proxy element carries the
projected centre and the zoom scale (``leaflet-proxy``: ``translate3d`` = the
centre in world px, ``scale`` = 2^(zoom-1)) — and turned into the centre and the
four edges with the Web Mercator formulas; nothing is read from the app's code.

Usage (from the unit directory, venv active, ``data.db`` present)::

    python tests/check_fence_browser.py                 # writes evidence
    python tests/check_fence_browser.py --out <dir>

Exit code 0 means every check passed. Evidence in ``--out`` (default
``doc/acceptance/screenshots/v2/issue-39/``): PNG screenshots,
``browser-check-results.json`` (every check with its observed values, including
the instrument readings) and ``network-log.json``.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

import representative  # noqa: E402
from tests.check_county_browser import (  # noqa: E402
    COUNTY_HELPERS, COUNTY_STATE_JS, S, add_variants, expected_detail,
)
from tests.check_modes_browser import JS_HELPERS, Checks, find_chrome  # noqa: E402
from tests.check_refresh_browser import LEAKS, Rig  # noqa: E402

DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "v2" / "issue-39"
OBS_PATH = "/api/observations/latest"

# The fence range E (SPEC-V2 §5.3; the same numbers as representative.MAP_RANGE).
E_LAT = tuple(representative.MAP_RANGE["latitude"])
E_LNG = tuple(representative.MAP_RANGE["longitude"])
MIN_ZOOM, MAX_ZOOM = 6, 12           # the §5.3 instruments this subject uses
MAIN_ISLAND = {"s": 21.90, "n": 25.30, "w": 120.03, "e": 122.01}   # 鵝鑾鼻 .. 富貴角, west coast .. 三貂角
PENGHU_MAIN = {"s": 23.52, "n": 23.66, "w": 119.52, "e": 119.70}   # 澎湖本島 (馬公)
KINMEN_LAND = {"s": 24.38, "n": 24.50, "w": 118.23, "e": 118.48}   # 大金門
MATSU_LAND = {"s": 26.14, "n": 26.17, "w": 119.92, "e": 119.97}    # 南竿
KINMEN_REP, MATSU_REP = "467110", "467990"
KAOHSIUNG_REP = "467441"  # 高雄市 representative, for the south edge
EARTH_M = 40075016.686

# --- page-side readings -----------------------------------------------------------------

VIEW_JS = r"""(function () {
  var p = document.querySelector('#map .leaflet-proxy');
  var m = p && /translate3d\(([-\d.e]+)px, ([-\d.e]+)px[^)]*\)\s*scale\(([-\d.e]+)\)/.exec(p.style.transform);
  var r = document.getElementById('map').getBoundingClientRect();
  if (!m) return null;
  return {x: +m[1], y: +m[2], scale: +m[3], w: r.width, h: r.height, left: r.left, top: r.top};
})()"""

EXTRA_HELPERS = r"""
window.__fx = {
  hit: function (el) {
    if (!el) return false;
    var r = el.getBoundingClientRect(); var x = r.x + r.width / 2, y = r.y + r.height / 2;
    if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) return false;
    var h = document.elementFromPoint(x, y); return !!h && (h === el || el.contains(h));
  },
  size: function (el) { var r = el.getBoundingClientRect(); return [Math.round(r.width * 10) / 10, Math.round(r.height * 10) / 10]; },
  // every point of a 44 x 44 square centred on the pill hits the pill
  touch: function (pill) {
    var r = pill.getBoundingClientRect(); var cx = r.x + r.width / 2, cy = r.y + r.height / 2, miss = 0;
    for (var i = 0; i < 5; i++) for (var j = 0; j < 5; j++) {
      var x = cx - 21.5 + i * 10.75, y = cy - 21.5 + j * 10.75;
      var h = document.elementFromPoint(x, y);
      if (!h || !(h === pill || pill.contains(h))) miss++;
    }
    return miss;
  },
  shown: function () {
    return Array.from(document.querySelectorAll('.station-icon')).filter(function (el) {
      return !el.classList.contains('is-culled') && getComputedStyle(el).visibility !== 'hidden'; });
  },
  box: function (el) {
    var p = el.querySelector('.spill').getBoundingClientRect(), cx = p.x + p.width / 2, cy = p.y + p.height / 2;
    var w = Math.max(p.width, 44) / 2, h = Math.max(p.height, 44) / 2, b = {l: cx - w, t: cy - h, r: cx + w, b: cy + h};
    var lab = el.querySelector('.slabel').getBoundingClientRect();
    if (lab.width > 0 && getComputedStyle(el.querySelector('.slabel')).display !== 'none') {
      b = {l: Math.min(b.l, lab.left), t: Math.min(b.t, lab.top), r: Math.max(b.r, lab.right), b: Math.max(b.b, lab.bottom)};
    }
    return b;
  },
  marker: function (prefix) {
    return Array.from(document.querySelectorAll('.station-icon')).filter(function (el) {
      return el.querySelector('.spill').getAttribute('aria-label').indexOf(prefix) === 0; })[0] || null;
  },
};
true;
"""

SHEET_JS = r"""(function () {
  var sh = document.getElementById('info-sheet'), m = document.getElementById('map').getBoundingClientRect();
  var s = sh.getBoundingClientRect(), st = sh.getAttribute('data-sheet');
  var open = (st === 'peek' || st === 'expanded') && s.height > 0;
  return {state: st, open: open, top: s.top, bottom: s.bottom, mapTop: m.top, mapBottom: m.bottom, mapH: m.height,
          clearFrac: open ? Math.max(0, s.top - m.top) / m.height : 1,
          title: document.getElementById('sheet-title').textContent,
          closeVisible: __chk.visible(document.getElementById('sheet-close')),
          closeHit: __fx.hit(document.getElementById('sheet-close')),
          reopen: __chk.visible(document.getElementById('sheet-reopen')),
          expanded: document.getElementById('sheet-expand').getAttribute('aria-expanded'),
          focus: document.activeElement ? document.activeElement.id : null,
          sw: document.documentElement.scrollWidth, iw: innerWidth};
})()"""


# --- Web Mercator ------------------------------------------------------------------------


def world(z: float) -> float:
    return 256 * 2 ** z


def lng_of(x: float, z: float) -> float:
    return x / world(z) * 360 - 180


def lat_of(y: float, z: float) -> float:
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / world(z)))))


def x_of(lng: float, z: float) -> float:
    return (lng + 180) / 360 * world(z)


def y_of(lat: float, z: float) -> float:
    s = math.sin(math.radians(lat))
    return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * world(z)


def view(b) -> dict | None:
    v = b.js(VIEW_JS)
    if not v:
        return None
    z = round(math.log2(v["scale"]) + 1, 3)
    x, y, w, h = v["x"], v["y"], v["w"], v["h"]
    return {"zoom": z, "center": [round(lat_of(y, z), 5), round(lng_of(x, z), 5)],
            "west": lng_of(x - w / 2, z), "east": lng_of(x + w / 2, z),
            "north": lat_of(y - h / 2, z), "south": lat_of(y + h / 2, z),
            "size": [w, h], "px": [x, y], "origin": [v["left"], v["top"]]}


def fence_ok(v: dict) -> tuple[bool, dict]:
    """R-V2-MAP-1 (i) centre in E; (ii) per axis: map within E, or E within map.
    One CSS px of tolerance (Leaflet rounds positions to whole px)."""
    z = v["zoom"]
    tol_lng = 360 / world(z)
    tol_lat = tol_lng
    c_lat, c_lng = v["center"]
    centre = E_LAT[0] - tol_lat <= c_lat <= E_LAT[1] + tol_lat and E_LNG[0] - tol_lng <= c_lng <= E_LNG[1] + tol_lng
    lng_in = v["west"] >= E_LNG[0] - tol_lng and v["east"] <= E_LNG[1] + tol_lng
    lng_cover = v["west"] <= E_LNG[0] + tol_lng and v["east"] >= E_LNG[1] - tol_lng
    lat_in = v["south"] >= E_LAT[0] - tol_lat and v["north"] <= E_LAT[1] + tol_lat
    lat_cover = v["south"] <= E_LAT[0] + tol_lat and v["north"] >= E_LAT[1] - tol_lat
    ok = centre and (lng_in or lng_cover) and (lat_in or lat_cover)
    return ok, {"zoom": z, "center": v["center"],
                "west_east": [round(v["west"], 4), round(v["east"], 4)],
                "south_north": [round(v["south"], 4), round(v["north"], 4)],
                "centreInE": centre, "lngAxis": ("map within E" if lng_in else "E within map" if lng_cover else "FAIL"),
                "latAxis": ("map within E" if lat_in else "E within map" if lat_cover else "FAIL")}


def box_in_view(v: dict, box: dict, whole: bool = True) -> bool:
    if whole:
        return v["west"] <= box["w"] and v["east"] >= box["e"] and v["south"] <= box["s"] and v["north"] >= box["n"]
    return v["west"] < box["e"] and v["east"] > box["w"] and v["south"] < box["n"] and v["north"] > box["s"]


def to_screen(v: dict, lat: float, lng: float) -> tuple[float, float]:
    z = v["zoom"]
    return (v["origin"][0] + v["size"][0] / 2 + x_of(lng, z) - v["px"][0],
            v["origin"][1] + v["size"][1] / 2 + y_of(lat, z) - v["px"][1])


# --- interactions ------------------------------------------------------------------------


class F(S):
    """One page at one viewport, with the #38 helpers plus the fence helpers."""

    def open(self) -> None:  # noqa: D401 - same flow as S.open plus our helpers
        super().open()
        self.b.js(EXTRA_HELPERS)

    def v(self) -> dict:
        return view(self.b)

    def mouse(self, kind: str, x: float, y: float, buttons: int = 0) -> None:
        p = {"type": kind, "x": x, "y": y, "button": "left" if kind != "mouseMoved" or buttons else "none",
             "buttons": buttons, "clickCount": 1 if kind != "mouseMoved" else 0}
        self.b.send("Input.dispatchMouseEvent", p)

    def drag(self, dx: float, dy: float) -> None:
        v = self.v()
        x0 = v["origin"][0] + v["size"][0] / 2
        y0 = v["origin"][1] + v["size"][1] / 2 - (self.sheet_cover() / 2)
        self.mouse("mouseMoved", x0, y0)
        self.mouse("mousePressed", x0, y0, 1)
        steps = 8
        for i in range(1, steps + 1):
            self.mouse("mouseMoved", x0 + dx * i / steps, y0 + dy * i / steps, 1)
            self.b.pump(0.03)
        self.mouse("mouseReleased", x0 + dx, y0 + dy, 0)
        self.b.pump(0.9)  # inertia + the fence's own settling

    def sheet_cover(self) -> float:
        st = self.b.js(SHEET_JS)
        return max(0.0, st["mapBottom"] - st["top"]) if st["open"] else 0.0

    def drag_to_end(self, direction: str) -> list[dict]:
        """Drag in one direction until the view stops moving (at most 16 drags)."""
        v = self.v()
        step = min(v["size"]) * 0.7
        d = {"west": (step, 0), "east": (-step, 0), "north": (0, step), "south": (0, -step)}[direction]
        seen = []
        last = None
        for _ in range(16):
            self.drag(*d)
            v = self.v()
            seen.append(v)
            if last and abs(v["px"][0] - last["px"][0]) < 0.5 and abs(v["px"][1] - last["px"][1]) < 0.5:
                break
            last = v
        return seen

    def wheel_in_at_edge(self, direction: str, zoom: int) -> None:
        """Zoom in with the wheel over a point near one edge of the map, so the
        view stays at that edge of the fence while zooming to ``zoom``."""
        for _ in range(16):
            v = self.v()
            if v["zoom"] >= zoom - 0.01:
                return
            w, h = v["size"][0], v["size"][1] - self.sheet_cover()
            x = v["origin"][0] + {"west": 40, "east": w - 40}.get(direction, w / 2)
            y = v["origin"][1] + {"north": 40, "south": h - 40}.get(direction, h / 2)
            self.b.send("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": x, "y": y, "deltaX": 0, "deltaY": -240})
            self.b.pump(0.8)

    def zoom_button(self, which: str) -> bool:
        """Click + or −; return False when the button is disabled (at the limit)."""
        cls = "leaflet-control-zoom-in" if which == "in" else "leaflet-control-zoom-out"
        disabled = self.b.js(f"document.querySelector('.{cls}').classList.contains('leaflet-disabled')")
        if disabled:
            return False
        self.b.js(f"document.querySelector('.{cls}').click(); true")
        self.b.pump(0.7)
        return True

    def zoom_to(self, z: int) -> None:
        for _ in range(12):
            cur = round(self.v()["zoom"])
            if cur == z:
                return
            if not self.zoom_button("in" if cur < z else "out"):
                return

    def key(self, key: str, code: str, vk: int) -> None:
        self.b.js("document.getElementById('map').focus(); true")
        down = {"type": "keyDown", "key": key, "code": code, "windowsVirtualKeyCode": vk}
        if len(key) == 1:
            down["text"] = key
        self.b.send("Input.dispatchKeyEvent", down)
        self.b.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": key, "code": code, "windowsVirtualKeyCode": vk})
        self.b.pump(0.7)

    def wheel(self, delta: float) -> None:
        v = self.v()
        x = v["origin"][0] + v["size"][0] / 2
        y = v["origin"][1] + v["size"][1] / 3
        self.b.send("Input.dispatchMouseEvent", {"type": "mouseWheel", "x": x, "y": y, "deltaX": 0, "deltaY": delta})
        self.b.pump(0.9)

    def marker_center(self, prefix: str):
        return self.b.js(f"""(function(){{var el=__fx.marker({json.dumps(prefix)}); if(!el) return null;
            var p=el.querySelector('.spill').getBoundingClientRect();
            return {{x:p.x+p.width/2, y:p.y+p.height/2, culled: el.classList.contains('is-culled')}};}})()""")

    def bring_marker_to(self, prefix: str, tx: float, ty: float) -> None:
        for _ in range(8):
            c = self.marker_center(prefix)
            if not c or (abs(tx - c["x"]) < 6 and abs(ty - c["y"]) < 6):
                return
            v = self.v()
            lim = min(v["size"]) * 0.7
            self.drag(max(-lim, min(lim, tx - c["x"])), max(-lim, min(lim, ty - c["y"])))

    def bring_marker_to_center(self, prefix: str) -> None:
        for _ in range(8):
            c = self.marker_center(prefix)
            v = self.v()
            if not c:
                return
            cx = v["origin"][0] + v["size"][0] / 2
            cy = v["origin"][1] + (v["size"][1] - self.sheet_cover()) / 2
            dx, dy = cx - c["x"], cy - c["y"]
            if abs(dx) < 40 and abs(dy) < 40:
                return
            lim = min(v["size"]) * 0.7
            self.drag(max(-lim, min(lim, dx)), max(-lim, min(lim, dy)))

    def show(self, sel: str) -> None:
        self.b.js(f"document.querySelector({json.dumps(sel)}).scrollIntoView({{block: 'center'}}); true")
        self.b.pump(0.2)

    def sheet(self) -> dict:
        return self.b.js(SHEET_JS)

    def sw(self) -> tuple[int, int]:
        r = self.b.js("[document.documentElement.scrollWidth, innerWidth]")
        return r[0], r[1]


def rep_label(body: dict, sid: str) -> str:
    s = next(x for x in body["stations"] if x["stationId"] == sid)
    return f"{s['stationName']} station, {s['countyName']}:"


# --- scenario: fence, zoom range, initial view (AC-V2-13) -------------------------------------


def scenario_fence(s: F, instruments: dict, sweeps: dict) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    s.show_map()
    body = s.success_bodies()[-1]
    v0 = s.v()
    ok_f, det_f = fence_ok(v0)
    s.add("AC-V2-13(a)/R-V2-MAP-4 initial Now view contains the whole main island and 澎湖's main island (fence holds)",
          box_in_view(v0, MAIN_ISLAND) and box_in_view(v0, PENGHU_MAIN) and ok_f, det_f)
    instruments[f"{s.label}-initial"] = det_f
    s.shot("initial")

    # zoom floor: − until disabled; then the key and the wheel change nothing
    for _ in range(8):
        if not s.zoom_button("out"):
            break
    vmin = s.v()
    s.key("-", "Minus", 189)
    s.wheel(600)
    vmin2 = s.v()
    z = vmin["zoom"]
    frac = (y_of(MAIN_ISLAND["s"], z) - y_of(MAIN_ISLAND["n"], z)) / vmin["size"][1]
    instruments[f"{s.label}-floor"] = {"zoom": z, "mainIslandNS_px": round(frac * vmin["size"][1], 1),
                                       "mapHeight": vmin["size"][1], "fraction": round(frac, 3)}
    s.add("AC-V2-13(c)/R-V2-MAP-2 zoom floor: the main island spans >= 25 % of the map height; − button disabled; "
          "key / wheel cannot zoom out further",
          abs(z - MIN_ZOOM) < 0.01 and frac >= 0.25 and abs(vmin2["zoom"] - z) < 0.01
          and b.js("document.querySelector('.leaflet-control-zoom-out').classList.contains('leaflet-disabled')"),
          instruments[f"{s.label}-floor"])
    s.shot("zoom-floor")
    res = {}
    for d in ("west", "east", "north", "south"):
        vs = s.drag_to_end(d)
        res[d] = [fence_ok(x) for x in vs]
    s.add("AC-V2-13(c) at the floor the fence holds after dragging to the end in each direction",
          all(ok for r in res.values() for ok, _ in r), {d: r[-1][1] for d, r in res.items()})
    sweeps[f"{s.label}-z{MIN_ZOOM}"] = {d: [x[1] for x in r] for d, r in res.items()}

    # zoom 8 (the §5.3 middle instrument): drag to the end four ways
    s.zoom_to(8)
    res = {}
    for d in ("west", "east", "north", "south"):
        vs = s.drag_to_end(d)
        res[d] = [fence_ok(x) for x in vs]
        s.shot(f"z8-drag-{d}")
    s.add("AC-V2-13(b)/R-V2-MAP-1 zoom 8: after dragging to the end W / E / N / S — centre in E; each axis map ⊆ E or E ⊆ map",
          all(ok for r in res.values() for ok, _ in r) and round(s.v()["zoom"]) == 8,
          {d: r[-1][1] for d, r in res.items()})
    sweeps[f"{s.label}-z8"] = {d: [x[1] for x in r] for d, r in res.items()}
    # keyboard panning is fenced too
    for key, code, vk in (("ArrowLeft", "ArrowLeft", 37), ("ArrowUp", "ArrowUp", 38)):
        for _ in range(10):
            s.key(key, code, vk)
    kb_ok, kb_det = fence_ok(s.v())
    s.add("R-V2-MAP-1 keyboard panning (arrow keys, to the north-west end) stays inside the fence", kb_ok, kb_det)

    # 金門 and 連江 reached by dragging at zoom 8; their station selected by a click
    for name, rep, land in (("金門縣", KINMEN_REP, KINMEN_LAND), ("連江縣", MATSU_REP, MATSU_LAND)):
        label = rep_label(body, rep)
        s.bring_marker_to_center(label)
        v = s.v()
        c = s.marker_center(label)
        ok_f, det_f = fence_ok(v)
        in_map = bool(c) and v["origin"][0] < c["x"] < v["origin"][0] + v["size"][0] \
            and v["origin"][1] < c["y"] < v["origin"][1] + v["size"][1] and not c["culled"]
        if c:
            s.click(c["x"], c["y"])
        d = s.ctx()["detail"]
        s.add(f"AC-V2-13(b) {name} reached by dragging at zoom 8: its land in the map, its station selected by a click; fence holds",
              box_in_view(v, land) and in_map and bool(d) and d["id"] == rep and ok_f and round(v["zoom"]) == 8,
              {"view": det_f, "marker": c, "detail": (d or {}).get("name")})
        s.shot(f"reach-{'kinmen' if rep == KINMEN_REP else 'lienchiang'}-z8")
        # … and still at the ceiling: zoom in on it, it stays reachable and selectable
        s.zoom_to(MAX_ZOOM)
        s.bring_marker_to_center(label)
        v = s.v()
        c = s.marker_center(label)
        if c:
            s.click(c["x"], c["y"])
        d = s.ctx()["detail"]
        ok_f, det_f = fence_ok(v)
        s.add(f"AC-V2-13(b) {name} at the zoom ceiling: land in the map, station selected by a click; fence holds",
              box_in_view(v, land, whole=False) and bool(c) and not c["culled"] and bool(d) and d["id"] == rep
              and ok_f and round(v["zoom"]) == MAX_ZOOM,
              {"view": det_f, "marker": c, "detail": (d or {}).get("name")})
        s.shot(f"reach-{'kinmen' if rep == KINMEN_REP else 'lienchiang'}-max")
        s.zoom_to(8)

    # zoom ceiling: + until disabled; the key cannot zoom in further; instruments
    for _ in range(8):
        if not s.zoom_button("in"):
            break
    vmax = s.v()
    s.key("=", "Equal", 187)
    vmax2 = s.v()
    z = vmax["zoom"]
    lat = vmax["center"][0]
    px_per_km = world(z) / (EARTH_M * math.cos(math.radians(lat))) * 1000
    km_375 = 375 / px_per_km
    instruments[f"{s.label}-ceiling"] = {"zoom": z, "px_per_km": round(px_per_km, 2), "km_per_375px": round(km_375, 2),
                                         "mapWidth_km": round(vmax["size"][0] / px_per_km, 2)}
    s.add("AC-V2-13(d)/R-V2-MAP-3 zoom ceiling: 1 km >= 20 CSS px and a 375 px map spans >= 5 km; + disabled; key cannot zoom further",
          abs(z - MAX_ZOOM) < 0.01 and px_per_km >= 20 and km_375 >= 5 and abs(vmax2["zoom"] - z) < 0.01
          and b.js("document.querySelector('.leaflet-control-zoom-in').classList.contains('leaflet-disabled')"),
          instruments[f"{s.label}-ceiling"])
    s.shot("zoom-ceiling")
    # at the ceiling, each edge: drag to that end at zoom 8, wheel-zoom in over that
    # edge up to the ceiling, then drag to the end again
    res = {}
    for d in ("west", "east", "north", "south"):
        s.zoom_to(8)
        s.drag_to_end(d)
        s.wheel_in_at_edge(d, MAX_ZOOM)
        vs = s.drag_to_end(d)
        res[d] = [fence_ok(x) for x in vs]
        edge = {"west": vs[-1]["west"] - E_LNG[0], "east": E_LNG[1] - vs[-1]["east"],
                "north": E_LAT[1] - vs[-1]["north"], "south": vs[-1]["south"] - E_LAT[0]}[d]
        res[d].append((round(vs[-1]["zoom"]) == MAX_ZOOM and abs(edge) < 0.01, {"distanceToEdgeDeg": round(edge, 5)}))
        s.shot(f"ceiling-drag-{d}")
    s.add("AC-V2-13(b) at the ceiling: dragged to the end W / E / N / S (the map reaches that edge of E) — the fence holds",
          all(ok for r in res.values() for ok, _ in r), {d: [r[-2][1], r[-1][1]] for d, r in res.items()})
    sweeps[f"{s.label}-z{MAX_ZOOM}"] = {d: [x[1] for x in r[:-1]] for d, r in res.items()}

    # Back to Taiwan returns a view with the whole main island and 澎湖
    s.choose("花蓮縣")
    s.press("#back-to-taiwan", "Enter")
    vb = s.v()
    ok_f, det_f = fence_ok(vb)
    s.add("R-V2-MAP-4/DD-8 after Back to Taiwan the view contains the whole main island and 澎湖's main island",
          box_in_view(vb, MAIN_ISLAND) and box_in_view(vb, PENGHU_MAIN) and ok_f, det_f)


# --- scenario: 臺北市 at the zoom ceiling (AC-V2-13(d)) ----------------------------------


def scenario_taipei(s: F, instruments: dict) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    s.show_map()
    body = s.success_bodies()[-1]
    s.choose("臺北市")
    s.zoom_to(MAX_ZOOM)
    on_map = [x for x in body["stations"] if x["countyName"] == "臺北市" and representative.in_map_range(x)]
    clicked, listed, problems = set(), set(), []
    for st in on_map:
        sid = st["stationId"]
        if sid in clicked:
            continue
        # choose it from the list: it must then be shown and marked on the map
        b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{sid}\"]').click(); true")
        b.pump(0.5)
        v = s.v()
        mark = b.js(f"""(function(){{var el=Array.from(document.querySelectorAll('.station-icon')).filter(function(e){{
              return e.classList.contains('is-active');}})[0]; if(!el) return null;
            var p=el.querySelector('.spill'); return {{culled: el.classList.contains('is-culled'), hit: __fx.hit(p),
              label: p.getAttribute('aria-label')}};}})()""")
        want = f"{st['stationName']} station, 臺北市:"
        if mark and not mark["culled"] and mark["hit"] and mark["label"].startswith(want) and round(v["zoom"]) == MAX_ZOOM:
            listed.add(sid)
        else:
            problems.append({"id": sid, "mark": mark, "zoom": v["zoom"]})
        # every other shown 臺北市 marker in this view: a click selects exactly it
        targets = b.js("""__fx.shown().filter(function(el){return !el.classList.contains('is-active') && __fx.hit(el.querySelector('.spill'));})
            .map(function(el){var p=el.querySelector('.spill').getBoundingClientRect();
              return {x:p.x+p.width/2, y:p.y+p.height/2, label: el.querySelector('.spill').getAttribute('aria-label')};})""")
        for t in targets:
            other = next((x for x in on_map if t["label"].startswith(f"{x['stationName']} station, 臺北市:")), None)
            if not other or other["stationId"] in clicked:
                continue
            # the previous click may have changed which markers are shown: click
            # only a marker that is still shown and hit where it is drawn now
            now = b.js(f"""(function(){{var el=__fx.marker({json.dumps(t["label"])}); if(!el||el.classList.contains('is-culled')) return null;
                var p=el.querySelector('.spill'); if(!__fx.hit(p)) return null; var r=p.getBoundingClientRect();
                return {{x:r.x+r.width/2, y:r.y+r.height/2}};}})()""")
            if not now:
                continue
            s.click(now["x"], now["y"])
            d = s.ctx()["detail"]
            if d and d["id"] == other["stationId"]:
                clicked.add(other["stationId"])
            else:
                problems.append({"click": t["label"], "detail": (d or {}).get("id")})
    instruments[f"{s.label}-taipei-ceiling"] = {"onMap": len(on_map), "selectedByMarkerClick": len(clicked),
                                                "shownAndMarkedAfterListChoice": len(listed), "problems": problems}
    s.add("AC-V2-13(d) 臺北市 at the ceiling: every on-map station is selected by a click on its marker, or shown and "
          "marked on the map after choosing it from the list",
          not problems and all(x["stationId"] in clicked or x["stationId"] in listed for x in on_map),
          instruments[f"{s.label}-taipei-ceiling"])
    s.shot("taipei-ceiling")


# --- scenario: density and 44 x 44 (R-V2-RSP-3, RSP-7) -----------------------------------------


CONTROLS = ("#mode-now", "#mode-forecast", "#refresh-button", "#county-select", "#back-to-taiwan",
            "#sheet-expand", "#sheet-close", "#sheet-reopen", ".leaflet-control-zoom-in", ".leaflet-control-zoom-out")


def density_and_touch(s: F, where: str) -> None:
    b = s.b
    d = b.js("""(function(){var sh=__fx.shown(), boxes=sh.map(__fx.box), clash=[];
        for (var i=0;i<boxes.length;i++) for (var j=i+1;j<boxes.length;j++){var a=boxes[i],c=boxes[j];
          if (a.l<c.r-1&&c.l<a.r-1&&a.t<c.b-1&&c.t<a.b-1) clash.push([i,j]);}
        var m=document.getElementById('map').getBoundingClientRect(), sheet=document.getElementById('info-sheet').getBoundingClientRect();
        var inside=sh.filter(function(el){var r=el.querySelector('.spill').getBoundingClientRect();
          return r.left>=m.left+24&&r.right<=m.right-60&&r.top>=m.top+24&&r.bottom<=m.bottom-26&&
                 !(sheet.height>0&&r.bottom>sheet.top-24);});
        var miss=inside.map(function(el){return __fx.touch(el.querySelector('.spill'));});
        var unread=inside.filter(function(el){return !__fx.hit(el.querySelector('.spill'));}).length;
        return {all: document.querySelectorAll('.station-icon').length, shown: sh.length, overlaps: clash.length,
                measured: inside.length, touchMisses: miss.filter(function(x){return x>0;}).length, unreadable: unread,
                culledVisible: Array.from(document.querySelectorAll('.station-icon.is-culled')).filter(function(el){
                  return getComputedStyle(el).visibility!=='hidden';}).length};})()""")
    s.add(f"R-V2-RSP-7/RSP-3 {where}: shown markers never overlap; each shown marker is hit where drawn and its whole "
          "44 x 44 touch area selects it; hidden markers are invisible",
          d["shown"] >= 1 and d["overlaps"] == 0 and d["measured"] >= 1 and d["touchMisses"] == 0
          and d["unreadable"] == 0 and d["culledVisible"] == 0, d)


def controls_44(s: F, where: str) -> dict:
    out = {}
    for sel in CONTROLS:
        r = s.b.js(f"""(function(){{var el=document.querySelector({json.dumps(sel)});
            return el && __chk.visible(el) ? __fx.size(el) : null;}})()""")
        if r:
            out[sel] = r
    items = s.b.js("Array.from(document.querySelectorAll('#county-list .county__item')).filter(__chk.visible).map(__fx.size)")
    out["list items"] = [min(x[0] for x in items), min(x[1] for x in items)] if items else None
    small = {k: v for k, v in out.items() if v and (v[0] < 44 or v[1] < 44)}
    s.add(f"R-V2-RSP-3 {where}: every visible control (mode switch, Refresh, County, Back to Taiwan, info panel "
          "controls, zoom, list items) is at least 44 x 44 CSS px", not small and len(out) >= 6, {"sizes": out, "small": small})
    return out


def scenario_density(s: F) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    s.show_map()
    density_and_touch(s, "Taiwan-wide initial view")
    n0 = len(b.js("__fx.shown()"))
    s.zoom_button("in")
    s.zoom_button("in")
    n2 = len(b.js("__fx.shown()"))
    density_and_touch(s, "Taiwan-wide, zoomed in two levels")
    s.add("R-V2-RSP-7 zooming in shows more of the representative markers (density rule is per zoom)",
          n2 >= n0, {"initial": n0, "zoomedIn": n2})
    s.choose("臺中市")
    density_and_touch(s, "臺中市 county view")
    b.js("document.querySelectorAll('#county-list .county__item')[2].click(); true")
    b.pump(0.6)
    controls_44(s, "county + station selected")
    s.shot("density-county")


# --- scenario: the 375 px bottom info panel (R-V2-RSP-5) ------------------------------------


def key_ok_visible(s: F) -> dict:
    """Zoom buttons, mode switch, Refresh and Back to Taiwan: hit at their centre
    (not covered) once scrolled into view."""
    out = {}
    for sel in (".leaflet-control-zoom-in", ".leaflet-control-zoom-out"):
        out[sel] = s.b.js(f"__fx.hit(document.querySelector('{sel}'))")
    for sel in ("#mode-now", "#mode-forecast", "#refresh-button", "#back-to-taiwan"):
        visible = s.b.js(f"__chk.visible(document.querySelector('{sel}'))")
        if not visible:
            out[sel] = None
            continue
        s.b.js(f"(function(){{var e=document.querySelector('{sel}'), r=e.getBoundingClientRect();"
               f" if(r.top<0||r.bottom>innerHeight) e.scrollIntoView({{block:'nearest'}}); return true;}})()")
        out[sel] = s.b.js(f"__fx.hit(document.querySelector('{sel}'))")
    return out


def scenario_sheet(s: F, states: dict) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    by_id = {x["stationId"]: x for x in body["stations"]}
    st = s.sheet()
    states["now-default"] = s.sw()
    s.add("375 RSP-5 no info panel before a selection", st["state"] == "empty" and not st["open"] and not st["reopen"], st)
    # peek on a county choice
    s.choose("臺中市")
    st = s.sheet()
    keys = key_ok_visible(s)
    s.add("375 RSP-5(b)(d)(g) county chosen -> info panel in peek: >= half the map uncovered; Close visible and not "
          "covered; zoom / mode switch / Refresh / Back to Taiwan not covered",
          st["state"] == "peek" and st["open"] and st["clearFrac"] >= 0.5 and st["closeVisible"] and st["closeHit"]
          and all(keys.values()) and st["title"] == "臺中市", {"sheet": st, "controls": keys})
    states["county-peek"] = s.sw()
    s.shot("sheet-peek-county")
    # expand -> the station list; zoom buttons still clear
    s.press("#sheet-expand", "Enter")
    st = s.sheet()
    lst = b.js("""(function(){var sh=document.getElementById('info-sheet').getBoundingClientRect();
        var it=document.querySelectorAll('#county-list .county__item'); if(!it.length) return null;
        var r=it[0].getBoundingClientRect(); return {n: it.length, firstInPanel: r.top>=sh.top && r.bottom<=sh.bottom};})()""")
    keys = key_ok_visible(s)
    s.add("375 RSP-5(c)(g) Expand (Enter) shows the station list in the panel; the zoom buttons and other key controls "
          "stay uncovered", st["state"] == "expanded" and st["expanded"] == "true" and lst and lst["firstInPanel"]
          and all(keys.values()), {"sheet": st, "list": lst, "controls": keys})
    states["expanded"] = s.sw()
    s.shot("sheet-expanded")
    # choose a station in the list while open -> the panel updates
    first = b.js("document.querySelectorAll('#county-list .county__item')[0].getAttribute('data-station-id')")
    b.js("document.querySelectorAll('#county-list .county__item')[0].click(); true")
    b.pump(0.6)
    c = s.ctx()
    st = s.sheet()
    s.add("375 RSP-5(f) choosing a station while the panel is open updates it (title + detail = /api/)",
          st["open"] and c["detail"] == expected_detail(by_id[first])
          and st["title"].startswith(by_id[first]["stationName"] + " station"), {"title": st["title"], "detail": c["detail"]})
    states["station-expanded"] = s.sw()
    # collapse to peek: the selected marker is kept clear of the panel
    s.press("#sheet-expand", "Enter")
    st = s.sheet()
    mk = b.js("""(function(){var el=Array.from(document.querySelectorAll('.station-icon.is-active'))[0]; if(!el) return null;
        var p=el.querySelector('.spill'), r=p.getBoundingClientRect(); return {bottom:r.bottom, hit: __fx.hit(p)};})()""")
    s.add("375 RSP-6 in peek the selected station's marker is visible above the panel (not covered)",
          st["state"] == "peek" and mk and mk["hit"] and mk["bottom"] <= st["top"], {"marker": mk, "sheet": st})
    s.shot("sheet-peek-station")
    # another county while open -> updates
    s.choose("花蓮縣")
    st = s.sheet()
    c = s.ctx()
    s.add("375 RSP-5(f) choosing another county while the panel is open updates it (花蓮縣)",
          st["open"] and st["title"] == "花蓮縣" and c["name"] == "花蓮縣" and c["visible"], {"title": st["title"]})
    # a map marker click while open updates it
    tgt = b.js("""(function(){var sh=document.getElementById('info-sheet').getBoundingClientRect();
        var el=__fx.shown().filter(function(e){var p=e.querySelector('.spill'), r=p.getBoundingClientRect();
          return !e.classList.contains('is-active') && r.bottom < sh.top - 4 && __fx.hit(p);})[0];
        if(!el) return null; var r=el.querySelector('.spill').getBoundingClientRect();
        return {x:r.x+r.width/2, y:r.y+r.height/2, label: el.querySelector('.spill').getAttribute('aria-label')};})()""")
    if tgt:
        s.click(tgt["x"], tgt["y"])
    c = s.ctx()
    st = s.sheet()
    s.add("375 RSP-5(f) clicking another station's marker while the panel is open updates it",
          bool(tgt) and st["open"] and c["detail"] is not None and tgt["label"].startswith(c["detail"]["name"] + ", ")
          and st["title"].startswith(c["detail"]["name"]),
          {"clicked": (tgt or {}).get("label"), "detail": (c["detail"] or {}).get("name")})
    # Close by keyboard -> closed, Details visible and focused; Details reopens; Esc closes
    b.js("document.getElementById('sheet-close').focus(); true")
    b.key("Enter")
    b.pump(0.5)
    st = s.sheet()
    sel_kept = s.ctx()["detail"] is not None
    s.add("375 RSP-5(a)(d)(e) Close by keyboard (Enter) closes the panel (no swipe needed); focus moves to 'Details'; "
          "the selection is kept", st["state"] == "closed" and not st["open"] and st["reopen"] and st["focus"] == "sheet-reopen"
          and sel_kept, st)
    states["closed"] = s.sw()
    s.shot("sheet-closed")
    b.key("Enter")
    b.pump(0.5)
    st = s.sheet()
    s.add("375 RSP-5 'Details' (Enter) reopens the panel with the same selection",
          st["open"] and st["focus"] == "sheet-close", st)
    b.js("document.getElementById('sheet-close').focus(); true")
    b.send("Input.dispatchKeyEvent", {"type": "keyDown", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
    b.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": "Escape", "code": "Escape", "windowsVirtualKeyCode": 27})
    b.pump(0.5)
    st = s.sheet()
    s.add("375 RSP-5(e) Esc inside the panel closes it too", st["state"] == "closed", st)
    b.js("document.getElementById('sheet-reopen').click(); true")
    b.pump(0.4)
    # a southern station at the fence edge: kept clear of the panel (zooming in if the fence stops the pan)
    s.choose("屏東縣")
    south = min((x for x in body["stations"] if x["countyName"] == "屏東縣" and representative.in_map_range(x)),
                key=lambda x: (x["latitude"], x["stationId"]))
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{south['stationId']}\"]').click(); true")
    b.pump(0.6)
    st = s.sheet()
    mk = b.js("""(function(){var el=Array.from(document.querySelectorAll('.station-icon.is-active'))[0]; if(!el) return null;
        var p=el.querySelector('.spill'), r=p.getBoundingClientRect(); return {bottom:r.bottom, hit: __fx.hit(p)};})()""")
    ok_f, det_f = fence_ok(s.v())
    s.add(f"375 RSP-6 the southernmost 屏東縣 station ({south['stationName']}, {south['latitude']}N) chosen from the list "
          "is kept visible above the panel; fence holds", st["state"] == "peek" and mk and mk["hit"]
          and mk["bottom"] <= st["top"] and ok_f, {"marker": mk, "sheet": st, "view": det_f})
    s.shot("sheet-southern-station")
    # Back to Taiwan with the panel open: it closes (nothing selected), initial view
    s.press("#back-to-taiwan", "Enter")
    st = s.sheet()
    s.add("375 Back to Taiwan clears the selection and the panel", st["state"] == "empty" and not st["open"], st)
    density_and_touch(s, "375 after Back to Taiwan")


def scenario_states(s: F, states: dict) -> None:
    """Loading, Stale and Unavailable (R-EN-1(5) on the Now mode, AC-V2-14) with
    the no-horizontal-scroll check, plus Forecast mode."""
    b = s.b
    s.rig.set("ok", "c0", delay=3.0)
    b_ = s.b
    b_.navigate(s.rig.base + "/")
    b_.js(JS_HELPERS)
    b_.js(COUNTY_HELPERS)
    b_.js(EXTRA_HELPERS)
    b_.wait_for("document.getElementById('now-panel').getAttribute('aria-busy') === 'true'", 10)
    loading = b.js("({state: document.getElementById('now-panel').getAttribute('data-obs-state'),"
                   " status: document.getElementById('obs-status').textContent})")
    states["loading"] = s.sw()
    s.shot("state-loading")
    b.wait_for("document.getElementById('now-panel').getAttribute('data-obs-state') !== 'loading'", 30)
    b.pump(0.5)
    s.add("R-EN-1(5) loading state visible (in-progress indicator) — screenshot",
          loading["state"] == "loading" and "Loading" in loading["status"], loading)
    s.rig.set("http", status=503)
    c = s.refresh()
    states["stale"] = s.sw()
    s.shot("state-stale")
    s.add("R-EN-1(5) Stale state visible with its reason — screenshot", c["obsState"] == "stale" and c["chip"] == "STALE"
          and c["reason"], {k: c[k] for k in ("obsState", "chip", "reason")})
    s.choose("臺中市")
    states["stale-county"] = s.sw()
    c = s.ctx()
    s.add("Stale + county: the County context's state line carries the reason (visible with the county values)",
          c["state"] and "Reason:" in c["state"], c["state"])
    s.shot("state-stale-county")
    # Unavailable on a fresh page
    s.rig.set("ok", "c0", key=False)
    b.navigate(s.rig.base + "/")
    b.js(JS_HELPERS)
    b.js(COUNTY_HELPERS)
    b.js(EXTRA_HELPERS)
    b.wait_for("document.getElementById('now-panel').getAttribute('data-obs-state') !== 'loading'", 30)
    b.pump(0.5)
    c = s.ctx()
    states["unavailable"] = s.sw()
    s.shot("state-unavailable")
    s.add("R-EN-1(5) Unavailable state visible with its reason — screenshot", c["obsState"] == "unavailable"
          and c["chip"] == "UNAVAILABLE" and c["reason"], {k: c[k] for k in ("obsState", "chip", "reason")})
    s.choose("花蓮縣")
    states["unavailable-county"] = s.sw()
    c = s.ctx()
    s.add("Unavailable + county: no digit in the County context (DV-21 §4.2 kept with the reason line)",
          not re.search(r"\d", c["text"]) and c["state"] and "Reason:" in c["state"], c["text"][:200])
    # Forecast mode
    s.rig.set("ok", "c0")
    s.press("#mode-forecast", "Enter")
    b.pump(0.8)
    states["forecast"] = s.sw()
    s.shot("forecast-mode")
    s.press("#mode-now", "Enter")


# --- scenario: desktop panel, tooltips (RSP-6) -----------------------------------------------


def scenario_desktop_panel(s: F) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    s.choose("臺中市")
    b.js("document.querySelectorAll('#county-list .county__item')[0].click(); true")
    b.pump(0.6)
    r = b.js("""(function(){var p=document.getElementById('now-panel').getBoundingClientRect(),
        m=document.getElementById('map').getBoundingClientRect(),
        a=document.querySelector('.station-icon.is-active .spill'), ar=a?a.getBoundingClientRect():null;
        return {apart: p.right <= m.left || p.left >= m.right || p.bottom <= m.top || p.top >= m.bottom,
                selectedHit: !!a && __fx.hit(a), selectedInMap: !!ar && ar.left>=m.left && ar.right<=m.right && ar.top>=m.top && ar.bottom<=m.bottom,
                zoomHit: __fx.hit(document.querySelector('.leaflet-control-zoom-in')) && __fx.hit(document.querySelector('.leaflet-control-zoom-out')),
                detail: __fx.hit(document.getElementById('obs-sel-name'))};})()""")
    s.add("RSP-6 desktop: the Now panel is beside the map (no overlap); the selected station and the zoom buttons are "
          "visible and not covered; the panel shows the detail in view", all(r.values()), r)
    controls_44(s, "desktop county + station")
    s.shot("desktop-panel-county-station")
    # tooltips near the map's edges stay inside the map
    s.press("#back-to-taiwan", "Enter")
    s.show_map()
    for _ in range(2):
        s.zoom_button("in")
    tips = []
    # a marker brought to about 36 px from each edge of the map, then hovered
    for rep, edge in ((KINMEN_REP, "west"), (MATSU_REP, "north"), ("467660", "east"), (KAOHSIUNG_REP, "south")):
        label = rep_label(body, rep)
        v = s.v()
        w, h = v["size"]
        tx = v["origin"][0] + {"west": 36, "east": w - 36}.get(edge, w / 2)
        ty = v["origin"][1] + {"north": 36, "south": h - 36}.get(edge, h / 2)
        s.bring_marker_to(label, tx, ty)
        c = s.marker_center(label)
        if not c:
            tips.append({"marker": label, "tooltip": None})
            continue
        b.hover(c["x"] - 1, c["y"] - 1)
        b.hover(c["x"], c["y"])
        b.wait_for("!!document.querySelector('.leaflet-tooltip.map-tip')", 5)
        t = b.js("""(function(){var t=document.querySelector('.leaflet-tooltip.map-tip'), m=document.getElementById('map').getBoundingClientRect();
            if(!t) return null; var r=t.getBoundingClientRect();
            return {inside: r.left>=m.left-0.5 && r.right<=m.right+0.5 && r.top>=m.top-0.5 && r.bottom<=m.bottom+0.5,
                    rect:[Math.round(r.left-m.left),Math.round(r.top-m.top),Math.round(r.width),Math.round(r.height)],
                    map:[Math.round(m.width),Math.round(m.height)]};})()""")
        tips.append({"marker": label, "edge": edge, "at": [round(c["x"] - v["origin"][0]), round(c["y"] - v["origin"][1])],
                     "tooltip": t})
        s.shot(f"tooltip-edge-{edge}")
        b.hover(5, 5)
        b.pump(0.3)
    s.add("RSP-6 marker tooltips of markers about 36 px from the map's west, north, east and south edges lie wholly "
          "inside the map (not clipped)", len(tips) == 4 and all(t["tooltip"] and t["tooltip"]["inside"] for t in tips), tips)


# --- scenario: 768 px breakage check (R-V2-RSP-1) -----------------------------------------


OVERLAP_JS = r"""(function () {
  var sels = ['#mode-now', '#mode-forecast', '#refresh-button', '#county-select', '#back-to-taiwan', '#sheet-reopen',
              '#sheet-expand', '#sheet-close', '.leaflet-control-zoom-in', '.leaflet-control-zoom-out', '#map-caption',
              '.map-card__head .section-heading', '#date-select', '#region-select'];
  var els = sels.map(function (s) { return [s, document.querySelector(s)]; })
    .filter(function (p) { return p[1] && __chk.visible(p[1]); });
  var clash = [];
  for (var i = 0; i < els.length; i++) for (var j = i + 1; j < els.length; j++) {
    var a = els[i][1].getBoundingClientRect(), b = els[j][1].getBoundingClientRect();
    if (a.left < b.right - 1 && b.left < a.right - 1 && a.top < b.bottom - 1 && b.top < a.bottom - 1) clash.push([els[i][0], els[j][0]]);
  }
  return {controls: els.length, overlaps: clash, sw: document.documentElement.scrollWidth, iw: innerWidth};
})()"""


def scenario_768(s: F) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    s.show_map()
    results = {}
    o = b.js(OVERLAP_JS)
    results["now"] = o
    s.shot("now")
    v1 = s.v()
    s.zoom_button("in")
    v2 = s.v()
    s.drag(-120, -80)
    v3 = s.v()
    operable = abs(v2["zoom"] - v1["zoom"] - 1) < 0.01 and (abs(v3["px"][0] - v2["px"][0]) > 5 or abs(v3["px"][1] - v2["px"][1]) > 5)
    s.choose("臺中市")
    results["county-peek"] = b.js(OVERLAP_JS)
    st = s.sheet()
    s.shot("county-peek")
    s.press("#sheet-expand", "Enter")
    results["county-expanded"] = b.js(OVERLAP_JS)
    keys = key_ok_visible(s)
    s.shot("county-expanded")
    s.press("#mode-forecast", "Enter")
    b.pump(0.8)
    results["forecast"] = b.js(OVERLAP_JS)
    s.shot("forecast")
    s.press("#mode-now", "Enter")
    b.pump(0.6)
    ok = all(not r["overlaps"] and r["sw"] <= r["iw"] for r in results.values())
    s.add("R-V2-RSP-1 768 px breakage check: no overlapping controls and no horizontal scroll (Now default, county "
          "peek / expanded, Forecast); the map drags and zooms; the info panel keeps >= half the map; key controls not covered",
          ok and operable and st["clearFrac"] >= 0.5 and all(keys.values()),
          {"states": results, "operable": operable, "sheet": st, "controls": keys})


# --- scenario: AC-V2-15 non-zero-size guard ----------------------------------------------------


def nan_state(b) -> dict:
    return b.js("""({nan: __chk.noNaN(), markers: document.querySelectorAll('.leaflet-marker-icon').length,
        shown: Array.from(document.querySelectorAll('.leaflet-marker-icon')).filter(function (el) {
          return getComputedStyle(el).visibility !== 'hidden'; }).length})""")


def scenario_guard(s: F) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    log = []

    def rec(step: str) -> None:
        st = nan_state(b)
        v = s.v()
        ok_f, _ = fence_ok(v) if v else (False, None)
        log.append({"step": step, "nan": st["nan"], "markers": st["markers"], "shown": st["shown"],
                    "zoom": v and v["zoom"], "fence": ok_f})

    rec("load 375")
    s.choose("臺中市")
    rec("county -> panel peek")
    s.press("#sheet-expand", "Enter")
    rec("panel expanded")
    b.js("document.querySelectorAll('#county-list .county__item')[1].click(); true")
    b.pump(0.5)
    rec("station chosen")
    s.press("#sheet-close", "Enter")
    rec("panel closed")
    b.js("document.getElementById('sheet-reopen').click(); true")
    b.pump(0.5)
    rec("panel reopened")
    s.press("#mode-forecast", "Enter")
    b.pump(0.6)
    rec("-> Forecast (panel open)")
    s.press("#mode-now", "Enter")
    b.pump(0.6)
    rec("-> Now")
    for w, h, mobile in ((768, 1024, False), (1280, 900, False), (1024, 768, False), (375, 812, True), (375, 640, True)):
        b.viewport(w, h, mobile)
        b.pump(0.9)
        rec(f"resize {w}x{h}")
    # a resize while the map has no size, then the info panel toggled, then shown again
    b.js("document.getElementById('map-shell').style.display = 'none'; true")
    b.viewport(768, 1024, False)
    b.pump(0.6)
    b.js("document.getElementById('sheet-reopen').click(); document.getElementById('sheet-close').click(); true")
    b.pump(0.3)
    b.js("document.getElementById('map-shell').style.display = ''; true")
    b.pump(1.0)
    rec("resize while hidden, panel toggled, shown again")
    b.viewport(375, 812, True)
    b.pump(0.9)
    rec("resize back to 375")
    bad = [x for x in log if x["nan"] or not x["markers"] or not x["fence"] or (x["shown"] or 0) < 1]
    s.add("AC-V2-15/R-V2-MAP-5 no NaN / 0x0 marker and a valid fenced view after the info panel opens / expands / "
          "closes / reopens, mode switches, width and height resizes and a resize while the map had no size",
          not bad and len(log) >= 14, log)


# --- scenario: R-EN-1 six items on the V2 page (§6.3 AC-19) ------------------------------------


def scenario_en1(s: F, desktop: bool) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    h = b.js("""({h1: document.querySelector('h1').textContent, h2: Array.from(document.querySelectorAll('h2')).map(function(e){return e.textContent;}),
        h3: document.querySelector('#now-panel h3').textContent.replace(/\\s+/g,' ').trim(),
        mapBeforeDashboard: document.getElementById('map').getBoundingClientRect().top < document.getElementById('forecast-section').getBoundingClientRect().top,
        toggleInView: document.querySelector('.mode-toggle').getBoundingClientRect().bottom <= innerHeight})""")
    s.add("R-EN-1(1) visual hierarchy: title verbatim, Taiwan Map card above the forecast section, headed Now panel; "
          "mode switch in the first screen",
          h["h1"] == "Taiwan Weather Forecast" and "Taiwan Map" in h["h2"] and h["h3"].startswith("Latest Observation")
          and h["mapBeforeDashboard"] and h["toggleInView"], h)
    summ = b.js("""({count: document.getElementById('obs-count').textContent,
        weekly: __chk.visible(document.getElementById('summary')) && document.getElementById('summary-min-value').textContent})""")
    s.add("R-EN-1(3) summary information: the valid-station count (Now) and the weekly summary (forecast) are shown",
          summ["count"].isdigit() and bool(summ["weekly"]) and summ["weekly"] != "–", summ)
    b.js("document.getElementById('chart').scrollIntoView({block: 'center'}); true")
    b.pump(0.3)
    hit = b.js("""(function(){var r=document.querySelectorAll('#chart .chart__hit')[2]; if(!r) return null; var b=r.getBoundingClientRect(); return [b.x+b.width/2, b.y+b.height/2];})()""")
    if hit:
        b.hover(hit[0], hit[1])
        b.pump(0.3)
    chart = b.js("""({tooltip: !document.getElementById('chart-tooltip').hidden, legend: document.querySelectorAll('.legend__item').length,
        axis: Array.from(document.querySelectorAll('#chart .chart__axis-label')).map(function(e){return e.textContent;})})""")
    s.add("R-EN-1(4) the chart is interactive and readable: legend, axis labels, hover tooltip (unchanged V1 chart)",
          chart["tooltip"] and chart["legend"] == 2 and "Date" in chart["axis"], chart)
    s.shot("en1-chart")
    b.hover(5, 5)


# --- run ------------------------------------------------------------------------------


def run(chrome: str, out: Path, only: str = "") -> Checks:
    checks = Checks()
    network: dict[str, list[str]] = {}
    instruments: dict = {}
    sweeps: dict = {}
    states375: dict = {}
    rig = Rig()
    add_variants(rig)
    plans = [
        ("desktop", 1280, 900, False, [("fence", lambda s: scenario_fence(s, instruments, sweeps)),
                                       ("taipei", lambda s: scenario_taipei(s, instruments)),
                                       ("density", scenario_density),
                                       ("panel", scenario_desktop_panel),
                                       ("en1", lambda s: scenario_en1(s, True))]),
        ("375", 375, 812, True, [("fence", lambda s: scenario_fence(s, instruments, sweeps)),
                                 ("taipei", lambda s: scenario_taipei(s, instruments)),
                                 ("density", scenario_density),
                                 ("sheet", lambda s: scenario_sheet(s, states375)),
                                 ("states", lambda s: scenario_states(s, states375)),
                                 ("guard", scenario_guard),
                                 ("en1", lambda s: scenario_en1(s, False))]),
        ("768", 768, 1024, False, [("breakage", scenario_768)]),
        ("desktop-states", 1280, 900, False, [("states", lambda s: scenario_states(s, {}))]),
    ]
    consoles = []
    try:
        for label, w, h, mobile, steps in plans:
            for name, fn in steps:
                if only and only not in f"{label}-{name}":
                    continue
                s = F(chrome, rig, out, checks, label, w, h, mobile)
                try:
                    fn(s)
                finally:
                    network[f"{label}-{name}"] = s.b.request_urls()
                    consoles += s.b.console_problems()
                    s.close()
    finally:
        rig.close()
    wide = {k: v for k, v in states375.items() if v[0] > v[1]}
    if not only:
        checks.add("R-V2-RSP-2/§6.3 AC-19 375 px: no horizontal scroll in each state (default, county peek, expanded, "
                   "station, closed, loading, Stale, Unavailable, with a county, Forecast mode)",
                   len(states375) >= 10 and not wide, {"states": states375, "wide": wide})
    urls = [u for v in network.values() for u in v]
    external = [u for u in urls if not u.startswith(rig.base) and not u.startswith("data:") and not u.startswith("about:")]
    checks.add("AC-V2-16/INV-V2-3 runtime network log: zero external requests (all scenarios)", not external and urls,
               {"requests": len(urls), "external": external[:5]})
    page_leaks = [x for x in LEAKS if any(x in u for u in urls)]
    checks.add("H-1 no key / upstream marker in any request URL", not page_leaks, page_leaks)
    checks.add("console: no JavaScript exception, no NaN / Invalid LatLng message",
               not [p for p in consoles if not re.search(r"\b(401|403|429|500|502|503|504)\b", p)], consoles[:5])
    out.mkdir(parents=True, exist_ok=True)
    (out / "browser-check-results.json").write_text(
        json.dumps({"checks": checks.items, "instruments": instruments, "fenceSweeps": sweeps},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "network-log.json").write_text(
        json.dumps({"origin": rig.base, "external": external, "byScenario": network}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--only", default="", help="run only the scenarios whose '<viewport>-<name>' contains this")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    checks = run(find_chrome(), args.out, args.only)
    n = len(checks.items)
    passed = sum(1 for i in checks.items if i["pass"])
    print(f"{passed}/{n} checks passed; evidence in {args.out}")
    return 0 if checks.ok else 1


if __name__ == "__main__":
    sys.exit(main())
