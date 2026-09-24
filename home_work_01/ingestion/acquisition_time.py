"""Acquisition-time format validation (DR-22.3 AT-1..AT-12).

A value is a **valid** acquisition time iff it is a *string* that exactly matches
``^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}\\+08:00$`` **and** denotes a real
calendar instant (month/day/hour/minute/second ranges, incl. leap years). The
offset must be exactly ``+08:00`` (``Z`` and every other offset are rejected,
never normalized); the precision is exactly to the second (fractional seconds are
rejected, never truncated); the date/time separator is an uppercase ``T``; there
is no space separator; and surrounding whitespace is never trimmed.

No future / range / plausibility check is done — that would read the clock, which
DR-17 §4.3(2) forbids on the offline path. A valid value is returned verbatim; the
caller stores exactly the input string (DR-17 §4.2(2), no normalization).

The same validator guards all three acquisition-time sources (DR-22.3 AT-8):
the CLI ``--acquired-at`` value, the provenance sidecar ``acquiredAt`` field, and
the online ``ingestion_timestamp()`` output. Failure messages name the offending
value and its source and the required format, and never contain a key, ``.env``
content, or any request header (H-1 / R-SEC-2).
"""

from __future__ import annotations

import re
from datetime import datetime

#: The exact required acquisition-time format, for messages and documentation.
REQUIRED_FORMAT = "YYYY-MM-DDTHH:MM:SS+08:00"
#: A concrete valid example, included in failure messages.
EXAMPLE = "2026-09-24T02:24:50+08:00"

# ASCII digits only; uppercase ``T``; the literal ``+08:00`` offset; exactly to the
# second (no fractional part); the whole string, anchored, so any leading/trailing
# whitespace or extra character fails.
_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+08:00$")


class AcquisitionTimeError(ValueError):
    """A supplied acquisition time is not a valid ``YYYY-MM-DDTHH:MM:SS+08:00`` instant.

    Raised so an acquisition-time source fails closed (the CLI/main turns it into a
    ``Ingestion failed: ...`` message and a non-zero exit with no database write),
    rather than recording a malformed or invented "last updated" value (DR-17).
    """


def _json_type(value: object) -> str:
    """A human-readable JSON type label for a non-string sidecar value (AT-11(b))."""
    if value is None:
        return "JSON null"
    if isinstance(value, bool):
        return "JSON boolean"
    if isinstance(value, (int, float)):
        return "JSON number"
    if isinstance(value, str):
        return "JSON string"
    if isinstance(value, list):
        return "JSON array"
    if isinstance(value, dict):
        return "JSON object"
    return type(value).__name__


def _render(value: object) -> str:
    """Render the offending value so an empty string or whitespace stays visible.

    Uses ``repr`` (so ``''`` and ``' '`` are distinguishable) and truncates very
    long inputs to keep the message bounded (AT-11(a)). This only ever echoes the
    acquisition-time input itself — never a key or header.
    """
    text = repr(value)
    if len(text) > 80:
        text = text[:77] + "..."
    return text


def is_valid_acquisition_time(value: object) -> bool:
    """Return ``True`` iff ``value`` is a valid acquisition time (AT-1..AT-6).

    ``value`` must be a ``str`` (AT-1), match the exact grammar (AT-2, which pins the
    ``+08:00`` offset, second precision, uppercase ``T``, and no whitespace), and
    denote a real calendar instant (AT-3). The grammar alone is not sufficient —
    e.g. ``datetime.fromisoformat`` accepts a bare date — so both the pattern and a
    strict ``strptime`` must succeed.
    """
    if not isinstance(value, str):
        return False
    if _PATTERN.match(value) is None:
        return False
    try:
        # The pattern already fixes the shape and the ``+08:00`` offset; strptime
        # confirms the numeric fields are a real instant (month 01-12, day in range
        # incl. leap years, hour 00-23, minute/second 00-59).
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        return False
    return True


def validate_acquisition_time(
    value: object, *, source: str, hint: str | None = None
) -> str:
    """Return ``value`` unchanged if it is valid; otherwise raise ``AcquisitionTimeError``.

    ``source`` labels where the value came from (e.g. ``--acquired-at`` or the
    sidecar field), so an operator can find the offending input (AT-11(b)). ``hint``
    adds an optional trailing clause (e.g. that omitting ``--acquired-at`` falls back
    to the sidecar). The message names the value, the source, and the required format
    with an example (AT-11(c)); it never contains a key, ``.env`` content, or any
    request header (H-1).
    """
    if is_valid_acquisition_time(value):
        return value  # verbatim; no normalization (AT-12)
    detail = _render(value)
    if not isinstance(value, str):
        detail = f"{detail} ({_json_type(value)})"
    message = (
        f"invalid acquisition time {detail} from {source}: "
        f"expected exactly {REQUIRED_FORMAT} (e.g. {EXAMPLE})"
    )
    if hint:
        message = f"{message}; {hint}"
    raise AcquisitionTimeError(message)
