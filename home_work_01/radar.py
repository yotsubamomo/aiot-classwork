"""Radar echo — server-side path for the Now mode's Radar overlay (SPEC-V2 §2.7).

This module is the deployed Dashboard backend's access to CWA for the radar path
(R-V2-SEC-2(a), R-V2-RAD-2; Issue #40). For ``GET /api/radar/latest`` it fetches,
in one server-side operation, the latest CWA **O-A0058-006** product
(雷達整合回波圖-臺灣(鄰近地區)_透明底圖: the composite radar echo of Taiwan's
surroundings on a transparent background, a PNG 3600×3600 over lon 118.0–124.0 /
lat 20.5–26.5): first the product metadata (it needs the maintainer's key, so it
is fetched here and nowhere else), then the image the metadata points to. The
browser receives the image bytes and the product time of that same fetch, and
never the key, the upstream URLs or the upstream metadata (R-V2-SEC-1, OBS-12).

Data flow::

    request ─▶ RadarService.latest()
                 ├─ key from the process env var ``CWA_API_KEY`` (R-V2-SEC-3)
                 ├─ reuse a recent success (≤ REUSE_WINDOW_SECONDS, R-V2-RAD-2)
                 └─ fetch_product()  — metadata, then image; both within
                                        UPSTREAM_DEADLINE_SECONDS (R-V2-OBS-13)
               ◀─ RadarResult: the PNG + its radar time, or a classified failure

Contract points implemented here (Executor HOW choices are documented in the
README section "Radar overlay"):

* **Product** (R-V2-RAD-1): the metadata must name ``O-A0058-006``, a parseable
  ``DateTime`` (the radar product time, returned exactly as published), the
  extent lon 118.0–124.0 / lat 20.5–26.5 and the dimension 3600×3600 the frontend
  aligns the image with (R-V2-RAD-5), and an ``https`` product URL on CWA's open
  data host. The image must be a PNG of that dimension. Anything else is
  ``invalid_response`` — the page never places an image whose geometry is unknown.
* **Four failure reasons** (R-V2-OBS-11 applied to radar, DV-6): the same four
  codes as the observation path, each a non-2xx JSON with a fixed ``error`` text.
  The server never returns stale data; "stale" is the page's state.
* **No secrets out** (R-V2-OBS-12, SEC-7, H-1): the key is sent only in the
  ``Authorization`` header of the metadata request and never to the image host;
  failure texts are constants; logs carry only the reason, the numeric upstream
  status and the radar time — never the key, headers, URLs, bodies or exception
  messages.

The module holds no SQL and does not touch ``data.db``; the forecast path does not
import it (INV-V2-1).
"""

from __future__ import annotations

import json
import logging
import os
import re
import struct
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Callable, Mapping
from urllib.parse import urlsplit

import requests

from observation import (
    ENV_KEY_NAME,
    INVALID_RESPONSE,
    KEY_NOT_CONFIGURED,
    TAIPEI,
    UPSTREAM_ERROR,
    UPSTREAM_UNREACHABLE,
    parse_obs_time,
)

logger = logging.getLogger(__name__)

# R-V2-SEC-7: the HTTP client's own logger would record the upstream host and
# request line; hold it at ERROR (observation.py does the same).
logging.getLogger("urllib3").setLevel(logging.ERROR)

# --- product (R-V2-RAD-1; the variant is HOW) --------------------------------------

DATASET_ID = "O-A0058-006"
DATASET_NAME = "雷達整合回波圖-臺灣(鄰近地區)_透明底圖"
_METADATA_URL = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/" + DATASET_ID
_METADATA_PARAMS = {"downloadType": "WEB", "format": "JSON"}
# The image is served from CWA's public open-data bucket. Only this host is
# fetched (the metadata cannot redirect the server anywhere else), and the key is
# never sent to it.
IMAGE_HOSTS: frozenset[str] = frozenset({"cwaopendata.s3.ap-northeast-1.amazonaws.com"})

# The product geometry the frontend aligns the image with (app.js RADAR_EXTENT,
# kept equal by a static test): an equirectangular 3600×3600 image whose edges are
# these meridians / parallels.
EXTENT = {"west": 118.0, "east": 124.0, "south": 20.5, "north": 26.5}
IMAGE_SIZE = (3600, 3600)

# The deployed function's response limit is 4.5 MB; the product is ~0.1 MB.
MAX_IMAGE_BYTES = 4_000_000

# --- Executor HOW choices (documented in the README) ----------------------------

# Upstream bound (R-V2-OBS-13 applied to radar): metadata + image together.
CONNECT_TIMEOUT_SECONDS = 3.0
READ_TIMEOUT_SECONDS = 5.0
UPSTREAM_DEADLINE_SECONDS = 8.0

# Reuse window (R-V2-RAD-2, DV-5): contract ceiling 5 minutes. Only successes.
REUSE_WINDOW_SECONDS = 120
REUSE_WINDOW_CEILING_SECONDS = 300

# --- failure classification (same four reasons as the observation path) ----------

_FAILURES: dict[str, tuple[int, str]] = {
    KEY_NOT_CONFIGURED: (
        503,
        "Radar is unavailable: the server has no CWA API key configured.",
    ),
    UPSTREAM_UNREACHABLE: (
        504,
        "Radar is unavailable: the CWA service could not be reached in time.",
    ),
    UPSTREAM_ERROR: (
        502,
        "Radar is unavailable: the CWA service returned an error status.",
    ),
    INVALID_RESPONSE: (
        502,
        "Radar is unavailable: the CWA radar product was not usable "
        "(unreadable metadata, an unexpected product or not the expected image).",
    ),
}
FAILURE_REASONS: tuple[str, ...] = tuple(_FAILURES)


class RadarFailure(Exception):
    """A classified failure of the radar path: a reason code and, for
    ``upstream_error``, the numeric upstream status — nothing else, so nothing
    secret can travel with it."""

    def __init__(self, reason: str, upstream_status: int | None = None):
        if reason not in _FAILURES:
            raise ValueError(f"unknown failure reason {reason!r}")
        super().__init__(reason)
        self.reason = reason
        self.upstream_status = upstream_status

    def body(self) -> tuple[int, dict[str, Any]]:
        """Return ``(HTTP status, JSON body)`` for this failure."""
        status, text = _FAILURES[self.reason]
        body: dict[str, Any] = {"dataset": DATASET_ID, "reason": self.reason, "error": text}
        if self.reason == UPSTREAM_ERROR and self.upstream_status is not None:
            body["upstreamStatus"] = self.upstream_status
        return status, body


@dataclass(frozen=True)
class RadarResult:
    """What ``/api/radar/latest`` answers: a success (``image`` set) or a failure
    (``body`` set, a non-2xx JSON)."""

    status: int
    image: bytes | None = None
    radar_time: str | None = None  # metadata DateTime, as published
    fetched_time: str | None = None  # server clock, +08:00, seconds
    body: dict[str, Any] | None = None


# --- metadata (fileapi JSON) ---------------------------------------------------------

_RANGE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*-\s*(-?\d+(?:\.\d+)?)\s*$")
_DIMENSION = re.compile(r"^\s*(\d+)\s*[xX×]\s*(\d+)\s*$")


def _range(value: Any) -> tuple[float, float] | None:
    match = _RANGE.match(value) if isinstance(value, str) else None
    return (float(match.group(1)), float(match.group(2))) if match else None


def _same(a: float, b: float) -> bool:
    return abs(a - b) < 1e-9


@dataclass(frozen=True)
class RadarMetadata:
    radar_time: str
    product_url: str


def parse_metadata(payload: Any) -> RadarMetadata:
    """Validate the fileapi metadata and return the product time and image URL.

    Raises ``RadarFailure(invalid_response)`` unless the payload names this
    dataset, a parseable ``DateTime``, exactly the expected extent and dimension,
    a PNG resource and an ``https`` URL on an allowed image host.
    """
    try:
        root = payload["cwaopendata"]
        if root.get("dataid") != DATASET_ID:
            raise RadarFailure(INVALID_RESPONSE)
        dataset = root["dataset"]
        radar_time = dataset["DateTime"]
        parameters = dataset["datasetInfo"]["parameterSet"]
        resource = dataset["resource"]
        product_url = resource["ProductURL"]
        mime_type = resource.get("mimeType")
    except (KeyError, TypeError, AttributeError):
        raise RadarFailure(INVALID_RESPONSE) from None

    if not isinstance(radar_time, str) or parse_obs_time(radar_time) is None:
        raise RadarFailure(INVALID_RESPONSE)
    lon = _range(parameters.get("LongitudeRange")) if isinstance(parameters, dict) else None
    lat = _range(parameters.get("LatitudeRange")) if isinstance(parameters, dict) else None
    size = parameters.get("ImageDimension") if isinstance(parameters, dict) else None
    size_match = _DIMENSION.match(size) if isinstance(size, str) else None
    if (
        lon is None or lat is None or size_match is None
        or not (_same(lon[0], EXTENT["west"]) and _same(lon[1], EXTENT["east"]))
        or not (_same(lat[0], EXTENT["south"]) and _same(lat[1], EXTENT["north"]))
        or (int(size_match.group(1)), int(size_match.group(2))) != IMAGE_SIZE
    ):
        raise RadarFailure(INVALID_RESPONSE)
    if mime_type is not None and mime_type != "image/png":
        raise RadarFailure(INVALID_RESPONSE)
    if not isinstance(product_url, str):
        raise RadarFailure(INVALID_RESPONSE)
    parts = urlsplit(product_url.strip())
    if (
        parts.scheme != "https"
        or parts.hostname not in IMAGE_HOSTS
        or parts.username or parts.password or parts.port not in (None, 443)
    ):
        raise RadarFailure(INVALID_RESPONSE)
    return RadarMetadata(radar_time=radar_time, product_url=product_url.strip())


# --- image ----------------------------------------------------------------------------

_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def png_size(data: bytes) -> tuple[int, int] | None:
    """Return a PNG's ``(width, height)`` from its IHDR chunk, or ``None``."""
    if len(data) < 24 or not data.startswith(_PNG_SIGNATURE) or data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def check_image(data: bytes) -> None:
    """Raise ``RadarFailure(invalid_response)`` unless ``data`` is a PNG of the
    product's dimension within the size limit."""
    if not data or len(data) > MAX_IMAGE_BYTES or png_size(data) != IMAGE_SIZE:
        raise RadarFailure(INVALID_RESPONSE)


# --- upstream fetch -------------------------------------------------------------------


def _get(http_get, url, *, headers, params, timeout, limit):
    """One upstream GET; returns the body bytes (at most ``limit`` + 1) or raises."""
    try:
        response = http_get(url, headers=headers, params=params, timeout=timeout, stream=True)
    except requests.RequestException:
        # Transport failure. The exception text may contain the URL: never logged.
        raise RadarFailure(UPSTREAM_UNREACHABLE) from None
    try:
        status = int(response.status_code)
        if not 200 <= status < 300:
            raise RadarFailure(UPSTREAM_ERROR, upstream_status=status)
        try:
            chunks, size = [], 0
            for chunk in response.iter_content(chunk_size=65536):
                chunks.append(chunk)
                size += len(chunk)
                if size > limit:
                    break
            return b"".join(chunks)
        except requests.RequestException:
            raise RadarFailure(UPSTREAM_UNREACHABLE) from None
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


def _fetch_once(api_key, metadata_url, connect_timeout, read_timeout, http_get):
    """Metadata (with the key), then the image it names (without the key)."""
    timeout = (connect_timeout, read_timeout)
    raw = _get(http_get, metadata_url, headers={"Authorization": api_key},
               params=_METADATA_PARAMS, timeout=timeout, limit=1_000_000)
    try:
        payload = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise RadarFailure(INVALID_RESPONSE) from None
    metadata = parse_metadata(payload)
    image = _get(http_get, metadata.product_url, headers={}, params=None,
                 timeout=timeout, limit=MAX_IMAGE_BYTES)
    check_image(image)
    return metadata, image


def fetch_product(
    api_key: str,
    *,
    metadata_url: str = _METADATA_URL,
    connect_timeout: float = CONNECT_TIMEOUT_SECONDS,
    read_timeout: float = READ_TIMEOUT_SECONDS,
    deadline: float = UPSTREAM_DEADLINE_SECONDS,
    http_get: Callable[..., Any] | None = None,
) -> tuple[RadarMetadata, bytes]:
    """Fetch the metadata and the image within an overall ``deadline`` (seconds).

    As on the observation path, the exchange runs in a daemon worker thread and
    the caller waits at most ``deadline``; a stall or a slow drip ends in
    ``upstream_unreachable``, and a late result is discarded (never cached).
    """
    getter = http_get if http_get is not None else requests.get
    outcome: dict[str, Any] = {}

    def work() -> None:
        try:
            outcome["product"] = _fetch_once(
                api_key, metadata_url, connect_timeout, read_timeout, getter)
        except RadarFailure as failure:
            outcome["failure"] = failure
        except Exception:  # noqa: BLE001 — any other transport surprise
            outcome["failure"] = RadarFailure(UPSTREAM_UNREACHABLE)

    worker = threading.Thread(target=work, name="cwa-radar-fetch", daemon=True)
    worker.start()
    worker.join(deadline)
    if worker.is_alive():
        raise RadarFailure(UPSTREAM_UNREACHABLE)
    if "failure" in outcome:
        raise outcome["failure"]
    return outcome["product"]


# --- service with reuse window (R-V2-RAD-2) -------------------------------------------


def _taipei_now() -> datetime:
    return datetime.now(TAIPEI)


class RadarService:
    """Produces the ``/api/radar/latest`` answer.

    ``env``, ``clock``, ``http_get`` and the timing parameters are injectable so
    tests run offline. The key is read from ``env`` on every request that needs
    the upstream and is never stored on the instance.
    """

    def __init__(
        self,
        *,
        env: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] = _taipei_now,
        http_get: Callable[..., Any] | None = None,
        metadata_url: str = _METADATA_URL,
        reuse_window_seconds: float = REUSE_WINDOW_SECONDS,
        connect_timeout: float = CONNECT_TIMEOUT_SECONDS,
        read_timeout: float = READ_TIMEOUT_SECONDS,
        deadline: float = UPSTREAM_DEADLINE_SECONDS,
    ):
        if not 0 <= reuse_window_seconds <= REUSE_WINDOW_CEILING_SECONDS:
            raise ValueError("radar reuse window must be between 0 and 300 seconds")
        self._env = env if env is not None else os.environ
        self._clock = clock
        self._http_get = http_get
        self._metadata_url = metadata_url
        self._reuse_window = timedelta(seconds=reuse_window_seconds)
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._deadline = deadline
        self._lock = threading.Lock()
        self._cached: tuple[datetime, RadarResult] | None = None

    def _reusable(self, now: datetime) -> RadarResult | None:
        if self._cached is None:
            return None
        fetched_at, result = self._cached
        if timedelta(0) <= now - fetched_at < self._reuse_window:
            return result
        return None

    def latest(self) -> RadarResult:
        """Return the latest radar product (or a reused one), or a classified failure."""
        with self._lock:
            try:
                api_key = (self._env.get(ENV_KEY_NAME) or "").strip()
                if not api_key:
                    raise RadarFailure(KEY_NOT_CONFIGURED)
                reused = self._reusable(self._clock())
                if reused is not None:
                    return reused
                metadata, image = fetch_product(
                    api_key,
                    metadata_url=self._metadata_url,
                    connect_timeout=self._connect_timeout,
                    read_timeout=self._read_timeout,
                    deadline=self._deadline,
                    http_get=self._http_get,
                )
            except RadarFailure as failure:
                logger.warning(
                    "radar failed: reason=%s upstream_status=%s",
                    failure.reason,
                    failure.upstream_status,
                )
                status, body = failure.body()
                return RadarResult(status=status, body=body)
            except Exception:  # noqa: BLE001 — never let an unclassified error escape
                logger.warning("radar failed: reason=%s", INVALID_RESPONSE)
                status, body = RadarFailure(INVALID_RESPONSE).body()
                return RadarResult(status=status, body=body)

            fetched_at = self._clock()
            result = RadarResult(
                status=200,
                image=image,
                radar_time=metadata.radar_time,
                fetched_time=fetched_at.astimezone(TAIPEI).isoformat(timespec="seconds"),
            )
            self._cached = (fetched_at, result)
            logger.info("radar fetched: radar time %s, %d bytes", metadata.radar_time, len(image))
            return result
