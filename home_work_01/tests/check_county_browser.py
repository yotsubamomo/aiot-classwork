"""Reproducible browser check for Issue #38 (Taiwan → County → Station).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the convention of ``check_modes_browser.py``, whose
DevTools driver it reuses). It runs the *unmodified* ``server.create_app``
in-process on loopback through the #37 rig (``check_refresh_browser.Rig``: the
real ``LatestObservationService`` with a controllable clock, a simulated upstream
derived from the committed sanitised sample, and the four server failure
classes), with a sentinel key — no real key, no network (R-V2-TC-3).

Two sample variants are added to the rig's upstream:

* ``c0`` — the capture hour as captured, with the 臺北 station's relative
  humidity, air pressure and weather set to sentinels (``-99`` / ``X``) so the
  station detail's "—" can be seen;
* ``zero`` — ``c0`` with every 連江縣 station's air temperature set to ``-99``, so
  連江縣 has **no valid station** in a *successful* Latest Observation (the
  "0 and —, not an error" case of R-V2-DD-5, and the no-data-vs-zero contrast of
  DV-21 §4.1(3)).

Checks (AC-V2-10, AC-V2-12, AC-V2-23 ``Back to Taiwan``, AC-V2-01 county round
trip per DV-20 §4.1, AC-V2-08(a)(b) county layer / County context per DV-21 §4.1
and §4.2, R-V2-DD-4..DD-9, DD-11, R-V2-RSP-2 / RSP-6 in the selected states,
AC-V2-16 runtime network log) read the ``/api/`` bodies the page actually
received through the DevTools protocol; expected values are computed from those
bodies with ``representative.in_map_range`` (the canonical map range E) and the
README's tie rule — nothing is typed in as an oracle.

Usage (from the unit directory, venv active, ``data.db`` present)::

    python tests/check_county_browser.py                 # writes evidence
    python tests/check_county_browser.py --out <dir>
    CHROME="/path/to/chrome" python tests/check_county_browser.py

Exit code 0 means every check passed. Evidence in ``--out`` (default
``doc/acceptance/screenshots/v2/issue-38/``): PNG screenshots,
``browser-check-results.json`` and ``network-log.json``.
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
from tests.check_modes_browser import (  # noqa: E402
    JS_HELPERS, Browser, Checks, find_chrome, fmt_temp, fmt_time,
)
from tests.check_refresh_browser import LEAKS, Rig  # noqa: E402

DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "v2" / "issue-38"
OBS_PATH = "/api/observations/latest"
TAIPEI_ID = "466920"
DONGSHA_ID = "468100"
MISSING = "—"
COUNTIES = list(representative.COUNTY_ORDER)
AGGREGATE_WORDS = re.compile(r"\b(average|mean)\b|平均", re.IGNORECASE)
FORBIDDEN_WORDS = re.compile(r"\b(real-?time|live)\b", re.IGNORECASE)

# Page-side helpers for the county layer: the interactive county paths, the one
# drawn as selected, and a screen point inside a path that is not covered by
# anything (a marker, the panel) — found with the path's own fill test.
COUNTY_HELPERS = r"""
window.__cty = {
  paths: function () {
    return Array.from(document.querySelectorAll('#map .leaflet-overlay-pane path.leaflet-interactive'));
  },
  selected: function () {
    return this.paths().filter(function (p) { return p.getAttribute('stroke') === '#fbbf24' && p.getAttribute('stroke-opacity') === '1'; });
  },
  pointIn: function (path) {
    var bb = path.getBBox(), m = path.getScreenCTM(), svg = path.ownerSVGElement;
    for (var n = 6; n <= 96; n *= 2) {
      for (var i = 1; i < n; i++) for (var j = 1; j < n; j++) {
        var pt = svg.createSVGPoint();
        pt.x = bb.x + bb.width * i / n; pt.y = bb.y + bb.height * j / n;
        if (!path.isPointInFill(pt)) continue;
        var s = pt.matrixTransform(m);
        if (s.x < 0 || s.y < 0 || s.x >= innerWidth || s.y >= innerHeight) continue;
        if (document.elementFromPoint(s.x, s.y) === path) return [s.x, s.y];
      }
    }
    return null;
  },
  styles: function () {
    return this.paths().map(function (p) {
      return {stroke: p.getAttribute('stroke'), so: p.getAttribute('stroke-opacity'),
              fill: p.getAttribute('fill'), fo: p.getAttribute('fill-opacity')};
    });
  },
  tip: function () {
    var t = document.querySelector('.leaflet-tooltip.county-tip');
    return t ? t.innerText.trim() : null;
  },
  // Keyboard focus is "not fully obscured" when the element itself is what is
  // hit at its own centre (no panel / overlay above it) and the centre is in view.
  focusVisible: function () {
    var el = document.activeElement;
    if (!el || el === document.body) return {ok: false, why: 'no focus'};
    var r = el.getBoundingClientRect();
    var x = r.x + r.width / 2, y = r.y + r.height / 2;
    var inView = x >= 0 && y >= 0 && x < innerWidth && y < innerHeight;
    var hit = inView ? document.elementFromPoint(x, y) : null;
    return {ok: inView && !!hit && (hit === el || el.contains(hit)), id: el.id || el.className,
            rect: [Math.round(r.x), Math.round(r.y), Math.round(r.width), Math.round(r.height)]};
  },
};
true;
"""

COUNTY_STATE_JS = r"""(function () {
  function t(id) { return document.getElementById(id).textContent; }
  var c = document.getElementById('county-context');
  var sel = document.getElementById('obs-selected');
  var stations = document.getElementById('county-stations');
  return {
    visible: __chk.visible(c), name: t('county-name'), count: t('county-count'), onmap: t('county-onmap'),
    max: t('county-max'), min: t('county-min'), select: document.getElementById('county-select').value,
    text: (__chk.visible(c) ? c.innerText : '') + '\n' + (__chk.visible(stations) ? stations.innerText : ''),
    listTitle: t('county-list-title'),
    empty: __chk.visible(document.getElementById('county-list-empty')) ? t('county-list-empty') : null,
    items: Array.from(document.querySelectorAll('#county-list .county__item')).map(function (b) {
      return {id: b.getAttribute('data-station-id'), text: b.innerText.replace(/\s+/g, ' ').trim(),
              pressed: b.getAttribute('aria-pressed'), off: !!b.querySelector('.county__item-off')};
    }),
    listVisible: __chk.visible(document.getElementById('county-list')),
    state: __chk.visible(document.getElementById('county-state')) ? t('county-state') : null,
    back: __chk.visible(document.getElementById('back-to-taiwan')) ? t('back-to-taiwan').trim() : null,
    markers: Array.from(document.querySelectorAll('.station-icon .spill')).map(function (p) { return p.getAttribute('aria-label'); }),
    countyMarkers: document.querySelectorAll('.station-icon--county').length,
    activeMarkers: Array.from(document.querySelectorAll('.station-icon.is-active .spill')).map(function (p) { return p.getAttribute('aria-label'); }),
    detail: sel.hidden ? null : {
      name: t('obs-sel-name'), place: t('obs-sel-place'), id: t('obs-sel-id'), temp: t('obs-sel-temp'),
      rh: t('obs-sel-rh'), wind: t('obs-sel-wind'), wdir: t('obs-sel-wdir'), pres: t('obs-sel-pres'),
      rain: t('obs-sel-rain'), weather: t('obs-sel-weather'), time: t('obs-sel-time'),
      offmap: !document.getElementById('obs-sel-offmap').hidden},
    obsState: document.getElementById('now-panel').getAttribute('data-obs-state'),
    chip: __chk.visible(document.getElementById('obs-state-chip')) ? t('obs-state-chip') : null,
    reason: __chk.visible(document.getElementById('obs-state')) ? t('obs-state-reason') : null,
    notice: __chk.visible(document.getElementById('obs-map-state')) ? t('obs-map-state') : null,
    refresh: __chk.visible(document.getElementById('refresh-button')) &&
             document.getElementById('refresh-button').getAttribute('aria-disabled') === 'false',
    nowPressed: document.getElementById('mode-now').getAttribute('aria-pressed'),
    countyPaths: __cty.paths().length,
    scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
  };
})()"""

# The view, read from the DOM: the map pane transform, one county path's
# geometry string (it changes with the zoom), and every marker's anchor point.
VIEW_JS = r"""(function () {
  var m = document.getElementById('map').getBoundingClientRect();
  var anchors = {};
  document.querySelectorAll('.station-icon').forEach(function (el) {
    var p = el.querySelector('.spill'); var r = el.getBoundingClientRect();
    anchors[p.getAttribute('aria-label')] = [r.x + 48 - m.x, r.y + 14 - m.y];
  });
  var path = document.querySelector('#map .leaflet-overlay-pane path');
  return {pane: document.querySelector('#map .leaflet-map-pane').style.transform,
          d: path ? path.getAttribute('d').slice(0, 120) : null, anchors: anchors,
          size: [m.width, m.height]};
})()"""


# --- expected values from the /api/ body ----------------------------------------------


def county_stations(body: dict, county: str) -> list[dict]:
    return [s for s in body["stations"] if s["countyName"] == county]


def name_of(s: dict) -> str:
    return s["stationName"] or MISSING


def expected_context(body: dict, county: str) -> dict:
    """County context computed by hand from a success body (README rules)."""
    st = county_stations(body, county)
    on = [s for s in st if representative.in_map_range(s)]
    order = sorted(st, key=lambda s: (-s["airTemperature"], s["stationId"]))
    hi = min(st, key=lambda s: (-s["airTemperature"], s["stationId"])) if st else None
    lo = min(st, key=lambda s: (s["airTemperature"], s["stationId"])) if st else None

    def ext(s):
        return MISSING if s is None else f"{fmt_temp(s['airTemperature'])} °C · {name_of(s)}"

    off = len(st) - len(on)
    return {
        "count": str(len(st)),
        "onmap": str(len(on)) + (f" ({off} not on the map)" if off else ""),
        "max": ext(hi), "min": ext(lo),
        "order": [s["stationId"] for s in order],
        "onmap_ids": sorted(s["stationId"] for s in on),
        "offmap_ids": sorted(s["stationId"] for s in st if not representative.in_map_range(s)),
        "temps": [fmt_temp(s["airTemperature"]) + " °C" for s in order],
    }


def context_matches(ctx: dict, exp: dict, county: str) -> bool:
    return (ctx["visible"] and ctx["name"] == county and ctx["select"] == county
            and ctx["count"] == exp["count"] and ctx["onmap"] == exp["onmap"]
            and ctx["max"] == exp["max"] and ctx["min"] == exp["min"]
            and [i["id"] for i in ctx["items"]] == exp["order"]
            and all(i["text"].endswith(t) for i, t in zip(ctx["items"], exp["temps"]))
            and ctx["back"] == "Back to Taiwan")


def expected_detail(s: dict) -> dict:
    def pub(v, unit):
        return MISSING if v is None else (str(int(v)) if isinstance(v, float) and v.is_integer() else str(v)) + unit
    return {
        "name": name_of(s) + " station", "id": s["stationId"],
        "place": s["countyName"] + " · " + (s["townName"] or MISSING),
        "temp": fmt_temp(s["airTemperature"]) + " °C", "rh": pub(s["relativeHumidity"], " %"),
        "wind": pub(s["windSpeed"], " m/s"), "wdir": pub(s["windDirection"], "°"),
        "pres": pub(s["airPressure"], " hPa"), "rain": pub(s["precipitation"], " mm"),
        "weather": s["weather"] if s["weather"] else MISSING,
        "time": fmt_time(s["observationTime"], False),
        "offmap": not representative.in_map_range(s),
    }


def same_anchors(v1: dict, v2: dict, tol: float = 0.5) -> bool:
    """The same visible view: every marker at the same place in the map (px)."""
    a1, a2 = v1["anchors"], v2["anchors"]
    return bool(a1) and a1.keys() == a2.keys() and all(
        abs(a1[k][0] - a2[k][0]) <= tol and abs(a1[k][1] - a2[k][1]) <= tol for k in a1)


def view_reading(view: dict, body: dict) -> dict:
    """Centre (lat, lng) and zoom of the map, derived from two marker anchors and
    the Web Mercator projection — the DV-20 'view reading'."""
    by_label = {}
    for s in body["stations"]:
        for label in view["anchors"]:
            if label.startswith(name_of(s) + " station, " + s["countyName"] + ":"):
                by_label[label] = s
    pts = [(view["anchors"][k], by_label[k]) for k in view["anchors"] if k in by_label]
    if len(pts) < 2:
        return {"zoom": None, "center": None, "pane": view["pane"]}

    def merc(s):
        lat, lng = math.radians(s["latitude"]), s["longitude"]
        return ((lng + 180) / 360, (1 - math.log(math.tan(lat) + 1 / math.cos(lat)) / math.pi) / 2)

    (pa, sa), (pb, sb) = max(((a, b) for a in pts for b in pts),
                             key=lambda ab: math.dist(ab[0][0], ab[1][0]))
    ma, mb = merc(sa), merc(sb)
    scale = math.dist(pa, pb) / math.dist(ma, mb)  # px per unit Mercator
    zoom = math.log2(scale / 256)
    cx, cy = view["size"][0] / 2, view["size"][1] / 2
    ux, uy = ma[0] + (cx - pa[0]) / scale, ma[1] + (cy - pa[1]) / scale
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * uy))))
    return {"zoom": round(zoom, 3), "center": [round(lat, 5), round(ux * 360 - 180, 5)], "pane": view["pane"]}


# --- view checks (R-V2-DD-5(a)) -------------------------------------------------------


def county_fitted(s, exp: dict) -> tuple[bool, dict]:
    """DD-5(a): the county's on-map stations are the markers, all inside the map
    and (floating panel) clear of the panel; the county's shape is in view too."""
    b = s.b
    c = s.ctx()
    frame = b.js("__chk.rect(document.getElementById('map'))")
    panel = b.js("__chk.rect(document.getElementById('now-panel'))")
    anchors = s.view()["anchors"]
    floating = not s.mobile and b.js("innerWidth") >= 1180
    in_view = all(0 <= x <= frame["w"] and 0 <= y <= frame["h"] for x, y in anchors.values())
    clear = (not floating) or all(x + frame["x"] > panel["x"] + panel["w"] for x, _y in anchors.values())
    shape_ok, shape = shape_in_view(s)
    ok = c["countyMarkers"] == len(exp["onmap_ids"]) == len(anchors) and in_view and clear and shape_ok
    return ok, {"markers": c["countyMarkers"], "expected": len(exp["onmap_ids"]), "inView": in_view,
                "clearOfPanel": clear, "shape": shape}


def shape_in_view(s) -> tuple[bool, dict]:
    """The selected county's polygon lies inside the map (1 px tolerance) and, with
    the floating panel, to the right of it — the county view is really shown."""
    b = s.b
    r = b.js("""(function(){var p=__cty.selected()[0]; if(!p) return null;
        var a=p.getBoundingClientRect(), m=document.getElementById('map').getBoundingClientRect(),
            n=document.getElementById('now-panel').getBoundingClientRect();
        return {x:a.x,y:a.y,r:a.right,b:a.bottom,mx:m.x,my:m.y,mr:m.right,mb:m.bottom,panelRight:n.right};})()""")
    if not r:
        return False, {"selected": None}
    floating = not s.mobile and b.js("innerWidth") >= 1180
    inside = (r["x"] >= r["mx"] - 1 and r["y"] >= r["my"] - 1 and r["r"] <= r["mr"] + 1 and r["b"] <= r["mb"] + 1)
    clear = (not floating) or r["x"] >= r["panelRight"] - 1
    return inside and clear, {k: round(v) for k, v in r.items()}


# --- session -------------------------------------------------------------------------


class S:
    """One page on the rig at one viewport."""

    def __init__(self, chrome: str, rig: Rig, out: Path, checks: Checks, label: str,
                 width: int, height: int, mobile: bool) -> None:
        self.b = Browser(chrome)
        self.rig, self.out, self.checks, self.label, self.mobile = rig, out, checks, label, mobile
        self.b.viewport(width, height, mobile)

    def open(self) -> None:
        self.b.navigate(self.rig.base + "/")
        self.b.js(JS_HELPERS)
        self.b.js(COUNTY_HELPERS)
        self.b.wait_for("document.getElementById('now-panel').getAttribute('data-obs-state') !== 'loading'", 30)
        self.b.pump(0.6)

    def add(self, name: str, ok: bool, detail) -> None:
        self.checks.add(f"{self.label} {name}", ok, detail)

    def shot(self, name: str) -> None:
        self.b.screenshot(self.out / f"{self.label}-{name}.png")

    def ctx(self) -> dict:
        return self.b.js(COUNTY_STATE_JS)

    def success_bodies(self) -> list[dict]:
        return [r["json"] for r in self.b.response_bodies(OBS_PATH) if r["status"] == 200]

    def view(self) -> dict:
        return self.b.js(VIEW_JS)

    def show_map(self) -> None:
        if self.mobile:
            self.b.js("document.getElementById('map').scrollIntoView({block: 'center'}); true")
            self.b.pump(0.3)

    def choose(self, county: str) -> None:
        """Select a county with the keyboard through the County chooser: focus it,
        press ArrowDown until the county is chosen (each press is a change)."""
        target = COUNTIES.index(county) + 1  # option 0 is "All of Taiwan"
        self.b.js("document.getElementById('county-select').focus(); true")
        cur = self.b.js("document.getElementById('county-select').selectedIndex")
        if cur > target:
            self.b.js("var s=document.getElementById('county-select'); s.selectedIndex=0; "
                      "s.dispatchEvent(new Event('change')); true")
            cur = 0
        for _ in range(target - cur):
            self.b.key("ArrowDown")
        self.b.pump(1.0)  # a fit asked for during a zoom animation lands at its end

    def hover_county(self, county_path_index: int):
        pt = self.b.js(f"__cty.pointIn(__cty.paths()[{county_path_index}])")
        if not pt:
            return None, None
        self.b.hover(pt[0] - 2, pt[1] - 2)
        self.b.hover(pt[0], pt[1])
        self.b.pump(0.3)
        return pt, self.b.js("__cty.tip()")

    def find_county_path(self, county: str):
        """Hover each county path in view until the tooltip names ``county``."""
        n = self.b.js("__cty.paths().length")
        for i in range(n):
            pt, tip = self.hover_county(i)
            if tip == county:
                return i, pt
        return None, None

    def first_hoverable(self, counties):
        for county in counties:
            _i, pt = self.find_county_path(county)
            if pt:
                return county, pt
        return None, None

    def click(self, x: float, y: float) -> None:
        for t in ("mousePressed", "mouseReleased"):
            self.b.send("Input.dispatchMouseEvent", {"type": t, "x": x, "y": y, "button": "left",
                                                      "clickCount": 1})
        self.b.pump(0.6)

    def press(self, selector: str, key: str) -> None:
        self.b.js(f"document.querySelector({json.dumps(selector)}).focus(); true")
        self.b.key(key)
        self.b.pump(0.6)

    def refresh(self) -> dict:
        self.press("#refresh-button", "Enter")
        self.b.wait_for("document.getElementById('now-panel').getAttribute('aria-busy') === 'false'", 30)
        self.b.pump(0.4)
        return self.ctx()

    def close(self) -> None:
        self.b.close()


def add_variants(rig: Rig) -> None:
    base = json.loads(rig.upstream.payloads["h0"])
    for r in base["records"]["Station"]:
        if r["StationId"] == TAIPEI_ID:
            r["WeatherElement"]["RelativeHumidity"] = "-99"
            r["WeatherElement"]["AirPressure"] = "-99"
            r["WeatherElement"]["Weather"] = "X"
    rig.upstream.payloads["c0"] = json.dumps(base, ensure_ascii=False).encode("utf-8")
    for r in base["records"]["Station"]:
        if r["GeoInfo"]["CountyName"] == "連江縣":
            r["WeatherElement"]["AirTemperature"] = "-99"
    rig.upstream.payloads["zero"] = json.dumps(base, ensure_ascii=False).encode("utf-8")


# --- scenario 1: success — hover, select, context, list, detail, Back to Taiwan --------


def scenario_success(s: S) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    initial_view = s.view()
    c = s.ctx()
    s.add("DD-4 county interaction layer: 22 interactive county paths in Now mode; no county context before a selection",
          c["countyPaths"] == 22 and not c["visible"] and c["select"] == "" and len(c["markers"]) == 22,
          {"paths": c["countyPaths"], "markers": len(c["markers"])})
    styles = b.js("__cty.styles()")
    s.add("DD-4 not coloured by data: every county path has the same transparent fill and no visible outline",
          len({(x["fill"], x["fo"], x["so"]) for x in styles}) == 1 and styles[0]["fo"] == "0"
          and styles[0]["so"] == "0", styles[:2])

    # all 22 names, one-to-one with the polygons: select each through the chooser,
    # hover the polygon drawn as selected, read the name the map shows for it.
    names = {}
    for county in COUNTIES:
        s.choose(county)
        sel = b.js("__cty.selected().length")
        idx = b.js("__cty.paths().indexOf(__cty.selected()[0])")
        shown, _shape = shape_in_view(s)
        pt, tip = s.hover_county(idx) if sel == 1 else (None, None)
        names[county] = {"selectedPaths": sel, "path": idx, "hoverTip": tip, "countyInView": shown}
    s.add("DD-1/DD-4 the 22 county polygons carry the 22 CountyName strings one-to-one (select -> the selected polygon's hover name)",
          # each polygon carries one name, so 22 distinct names on the selected
          # polygons are 22 distinct polygons (the selected one is raised to the
          # end of the SVG, so its DOM index is not an identity)
          all(v["selectedPaths"] == 1 and v["hoverTip"] == k for k, v in names.items())
          and len({v["hoverTip"] for v in names.values()}) == 22, names)
    s.add("DD-5(a)/DD-9(a) every county chosen with the keyboard (ArrowDown through all 22) is shown: its shape in the map, clear of the panel",
          all(v["countyInView"] for v in names.values()),
          {k: v["countyInView"] for k, v in names.items()})
    b.js("var s=document.getElementById('county-select'); s.selectedIndex=0; s.dispatchEvent(new Event('change')); true")
    b.pump(0.8)

    # hover: highlight + county name (desktop pointer)
    s.show_map()
    i, pt = s.find_county_path("臺中市")
    hov = b.js(f"__cty.styles()[{i}]") if i is not None else None
    s.add("AC-V2-10 hover a county -> highlighted (fixed outline + faint fill) and its name shown",
          i is not None and hov["so"] == "1" and hov["fo"] != "0" and b.js("__cty.tip()") == "臺中市",
          {"path": i, "style": hov, "tip": b.js("__cty.tip()")})
    s.shot("county-hover")

    def fitted(county: str, exp: dict) -> tuple[bool, dict]:
        return county_fitted(s, exp)

    # click 臺中市 on the map (the Taiwan-wide view)
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    c = s.ctx()
    exp = expected_context(body, "臺中市")
    s.add("AC-V2-10 click 臺中市 on the map -> County context: name, count, on-map count, highest/lowest = hand-computed from /api/",
          pt is not None and context_matches(c, exp, "臺中市"),
          {"page": {k: c[k] for k in ("name", "count", "onmap", "max", "min", "select")},
           "expected": {k: exp[k] for k in ("count", "onmap", "max", "min")}})
    ok, det = fitted("臺中市", exp)
    s.add("AC-V2-10/DD-5(a) the view holds every on-map 臺中市 station (markers = those stations, inside the map, clear of the panel)",
          ok, det)
    b.js("document.getElementById('back-to-taiwan').click(); true")
    b.pump(0.8)

    # 臺北市 is small at the Taiwan-wide zoom (its polygon lies under the
    # clustered markers there), so drill in: click 新北市, then 臺北市 inside it.
    i, pt = s.find_county_path("新北市")
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    via = s.ctx()["name"]
    i, pt = s.find_county_path("臺北市")
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    c = s.ctx()
    exp = expected_context(body, "臺北市")
    s.add("AC-V2-10 click 新北市, then 臺北市 on the map -> 臺北市 County context = hand-computed from /api/ (densest county)",
          via == "新北市" and pt is not None and context_matches(c, exp, "臺北市"),
          {"via": via, "page": {k: c[k] for k in ("name", "count", "onmap", "max", "min", "select")},
           "expected": {k: exp[k] for k in ("count", "onmap", "max", "min")}})
    ok, det = fitted("臺北市", exp)
    s.add("AC-V2-10/DD-5(a) the view holds every on-map 臺北市 station (markers = those stations, inside the map, clear of the panel)",
          ok, det)
    s.add("AC-V2-10/DD-6 station list complete (every valid station, temperature high to low, value = /api/)",
          [i["id"] for i in c["items"]] == exp["order"] and c["listTitle"] == f"Stations ({exp['count']})",
          {"items": c["items"][:4], "n": len(c["items"])})
    page = b.js("document.body.innerText")
    s.add("AC-V2-10/H-3/INV-V2-5 no average / mean / 平均 anywhere in the Now mode page text; values labelled station values",
          not AGGREGATE_WORDS.search(page) and "no county-level value is computed" in c["text"]
          and not FORBIDDEN_WORDS.search(page),
          AGGREGATE_WORDS.findall(page))
    s.shot("county-taipei")

    # keyboard: Tab from Back to Taiwan into the list, Enter selects -> detail
    b.js("document.getElementById('back-to-taiwan').focus(); true")
    b.key("Tab")
    first = b.js("document.activeElement.getAttribute('data-station-id')")
    fv1 = b.js("__cty.focusVisible()")
    b.key("Tab")
    second = b.js("document.activeElement.getAttribute('data-station-id')")
    fv2 = b.js("__cty.focusVisible()")
    s.add("AC-V2-12/DD-6/DD-9(b) the station list is reached with Tab; focus visible, not covered",
          first == exp["order"][0] and second == exp["order"][1] and fv1["ok"] and fv2["ok"],
          {"first": first, "second": second, "focus": [fv1, fv2]})
    # the list item for 臺北 (sentinels in RH / pressure / weather)
    pos = exp["order"].index(TAIPEI_ID)
    b.js(f"document.querySelectorAll('#county-list .county__item')[{pos}].focus(); true")
    b.key("Enter")
    b.pump(0.5)
    c = s.ctx()
    by_id = {x["stationId"]: x for x in body["stations"]}
    want = expected_detail(by_id[TAIPEI_ID])
    s.add("AC-V2-12/DD-7 Enter on a list item -> detail: name, StationId, county · town, Observation Time, temperature; invalid optional values '—'",
          c["detail"] == want and want["rh"] == MISSING and want["pres"] == MISSING and want["weather"] == MISSING
          and any(a.startswith("臺北 station, 臺北市:") for a in c["activeMarkers"])
          and [i for i in c["items"] if i["pressed"] == "true"][0]["id"] == TAIPEI_ID,
          {"page": c["detail"], "expected": want, "active": c["activeMarkers"]})
    focused = b.js("document.activeElement.getAttribute('data-station-id')")
    s.add("DD-9(e) focus stays on the selected list item after selecting (not lost, not covered)",
          focused == TAIPEI_ID and b.js("__cty.focusVisible()")["ok"], focused)
    # Space on another item; its optional values, as published
    other = next(x for x in exp["order"] if x != TAIPEI_ID)
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{other}\"]').focus(); true")
    b.key(" ")
    b.pump(0.4)
    c = s.ctx()
    s.add("AC-V2-12/DD-7 Space on another list item -> that station's detail = /api/",
          c["detail"] == expected_detail(by_id[other]), {"page": c["detail"], "expected": expected_detail(by_id[other])})
    # a marker click in the county view selects that station too
    b.js("document.querySelector('.station-icon--county .spill').click(); true")
    b.pump(0.4)
    c = s.ctx()
    s.add("DD-5(d)/DD-7 a county-view marker click selects its station (detail + list item marked)",
          c["detail"] is not None and len([i for i in c["items"] if i["pressed"] == "true"]) == 1, c["detail"])
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{TAIPEI_ID}\"]').click(); true")
    b.pump(0.4)
    s.shot("station-detail")

    # Back to Taiwan with the keyboard
    s.press("#back-to-taiwan", "Enter")
    b.pump(0.6)
    c = s.ctx()
    back_view = s.view()
    s.add("AC-V2-12/DD-8/AC-V2-23 'Back to Taiwan' (Enter) clears county and station, returns the Taiwan-wide view (= initial view)",
          not c["visible"] and c["select"] == "" and c["detail"] is None and len(c["markers"]) == 22
          and c["countyMarkers"] == 0 and same_anchors(back_view, initial_view)
          and b.js("document.activeElement.id") == "county-select",
          {"select": c["select"], "markers": len(c["markers"]), "sameView": same_anchors(back_view, initial_view),
           "focus": b.js("document.activeElement.id")})
    s.shot("back-to-taiwan")

    # non-map keyboard path: an outlying county and the off-map station (高雄市 東沙島)
    s.choose("金門縣")
    c = s.ctx()
    exp = expected_context(body, "金門縣")
    s.add("AC-V2-10/AC-V2-12/DD-9(a) keyboard chooser (ArrowDown) selects 金門縣 (outlying island): context = /api/",
          context_matches(c, exp, "金門縣") and county_fitted(s, exp)[0],
          {k: c[k] for k in ("name", "count", "onmap", "max", "min")})
    s.shot("county-kinmen")
    s.choose("連江縣")
    c = s.ctx()
    exp = expected_context(body, "連江縣")
    s.add("AC-V2-10 the county with the fewest valid stations (連江縣): context = /api/; view = its stations",
          context_matches(c, exp, "連江縣") and county_fitted(s, exp)[0], {k: c[k] for k in ("name", "count", "onmap", "max", "min")})
    s.choose("高雄市")
    c = s.ctx()
    exp = expected_context(body, "高雄市")
    off = [i for i in c["items"] if i["off"]]
    s.add("AC-V2-12/DD-11 高雄市: 東沙島 counted, listed and marked 'not on the map', no marker for it",
          context_matches(c, exp, "高雄市") and exp["offmap_ids"] == [DONGSHA_ID]
          and [i["id"] for i in off] == [DONGSHA_ID] and "not on the map" in off[0]["text"]
          and c["countyMarkers"] == len(exp["onmap_ids"]) == int(exp["count"]) - 1
          and not any(m.startswith("東沙島 station") for m in c["markers"]) and county_fitted(s, exp)[0],
          {"onmap": c["onmap"], "count": c["count"], "off": off, "markers": c["countyMarkers"]})
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{DONGSHA_ID}\"]').focus(); true")
    b.key("Enter")
    b.pump(0.4)
    c = s.ctx()
    s.add("AC-V2-12/DD-11 東沙島 detail viewable from the list, marked not on the map",
          c["detail"] == expected_detail(by_id[DONGSHA_ID]) and c["detail"]["offmap"], c["detail"])
    s.shot("county-kaohsiung-offmap")

    # a county with zero valid stations in a SUCCESSFUL observation: 0 and —
    s.rig.set("ok", "zero")
    s.refresh()
    zbody = s.success_bodies()[-1]
    s.choose("連江縣")
    c = s.ctx()
    s.add("DD-5 zero-valid-station county (derived sample, 連江縣) is selectable: 0 and '—', not an error",
          c["visible"] and c["name"] == "連江縣" and c["count"] == "0" and c["onmap"] == "0"
          and c["max"] == MISSING and c["min"] == MISSING and not c["items"] and c["empty"]
          and c["obsState"] == "success" and c["state"] is None and c["chip"] is None
          and not county_stations(zbody, "連江縣") and len(zbody["representativeStationIds"]) == 21,
          {k: c[k] for k in ("count", "onmap", "max", "min", "empty", "obsState", "state")})
    s.zero_text = c["text"]
    s.shot("county-zero-valid")
    s.rig.set("ok", "c0")
    s.refresh()
    b.js("var s=document.getElementById('county-select'); s.selectedIndex=0; s.dispatchEvent(new Event('change')); true")
    b.pump(0.6)

    # a representative marker under the floating panel: focusing it brings it clear
    if not s.mobile:
        b.js("document.getElementById('map').focus(); true")
        for _ in range(6):
            b.key("ArrowRight")
            b.pump(0.4)  # Leaflet ignores a pan key while a pan animates
        under = b.js("""(function(){var p=document.getElementById('now-panel').getBoundingClientRect();
            var hit=null; document.querySelectorAll('.station-icon .spill').forEach(function(el){
              var r=el.getBoundingClientRect(); var x=r.x+r.width/2, y=r.y+r.height/2;
              if(!hit && x>p.x && x<p.x+p.width && y>p.y && y<p.y+p.height) hit=el.getAttribute('aria-label');});
            return hit;})()""")
        if under:
            b.js(f"Array.from(document.querySelectorAll('.station-icon .spill')).filter(function(e){{return e.getAttribute('aria-label')==={json.dumps(under)};}})[0].focus(); true")
            b.pump(0.4)
            fv = b.js("__cty.focusVisible()")
        else:
            fv = {"ok": False, "why": "no marker under the panel after panning"}
        s.add("DD-9(e)/RSP-6 a marker focused while under the floating panel is brought clear (focus never fully covered)",
              bool(under) and fv["ok"], {"marker": under, "focus": fv})
        s.press("#back-to-taiwan", "Enter") if b.js("__chk.visible(document.getElementById('back-to-taiwan'))") else None


# --- scenario 2: DV-20 — AC-V2-01 county round trip -----------------------------------


def scenario_round_trip(s: S) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    s.show_map()
    county, pt = s.first_hoverable(("臺中市", "花蓮縣", "臺東縣", "南投縣"))
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    county_view = s.view()
    exp = expected_context(body, county)
    # select a station of the county from the list, then zoom in: a view that is
    # neither the county fit nor the initial view
    sid = exp["order"][2]
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{sid}\"]').focus(); true")
    b.key("Enter")
    b.pump(0.4)
    s.show_map()
    b.js("document.querySelector('.leaflet-control-zoom-in').click(); true")
    b.pump(0.9)
    before = s.view()
    ctx_before = s.ctx()
    s.press("#mode-forecast", "Enter")
    b.wait_for("document.querySelectorAll('.pill-icon .pill').length === 6", 10)
    b.pump(0.6)
    fc = b.js("""({pills: document.querySelectorAll('.pill-icon').length, stations: document.querySelectorAll('.station-icon').length,
        countyPaths: __cty.paths().length, nowPanel: __chk.visible(document.getElementById('now-panel')),
        text: document.querySelector('.map-shell').innerText})""")
    s.add(f"DV-20/MODE-4 Forecast mode: no county layer, no County context, six Region pills (county {county})",
          fc["pills"] == 6 and fc["stations"] == 0 and fc["countyPaths"] == 0 and not fc["nowPanel"]
          and "Back to Taiwan" not in fc["text"] and county not in fc["text"], {k: fc[k] for k in ("pills", "stations", "countyPaths", "nowPanel")})
    s.press("#mode-now", "Enter")
    b.pump(0.9)
    after = s.view()
    ctx_after = s.ctx()
    rb, ra, rc = view_reading(before, body), view_reading(after, body), view_reading(county_view, body)
    s.add("DV-20 AC-V2-01 (i) after Now -> Forecast -> Now the county is still selected and the County context shows the same county",
          ctx_after["visible"] and ctx_after["name"] == county and ctx_after["select"] == county
          and b.js("__cty.selected().length") == 1 and context_matches(ctx_after, exp, county),
          {"name": ctx_after["name"], "select": ctx_after["select"], "selectedPaths": b.js("__cty.selected().length")})
    s.add("DV-20 AC-V2-01 (ii) the view equals the view on leaving Now mode (not the county fit, not the initial view)",
          same_anchors(after, before) and not same_anchors(county_view, before)
          and ra["zoom"] == rb["zoom"] and ra["center"] == rb["center"] and rc["zoom"] != rb["zoom"],
          {"before": rb, "after": ra, "countyFit": rc})
    s.add("DV-20 AC-V2-01 (iii) the station selected in the county and its detail are restored",
          ctx_after["detail"] == ctx_before["detail"] is not None and ctx_after["detail"]["id"] == sid
          and ctx_after["activeMarkers"] == ctx_before["activeMarkers"] and len(ctx_after["activeMarkers"]) == 1
          and [i["id"] for i in ctx_after["items"] if i["pressed"] == "true"] == [sid],
          {"detail": ctx_after["detail"], "active": ctx_after["activeMarkers"]})
    s.add("RSP-2 no horizontal scroll with a county and a station selected",
          ctx_after["scrollWidth"] <= ctx_after["innerWidth"], [ctx_after["scrollWidth"], ctx_after["innerWidth"]])
    s.round_trip = {"countyFit": rc, "beforeLeaving": rb, "afterReturn": ra}
    s.shot("roundtrip-returned")


# --- scenario 3: DV-21 (1) Unavailable ------------------------------------------------


def scenario_unavailable(s: S) -> None:
    b = s.b
    s.rig.set("http", status=500)
    s.open()
    c = s.ctx()
    s.add("DV-21(1) first load fails -> Unavailable; the 22-polygon county layer is present",
          c["obsState"] == "unavailable" and c["countyPaths"] == 22 and c["chip"] == "UNAVAILABLE",
          {k: c[k] for k in ("obsState", "countyPaths", "chip")})
    s.show_map()
    i, pt = s.find_county_path("臺中市")
    hov = b.js(f"__cty.styles()[{i}]") if i is not None else None
    s.add("DV-21(1) Unavailable: hover still highlights a county and shows its name",
          i is not None and hov["so"] == "1" and b.js("__cty.tip()") == "臺中市", {"style": hov})
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    c = s.ctx()
    digits = re.findall(r"\d", c["text"])

    def unavailable_ok(c, county):
        return (c["visible"] and c["name"] == county and c["select"] == county
                and c["count"] == MISSING and c["onmap"] == MISSING and c["max"] == MISSING
                and c["min"] == MISSING and not c["items"] and not c["listVisible"] and c["empty"]
                and not re.search(r"\d", c["text"]) and c["countyMarkers"] == 0 and not c["markers"]
                and c["state"] and "unavailable" in c["state"].lower()
                and c["chip"] == "UNAVAILABLE" and c["reason"] and c["refresh"] and c["nowPressed"] == "true"
                and c["back"] == "Back to Taiwan")

    s.add("DV-21(1)/§4.2 map click selects 臺中市: name shown; count, on-map, highest, lowest all '—' (never 0 or any number); no station listed",
          unavailable_ok(c, "臺中市"),
          {k: c[k] for k in ("name", "count", "onmap", "max", "min", "empty", "state", "chip", "reason")} | {"digits": digits})
    s.unavailable_text = c["text"]
    s.shot("unavailable-county")
    pan = "document.querySelector('#map .leaflet-map-pane').style.transform"
    b.js("document.getElementById('map').focus(); true")
    t0 = b.js(pan)
    b.key("ArrowRight")
    b.pump(0.5)
    s.add("DV-21(1) with no station to fit, the map stays usable (keyboard pan works)", b.js(pan) != t0, None)
    s.choose("花蓮縣")
    c = s.ctx()
    s.add("DV-21(1) keyboard chooser selects 花蓮縣 under Unavailable: same '—' context, state and Refresh visible; its shape is the view",
          unavailable_ok(c, "花蓮縣") and shape_in_view(s)[0], {k: c[k] for k in ("name", "count", "max", "state")})
    s.press("#back-to-taiwan", "Enter")
    c = s.ctx()
    s.add("DV-21(1) Back to Taiwan works under Unavailable (county cleared, still Now mode, still Unavailable)",
          not c["visible"] and c["select"] == "" and c["nowPressed"] == "true" and c["obsState"] == "unavailable",
          {k: c[k] for k in ("visible", "select", "obsState")})
    s.choose("花蓮縣")
    s.rig.set("ok", "c0")
    c = s.refresh()
    body = s.success_bodies()[-1]
    exp = expected_context(body, "花蓮縣")
    s.add("DV-21(1) a later successful Refresh: the kept county's context = the new response's valid stations",
          c["obsState"] == "success" and context_matches(c, exp, "花蓮縣") and c["state"] is None
          and c["countyMarkers"] == len(exp["onmap_ids"]),
          {k: c[k] for k in ("obsState", "count", "onmap", "max", "min")})


# --- scenario 4: DV-21 (2) Stale ------------------------------------------------------


def scenario_stale(s: S) -> None:
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    s.choose("花蓮縣")
    before = s.ctx()
    exp_a = expected_context(body, "花蓮縣")
    ok, det = county_fitted(s, exp_a)
    s.add("DD-5(a) 花蓮縣 chosen with the keyboard: the view holds its stations and shape", ok, det)
    s.rig.set("http", status=429)
    c = s.refresh()
    s.add("DV-21(2) county selected BEFORE the failure: Stale; context unchanged and = the retained response by hand",
          c["obsState"] == "stale" and context_matches(c, exp_a, "花蓮縣")
          and all(c[k] == before[k] for k in ("count", "onmap", "max", "min", "items")),
          {k: c[k] for k in ("obsState", "count", "onmap", "max", "min")})
    s.add("DV-21(2) the Stale marking and reason stay visible with the county selected (chip, County context, on-map notice)",
          c["chip"] == "STALE" and c["state"] and c["state"].startswith("Stale") and c["reason"]
          and "upstream_error" in c["reason"] and c["notice"] and c["notice"].startswith("Stale"),
          {k: c[k] for k in ("chip", "state", "reason", "notice")})
    s.shot("stale-county")
    # select another county AFTER the failure, on the map
    s.show_map()
    i, pt = s.find_county_path("臺東縣")
    if pt is None:  # not in the 花蓮縣 view: go back to Taiwan and pick it there
        b.js("document.getElementById('back-to-taiwan').click(); true")
        b.pump(0.8)
        i, pt = s.find_county_path("臺東縣")
    tip_ok = b.js("__cty.tip()") == "臺東縣"
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.8)
    c = s.ctx()
    retained = s.success_bodies()[-1]
    exp_b = expected_context(retained, "臺東縣")
    s.add("DV-21(2) hover + map click select 臺東縣 AFTER the failure: context = the retained response by hand; Stale still shown",
          tip_ok and c["obsState"] == "stale" and context_matches(c, exp_b, "臺東縣")
          and c["state"] and c["state"].startswith("Stale") and c["chip"] == "STALE"
          and retained["fetchedTime"] == body["fetchedTime"],
          {k: c[k] for k in ("count", "onmap", "max", "min", "state")})
    sid = exp_b["order"][0]
    b.js(f"document.querySelector('#county-list .county__item[data-station-id=\"{sid}\"]').focus(); true")
    b.key("Enter")
    b.pump(0.4)
    c = s.ctx()
    by_id = {x["stationId"]: x for x in retained["stations"]}
    s.add("DV-21(2) station list selection works while Stale (detail = retained data)",
          c["detail"] == expected_detail(by_id[sid]), c["detail"])
    s.press("#back-to-taiwan", "Enter")
    c = s.ctx()
    s.add("DV-21(2) Back to Taiwan works while Stale (county cleared; still Stale)",
          not c["visible"] and c["obsState"] == "stale" and len(c["markers"]) == 22, {k: c[k] for k in ("visible", "obsState")})
    s.choose("臺東縣")
    # not-newer success clears Stale; the context stays the displayed data
    s.rig.set("ok", "hm1")
    c = s.refresh()
    s.add("DV-21(2) a not-newer Refresh clears Stale; County context = the displayed data",
          c["obsState"] == "success" and c["state"] is None and context_matches(c, exp_b, "臺東縣"),
          {k: c[k] for k in ("obsState", "count", "max")})
    # fail again, then a newer success: Stale cleared, context = the new data
    s.rig.set("unreachable")
    c = s.refresh()
    stale_again = c["obsState"] == "stale"
    s.rig.set("ok", "h1")
    c = s.refresh()
    newest = s.success_bodies()[-1]
    exp_n = expected_context(newest, "臺東縣")
    s.add("DV-21(2) after another failure, a newer Refresh clears Stale; County context = the new response",
          stale_again and c["obsState"] == "success" and c["state"] is None and context_matches(c, exp_n, "臺東縣")
          and newest["observationTime"] != retained["observationTime"],
          {k: c[k] for k in ("obsState", "count", "max", "min")})


def mobile_walk(s: S) -> None:
    """375 px: the county paths, list keyboard, detail, Back to Taiwan and no
    horizontal scroll in the selected states (the full 375 panel is #39)."""
    b = s.b
    s.rig.set("ok", "c0")
    s.open()
    body = s.success_bodies()[-1]
    initial_view = s.view()
    s.choose("臺北市")
    c = s.ctx()
    exp = expected_context(body, "臺北市")
    s.add("375 AC-V2-10/12 keyboard chooser selects 臺北市: context = /api/; no horizontal scroll",
          context_matches(c, exp, "臺北市") and c["scrollWidth"] <= c["innerWidth"] and county_fitted(s, exp)[0],
          {k: c[k] for k in ("count", "onmap", "max", "min", "scrollWidth", "innerWidth")})
    s.shot("county-context")
    b.js("document.getElementById('back-to-taiwan').focus(); true")
    b.key("Tab")
    fv = b.js("__cty.focusVisible()")
    b.key("Enter")
    b.pump(0.4)
    c = s.ctx()
    by_id = {x["stationId"]: x for x in body["stations"]}
    s.add("375 AC-V2-12 Tab into the list + Enter -> detail = /api/; focus visible; no horizontal scroll",
          c["detail"] == expected_detail(by_id[exp["order"][0]]) and fv["ok"] and c["scrollWidth"] <= c["innerWidth"],
          {"detail": c["detail"], "focus": fv})
    s.shot("station-detail")
    s.press("#back-to-taiwan", "Enter")
    c = s.ctx()
    back = s.view()
    s.add("375 AC-V2-12/DD-8 Back to Taiwan (Enter) clears the selection and returns the initial view",
          not c["visible"] and c["detail"] is None and same_anchors(back, initial_view)
          and b.js("document.activeElement.id") == "county-select", {"select": c["select"]})
    # the map path at 375: tap a county
    s.show_map()
    county, pt = s.first_hoverable(("花蓮縣", "臺東縣", "南投縣", "臺中市"))
    s.click(pt[0], pt[1]) if pt else None
    b.pump(0.6)
    c = s.ctx()
    s.add(f"375 DD-4 hover shows a county name and a click on its polygon selects it ({county}); no horizontal scroll",
          pt is not None and c["name"] == county and c["visible"] and c["scrollWidth"] <= c["innerWidth"],
          {"name": c["name"], "sw": c["scrollWidth"]})


def mobile_round_trip(s: S) -> None:
    scenario_round_trip(s)


def mobile_states(s: S) -> None:
    b = s.b
    s.rig.set("ok", "c0", key=False)  # no key -> key_not_configured on first load
    s.open()
    s.choose("臺中市")
    c = s.ctx()
    s.add("375 DV-21(1) Unavailable (key_not_configured) + keyboard county: '—' only, state + Refresh visible, no horizontal scroll",
          c["obsState"] == "unavailable" and c["count"] == MISSING and c["max"] == MISSING
          and not re.search(r"\d", c["text"]) and c["state"] and c["refresh"] and c["scrollWidth"] <= c["innerWidth"],
          {k: c[k] for k in ("obsState", "count", "max", "state", "reason", "scrollWidth")})
    s.shot("unavailable-county")
    s.rig.set("ok", "c0")
    c = s.refresh()
    body = s.success_bodies()[-1]
    s.rig.set("nonjson")
    c = s.refresh()
    exp = expected_context(body, "臺中市")
    s.add("375 DV-21(2) Stale (invalid_response) with 臺中市 selected: retained context = /api/, Stale shown, no horizontal scroll",
          c["obsState"] == "stale" and context_matches(c, exp, "臺中市") and c["state"] and c["chip"] == "STALE"
          and c["scrollWidth"] <= c["innerWidth"], {k: c[k] for k in ("obsState", "count", "state", "scrollWidth")})
    s.shot("stale-county")


def run(chrome: str, out: Path) -> Checks:
    checks = Checks()
    network: dict[str, list[str]] = {}
    evidence: dict = {}
    rig = Rig()
    add_variants(rig)
    plans = [
        ("desktop", 1280, 900, False, [("success", scenario_success), ("roundtrip", scenario_round_trip),
                                       ("unavailable", scenario_unavailable), ("stale", scenario_stale)]),
        ("375", 375, 812, True, [("walk", mobile_walk), ("roundtrip", mobile_round_trip),
                                 ("states", mobile_states)]),
    ]
    consoles = []
    try:
        for label, w, h, mobile, steps in plans:
            for name, fn in steps:
                s = S(chrome, rig, out, checks, label, w, h, mobile)
                try:
                    fn(s)
                    for attr in ("round_trip", "zero_text", "unavailable_text"):
                        if hasattr(s, attr):
                            evidence[f"{label}-{name}-{attr}"] = getattr(s, attr)
                finally:
                    network[f"{label}-{name}"] = s.b.request_urls()
                    consoles += s.b.console_problems()
                    s.close()
    finally:
        rig.close()
    # DV-21 (3): no data vs zero, side by side
    z, u = evidence.get("desktop-success-zero_text", ""), evidence.get("desktop-unavailable-unavailable_text", "")
    checks.add("DV-21(3)/H-3 no data vs zero: success shows 0 with no state marking; Unavailable shows only '—' with the state marking",
               "0" in re.findall(r"\b0\b", z) and "unavailable" not in z.lower()
               and not re.search(r"\d", u) and "unavailable" in u.lower(),
               {"success-zero": z, "unavailable": u})
    urls = [u for v in network.values() for u in v]
    external = [u for u in urls if not u.startswith(rig.base) and not u.startswith("data:")
                and not u.startswith("about:")]
    checks.add("AC-V2-16/INV-V2-3 runtime network log: zero external requests (county layer and all scenarios)",
               not external and any("/static/data/counties.js" in u for u in urls),
               {"requests": len(urls), "external": external[:5]})
    page_leaks = [x for x in LEAKS if any(x in u for u in urls)]
    checks.add("H-1 no key / upstream marker in any request URL", not page_leaks, page_leaks)
    checks.add("console: no JavaScript exception, no NaN / Invalid LatLng message",
               not [p for p in consoles if "503" not in p and "429" not in p and "500" not in p
                    and "502" not in p and "504" not in p], consoles[:5])
    out.mkdir(parents=True, exist_ok=True)
    (out / "browser-check-results.json").write_text(
        json.dumps({"checks": checks.items, "evidence": evidence}, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "network-log.json").write_text(
        json.dumps({"origin": rig.base, "external": external, "byScenario": network}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    checks = run(find_chrome(), args.out)
    n = len(checks.items)
    passed = sum(1 for i in checks.items if i["pass"])
    print(f"{passed}/{n} checks passed; evidence in {args.out}")
    return 0 if checks.ok else 1


if __name__ == "__main__":
    sys.exit(main())
