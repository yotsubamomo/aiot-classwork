"""AC-07(d): the committed fixture and raw observation JSON contain no CWA key
and no Authorization value. Runs offline (no key needed) using the pattern scan.

V2 extension (AC-V2-17(a), R-V2-SEC-5): the O-A0001-001 sample and the V2
backend code are scanned as well."""

from __future__ import annotations

from pathlib import Path

import pytest

from ingestion.checks import scan_file, scan_text

UNIT_DIR = Path(__file__).resolve().parent.parent
ARTIFACTS = [
    UNIT_DIR / "tests" / "fixtures" / "F-D0047-091_sample.json",
    UNIT_DIR / "data" / "raw" / "F-D0047-091.json",
    UNIT_DIR / "data" / "raw" / "F-D0047-091.meta.json",  # provenance sidecar (DR-17 T-4)
    # V2 sanitised real O-A0001-001 sample (SPEC-V2 R-V2-SEC-5, R-V2-TC-2; #35)
    UNIT_DIR / "tests" / "fixtures" / "O-A0001-001_sample.json",
    # V2 sanitised real O-A0058-006 radar metadata sample (R-V2-SEC-5; #40)
    UNIT_DIR / "tests" / "fixtures" / "O-A0058-006_metadata_sample.json",
]

# V2 backend code that may hold server-side CWA access (R-V2-SEC-4(a') moved it
# out of the static HTTP-client check); it must pass the credential scan instead.
V2_CODE = [
    UNIT_DIR / "server.py",
    UNIT_DIR / "api" / "index.py",
    UNIT_DIR / "observation.py",
    UNIT_DIR / "tests" / "test_observation.py",
    # Issue #36: representative-station rule and its tests, the Now/Forecast
    # mode frontend guards and the reproducible browser check.
    UNIT_DIR / "representative.py",
    UNIT_DIR / "tests" / "test_representative.py",
    UNIT_DIR / "tests" / "test_modes_frontend.py",
    UNIT_DIR / "tests" / "check_modes_browser.py",
    UNIT_DIR / "static" / "app.js",
    UNIT_DIR / "static" / "index.html",
    # Issue #37: Refresh / Stale / Unavailable guards and browser check.
    UNIT_DIR / "tests" / "test_refresh_frontend.py",
    UNIT_DIR / "tests" / "check_refresh_browser.py",
    # Issue #38: county interaction layer names, County context guards and
    # browser check.
    UNIT_DIR / "static" / "data" / "counties.js",
    UNIT_DIR / "tests" / "test_county_frontend.py",
    UNIT_DIR / "tests" / "check_county_browser.py",
    # Issue #39: map fence / responsive guards, stylesheet and browser check.
    UNIT_DIR / "static" / "styles.css",
    UNIT_DIR / "tests" / "test_fence_frontend.py",
    UNIT_DIR / "tests" / "check_fence_browser.py",
    # Issue #40: radar module, its tests, frontend guards and browser check.
    UNIT_DIR / "radar.py",
    UNIT_DIR / "tests" / "test_radar.py",
    UNIT_DIR / "tests" / "test_radar_frontend.py",
    UNIT_DIR / "tests" / "check_radar_browser.py",
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


@pytest.mark.parametrize("path", V2_CODE, ids=lambda p: p.name)
def test_v2_code_has_no_secret(path):
    assert path.is_file(), f"expected V2 code file {path}"
    assert scan_file(path) == []


def test_ci_credential_scan_covers_the_v2_sample():
    from tools.credential_scan import _AUTH_ARTIFACTS

    assert "home_work_01/tests/fixtures/O-A0001-001_sample.json" in _AUTH_ARTIFACTS
    assert "home_work_01/tests/fixtures/O-A0058-006_metadata_sample.json" in _AUTH_ARTIFACTS
