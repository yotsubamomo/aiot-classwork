"""Static guards for Taiwan → County → Station (Issue #38, SPEC-V2 §2.3).

Fully offline (R-V2-TC-3): these read ``static/index.html``, ``static/app.js``,
``static/data/counties.js`` and ``static/data/basemap.js`` as text and check the
county-name join against the committed sanitised sample — no browser, no
network. Behaviour in a real browser (hover, select, County context, list,
detail, Back to Taiwan, the round trip, Stale / Unavailable) is exercised by the
reproducible ``tests/check_county_browser.py``; these guards pin the source-level
properties so a regression fails CI:

* R-V2-DD-1 / DD-4: the vendored county names are the 22 CountyName strings, one
  per basemap polygon, and each polygon really is that county (sample stations);
  same-origin script, no URL, no key; the layer is Now-mode only and never
  coloured by data.
* R-V2-DD-11: the frontend's map range equals ``representative.MAP_RANGE``.
* R-V2-DD-5(c), INV-V2-5 (H-3): the County context computes no aggregate; with no
  Latest Observation every value is "—", never 0 (DV-21 §4.2).
* R-V2-DD-6..9: list items are buttons, a non-map county chooser exists,
  ``Back to Taiwan`` is a verbatim button that clears both selections.
* R-V2-MODE-5(a) (DV-20): the mode switch never clears the county selection.
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

import observation
import representative
from tests.test_map_frontend import _function_body, _strip_comments
from tests.test_modes_frontend import _inside, _mode_of, _tree

_UNIT = Path(__file__).resolve().parent.parent
_STATIC = _UNIT / "static"
_INDEX = _STATIC / "index.html"
_APP_JS = _STATIC / "app.js"
_COUNTIES = _STATIC / "data" / "counties.js"
_BASEMAP = _STATIC / "data" / "basemap.js"
_SAMPLE = _UNIT / "tests" / "fixtures" / "O-A0001-001_sample.json"


def _js() -> str:
    return _APP_JS.read_text(encoding="utf-8")


def _body(name: str) -> str:
    return _strip_comments(_function_body(_js(), name))


def _names() -> list[str]:
    src = _COUNTIES.read_text(encoding="utf-8")
    m = re.search(r"window\.TAIWAN_COUNTY_NAMES\s*=\s*Object\.freeze\((\[.*?\])\);", src, re.DOTALL)
    assert m, "cannot find the TAIWAN_COUNTY_NAMES array literal"
    return json.loads(m.group(1))


def _taiwan_geometries() -> list[dict]:
    src = _BASEMAP.read_text(encoding="utf-8")
    m = re.search(r"window\.TAIWAN_BASEMAP\s*=\s*Object\.freeze\((\{.*\})\);", src, re.DOTALL)
    assert m
    return json.loads(m.group(1))["taiwan"]["geometries"]


def _in_ring(x: float, y: float, ring: list) -> bool:
    inside = False
    for k in range(len(ring)):
        x1, y1 = ring[k]
        x2, y2 = ring[k - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def _in_geometry(lng: float, lat: float, g: dict) -> bool:
    polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    return any(_in_ring(lng, lat, p[0]) and not any(_in_ring(lng, lat, h) for h in p[1:]) for p in polys)


def _js_list(name: str) -> list[str]:
    m = re.search(r"var " + name + r"\s*=\s*\[(.*?)\];", _js(), re.DOTALL)
    assert m, name
    return re.findall(r'"([^"]+)"', m.group(1))


# --- R-V2-DD-1 / DD-4: the vendored names and their join with the polygons ----------


def test_county_names_are_a_same_origin_global_with_no_url_or_key() -> None:
    src = _COUNTIES.read_text(encoding="utf-8")
    assert "window.TAIWAN_COUNTY_NAMES" in src
    assert "fetch(" not in src and not re.search(r"https?://|//[a-z0-9.-]+\.[a-z]{2,}/", src)
    assert "opendata.cwa.gov.tw" not in src and "CWA_API_KEY" not in src
    html = _INDEX.read_text(encoding="utf-8")
    b, c, a = (html.index(f'src="/static/{p}"') for p in ("data/basemap.js", "data/counties.js", "app.js"))
    assert b < c < a, "counties.js must load after the basemap and before the app"


def test_the_22_names_are_the_22_counties_once_each_one_per_polygon() -> None:
    names = _names()
    assert len(names) == 22 and len(set(names)) == 22
    assert set(names) == set(representative.COUNTY_ORDER) == set(observation.COUNTIES)
    assert all("台" not in n for n in names), "CountyName uses 臺, never 台"
    assert len(_taiwan_geometries()) == len(names), "one name per basemap polygon"


def test_each_polygon_is_the_county_it_is_named() -> None:
    """Join check against the committed sample: every polygon's majority of the
    valid stations inside it are of the county named for it, and (almost) every
    on-map valid station lies in its own county's polygon (the simplified
    coastline can leave a few coastal / tiny-islet stations just outside)."""
    names = _names()
    geoms = _taiwan_geometries()
    stations = observation.normalize(json.loads(_SAMPLE.read_text(encoding="utf-8"))).stations
    for name, g in zip(names, geoms):
        inside = collections.Counter(s["countyName"] for s in stations
                                     if _in_geometry(s["longitude"], s["latitude"], g))
        assert inside, f"no sample station inside the polygon named {name}"
        top, n = inside.most_common(1)[0]
        assert top == name, f"polygon named {name} holds mostly {top} stations"
        assert n / sum(inside.values()) >= 0.9, (name, inside)
    on_map = [s for s in stations if representative.in_map_range(s)]
    own = sum(_in_geometry(s["longitude"], s["latitude"], geoms[names.index(s["countyName"])]) for s in on_map)
    assert own / len(on_map) >= 0.98, f"{own}/{len(on_map)} on-map stations inside their county polygon"


def test_frontend_county_order_and_map_range_equal_the_backend() -> None:
    assert _js_list("COUNTY_ORDER") == list(representative.COUNTY_ORDER)
    m = re.search(r"var MAP_RANGE\s*=\s*\{\s*latitude:\s*\[([^\]]+)\],\s*longitude:\s*\[([^\]]+)\]\s*\}", _js())
    assert m, "MAP_RANGE not found in app.js"
    lat = tuple(float(x) for x in m.group(1).split(","))
    lng = tuple(float(x) for x in m.group(2).split(","))
    assert lat == tuple(representative.MAP_RANGE["latitude"])
    assert lng == tuple(representative.MAP_RANGE["longitude"])
    body = _body("onMap")
    assert "MAP_RANGE.latitude[0]" in body and "MAP_RANGE.longitude[1]" in body and "<=" in body


# --- R-V2-DD-4: interaction only, Now mode only ---------------------------------------


def test_county_layer_is_interaction_geometry_never_coloured_by_data() -> None:
    style = _body("countyStyle")
    for data_word in ("airTemperature", "obs", "stations", "BAND_COLOURS", "colourBand"):
        assert data_word not in style, f"countyStyle depends on {data_word}"
    colours = set(re.findall(r'"(#[0-9a-fA-F]{6})"', style))
    assert colours and colours <= {"#fbbf24", "#9ed0ff"}, colours
    build = _body("buildCountyLayer")
    assert "TAIWAN_COUNTY_NAMES" in build and "countyName" in build
    for event in ('"mouseover"', '"mouseout"', '"click"', "bindTooltip("):
        assert event in build, event


def test_county_polygons_are_never_keyboard_tab_stops() -> None:
    """#38 cycle 1 F-1: the bound tooltip gives each path focus listeners, which
    Chromium turns into an invisible, inert Tab stop. Every county path must get
    tabindex="-1" each time it is (re)created on the map (DD-9(d), DD-9(e))."""
    build = _body("buildCountyLayer")
    add = build[build.index('layer.on("add"'):]
    assert 'setAttribute("tabindex", "-1")' in add[:add.index("});")], (
        "county paths must be taken out of the Tab order on every add")
    assert "bindTooltip(" in build  # the reason the guard is needed stays visible here
    # the keyboard path to a county is the chooser, a native <select>
    assert _tree().by_id["county-select"]["tag"] == "select"


def test_county_layer_is_on_the_map_only_in_now_mode() -> None:
    sync = _body("syncMap")
    forecast = sync[sync.index("if (mode === MODE_FORECAST)"):sync.index("} else {")]
    now = sync[sync.index("} else {"):]
    assert "map.removeLayer(countyLayer)" in forecast
    assert "countyLayer.addTo(map)" in now
    assert "if (mode === MODE_NOW && countyLayer) countyLayer.addTo(map);" in _body("initMap")


# --- R-V2-DD-5 / INV-V2-5 (H-3) / DV-21 §4.2 -------------------------------------------


def test_county_context_computes_no_aggregate() -> None:
    for fn in ("renderCountyContext", "highestStation", "lowestStation", "extremeText",
               "renderCountyList", "countyStations", "byTemperatureDesc"):
        body = _body(fn)
        assert "reduce(" not in body, fn
        assert not re.search(r"\b(sum|total|avg|average|mean)\b", body, re.IGNORECASE), fn
        assert not re.search(r"/\s*(list|st|stations)\.length", body), fn
        assert "+=" not in body, fn


def test_no_average_wording_in_the_now_mode_texts() -> None:
    tree = _tree()
    html = _INDEX.read_text(encoding="utf-8")
    start = html.index('id="now-panel"')
    now_html = html[start:html.index('id="forecast-panel"')]
    visible = re.sub(r"<!--.*?-->", "", now_html, flags=re.DOTALL)
    assert not re.search(r"\b(average|mean)\b|平均", re.sub(r"<[^>]+>", " ", visible), re.IGNORECASE)
    for fn in ("renderCountyContext", "renderCountyList", "renderCountySelection", "renderObsState"):
        literals = " ".join(re.findall(r'"([^"]*)"', _body(fn)))
        assert not re.search(r"\b(average|mean)\b|平均", literals, re.IGNORECASE), fn
    assert _mode_of(tree.by_id["county-context"]) == "now"


def test_unavailable_county_context_is_dashes_never_zero() -> None:
    body = _body("renderCountyContext")
    branch = body[body.index("if (!obs) {"):body.index("} else {")]
    for field in ("countyCount", "countyOnMap", "countyMax", "countyMin"):
        assert f"els.{field}.textContent = MISSING;" in branch, field
    assert "String(" not in branch and "length" not in branch
    # the count is only ever the length of an actual station set
    assert body.index("if (!obs) {") < body.index("String(list.length)")
    assert "if (!obs || !Array.isArray(obs.stations)) return [];" in _body("countyStations")
    lst = _body("renderCountyList")
    assert 'obs ? "Stations (" + list.length + ")" : "Stations"' in lst


def test_county_context_shows_the_observation_state() -> None:
    body = _body("renderObsState")
    assert "els.countyState.hidden = !shown;" in body
    assert '"Stale' in body and "unavailable" in body


# --- R-V2-DD-6..9: list, chooser, Back to Taiwan ----------------------------------------


def test_station_list_items_are_buttons_and_update_the_detail() -> None:
    body = _body("renderCountyList")
    assert 'document.createElement("button")' in body and 'btn.type = "button"' in body
    assert "selectStation(s.stationId)" in body
    assert "not on the map</span>" in body and "onMap(s)" in body, (
        "off-map stations are listed and marked (DD-11)")
    sel = _body("selectStation")
    assert "renderSelectedStation()" in sel and "markListSelection()" in sel


def test_station_detail_has_every_required_and_optional_field() -> None:
    html = _INDEX.read_text(encoding="utf-8")
    for label, id_ in (("StationId", "obs-sel-id"), ("Air temperature", "obs-sel-temp"),
                       ("Relative humidity", "obs-sel-rh"), ("Wind speed", "obs-sel-wind"),
                       ("Wind direction", "obs-sel-wdir"), ("Air pressure", "obs-sel-pres"),
                       ("Precipitation (today)", "obs-sel-rain"), ("Weather", "obs-sel-weather"),
                       ("Observation Time", "obs-sel-time")):
        assert f'<span>{label}</span><span id="{id_}">' in html, label
    body = _body("renderSelectedStation")
    for field in ("stationId", "countyName", "townName", "observationTime", "airTemperature",
                  "relativeHumidity", "windSpeed", "windDirection", "airPressure", "precipitation",
                  "weather"):
        assert "s." + field in body, field
    assert "els.obsSelOffmap.hidden = onMap(s);" in body


def test_non_map_county_chooser_and_back_to_taiwan() -> None:
    tree = _tree()
    select = tree.by_id["county-select"]
    assert select["tag"] == "select" and _inside(select, "now-panel") and _mode_of(select) == "now"
    html = _INDEX.read_text(encoding="utf-8")
    assert '<label class="map-control__label" for="county-select">County</label>' in html
    back = tree.by_id["back-to-taiwan"]
    assert back["tag"] == "button" and back["attrs"].get("type") == "button"
    assert ">Back to Taiwan</button>" in html, "Back to Taiwan must be verbatim (AC-V2-23)"
    body = _body("backToTaiwan")
    assert "selectedCounty = null;" in body and "selectedStationId = null;" in body
    assert "fitToMarkers()" in body, "Back to Taiwan returns to the initial Taiwan-wide view"


def test_county_markers_are_the_on_map_stations_and_not_tab_stops() -> None:
    body = _body("renderStations")
    assert "countyStations(selectedCounty).filter(onMap)" in body
    assert "representativeIds()" in body
    assert 'inCounty ? "-1" : "0"' in _body("stationIcon")


# --- R-V2-MODE-5(a) / DV-20: the round trip keeps the county ---------------------------


def test_mode_switch_never_clears_the_county_selection() -> None:
    for fn in ("setMode", "syncMap", "restoreNowView", "renderModeChrome", "showSixRegions"):
        body = _body(fn)
        assert "selectedCounty =" not in body and "selectedStationId =" not in body, fn
    # only the county actions change it
    writers = re.findall(r"(?<!var )\bselectedCounty = [^;]*;", _js())
    assert writers == ["selectedCounty = name;", "selectedCounty = null;"], (
        "selectedCounty is written only by selectCounty and backToTaiwan")
    assert "selectedCounty = name;" in _body("selectCounty")
    assert "selectedCounty = null;" in _body("backToTaiwan")
