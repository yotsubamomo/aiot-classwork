"""Reproducible browser check for Issue #37 (Refresh results, Stale / Unavailable).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the convention of ``check_modes_browser.py``, whose
DevTools driver it reuses). It runs the *unmodified* ``server.create_app``
in-process on loopback (threaded, so a hanging request does not block the page's
other requests), with Flask ``DEBUG`` on and the root logger at ``DEBUG``, and a
**sentinel** ``CWA_API_KEY`` that must never reach the browser or the log (H-1).

The Latest Observation service is the real ``observation.LatestObservationService``
with a controllable clock (its reuse window is 600 s; the check moves the clock
past it whenever a fresh upstream fetch is wanted) and a simulated upstream derived
from the committed sanitised sample (no key, no network, R-V2-TC-3):

* ``ok`` — the sample with every ``ObsTime`` of the capture hour moved to a chosen
  hour (one hour earlier, the capture hour, one / two / three hours later) and the
  臺北 station's air temperature changed per variant;
* the four server failure classes: ``key_not_configured`` (key removed from the
  environment), ``upstream_unreachable`` (a connection error whose message carries
  the upstream host and the key), ``upstream_error`` (HTTP 429 / 500 whose body
  carries a marker and the key), ``invalid_response`` (a 2xx non-JSON body with a
  marker);
* ``stall`` — the upstream never answers within the server's 8 s bound;

and a platform layer in front of the app that can answer the observation path with
an HTML ``502`` page, or hold the request longer than the page's own time bound
before passing it on (the late answer must never be applied).

Checks (AC-V2-06 browser (a)–(f), AC-V2-08, AC-V2-04 stale / unavailable,
AC-V2-09(b), INV-V2-6, INV-V2-7, H-1, H-3) read the ``/api/`` bodies the page
actually received through the DevTools protocol; nothing is typed in as an oracle.
Every browser request is recorded; any request off the loopback origin fails.

Usage (from the unit directory, venv active, ``data.db`` present)::

    python tests/check_refresh_browser.py                 # writes evidence
    python tests/check_refresh_browser.py --out <dir>
    CHROME="/path/to/chrome" python tests/check_refresh_browser.py

Exit code 0 means every check passed. Evidence in ``--out`` (default
``doc/acceptance/screenshots/v2/issue-37/``): PNG screenshots,
``browser-check-results.json`` and ``network-log.json``.
"""

from __future__ import annotations

import argparse
import base64
import copy
import io
import json
import logging
import re
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, make_server

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

import requests  # noqa: E402

import observation as obs  # noqa: E402
from server import create_app  # noqa: E402
from tests.check_modes_browser import (  # noqa: E402
    JS_HELPERS, Browser, Checks, _QuietHandler, find_chrome, fmt_temp, fmt_time,
)

SAMPLE = _UNIT_DIR / "tests" / "fixtures" / "O-A0001-001_sample.json"
DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "v2" / "issue-37"
OBS_PATH = "/api/observations/latest"
CAPTURE_HOUR = "2026-09-25T23:00:00+08:00"
TAIPEI_ID = "466920"
TAIPEI_TZ = timezone(timedelta(hours=8))

SENTINEL_KEY = "SENTINEL-KEY-issue37-must-never-leak"
UPSTREAM_MARKER = "UPSTREAM-BODY-MARKER-issue37"
PLATFORM_MARKER = "PLATFORM-PAGE-MARKER-issue37"
UPSTREAM_HOST = "opendata.cwa.gov.tw"
# Strings that must never reach the page, the console or the server log (H-1).
LEAKS = (SENTINEL_KEY, UPSTREAM_MARKER, UPSTREAM_HOST, "Authorization")

CLIENT_BOUND_S = 20.0      # app.js OBS_TIMEOUT_MS
INSTRUMENT_S = 30.0        # SPEC-V2 §5.3 bounded-time instrument
STALL_S = 40.0             # simulated upstream stall (> the server's 8 s bound)
HANG_S = 25.0              # platform hold (> the page's 20 s bound)
FORBIDDEN_WORDS = re.compile(r"\b(real-?time|live)\b", re.IGNORECASE)
BAND_COLOURS = {"rgb(43, 108, 176)", "rgb(47, 133, 90)", "rgb(214, 158, 46)", "rgb(197, 48, 48)"}

REASON_TEXT = {  # app.js OBS_FAILURE_TEXT (the category text the page must show)
    "key_not_configured": "the server has no CWA API key configured",
    "upstream_unreachable": "the CWA service could not be reached in time",
    "upstream_error": "the CWA service answered with an error status",
    "invalid_response": "the CWA response was not usable",
    "no_response": "this site's server did not answer in time or could not be reached",
    "unexpected_response": "this site's server gave an unexpected answer",
}


def hour(offset: int) -> str:
    base = datetime.fromisoformat(CAPTURE_HOUR)
    return (base + timedelta(hours=offset)).isoformat()


# --- simulated upstream, clock and platform -------------------------------------------


class Upstream:
    """A ``requests.get`` stand-in: sample-derived payloads and the failure classes."""

    VARIANTS = {"hm1": (-1, "30.0"), "h0": (0, None), "h1": (1, "26.4"),
                "h1b": (1, "25.9"), "h2": (2, "24.8"), "h3": (3, "24.1"), "h4": (4, "23.7")}

    def __init__(self) -> None:
        raw = json.loads(SAMPLE.read_text(encoding="utf-8"))
        self.payloads: dict[str, bytes] = {}
        for name, (offset, taipei_temp) in self.VARIANTS.items():
            data = copy.deepcopy(raw)
            for record in data["records"]["Station"]:
                if record["ObsTime"]["DateTime"] == CAPTURE_HOUR:
                    record["ObsTime"]["DateTime"] = hour(offset)
                if record["StationId"] == TAIPEI_ID and taipei_temp:
                    record["WeatherElement"]["AirTemperature"] = taipei_temp
            self.payloads[name] = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.mode = "ok"
        self.variant = "h0"
        self.status = 200
        self.delay = 0.0
        self.calls = 0

    def __call__(self, url, headers=None, params=None, timeout=None):
        self.calls += 1
        key = (headers or {}).get("Authorization", "")
        if self.delay:
            time.sleep(self.delay)
        if self.mode == "stall":
            time.sleep(STALL_S)
        if self.mode == "unreachable":
            raise requests.ConnectionError(
                f"HTTPSConnectionPool(host='{UPSTREAM_HOST}', port=443): Max retries exceeded "
                f"with url: /api/v1/rest/datastore/O-A0001-001?Authorization={key} ({UPSTREAM_MARKER})")
        if self.mode == "http":
            return _Response(self.status, json.dumps(
                {"message": f"{UPSTREAM_MARKER} rejected Authorization {key}"}).encode())
        if self.mode == "nonjson":
            return _Response(200, f"<html>{UPSTREAM_MARKER} {key}</html>".encode())
        return _Response(200, self.payloads[self.variant])


class _Response:
    def __init__(self, status: int, content: bytes) -> None:
        self.status_code = status
        self.content = content

    def close(self) -> None:
        pass


class Clock:
    """The service clock: Fetched Time and the reuse window follow it."""

    def __init__(self) -> None:
        self.now = datetime(2026, 9, 26, 0, 4, 56, tzinfo=TAIPEI_TZ)

    def __call__(self) -> datetime:
        return self.now

    def past_reuse_window(self) -> None:
        self.now += timedelta(seconds=601)


class Platform:
    """WSGI layer in front of the app for the observation path only: ``html502``
    answers a platform HTML error page; ``hang`` holds the request HANG_S seconds
    and then passes it to the app (whose late answer must not be applied)."""

    def __init__(self, app) -> None:
        self.app = app
        self.mode = None

    def __call__(self, environ, start_response):
        if environ.get("PATH_INFO") == OBS_PATH and self.mode:
            if self.mode == "html502":
                start_response("502 Bad Gateway", [("Content-Type", "text/html; charset=utf-8")])
                return [f"<html><body><h1>502 Bad Gateway</h1><p>{PLATFORM_MARKER}</p></body></html>".encode()]
            if self.mode == "hang":
                time.sleep(HANG_S)
        return self.app(environ, start_response)


class _ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True


class Rig:
    def __init__(self) -> None:
        self.upstream = Upstream()
        self.clock = Clock()
        self.env = {"CWA_API_KEY": SENTINEL_KEY}
        service = obs.LatestObservationService(
            env=self.env, http_get=self.upstream, clock=self.clock, reuse_window_seconds=600)
        app = create_app(db_path=None, observation_service=service)
        app.debug = True  # DEBUG on: failure answers must still carry no secret
        self.platform = Platform(app)
        self.server = make_server("127.0.0.1", 0, self.platform,
                                  server_class=_ThreadingWSGIServer, handler_class=_QuietHandler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def set(self, mode="ok", variant=None, status=200, delay=0.0, key=True, platform=None,
            fresh=True) -> None:
        """Configure the next observation request; ``fresh`` moves the clock past the
        reuse window so the server fetches again instead of reusing a success."""
        if fresh:
            self.clock.past_reuse_window()
        self.upstream.mode, self.upstream.status, self.upstream.delay = mode, status, delay
        if variant:
            self.upstream.variant = variant
        if key:
            self.env["CWA_API_KEY"] = SENTINEL_KEY
        else:
            self.env.pop("CWA_API_KEY", None)
        self.platform.mode = platform

    def close(self) -> None:
        self.server.shutdown()


# --- page-side helpers --------------------------------------------------------------

# Installed before any page script: records every value of the dataset Observation
# Time and of the Now mode state over the page's lifetime (INV-V2-6 evidence).
HISTORY_HOOK = r"""
window.__hist = {times: [], states: []};
document.addEventListener('DOMContentLoaded', function () {
  var t = document.getElementById('obs-time'), p = document.getElementById('now-panel');
  function rec() { var h = window.__hist.times, v = t.textContent; if (!h.length || h[h.length - 1] !== v) h.push(v); }
  function recS() { var h = window.__hist.states, v = p.getAttribute('data-obs-state'); if (!h.length || h[h.length - 1] !== v) h.push(v); }
  rec(); recS();
  new MutationObserver(rec).observe(t, {childList: true, characterData: true, subtree: true});
  new MutationObserver(recS).observe(p, {attributes: true, attributeFilter: ['data-obs-state']});
});
"""

NOW_STATE_JS = r"""(function () {
  var p = document.getElementById('now-panel');
  var chip = document.getElementById('obs-state-chip');
  var banner = document.getElementById('obs-state');
  var badge = document.getElementById('obs-map-state');
  var sel = document.getElementById('obs-selected');
  return {
    state: p.getAttribute('data-obs-state'),
    result: p.getAttribute('data-refresh-result'),
    busy: document.getElementById('refresh-button').getAttribute('aria-disabled'),
    panelBusy: p.getAttribute('aria-busy'),
    time: document.getElementById('obs-time').textContent,
    fetched: document.getElementById('obs-fetched').textContent,
    count: document.getElementById('obs-count').textContent,
    status: document.getElementById('obs-status').textContent,
    statusClass: document.getElementById('obs-status').className,
    spinner: !!document.querySelector('#obs-status .spinner'),
    chip: __chk.visible(chip) ? chip.textContent : null,
    banner: __chk.visible(banner) ? {title: document.getElementById('obs-state-title').textContent,
      body: document.getElementById('obs-state-body').textContent,
      reason: document.getElementById('obs-state-reason').textContent, cls: banner.className} : null,
    badge: __chk.visible(badge) ? badge.textContent : null,
    mapStale: document.getElementById('map').classList.contains('map--obs-stale'),
    markers: Array.from(document.querySelectorAll('.station-icon .spill')).map(function (s) { return s.textContent; }),
    markerFill: Array.from(new Set(Array.from(document.querySelectorAll('.station-icon .spill')).map(function (s) { return getComputedStyle(s).backgroundColor; }))),
    markerBorder: Array.from(new Set(Array.from(document.querySelectorAll('.station-icon .spill')).map(function (s) { return getComputedStyle(s).borderStyle; }))),
    selected: sel.hidden ? null : {name: document.getElementById('obs-sel-name').textContent,
      temp: document.getElementById('obs-sel-temp').textContent},
    nowPressed: document.getElementById('mode-now').getAttribute('aria-pressed'),
    refreshVisible: __chk.visible(document.getElementById('refresh-button')),
    toggleVisible: __chk.visible(document.querySelector('.mode-toggle')),
    scrollWidth: document.documentElement.scrollWidth, innerWidth: innerWidth,
  };
})()"""


def parse_shown(text: str) -> datetime | None:
    """A displayed Observation Time ("2026-09-25 23:00 +08:00") as an instant."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2})(?::\d{2})? ([+-]\d{2}:\d{2})$", text)
    return datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}{m.group(3)}") if m else None


class Session:
    """One browser page against the rig, with the evidence the checks need."""

    def __init__(self, chrome: str, rig: Rig, out: Path, checks: Checks, label: str,
                 width: int, height: int, mobile: bool) -> None:
        self.b = Browser(chrome)
        self.rig, self.out, self.checks, self.label = rig, out, checks, label
        self.mobile = mobile
        self.b.viewport(width, height, mobile)
        self.b.send("Page.addScriptToEvaluateOnNewDocument", {"source": HISTORY_HOOK})
        self.dom_snapshots: list[str] = []
        self._bodies: dict[str, dict] = {}  # requestId -> {status, text}, read while available

    def open(self, wait: bool = True) -> dict:
        self.b.navigate(self.rig.base + "/")
        self.b.js(JS_HELPERS)
        return self.wait_terminal(INSTRUMENT_S + 5) if wait else {}

    def state(self) -> dict:
        return self.b.js(NOW_STATE_JS)

    def wait_terminal(self, timeout: float) -> dict:
        self.b.wait_for("document.getElementById('now-panel').getAttribute('data-obs-state') !== 'loading'"
                        " && document.getElementById('refresh-button').getAttribute('aria-disabled') === 'false'",
                        timeout)
        self.b.pump(0.2)
        st = self.state()
        self.dom_snapshots.append(self.b.js("document.documentElement.outerHTML"))
        self.obs_bodies()  # read the answers now: a later navigation may evict them
        return st

    def refresh(self, timeout: float = INSTRUMENT_S + 5) -> tuple[dict, float]:
        """Click Refresh and wait for the terminal state; returns (state, seconds)."""
        t0 = time.time()
        self.b.js("document.getElementById('refresh-button').click(); true")
        st = self.wait_terminal(timeout)
        return st, time.time() - t0

    def obs_bodies(self) -> list[dict]:
        """Every finished /api/observations/latest answer: status and raw text."""
        finished = {e["params"]["requestId"] for e in self.b.events
                    if e["method"] == "Network.loadingFinished"}
        out = []
        for e in self.b.events:
            if e["method"] == "Network.responseReceived" and OBS_PATH in e["params"]["response"]["url"]:
                rid = e["params"]["requestId"]
                if rid not in self._bodies and rid in finished:
                    try:
                        body = self.b.send("Network.getResponseBody", {"requestId": rid})
                    except RuntimeError:
                        continue
                    text = body["body"] if not body.get("base64Encoded") else base64.b64decode(body["body"]).decode()
                    self._bodies[rid] = {"status": e["params"]["response"]["status"], "text": text}
                if rid in self._bodies:
                    out.append(self._bodies[rid])
        return out

    def last_json(self) -> dict:
        bodies = self.obs_bodies()
        return json.loads(bodies[-1]["text"]) if bodies else {}

    def obs_requests(self) -> int:
        return len([u for u in self.b.request_urls() if OBS_PATH in u])

    def shot(self, name: str) -> None:
        self.b.screenshot(self.out / f"{self.label}-{name}.png", full_page=self.mobile)

    def add(self, check_id: str, ok: bool, detail) -> None:
        self.checks.add(f"{self.label} {check_id}", ok, detail)

    def close(self) -> None:
        self.b.close()


def expect_stale(s: Session, st: dict, before: dict, category: str) -> bool:
    """Stale: last successful data and both times kept; Stale label + category."""
    return (st["state"] == "stale" and st["result"] == "failure" and st["busy"] == "false"
            and st["time"] == before["time"] and st["fetched"] == before["fetched"]
            and st["count"] == before["count"] and st["markers"] == before["markers"]
            and st["selected"] == before["selected"] and st["chip"] == "STALE"
            and st["banner"] is not None and st["banner"]["title"] == "Stale"
            and REASON_TEXT[category] in st["banner"]["reason"]
            and (category not in obs.FAILURE_REASONS or category in st["banner"]["reason"])
            and st["badge"] is not None and st["badge"].startswith("Stale") and st["mapStale"]
            and st["refreshVisible"] and st["nowPressed"] == "true")


def expect_unavailable(st: dict, category: str) -> bool:
    return (st["state"] == "unavailable" and st["result"] == "failure" and st["busy"] == "false"
            and st["time"] == "—" and st["fetched"] == "—" and st["count"] == "—"
            and st["markers"] == [] and st["chip"] == "UNAVAILABLE"
            and st["banner"] is not None and st["banner"]["title"] == "Latest Observation unavailable"
            and REASON_TEXT[category] in st["banner"]["reason"]
            and (category not in obs.FAILURE_REASONS or category in st["banner"]["reason"])
            and st["badge"] == "Latest Observation unavailable" and not st["mapStale"]
            and st["refreshVisible"] and st["nowPressed"] == "true" and st["toggleVisible"])


def expect_success(st: dict) -> bool:
    return (st["state"] == "success" and st["chip"] is None and st["banner"] is None
            and st["badge"] is None and not st["mapStale"] and st["busy"] == "false")


def reason_line(st: dict) -> str:
    return (st.get("banner") or {}).get("reason", "")


# --- scenario R: the three Refresh results and Stale (success first) -------------------------


def scenario_refresh(chrome: str, rig: Rig, out: Path, checks: Checks, network: dict,
                     label: str, size: tuple[int, int, bool], full: bool) -> Session:
    s = Session(chrome, rig, out, checks, label, *size)
    reasons_seen: dict[str, str] = {}

    # first load, slowed so the loading state can be seen
    rig.set("ok", "h0", delay=2.0)
    s.open(wait=False)
    loading = s.state()
    s.add("R-V2-OBS-7(c)/RSP-8 first load shows the loading state with an in-progress indicator",
          loading["state"] == "loading" and loading["busy"] == "true" and loading["spinner"]
          and "Loading the Latest Observation" in loading["status"] and loading["time"] == "—", loading)
    s.shot("now-loading")
    first = s.wait_terminal(INSTRUMENT_S)
    body0 = s.last_json()
    by_id = {x["stationId"]: x for x in body0.get("stations", [])}
    s.add("first load success: data and both times = /api/, no state label, no notice",
          expect_success(first) and first["result"] == "newer" and first["status"] == ""
          and first["time"] == fmt_time(body0["observationTime"], False)
          and first["fetched"] == fmt_time(body0["fetchedTime"], True)
          and first["count"] == str(body0["validStationCount"]) and len(first["markers"]) == 22,
          {"page": {k: first[k] for k in ("state", "time", "fetched", "count", "status")},
           "api": {k: body0.get(k) for k in ("observationTime", "fetchedTime", "validStationCount")}})
    reps = body0["representativeStationIds"]
    taipei = reps.index(TAIPEI_ID)
    s.b.js(f"document.querySelectorAll('.station-icon .spill')[{taipei}].click(); true")
    s.b.pump(0.3)
    base = s.state()
    s.add("selecting 臺北 shows its /api/ values", base["selected"] is not None
          and base["selected"]["temp"] == fmt_temp(by_id[TAIPEI_ID]["airTemperature"]) + " °C", base["selected"])
    if full:
        s.shot("now-success")

    # (c) same Fetched Time (the server's reuse window) -> not-newer
    rig.set("ok", "h0", fresh=False)
    st, _ = s.refresh()
    reuse = s.last_json()
    s.add("AC-V2-06(c) same Fetched Time (reuse window) -> not-newer: display unchanged, 'already the latest', not Stale",
          reuse.get("fetchedTime") == body0["fetchedTime"] and expect_success(st) and st["result"] == "not-newer"
          and st["time"] == base["time"] and st["fetched"] == base["fetched"] and st["markers"] == base["markers"]
          and st["selected"] == base["selected"] and st["status"].startswith("Already the latest")
          and "obs-status--done" in st["statusClass"],
          {"status": st["status"], "result": st["result"], "state": st["state"]})
    s.shot("not-newer-same-fetched-time")

    # (b) an OLDER dataset Observation Time -> not-newer (never replaces newer)
    rig.set("ok", "hm1")
    st, _ = s.refresh()
    older = s.last_json()
    s.add("AC-V2-06(b) older Observation Time -> not-newer: data and both times unchanged, 'already the latest', not Stale",
          older.get("observationTime") == hour(-1) and older.get("fetchedTime") != body0["fetchedTime"]
          and expect_success(st) and st["result"] == "not-newer" and st["time"] == base["time"]
          and st["fetched"] == base["fetched"] and st["markers"] == base["markers"]
          and st["selected"] == base["selected"] and st["status"].startswith("Already the latest"),
          {"api": {k: older.get(k) for k in ("observationTime", "fetchedTime")},
           "page": {k: st[k] for k in ("time", "fetched", "status", "result")}})
    if full:
        s.shot("not-newer-older-observation-time")

    # (a) a newer Observation Time -> newer: data + both times update
    rig.set("ok", "h1")
    st, _ = s.refresh()
    newer = s.last_json()
    new_taipei = {x["stationId"]: x for x in newer["stations"]}[TAIPEI_ID]
    s.add("AC-V2-06(a) newer Observation Time -> newer: data, Observation Time and Fetched Time all update",
          newer.get("observationTime") == hour(1) and expect_success(st) and st["result"] == "newer"
          and st["time"] == fmt_time(newer["observationTime"], False)
          and st["fetched"] == fmt_time(newer["fetchedTime"], True)
          and st["selected"]["temp"] == fmt_temp(new_taipei["airTemperature"]) + " °C"
          and st["markers"] != base["markers"] and st["status"] == "Updated to a newer Latest Observation.",
          {"page": {k: st[k] for k in ("time", "fetched", "status", "selected")},
           "api": {k: newer.get(k) for k in ("observationTime", "fetchedTime")}})
    s.shot("newer")

    # equal Observation Time fetched again -> applied (>= applies, DV-4)
    rig.set("ok", "h1b")
    st, _ = s.refresh()
    equal = s.last_json()
    eq_taipei = {x["stationId"]: x for x in equal["stations"]}[TAIPEI_ID]
    s.add("DV-4 equal Observation Time with a new Fetched Time is applied (Fetched Time and data update)",
          equal.get("observationTime") == hour(1) and expect_success(st) and st["result"] == "newer"
          and st["fetched"] == fmt_time(equal["fetchedTime"], True)
          and st["time"] == fmt_time(equal["observationTime"], False)
          and st["selected"]["temp"] == fmt_temp(eq_taipei["airTemperature"]) + " °C"
          and st["status"].startswith("Updated: fetched again"),
          {"page": {k: st[k] for k in ("time", "fetched", "status")}, "api": equal.get("fetchedTime")})

    # (d) rapid repeated clicks while in progress -> one request, one result applied
    rig.set("ok", "h2", delay=1.5)
    before_n = s.obs_requests()
    s.b.js("for (var i = 0; i < 5; i++) document.getElementById('refresh-button').click(); true")
    s.b.pump(0.3)
    mid = s.state()
    st = s.wait_terminal(INSTRUMENT_S)
    rapid = s.last_json()
    s.add("AC-V2-06(d) rapid repeated Refresh while in progress -> one request, one result applied in order",
          mid["busy"] == "true" and s.obs_requests() - before_n == 1 and expect_success(st)
          and st["result"] == "newer" and st["time"] == fmt_time(rapid["observationTime"], False)
          and rapid["observationTime"] == hour(2),
          {"requests": s.obs_requests() - before_n, "mid_busy": mid["busy"], "time": st["time"]})
    good = s.state()

    # Stale: each of the four server failure classes after a success
    cases = [("upstream_error", dict(mode="http", status=429), 502),
             ("upstream_unreachable", dict(mode="unreachable"), 504),
             ("invalid_response", dict(mode="nonjson"), 502),
             ("key_not_configured", dict(key=False), 503)]
    for reason, setup, http in cases:
        rig.set(**setup)
        st, secs = s.refresh()
        answer = s.obs_bodies()[-1]
        body = json.loads(answer["text"])
        s.add(f"AC-V2-08(b) {reason} after success -> Stale: data and both times kept, Stale label and category, Refresh usable",
              answer["status"] == http and body.get("reason") == reason and expect_stale(s, st, good, reason)
              and secs < INSTRUMENT_S,
              {"api": [answer["status"], body.get("reason"), body.get("upstreamStatus")],
               "page": {k: st[k] for k in ("state", "chip", "badge", "time", "fetched", "status")},
               "reason": reason_line(st), "seconds": round(secs, 2)})
        reasons_seen[reason] = reason_line(st)
        if full or reason == "upstream_error":
            s.shot(f"stale-{reason}")
    s.add("R-V2-OBS-12 the four failure classes are distinguishable in the page (upstream_error with its HTTP status)",
          len(set(reasons_seen.values())) == 4 and all(r in reasons_seen[r] for r in reasons_seen)
          and "(HTTP 429)" in reasons_seen.get("upstream_error", ""), reasons_seen)

    # a later newer success clears Stale
    rig.set("ok", "h3")
    st, _ = s.refresh()
    recovered = s.last_json()
    s.add("AC-V2-08(c) a later newer success clears Stale and applies the data",
          expect_success(st) and st["result"] == "newer" and st["time"] == fmt_time(recovered["observationTime"], False)
          and st["fetched"] == fmt_time(recovered["fetchedTime"], True), {k: st[k] for k in ("state", "time", "status")})
    good = s.state()

    # a later NOT-newer success also clears Stale (R-V2-OBS-10(c)), data unchanged
    rig.set("http", status=500)
    st, _ = s.refresh()
    stale_again = st["state"] == "stale"
    rig.set("ok", "hm1")
    st, _ = s.refresh()
    s.add("AC-V2-08(c) a later not-newer success also clears Stale, display unchanged",
          stale_again and expect_success(st) and st["result"] == "not-newer" and st["time"] == good["time"]
          and st["fetched"] == good["fetched"] and st["status"].startswith("Already the latest"),
          {k: st[k] for k in ("state", "result", "time", "status")})

    # (e) upstream stall -> classified upstream_unreachable JSON, Stale within 30 s
    rig.set("stall")
    st, secs = s.refresh()
    answer = s.obs_bodies()[-1]
    s.add("AC-V2-06(e) upstream stall -> upstream_unreachable JSON (not a gateway page) and Stale within 30 s",
          answer["status"] == 504 and json.loads(answer["text"]).get("reason") == "upstream_unreachable"
          and expect_stale(s, st, good, "upstream_unreachable") and secs < INSTRUMENT_S,
          {"status": answer["status"], "seconds": round(secs, 2), "state": st["state"]})
    if full:
        s.shot("stale-upstream-stall")

    # stall with other clients' requests already queued on the server (the #35
    # service serialises upstream fetches, audit #35 F-2): this page's Refresh
    # still ends within the bound — here by the page's own 20 s limit
    rig.set("stall")
    s.b.js(f"fetch('{OBS_PATH}'); fetch('{OBS_PATH}'); true")  # two other waiting requests
    s.b.pump(0.3)
    st, secs = s.refresh()
    s.add("R-V2-OBS-13 stalled upstream with two requests queued ahead -> this Refresh still reaches Stale within 30 s",
          (expect_stale(s, st, good, "no_response") or expect_stale(s, st, good, "upstream_unreachable"))
          and secs < INSTRUMENT_S, {"seconds": round(secs, 2), "reason": reason_line(st)})
    s.b.pump(max(0.0, 3 * 8.5 - secs + 1))  # let the queued server work drain

    # (f) platform-layer non-JSON 5xx -> failure (Stale), never stuck
    rig.set("ok", "h3", platform="html502")
    st, secs = s.refresh()
    answer = s.obs_bodies()[-1]
    s.add("AC-V2-06(f) platform HTML 502 -> Stale with the 'unexpected answer' category, within 30 s",
          answer["status"] == 502 and PLATFORM_MARKER in answer["text"]
          and expect_stale(s, st, good, "unexpected_response") and "(HTTP 502)" in reason_line(st)
          and secs < INSTRUMENT_S, {"seconds": round(secs, 2), "reason": reason_line(st)})
    s.add("H-1 the platform page body never reaches the page",
          PLATFORM_MARKER not in s.b.js("document.documentElement.outerHTML"), "")
    if full:
        s.shot("stale-platform-502")

    # platform hold beyond the page's own bound -> the page gives up (Stale) in
    # bounded time and the late (newer!) answer is never applied
    rig.set("ok", "h4", platform="hang")  # the held answer would be NEWER
    st, secs = s.refresh(timeout=INSTRUMENT_S + 5)
    s.add("R-V2-OBS-13 no answer within the page's bound -> Stale ('did not answer in time') within 30 s",
          expect_stale(s, st, good, "no_response") and CLIENT_BOUND_S - 1 <= secs < INSTRUMENT_S,
          {"seconds": round(secs, 2), "reason": reason_line(st)})
    s.b.pump(HANG_S - secs + 3)  # let the held request finish on the server
    late = s.state()
    s.add("AC-V2-06(d)/OBS-7(e) a late answer after the bound is never applied",
          late["state"] == "stale" and late["time"] == good["time"] and late["fetched"] == good["fetched"],
          {k: late[k] for k in ("state", "time", "fetched")})
    rig.platform.mode = None

    # observation failure only affects the Now observation layer (AC-V2-09(b), stale side)
    isolation(s, "stale")

    # freshness monotonic over the whole page lifetime (INV-V2-6)
    hist = s.b.js("window.__hist")
    shown = [parse_shown(t) for t in hist["times"] if t != "—"]
    s.add("INV-V2-6 the displayed dataset Observation Time never decreased during the page's lifetime",
          all(x is not None for x in shown) and all(a <= b for a, b in zip(shown, shown[1:])) and len(shown) >= 3,
          hist)
    network[label + "-refresh"] = s.b.request_urls()
    return s


# --- scenario U: first-load failures (Unavailable) ------------------------------------------


def scenario_unavailable(chrome: str, rig: Rig, out: Path, checks: Checks, network: dict,
                         label: str, size: tuple[int, int, bool], full: bool) -> Session:
    s = Session(chrome, rig, out, checks, label, *size)
    cases = [("key_not_configured", dict(key=False), 503),
             ("upstream_unreachable", dict(mode="unreachable"), 504),
             ("upstream_error", dict(mode="http", status=403), 502),
             ("invalid_response", dict(mode="nonjson"), 502)]
    if full:
        cases += [("upstream_unreachable", dict(mode="stall"), 504),
                  ("unexpected_response", dict(platform="html502"), 502)]
    else:
        cases = cases[:2]
    texts = {}
    for i, (category, setup, http) in enumerate(cases):
        rig.set(**setup)
        t0 = time.time()
        st = s.open()
        secs = time.time() - t0
        s.b.pump(1.5)  # no automatic mode switch afterwards
        st2 = s.state()
        answer = s.obs_bodies()[-1]
        tag = "stall" if setup.get("mode") == "stall" else category
        s.add(f"AC-V2-08(a) first-load {tag} -> Unavailable: stays in Now mode, '—' times, category reason, Refresh usable",
              answer["status"] == http and expect_unavailable(st, category) and expect_unavailable(st2, category)
              and secs < INSTRUMENT_S + 3,
              {"api_status": answer["status"], "reason": reason_line(st), "seconds": round(secs, 2),
               "page": {k: st[k] for k in ("state", "time", "fetched", "count", "chip", "badge", "nowPressed")}})
        texts[tag] = reason_line(st)
        map_ok = s.b.js("""({frame: __chk.visible(document.getElementById('map-frame')),
            map: __chk.visible(document.getElementById('map')),
            paths: document.querySelectorAll('#map .leaflet-overlay-pane path').length,
            text: document.querySelector('#now-panel').innerText,
            pills: document.querySelectorAll('.pill-icon').length,
            forecastStatus: __chk.visible(document.getElementById('map-status'))})""")
        s.add(f"AC-V2-08(a)/H-3 {tag}: map and county boundaries visible; no forecast value shown as observation",
              map_ok["frame"] and map_ok["map"] and map_ok["paths"] >= 22 and map_ok["pills"] == 0
              and not map_ok["forecastStatus"] and not re.search(r"\d\s*°", map_ok["text"])
              and "DERIVED" not in map_ok["text"]
              and "Select Date" not in map_ok["text"] and not FORBIDDEN_WORDS.search(map_ok["text"]),
              {k: map_ok[k] for k in ("frame", "map", "paths", "pills", "forecastStatus")})
        if full or i == 0:
            s.shot(f"unavailable-{tag}")
        if i == 0:
            isolation(s, "unavailable")
    if full:
        s.add("R-V2-OBS-12 the four server failure classes are distinguishable on first load",
              len({texts[k] for k in obs.FAILURE_REASONS}) == 4, texts)
    # recovery from Unavailable by Refresh
    rig.set("ok", "h0")
    st, _ = s.refresh()
    body = s.last_json()
    s.add("AC-V2-08 Refresh after Unavailable succeeds and clears Unavailable",
          expect_success(st) and st["result"] == "newer" and st["time"] == fmt_time(body["observationTime"], False)
          and st["status"] == "Loaded the Latest Observation." and len(st["markers"]) == 22,
          {k: st[k] for k in ("state", "time", "status")})
    network[label + "-unavailable"] = s.b.request_urls()
    return s


def isolation(s: Session, state: str) -> None:
    """AC-V2-09(b) / R-V2-DEG-2 / INV-V2-7: with the observation failing, the map
    still pans and zooms, the mode switch and Forecast mode work, and the lower
    dashboard works; coming back, the Now mode still shows its state."""
    b = s.b
    pane = "document.querySelector('#map .leaflet-map-pane').style.transform"
    # zoom in first, then pan (WI-UI-POLISH-1): at the opening zoom the whole range
    # E fits inside the wider desktop map, so the fence keeps E centred and a pan
    # has nowhere to go (R-V2-MAP-1 (ii)); one level in, the view is smaller than E
    d_before = b.js("(document.querySelector('#map .leaflet-overlay-pane path')||{}).getAttribute('d')")
    b.js("document.querySelector('.leaflet-control-zoom-in').click(); true")
    b.pump(0.8)
    zoomed = b.js("(document.querySelector('#map .leaflet-overlay-pane path')||{}).getAttribute('d')") != d_before
    b.js("document.getElementById('map').focus(); true")
    t_before = b.js(pane)
    b.key("ArrowRight")
    b.pump(0.6)
    panned = b.js(pane) != t_before
    b.js("document.querySelector('.leaflet-control-zoom-out').click(); true")
    b.pump(0.6)
    s.add(f"AC-V2-09(b) observation {state}: the map still pans and zooms", panned and zoomed,
          {"panned": panned, "zoomed": zoomed})

    api_days = json.loads(b.js(f"fetch('/api/days').then(r => r.text())"))["days"]
    d0 = api_days[0]
    day = json.loads(b.js(f"fetch('/api/days/{d0}').then(r => r.text())"))["values"]
    b.js("document.getElementById('mode-forecast').focus(); true")
    b.key("Enter")
    b.wait_for("document.querySelectorAll('.pill-icon .pill').length === 6 && "
               "document.querySelector('.pill-icon .pill').textContent !== '–'", 10)
    b.pump(0.5)
    f = b.js("""({pressed: document.getElementById('mode-forecast').getAttribute('aria-pressed'),
        pills: Array.from(document.querySelectorAll('.pill-icon .pill')).map(p => [p.textContent, getComputedStyle(p).backgroundColor]),
        dates: Array.from(document.getElementById('date-select').options).map(o => o.value),
        dateDisabled: document.getElementById('date-select').disabled,
        mapStatus: __chk.visible(document.getElementById('map-status')),
        nowNotice: __chk.visible(document.getElementById('obs-map-state')),
        nowPanel: __chk.visible(document.getElementById('now-panel')),
        forecastPanel: __chk.visible(document.getElementById('forecast-panel')),
        legend: __chk.visible(document.getElementById('forecast-legend')),
        text: document.querySelector('.map-shell').innerText})""")
    s.add(f"AC-V2-09(b) observation {state}: Forecast mode fully normal (six pills = /api/days, Select Date, legend, no Now state shown)",
          f["pressed"] == "true" and [p[0] for p in f["pills"]] == [f"{v['derivedMapTemperature']:.1f}°" for v in day]
          and all(p[1] in BAND_COLOURS for p in f["pills"]) and f["dates"] == api_days and not f["dateDisabled"]
          and not f["mapStatus"] and not f["nowNotice"] and not f["nowPanel"] and f["forecastPanel"] and f["legend"]
          and "Stale" not in f["text"] and "unavailable" not in f["text"].lower(),
          {k: f[k] for k in ("pressed", "pills", "dateDisabled", "mapStatus", "nowNotice")})
    s.shot(f"obs-{state}-forecast-mode")
    region = "南部地區"
    series = json.loads(b.js(f"fetch('/api/regions/' + encodeURIComponent('{region}') + '/series').then(r => r.text())"))["series"]
    b.js(f"var r=document.getElementById('region-select'); r.value='{region}'; r.dispatchEvent(new Event('change')); true")
    b.wait_for(f"document.getElementById('panel-heading').textContent.indexOf('{region}') >= 0 && "
               "document.querySelectorAll('#table-body tr').length === 7", 10)
    b.pump(0.4)
    dash = b.js("""({visible: __chk.visible(document.getElementById('dashboard')),
        error: __chk.visible(document.getElementById('page-error')),
        rows: Array.from(document.querySelectorAll('#table-body tr')).map(tr => tr.children[0].textContent),
        chart: document.querySelectorAll('#chart svg polyline').length})""")
    s.add(f"AC-V2-09(b) observation {state}: the lower dashboard works (Select Region -> seven rows = /api/, chart drawn)",
          dash["visible"] and not dash["error"] and dash["rows"] == [r["dataDate"] for r in series] and dash["chart"] == 2,
          dash)
    if not s.mobile:
        b.screenshot(s.out / f"{s.label}-obs-{state}-full-page.png", full_page=True)
    b.js("window.scrollTo(0, 0); document.getElementById('mode-now').focus(); true")
    b.key("Enter")
    b.pump(0.8)
    back = s.state()
    s.add(f"AC-V2-09(b) back in Now mode the {state} state is still shown, unchanged",
          back["state"] == state and back["nowPressed"] == "true"
          and (back["chip"] == ("STALE" if state == "stale" else "UNAVAILABLE")),
          {k: back[k] for k in ("state", "chip", "nowPressed")})


# --- scenario A: age never triggers Stale --------------------------------------------------


def scenario_age(chrome: str, rig: Rig, out: Path, checks: Checks, network: dict) -> None:
    s = Session(chrome, rig, out, checks, "age", 1280, 900, False)
    try:
        rig.set("ok", "h0")
        st = s.open()
        ok = expect_success(st)
        t0 = s.b.js("Date.now()")
        budget = 2 * 3600 * 1000 + 5 * 60 * 1000  # > 2 hours of page time
        s.b.send("Emulation.setVirtualTimePolicy", {"policy": "advance", "budget": budget})
        end = time.time() + 60
        expired = False
        while time.time() < end and not expired:
            s.b.pump(0.2)
            expired = any(e["method"] == "Emulation.virtualTimeBudgetExpired" for e in s.b.events)
        t1 = s.b.js("Date.now()")
        st2 = s.state()
        s.add("AC-V2-08(d) page clock advanced > 2 h with no failure -> still success, no Stale",
              ok and expired and t1 - t0 >= 2 * 3600 * 1000 and expect_success(st2) and st2["time"] == st["time"],
              {"advanced_ms": t1 - t0, "expired": expired, "state": st2["state"], "chip": st2["chip"]})
        # a Refresh answered from the reuse window after that (same Fetched Time) -> not-newer, still no Stale
        rig.set("ok", "h0", fresh=False)
        st3, _ = s.refresh()
        s.add("AC-V2-08(d) after the clock advance a not-newer Refresh is still success, not Stale",
              expect_success(st3) and st3["result"] == "not-newer", {k: st3[k] for k in ("state", "result", "status")})
        network["age"] = s.b.request_urls()
    finally:
        s.close()


# --- H-1 / H-3 sweeps ------------------------------------------------------------------------


def leak_sweep(checks: Checks, sessions: list[Session], log_text: str) -> None:
    for s in sessions:
        bodies = s.obs_bodies()
        bad_bodies = [b["status"] for b in bodies if any(x in b["text"] for x in LEAKS)]
        bad_dom = [i for i, html in enumerate(s.dom_snapshots)
                   if any(x in html for x in LEAKS + (PLATFORM_MARKER,))]
        console = json.dumps([e for e in s.b.events if e["method"] in
                              ("Runtime.consoleAPICalled", "Runtime.exceptionThrown", "Log.entryAdded")])
        bad_console = [x for x in LEAKS if x in console]
        texts = " ".join(s.dom_snapshots)
        s.add("H-1 no key / upstream URL / upstream body in any observation answer, page DOM (every state) or console",
              not bad_bodies and not bad_dom and not bad_console and len(bodies) > 0,
              {"answers": len(bodies), "dom_snapshots": len(s.dom_snapshots), "bad_answers": bad_bodies,
               "bad_dom": bad_dom, "bad_console": bad_console})
        words = FORBIDDEN_WORDS.findall(re.sub(r"<[^>]+>", " ", texts.replace("aria-live", "")))
        s.add("H-3 no real-time / realtime / live wording in any state", not words, words)
        s.add("console: no JavaScript exception", not [p for p in s.b.console_problems() if p.startswith("exception")],
              s.b.console_problems())
    bad_log = [x for x in LEAKS if x in log_text]
    checks.add("H-1 server log at DEBUG (Flask debug on) carries no key, upstream URL or upstream body",
               not bad_log and "latest observation failed: reason=" in log_text,
               {"bad": bad_log, "lines": log_text.count("\n")})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--chrome", default=None)
    args = parser.parse_args()
    chrome = args.chrome or find_chrome()
    args.out.mkdir(parents=True, exist_ok=True)

    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.DEBUG)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)

    checks = Checks()
    network: dict[str, list[str]] = {}
    rig = Rig()
    sessions: list[Session] = []
    try:
        sessions.append(scenario_refresh(chrome, rig, args.out, checks, network, "desktop", (1280, 900, False), True))
        sessions.append(scenario_unavailable(chrome, rig, args.out, checks, network, "desktop", (1280, 900, False), True))
        sessions.append(scenario_refresh(chrome, rig, args.out, checks, network, "375", (375, 812, True), False))
        sessions.append(scenario_unavailable(chrome, rig, args.out, checks, network, "375", (375, 812, True), False))
        for s in sessions:
            if s.mobile:
                widths = s.b.js("({w: document.documentElement.scrollWidth, i: innerWidth})")
                s.add("R-V2-RSP-2 no horizontal scroll at 375 px in this state sequence", widths["w"] <= widths["i"], widths)
        scenario_age(chrome, rig, args.out, checks, network)
        leak_sweep(checks, sessions, log_stream.getvalue())
    finally:
        for s in sessions:
            s.close()
        rig.close()
        root.removeHandler(handler)

    log, external = {}, []
    for scenario, urls in network.items():
        counts: dict[str, int] = {}
        for url in urls:
            generic = re.sub(r"^http://127\.0\.0\.1:\d+", "http://127.0.0.1:<port>", url)
            counts[generic] = counts.get(generic, 0) + 1
            if not (url.startswith("http://127.0.0.1:") or url.startswith("data:")):
                external.append(url)
        log[scenario] = {"total_requests": len(urls), "urls": counts}
    log["external_requests"] = external
    checks.add("AC-V2-16/INV-V2-3 runtime network log: zero external requests in every state",
               not external and all(v["total_requests"] > 0 for k, v in log.items() if k != "external_requests"),
               external)
    (args.out / "network-log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2), encoding="utf-8")
    (args.out / "browser-check-results.json").write_text(
        json.dumps({"checks": checks.items, "all_pass": checks.ok}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    passed = sum(1 for c in checks.items if c["pass"])
    print(f"{passed}/{len(checks.items)} checks passed; evidence in {args.out}")
    return 0 if checks.ok else 1


if __name__ == "__main__":
    sys.exit(main())
