"""Reproducible browser check for Issue #36 (Now mode / Forecast mode).

Not part of the offline pytest suite (it needs a local Chrome, so it is named so
pytest does not collect it — the same convention as
``check_series_error_visible.py``). It runs the *unmodified*
``server.create_app`` in-process on loopback, twice:

* **A (forecast OK)** — the committed ``data.db``;
* **B (forecast 503)** — a missing database path, so ``/api/health`` and every
  forecast endpoint answer 503 (AC-V2-09(a)).

In both, the Latest Observation service is fed from the committed sanitised
sample ``fixtures/O-A0001-001_sample.json`` through a simulated upstream — no key,
no network (R-V2-TC-3). The simulated upstream derives two variants from the
sample: phase 0 (as captured, plus the 臺北 station's relative humidity and
weather set to the ``-99`` / ``X`` sentinels so the "—" display can be seen) and
phase 1 (every ``ObsTime`` of the capture hour moved one hour later and 臺北's
air temperature changed), which a Refresh then fetches after a delay so the
in-progress indicator is observable.

Headless Chrome is driven over the DevTools protocol (``websocket-client``) at
1280 x 900 and 375 x 812. Every browser request is recorded; the check fails if
any request leaves the loopback origin (INV-V2-3 / AC-V2-16 runtime network log).
Oracles are the exact ``/api/`` response bodies the page received (read back
through the DevTools protocol), never values typed into this script.

Usage (from the unit directory, with the venv active and ``data.db`` present)::

    python tests/check_modes_browser.py                       # writes evidence
    python tests/check_modes_browser.py --out <dir>
    CHROME="/path/to/chrome" python tests/check_modes_browser.py

Exit code 0 means every check passed. Evidence written to ``--out`` (default
``doc/acceptance/screenshots/v2/issue-36/``): PNG screenshots,
``browser-check-results.json`` (every check with its observed values) and
``network-log.json`` (every request URL the browser made, by scenario).
"""

from __future__ import annotations

import argparse
import base64
import copy
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.request
from datetime import timedelta
from pathlib import Path
from wsgiref.simple_server import WSGIRequestHandler, make_server

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

import websocket  # noqa: E402  (websocket-client)

import observation as obs  # noqa: E402
from server import create_app  # noqa: E402

SAMPLE = _UNIT_DIR / "tests" / "fixtures" / "O-A0001-001_sample.json"
DEFAULT_OUT = _UNIT_DIR / "doc" / "acceptance" / "screenshots" / "v2" / "issue-36"
CAPTURE_HOUR = "2026-09-25T23:00:00+08:00"
NEXT_HOUR = "2026-09-26T00:00:00+08:00"
TAIPEI_ID = "466920"
REFRESH_DELAY_SECONDS = 1.5
FORBIDDEN_WORDS = re.compile(r"\b(real-?time|live)\b", re.IGNORECASE)
BAND_COLOURS = {"blue": "rgb(43, 108, 176)", "green": "rgb(47, 133, 90)",
                "yellow": "rgb(214, 158, 46)", "red": "rgb(197, 48, 48)"}


# --- simulated upstream (phase-controlled) ----------------------------------------


class Upstream:
    """A ``requests.get`` stand-in serving sample-derived O-A0001-001 payloads."""

    def __init__(self) -> None:
        raw = json.loads(SAMPLE.read_text(encoding="utf-8"))
        for record in raw["records"]["Station"]:
            if record["StationId"] == TAIPEI_ID:
                record["WeatherElement"]["RelativeHumidity"] = "-99"
                record["WeatherElement"]["Weather"] = "X"
        phase1 = copy.deepcopy(raw)
        for record in phase1["records"]["Station"]:
            if record["ObsTime"]["DateTime"] == CAPTURE_HOUR:
                record["ObsTime"]["DateTime"] = NEXT_HOUR
            if record["StationId"] == TAIPEI_ID:
                record["WeatherElement"]["AirTemperature"] = "26.4"
        self.payloads = [
            json.dumps(raw, ensure_ascii=False).encode("utf-8"),
            json.dumps(phase1, ensure_ascii=False).encode("utf-8"),
        ]
        self.phase = 0
        self.delay = 0.0
        self.calls = 0

    def __call__(self, url, headers=None, params=None, timeout=None):
        self.calls += 1
        if self.delay:
            time.sleep(self.delay)
        body = self.payloads[self.phase]

        class Response:
            status_code = 200
            content = body

            def close(self) -> None:
                pass

        return Response()


class _QuietHandler(WSGIRequestHandler):
    def log_message(self, *args) -> None:  # keep the console readable
        pass


class SecondApartClock:
    """The real Taipei clock, but every reading is at least one second after the last.

    Fetched Time has one-second resolution. With the real clock, a first load and a
    Refresh that fall in the same wall-clock second get the same Fetched Time, and the
    page then correctly reports the Refresh as not-newer (R-V2-OBS-8) — which made the
    "Refresh works while the forecast snapshot is unavailable" check fail at random
    (#38 R2 N-1). Keeping every fetch at least a second apart makes each Refresh a
    genuinely new fetch, which is what that check is about; its assertion is unchanged.
    """

    def __init__(self) -> None:
        self._last = None
        self._lock = threading.Lock()

    def __call__(self):
        with self._lock:
            now = obs._taipei_now().replace(microsecond=0)
            if self._last is not None and now <= self._last:
                now = self._last + timedelta(seconds=1)
            self._last = now
            return now


def start_server(db_path):
    upstream = Upstream()
    service = obs.LatestObservationService(
        env={"CWA_API_KEY": "placeholder-not-a-key"}, http_get=upstream, reuse_window_seconds=0,
        clock=SecondApartClock(),
    )
    app = create_app(db_path=db_path, observation_service=service)
    server = make_server("127.0.0.1", 0, app, handler_class=_QuietHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, upstream, f"http://127.0.0.1:{server.server_port}"


def get_json(url: str):
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode("utf-8"))


# --- Chrome over the DevTools protocol ---------------------------------------------


def find_chrome() -> str:
    candidates = [
        os.environ.get("CHROME"),
        shutil.which("chrome"), shutil.which("google-chrome"), shutil.which("chromium"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise SystemExit("Chrome not found; set CHROME=/path/to/chrome")


def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class Browser:
    def __init__(self, chrome: str) -> None:
        self.profile = tempfile.mkdtemp(prefix="hw01-check-")
        port = free_port()
        self.proc = subprocess.Popen(
            [chrome, "--headless=new", f"--remote-debugging-port={port}",
             f"--user-data-dir={self.profile}", "--no-first-run", "--no-default-browser-check",
             "--disable-extensions", "--disable-background-networking",
             "--disable-component-update", "--disable-sync", "--hide-scrollbars",
             "--force-color-profile=srgb", "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + 20
        ws_url = None
        while time.time() < deadline and ws_url is None:
            try:
                targets = json.loads(urllib.request.urlopen(
                    f"http://127.0.0.1:{port}/json/list", timeout=2).read())
                pages = [t for t in targets if t.get("type") == "page"]
                if pages:
                    ws_url = pages[0]["webSocketDebuggerUrl"]
            except OSError:
                time.sleep(0.2)
        if ws_url is None:
            self.close()
            raise SystemExit("could not attach to Chrome")
        self.ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)
        self.next_id = 0
        self.events: list[dict] = []
        for domain in ("Page", "Runtime", "Network", "Log"):
            self.send(f"{domain}.enable")

    def send(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        my_id = self.next_id
        self.ws.send(json.dumps({"id": my_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == my_id:
                if "error" in message:
                    raise RuntimeError(f"{method}: {message['error']}")
                return message.get("result", {})
            if "method" in message:
                self.events.append(message)

    def pump(self, seconds: float) -> None:
        end = time.time() + seconds
        self.ws.settimeout(0.05)
        try:
            while time.time() < end:
                try:
                    message = json.loads(self.ws.recv())
                except websocket.WebSocketTimeoutException:
                    continue
                if "method" in message:
                    self.events.append(message)
        finally:
            self.ws.settimeout(30)

    def js(self, expression: str):
        result = self.send("Runtime.evaluate", {
            "expression": expression, "returnByValue": True, "awaitPromise": True,
        })
        if "exceptionDetails" in result:
            raise RuntimeError(f"JS error in {expression[:80]!r}: {result['exceptionDetails']}")
        return result["result"].get("value")

    def wait_for(self, expression: str, timeout: float = 10.0, what: str = "") -> bool:
        end = time.time() + timeout
        while time.time() < end:
            if self.js(expression):
                return True
            self.pump(0.1)
        return False

    def viewport(self, width: int, height: int, mobile: bool) -> None:
        self.send("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height, "deviceScaleFactor": 1, "mobile": mobile,
        })

    def navigate(self, url: str) -> None:
        self.send("Page.navigate", {"url": url})
        self.wait_for("document.readyState === 'complete'", 15)

    def key(self, key: str) -> None:
        codes = {"Enter": ("Enter", 13, "\r"), " ": ("Space", 32, " "), "Tab": ("Tab", 9, ""),
                 "ArrowRight": ("ArrowRight", 39, ""), "ArrowDown": ("ArrowDown", 40, "")}
        code, vk, text = codes[key]
        down = {"type": "keyDown", "key": key, "code": code, "windowsVirtualKeyCode": vk}
        if text:
            down["text"] = text
        self.send("Input.dispatchKeyEvent", down)
        self.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": key, "code": code,
                                             "windowsVirtualKeyCode": vk})

    def hover(self, x: float, y: float) -> None:
        self.send("Input.dispatchMouseEvent", {"type": "mouseMoved", "x": x, "y": y})

    def screenshot(self, path: Path, full_page: bool = False) -> None:
        params: dict = {"format": "png"}
        if full_page:
            size = self.js("({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})")
            params.update({"captureBeyondViewport": True,
                           "clip": {"x": 0, "y": 0, "width": size["w"], "height": size["h"], "scale": 1}})
        data = self.send("Page.captureScreenshot", params)["data"]
        path.write_bytes(base64.b64decode(data))

    def response_bodies(self, url_part: str) -> list[dict]:
        """Bodies of every finished response whose URL contains ``url_part``, in order."""
        finished = {e["params"]["requestId"] for e in self.events
                    if e["method"] == "Network.loadingFinished"}
        out = []
        for e in self.events:
            if e["method"] == "Network.responseReceived" and url_part in e["params"]["response"]["url"]:
                rid = e["params"]["requestId"]
                if rid in finished:
                    body = self.send("Network.getResponseBody", {"requestId": rid})
                    text = body["body"] if not body.get("base64Encoded") else base64.b64decode(body["body"]).decode()
                    out.append({"status": e["params"]["response"]["status"], "json": json.loads(text)})
        return out

    def request_urls(self) -> list[str]:
        return [e["params"]["request"]["url"] for e in self.events
                if e["method"] == "Network.requestWillBeSent"]

    def console_problems(self) -> list[str]:
        problems = []
        for e in self.events:
            if e["method"] == "Runtime.exceptionThrown":
                problems.append("exception: " + json.dumps(e["params"]["exceptionDetails"])[:300])
            elif e["method"] == "Runtime.consoleAPICalled":
                text = " ".join(str(a.get("value", a.get("description", ""))) for a in e["params"]["args"])
                if "NaN" in text or "Invalid LatLng" in text or e["params"]["type"] == "error":
                    problems.append("console: " + text[:300])
            elif e["method"] == "Log.entryAdded":
                entry = e["params"]["entry"]
                # 503s of the forecast-unavailable scenario are expected network errors
                if entry["level"] == "error" and entry.get("source") != "network":
                    problems.append("log: " + entry.get("text", "")[:300])
        return problems

    def close(self) -> None:
        try:
            self.ws.close()
        except Exception:  # noqa: BLE001
            pass
        self.proc.terminate()
        try:
            self.proc.wait(10)
        except subprocess.TimeoutExpired:
            self.proc.kill()
        shutil.rmtree(self.profile, ignore_errors=True)


# --- page helpers (evaluated in the page) ---------------------------------------------

JS_HELPERS = r"""
window.__chk = {
  visible: function (el) {
    if (!el) return false;
    var r = el.getBoundingClientRect();
    var cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && !el.closest('[hidden]');
  },
  rect: function (el) { var r = el.getBoundingClientRect(); return {x: r.x, y: r.y, w: r.width, h: r.height}; },
  markerPositions: function (sel) {
    var out = {};
    document.querySelectorAll(sel).forEach(function (el, i) {
      var p = el.querySelector('.spill, .pill');
      var key = p ? (p.getAttribute('aria-label') || String(i)) : String(i);
      var r = el.getBoundingClientRect();
      out[key] = [Math.round(r.x * 10) / 10, Math.round(r.y * 10) / 10];
    });
    return out;
  },
  noNaN: function () {
    var bad = [];
    document.querySelectorAll('.leaflet-marker-icon').forEach(function (el) {
      var t = el.style.transform || '';
      var r = el.getBoundingClientRect();
      if (/NaN/.test(t) || !(r.width > 0 && r.height > 0)) bad.push(t + ' ' + r.width + 'x' + r.height);
    });
    return bad;
  },
};
true;
"""


def fmt_time(text: str, seconds: bool) -> str:
    """The display rule of app.js formatObsTime (re-layout only, no conversion)."""
    m = re.match(r"^(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2})(:\d{2})?(?:\.\d+)?(Z|[+-]\d{2}:?\d{2})?$", text)
    if not m:
        return text
    return m.group(1) + " " + m.group(2) + (m.group(3) if seconds and m.group(3) else "") + \
        (" " + m.group(4) if m.group(4) else "")


def fmt_temp(value) -> str:
    """The display rule of app.js formatObsTemp: the /api/ number, >= one decimal."""
    text = repr(float(value)) if isinstance(value, float) else str(value)
    if isinstance(value, int):
        return f"{value:.1f}"
    return text if ("." in text or "e" in text) else f"{value:.1f}"


def js_string(value) -> str:
    """JavaScript's String(number) for the dashboard table (V1 formatTemp)."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return repr(value) if isinstance(value, float) else str(value)


class Checks:
    def __init__(self) -> None:
        self.items: list[dict] = []

    def add(self, check_id: str, ok: bool, detail) -> None:
        self.items.append({"id": check_id, "pass": bool(ok), "detail": detail})
        print(("PASS " if ok else "FAIL ") + check_id + ("" if ok else f"  {detail}"))

    @property
    def ok(self) -> bool:
        return all(i["pass"] for i in self.items)


def mode_state(b: Browser) -> dict:
    return b.js("""({
      nowPressed: document.getElementById('mode-now').getAttribute('aria-pressed'),
      forecastPressed: document.getElementById('mode-forecast').getAttribute('aria-pressed'),
      nowPanel: __chk.visible(document.getElementById('now-panel')),
      forecastPanel: __chk.visible(document.getElementById('forecast-panel')),
      legend: __chk.visible(document.getElementById('forecast-legend')),
      stations: document.querySelectorAll('.station-icon').length,
      pills: document.querySelectorAll('.pill-icon').length,
    })""")


def map_card_text(b: Browser) -> str:
    """Visible text of the map area (panels, map, legend) below the card head."""
    return b.js("document.querySelector('.map-shell').innerText")


def focus_and_key(b: Browser, selector: str, key: str) -> None:
    b.js(f"document.querySelector({json.dumps(selector)}).focus(); true")
    b.key(key)
    b.pump(0.3)


# --- scenario A: forecast OK -----------------------------------------------------------


def scenario_forecast_ok(chrome: str, out: Path, checks: Checks, network: dict) -> None:
    server, upstream, base = start_server(None)
    api_days = get_json(base + "/api/days")["days"]
    api_day = {d: get_json(base + "/api/days/" + d)["values"] for d in api_days[:3]}
    api_health = get_json(base + "/api/health")
    api_regions = get_json(base + "/api/regions")["regions"]
    api_series = {r: get_json(base + "/api/regions/" + urllib.request.quote(r) + "/series")["series"]
                  for r in api_regions}
    b = Browser(chrome)
    try:
        # ---------------- desktop 1280 ----------------
        b.viewport(1280, 900, False)
        b.navigate(base + "/")
        b.js(JS_HELPERS)
        st = mode_state(b)  # right after load, before any user action
        checks.add("A-desktop AC-V2-01 opens in Now mode without user action",
                   st["nowPressed"] == "true" and st["forecastPressed"] == "false" and st["nowPanel"]
                   and not st["forecastPanel"] and not st["legend"], st)
        loaded = b.wait_for("document.getElementById('obs-count').textContent !== '—'", 15)
        b.pump(0.8)
        bodies = b.response_bodies("/api/observations/latest")
        body = bodies[0]["json"] if bodies else {}
        reps = body.get("representativeStationIds", [])
        by_id = {s["stationId"]: s for s in body.get("stations", [])}
        panel = b.js("""({
          dts: Array.from(document.querySelectorAll('#now-panel dt')).map(e => e.textContent.trim()),
          time: document.getElementById('obs-time').textContent,
          fetched: document.getElementById('obs-fetched').textContent,
          count: document.getElementById('obs-count').textContent,
          refresh: document.getElementById('refresh-button').textContent.trim(),
          heading: document.querySelector('#now-panel .map-panel__title').textContent.trim(),
        })""")
        checks.add("A-desktop AC-V2-04 Observation Time / Fetched Time / count equal the /api/ response",
                   loaded and panel["dts"][:2] == ["Observation Time", "Fetched Time"]
                   and panel["time"] == fmt_time(body["observationTime"], False)
                   and panel["fetched"] == fmt_time(body["fetchedTime"], True)
                   and panel["count"] == str(body["validStationCount"])
                   and panel["refresh"] == "Refresh" and panel["heading"].startswith("Latest Observation"),
                   {"panel": panel, "api": {k: body.get(k) for k in ("observationTime", "fetchedTime", "validStationCount")}})
        markers = b.js("""Array.from(document.querySelectorAll('.station-icon .spill')).map(p => ({
            text: p.textContent, label: p.getAttribute('aria-label'),
            name: p.parentElement.querySelector('.slabel').textContent }))""")
        expected = [{"text": fmt_temp(by_id[i]["airTemperature"]) + "°", "name": by_id[i]["stationName"],
                     "county": by_id[i]["countyName"]} for i in reps]
        counties = [m["label"].split(", ")[1].split(":")[0] for m in markers]
        checks.add("A-desktop AC-V2-03/DD-2 one marker per county, text = /api/ airTemperature, name = station",
                   len(markers) == len(reps) == 22 and len(set(counties)) == len(counties)
                   and all(m["text"] == e["text"] and m["name"] == e["name"] and e["county"] in m["label"]
                           for m, e in zip(markers, expected)),
                   {"markers": markers[:5], "expected": expected[:5], "count": len(markers)})
        checks.add("A-desktop H-3 marker never labelled as a county value",
                   all(" station, " in m["label"] and "station value" in m["label"] for m in markers),
                   markers[:3])
        fills = b.js("Array.from(new Set(Array.from(document.querySelectorAll('.station-icon .spill')).map(p => getComputedStyle(p).backgroundColor)))")
        checks.add("A-desktop AC-V2-02/MODE-6(b) observation markers use no derived band colour",
                   bool(fills) and not set(fills) & set(BAND_COLOURS.values()), fills)
        toggle = b.js("""(function(){var r=document.querySelector('.mode-toggle').getBoundingClientRect();
            return {top:r.top,bottom:r.bottom,innerHeight:innerHeight,scrollY:scrollY,
            now:document.getElementById('mode-now').textContent.trim(),
            forecast:document.getElementById('mode-forecast').textContent.trim()};})()""")
        checks.add("A-desktop AC-V2-01 mode switch visible without scrolling, labels contain Now/Forecast",
                   toggle["scrollY"] == 0 and toggle["top"] >= 0 and toggle["bottom"] <= toggle["innerHeight"]
                   and "Now" in toggle["now"] and "Forecast" in toggle["forecast"], toggle)
        now_text = map_card_text(b)
        checks.add("A-desktop AC-V2-02 Now mode shows no Select Date / derived legend / DERIVED / forecast pills",
                   "Select Date" not in now_text and "Derived map temperature" not in now_text
                   and "DERIVED" not in now_text and mode_state(b)["pills"] == 0,
                   now_text[:400])
        page_text = b.js("document.body.innerText")
        checks.add("A-desktop AC-V2-02/23 no real-time / realtime / live wording; Latest Observation present",
                   not FORBIDDEN_WORDS.search(page_text) and "Latest Observation" in page_text,
                   FORBIDDEN_WORDS.findall(page_text))
        labels = b.js("""({ing: document.getElementById('ingestion-time').textContent,
            fetchedRect: __chk.rect(document.getElementById('obs-fetched')),
            ingRect: __chk.rect(document.getElementById('ingestion-time')),
            fetchedInNow: !!document.getElementById('obs-fetched').closest('#now-panel'),
            ingInForecast: !!document.getElementById('ingestion-time').closest('#forecast-section')})""")
        checks.add("A-desktop AC-V2-02 Now Fetched Time distinguishable (text + position) from the forecast snapshot time",
                   labels["ing"].startswith("Last updated (data fetched from CWA): ")
                   and labels["ing"].endswith(api_health["ingestion_time"])
                   and "Fetched Time" not in labels["ing"] and labels["fetchedInNow"] and labels["ingInForecast"]
                   and abs(labels["fetchedRect"]["y"] - labels["ingRect"]["y"]) > 100, labels)
        b.screenshot(out / "desktop-now-default.png")

        # hover a marker (澎湖, isolated) -> tooltip with station + county
        target = reps.index("467350") if "467350" in reps else 0
        center = b.js(f"""(function(){{var p=document.querySelectorAll('.station-icon .spill')[{target}];
            var r=p.getBoundingClientRect(); return [r.x+r.width/2, r.y+r.height/2];}})()""")
        b.hover(center[0] - 1, center[1] - 1)
        b.hover(center[0], center[1])
        shown = b.wait_for("!!document.querySelector('.leaflet-tooltip.map-tip')", 5)
        tip = b.js("(document.querySelector('.leaflet-tooltip.map-tip')||{}).innerText || ''")
        s = by_id[reps[target]]
        checks.add("A-desktop DD-2 hover shows station name + county, labelled a station value",
                   shown and s["stationName"] in tip and s["countyName"] in tip
                   and "Station value, not a county value" in tip, tip)
        b.screenshot(out / "desktop-now-hover-tooltip.png")
        b.hover(5, 5)

        # keyboard: Tab from the top reaches the Now button first; select 臺北 by Enter
        b.js("document.activeElement && document.activeElement.blur(); window.scrollTo(0,0); true")
        b.key("Tab")
        first_focus = b.js("document.activeElement.id")
        checks.add("A-desktop AC-V2-01 mode switch reachable by keyboard (first Tab stop)",
                   first_focus == "mode-now", first_focus)
        taipei_index = reps.index(TAIPEI_ID)
        b.js(f"document.querySelectorAll('.station-icon .spill')[{taipei_index}].focus(); true")
        b.key("Enter")
        b.pump(0.3)
        sel = b.js("""({hidden: document.getElementById('obs-selected').hidden,
            name: document.getElementById('obs-sel-name').textContent,
            place: document.getElementById('obs-sel-place').textContent,
            temp: document.getElementById('obs-sel-temp').textContent,
            rh: document.getElementById('obs-sel-rh').textContent,
            weather: document.getElementById('obs-sel-weather').textContent,
            time: document.getElementById('obs-sel-time').textContent,
            active: Array.from(document.querySelectorAll('.station-icon.is-active')).length})""")
        t = by_id[TAIPEI_ID]
        checks.add("A-desktop AC-V2-03 selected station values = /api/; sentinel fields shown as —",
                   not sel["hidden"] and sel["name"] == t["stationName"] + " station"
                   and t["countyName"] in sel["place"] and sel["temp"] == fmt_temp(t["airTemperature"]) + " °C"
                   and t["relativeHumidity"] is None and sel["rh"] == "—"
                   and t["weather"] is None and sel["weather"] == "—"
                   and sel["time"] == fmt_time(t["observationTime"], False) and sel["active"] == 1,
                   {"shown": sel, "api": {k: t[k] for k in ("stationName", "airTemperature", "relativeHumidity", "weather", "observationTime")}})

        # zoom in once and pan with the keyboard, then record the Now view
        b.js("document.querySelector('.leaflet-control-zoom-in').click(); true")
        b.pump(0.8)
        b.js("document.getElementById('map').focus(); true")
        b.key("ArrowRight")
        b.key("ArrowDown")
        b.pump(0.8)
        view_before = b.js("__chk.markerPositions('.station-icon')")
        b.screenshot(out / "desktop-now-selected-zoomed.png")

        # Refresh: in-progress indicator, then success with the newer hour
        upstream.phase, upstream.delay = 1, REFRESH_DELAY_SECONDS
        requests_before = len([u for u in b.request_urls() if "/api/observations/latest" in u])
        focus_and_key(b, "#refresh-button", "Enter")
        busy = b.js("""({aria: document.getElementById('refresh-button').getAttribute('aria-disabled'),
            cls: document.getElementById('obs-status').className,
            text: document.getElementById('obs-status').textContent,
            spinner: !!document.querySelector('#obs-status .spinner'),
            busyPanel: document.getElementById('now-panel').getAttribute('aria-busy')})""")
        b.screenshot(out / "desktop-now-refresh-in-progress.png")
        b.key("Enter")  # a second trigger while in progress is ignored
        done = b.wait_for("document.getElementById('refresh-button').getAttribute('aria-disabled') === 'false'", 15)
        b.pump(0.8)
        requests_after = len([u for u in b.request_urls() if "/api/observations/latest" in u])
        body2 = b.response_bodies("/api/observations/latest")[-1]["json"]
        after = b.js("""({time: document.getElementById('obs-time').textContent,
            fetched: document.getElementById('obs-fetched').textContent,
            status: document.getElementById('obs-status').textContent,
            temp: document.getElementById('obs-sel-temp').textContent})""")
        checks.add("A-desktop AC-V2-04/OBS-7(c) Refresh shows an in-progress indicator",
                   busy["aria"] == "true" and "obs-status--busy" in busy["cls"] and busy["spinner"]
                   and "Refreshing" in busy["text"] and busy["busyPanel"] == "true", busy)
        checks.add("A-desktop OBS-7 Refresh success applies the newer Latest Observation; a second press while busy is ignored",
                   done and requests_after - requests_before == 1
                   and body2["observationTime"] == NEXT_HOUR
                   and after["time"] == fmt_time(body2["observationTime"], False)
                   and after["fetched"] == fmt_time(body2["fetchedTime"], True)
                   and after["temp"] == fmt_temp(26.4) + " °C"
                   # #37: a newer result is announced next to Refresh
                   and after["status"] == "Updated to a newer Latest Observation.",
                   {"after": after, "requests": requests_after - requests_before})
        b.screenshot(out / "desktop-now-after-refresh.png")
        view_before = b.js("__chk.markerPositions('.station-icon')")

        # Forecast mode by keyboard
        dash_now = b.js("document.getElementById('dashboard').innerText")
        focus_and_key(b, "#mode-forecast", "Enter")
        b.pump(1.0)
        st = mode_state(b)
        pills = b.js("""Array.from(document.querySelectorAll('.pill-icon .pill')).map(p => {
            var m = document.getElementById('map').getBoundingClientRect(); var r = p.getBoundingClientRect();
            return {text: p.textContent, bg: getComputedStyle(p).backgroundColor,
                    inside: r.left >= m.left && r.right <= m.right && r.top >= m.top && r.bottom <= m.bottom,
                    label: p.getAttribute('aria-label')}; })""")
        d0 = api_days[0]
        exp = [f"{v['derivedMapTemperature']:.1f}°" for v in api_day[d0]]
        checks.add("A-desktop AC-V2-01 Forecast mode: switch by keyboard, six Region markers visible",
                   st["forecastPressed"] == "true" and st["forecastPanel"] and st["legend"]
                   and not st["nowPanel"] and st["stations"] == 0 and len(pills) == 6
                   and all(p["inside"] for p in pills), {"state": st, "pills": pills})
        checks.add("A-desktop AC-17 pill text/colour = /api/days/<d> derived value and band",
                   [p["text"] for p in pills] == exp
                   and all(p["bg"] == BAND_COLOURS[v["colourBand"]] for p, v in zip(pills, api_day[d0])),
                   {"pills": [(p["text"], p["bg"]) for p in pills], "api": [(v["regionName"], v["derivedMapTemperature"], v["colourBand"]) for v in api_day[d0]]})
        legend = b.js("""({sw: Array.from(document.querySelectorAll('#forecast-legend .band-swatch')).map(e => getComputedStyle(e).backgroundColor),
            note: document.querySelector('#forecast-legend .map-legend__note').textContent,
            dates: Array.from(document.getElementById('date-select').options).map(o => o.value),
            selected: document.getElementById('date-select').value,
            disabled: document.getElementById('date-select').disabled})""")
        checks.add("A-desktop AC-17/AC-18 legend four bands + derived caveat; Select Date = seven days ascending, first default",
                   legend["sw"] == [BAND_COLOURS[k] for k in ("blue", "green", "yellow", "red")]
                   and "derived value" in legend["note"] and legend["dates"] == api_days
                   and legend["dates"] == sorted(legend["dates"]) and len(legend["dates"]) == 7
                   and legend["selected"] == api_days[0] and not legend["disabled"], legend)
        f_text = map_card_text(b)
        checks.add("A-desktop AC-V2-02 Forecast mode shows no Refresh / Observation Time / Fetched Time / station values",
                   "Refresh" not in f_text and "Observation Time" not in f_text and "Fetched Time" not in f_text
                   and "Latest Observation" not in f_text and "DERIVED" in f_text, f_text[:500])
        # click a pill (keyboard) -> Region, Date, Min, Max, derived
        central = next(i for i, v in enumerate(api_day[d0]) if v["regionName"] == "中部地區")
        b.js(f"document.querySelectorAll('.pill-icon .pill')[{central}].focus(); true")
        b.key("Enter")
        b.pump(0.3)
        block = b.js("""({r: document.getElementById('sel-region').textContent, d: document.getElementById('sel-date').textContent,
            mn: document.getElementById('sel-min').textContent, mx: document.getElementById('sel-max').textContent,
            dv: document.getElementById('sel-derived').textContent})""")
        v = api_day[d0][central]
        checks.add("A-desktop AC-17 selecting a Region pill shows Region/Date/Min/Max/derived = endpoint",
                   block == {"r": "中部地區", "d": d0, "mn": f"{v['mint']:.1f} °C", "mx": f"{v['maxt']:.1f} °C",
                             "dv": f"{v['derivedMapTemperature']:.1f}"}, {"block": block, "api": v})
        b.screenshot(out / "desktop-forecast-ac17.png")
        pos_before_date = b.js("__chk.markerPositions('.pill-icon')")
        d2 = api_days[2]
        b.js(f"var s=document.getElementById('date-select'); s.value={json.dumps(d2)}; s.dispatchEvent(new Event('change')); true")
        b.wait_for(f"document.getElementById('map-forecast-day').textContent === {json.dumps(d2)}", 10)
        b.pump(0.5)
        pills2 = b.js("Array.from(document.querySelectorAll('.pill-icon .pill')).map(p => [p.textContent, getComputedStyle(p).backgroundColor])")
        block2 = b.js("({d: document.getElementById('sel-date').textContent, dv: document.getElementById('sel-derived').textContent})")
        v2 = api_day[d2]
        pos_after_date = b.js("__chk.markerPositions('.pill-icon')")
        checks.add("A-desktop AC-18 Select Date change updates pills and panel to that day, view not reset",
                   [p[0] for p in pills2] == [f"{x['derivedMapTemperature']:.1f}°" for x in v2]
                   and all(p[1] == BAND_COLOURS[x["colourBand"]] for p, x in zip(pills2, v2))
                   and block2["d"] == d2 and block2["dv"] == f"{v2[central]['derivedMapTemperature']:.1f}"
                   and list(pos_before_date.values()) == list(pos_after_date.values()),
                   {"pills": pills2, "block": block2})
        b.screenshot(out / "desktop-forecast-ac18-date3.png")
        dash_forecast = b.js("document.getElementById('dashboard').innerText")
        checks.add("A-desktop AC-V2-02 lower dashboard identical in both modes",
                   dash_now == dash_forecast and len(dash_now) > 50, len(dash_now))

        # back to Now by keyboard (Space): view and selection restored
        focus_and_key(b, "#mode-now", " ")
        b.pump(1.0)
        view_after = b.js("__chk.markerPositions('.station-icon')")
        sel_after = b.js("""({hidden: document.getElementById('obs-selected').hidden,
            name: document.getElementById('obs-sel-name').textContent,
            active: Array.from(document.querySelectorAll('.station-icon.is-active .spill')).map(p => p.getAttribute('aria-label'))})""")
        checks.add("A-desktop AC-V2-01/MODE-5 Now -> Forecast -> Now restores the Now selection and view",
                   view_after == view_before and not sel_after["hidden"]
                   and sel_after["name"] == t["stationName"] + " station" and len(sel_after["active"]) == 1
                   and sel_after["active"][0].startswith(t["stationName"] + " station"),
                   {"same_view": view_after == view_before, "selection": sel_after})
        checks.add("A-desktop AC-V2-15 no NaN / 0x0 markers after the mode switches",
                   b.js("__chk.noNaN()") == [], b.js("__chk.noNaN()"))

        # lower dashboard = V1 (AC-02 / AC-03 / AC-24 dashboard side)
        dash = b.js("""({options: Array.from(document.getElementById('region-select').options).map(o => o.value),
            heading: document.getElementById('panel-heading').textContent,
            rows: Array.from(document.querySelectorAll('#table-body tr')).map(tr => Array.from(tr.children).map(td => td.textContent)),
            headers: Array.from(document.querySelectorAll('.table thead th')).map(th => th.textContent),
            title: document.querySelector('h1').textContent, label: document.querySelector('label[for=region-select]').textContent})""")
        first_region = api_regions[0]
        checks.add("A-desktop AC-02/AC-03/AC-24 lower dashboard: title, Select Region six names in order, 7-row table = /api/",
                   dash["title"] == "Taiwan Weather Forecast" and dash["label"] == "Select Region"
                   and dash["options"] == api_regions and dash["headers"] == ["Date", "MinT", "MaxT"]
                   and dash["rows"] == [[r["dataDate"], js_string(r["mint"]), js_string(r["maxt"])]
                                        for r in api_series[first_region]],
                   dash)
        b.screenshot(out / "desktop-full-page-now.png", full_page=True)

        # ---------------- 375 x 812 ----------------
        upstream.phase, upstream.delay = 0, 0.0
        b.viewport(375, 812, True)
        b.navigate(base + "/")
        b.js(JS_HELPERS)
        b.wait_for("document.getElementById('obs-count').textContent !== '—'", 15)
        b.pump(0.8)
        m = b.js("""(function(){var r=document.querySelector('.mode-toggle').getBoundingClientRect();
            return {top:r.top,bottom:r.bottom,innerHeight:innerHeight,innerWidth:innerWidth,scrollY:scrollY,
            scrollWidth:document.documentElement.scrollWidth,
            nowPressed:document.getElementById('mode-now').getAttribute('aria-pressed'),
            stations:document.querySelectorAll('.station-icon').length,
            time:document.getElementById('obs-time').textContent,
            fetched:document.getElementById('obs-fetched').textContent};})()""")
        checks.add("A-375 AC-V2-01 Now mode default; mode switch visible without scrolling; no horizontal scroll",
                   m["nowPressed"] == "true" and m["scrollY"] == 0 and m["top"] >= 0
                   and m["bottom"] <= m["innerHeight"] and m["scrollWidth"] <= m["innerWidth"]
                   and m["stations"] == 22 and m["time"] != "—" and m["fetched"] != "—", m)
        b.screenshot(out / "375-now-default.png", full_page=True)
        focus_and_key(b, "#mode-forecast", "Enter")
        b.pump(1.0)
        st = mode_state(b)
        inside = b.js("""Array.from(document.querySelectorAll('.pill-icon .pill')).every(p => {
            var m = document.getElementById('map').getBoundingClientRect(); var r = p.getBoundingClientRect();
            return r.left >= m.left && r.right <= m.right && r.top >= m.top && r.bottom <= m.bottom; })""")
        sw = b.js("document.documentElement.scrollWidth <= innerWidth")
        checks.add("A-375 AC-V2-01 Forecast mode: six Region markers visible; no horizontal scroll",
                   st["forecastPressed"] == "true" and st["pills"] == 6 and inside and sw and st["stations"] == 0, st)
        b.screenshot(out / "375-forecast.png", full_page=True)
        b.js("window.scrollTo(0, 0); true")
        focus_and_key(b, "#mode-now", "Enter")
        b.pump(0.8)
        checks.add("A-375 AC-V2-15 no NaN / 0x0 markers after the mode switches",
                   b.js("__chk.noNaN()") == [] and mode_state(b)["stations"] == 22, b.js("__chk.noNaN()"))
        b.pump(0.5)
        checks.add("A console: no JavaScript exception, no NaN / Invalid LatLng message",
                   b.console_problems() == [], b.console_problems())
        network["A_forecast_ok"] = b.request_urls()
    finally:
        b.close()
        server.shutdown()


# --- scenario B: forecast snapshot unavailable (503) -----------------------------------


def scenario_forecast_503(chrome: str, out: Path, checks: Checks, network: dict) -> None:
    missing = _UNIT_DIR / "no-such-database-for-check.db"
    server, upstream, base = start_server(missing)
    health = urllib.request.Request(base + "/api/health")
    try:
        urllib.request.urlopen(health, timeout=10)
        health_status, health_error = 200, None
    except urllib.error.HTTPError as err:
        health_status, health_error = err.code, json.loads(err.read().decode())["error"]
    b = Browser(chrome)
    try:
        for label, (w, h, mobile) in (("desktop", (1280, 900, False)), ("375", (375, 812, True))):
            upstream.phase, upstream.delay = 0, 0.0
            b.viewport(w, h, mobile)
            b.navigate(base + "/")
            b.js(JS_HELPERS)
            ok_now = b.wait_for("document.getElementById('obs-count').textContent !== '—'", 15)
            b.wait_for("!document.getElementById('page-error').hidden", 10)
            b.pump(0.5)
            state = b.js("""({mode: document.getElementById('mode-now').getAttribute('aria-pressed'),
                stations: document.querySelectorAll('.station-icon').length,
                mapCard: __chk.visible(document.querySelector('.map-card')),
                nowPanel: __chk.visible(document.getElementById('now-panel')),
                error: __chk.visible(document.getElementById('page-error')),
                errorRole: document.getElementById('page-error').getAttribute('role'),
                errorText: document.getElementById('page-error-text').textContent,
                errorInSection: !!document.getElementById('page-error').closest('#forecast-section'),
                dashboard: __chk.visible(document.getElementById('dashboard')),
                toggleVisible: __chk.visible(document.querySelector('.mode-toggle'))})""")
            checks.add(f"B-{label} AC-V2-09(a) forecast 503: Now mode fully shown, section-level V1 error with server message",
                       health_status == 503 and ok_now and state["mode"] == "true" and state["stations"] == 22
                       and state["mapCard"] and state["nowPanel"] and state["toggleVisible"]
                       and state["error"] and state["errorRole"] == "alert" and state["errorText"] == health_error
                       and state["errorInSection"] and not state["dashboard"],
                       {"health": [health_status, health_error], "page": state})
            b.screenshot(out / f"{label}-forecast503-now-ok.png", full_page=True)
            # Refresh still works while the forecast is down
            upstream.phase = 1
            focus_and_key(b, "#refresh-button", "Enter")
            refreshed = b.wait_for(
                f"document.getElementById('obs-time').textContent.indexOf({json.dumps(NEXT_HOUR[:10])}) === 0", 15)
            checks.add(f"B-{label} AC-V2-09(a) Refresh works while the forecast snapshot is unavailable",
                       refreshed, b.js("document.getElementById('obs-time').textContent"))
            # Forecast mode shows the inline error with the server message
            focus_and_key(b, "#mode-forecast", "Enter")
            b.pump(0.8)
            inline = b.js("""({shown: __chk.visible(document.getElementById('map-status')),
                role: document.getElementById('map-status').getAttribute('role'),
                text: document.getElementById('map-status').textContent,
                dateDisabled: document.getElementById('date-select').disabled,
                panel: __chk.visible(document.getElementById('forecast-panel')),
                pressed: document.getElementById('mode-forecast').getAttribute('aria-pressed')})""")
            checks.add(f"B-{label} AC-V2-09(a)/AC-10 Forecast mode inline error with server message; Select Date disabled",
                       inline["shown"] and inline["role"] == "alert" and inline["text"] == health_error
                       and inline["dateDisabled"] and inline["panel"] and inline["pressed"] == "true", inline)
            b.screenshot(out / f"{label}-forecast503-forecast-mode.png", full_page=(label == "375"))
            focus_and_key(b, "#mode-now", "Enter")
            b.pump(0.6)
            back = b.js("""({status: __chk.visible(document.getElementById('map-status')),
                stations: document.querySelectorAll('.station-icon').length})""")
            checks.add(f"B-{label} AC-V2-09(a) back in Now mode the forecast error does not cover the map",
                       not back["status"] and back["stations"] == 22, back)
        network["B_forecast_503"] = b.request_urls()
    finally:
        b.close()
        server.shutdown()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--chrome", default=None)
    args = parser.parse_args()
    chrome = args.chrome or find_chrome()
    args.out.mkdir(parents=True, exist_ok=True)
    checks = Checks()
    network: dict[str, list[str]] = {}
    scenario_forecast_ok(chrome, args.out, checks, network)
    scenario_forecast_503(chrome, args.out, checks, network)

    # Runtime network log: every request stays on the loopback origin (INV-V2-3).
    log = {}
    external = []
    for scenario, urls in network.items():
        counts: dict[str, int] = {}
        for url in urls:
            generic = re.sub(r"^http://127\.0\.0\.1:\d+", "http://127.0.0.1:<port>", url)
            counts[generic] = counts.get(generic, 0) + 1
            if not (url.startswith("http://127.0.0.1:") or url.startswith("data:")):
                external.append(url)
        log[scenario] = {"total_requests": len(urls), "urls": counts}
    log["external_requests"] = external
    checks.add("AC-V2-16 runtime network log: zero external requests (Now mode and Forecast mode)",
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
