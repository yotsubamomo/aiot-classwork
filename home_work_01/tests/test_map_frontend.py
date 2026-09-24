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


def _function_body(src: str, name: str) -> str:
    """Return the body (between the outermost braces) of ``function <name>(...)``,
    brace-matching while skipping string literals and comments so nested object
    literals, comment braces and string braces do not fool the matcher."""
    i = src.index("function " + name)
    # skip the parameter list
    p = src.index("(", i)
    depth = 0
    j = p
    while j < len(src):
        c = src[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        j += 1
    b = src.index("{", j)
    depth = 0
    k = b
    instr = None
    esc = False
    while k < len(src):
        c = src[k]
        two = src[k:k + 2]
        if instr is not None:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == instr:
                instr = None
        elif two == "//":
            k = src.index("\n", k)
            continue
        elif two == "/*":
            k = src.index("*/", k) + 2
            continue
        elif c in "\"'`":
            instr = c
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return src[b + 1:k]
        k += 1
    raise AssertionError(f"unbalanced braces for function {name}")


def _strip_comments(body: str) -> str:
    out = []
    i = 0
    n = len(body)
    instr = None
    esc = False
    while i < n:
        c = body[i]
        two = body[i:i + 2]
        if instr is not None:
            out.append(c)
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == instr:
                instr = None
            i += 1
        elif two == "//":
            i = body.index("\n", i) if "\n" in body[i:] else n
        elif two == "/*":
            i = body.index("*/", i) + 2
        elif c in "\"'`":
            instr = c
            out.append(c)
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


# --- init hardening (the NaN / 0x0 hazard, P-12) -------------------------------
# These are scoped to the actual function BODIES (comments stripped) so they FAIL
# when the guard is removed or the invalidateSize()->fitBounds() order is broken —
# i.e. they genuinely lock the hazard fix, not just the presence of some strings
# (#28 F-5).


def test_ensuremapsized_guards_on_nonzero_container_size() -> None:
    """ensureMapSized MUST early-return by calling the callback ONLY when the map
    container already has a non-zero box, and otherwise defer (ResizeObserver +
    visibilitychange). Removing the `if (sized())` guard so the callback runs
    unconditionally must fail this test."""
    body = _strip_comments(_function_body(_app_js(), "ensureMapSized"))
    # a real non-zero-size predicate
    assert "clientWidth > 0" in body and "clientHeight > 0" in body, (
        "ensureMapSized has no non-zero-size predicate"
    )
    # the immediate-run path MUST be guarded by sized()
    assert re.search(r"if\s*\(\s*sized\(\)\s*\)\s*\{\s*cb\(\)\s*;\s*return\s*;\s*\}", body), (
        "ensureMapSized calls cb() without first checking sized() — 0x0 init hazard unguarded"
    )
    # the deferred path uses ResizeObserver and visibilitychange
    assert "ResizeObserver" in body, "ensureMapSized does not observe the container size"
    assert "visibilitychange" in body, "ensureMapSized does not handle a hidden tab"
    # cb() is never called unconditionally: every cb() sits after a sized()/if guard
    for m in re.finditer(r"cb\(\)", body):
        pre = body[:m.start()]
        assert "sized()" in pre, "an unguarded cb() precedes the size check"


def test_fittomarkers_invalidatesize_precedes_fitbounds() -> None:
    """Inside the single fit function, invalidateSize() MUST run before fitBounds()
    so fitBounds measures real pixels (else infinite zoom -> NaN markers). Moving
    invalidateSize() after fitBounds() must fail this test."""
    body = _strip_comments(_function_body(_app_js(), "fitToMarkers"))
    inv = body.find("invalidateSize()")
    fit = body.find("fitBounds(")
    assert inv != -1, "fitToMarkers does not call invalidateSize()"
    assert fit != -1, "fitToMarkers does not call fitBounds()"
    assert inv < fit, "invalidateSize() must run before fitBounds() in fitToMarkers"


def test_init_path_is_wired_through_the_guard_and_single_fit() -> None:
    """The day path reaches the map through the size guard and the single fit."""
    src = _app_js()
    assert "ensureMapSized(function" in src, "applyDay must defer via ensureMapSized"
    assert _function_body(src, "initMap").count("fitToMarkers()") >= 1, (
        "initMap must fit via fitToMarkers()"
    )


def test_fitbounds_called_exactly_once() -> None:
    """fitBounds has exactly one call site (fitToMarkers). Changing Select Date must
    not reset the view (AC-18 / P-12); only init and resize re-fit."""
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
