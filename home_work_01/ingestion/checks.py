"""Secret-scan helpers used before committing captured artifacts (AC-07(d)).

These functions confirm that a saved raw JSON / fixture contains no CWA key and
no ``Authorization`` value. They report *that* a secret was found, never the
secret itself, so the scan output is safe to print and to store in evidence.
"""

from __future__ import annotations

import re
from pathlib import Path

# CWA Open Data keys look like ``CWA-`` followed by a UUID-style token. The
# pattern is deliberately broad so a slightly different key shape is still caught.
KEY_PATTERN = re.compile(r"CWA-[0-9A-Za-z]{4,}(?:-[0-9A-Za-z]+){2,}")
# An "Authorization": "<value>" pair with a non-empty value would mean the header
# leaked into the payload.
AUTH_VALUE_PATTERN = re.compile(
    r'"[Aa]uthorization"\s*:\s*"(?P<value>[^"]+)"'
)


def scan_text(text: str, key: str | None = None) -> list[str]:
    """Return a list of human-readable findings (empty means clean).

    Findings never include the secret value. If ``key`` is given, the exact
    literal is also searched for.
    """
    findings: list[str] = []
    if key and key in text:
        findings.append("literal CWA_API_KEY value present")
    if KEY_PATTERN.search(text):
        findings.append("string matching the CWA key pattern present")
    for match in AUTH_VALUE_PATTERN.finditer(text):
        if match.group("value").strip():
            findings.append("non-empty Authorization value present")
            break
    return findings


def scan_file(path: str | Path, key: str | None = None) -> list[str]:
    """Scan a file's text for secrets; see :func:`scan_text`."""
    return scan_text(Path(path).read_text(encoding="utf-8"), key=key)
