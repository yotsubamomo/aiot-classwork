"""Static guards for the V2 Now mode / Forecast mode frontend (Issue #36).

Fully offline (R-V2-TC-3): these read ``static/index.html``, ``static/app.js`` and
``static/styles.css`` as text — no browser, no network — so they run in the same
pytest suite and CI as the rest. Behaviour in a real browser (both modes, the
round trip, the forecast-503 case, the network log) is exercised by the
reproducible ``tests/check_modes_browser.py``; these guards pin the source-level
properties so a regression fails CI:

* R-V2-MODE-1/2: the page opens in Now mode; the switch is two real buttons with
  visible "Now" / "Forecast" text and aria-pressed.
* R-V2-DEG-1 / INV-V2-7: the Now mode's observation load is not gated on
  ``/api/health``; the V1 page-level states are scoped to the forecast section.
* R-V2-MODE-4/6, INV-V2-5 (H-3): mode-owned controls, the derived legend only in
  Forecast mode, no colour scale shared with the observation markers, verbatim
  labels, no real-time / live wording, the DR-17 label left unchanged.
* R-V2-MAP-5: the mode-switch path goes through the non-zero-size guard and
  recomputes the size before any view change.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

from tests.test_map_frontend import _function_body, _strip_comments

_STATIC = Path(__file__).resolve().parent.parent / "static"
_INDEX = _STATIC / "index.html"
_APP_JS = _STATIC / "app.js"
_STYLES = _STATIC / "styles.css"
_CONTEXT = _STATIC.parent / "CONTEXT.md"
_BRIEF_V2 = _STATIC.parent / "doc" / "brief" / "BRIEF-V2.md"

REGIONS = ["北部地區", "中部地區", "南部地區", "東北部地區", "東部地區", "東南部地區"]


def _html() -> str:
    return _INDEX.read_text(encoding="utf-8")


def _js() -> str:
    return _APP_JS.read_text(encoding="utf-8")


def _body(name: str) -> str:
    return _strip_comments(_function_body(_js(), name))


class _Tree(HTMLParser):
    """Records, for every element with an id, the ids and data-mode values of
    its ancestors (void elements do not nest)."""

    VOID = {"meta", "link", "br", "img", "input", "hr", "source"}

    def __init__(self) -> None:
        super().__init__()
        self.stack: list[dict] = []
        self.by_id: dict[str, dict] = {}

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        node = {"tag": tag, "attrs": a,
                "ancestors": [dict(n["attrs"]) for n in self.stack]}
        if "id" in a:
            self.by_id[a["id"]] = node
        if tag not in self.VOID:
            self.stack.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                break


def _tree() -> _Tree:
    t = _Tree()
    t.feed(_html())
    return t


def _mode_of(node: dict) -> str | None:
    for attrs in [node["attrs"]] + list(reversed(node["ancestors"])):
        if "data-mode" in attrs:
            return attrs["data-mode"]
    return None


def _inside(node: dict, ancestor_id: str) -> bool:
    return any(a.get("id") == ancestor_id for a in node["ancestors"])


# --- R-V2-MODE-1 / MODE-2: default Now mode and the switch ----------------------


def test_page_opens_in_now_mode() -> None:
    js = _js()
    assert re.search(r'var MODE_NOW = "now";', js)
    assert re.search(r"var mode = MODE_NOW;", js), "the initial mode must be Now"
    t = _tree()
    assert t.by_id["mode-now"]["attrs"].get("aria-pressed") == "true"
    assert t.by_id["mode-forecast"]["attrs"].get("aria-pressed") == "false"
    # Forecast-owned elements start hidden; the Now panel does not.
    assert "hidden" in t.by_id["forecast-panel"]["attrs"]
    assert "hidden" in t.by_id["forecast-legend"]["attrs"]
    assert "hidden" not in t.by_id["now-panel"]["attrs"]


def test_mode_switch_is_two_labelled_buttons() -> None:
    html = _html()
    for mode_id, word in (("mode-now", "Now"), ("mode-forecast", "Forecast")):
        m = re.search(r'<button type="button"[^>]*id="' + mode_id + r'"[^>]*>(.*?)</button>', html, re.S)
        assert m, f"{mode_id} is not a <button type=button>"
        visible = re.sub(r"<[^>]+>", "", m.group(1))
        assert word in visible, f"{mode_id} visible text lacks {word!r}"
        assert "aria-pressed=" in m.group(0)
    # The switch sits in the map card head, before the map (visible without scrolling).
    assert html.index('class="mode-toggle"') < html.index('id="map-frame"')


def test_mode_buttons_drive_setmode() -> None:
    body = _body("renderModeChrome")
    assert "aria-pressed" in body
    assert 'getAttribute("data-mode")' in body and ".hidden" in body


# --- R-V2-DEG-1 / DEG-3: Now mode independent of the forecast snapshot ------------


def test_observation_load_is_not_gated_on_health() -> None:
    js = _js()
    handler = js[js.index('document.addEventListener("DOMContentLoaded"'):]
    handler = handler[:handler.index("\n  });\n") + 1]
    # Called directly at page load (4-space statement level of the handler) —
    # not only from the Refresh button's listener — beside the forecast bootstrap.
    assert re.search(r"\n    loadObservation\(\);\n", handler), "the Now mode does not load on its own"
    assert re.search(r"\n    bootstrap\(\);\n", handler)
    for fn in ("bootstrap", "loadRegions", "showDashboard"):
        assert "loadObservation" not in _body(fn), f"{fn} gates the Now mode on the forecast"
    # #37 moved the request into requestObservation() (bounded in time), which
    # loadObservation() calls; the endpoint literal is pinned there.
    assert "requestObservation()" in _body("loadObservation")
    assert 'fetch("/api/observations/latest"' in _body("requestObservation")


def test_v1_page_states_are_scoped_to_the_forecast_section() -> None:
    t = _tree()
    for el in ("page-error", "page-loading", "page-empty", "dashboard"):
        assert _inside(t.by_id[el], "forecast-section"), f"#{el} must be inside the forecast section"
    assert t.by_id["page-error"]["attrs"].get("role") == "alert"
    # The map (both modes and the switch) is outside the forecast section.
    for el in ("map", "mode-now", "now-panel", "forecast-panel"):
        assert not _inside(t.by_id[el], "forecast-section"), f"#{el} must not be hidden with the forecast"
        assert not _inside(t.by_id[el], "dashboard")


def test_forecast_failure_is_shown_inline_in_forecast_mode() -> None:
    body = _body("showError")
    assert "setDateSelectEnabled(false)" in body
    assert 'setMapStatus(message, "error")' in body
    # the inline status is only rendered in Forecast mode
    assert "mode === MODE_FORECAST ? forecastMapStatus : null" in _body("renderMapStatus")


# --- R-V2-MODE-4 / MODE-6 (H-3): what belongs to which mode ------------------------


def test_controls_and_legend_belong_to_their_mode() -> None:
    t = _tree()
    for el in ("date-select", "forecast-legend", "map-forecast-day", "sel-derived"):
        assert _mode_of(t.by_id[el]) == "forecast", el
    for el in ("refresh-button", "obs-time", "obs-fetched", "obs-count", "obs-selected"):
        assert _mode_of(t.by_id[el]) == "now", el
    # the band swatches exist only inside the Forecast mode legend
    html = _html()
    legend = html[html.index('id="forecast-legend"'):]
    legend = legend[:legend.index("</div>\n      </div>")]
    assert legend.count('class="band-swatch"') == html.count('class="band-swatch"') == 4


def test_verbatim_labels() -> None:
    html = _html()
    assert "<dt>Observation Time</dt>" in html
    assert "<dt>Fetched Time</dt>" in html
    assert re.search(r'id="refresh-button"[^>]*>Refresh</button>', html)
    assert "Latest Observation" in html
    # H-2: V1 page words unchanged
    assert ">Taiwan Weather Forecast</h1>" in html
    assert ">Select Region</label>" in html and ">Select Date</label>" in html
    for header in ("Date", "MinT", "MaxT"):
        assert f'<th scope="col">{header}</th>' in html
    assert re.search(r"var REGION_ORDER = \[\s*" + r",\s*".join(f'"{r}"' for r in REGIONS), _js())


def test_no_real_time_or_live_wording() -> None:
    for path in (_INDEX, _APP_JS):
        text = path.read_text(encoding="utf-8").replace("aria-live", "")
        found = re.findall(r"\b(real-?time|live)\b", text, re.IGNORECASE)
        assert not found, f"{path.name}: {found}"


def test_forecast_snapshot_label_unchanged_and_distinct_from_fetched_time() -> None:
    """DR-17's label is unchanged; the Now mode's 'Fetched Time' is a different
    label in a different place (R-V2-MODE-6(d))."""
    body = _body("showIngestionTime")
    assert '"Last updated (data fetched from CWA): "' in body
    assert "Fetched Time" not in body
    t = _tree()
    assert _inside(t.by_id["ingestion-time"], "forecast-section")
    assert _inside(t.by_id["obs-fetched"], "now-panel")


def test_observation_markers_share_no_colour_with_the_derived_bands() -> None:
    for fn in ("renderStations", "stationIcon", "wireStationMarker", "highlightStations"):
        body = _body(fn)
        assert "BAND_COLOURS" not in body and "colourBand" not in body, fn
    css = _STYLES.read_text(encoding="utf-8")
    bands = {v.lower() for v in re.findall(r"--band-\w+:\s*(#[0-9a-fA-F]{6})", css)}
    obs = {v.lower() for v in re.findall(r"--obs-pill-\w+:\s*(#[0-9a-fA-F]{6})", css)}
    assert len(bands) == 4 and obs, (bands, obs)
    assert not bands & obs, "an observation marker colour equals a derived band colour"
    spill = css[css.index(".spill {"):]
    spill = spill[:spill.index("}")]
    assert "var(--obs-pill-bg)" in spill and "--band-" not in spill


def test_markers_are_the_representative_stations_and_never_nan() -> None:
    body = _body("renderStations")
    assert "representativeIds()" in body
    assert "isFinite(lat)" in body and "isFinite(lng)" in body
    assert body.index("isFinite(lat)") < body.index("L.marker(")
    assert "representativeStationIds" in _body("representativeIds")
    # labelled as a station value, never as the county's temperature
    label = _body("stationLabel")
    assert '" station, "' in label and "station value" in label


def test_observation_times_are_shown_as_published() -> None:
    body = _body("formatObsTime")
    assert "new Date" not in body and "toLocale" not in body, "time converted through the browser clock"


def test_older_observation_never_replaces_newer() -> None:
    body = _body("applyObservation")
    assert "instant(body.observationTime) < instant(obs.observationTime)" in body


def test_refresh_ignored_while_in_progress_and_shows_progress() -> None:
    body = _body("loadObservation")
    assert body.strip().startswith("if (obsInFlight) return;")
    busy = _body("setObsBusy")
    assert "aria-disabled" in busy and '"busy"' in busy


# --- R-V2-MAP-5: the mode-switch path keeps the non-zero-size init guard ------------


def test_mode_switch_goes_through_the_size_guard() -> None:
    assert "bringUpMap()" in _body("setMode")
    assert "ensureMapSized(function" in _body("bringUpMap")
    assert "initMap()" in _body("bringUpMap")


def test_mode_switch_recomputes_size_before_any_view_change() -> None:
    body = _body("syncMap")
    branch = body[body.index("if (appliedMode !== mode)"):]
    inv = branch.find("map.invalidateSize()")
    assert inv != -1, "the mode-switch branch does not call invalidateSize()"
    for later in ("removeLayer(", "showSixRegions()", "restoreNowView()"):
        assert inv < branch.index(later), f"invalidateSize() must precede {later}"
    # the views themselves are restored / fitted only through setView or the single fit
    assert "setView(" in _body("restoreNowView") and "fitToMarkers()" in _body("restoreNowView")
    assert "fitToMarkers(" in _body("showSixRegions")


# --- R-V2-DOC-4 / AC-V2-21(13): CONTEXT.md carries the BRIEF-V2 §9 delta verbatim ----


def test_context_glossary_delta_is_verbatim() -> None:
    brief = _BRIEF_V2.read_text(encoding="utf-8")
    section = brief[brief.index("## 9."):]
    section = section[:section.index("\n## ", 5)]
    rows = re.findall(r"^\| \*\*(.+?)\*\* \| (.+?) \| (.+?) \|$", section, re.M)
    assert len(rows) == 10, rows
    context = _CONTEXT.read_text(encoding="utf-8").replace("\r\n", "\n")
    for term, definition, avoid in rows:
        entry = f"**{term}**:\n{definition}\n_Avoid_: {avoid}\n"
        assert entry in context, f"CONTEXT.md entry for {term!r} is not the BRIEF-V2 §9 text"
    # the old meaning of "Refresh" (re-running ingestion) is gone
    assert "Running Ingestion again" not in context
