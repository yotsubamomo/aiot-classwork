"""Static guards for the Now mode's Refresh semantics and Stale / Unavailable
states (Issue #37).

Fully offline (R-V2-TC-3): these read ``static/index.html``, ``static/app.js`` and
``static/styles.css`` as text, so they run in the pytest suite and CI. The
behaviour itself — the three Refresh results, Stale / Unavailable for each failure
class, the time bound against a stalled upstream, a platform HTML 502 and a held
request, age never triggering Stale, the observation failure leaving the rest of
the page usable, and the H-1 leak sweep — is exercised in a real browser by the
reproducible ``tests/check_refresh_browser.py``. These guards pin the source-level
properties so a regression fails CI:

* R-V2-OBS-13 / DV-7: a client-side bound between the server's upstream bound and
  the 30 s instrument; the request is aborted and settled exactly once.
* R-V2-OBS-7(b)(e): no polling; one Refresh at a time; only the current one applies.
* R-V2-OBS-8 / DV-4 / INV-V2-6: the same Fetched Time and an older Observation Time
  are "not-newer" and never replace what is shown.
* R-V2-OBS-10(d) / INV-V2-6: Stale / Unavailable are set only by a failure and
  cleared only by a success — no clock or age test in the state code.
* R-V2-OBS-11/12 / H-1: the four server reasons map to fixed, distinct page texts;
  nothing from a response body is ever displayed.
* R-V2-OBS-10(e) / H-3: the Stale / Unavailable presentation belongs to the Now
  mode and the stale marker style shares no colour with the derived bands.
"""

from __future__ import annotations

import re

import observation
from tests.test_map_frontend import _function_body, _strip_comments
from tests.test_modes_frontend import _APP_JS, _STYLES, _mode_of, _tree


def _js() -> str:
    return _APP_JS.read_text(encoding="utf-8")


def _code() -> str:
    return _strip_comments(_js())


def _body(name: str) -> str:
    return _strip_comments(_function_body(_js(), name))


# --- R-V2-OBS-13: bounded time -------------------------------------------------------


def test_client_bound_between_server_bound_and_instrument() -> None:
    m = re.search(r"var OBS_TIMEOUT_MS = (\d+);", _js())
    assert m, "no client-side time bound for the Latest Observation request"
    bound = int(m.group(1))
    assert observation.UPSTREAM_DEADLINE_SECONDS * 1000 < bound < 30000, bound


def test_request_is_aborted_and_settled_once_within_the_bound() -> None:
    body = _body("requestObservation")
    assert 'fetch("/api/observations/latest"' in body
    assert "setTimeout(" in body and "OBS_TIMEOUT_MS" in body
    assert "controller.abort()" in body and "signal:" in body
    settle = body[body.index("function settle("):]
    assert settle.index("if (settled) return;") < settle.index("resolve(result)")
    assert "clearTimeout(timer)" in settle
    # every path settles: success/failure answers, network failure / abort, timeout
    assert body.count("settle(") >= 4


def test_non_json_or_unclassified_answers_are_failures() -> None:
    body = _body("classifyObservationResponse")
    assert "JSON.parse(text)" in body and "catch" in body
    assert 'category: "unexpected_response"' in body
    assert "OBS_SERVER_REASONS.indexOf(body.reason)" in body
    usable = _body("usableObservation")
    for part in ("Array.isArray(body.stations)", "isFinite(instant(body.observationTime))",
                 "isFinite(instant(body.fetchedTime))"):
        assert part in usable, part


def test_refresh_always_reaches_a_terminal_state() -> None:
    body = _body("loadObservation")
    assert body.strip().startswith("if (obsInFlight) return;")
    assert "requestObservation()" in body
    # a rendering error still ends in a failure state, then the busy flag clears
    assert body.index("applyObservationFailure(") < body.rindex("obsInFlight = false;")
    assert body.rindex("setObsBusy(false)") > body.rindex("obsInFlight = false;")


# --- R-V2-OBS-7(b)(e): manual only, one at a time, current only ----------------------


def test_no_polling_or_automatic_refresh() -> None:
    code = _code()
    assert "setInterval(" not in code
    calls = re.findall(r"\bloadObservation\(\)", code)
    # the definition, the page load, and the Refresh button's click listener
    assert len(calls) == 3, calls
    assert re.search(r'refreshButton\.addEventListener\("click", function \(\) \{\s*loadObservation\(\);',
                     code)


def test_only_the_current_refresh_applies() -> None:
    body = _body("loadObservation")
    assert "var seq = ++obsSeq;" in body
    assert body.index("if (seq !== obsSeq) return;") < body.index("applyObservation(result.body)")


# --- R-V2-OBS-8 / DV-4 / INV-V2-6: newer vs not-newer ----------------------------------


def test_not_newer_never_replaces_the_shown_data() -> None:
    body = _body("applyObservation")
    same = body.index("body.fetchedTime === obs.fetchedTime")
    older = body.index("instant(body.observationTime) < instant(obs.observationTime)")
    replace = body.index("obs = body;")
    assert same < replace and older < replace, "a not-newer answer is compared after replacing"
    assert body.count('setRefreshResult("not-newer")') == 2
    assert body.count("obs = body;") == 1
    # the not-newer branches tell the user it is already the latest
    head = body[:replace]
    assert head.count("Already the latest") == 2


# --- R-V2-OBS-10: Stale / Unavailable only from failures, never from age ----------------


def test_stale_and_unavailable_are_set_only_by_a_failure() -> None:
    code = _code()
    assignments = re.findall(r'(?<![.\w])obsState = ([^;]+);', code)
    assert sorted(assignments) == sorted(['"loading"', '"success"', 'obs ? "stale" : "unavailable"']), assignments
    assert 'obsState = obs ? "stale" : "unavailable";' in _body("applyObservationFailure")
    assert 'obsState = "success";' in _body("applyObservation")
    assert "obsFailure = null;" in _body("applyObservation")
    # a failure keeps the last successful data (Stale): the shown body is only
    # ever replaced by a newer success, never cleared
    assert len(re.findall(r"(?<![.\w])obs = ", code)) == 2  # "var obs = null;" and "obs = body;"
    assert not re.search(r"(?<![.\w])obs = ", _body("applyObservationFailure"))


def test_no_clock_or_age_in_the_observation_state_code() -> None:
    for fn in ("loadObservation", "applyObservation", "applyObservationFailure",
               "renderObsState", "failureText", "classifyObservationResponse"):
        body = _body(fn)
        for banned in ("Date.now", "new Date", "performance.now", "setTimeout", "setInterval"):
            assert banned not in body, f"{fn} uses {banned}"


# --- R-V2-OBS-11/12, H-1: failure categories -------------------------------------------


def test_the_four_server_reasons_have_fixed_distinct_texts() -> None:
    js = _js()
    table = js[js.index("var OBS_FAILURE_TEXT = {"):]
    table = table[:table.index("};")]
    texts = dict(re.findall(r'(\w+): "([^"]+)"', table))
    assert set(texts) == set(observation.FAILURE_REASONS) | {"no_response", "unexpected_response"}
    assert len(set(texts.values())) == len(texts), "two failure categories share a text"
    server = re.search(r"var OBS_SERVER_REASONS = \[([^\]]+)\];", js).group(1)
    assert re.findall(r'"(\w+)"', server) == list(observation.FAILURE_REASONS)


def test_no_response_text_is_ever_displayed() -> None:
    for fn in ("applyObservationFailure", "failureText", "renderObsState", "classifyObservationResponse"):
        body = _body(fn)
        assert ".error" not in body, f"{fn} reads a server error text"
        assert "textContent = text" not in body and "innerHTML" not in body, fn
    classify = _body("classifyObservationResponse")
    # only the reason code and a numeric status leave the parsed body
    copied = re.findall(r"body\.(\w+)", classify)
    assert set(copied) <= {"reason", "upstreamStatus"}, copied
    assert "isHttpStatus(body.upstreamStatus)" in classify


# --- R-V2-OBS-10(e), H-3: presentation ---------------------------------------------------


def test_state_presentation_belongs_to_the_now_mode() -> None:
    t = _tree()
    for el in ("obs-state", "obs-state-chip", "obs-map-state", "obs-status"):
        assert _mode_of(t.by_id[el]) == "now", el
    for el in ("obs-state", "obs-state-chip", "obs-map-state"):
        assert "hidden" in t.by_id[el]["attrs"], f"#{el} must start hidden"
    assert t.by_id["now-panel"]["attrs"].get("data-obs-state") == "loading"
    # the on-map notice never takes the pointer
    css = _STYLES.read_text(encoding="utf-8")
    wrap = css[css.index(".obs-map-state-wrap {"):]
    assert "pointer-events: none" in wrap[:wrap.index("}")]


def test_state_labels_and_wording() -> None:
    body = _body("renderObsState")
    for text in ('"STALE"', '"UNAVAILABLE"', '"Stale"', '"Latest Observation unavailable"'):
        assert text in body, text
    for path_text in (_js(),):
        assert not re.findall(r"\b(real-?time|live)\b", path_text.replace("aria-live", ""), re.IGNORECASE)


def test_stale_markers_share_no_colour_with_the_derived_bands() -> None:
    css = _STYLES.read_text(encoding="utf-8")
    bands = {v.lower() for v in re.findall(r"--band-\w+:\s*(#[0-9a-fA-F]{6})", css)}
    stale = {v.lower() for v in re.findall(r"--obs-stale-[\w-]+:\s*(#[0-9a-fA-F]{6})", css)}
    assert len(bands) == 4 and len(stale) == 2
    assert not bands & stale
    rule = css[css.index(".map--obs-stale .spill {"):]
    rule = rule[:rule.index("}")]
    assert "var(--obs-stale-bg)" in rule and "--band-" not in rule
