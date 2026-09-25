"""Latest Observation — server-side path for the Now mode (SPEC-V2 §2.2, §2.4).

This module is the deployed Dashboard backend's **only** access to CWA for the
observation path (R-V2-SEC-2(a)). It fetches the CWA dataset **O-A0001-001**
(hourly station observations) with the maintainer's key, normalises and trims
the upstream payload, and hands ``server.py`` either a success body or a
classified failure body for ``GET /api/observations/latest``. The browser never
sees the upstream structure, the upstream URL or the key (R-V2-OBS-3, OBS-12).

Data flow::

    request ─▶ LatestObservationService.latest()
                 ├─ key from the process env var ``CWA_API_KEY`` (R-V2-SEC-3)
                 ├─ reuse a recent success (≤ REUSE_WINDOW_SECONDS, R-V2-OBS-9)
                 ├─ fetch_upstream()  — bounded by UPSTREAM_DEADLINE_SECONDS (OBS-13)
                 └─ normalize()       — valid-station rules, dataset Observation Time
               ◀─ (HTTP status, JSON body): success, or failure with one ``reason``

Contract points implemented here (Executor HOW choices are documented in the
README section "Latest Observation endpoint"):

* **Valid station** (R-V2-OBS-2): non-empty ``StationId``; air temperature a
  finite decimal that is not a sentinel; finite WGS84 latitude / longitude;
  ``CountyName`` verbatim one of the 22 counties; a published ``ObsTime`` that
  parses to a date plus hour and minute. Invalid records never reach the
  response's station list, count or dataset Observation Time.
* **Per-field sentinels** (data standard V1.05, BRIEF-V2 §3.2): ``X`` / ``-99``
  apply to every field; ``T`` / ``-98`` only to precipitation; ``990`` (variable
  wind direction) only to wind direction; the whole set to air-temperature
  validity (R-V2-OBS-2(b)). See ``FIELD_SENTINELS``.
* **Values as published** (H-3): numbers are parsed from the published decimal
  strings without rounding or unit conversion; ``ObsTime`` strings are returned
  exactly as CWA published them; a sentinel never becomes a number (``null``).
* **Dataset Observation Time** (R-V2-OBS-4, DV-2): the largest valid-station
  ``ObsTime`` (compared as instants), returned as that station's published string.
* **Fetched Time**: the server clock (``+08:00``, seconds) at the moment the
  upstream fetch succeeded and produced this body.
* **Four failure reasons** (R-V2-OBS-11, DV-6): ``key_not_configured``,
  ``upstream_unreachable``, ``upstream_error``, ``invalid_response`` — each a
  non-2xx JSON with a fixed ``error`` text. The server never returns stale data.
* **No secrets out** (R-V2-OBS-12, SEC-7, H-1): failure texts are constants;
  logs carry only the reason and, for ``upstream_error``, the numeric HTTP
  status — never the key, the request headers, the upstream URL, the upstream
  body or an exception message (which could contain the URL).

* **Representative stations** (R-V2-DD-3, Issue #36): the success body also lists
  ``representativeStationIds`` — at most one valid station per county, chosen by
  the documented rule in :mod:`representative` — for the Now mode's
  Taiwan-wide view.

The module holds no SQL and does not touch ``data.db``; the forecast path
(``weather_query``, ``app.py``, the forecast ``/api/`` endpoints) does not import
it, so the forecast path stays CWA-free and key-free (INV-V2-1).
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Callable, Mapping

import requests

import representative

logger = logging.getLogger(__name__)

# The HTTP client's own logger records the upstream host and request line at
# DEBUG/INFO and retry details at WARNING. R-V2-SEC-7 forbids the upstream URL in
# server logs under any logging configuration, so it is held at ERROR here; this
# module's own log lines carry only the failure reason and status code.
logging.getLogger("urllib3").setLevel(logging.ERROR)

# --- contract-fixed constants (SPEC-V2 §5.1) ------------------------------------

DATASET_ID = "O-A0001-001"
ENV_KEY_NAME = "CWA_API_KEY"
_UPSTREAM_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/" + DATASET_ID
_UPSTREAM_PARAMS = {"format": "JSON"}

# The 22 counties (R-V2-DD-1): V1 R-DER-5's 19 Region members + the three
# outlying-island counties. Matched verbatim against ``CountyName`` (臺, not 台).
COUNTIES: frozenset[str] = frozenset(
    {
        "基隆市", "臺北市", "新北市", "桃園市", "新竹市", "新竹縣", "苗栗縣",
        "臺中市", "彰化縣", "南投縣", "雲林縣", "嘉義市", "嘉義縣",
        "臺南市", "高雄市", "屏東縣",
        "宜蘭縣", "花蓮縣", "臺東縣",
        "澎湖縣", "金門縣", "連江縣",
    }
)

# Sentinel codes of the CWA data standard V1.05 (BRIEF-V2 §3.2), grouped by the
# fields they are defined for. A published value equal to a code that applies to
# its field — as text, or numerically for the numeric codes (``-99.0``) — is "no
# valid value": it makes the air temperature invalid (station excluded) and
# turns an optional field into ``null``. A code is NOT applied to a field it is
# not defined for, so e.g. a published air pressure or rainfall of ``990.0`` is a
# real reading and is returned as published (H-3; audit #35 F-1).
MISSING_CODES: frozenset[str] = frozenset({"X", "-99"})  # 儀器故障; 缺值／異常 — any field
PRECIPITATION_CODES: frozenset[str] = frozenset({"T", "-98"})  # 雨跡; 連續無降水
WIND_DIRECTION_CODES: frozenset[str] = frozenset({"990"})  # 風向不定

# R-V2-OBS-2(b) names the whole set for air-temperature validity.
SENTINELS: frozenset[str] = MISSING_CODES | PRECIPITATION_CODES | WIND_DIRECTION_CODES

# The per-field sentinel sets actually applied (configurable via the service's
# ``field_sentinels=``; documented in the README).
FIELD_SENTINELS: dict[str, frozenset[str]] = {
    "airTemperature": SENTINELS,
    "relativeHumidity": MISSING_CODES,
    "windSpeed": MISSING_CODES,
    "windDirection": MISSING_CODES | WIND_DIRECTION_CODES,
    "airPressure": MISSING_CODES,
    "precipitation": MISSING_CODES | PRECIPITATION_CODES,
    "weather": MISSING_CODES,
    "coordinates": MISSING_CODES,
}

# --- Executor HOW choices (documented in the README) ----------------------------

# Upstream bound (R-V2-OBS-13, DV-7): the whole upstream exchange must finish
# within UPSTREAM_DEADLINE_SECONDS or the request is classified
# ``upstream_unreachable``. 8 s keeps the function under the smallest Vercel
# default function duration (10 s) with room for a cold start and normalisation.
CONNECT_TIMEOUT_SECONDS = 3.0
READ_TIMEOUT_SECONDS = 5.0
UPSTREAM_DEADLINE_SECONDS = 8.0

# Reuse window (R-V2-OBS-9, DV-5): a success is reused for this long (contract
# ceiling 600 s). Only successes are ever reused.
REUSE_WINDOW_SECONDS = 300
REUSE_WINDOW_CEILING_SECONDS = 600

TAIPEI = timezone(timedelta(hours=8))

# --- failure classification (R-V2-OBS-11, DV-6) ---------------------------------

KEY_NOT_CONFIGURED = "key_not_configured"
UPSTREAM_UNREACHABLE = "upstream_unreachable"
UPSTREAM_ERROR = "upstream_error"
INVALID_RESPONSE = "invalid_response"

# reason -> (HTTP status of our response, fixed human-readable text). The texts
# are constants: nothing from the upstream, the URL or the key is interpolated.
_FAILURES: dict[str, tuple[int, str]] = {
    KEY_NOT_CONFIGURED: (
        503,
        "Latest Observation is unavailable: the server has no CWA API key configured.",
    ),
    UPSTREAM_UNREACHABLE: (
        504,
        "Latest Observation is unavailable: the CWA service could not be reached "
        "in time.",
    ),
    UPSTREAM_ERROR: (
        502,
        "Latest Observation is unavailable: the CWA service returned an error status.",
    ),
    INVALID_RESPONSE: (
        502,
        "Latest Observation is unavailable: the CWA response was not usable "
        "(unreadable, unsuccessful, or no valid station).",
    ),
}
FAILURE_REASONS: tuple[str, ...] = tuple(_FAILURES)


class ObservationFailure(Exception):
    """A classified failure of the observation path.

    Carries only the reason code and, for ``upstream_error``, the numeric
    upstream HTTP status. It deliberately stores no message from the upstream or
    from a lower-level exception, so nothing secret can leak through it.
    """

    def __init__(self, reason: str, upstream_status: int | None = None):
        if reason not in _FAILURES:
            raise ValueError(f"unknown failure reason {reason!r}")
        super().__init__(reason)
        self.reason = reason
        self.upstream_status = upstream_status

    def response(self) -> tuple[int, dict[str, Any]]:
        """Return ``(HTTP status, JSON body)`` for this failure."""
        status, text = _FAILURES[self.reason]
        body: dict[str, Any] = {
            "dataset": DATASET_ID,
            "reason": self.reason,
            "error": text,
        }
        if self.reason == UPSTREAM_ERROR and self.upstream_status is not None:
            body["upstreamStatus"] = self.upstream_status
        return status, body


# --- value parsing ---------------------------------------------------------------

_OBS_TIME_SHAPE = re.compile(r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")


def parse_published_number(value: Any, sentinels: frozenset[str] = MISSING_CODES):
    """Return the published value as a JSON number, or ``None`` if not valid.

    ``None`` for: missing, non-numeric text, non-finite, booleans, or a sentinel
    (text match, or numeric match for numeric sentinels such as ``-99`` /
    ``-99.0``). A published integer string stays an ``int`` and a decimal string
    becomes the ``float`` with the same digits — no rounding (H-3, "as published").
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        text = repr(value)
    elif isinstance(value, str):
        text = value.strip()
    else:
        return None
    if not text or text in sentinels:
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    for sentinel in sentinels:
        try:
            if number == Decimal(sentinel):
                return None
        except InvalidOperation:
            continue  # a non-numeric sentinel such as "X" or "T"
    if number == number.to_integral_value() and "." not in text and "e" not in text.lower():
        return int(number)
    result = float(number)
    return result if math.isfinite(result) else None


def parse_published_text(value: Any, sentinels: frozenset[str] = MISSING_CODES) -> str | None:
    """Return a published text field (e.g. ``Weather``) or ``None`` if missing /
    empty / a sentinel."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or text in sentinels:
        return None
    return text


def parse_obs_time(value: Any) -> datetime | None:
    """Parse a published ``ObsTime`` to an aware instant, or ``None``.

    Valid means: a string with at least a date plus hour and minute
    (``YYYY-MM-DD[T ]HH:MM``) that ISO 8601 parsing accepts. The instant is used
    only for comparison (the maximum); the response keeps the published string.
    A time without an offset is read as Taiwan time (``+08:00``), the zone CWA
    publishes in.
    """
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not _OBS_TIME_SHAPE.match(text):
        return None
    try:
        instant = datetime.fromisoformat(text)
    except ValueError:
        return None
    if instant.tzinfo is None:
        instant = instant.replace(tzinfo=TAIPEI)
    return instant


def _wgs84(
    geo: Mapping[str, Any], sentinels: frozenset[str] = MISSING_CODES
) -> tuple[float, float] | None:
    """Return the station's finite WGS84 ``(latitude, longitude)`` or ``None``.

    A missing, non-numeric, non-finite or sentinel coordinate is no coordinate.
    """
    coordinates = geo.get("Coordinates")
    if not isinstance(coordinates, list):
        return None
    for entry in coordinates:
        if isinstance(entry, dict) and entry.get("CoordinateName") == "WGS84":
            lat = parse_published_number(entry.get("StationLatitude"), sentinels)
            lon = parse_published_number(entry.get("StationLongitude"), sentinels)
            if lat is None or lon is None:
                return None
            return float(lat), float(lon)
    return None


# --- normalisation (R-V2-OBS-2..5) ------------------------------------------------


@dataclass(frozen=True)
class NormalizedObservation:
    """The trimmed dataset: what the success body is built from."""

    observation_time: str  # dataset-level, as published (max of valid stations)
    stations: list[dict[str, Any]]
    received_station_count: int


def normalize_station(
    record: Any, field_sentinels: Mapping[str, frozenset[str]] = FIELD_SENTINELS
) -> tuple[dict[str, Any], datetime] | None:
    """Normalise one upstream station record, or return ``None`` if it is invalid.

    Returns the trimmed station dict and its parsed ``ObsTime`` instant. Each
    field is checked only against the sentinel codes defined for it
    (``field_sentinels``).
    """
    codes = field_sentinels
    if not isinstance(record, dict):
        return None
    station_id = record.get("StationId")
    if not isinstance(station_id, str) or not station_id.strip():
        return None
    geo = record.get("GeoInfo")
    elements = record.get("WeatherElement")
    obs = record.get("ObsTime")
    if not isinstance(geo, dict) or not isinstance(elements, dict) or not isinstance(obs, dict):
        return None

    temperature = parse_published_number(elements.get("AirTemperature"), codes["airTemperature"])
    if temperature is None:
        return None
    position = _wgs84(geo, codes["coordinates"])
    if position is None:
        return None
    county = geo.get("CountyName")
    if county not in COUNTIES:
        return None
    obs_time_text = obs.get("DateTime")
    obs_instant = parse_obs_time(obs_time_text)
    if obs_instant is None:
        return None

    now = elements.get("Now")
    precipitation = now.get("Precipitation") if isinstance(now, dict) else None
    name = record.get("StationName")
    town = geo.get("TownName")
    station = {
        "stationId": station_id,
        "stationName": name if isinstance(name, str) else None,
        "countyName": county,
        "townName": town if isinstance(town, str) else None,
        "latitude": position[0],
        "longitude": position[1],
        "observationTime": obs_time_text,
        "airTemperature": temperature,
        "relativeHumidity": parse_published_number(
            elements.get("RelativeHumidity"), codes["relativeHumidity"]
        ),
        "windSpeed": parse_published_number(elements.get("WindSpeed"), codes["windSpeed"]),
        "windDirection": parse_published_number(
            elements.get("WindDirection"), codes["windDirection"]
        ),
        "airPressure": parse_published_number(elements.get("AirPressure"), codes["airPressure"]),
        "precipitation": parse_published_number(precipitation, codes["precipitation"]),
        "weather": parse_published_text(elements.get("Weather"), codes["weather"]),
    }
    return station, obs_instant


def normalize(
    payload: Any, field_sentinels: Mapping[str, frozenset[str]] = FIELD_SENTINELS
) -> NormalizedObservation:
    """Validate the upstream payload and trim it to the valid stations.

    Raises :class:`ObservationFailure` (``invalid_response``) when the payload is
    not a successful O-A0001-001 response of the expected shape, or when it has
    zero valid stations (R-V2-OBS-5).
    """
    if not isinstance(payload, dict) or payload.get("success") != "true":
        raise ObservationFailure(INVALID_RESPONSE)
    result = payload.get("result")
    if not isinstance(result, dict) or result.get("resource_id") != DATASET_ID:
        raise ObservationFailure(INVALID_RESPONSE)
    records = payload.get("records")
    raw_stations = records.get("Station") if isinstance(records, dict) else None
    if not isinstance(raw_stations, list):
        raise ObservationFailure(INVALID_RESPONSE)

    stations: list[dict[str, Any]] = []
    latest_text: str | None = None
    latest_instant: datetime | None = None
    for record in raw_stations:
        normalized = normalize_station(record, field_sentinels)
        if normalized is None:
            continue
        station, instant = normalized
        stations.append(station)
        # Strictly greater keeps the first-seen published string on ties, so the
        # result is deterministic for a given payload.
        if latest_instant is None or instant > latest_instant:
            latest_instant, latest_text = instant, station["observationTime"]
    if not stations or latest_text is None:
        raise ObservationFailure(INVALID_RESPONSE)
    return NormalizedObservation(
        observation_time=latest_text,
        stations=stations,
        received_station_count=len(raw_stations),
    )


# --- upstream fetch (R-V2-OBS-13) -------------------------------------------------


def _fetch_once(
    api_key: str,
    url: str,
    connect_timeout: float,
    read_timeout: float,
    http_get: Callable[..., Any],
) -> Any:
    """One upstream GET. Returns the parsed JSON or raises ObservationFailure."""
    try:
        response = http_get(
            url,
            headers={"Authorization": api_key},
            params=_UPSTREAM_PARAMS,
            timeout=(connect_timeout, read_timeout),
        )
    except requests.RequestException:
        # Transport failure (DNS / connect / read timeout / reset). The exception
        # text may contain the URL, so it is never logged or returned.
        raise ObservationFailure(UPSTREAM_UNREACHABLE) from None
    try:
        status = int(response.status_code)
        if not 200 <= status < 300:
            raise ObservationFailure(UPSTREAM_ERROR, upstream_status=status)
        try:
            body = response.content
        except requests.RequestException:
            raise ObservationFailure(UPSTREAM_UNREACHABLE) from None
        try:
            return json.loads(body)
        except (ValueError, UnicodeDecodeError):
            raise ObservationFailure(INVALID_RESPONSE) from None
    finally:
        close = getattr(response, "close", None)
        if callable(close):
            close()


def fetch_upstream(
    api_key: str,
    *,
    url: str = _UPSTREAM_URL,
    connect_timeout: float = CONNECT_TIMEOUT_SECONDS,
    read_timeout: float = READ_TIMEOUT_SECONDS,
    deadline: float = UPSTREAM_DEADLINE_SECONDS,
    http_get: Callable[..., Any] | None = None,
) -> Any:
    """Fetch the raw upstream JSON within an overall ``deadline`` (seconds).

    The GET runs in a daemon worker thread; the caller waits at most
    ``deadline`` seconds. A stalled or slow-dripping upstream therefore ends in
    ``upstream_unreachable`` within the bound even when every individual socket
    read stays under ``read_timeout``. A result that arrives after the deadline
    is discarded (never cached).
    """
    getter = http_get if http_get is not None else requests.get
    outcome: dict[str, Any] = {}

    def work() -> None:
        try:
            outcome["payload"] = _fetch_once(api_key, url, connect_timeout, read_timeout, getter)
        except ObservationFailure as failure:
            outcome["failure"] = failure
        except Exception:  # noqa: BLE001 — any other transport surprise
            outcome["failure"] = ObservationFailure(UPSTREAM_UNREACHABLE)

    worker = threading.Thread(target=work, name="cwa-observation-fetch", daemon=True)
    worker.start()
    worker.join(deadline)
    if worker.is_alive():
        raise ObservationFailure(UPSTREAM_UNREACHABLE)
    if "failure" in outcome:
        raise outcome["failure"]
    return outcome["payload"]


# --- service with reuse window (R-V2-OBS-9) ---------------------------------------


def _taipei_now() -> datetime:
    return datetime.now(TAIPEI)


class LatestObservationService:
    """Produces the ``/api/observations/latest`` response.

    ``env``, ``clock``, ``http_get`` and the timing parameters are injectable so
    tests run offline with a controllable clock and simulated upstream responses.
    The key is read from ``env`` on every request that needs the upstream, never
    at construction, and is never stored on the instance.
    """

    def __init__(
        self,
        *,
        env: Mapping[str, str] | None = None,
        clock: Callable[[], datetime] = _taipei_now,
        http_get: Callable[..., Any] | None = None,
        url: str = _UPSTREAM_URL,
        reuse_window_seconds: float = REUSE_WINDOW_SECONDS,
        connect_timeout: float = CONNECT_TIMEOUT_SECONDS,
        read_timeout: float = READ_TIMEOUT_SECONDS,
        deadline: float = UPSTREAM_DEADLINE_SECONDS,
        field_sentinels: Mapping[str, frozenset[str]] = FIELD_SENTINELS,
    ):
        if not 0 <= reuse_window_seconds <= REUSE_WINDOW_CEILING_SECONDS:
            raise ValueError("reuse window must be between 0 and 600 seconds")
        self._env = env if env is not None else os.environ
        self._clock = clock
        self._http_get = http_get
        self._url = url
        self._reuse_window = timedelta(seconds=reuse_window_seconds)
        self._connect_timeout = connect_timeout
        self._read_timeout = read_timeout
        self._deadline = deadline
        if set(field_sentinels) != set(FIELD_SENTINELS):
            raise ValueError(f"field_sentinels must define exactly {sorted(FIELD_SENTINELS)}")
        self._field_sentinels = dict(field_sentinels)
        self._lock = threading.Lock()
        self._cached: tuple[datetime, dict[str, Any]] | None = None

    def _reusable(self, now: datetime) -> dict[str, Any] | None:
        if self._cached is None:
            return None
        fetched_at, body = self._cached
        age = now - fetched_at
        if timedelta(0) <= age < self._reuse_window:
            return body
        return None

    def latest(self) -> tuple[int, dict[str, Any]]:
        """Return ``(HTTP status, JSON body)``: a success or a classified failure."""
        with self._lock:
            try:
                api_key = (self._env.get(ENV_KEY_NAME) or "").strip()
                if not api_key:
                    raise ObservationFailure(KEY_NOT_CONFIGURED)
                reused = self._reusable(self._clock())
                if reused is not None:
                    return 200, reused
                payload = fetch_upstream(
                    api_key,
                    url=self._url,
                    connect_timeout=self._connect_timeout,
                    read_timeout=self._read_timeout,
                    deadline=self._deadline,
                    http_get=self._http_get,
                )
                dataset = normalize(payload, self._field_sentinels)
            except ObservationFailure as failure:
                logger.warning(
                    "latest observation failed: reason=%s upstream_status=%s",
                    failure.reason,
                    failure.upstream_status,
                )
                return failure.response()
            except Exception:  # noqa: BLE001 — never let an unclassified error escape
                logger.warning("latest observation failed: reason=%s", INVALID_RESPONSE)
                return ObservationFailure(INVALID_RESPONSE).response()

            fetched_at = self._clock()
            body = {
                "dataset": DATASET_ID,
                "observationTime": dataset.observation_time,
                "fetchedTime": fetched_at.astimezone(TAIPEI).isoformat(timespec="seconds"),
                "validStationCount": len(dataset.stations),
                "receivedStationCount": dataset.received_station_count,
                "stations": dataset.stations,
                # At most one representative valid station per county for the
                # Now mode's Taiwan-wide view (R-V2-DD-3; rule in representative.py).
                "representativeStationIds": representative.select_representatives(
                    dataset.stations
                ),
            }
            self._cached = (fetched_at, body)
            logger.info(
                "latest observation fetched: %d valid of %d stations",
                len(dataset.stations),
                dataset.received_station_count,
            )
            return 200, body


# --- local .env loading (R-V2-SEC-3(b)) --------------------------------------------


def load_local_env(env_path: str | Path, environ: dict[str, str] | None = None) -> bool:
    """Copy ``CWA_API_KEY`` from the unit's untracked ``.env`` into the process
    environment for a **local** run (``python server.py``).

    Only that one variable is read, only from the given path, and only when the
    environment does not already define it. Returns whether a value was loaded.
    Never prints or logs the value. The deployed function does not call this: on
    Vercel the variable comes from the project environment (R-V2-SEC-3(c)).
    """
    target = os.environ if environ is None else environ
    if (target.get(ENV_KEY_NAME) or "").strip():
        return False
    path = Path(env_path)
    if not path.is_file():
        return False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name, _, value = stripped.partition("=")
        if name.strip() == ENV_KEY_NAME:
            key = value.strip().strip('"').strip("'")
            if key:
                target[ENV_KEY_NAME] = key
                return True
    return False
