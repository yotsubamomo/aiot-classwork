"""Parse stage: turn one F-D0047-091 JSON object into the 42-row snapshot.

Pure functions only — no network, no filesystem, no clock. The single public
entry point is :func:`derive_snapshot`, which either returns exactly
6 Regions x 7 Forecast Days = 42 rows or raises :class:`DeriveError` naming the
problem (missing county, missing half-day, invalid value, too few / non-consecutive
days). Callers treat any :class:`DeriveError` as "do not write the database".

Implements Spec R-DER-1..R-DER-8 with decisions DR-4 (half-up rounding),
DR-5 (retention: drop one leading incomplete day, then seven consecutive complete
days else fail) and DR-16 (invalid value -> county-day incomplete -> named error,
never a denominator change).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Iterable

from . import config


class DeriveError(ValueError):
    """A validation failure that must abort ingestion without a database write.

    The message always names the concrete problem (county and/or date) so the
    operator can see why the snapshot was rejected.
    """


# A single county's parsed periods: raw value strings keyed by (date, segment).
# segment is "day" (06:00 start) or "night" (18:00 start).
_Periods = dict[tuple[date, str], str]


def derive_snapshot(
    data: dict,
    invalid_values: Iterable[str] = config.DEFAULT_INVALID_VALUES,
) -> list[dict]:
    """Derive the six-Region x seven-day Forecast Snapshot from a raw response.

    Returns a list of 42 dicts ``{regionName, dataDate, mint, maxt}`` ordered by
    the canonical Region order then ``dataDate`` ascending. Raises
    :class:`DeriveError` on any validation failure defined by R-DER-3/4/6.
    """
    invalid = frozenset(invalid_values)
    counties = _extract_counties(data)

    # county name -> {"max": _Periods, "min": _Periods}
    parsed: dict[str, dict[str, _Periods]] = {}
    # date -> set of segments present anywhere (used to pick the window)
    global_segments: dict[date, set[str]] = {}

    for county in counties:
        name = county.get("LocationName")
        if not name:
            continue
        max_periods = _element_periods(county, config.ELEMENT_MAX, config.FIELD_MAX)
        min_periods = _element_periods(county, config.ELEMENT_MIN, config.FIELD_MIN)
        parsed[name] = {"max": max_periods, "min": min_periods}
        for (d, seg) in list(max_periods) + list(min_periods):
            global_segments.setdefault(d, set()).add(seg)

    window = _select_window(global_segments)

    rows: list[dict] = []
    for region in config.REGION_ORDER:
        members = config.REGION_MEMBERS[region]
        for d in window:
            county_mins: list[Decimal] = []
            county_maxs: list[Decimal] = []
            for county_name in members:
                cmin, cmax = _county_day_values(parsed, county_name, d, invalid)
                county_mins.append(cmin)
                county_maxs.append(cmax)
            rows.append(
                {
                    "regionName": region,
                    "dataDate": d.isoformat(),
                    "mint": _mean_half_up(county_mins),
                    "maxt": _mean_half_up(county_maxs),
                }
            )

    # Defensive post-condition: the loops above always build REGION_COUNT x
    # FORECAST_DAYS_REQUIRED rows, so this guards against a future refactor
    # silently changing the snapshot shape rather than a currently reachable path.
    expected = config.REGION_COUNT * config.FORECAST_DAYS_REQUIRED
    if len(rows) != expected:
        raise DeriveError(f"expected {expected} rows but derived {len(rows)}")
    return rows


def _extract_counties(data: dict) -> list[dict]:
    """Return ``records.Locations[0].Location[]`` or raise DeriveError."""
    try:
        locations = data["records"]["Locations"]
        location_block = locations[0]
        counties = location_block["Location"]
    except (KeyError, IndexError, TypeError) as exc:
        raise DeriveError(
            "unexpected response structure: missing records.Locations[0].Location"
        ) from exc
    if not isinstance(counties, list) or not counties:
        raise DeriveError("response contains no Location entries")
    return counties


def _element_periods(county: dict, element_name: str, field: str) -> _Periods:
    """Collect one weather element's raw period values keyed by (date, segment)."""
    periods: _Periods = {}
    for element in county.get("WeatherElement", []) or []:
        if element.get("ElementName") != element_name:
            continue
        for entry in element.get("Time", []) or []:
            start = entry.get("StartTime")
            key = _period_key(start)
            if key is None:
                continue
            values = entry.get("ElementValue") or []
            raw = values[0].get(field) if values else None
            periods[key] = raw
    return periods


def _period_key(start_time: str | None) -> tuple[date, str] | None:
    """Map a StartTime to (date, segment). Segment: 06:00 -> day, 18:00 -> night."""
    if not start_time:
        return None
    try:
        dt = datetime.fromisoformat(start_time)
    except ValueError:
        return None
    if dt.hour == 6:
        return dt.date(), "day"
    if dt.hour == 18:
        return dt.date(), "night"
    # Any other start hour is outside the fixed F-D0047-091 12-hour cadence.
    return None


def _select_window(global_segments: dict[date, set[str]]) -> list[date]:
    """Pick the seven retained Forecast Days per R-DER-3 / DR-5."""
    all_dates = sorted(global_segments)
    if not all_dates:
        raise DeriveError("no forecast periods found in response")

    # Drop at most one leading incomplete date.
    if not _is_complete(global_segments, all_dates[0]):
        all_dates = all_dates[1:]

    window = all_dates[: config.FORECAST_DAYS_REQUIRED]
    if len(window) < config.FORECAST_DAYS_REQUIRED:
        raise DeriveError(
            "fewer than seven complete forecast days after dropping the leading "
            f"incomplete day: found {len(window)}"
        )

    for previous, current in zip(window, window[1:]):
        if current != previous + timedelta(days=1):
            raise DeriveError(
                "forecast days are not seven consecutive calendar days: "
                f"{previous.isoformat()} is not followed by {current.isoformat()}"
            )

    for d in window:
        if not _is_complete(global_segments, d):
            raise DeriveError(
                f"forecast day {d.isoformat()} is missing a 12-hour period"
            )
    return window


def _is_complete(global_segments: dict[date, set[str]], d: date) -> bool:
    """A Forecast Day is complete when both its 12-hour periods exist."""
    return global_segments.get(d, set()) >= {"day", "night"}


def _county_day_values(
    parsed: dict[str, dict[str, _Periods]],
    county_name: str,
    d: date,
    invalid: frozenset[str],
) -> tuple[Decimal, Decimal]:
    """Return (county-day MinT, county-day MaxT) or raise a named DeriveError."""
    county = parsed.get(county_name)
    if county is None:
        raise DeriveError(
            f"member county {county_name} is missing from the response "
            f"(needed for {d.isoformat()})"
        )

    day_min = _value(county["min"], (d, "day"), invalid)
    night_min = _value(county["min"], (d, "night"), invalid)
    day_max = _value(county["max"], (d, "day"), invalid)
    night_max = _value(county["max"], (d, "night"), invalid)

    if None in (day_min, night_min, day_max, night_max):
        raise DeriveError(
            f"county {county_name} has an incomplete or invalid value on "
            f"{d.isoformat()} (missing half-day or unparseable temperature)"
        )

    # county-day MinT = minimum of period minima; MaxT = maximum of period maxima.
    return min(day_min, night_min), max(day_max, night_max)


def _value(
    periods: _Periods, key: tuple[date, str], invalid: frozenset[str]
) -> Decimal | None:
    """Parse one period's raw value; None if absent, invalid, or unparseable."""
    if key not in periods:
        return None
    raw = periods[key]
    if raw is None:
        return None
    text = str(raw).strip()
    if text in invalid:
        return None
    try:
        value = Decimal(text)
    except InvalidOperation:
        return None
    # NaN / Infinity parse as Decimal but are not usable temperatures; treat them
    # as invalid so they surface as a named county-day error, not a later crash.
    if not value.is_finite():
        return None
    return value


def _mean_half_up(values: list[Decimal]) -> float:
    """Arithmetic mean rounded half-up to one decimal place (DR-4)."""
    total = sum(values, Decimal(0))
    mean = total / Decimal(len(values))
    quantized = mean.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return float(quantized)
