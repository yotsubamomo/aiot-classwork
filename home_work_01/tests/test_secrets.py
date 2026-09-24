"""AC-07(d): the committed fixture and raw observation JSON contain no CWA key
and no Authorization value. Runs offline (no key needed) using the pattern scan."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.checks import scan_file, scan_text

UNIT_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS = [
    UNIT_DIR / "tests" / "fixtures" / "F-D0047-091_sample.json",
    UNIT_DIR / "data" / "raw" / "F-D0047-091.json",
    UNIT_DIR / "data" / "raw" / "F-D0047-091.meta.json",  # provenance sidecar (DR-17 T-4)
]


@pytest.mark.parametrize("path", ARTIFACTS, ids=lambda p: p.name)
def test_artifact_has_no_secret(path):
    assert path.is_file(), f"expected committed artifact {path}"
    assert scan_file(path) == []
    assert "Authorization" not in path.read_text(encoding="utf-8")


def test_scanner_flags_a_key_and_auth_value():
    # Guards against a scanner that silently passes everything.
    assert scan_text('{"Authorization": "CWA-1234-5678-90ab-cdef"}')
    assert scan_text("token CWA-1234-5678-90ab-cdef here")
    assert scan_text('{"note": "no secrets here"}') == []
