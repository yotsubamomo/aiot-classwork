"""Static guards for the reworked Taiwan Map frontend (Issue #28).

Fully offline: these read the frontend source text (no browser, no network), so
they run in the same pytest suite and CI as the rest (R-TC-1, R-TC-5). They are
reproducible by a reviewer with only Python — no Node/jsdom/headless browser is
required (DR-20 P-12 allows a "pytest 驅動的檢查").

They guard the specific regressions this work item must not reintroduce:

* the ``Invalid LatLng (NaN, NaN)`` / 0x0-marker init hazard (P-12, task item 8):
  the map is only created once its container has a non-zero size, ``invalidateSize``
  runs before ``fitBounds``, and ``fitBounds`` is called exactly once (so changing
  Select Date never resets the view);
* H-3 / R-SHR-4 / AC-28 front-end side: the pills' value and colour come straight
  from the endpoint and the frontend re-derives / re-bands nothing;
* R-EN-5 / AC-17: the pill band colours and the legend swatch colours are the same
  four tokens;
* the vendored basemap is a same-origin JS global with finite geometry, no URL /
  key, and stays within the size budget.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_UNIT_DIR = Path(__file__).resolve().parent.parent
_STATIC = _UNIT_DIR / "static"
_APP_JS = _STATIC / "app.js"
_STYLES = _STATIC / "styles.css"
_INDEX = _STATIC / "index.html"
_BASEMAP = _STATIC / "data" / "basemap.js"


def _app_js() -> str:
    return _APP_JS.read_text(encoding="utf-8")


# --- init hardening (the NaN / 0x0 hazard, P-12) -------------------------------


def test_map_init_defers_until_container_has_nonzero_size() -> None:
    """The map must only initialise once its container reports a non-zero box."""
    src = _app_js()
    assert "ResizeObserver" in src, "no ResizeObserver: the 0x0 init hazard is unguarded"
    assert "visibilitychange" in src, "no visibilitychange guard for a hidden tab"
    # A real non-zero-size predicate on the map container.
    assert "clientWidth > 0" in src and "clientHeight > 0" in src, (
        "no non-zero-size guard before creating the map"
    )


def test_map_invalidates_size_before_fitbounds() -> None:
    """invalidateSize() must run before fitBounds() so fitBounds sees real pixels
    (otherwise it computes an infinite zoom and the markers become NaN)."""
    src = _app_js()
    inv = src.find("invalidateSize()")
    fit = src.find("fitBounds(")
    assert inv != -1, "invalidateSize() is missing"
    assert fit != -1, "fitBounds( is missing"
    assert inv < fit, "invalidateSize() must be called before fitBounds()"


def test_fitbounds_called_exactly_once() -> None:
    """fitBounds is called once (at init). Changing Select Date must not reset the
    view (AC-18 / P-12), so there must be no second fitBounds on the day path."""
    assert _app_js().count("fitBounds(") == 1


def test_representative_points_are_finite_and_within_taiwan() -> None:
    """Guard against NaN / out-of-range representative points feeding L.marker.

    All six [lat, lng] points must be finite and inside Taiwan's bounding box
    (a bad coordinate is a direct cause of ``Invalid LatLng``)."""
    src = _app_js()
    block = re.search(r"REGION_POINTS\s*=\s*\{(.+?)\};", src, re.DOTALL)
    assert block, "REGION_POINTS not found"
    pairs = re.findall(r"\[\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\]", block.group(1))
    assert len(pairs) == 6, f"expected 6 representative points, found {len(pairs)}"
    for lat_s, lng_s in pairs:
        lat, lng = float(lat_s), float(lng_s)
        assert 21.5 <= lat <= 26.5, f"lat {lat} outside Taiwan"
        assert 119.0 <= lng <= 122.5, f"lng {lng} outside Taiwan"


# --- H-3 / AC-28 front-end side: no re-derivation, no re-banding ---------------


def test_frontend_does_not_re_derive_or_re_band() -> None:
    """The pills take value + band from the endpoint; the frontend must not compute
    the derived average or the band thresholds itself (H-3, R-SHR-4, AC-28)."""
    for path in (_APP_JS, _BASEMAP):
        src = path.read_text(encoding="utf-8")
        # No derived-average arithmetic.
        assert not re.search(r"mint\s*\+\s*maxt", src), f"{path.name} re-derives the average"
        assert not re.search(r"maxt\s*\+\s*mint", src), f"{path.name} re-derives the average"
        # No band-threshold branching on temperature values (the 20/25/30 cutoffs
        # live only in the shared Python module).
        assert not re.search(r"[<>]=?\s*(?:20|25|30)\b", src), (
            f"{path.name} appears to re-band by a temperature threshold"
        )


def test_pill_uses_endpoint_value_and_band() -> None:
    """The pill text is the endpoint's derivedMapTemperature and its colour is the
    endpoint's colourBand (single-sourced, H-3)."""
    src = _app_js()
    assert "v.derivedMapTemperature" in src, "pill text must come from the endpoint value"
    assert "v.colourBand" in src, "pill colour must come from the endpoint band"


# --- R-EN-5 / AC-17: pill colours == legend colours ----------------------------


def test_band_colours_match_between_pills_and_legend_tokens() -> None:
    """The four band hex values used for the pills (app.js BAND_COLOURS) must equal
    the four --band-* CSS tokens the legend swatches are painted from."""
    src = _app_js()
    block = re.search(r"BAND_COLOURS\s*=\s*\{(.+?)\};", src, re.DOTALL)
    assert block, "BAND_COLOURS not found"
    js_bands = dict(
        re.findall(r"(blue|green|yellow|red):\s*\"(#[0-9a-fA-F]{6})\"", block.group(1))
    )
    assert set(js_bands) == {"blue", "green", "yellow", "red"}, js_bands
    css = _STYLES.read_text(encoding="utf-8")
    css_bands = dict(
        re.findall(r"--band-(blue|green|yellow|red):\s*(#[0-9a-fA-F]{6})", css)
    )
    assert set(css_bands) == {"blue", "green", "yellow", "red"}, css_bands
    for band in ("blue", "green", "yellow", "red"):
        assert js_bands[band].lower() == css_bands[band].lower(), (
            f"{band}: pill {js_bands[band]} != legend token {css_bands[band]}"
        )


# --- vendored basemap integrity ------------------------------------------------


def test_basemap_is_a_same_origin_global_with_no_url_or_key() -> None:
    src = _BASEMAP.read_text(encoding="utf-8")
    assert "window.TAIWAN_BASEMAP" in src
    assert "fetch(" not in src, "the basemap must be a global, not a fetch"
    assert not re.search(r"https?://", src), "the basemap must contain no absolute URL"
    assert "opendata.cwa.gov.tw" not in src and "CWA_API_KEY" not in src


def test_basemap_geometry_is_finite_and_within_budget() -> None:
    """The two vendored layers parse, carry finite coordinates, and the vendored
    data stays within the <= 300 KB budget (DR-20 P-2)."""
    src = _BASEMAP.read_text(encoding="utf-8")
    m = re.search(r"window\.TAIWAN_BASEMAP\s*=\s*Object\.freeze\((\{.*\})\);", src, re.DOTALL)
    assert m, "cannot find the TAIWAN_BASEMAP object literal"
    data = json.loads(m.group(1))
    assert set(data) >= {"context", "taiwan"}, data.keys()

    def coords_finite(node) -> bool:
        if isinstance(node, list):
            if node and isinstance(node[0], (int, float)):
                return all(isinstance(x, (int, float)) for x in node)
            return all(coords_finite(x) for x in node)
        return True

    for layer_name in ("context", "taiwan"):
        layer = data[layer_name]
        geoms = layer.get("geometries") or [f["geometry"] for f in layer.get("features", [])]
        assert geoms, f"{layer_name} has no geometry"
        for g in geoms:
            assert coords_finite(g["coordinates"]), f"{layer_name} has a non-finite coordinate"

    assert _BASEMAP.stat().st_size <= 300 * 1024, (
        f"vendored basemap is {_BASEMAP.stat().st_size} bytes (> 300 KB budget)"
    )


# --- the info panel wiring the page relies on ----------------------------------


def test_index_has_map_panel_select_date_and_legend() -> None:
    """The Select Date control lives in the map info panel and the four-band legend
    is present with the derived-average caveat (R-EN-3, R-EN-5, P-7)."""
    html = _INDEX.read_text(encoding="utf-8")
    assert 'id="date-select"' in html
    assert ">Select Date</label>" in html
    assert html.count('class="band-swatch"') == 4
    assert "not an observed daily mean" in html
    assert 'src="/static/data/basemap.js"' in html
