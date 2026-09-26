"""Reproducible browser check for WI-UI-POLISH-1 (post-release visual polish).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the convention of ``check_modes_browser.py``, whose
DevTools driver it reuses). It runs the *unmodified* ``server.create_app``
in-process on loopback through the #37 rig (``check_refresh_browser.Rig``: the
real ``LatestObservationService`` with a controllable clock and a simulated
upstream from the committed sanitised sample, the committed ``data.db`` for the
forecast) with a sentinel key — no real key, no network (R-V2-TC-3).

It measures the layout the work item changes and nothing the other checks own:

* geometry at 1440 / 1280 / 1024 / 768 / 375: the page container width and
  centring, the map height (640 / 440 / 360), the desktop Now panel width (360),
  the mode switch and the whole map visible without scrolling on desktop, and
  ``scrollWidth <= innerWidth`` in Now (Taiwan, a county) and Forecast mode;
* the Forecast section's desktop composition (a compact header, a left trend
  column with the weekly summary above the chart, the daily table in a right
  column of the same height) and its single-column order below;
* map initialisation and resize: Leaflet's own size equals the map container
  after load, after Now -> Forecast -> Now and after 1440 -> 768 -> 375 -> 1440,
  and the fitted view still holds the main island and 澎湖;
* the zoom floor at the 640 px desktop map (the main island >= 25 % of the map's
  height at minZoom, SPEC-V2 §5.3);
* screenshots of the first screen and the full page in light (and, at 1440, dark)
  colour schemes, used as the before / after evidence.

Usage (from the unit directory, venv active, ``data.db`` present)::

    python tests/check_ui_polish_browser.py --out <dir>

Exit code 0 means every check passed. Evidence in ``--out``: PNG screenshots,
``browser-check-results.json``.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

from tests.check_county_browser import add_variants  # noqa: E402
from tests.check_modes_browser import Checks, find_chrome  # noqa: E402
from tests.check_refresh_browser import Rig, Session  # noqa: E402

DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "ui-polish" / "after"
MAIN_ISLAND = {"s": 21.90, "n": 25.30, "w": 120.03, "e": 122.01}
PENGHU_MAIN = {"s": 23.52, "n": 23.66, "w": 119.52, "e": 119.70}
MAP_H = {1440: 640, 1280: 640, 1024: 640, 768: 440, 375: 360}

# Exposes the Leaflet map (no app change), as check_radar_browser.py does.
MAP_HOOK = r"""
Object.defineProperty(window, 'L', {configurable: true, get: function () { return undefined; },
  set: function (v) {
    Object.defineProperty(window, 'L', {value: v, writable: true, configurable: true, enumerable: true});
    if (v && v.Map && v.Map.addInitHook) v.Map.addInitHook(function () { window.__map = this; });
  }});
"""

GEOMETRY_JS = r"""(function () {
  function r(sel) {
    var el = typeof sel === 'string' ? document.querySelector(sel) : sel;
    if (!el) return null;
    var b = el.getBoundingClientRect();
    return {l: Math.round(b.left), t: Math.round(b.top + scrollY), r: Math.round(b.right),
            b: Math.round(b.bottom + scrollY), w: Math.round(b.width), h: Math.round(b.height),
            shown: b.width > 0 && b.height > 0};
  }
  var m = window.__map, c = document.getElementById('map');
  var size = m ? m.getSize() : null, bounds = m ? m.getBounds() : null;
  return {
    iw: innerWidth, ih: innerHeight, sw: document.documentElement.scrollWidth,
    page: r('.page'), masthead: r('.masthead'), mapCard: r('.map-card'), toggle: r('.mode-toggle'),
    map: r('#map'), nowPanel: r('#now-panel'), forecastPanel: r('#forecast-panel'),
    section: r('#forecast-section'), controls: r('.controls'), summary: r('#summary'),
    chart: r('#region-panel'), table: r('.table-card'), notes: r('.now-notes'),
    leaflet: size ? {w: size.x, h: size.y} : null,
    container: {w: c.clientWidth, h: c.clientHeight},
    zoom: m ? m.getZoom() : null,
    view: bounds ? {s: bounds.getSouth(), n: bounds.getNorth(), w: bounds.getWest(), e: bounds.getEast()} : null,
    mode: document.querySelector('.mode-toggle__btn[aria-pressed="true"]').id,
    bg: getComputedStyle(document.body).backgroundImage !== 'none' ? 'layered' : getComputedStyle(document.body).backgroundColor
  };
})()"""


def contains(view: dict | None, box: dict) -> bool:
    return bool(view) and view["s"] <= box["s"] and view["n"] >= box["n"] and view["w"] <= box["w"] and view["e"] >= box["e"]


def leaflet_matches(g: dict) -> bool:
    return (g["leaflet"] is not None and g["container"]["w"] > 0 and g["container"]["h"] > 0
            and g["leaflet"] == g["container"])


def open_page(chrome: str, rig: Rig, out: Path, checks: Checks, label: str, w: int, h: int,
              mobile: bool, dark: bool = False) -> Session:
    s = Session(chrome, rig, out, checks, label, w, h, mobile)
    s.b.send("Page.addScriptToEvaluateOnNewDocument", {"source": MAP_HOOK})
    if dark:
        s.b.send("Emulation.setEmulatedMedia", {"features": [{"name": "prefers-color-scheme", "value": "dark"}]})
    rig.set("ok", "c0")
    s.open()
    s.b.wait_for("!document.getElementById('dashboard').hidden && "
                 "document.querySelectorAll('#table-body tr').length === 7", 15)
    s.b.pump(0.8)
    return s


def shots(s: Session, name: str) -> None:
    s.b.screenshot(s.out / f"{s.label}-{name}-first-screen.png")
    s.b.screenshot(s.out / f"{s.label}-{name}-full.png", full_page=True)


def scenario_viewport(chrome: str, rig: Rig, out: Path, checks: Checks, w: int, h: int, record: dict) -> None:
    mobile = w < 768
    s = open_page(chrome, rig, out, checks, str(w), w, h, mobile)
    try:
        g = s.b.js(GEOMETRY_JS)
        record[f"{w}-now"] = g
        shots(s, "now")
        desktop = w >= 1024
        s.add("map height", g["map"]["h"] == MAP_H[w], {"map": g["map"]["h"], "expected": MAP_H[w]})
        s.add("page container <= 1440 px and centred", g["page"]["w"] <= 1440
              and abs(g["page"]["l"] - (g["iw"] - g["page"]["r"])) <= 1, g["page"])
        s.add("no horizontal scroll (Now, Taiwan)", g["sw"] <= g["iw"], {"sw": g["sw"], "iw": g["iw"]})
        s.add("Leaflet size == map container after load; initial view holds the main island and 澎湖",
              leaflet_matches(g) and contains(g["view"], MAIN_ISLAND) and contains(g["view"], PENGHU_MAIN),
              {"leaflet": g["leaflet"], "container": g["container"], "view": g["view"], "zoom": g["zoom"]})
        s.add("mode switch visible without scrolling", 0 <= g["toggle"]["t"] and g["toggle"]["b"] <= g["ih"], g["toggle"])
        if desktop:
            s.add("desktop Now panel is 360 px wide, beside the map", g["nowPanel"]["w"] == 360
                  and g["nowPanel"]["r"] <= g["map"]["l"], {"panel": g["nowPanel"], "map": g["map"]})
            if h >= 900:  # the brief's first-screen instrument: 1440 x 900 and 1280 x 900
                s.add("desktop: the whole map is on the first screen", g["map"]["b"] <= g["ih"],
                      {"mapBottom": g["map"]["b"], "ih": g["ih"]})
            sec = [g["summary"], g["chart"], g["table"]]
            s.add("Forecast section composition A: summary above the chart (left), table in a right column of the "
                  "same height",
                  all(x and x["shown"] for x in sec)
                  and abs(g["summary"]["l"] - g["chart"]["l"]) <= 1 and g["summary"]["b"] <= g["chart"]["t"]
                  and g["table"]["l"] >= g["chart"]["r"] and abs(g["table"]["t"] - g["summary"]["t"]) <= 1
                  and abs(g["table"]["b"] - g["chart"]["b"]) <= 1,
                  {"controls": g["controls"], "summary": g["summary"], "chart": g["chart"], "table": g["table"]})
        else:
            s.add("narrow: Forecast section is one column in the order header, summary, chart, table",
                  g["controls"]["b"] <= g["summary"]["t"] and g["summary"]["b"] <= g["chart"]["t"]
                  and g["chart"]["b"] <= g["table"]["t"] and abs(g["chart"]["l"] - g["table"]["l"]) <= 1,
                  {"controls": g["controls"], "summary": g["summary"], "chart": g["chart"], "table": g["table"]})

        # a county (the drill-down layout) — no horizontal scroll, map sized
        s.b.js("var sel = document.getElementById('county-select'); sel.value = '花蓮縣';"
               "sel.dispatchEvent(new Event('change', {bubbles: true})); true")
        s.b.pump(1.2)
        gc = s.b.js(GEOMETRY_JS)
        record[f"{w}-county"] = gc
        s.b.screenshot(out / f"{w}-county-first-screen.png")
        s.add("no horizontal scroll (Now, a county)", gc["sw"] <= gc["iw"], {"sw": gc["sw"], "iw": gc["iw"]})
        s.add("Leaflet size == map container with a county selected", leaflet_matches(gc),
              {"leaflet": gc["leaflet"], "container": gc["container"]})
        s.b.js("document.getElementById('back-to-taiwan').click(); true")
        s.b.pump(1.0)

        # Now -> Forecast -> Now
        s.b.js("document.getElementById('mode-forecast').click(); true")
        s.b.pump(1.2)
        gf = s.b.js(GEOMETRY_JS)
        record[f"{w}-forecast"] = gf
        shots(s, "forecast")
        s.add("Forecast mode: no horizontal scroll; Leaflet size == map container",
              gf["mode"] == "mode-forecast" and gf["sw"] <= gf["iw"] and leaflet_matches(gf),
              {"sw": gf["sw"], "iw": gf["iw"], "leaflet": gf["leaflet"], "container": gf["container"]})
        s.b.js("document.getElementById('mode-now').click(); true")
        s.b.pump(1.2)
        gn = s.b.js(GEOMETRY_JS)
        s.add("back to Now: Leaflet size == map container; view holds the main island and 澎湖",
              gn["mode"] == "mode-now" and leaflet_matches(gn) and contains(gn["view"], MAIN_ISLAND)
              and contains(gn["view"], PENGHU_MAIN), {"leaflet": gn["leaflet"], "view": gn["view"]})

        if w == 1440:
            # zoom floor on the 640 px desktop map (SPEC-V2 §5.3 R-V2-MAP-2)
            s.b.js("__map.setZoom(__map.getMinZoom(), {animate: false}); true")
            s.b.pump(0.8)
            z = s.b.js("(function(){var a=__map.latLngToContainerPoint([21.90,121]),"
                       "b=__map.latLngToContainerPoint([25.30,121]);"
                       "return {zoom: __map.getZoom(), ns: a.y-b.y, h: __map.getSize().y};})()")
            record["1440-zoom-floor"] = z
            s.add("zoom floor: at minZoom 6 the main island spans >= 25 % of the 640 px map",
                  z["zoom"] == 6 and z["h"] == 640 and z["ns"] / z["h"] >= 0.25, z)

            # resize 1440 -> 768 -> 375 -> 1440 on the same page
            s.b.js("__map.setZoom(8, {animate: false}); true")
            seq = []
            for rw, rh, rm in ((768, 1024, False), (375, 812, True), (1440, 900, False)):
                s.b.viewport(rw, rh, rm)
                s.b.pump(1.2)
                gr = s.b.js(GEOMETRY_JS)
                seq.append({"w": rw, "map": gr["map"]["h"], "leaflet": gr["leaflet"], "container": gr["container"],
                            "sw": gr["sw"], "view": gr["view"]})
            record["resize-sequence"] = seq
            s.add("resize 1440 -> 768 -> 375 -> 1440: map height follows 440 / 360 / 640, Leaflet size == container, "
                  "no horizontal scroll, the refitted view holds the main island and 澎湖",
                  [x["map"] for x in seq] == [440, 360, 640]
                  and all(x["leaflet"] == x["container"] and x["container"]["h"] > 0 and x["sw"] <= x["w"]
                          and contains(x["view"], MAIN_ISLAND) and contains(x["view"], PENGHU_MAIN) for x in seq),
                  seq)
    finally:
        s.close()


def scenario_dark(chrome: str, rig: Rig, out: Path, checks: Checks, record: dict) -> None:
    s = open_page(chrome, rig, out, checks, "1440-dark", 1440, 900, False, dark=True)
    try:
        g = s.b.js(GEOMETRY_JS)
        record["1440-dark"] = {"bg": g["bg"], "sw": g["sw"], "map": g["map"]}
        shots(s, "now")
        s.add("dark scheme renders with no horizontal scroll and the 640 px map", g["sw"] <= g["iw"]
              and g["map"]["h"] == 640, {"sw": g["sw"], "map": g["map"]["h"]})
    finally:
        s.close()


def run(chrome: str, out: Path) -> Checks:
    checks = Checks()
    record: dict = {}
    rig = Rig()
    add_variants(rig)
    try:
        for w, h in ((1440, 900), (1280, 900), (1024, 768), (768, 1024), (375, 812)):
            scenario_viewport(chrome, rig, out, checks, w, h, record)
        scenario_dark(chrome, rig, out, checks, record)
    finally:
        rig.close()
    out.mkdir(parents=True, exist_ok=True)
    (out / "browser-check-results.json").write_text(
        json.dumps({"checks": checks.items, "geometry": record}, ensure_ascii=False, indent=2), encoding="utf-8")
    return checks


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    checks = run(find_chrome(), args.out)
    n = len(checks.items)
    passed = sum(1 for i in checks.items if i["pass"])
    for i in checks.items:
        if not i["pass"]:
            print("FAIL", i["id"])
    print(f"{passed}/{n} checks passed; evidence in {args.out}")
    return 0 if checks.ok else 1


if __name__ == "__main__":
    sys.exit(main())
