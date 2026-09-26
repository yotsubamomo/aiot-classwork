"""Static guards for the map fence and responsive usability (Issue #39).

Offline and browser-free, like ``test_map_frontend.py`` (whose V1 init-guard
tests stay unchanged): they read the frontend source text. They lock:

* the fence and zoom range (R-V2-MAP-1..3): Leaflet's ``maxBounds`` is the map
  range E with a hard edge, and ``minZoom`` / ``maxZoom`` still satisfy the
  SPEC-V2 §5.3 product criteria, recomputed here with the Web Mercator formulas;
* the Now mode's initial view (R-V2-MAP-4): the fitted box holds the main
  island and 澎湖 and lies in E;
* the non-zero-size guard on the new paths (R-V2-MAP-5): the info panel's open /
  close / expand path and the resize path go through ``ensureMapSized`` and
  measure the map (``invalidateSize``) before any view change;
* the 375 px info panel (R-V2-RSP-5): a real Close button with visible text, Esc,
  a peek size of at most half the map, an expanded size that leaves the zoom
  buttons clear;
* 44 x 44 touch targets and marker density (R-V2-RSP-3, RSP-7);
* the desktop Now panel beside the map, never floating over it (R-V2-RSP-6).
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import representative
from tests.test_map_frontend import _function_body, _strip_comments

_UNIT_DIR = Path(__file__).resolve().parent.parent
_STATIC = _UNIT_DIR / "static"
_JS = (_STATIC / "app.js").read_text(encoding="utf-8")
_CSS = (_STATIC / "styles.css").read_text(encoding="utf-8")
_HTML = (_STATIC / "index.html").read_text(encoding="utf-8")

EARTH_M = 40075016.686
MAIN_ISLAND = {"s": 21.90, "n": 25.30, "w": 120.03, "e": 122.01}
PENGHU_MAIN = {"s": 23.52, "n": 23.66, "w": 119.52, "e": 119.70}
MAP_HEIGHTS = {"desktop": 560, "tablet": 440, "phone": 360}  # styles.css .map heights (DR-20 P-1)


def _body(name: str) -> str:
    return _strip_comments(_function_body(_JS, name))


def _num(name: str) -> float:
    m = re.search(r"var " + name + r" = (\d+(?:\.\d+)?);", _JS)
    assert m, f"{name} not found"
    return float(m.group(1))


def _y(lat: float, z: float) -> float:
    s = math.sin(math.radians(lat))
    return (0.5 - math.log((1 + s) / (1 - s)) / (4 * math.pi)) * 256 * 2 ** z


def _px_per_km(lat: float, z: float) -> float:
    return 256 * 2 ** z / (EARTH_M * math.cos(math.radians(lat))) * 1000


# --- R-V2-MAP-1..3: fence and zoom range ------------------------------------------------


def test_leaflet_map_is_fenced_to_the_map_range_with_the_zoom_range() -> None:
    init = _body("initMap")
    assert "minZoom: MIN_ZOOM" in init and "maxZoom: MAX_ZOOM" in init
    assert "maxBoundsViscosity: 1.0" in init, "the fence must be a hard edge"
    assert re.search(r"maxBounds: L\.latLngBounds\(\s*\[MAP_RANGE\.latitude\[0\], MAP_RANGE\.longitude\[0\]\],\s*"
                     r"\[MAP_RANGE\.latitude\[1\], MAP_RANGE\.longitude\[1\]\]\s*\)", init), "maxBounds must be E"
    m = re.search(r"var MAP_RANGE = \{ latitude: \[([\d.]+), ([\d.]+)\], longitude: \[([\d.]+), ([\d.]+)\] \};", _JS)
    assert m and (float(m.group(1)), float(m.group(2))) == tuple(representative.MAP_RANGE["latitude"])
    assert (float(m.group(3)), float(m.group(4))) == tuple(representative.MAP_RANGE["longitude"])


def test_zoom_floor_keeps_the_main_island_at_least_a_quarter_of_the_map_height() -> None:
    """R-V2-MAP-2: at minZoom the main island's north–south extent is >= 25 % of the
    map's height in every layout (the map is at most 560 px tall)."""
    z = _num("MIN_ZOOM")
    ns = _y(MAIN_ISLAND["s"], z) - _y(MAIN_ISLAND["n"], z)
    for layout, height in MAP_HEIGHTS.items():
        assert ns / height >= 0.25, (layout, round(ns / height, 3))
    assert _num("MIN_ZOOM") - 1 >= 0
    # one level further out would fail at the desktop height: the floor is meaningful
    assert (_y(MAIN_ISLAND["s"], z - 1) - _y(MAIN_ISLAND["n"], z - 1)) / MAP_HEIGHTS["desktop"] < 0.25


def test_zoom_ceiling_selects_stations_without_meaningless_over_zoom() -> None:
    """R-V2-MAP-3: at maxZoom 1 km >= 20 CSS px everywhere in E, and a 375 px wide map
    still spans >= 5 km everywhere in E."""
    z = _num("MAX_ZOOM")
    lat_lo, lat_hi = representative.MAP_RANGE["latitude"]
    assert min(_px_per_km(lat_lo, z), _px_per_km(lat_hi, z)) >= 20
    assert 375 / max(_px_per_km(lat_lo, z), _px_per_km(lat_hi, z)) >= 5
    assert _num("COUNTY_MAX_ZOOM") <= z


def test_initial_now_view_box_holds_the_main_island_and_penghu_inside_e() -> None:
    """R-V2-MAP-4: the box the Now mode fits at load and after Back to Taiwan."""
    m = re.search(r"var NOW_INITIAL_BOUNDS = \[\[([\d.]+), ([\d.]+)\], \[([\d.]+), ([\d.]+)\]\];", _JS)
    assert m
    s, w, n, e = (float(m.group(i)) for i in range(1, 5))
    for box in (MAIN_ISLAND, PENGHU_MAIN):
        assert s <= box["s"] and n >= box["n"] and w <= box["w"] and e >= box["e"], box
    lat_lo, lat_hi = representative.MAP_RANGE["latitude"]
    lng_lo, lng_hi = representative.MAP_RANGE["longitude"]
    assert lat_lo <= s and n <= lat_hi and lng_lo <= w and e <= lng_hi
    assert "fitToMarkers()" in _body("backToTaiwan")


def test_every_fit_settles_inside_the_fence_at_once() -> None:
    """A fit is not animated and is followed by panInsideBounds(maxBounds), after
    fitBounds and still after invalidateSize (the V1 order is kept)."""
    body = _body("fitToMarkers")
    inv, fit = body.index("invalidateSize()"), body.index("fitBounds(")
    pan = body.index("panInsideBounds(map.options.maxBounds, { animate: false })")
    assert inv < fit < pan
    assert "animate: false" in body[fit:pan]
    assert _JS.count("fitBounds(") == 1


def test_reveal_limits_its_view_to_the_fence() -> None:
    body = _body("reveal")
    assert "_limitCenter(" in body and "map.options.maxBounds" in body
    assert "setView(center, z, { animate: false })" in body
    assert "map.getMaxZoom()" in body


# --- R-V2-MAP-5: the non-zero-size guard on the info panel and resize paths ---------------


def test_info_panel_changes_go_through_the_size_guard() -> None:
    body = _body("afterSheetChange")
    assert "ensureMapSized(function" in body
    guarded = body[body.index("ensureMapSized(function"):]
    assert guarded.index("invalidateSize()") < guarded.index("revealSelection()")
    for fn in ("closeSheet", "reopenSheet", "toggleSheetExpanded", "selectStation", "selectCounty", "backToTaiwan"):
        assert "afterSheetChange(" in _body(fn), fn


def test_resize_goes_through_the_size_guard() -> None:
    handler = _JS[_JS.index('window.addEventListener("resize"'):]
    handler = handler[:handler.index("});")]
    assert "ensureMapSized(resizeMap)" in handler
    assert "fitBounds(" not in handler and "invalidateSize" not in handler
    body = _body("resizeMap")
    assert "fitBounds(" not in body, "resize fits only through fitToMarkers (guarded order)"
    assert "fitToMarkers()" in body and "invalidateSize()" in body


# --- R-V2-RSP-5: the 375 px info panel -------------------------------------------------------


def test_info_panel_markup_has_a_visible_keyboard_close() -> None:
    now = _HTML[_HTML.index('id="now-panel"'):_HTML.index('id="forecast-panel"')]
    assert 'id="info-sheet"' in now, "the info panel belongs to the Now panel"
    close = re.search(r'<button type="button" id="sheet-close"[^>]*>(.*?)</button>', now)
    assert close and "Close" in re.sub(r"<[^>]+>", "", close.group(1)), "Close has visible text"
    assert re.search(r'<button type="button" id="sheet-expand"[^>]*aria-expanded="false"', now)
    assert re.search(r'<button type="button" id="sheet-reopen"', now)
    assert re.search(r'<button type="button" id="back-to-taiwan"', now)
    # Back to Taiwan is outside the panel that can be closed
    assert now.index('id="back-to-taiwan"') < now.index('id="info-sheet"')
    wiring = _JS[_JS.index('els.sheetClose.addEventListener("click", closeSheet);'):]
    wiring = wiring[:wiring.index("// Redraw the chart")]
    assert '"Escape"' in wiring and "closeSheet()" in wiring


def test_info_panel_sizes_keep_the_map_and_zoom_buttons() -> None:
    """Peek <= 50 % of the map height; expanded stops below the 2 x 44 px zoom
    buttons (10 px margin + borders)."""
    peeks = [int(x) for x in re.findall(r'\.sheet\[data-sheet="peek"\] \{ max-height: (\d+)px; \}', _CSS)]
    assert sorted(peeks) == [172, 212]
    assert 172 <= MAP_HEIGHTS["phone"] / 2 and 212 <= MAP_HEIGHTS["tablet"] / 2
    exp = re.findall(r'\.sheet\[data-sheet="expanded"\] \{ max-height: calc\((\d+)px - (\d+)px\); \}', _CSS)
    assert sorted((int(a), int(b)) for a, b in exp) == [(360, 104), (440, 104)]
    assert 104 >= 10 + 2 * 44 + 4
    assert '.sheet[data-sheet="empty"], .sheet[data-sheet="closed"] { display: none; }' in _CSS


def test_closing_keeps_focus_and_the_selection() -> None:
    body = _body("closeSheet")
    assert "sheetOpen = false;" in body and "selectedCounty" not in body and "selectedStationId" not in body
    assert "els.sheetReopen.focus()" in body
    assert "els.sheetClose.focus()" in _body("reopenSheet")


# --- R-V2-RSP-3 / RSP-7 / RSP-6 --------------------------------------------------------------


def test_touch_targets_are_44_px() -> None:
    assert _num("TOUCH") == 44
    zoom = _CSS[_CSS.index(".leaflet-control-zoom a,\n.leaflet-touch .leaflet-control-zoom a {"):]
    zoom = zoom[:zoom.index("}")]
    assert "width: 44px" in zoom and "height: 44px" in zoom
    spill = _CSS[_CSS.index(".spill::before {"):]
    spill = spill[:spill.index("}")]
    assert "min-width: 44px" in spill and "height: 44px" in spill
    sheet_btn = _CSS[_CSS.index(".btn {"):]
    sheet_btn = sheet_btn[:sheet_btn.index("}")]
    assert "min-height: 44px" in sheet_btn and "min-width: 44px" in sheet_btn


def test_density_rule_ranks_every_county_and_hides_without_removing() -> None:
    m = re.search(r"var DENSITY_PRIORITY = \[(.*?)\];", _JS, re.DOTALL)
    names = re.findall(r'"([^"]+)"', m.group(1))
    assert sorted(names) == sorted(representative.COUNTY_ORDER) and len(names) == 22
    assert ".station-icon.is-culled { visibility: hidden; }" in _CSS
    body = _body("updateMarkerAccess")
    assert 'classList.toggle("is-culled", hidden)' in body
    assert 'renderedCounty || hidden || covered ? "-1" : "0"' in body, "a hidden or covered marker is never a Tab stop"
    rank = _body("densityRank")
    assert "id === selectedStationId) return -3" in rank, "the selected station is always shown"


def test_mouse_focus_does_not_move_the_map() -> None:
    body = _body("wireStationMarker")
    assert 'pill.matches(":focus-visible")' in body and "keepInClearArea(" in body


def test_desktop_now_panel_sits_beside_the_map() -> None:
    block = _CSS[_CSS.index("@media (min-width: 1024px) {\n  .map-shell.map-shell--now {"):]
    block = block[:block.index("\n}\n")]
    assert "display: grid;" in block and "grid-template-columns: 312px minmax(0, 1fr);" in block
    assert ".map-shell--now .map-panel--now {\n    position: static;" in block
    assert 'classList.toggle("map-shell--now", mode === MODE_NOW)' in _body("renderModeChrome")
    pad = _body("fitPadding")
    assert "{ tl: [24, 24], br: [24, 24 + sheetCover()] }" in pad
    assert "{ tl: [392, 64], br: [300, 56] }" in pad, "Forecast mode keeps the V1 padding"


def test_tooltips_are_kept_inside_the_map() -> None:
    body = _body("keepTooltipsInsideMap")
    assert "L.Tooltip" in body and "_setPosition" in body and "clamp(" in body
    init = _body("initMap")
    assert init.index("keepTooltipsInsideMap()") < init.index('L.map("map"')
