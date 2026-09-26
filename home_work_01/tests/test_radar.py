"""Radar path (SPEC-V2 §2.7; Issue #40): ``GET /api/radar/latest`` and ``radar.py``.

Offline (R-TC-5, R-V2-TC-3): the CWA upstream is simulated from the committed
sanitised metadata sample (``tests/fixtures/O-A0058-006_metadata_sample.json``,
captured once under A-3) and a synthetic PNG header of the product's dimension —
the radar image itself is not committed (R-V2-TC-2: the alignment oracle is
geometric). A sentinel key must never appear in a response, a log or stdout /
stderr (H-1, R-V2-SEC-7).

Covers AC-V2-18 (API: image content-type, radar time, reuse ≤ 5 min), AC-V2-07 for
the radar path (four failure classes, non-secret), AC-V2-09(c) API side (radar and
observation fail independently; ``/api/health`` and the forecast endpoints are
unchanged), AC-V2-17(a) (sample carries no key) and the product checks the
alignment relies on (extent, dimension, host).
"""

from __future__ import annotations

import copy
import json
import logging
import socket
import struct
import threading
import time
import zlib
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests

import observation as obs
import radar
from server import create_app

META_PATH = Path(__file__).parent / "fixtures" / "O-A0058-006_metadata_sample.json"
SAMPLE_OBS_PATH = Path(__file__).parent / "fixtures" / "O-A0001-001_sample.json"
SENTINEL_KEY = "SENTINEL-KEY-radar-40-must-never-leak"
UPSTREAM_BODY_MARKER = "UPSTREAM-BODY-MARKER-radar-40"
UPSTREAM_HOSTS = ("opendata.cwa.gov.tw", "cwaopendata.s3.ap-northeast-1.amazonaws.com")
SAMPLE_RADAR_TIME = "2026-09-26T14:40:00+08:00"
TAIPEI = timezone(timedelta(hours=8))


def png(width: int = 3600, height: int = 3600) -> bytes:
    """A valid, fully transparent RGBA PNG of the given size."""
    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))
    row = b"\x00" * (1 + 4 * width)  # filter byte + transparent pixels
    packer = zlib.compressobj(9)
    idat = b"".join(packer.compress(row) for _ in range(height)) + packer.flush()
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", idat) + chunk(b"IEND", b""))


IMAGE = png()


@pytest.fixture
def meta() -> dict:
    return json.loads(META_PATH.read_text(encoding="utf-8"))


class FakeResponse:
    def __init__(self, status: int, content: bytes = b""):
        self.status_code = status
        self.content = content
        self.closed = False

    def iter_content(self, chunk_size=65536):
        for i in range(0, len(self.content), chunk_size):
            yield self.content[i:i + chunk_size]

    def close(self) -> None:
        self.closed = True


class FakeUpstream:
    """``requests.get`` stand-in: the metadata request (fileapi) and the image
    request (the product URL) each answer from their own outcome."""

    def __init__(self, metadata, image=None):
        self.metadata = metadata
        self.image = image if image is not None else FakeResponse(200, IMAGE)
        self.calls: list[dict] = []

    def __call__(self, url, headers=None, params=None, timeout=None, stream=False):
        self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
        outcome = self.metadata if "/fileapi/" in url else self.image
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def ok_meta(payload) -> FakeResponse:
    return FakeResponse(200, json.dumps(payload, ensure_ascii=False).encode("utf-8"))


class Clock:
    def __init__(self, start: datetime | None = None):
        self.now = start or datetime(2026, 9, 26, 14, 45, 0, tzinfo=TAIPEI)

    def __call__(self) -> datetime:
        return self.now


def service(upstream, *, env=None, clock=None, **kw) -> radar.RadarService:
    return radar.RadarService(
        env={"CWA_API_KEY": SENTINEL_KEY} if env is None else env,
        clock=clock or Clock(), http_get=upstream, **kw)


# --- the committed sample and the product checks (R-V2-RAD-1, RAD-5) ------------------


def test_sample_is_the_transparent_near_taiwan_product(meta) -> None:
    parsed = radar.parse_metadata(meta)
    assert parsed.radar_time == SAMPLE_RADAR_TIME
    assert parsed.product_url.startswith("https://cwaopendata.s3.ap-northeast-1.amazonaws.com/")
    info = meta["cwaopendata"]["dataset"]
    assert meta["cwaopendata"]["dataid"] == radar.DATASET_ID == "O-A0058-006"
    assert info["resource"]["resourceDesc"] == radar.DATASET_NAME
    assert info["datasetInfo"]["parameterSet"]["LongitudeRange"] == "118.0-124.0"
    assert info["datasetInfo"]["parameterSet"]["LatitudeRange"] == "20.5-26.5"
    assert info["datasetInfo"]["parameterSet"]["ImageDimension"] == "3600x3600"


def test_extent_and_size_are_the_spec_product_range() -> None:
    assert radar.EXTENT == {"west": 118.0, "east": 124.0, "south": 20.5, "north": 26.5}
    assert radar.IMAGE_SIZE == (3600, 3600)


def _mutated(meta, path, value):
    data = copy.deepcopy(meta)
    node = data
    for key in path[:-1]:
        node = node[key]
    if value is KeyError:
        del node[path[-1]]
    else:
        node[path[-1]] = value
    return data


DS = ("cwaopendata", "dataset")
PS = DS + ("datasetInfo", "parameterSet")
BAD_METADATA = [
    ("wrong-dataset", ("cwaopendata", "dataid"), "O-A0058-005"),
    ("no-datetime", DS + ("DateTime",), KeyError),
    ("bad-datetime", DS + ("DateTime",), "not-a-time"),
    ("date-only", DS + ("DateTime",), "2026-09-26"),
    ("larger-range-lon", PS + ("LongitudeRange",), "115.00-126.50"),
    ("larger-range-lat", PS + ("LatitudeRange",), "17.75-29.25"),
    ("shifted-lat", PS + ("LatitudeRange",), "20.6-26.6"),
    ("no-lon-range", PS + ("LongitudeRange",), KeyError),
    ("other-dimension", PS + ("ImageDimension",), "1800x1800"),
    ("not-png", DS + ("resource", "mimeType"), "image/jpeg"),
    ("http-url", DS + ("resource", "ProductURL"),
     "http://cwaopendata.s3.ap-northeast-1.amazonaws.com/Observation/O-A0058-006.png"),
    ("other-host", DS + ("resource", "ProductURL"), "https://example.test/O-A0058-006.png"),
    ("lookalike-host", DS + ("resource", "ProductURL"),
     "https://cwaopendata.s3.ap-northeast-1.amazonaws.com.example.test/x.png"),
    ("userinfo", DS + ("resource", "ProductURL"),
     "https://user:pw@cwaopendata.s3.ap-northeast-1.amazonaws.com/x.png"),
    ("other-port", DS + ("resource", "ProductURL"),
     "https://cwaopendata.s3.ap-northeast-1.amazonaws.com:8443/x.png"),
    ("no-url", DS + ("resource", "ProductURL"), KeyError),
    ("url-not-text", DS + ("resource", "ProductURL"), 42),
]


@pytest.mark.parametrize("path, value", [c[1:] for c in BAD_METADATA], ids=[c[0] for c in BAD_METADATA])
def test_unexpected_metadata_is_invalid_response(meta, path, value) -> None:
    with pytest.raises(radar.RadarFailure) as caught:
        radar.parse_metadata(_mutated(meta, path, value))
    assert caught.value.reason == "invalid_response"


@pytest.mark.parametrize("payload", [None, [], "text", {"cwaopendata": []}, {"cwaopendata": {"dataid": "O-A0058-006"}}])
def test_metadata_of_the_wrong_shape_is_invalid_response(payload) -> None:
    with pytest.raises(radar.RadarFailure) as caught:
        radar.parse_metadata(payload)
    assert caught.value.reason == "invalid_response"


def test_equivalent_range_spellings_are_accepted(meta) -> None:
    data = _mutated(meta, PS + ("LongitudeRange",), " 118.00 - 124.00 ")
    data = _mutated(data, PS + ("ImageDimension",), "3600 x 3600")
    assert radar.parse_metadata(data).radar_time == SAMPLE_RADAR_TIME


@pytest.mark.parametrize(
    "data",
    [b"", b"GIF89a" + b"\x00" * 40, png(1800, 1800), png(3600, 3599), IMAGE[:20],
     b"\x89PNG\r\n\x1a\n" + b"\x00" * 30],
    ids=["empty", "gif", "half-size", "one-row-short", "truncated", "no-ihdr"],
)
def test_image_that_is_not_the_product_grid_is_invalid(data) -> None:
    with pytest.raises(radar.RadarFailure) as caught:
        radar.check_image(data)
    assert caught.value.reason == "invalid_response"


def test_image_over_the_size_limit_is_invalid() -> None:
    big = IMAGE + b"\x00" * (radar.MAX_IMAGE_BYTES - len(IMAGE) + 1)
    with pytest.raises(radar.RadarFailure):
        radar.check_image(big)
    radar.check_image(IMAGE)  # the real-size grid passes


# --- success through the API (AC-V2-18 API side) ---------------------------------------


def test_success_is_the_png_with_the_radar_time_of_the_same_fetch(meta, caplog, capfd) -> None:
    caplog.set_level(logging.DEBUG)
    clock = Clock(datetime(2026, 9, 26, 6, 45, 7, tzinfo=timezone.utc))
    upstream = FakeUpstream(ok_meta(meta))
    client = create_app(radar_service=service(upstream, clock=clock)).test_client()

    response = client.get("/api/radar/latest")

    assert response.status_code == 200
    assert response.mimetype == "image/png"
    assert response.get_data() == IMAGE
    assert response.headers["X-Radar-Time"] == SAMPLE_RADAR_TIME
    assert response.headers["X-Radar-Fetched-Time"] == "2026-09-26T14:45:07+08:00"
    assert response.headers["X-Radar-Dataset"] == "O-A0058-006"
    assert response.headers["Cache-Control"] == "no-store"
    out, err = capfd.readouterr()
    for text in (str(response.headers), caplog.text, out, err):
        assert SENTINEL_KEY not in text
        for host in UPSTREAM_HOSTS:
            assert host not in text
    assert not [r for r in caplog.records if r.name.startswith("urllib3")]


def test_key_goes_only_to_the_metadata_request_as_a_header(meta) -> None:
    upstream = FakeUpstream(ok_meta(meta))
    assert service(upstream).latest().status == 200
    metadata_call, image_call = upstream.calls
    assert metadata_call["url"] == "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/O-A0058-006"
    assert metadata_call["headers"] == {"Authorization": SENTINEL_KEY}
    assert SENTINEL_KEY not in json.dumps(metadata_call["params"])
    # the image host is a third party: it never sees the key, in any part
    assert image_call["url"] == meta["cwaopendata"]["dataset"]["resource"]["ProductURL"]
    assert image_call["headers"] == {}
    assert SENTINEL_KEY not in json.dumps(image_call)


def test_timeouts_are_passed_to_both_requests(meta) -> None:
    upstream = FakeUpstream(ok_meta(meta))
    service(upstream).latest()
    for call in upstream.calls:
        assert call["timeout"] == (radar.CONNECT_TIMEOUT_SECONDS, radar.READ_TIMEOUT_SECONDS)


def test_radar_time_is_returned_exactly_as_published(meta) -> None:
    data = _mutated(meta, DS + ("DateTime",), "2026-09-26T14:50:00+08:00")
    result = service(FakeUpstream(ok_meta(data))).latest()
    assert result.radar_time == "2026-09-26T14:50:00+08:00"


# --- reuse window ≤ 5 minutes (R-V2-RAD-2, DV-5) ----------------------------------------


def test_reuse_window_is_within_the_contract_ceiling() -> None:
    assert 0 <= radar.REUSE_WINDOW_SECONDS <= radar.REUSE_WINDOW_CEILING_SECONDS == 300
    with pytest.raises(ValueError):
        radar.RadarService(env={}, reuse_window_seconds=301)
    radar.RadarService(env={}, reuse_window_seconds=300)


def test_reuse_window_returns_the_same_image_and_times_then_refetches(meta) -> None:
    clock = Clock()
    upstream = FakeUpstream(ok_meta(meta))
    svc = service(upstream, clock=clock)
    first = svc.latest()
    clock.now += timedelta(seconds=radar.REUSE_WINDOW_SECONDS - 1)
    second = svc.latest()
    assert second is first  # same image, radar time and fetched time
    assert len(upstream.calls) == 2  # metadata + image, once
    clock.now += timedelta(seconds=1)
    upstream.metadata = ok_meta(_mutated(meta, DS + ("DateTime",), "2026-09-26T14:50:00+08:00"))
    third = svc.latest()
    assert len(upstream.calls) == 4
    assert third.radar_time == "2026-09-26T14:50:00+08:00"
    assert third.fetched_time != first.fetched_time


def test_zero_window_always_refetches(meta) -> None:
    upstream = FakeUpstream(ok_meta(meta))
    svc = service(upstream, reuse_window_seconds=0)
    svc.latest()
    svc.latest()
    assert len(upstream.calls) == 4


def test_failures_are_never_reused_and_never_answered_with_an_old_image(meta) -> None:
    clock = Clock()
    upstream = FakeUpstream(ok_meta(meta))
    svc = service(upstream, clock=clock)
    assert svc.latest().status == 200
    clock.now += timedelta(seconds=radar.REUSE_WINDOW_SECONDS)
    upstream.metadata = FakeResponse(500, UPSTREAM_BODY_MARKER.encode())
    failed = svc.latest()
    assert failed.status == 502 and failed.image is None and failed.body["reason"] == "upstream_error"
    upstream.metadata = ok_meta(meta)
    assert svc.latest().status == 200  # the failure was not cached


def test_clock_moving_backwards_does_not_extend_reuse(meta) -> None:
    clock = Clock()
    upstream = FakeUpstream(ok_meta(meta))
    svc = service(upstream, clock=clock)
    svc.latest()
    clock.now -= timedelta(seconds=5)
    svc.latest()
    assert len(upstream.calls) == 4


def test_default_bounds_are_below_the_platform_limit() -> None:
    assert radar.UPSTREAM_DEADLINE_SECONDS < 10
    assert radar.CONNECT_TIMEOUT_SECONDS <= radar.UPSTREAM_DEADLINE_SECONDS
    assert radar.READ_TIMEOUT_SECONDS <= radar.UPSTREAM_DEADLINE_SECONDS


# --- AC-V2-07, radar path: four failure classes, nothing secret out --------------------


def _leak_free(text: str) -> None:
    assert SENTINEL_KEY not in text
    for host in UPSTREAM_HOSTS:
        assert host not in text
    assert UPSTREAM_BODY_MARKER not in text
    assert "Authorization" not in text
    assert "ProductURL" not in text


def _meta_case(mutate):
    def build(meta):
        return ok_meta(mutate(meta))
    return build


FAILURE_CASES = [
    # (id, env, metadata outcome, image outcome, reason, upstream status)
    ("no-key", {}, None, None, "key_not_configured", None),
    ("blank-key", {"CWA_API_KEY": " "}, None, None, "key_not_configured", None),
    ("metadata-connection-error", None,
     requests.ConnectionError(f"https://{UPSTREAM_HOSTS[0]}/fileapi?Authorization={SENTINEL_KEY} {UPSTREAM_BODY_MARKER}"),
     None, "upstream_unreachable", None),
    ("metadata-read-timeout", None, requests.ReadTimeout(f"https://{UPSTREAM_HOSTS[0]} timed out"),
     None, "upstream_unreachable", None),
    ("metadata-unexpected-exception", None, RuntimeError(f"{SENTINEL_KEY} {UPSTREAM_HOSTS[0]}"),
     None, "upstream_unreachable", None),
    ("image-connection-error", None, "ok",
     requests.ConnectionError(f"https://{UPSTREAM_HOSTS[1]}/Observation/x.png {UPSTREAM_BODY_MARKER}"),
     "upstream_unreachable", None),
    ("metadata-401", None, FakeResponse(401, f'{{"message":"{UPSTREAM_BODY_MARKER} {SENTINEL_KEY}"}}'.encode()),
     None, "upstream_error", 401),
    ("metadata-403", None, FakeResponse(403, UPSTREAM_BODY_MARKER.encode()), None, "upstream_error", 403),
    ("metadata-429", None, FakeResponse(429, UPSTREAM_BODY_MARKER.encode()), None, "upstream_error", 429),
    ("metadata-500", None, FakeResponse(500, UPSTREAM_BODY_MARKER.encode()), None, "upstream_error", 500),
    ("image-403", None, "ok", FakeResponse(403, f"<Error>{UPSTREAM_BODY_MARKER}</Error>".encode()),
     "upstream_error", 403),
    ("image-500", None, "ok", FakeResponse(500, UPSTREAM_BODY_MARKER.encode()), "upstream_error", 500),
    ("metadata-non-json", None, FakeResponse(200, f"<html>{UPSTREAM_BODY_MARKER} {UPSTREAM_HOSTS[0]}</html>".encode()),
     None, "invalid_response", None),
    ("metadata-invalid-utf8", None, FakeResponse(200, b"\xff\xfe\xfa"), None, "invalid_response", None),
    ("metadata-json-array", None, ok_meta([UPSTREAM_BODY_MARKER]), None, "invalid_response", None),
    ("metadata-other-product", None, "larger-range", None, "invalid_response", None),
    ("image-not-png", None, "ok", FakeResponse(200, f"<html>{UPSTREAM_BODY_MARKER}</html>".encode()),
     "invalid_response", None),
    ("image-wrong-size", None, "ok", FakeResponse(200, png(1800, 1800)), "invalid_response", None),
]


@pytest.mark.parametrize(
    "env, metadata, image, reason, upstream_status",
    [c[1:] for c in FAILURE_CASES],
    ids=[c[0] for c in FAILURE_CASES],
)
def test_failure_class_through_the_api(meta, env, metadata, image, reason, upstream_status, caplog, capfd) -> None:
    caplog.set_level(logging.DEBUG)
    if metadata == "ok":
        metadata = ok_meta(meta)
    elif metadata == "larger-range":
        metadata = ok_meta(_mutated(meta, PS + ("LongitudeRange",), "115.00-126.50"))
    upstream = FakeUpstream(metadata, image)
    svc = service(upstream, env={"CWA_API_KEY": SENTINEL_KEY} if env is None else env)
    client = create_app(radar_service=svc).test_client()

    response = client.get("/api/radar/latest")

    assert 400 <= response.status_code < 600
    assert response.is_json
    body = response.get_json()
    assert body["reason"] == reason
    assert body["dataset"] == "O-A0058-006"
    assert isinstance(body["error"], str) and body["error"].startswith("Radar is unavailable")
    assert body.get("upstreamStatus") == upstream_status
    assert "X-Radar-Time" not in response.headers
    assert response.headers["Cache-Control"] == "no-store"
    out, err = capfd.readouterr()
    for text in (response.get_data(as_text=True), str(response.headers), caplog.text, out, err):
        _leak_free(text)
    assert reason in caplog.text  # the reason class is logged, nothing more
    if reason == "key_not_configured":
        assert upstream.calls == []  # no upstream request without a key


def test_four_reasons_are_the_observation_codes_with_distinct_fixed_texts() -> None:
    assert radar.FAILURE_REASONS == obs.FAILURE_REASONS
    texts = {radar.RadarFailure(r).body()[1]["error"] for r in radar.FAILURE_REASONS}
    assert len(texts) == 4
    for reason in radar.FAILURE_REASONS:
        status, _ = radar.RadarFailure(reason).body()
        assert not 200 <= status < 300


class _LoopbackServer:
    """Accepts and then stalls, or drips one byte at a time (never finishes)."""

    def __init__(self, mode: str):
        self.mode = mode
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1", 0))
        self.sock.listen(5)
        self.sock.settimeout(0.2)
        self.stop = threading.Event()
        self.conns: list[socket.socket] = []
        threading.Thread(target=self._serve, daemon=True).start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.sock.getsockname()[1]}/fileapi/stall"

    def _serve(self) -> None:
        while not self.stop.is_set():
            try:
                conn, _ = self.sock.accept()
            except OSError:
                continue
            self.conns.append(conn)
            if self.mode == "drip":
                threading.Thread(target=self._drip, args=(conn,), daemon=True).start()

    def _drip(self, conn: socket.socket) -> None:
        try:
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 100000\r\n\r\n{")
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
    """Bounded time on the radar path (R-V2-OBS-13 applied): a stalled or dripping
    upstream yields ``upstream_unreachable`` within the deadline, real client."""
    server = _LoopbackServer(mode)
    try:
        svc = radar.RadarService(env={"CWA_API_KEY": SENTINEL_KEY}, metadata_url=server.url,
                                 connect_timeout=1.0, read_timeout=5.0, deadline=0.6)
        started = time.monotonic()
        result = svc.latest()
        elapsed = time.monotonic() - started
    finally:
        server.close()
    assert result.status == 504 and result.body["reason"] == "upstream_unreachable"
    assert elapsed < 3.0


@pytest.fixture
def network_blocked(monkeypatch):
    def refuse(*args, **kwargs):
        raise OSError("network blocked by test")

    monkeypatch.setattr(socket.socket, "connect", refuse)
    monkeypatch.setattr(socket.socket, "connect_ex", refuse)
    monkeypatch.setattr(socket, "create_connection", refuse)
    monkeypatch.setattr(socket, "getaddrinfo", refuse)


def test_radar_with_network_blocked_is_upstream_unreachable(network_blocked, monkeypatch, caplog, capfd) -> None:
    """The real ``requests.get`` path end to end with a sentinel key."""
    caplog.set_level(logging.DEBUG)
    monkeypatch.setenv("CWA_API_KEY", SENTINEL_KEY)
    response = create_app().test_client().get("/api/radar/latest")
    assert response.status_code == 504
    assert response.get_json()["reason"] == "upstream_unreachable"
    out, err = capfd.readouterr()
    for text in (response.get_data(as_text=True), caplog.text, out, err):
        _leak_free(text)


def test_no_key_in_process_env_is_key_not_configured(monkeypatch) -> None:
    monkeypatch.delenv("CWA_API_KEY", raising=False)
    response = create_app().test_client().get("/api/radar/latest")
    assert response.status_code == 503
    assert response.get_json()["reason"] == "key_not_configured"


def test_key_is_read_at_request_time_and_never_stored(meta) -> None:
    env: dict[str, str] = {}
    svc = service(FakeUpstream(ok_meta(meta)), env=env)
    assert svc.latest().body["reason"] == "key_not_configured"
    env["CWA_API_KEY"] = SENTINEL_KEY
    assert svc.latest().status == 200
    assert not any(SENTINEL_KEY in repr(v) for v in vars(svc).values() if not isinstance(v, dict))


# --- AC-V2-09(c) API side: radar and the other paths fail independently ----------------


class _ObsUpstream:
    def __init__(self):
        self.fail = False
        self.sample = SAMPLE_OBS_PATH.read_bytes()

    def __call__(self, url, headers=None, params=None, timeout=None):
        if self.fail:
            raise requests.ConnectionError("down")

        class _R:
            status_code = 200
            content = self.sample

            def close(self):
                pass
        return _R()


def test_radar_failure_leaves_observation_and_forecast_answers_unchanged(meta) -> None:
    obs_up = _ObsUpstream()
    radar_up = FakeUpstream(FakeResponse(500, b"x"))
    client = create_app(
        observation_service=obs.LatestObservationService(env={"CWA_API_KEY": SENTINEL_KEY}, http_get=obs_up,
                                                         reuse_window_seconds=0),
        radar_service=service(radar_up, reuse_window_seconds=0),
    ).test_client()
    before = client.get("/api/observations/latest").get_json()
    health_before = client.get("/api/health")
    assert client.get("/api/radar/latest").status_code == 502
    after = client.get("/api/observations/latest")
    assert after.status_code == 200
    assert after.get_json()["stations"] == before["stations"]
    health_after = client.get("/api/health")
    assert (health_after.status_code, health_after.get_json()) == (health_before.status_code, health_before.get_json())
    assert set(health_after.get_json()) == {"status", "region_count", "forecast_day_count", "ingestion_time"}


def test_observation_failure_leaves_radar_working(meta) -> None:
    obs_up = _ObsUpstream()
    obs_up.fail = True
    client = create_app(
        observation_service=obs.LatestObservationService(env={"CWA_API_KEY": SENTINEL_KEY}, http_get=obs_up),
        radar_service=service(FakeUpstream(ok_meta(meta))),
    ).test_client()
    assert client.get("/api/observations/latest").status_code == 504
    response = client.get("/api/radar/latest")
    assert response.status_code == 200 and response.mimetype == "image/png"
    assert response.headers["X-Radar-Time"] == SAMPLE_RADAR_TIME


def test_forecast_endpoints_answer_while_the_radar_path_is_air_gapped(network_blocked, monkeypatch) -> None:
    """INV-V2-1 / INV-V2-4: after a failed radar request (sockets blocked, no key),
    ``/api/health`` and the forecast endpoints still answer 200."""
    monkeypatch.delenv("CWA_API_KEY", raising=False)
    client = create_app().test_client()
    assert client.get("/api/radar/latest").get_json()["reason"] == "key_not_configured"
    for path in ("/api/health", "/api/regions", "/api/days"):
        assert client.get(path).status_code == 200, path


# --- the committed sample carries no secret (AC-V2-17(a)) ------------------------------


def test_metadata_sample_has_no_secret() -> None:
    from ingestion.checks import scan_file

    assert scan_file(META_PATH) == []
    text = META_PATH.read_text(encoding="utf-8")
    assert "Authorization" not in text and "CWA_API_KEY" not in text
