"""V2 Latest Observation path (Issue #35; SPEC-V2 §2.2, §2.4, §2.5, §2.9).

Fully offline (R-V2-TC-3 / V1 R-TC-5): every upstream response is simulated —
either derived from the committed sanitised real sample
``fixtures/O-A0001-001_sample.json`` (captured once under OC-V2 A-3) or produced
by a loopback-only socket server for the stall cases. No test reads ``.env`` or
needs a real key; the key used below is a sentinel that must never appear in any
response, log line or console output (R-V2-SEC-7, H-1).

Coverage (AC ids from SPEC-V2 v2.2):
* AC-V2-03  normalisation of the real sample; hand-computed expectations for
            six stations; no upstream structure in the response.
* AC-V2-04  dataset Observation Time = max valid ``ObsTime``; Fetched Time format
            and value from a controllable clock.
* AC-V2-05  the eight derived counter-examples.
* AC-V2-06  (API) reuse window with a controllable clock; refetch outside it;
            a stalled / slow upstream ends as ``upstream_unreachable`` in bounded time.
* AC-V2-07  (observation path) the four failure reasons; nothing secret out.
* AC-V2-17(b)(d)  key only from ``CWA_API_KEY``; no key → ``key_not_configured``
            while the forecast path stays healthy.
* INV-V2-1 / INV-V2-4  forecast endpoints and ``/api/health`` answer exactly as
            before with the network blocked and no key.
"""

from __future__ import annotations

import copy
import json
import logging
import socket
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests

import observation as obs
import weather_query as wq
from server import create_app

SAMPLE_PATH = Path(__file__).parent / "fixtures" / "O-A0001-001_sample.json"
SENTINEL_KEY = "SENTINEL-KEY-7f3a9c-must-never-leak"
UPSTREAM_BODY_MARKER = "UPSTREAM-BODY-MARKER-4d21"
UPSTREAM_HOST = "opendata.cwa.gov.tw"
TAIPEI = timezone(timedelta(hours=8))
T0 = datetime(2026, 9, 26, 0, 10, 5, tzinfo=TAIPEI)
SAMPLE_OBS_TIME = "2026-09-25T23:00:00+08:00"
SAMPLE_RECEIVED = 876
SAMPLE_VALID = 849  # 876 records − 27 with the -99 air-temperature sentinel

# Keys of the upstream structure that must never reach the client (AC-V2-03).
UPSTREAM_KEYS = (
    "records", "Station", "WeatherElement", "GeoInfo", "ObsTime", "Coordinates",
    "success", "result", "fields", "GustInfo", "DailyExtreme",
)


# --- helpers -----------------------------------------------------------------------


@pytest.fixture
def sample() -> dict:
    return json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))


def stations_of(payload: dict) -> list[dict]:
    return payload["records"]["Station"]


def station(payload: dict, station_id: str) -> dict:
    return next(s for s in stations_of(payload) if s["StationId"] == station_id)


class FakeResponse:
    def __init__(self, status: int, content: bytes):
        self.status_code = status
        self.content = content

    def close(self) -> None:
        pass


class FakeUpstream:
    """Simulated ``requests.get``: records calls, returns a scripted outcome."""

    def __init__(self, outcome):
        self.outcome = outcome
        self.calls: list[dict] = []

    def __call__(self, url, headers=None, params=None, timeout=None):
        self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
        outcome = self.outcome(len(self.calls)) if callable(self.outcome) else self.outcome
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def ok(payload) -> FakeResponse:
    return FakeResponse(200, json.dumps(payload, ensure_ascii=False).encode("utf-8"))


class Clock:
    def __init__(self, now: datetime):
        self.now = now

    def __call__(self) -> datetime:
        return self.now


def service(upstream, *, env=None, clock=None, **kw) -> obs.LatestObservationService:
    return obs.LatestObservationService(
        env={"CWA_API_KEY": SENTINEL_KEY} if env is None else env,
        clock=clock or Clock(T0),
        http_get=upstream,
        **kw,
    )


def latest(payload) -> tuple[int, dict]:
    return service(FakeUpstream(ok(payload))).latest()


def by_id(body: dict) -> dict[str, dict]:
    return {s["stationId"]: s for s in body["stations"]}


def assert_no_upstream_structure(value) -> None:
    if isinstance(value, dict):
        for key, inner in value.items():
            assert key not in UPSTREAM_KEYS, f"upstream key {key!r} leaked"
            assert_no_upstream_structure(inner)
    elif isinstance(value, list):
        for inner in value:
            assert_no_upstream_structure(inner)


# --- AC-V2-03 normalisation of the real sample -------------------------------------

EXPECTED_STATIONS = {
    # normal station, hand-read from the sample
    "C0TB40": {
        "stationId": "C0TB40", "stationName": "崇德", "countyName": "花蓮縣",
        "townName": "秀林鄉", "latitude": 24.166144, "longitude": 121.657414,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 25.5,
        "relativeHumidity": 82, "windSpeed": 1.1, "windDirection": 259.0,
        "airPressure": 1010.8, "precipitation": 0.0, "weather": "晴",
    },
    # sentinel optional fields: WindSpeed / WindDirection are -99 -> null
    "C0TC30": {
        "stationId": "C0TC30", "stationName": "虎頭山", "countyName": "花蓮縣",
        "townName": "萬榮鄉", "latitude": 23.52849, "longitude": 121.33992,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 19.7,
        "relativeHumidity": 93, "windSpeed": None, "windDirection": None,
        "airPressure": 888.4, "precipitation": 0.5, "weather": "晴",
    },
    # sentinel optional field: AirPressure is -99 -> null
    "C2I260": {
        "stationId": "C2I260", "stationName": "北坑", "countyName": "南投縣",
        "townName": "埔里鎮", "latitude": 23.92463, "longitude": 121.00683,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 21.7,
        "relativeHumidity": 98, "windSpeed": 0.5, "windDirection": 90.0,
        "airPressure": None, "precipitation": 0.5, "weather": "晴",
    },
    # outlying-island county 金門縣
    "C0W240": {
        "stationId": "C0W240", "stationName": "九宮", "countyName": "金門縣",
        "townName": "烈嶼鄉", "latitude": 24.423753, "longitude": 118.240186,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 25.5,
        "relativeHumidity": 85, "windSpeed": 0.4, "windDirection": 101.0,
        "airPressure": 1008.1, "precipitation": 0.0, "weather": "晴",
    },
    # outlying-island county 連江縣
    "467990": {
        "stationId": "467990", "stationName": "馬祖", "countyName": "連江縣",
        "townName": "南竿鄉", "latitude": 26.169467, "longitude": 119.923158,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 24.6,
        "relativeHumidity": 90, "windSpeed": 0.8, "windDirection": 10.0,
        "airPressure": 1003.1, "precipitation": 0.0, "weather": "晴",
    },
    # densest county 臺北市
    "C0AH70": {
        "stationId": "C0AH70", "stationName": "松山", "countyName": "臺北市",
        "townName": "松山區", "latitude": 25.048711, "longitude": 121.550428,
        "observationTime": SAMPLE_OBS_TIME, "airTemperature": 26.2,
        "relativeHumidity": 86, "windSpeed": 2.3, "windDirection": 82.0,
        "airPressure": 1009.1, "precipitation": 0.0, "weather": "晴",
    },
}
# Air temperature is the -99 sentinel for these: they must not be in the response.
SENTINEL_TEMPERATURE_STATIONS = ("C0TC00", "A0W080")


def test_sample_normalises_to_hand_computed_stations(sample) -> None:
    status, body = latest(sample)
    assert status == 200
    stations = by_id(body)
    for station_id, expected in EXPECTED_STATIONS.items():
        assert stations[station_id] == expected, station_id
    for station_id in SENTINEL_TEMPERATURE_STATIONS:
        assert station_id not in stations  # sentinel never becomes -99 °C
    assert body["dataset"] == "O-A0001-001"
    assert body["validStationCount"] == SAMPLE_VALID == len(body["stations"])
    assert body["receivedStationCount"] == SAMPLE_RECEIVED


def test_every_station_has_the_contract_fields(sample) -> None:
    _, body = latest(sample)
    required = {"stationId", "stationName", "countyName", "townName", "latitude",
                "longitude", "observationTime", "airTemperature"}
    optional = {"relativeHumidity", "windSpeed", "windDirection", "airPressure",
                "precipitation", "weather"}
    for s in body["stations"]:
        assert set(s) == required | optional
        assert isinstance(s["airTemperature"], (int, float))
        assert s["airTemperature"] not in (-99, -98, 990)
        for field in optional:
            assert s[field] is None or s[field] not in (-99, -98, 990, "-99", "X", "T")
    assert {s["countyName"] for s in body["stations"]} == obs.COUNTIES  # 22 incl. islands


def test_response_carries_no_upstream_structure(sample) -> None:
    _, body = latest(sample)
    assert_no_upstream_structure(body)
    assert set(body) == {"dataset", "observationTime", "fetchedTime",
                         "validStationCount", "receivedStationCount", "stations"}


def test_values_are_as_published_not_rounded(sample) -> None:
    """H-3: numbers keep the published digits; ObsTime strings are unchanged."""
    target = station(sample, "C0TB40")
    target["WeatherElement"]["AirTemperature"] = "25.46"
    target["ObsTime"]["DateTime"] = "2026-09-25 23:00"  # different published form
    _, body = latest(sample)
    got = by_id(body)["C0TB40"]
    assert got["airTemperature"] == 25.46
    assert got["observationTime"] == "2026-09-25 23:00"


# --- AC-V2-04 Observation Time and Fetched Time -----------------------------------


def test_dataset_observation_time_is_the_max_valid_obstime(sample) -> None:
    station(sample, "C0AH70")["ObsTime"]["DateTime"] = "2026-09-26T00:00:00+08:00"
    station(sample, "C0W240")["ObsTime"]["DateTime"] = "2026-09-25T22:00:00+08:00"
    _, body = latest(sample)
    assert body["observationTime"] == "2026-09-26T00:00:00+08:00"


def test_sample_dataset_observation_time() -> None:
    sample = json.loads(SAMPLE_PATH.read_text(encoding="utf-8"))
    _, body = latest(sample)
    assert body["observationTime"] == SAMPLE_OBS_TIME


@pytest.mark.parametrize(
    "clock_value, expected",
    [
        (T0, "2026-09-26T00:10:05+08:00"),
        # a UTC clock is presented in +08:00 at second precision
        (datetime(2026, 9, 25, 16, 10, 5, 987654, tzinfo=timezone.utc),
         "2026-09-26T00:10:05+08:00"),
    ],
)
def test_fetched_time_is_the_server_clock_in_plus_0800(sample, clock_value, expected) -> None:
    _, body = service(FakeUpstream(ok(sample)), clock=Clock(clock_value)).latest()
    assert body["fetchedTime"] == expected


def test_default_clock_fetched_time_format(sample) -> None:
    svc = obs.LatestObservationService(
        env={"CWA_API_KEY": SENTINEL_KEY}, http_get=FakeUpstream(ok(sample))
    )
    _, body = svc.latest()
    parsed = datetime.fromisoformat(body["fetchedTime"])
    assert body["fetchedTime"].endswith("+08:00")
    assert len(body["fetchedTime"]) == len("2026-09-26T00:10:05+08:00")
    assert abs((datetime.now(TAIPEI) - parsed).total_seconds()) < 60


# --- AC-V2-05 the eight derived counter-examples ----------------------------------


@pytest.mark.parametrize("bad", ["-99", "X", "", "abc", "-98", "T", "990", "-99.0", "NaN", "inf", None])
def test_ce1_invalid_air_temperature_excludes_only_that_station(sample, bad) -> None:
    _, before = latest(copy.deepcopy(sample))
    target = station(sample, "C0TB40")
    if bad is None:
        del target["WeatherElement"]["AirTemperature"]
    else:
        target["WeatherElement"]["AirTemperature"] = bad
    status, after = latest(sample)
    assert status == 200
    assert "C0TB40" not in by_id(after)
    assert after["validStationCount"] == before["validStationCount"] - 1
    others_before = {k: v for k, v in by_id(before).items() if k != "C0TB40"}
    assert by_id(after) == others_before


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda g: g.__setitem__("Coordinates", [c for c in g["Coordinates"] if c["CoordinateName"] != "WGS84"]), id="no-wgs84"),
        pytest.param(lambda g: g["Coordinates"][1].__setitem__("StationLatitude", "NaN"), id="lat-nan"),
        pytest.param(lambda g: g["Coordinates"][1].__setitem__("StationLongitude", "inf"), id="lon-inf"),
        pytest.param(lambda g: g["Coordinates"][1].__setitem__("StationLatitude", ""), id="lat-empty"),
        pytest.param(lambda g: g["Coordinates"][1].__setitem__("StationLongitude", "-99"), id="lon-sentinel"),
        pytest.param(lambda g: g.pop("Coordinates"), id="no-coordinates"),
    ],
)
def test_ce2_missing_or_non_finite_wgs84_excludes_station(sample, mutate) -> None:
    geo = station(sample, "C0TB40")["GeoInfo"]
    assert geo["Coordinates"][1]["CoordinateName"] == "WGS84"
    mutate(geo)
    status, body = latest(sample)
    assert status == 200
    assert "C0TB40" not in by_id(body)
    assert body["validStationCount"] == SAMPLE_VALID - 1
    assert all(s["latitude"] is not None and s["longitude"] is not None for s in body["stations"])


@pytest.mark.parametrize("county", ["台北市", "東京都", "", None, "臺北"])
def test_ce3_county_outside_the_22_excludes_station(sample, county) -> None:
    station(sample, "C0AH70")["GeoInfo"]["CountyName"] = county
    status, body = latest(sample)
    assert status == 200
    assert "C0AH70" not in by_id(body)
    assert body["validStationCount"] == SAMPLE_VALID - 1


def test_ce4_all_stations_invalid_is_invalid_response(sample) -> None:
    for s in stations_of(sample):
        s["WeatherElement"]["AirTemperature"] = "-99"
    status, body = latest(sample)
    assert status == 502
    assert body["reason"] == "invalid_response"
    assert "stations" not in body


def test_ce5_half_the_stations_removed_is_still_success(sample) -> None:
    kept = stations_of(sample)[::2]
    sample["records"]["Station"] = kept
    # Independent expectation: in this sample the only invalid records are the
    # -99 air-temperature ones, so the remaining valid count is simply this.
    expected_valid = sum(1 for s in kept if s["WeatherElement"]["AirTemperature"] != "-99")
    status, body = latest(sample)
    assert status == 200
    assert body["validStationCount"] == expected_valid == len(body["stations"])
    assert body["receivedStationCount"] == len(kept)


def test_ce6_same_name_different_station_ids_are_independent(sample) -> None:
    # Real duplicates in the sample: 大坑 (C0T9E0 花蓮縣, C0F970 臺中市).
    _, body = latest(copy.deepcopy(sample))
    stations = by_id(body)
    assert stations["C0T9E0"]["stationName"] == stations["C0F970"]["stationName"] == "大坑"
    assert stations["C0T9E0"]["airTemperature"] == 23.0
    assert stations["C0F970"]["airTemperature"] == 26.9
    # Derived: give C0AH70 the name of C0TB40 — both stay, each with its own data.
    station(sample, "C0AH70")["StationName"] = "崇德"
    _, body = latest(sample)
    stations = by_id(body)
    assert stations["C0AH70"]["stationName"] == stations["C0TB40"]["stationName"] == "崇德"
    assert stations["C0AH70"]["airTemperature"] == 26.2
    assert stations["C0TB40"]["airTemperature"] == 25.5
    assert body["validStationCount"] == SAMPLE_VALID


@pytest.mark.parametrize(
    "bad_obs_time",
    [None, "", "not-a-time", "2026-09-25", "2026-13-45T25:61:00+08:00", 20260925, "-99"],
)
def test_ce7_missing_or_unparseable_obstime_excludes_station(sample, bad_obs_time) -> None:
    target = station(sample, "C0AH70")
    if bad_obs_time is None:
        del target["ObsTime"]["DateTime"]
    else:
        target["ObsTime"]["DateTime"] = bad_obs_time
    status, body = latest(sample)
    assert status == 200
    assert "C0AH70" not in by_id(body)
    assert body["validStationCount"] == SAMPLE_VALID - 1  # not counted
    assert body["observationTime"] == SAMPLE_OBS_TIME


def test_ce7_newest_station_corrupted_falls_back_to_the_rest(sample) -> None:
    newest = "2026-09-26T00:00:00+08:00"
    station(sample, "C0AH70")["ObsTime"]["DateTime"] = newest
    _, with_newest = latest(copy.deepcopy(sample))
    assert with_newest["observationTime"] == newest
    station(sample, "C0AH70")["ObsTime"]["DateTime"] = "not-a-time"
    status, body = latest(sample)
    assert status == 200
    assert "C0AH70" not in by_id(body)
    assert body["observationTime"] == SAMPLE_OBS_TIME  # max of the remaining valid
    others = {k: v for k, v in by_id(with_newest).items() if k != "C0AH70"}
    assert by_id(body) == others  # other stations unaffected


def test_ce7_invalid_station_obstime_never_drives_the_dataset_time(sample) -> None:
    """A station invalid for another reason must not contribute its ObsTime."""
    target = station(sample, "C0TC00")  # -99 air temperature → invalid
    target["ObsTime"]["DateTime"] = "2026-09-26T05:00:00+08:00"
    _, body = latest(sample)
    assert body["observationTime"] == SAMPLE_OBS_TIME


def test_ce8_all_obstime_unusable_is_invalid_response(sample) -> None:
    for i, s in enumerate(stations_of(sample)):
        if i % 2:
            s["ObsTime"]["DateTime"] = "not-a-time"
        else:
            del s["ObsTime"]["DateTime"]
    status, body = latest(sample)
    assert status == 502
    assert body["reason"] == "invalid_response"


# --- AC-V2-06 (API) reuse window, refetch, bounded time ----------------------------


def test_reuse_window_returns_the_same_body_then_refetches(sample) -> None:
    upstream = FakeUpstream(lambda n: ok(sample))
    clock = Clock(T0)
    svc = service(upstream, clock=clock)
    status1, first = svc.latest()
    clock.now = T0 + timedelta(seconds=obs.REUSE_WINDOW_SECONDS - 1)
    status2, second = svc.latest()
    assert (status1, status2) == (200, 200)
    assert len(upstream.calls) == 1  # reused, no upstream call
    assert second == first
    assert second["fetchedTime"] == first["fetchedTime"] == "2026-09-26T00:10:05+08:00"
    clock.now = T0 + timedelta(seconds=obs.REUSE_WINDOW_SECONDS)
    _, third = svc.latest()
    assert len(upstream.calls) == 2  # outside the window: refetched
    assert third["fetchedTime"] == "2026-09-26T00:15:05+08:00"


def test_reuse_window_is_within_the_contract_ceiling() -> None:
    assert 0 <= obs.REUSE_WINDOW_SECONDS <= 600
    with pytest.raises(ValueError):
        obs.LatestObservationService(reuse_window_seconds=601)


def test_zero_window_always_refetches(sample) -> None:
    upstream = FakeUpstream(lambda n: ok(sample))
    svc = service(upstream, reuse_window_seconds=0)
    svc.latest()
    svc.latest()
    assert len(upstream.calls) == 2


def test_failure_outside_the_window_is_never_answered_with_old_data(sample) -> None:
    """INV-V2-6 (server): only success or classified failure — never stale data."""
    upstream = FakeUpstream(lambda n: ok(sample) if n == 1 else FakeResponse(500, b"x"))
    clock = Clock(T0)
    svc = service(upstream, clock=clock)
    assert svc.latest()[0] == 200
    clock.now = T0 + timedelta(seconds=obs.REUSE_WINDOW_SECONDS + 1)
    status, body = svc.latest()
    assert status == 502
    assert body["reason"] == "upstream_error"
    assert "stations" not in body and "observationTime" not in body


def test_failures_are_not_reused(sample) -> None:
    upstream = FakeUpstream(lambda n: FakeResponse(503, b"busy") if n == 1 else ok(sample))
    svc = service(upstream)
    assert svc.latest()[0] == 502
    status, body = svc.latest()  # same instant: a failure is never cached
    assert status == 200 and len(upstream.calls) == 2
    assert body["validStationCount"] == SAMPLE_VALID


def test_clock_moving_backwards_does_not_extend_reuse(sample) -> None:
    upstream = FakeUpstream(lambda n: ok(sample))
    clock = Clock(T0)
    svc = service(upstream, clock=clock)
    svc.latest()
    clock.now = T0 - timedelta(seconds=1)
    svc.latest()
    assert len(upstream.calls) == 2


def test_default_bounds_are_below_the_platform_limit() -> None:
    """R-V2-OBS-13: the upstream bound exists and is below the smallest Vercel
    default function duration (10 s) and the 30 s verification instrument."""
    assert 0 < obs.UPSTREAM_DEADLINE_SECONDS < 10
    assert obs.CONNECT_TIMEOUT_SECONDS <= obs.UPSTREAM_DEADLINE_SECONDS
    assert obs.READ_TIMEOUT_SECONDS <= obs.UPSTREAM_DEADLINE_SECONDS


def test_timeouts_are_passed_to_the_http_client(sample) -> None:
    upstream = FakeUpstream(ok(sample))
    service(upstream).latest()
    assert upstream.calls[0]["timeout"] == (obs.CONNECT_TIMEOUT_SECONDS, obs.READ_TIMEOUT_SECONDS)


class _LoopbackServer:
    """A loopback TCP server that accepts and then stalls or drips (never finishes)."""

    def __init__(self, mode: str):
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(5)
        self.sock.settimeout(0.2)
        self.stop = threading.Event()
        self.conns: list[socket.socket] = []
        self.thread = threading.Thread(target=self._serve, daemon=True)
        self.thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.sock.getsockname()[1]}/stall"

    def _serve(self) -> None:
        while not self.stop.is_set():
            try:
                conn, _ = self.sock.accept()
            except OSError:
                continue
            self.conns.append(conn)
            if self.mode == "drip":
                threading.Thread(target=self._drip, args=(conn,), daemon=True).start()
            elif self.mode == "ok":
                threading.Thread(target=self._answer, args=(conn,), daemon=True).start()

    def _answer(self, conn: socket.socket) -> None:
        """Serve the sanitised sample once as a normal 200 JSON response."""
        try:
            conn.recv(65536)
            payload = SAMPLE_PATH.read_bytes()
            head = (b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                    b"Connection: close\r\nContent-Length: "
                    + str(len(payload)).encode() + b"\r\n\r\n")
            conn.sendall(head + payload)
        except OSError:
            pass

    def _drip(self, conn: socket.socket) -> None:
        try:
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n"
                         b"Content-Length: 100000\r\n\r\n{")
            while not self.stop.is_set():
                conn.sendall(b" ")
                time.sleep(0.05)
        except OSError:
            pass

    def close(self) -> None:
        self.stop.set()
        for conn in self.conns:
            conn.close()
        self.sock.close()


@pytest.mark.parametrize("mode", ["stall", "drip"])
def test_stalled_upstream_ends_classified_within_the_bound(mode) -> None:
    """AC-V2-06(e) API side: a stalled or slow-dripping upstream yields an
    ``upstream_unreachable`` JSON well within the bound, via the real HTTP client."""
    server = _LoopbackServer(mode)
    try:
        svc = obs.LatestObservationService(
            env={"CWA_API_KEY": SENTINEL_KEY},
            url=server.url,
            connect_timeout=1.0,
            read_timeout=5.0,  # each read would wait longer than the deadline
            deadline=0.6,
        )
        started = time.monotonic()
        status, body = svc.latest()
        elapsed = time.monotonic() - started
    finally:
        server.close()
    assert status == 504
    assert body["reason"] == "upstream_unreachable"
    assert elapsed < 3.0


def test_real_client_success_logs_no_url_or_key(caplog, capfd) -> None:
    """R-V2-SEC-7 on the success path through the real HTTP client, with every
    logger at DEBUG: neither the upstream address nor the key reaches the log."""
    caplog.set_level(logging.DEBUG)
    server = _LoopbackServer("ok")
    try:
        svc = obs.LatestObservationService(env={"CWA_API_KEY": SENTINEL_KEY}, url=server.url)
        status, body = svc.latest()
    finally:
        server.close()
    assert status == 200 and body["validStationCount"] == SAMPLE_VALID
    out, err = capfd.readouterr()
    for text in (caplog.text, out, err):
        assert SENTINEL_KEY not in text
        assert "127.0.0.1" not in text and "/stall" not in text
    assert not [r for r in caplog.records if r.name.startswith("urllib3")]


# --- AC-V2-07 four failure classes, nothing secret out -----------------------------


def _leak_free(text: str) -> None:
    assert SENTINEL_KEY not in text
    assert UPSTREAM_HOST not in text
    assert UPSTREAM_BODY_MARKER not in text
    assert "Authorization" not in text


FAILURE_CASES = [
    # (id, env, upstream outcome, expected reason, expected upstream status)
    ("no-key", {}, None, "key_not_configured", None),
    ("blank-key", {"CWA_API_KEY": "   "}, None, "key_not_configured", None),
    ("connection-error", None,
     requests.ConnectionError(f"https://{UPSTREAM_HOST}/x?Authorization={SENTINEL_KEY} {UPSTREAM_BODY_MARKER}"),
     "upstream_unreachable", None),
    ("connect-timeout", None, requests.ConnectTimeout(f"https://{UPSTREAM_HOST} timed out"),
     "upstream_unreachable", None),
    ("read-timeout", None, requests.ReadTimeout(f"https://{UPSTREAM_HOST} read timed out"),
     "upstream_unreachable", None),
    ("unexpected-exception", None, RuntimeError(f"{SENTINEL_KEY} {UPSTREAM_HOST}"),
     "upstream_unreachable", None),
    ("http-401", None, FakeResponse(401, f'{{"message":"{UPSTREAM_BODY_MARKER} key {SENTINEL_KEY}"}}'.encode()),
     "upstream_error", 401),
    ("http-403", None, FakeResponse(403, UPSTREAM_BODY_MARKER.encode()), "upstream_error", 403),
    ("http-429", None, FakeResponse(429, UPSTREAM_BODY_MARKER.encode()), "upstream_error", 429),
    ("http-500", None, FakeResponse(500, UPSTREAM_BODY_MARKER.encode()), "upstream_error", 500),
    ("non-json", None, FakeResponse(200, f"<html>{UPSTREAM_BODY_MARKER} {UPSTREAM_HOST}</html>".encode()),
     "invalid_response", None),
    ("invalid-utf8", None, FakeResponse(200, b"\xff\xfe\xfa"), "invalid_response", None),
    ("success-false", None,
     ok({"success": "false", "message": UPSTREAM_BODY_MARKER, "result": {"resource_id": "O-A0001-001"}}),
     "invalid_response", None),
    ("success-boolean", None,
     ok({"success": True, "result": {"resource_id": "O-A0001-001"}, "records": {"Station": []}}),
     "invalid_response", None),
    ("wrong-dataset", None,
     ok({"success": "true", "result": {"resource_id": "F-D0047-091"}, "records": {"Station": []}}),
     "invalid_response", None),
    ("no-records", None, ok({"success": "true", "result": {"resource_id": "O-A0001-001"}}),
     "invalid_response", None),
    ("json-array", None, ok([UPSTREAM_BODY_MARKER]), "invalid_response", None),
    ("zero-valid", None,
     ok({"success": "true", "result": {"resource_id": "O-A0001-001"},
         "records": {"Station": [{"StationId": "X1", "note": UPSTREAM_BODY_MARKER}]}}),
     "invalid_response", None),
]


@pytest.mark.parametrize(
    "env, outcome, reason, upstream_status",
    [c[1:] for c in FAILURE_CASES],
    ids=[c[0] for c in FAILURE_CASES],
)
def test_failure_class_through_the_api(env, outcome, reason, upstream_status, caplog, capfd) -> None:
    caplog.set_level(logging.DEBUG)
    upstream = FakeUpstream(outcome)
    svc = service(upstream, env={"CWA_API_KEY": SENTINEL_KEY} if env is None else env)
    client = create_app(observation_service=svc).test_client()

    response = client.get("/api/observations/latest")

    assert 400 <= response.status_code < 600
    assert response.is_json
    body = response.get_json()
    assert body["reason"] == reason
    assert isinstance(body["error"], str) and body["error"]
    assert body.get("upstreamStatus") == upstream_status
    assert "stations" not in body
    assert response.headers["Cache-Control"] == "no-store"
    out, err = capfd.readouterr()
    for text in (response.get_data(as_text=True), caplog.text, out, err):
        _leak_free(text)
    assert reason in caplog.text  # the reason class is logged, nothing more
    if reason == "key_not_configured":
        assert upstream.calls == []  # no upstream request without a key


def test_four_reasons_are_distinct_and_fixed() -> None:
    assert obs.FAILURE_REASONS == (
        "key_not_configured", "upstream_unreachable", "upstream_error", "invalid_response",
    )
    texts = {obs.ObservationFailure(r).response()[1]["error"] for r in obs.FAILURE_REASONS}
    assert len(texts) == 4
    for reason in obs.FAILURE_REASONS:
        status, _ = obs.ObservationFailure(reason).response()
        assert not 200 <= status < 300


def test_key_is_sent_only_as_the_authorization_header(sample) -> None:
    upstream = FakeUpstream(ok(sample))
    service(upstream).latest()
    call = upstream.calls[0]
    assert call["headers"] == {"Authorization": SENTINEL_KEY}
    assert SENTINEL_KEY not in call["url"]
    assert SENTINEL_KEY not in json.dumps(call["params"])
    assert call["url"] == "https://opendata.cwa.gov.tw/api/v1/rest/datastore/O-A0001-001"


def test_success_response_and_logs_carry_no_key(sample, caplog, capfd) -> None:
    caplog.set_level(logging.DEBUG)
    client = create_app(observation_service=service(FakeUpstream(ok(sample)))).test_client()
    response = client.get("/api/observations/latest")
    assert response.status_code == 200
    assert response.headers["Cache-Control"] == "no-store"
    out, err = capfd.readouterr()
    for text in (response.get_data(as_text=True), caplog.text, out, err):
        assert SENTINEL_KEY not in text
        assert UPSTREAM_HOST not in text


def test_key_is_read_at_request_time_from_the_env_var(sample) -> None:
    env: dict[str, str] = {}
    upstream = FakeUpstream(ok(sample))
    svc = service(upstream, env=env)
    assert svc.latest()[1]["reason"] == "key_not_configured"
    env["CWA_API_KEY"] = SENTINEL_KEY  # set after construction
    assert svc.latest()[0] == 200
    assert not any(SENTINEL_KEY in repr(v) for v in vars(svc).values() if not isinstance(v, dict))


# --- network blocked: real HTTP client, and the forecast path unchanged ------------


@pytest.fixture
def network_blocked(monkeypatch):
    """Block every outbound socket connection and DNS lookup (air-gapped)."""

    def refuse(*args, **kwargs):
        raise OSError("network blocked by test")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)


def test_observation_with_network_blocked_is_upstream_unreachable(
    network_blocked, monkeypatch, caplog, capfd
) -> None:
    """Exercises the real ``requests.get`` path end to end with a sentinel key."""
    caplog.set_level(logging.DEBUG)
    monkeypatch.setenv("CWA_API_KEY", SENTINEL_KEY)
    client = create_app().test_client()  # default service: process env, real client
    response = client.get("/api/observations/latest")
    assert response.status_code == 504
    assert response.get_json()["reason"] == "upstream_unreachable"
    out, err = capfd.readouterr()
    for text in (response.get_data(as_text=True), caplog.text, out, err):
        _leak_free(text)


def test_no_key_in_process_env_is_key_not_configured(monkeypatch) -> None:
    """AC-V2-17(d): an environment without a key → ``key_not_configured``."""
    monkeypatch.delenv("CWA_API_KEY", raising=False)
    client = create_app().test_client()
    response = client.get("/api/observations/latest")
    assert response.status_code == 503
    assert response.get_json()["reason"] == "key_not_configured"


def _forecast_expectations() -> dict[str, tuple[int, object]]:
    """Expected forecast-endpoint answers, computed from the shared module directly."""
    expected: dict[str, tuple[int, object]] = {
        "/api/health": (200, {
            "status": "ok",
            "region_count": len(wq.region_list()),
            "forecast_day_count": len(wq.forecast_days()),
            "ingestion_time": wq.last_ingestion_time(),
        }),
        "/api/regions": (200, {"regions": list(wq.region_list())}),
        "/api/days": (200, {"days": wq.forecast_days()}),
    }
    for region in wq.region_list():
        expected[f"/api/regions/{region}/series"] = (
            200, {"region": region, "series": wq.region_series(region)}
        )
    for day in wq.forecast_days():
        values = [
            {"regionName": v.region_name, "mint": v.mint, "maxt": v.maxt,
             "derivedMapTemperature": v.derived_map_temperature, "colourBand": v.colour_band}
            for v in wq.day_values(day)
        ]
        expected[f"/api/days/{day}"] = (200, {"date": day, "values": values})
    return expected


def test_forecast_endpoints_unchanged_air_gapped_and_keyless(network_blocked, monkeypatch) -> None:
    """INV-V2-1 / INV-V2-4 / AC-V2-16 behaviour check: with sockets blocked and
    no ``CWA_API_KEY``, every forecast endpoint and ``/api/health`` answers 200
    with exactly the shared module's data — also after the observation path failed."""
    monkeypatch.delenv("CWA_API_KEY", raising=False)
    expected = _forecast_expectations()
    json.loads(json.dumps(expected, default=list))  # sanity: serialisable
    client = create_app().test_client()
    assert client.get("/api/observations/latest").get_json()["reason"] == "key_not_configured"
    for path, (status, body) in expected.items():
        response = client.get(path)
        assert response.status_code == status, path
        assert response.get_json() == json.loads(json.dumps(body)), path
    assert set(client.get("/api/health").get_json()) == {
        "status", "region_count", "forecast_day_count", "ingestion_time"
    }  # observation state is not merged into health (R-V2-DEG-5)


def test_health_stays_200_while_the_observation_upstream_fails(network_blocked, monkeypatch) -> None:
    monkeypatch.setenv("CWA_API_KEY", SENTINEL_KEY)
    client = create_app().test_client()
    assert client.get("/api/observations/latest").status_code == 504
    assert client.get("/api/health").status_code == 200


# --- local .env loading (R-V2-SEC-3(b)) ---------------------------------------------


def test_load_local_env_reads_only_the_key(tmp_path, capfd) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(f"# comment\nOTHER=1\nCWA_API_KEY={SENTINEL_KEY}\n", encoding="utf-8")
    environ: dict[str, str] = {}
    assert obs.load_local_env(env_file, environ) is True
    assert environ == {"CWA_API_KEY": SENTINEL_KEY}
    out, err = capfd.readouterr()
    assert SENTINEL_KEY not in out + err


def test_load_local_env_does_not_override_and_tolerates_absence(tmp_path) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text("CWA_API_KEY=from-file\n", encoding="utf-8")
    environ = {"CWA_API_KEY": "already-set"}
    assert obs.load_local_env(env_file, environ) is False
    assert environ["CWA_API_KEY"] == "already-set"
    assert obs.load_local_env(tmp_path / "missing.env", {}) is False
    empty: dict[str, str] = {}
    (tmp_path / "blank.env").write_text("CWA_API_KEY=\n", encoding="utf-8")
    assert obs.load_local_env(tmp_path / "blank.env", empty) is False and empty == {}


# --- value parsing -------------------------------------------------------------------


@pytest.mark.parametrize(
    "value, expected",
    [("25.5", 25.5), ("82", 82), ("259.0", 259.0), ("0.0", 0.0), ("-3.2", -3.2),
     ("-99", None), ("-99.0", None), ("-98", None), ("990", None), ("990.0", None),
     ("X", None), ("T", None), ("", None), ("  ", None), ("abc", None), ("NaN", None),
     ("Infinity", None), (None, None), (True, None), (25.5, 25.5), (-99, None), ([], None)],
)
def test_parse_published_number(value, expected) -> None:
    result = obs.parse_published_number(value)
    assert result == expected
    if expected is not None:
        assert type(result) is type(expected)


def test_county_set_is_v1_members_plus_three_islands() -> None:
    from ingestion.config import REGION_MEMBERS

    members = {c for counties in REGION_MEMBERS.values() for c in counties}
    assert len(members) == 19
    assert obs.COUNTIES == members | {"澎湖縣", "金門縣", "連江縣"}
