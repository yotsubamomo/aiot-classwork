"""Dashboard skeleton: local-only resources and the static scan (BR-04; OV-1 precondition)."""
import hashlib
import re
import shutil
import subprocess

import pytest

from hw2 import offline_scan
from hw2.paths import ASSETS_DIR, DASHBOARD_HTML, UNIT_DIR

CHARTJS = ASSETS_DIR / "vendor" / "chart.umd.js"
CHARTJS_SHA256 = "74401d738dd3e03ee5dfb3b6841210fe2c4ead8a960c4011ca4ba0b78a9fd8f3"   # npm chart.js@4.4.1


def test_dashboard_has_no_external_resource_reference():
    findings = offline_scan.scan()
    assert findings == [], "\n".join(map(str, findings))
    scanned = {p.relative_to(UNIT_DIR).as_posix() for p in offline_scan.dashboard_files()}
    assert {"index.html", "assets/app.js", "assets/style.css", "assets/model_data.js",
            "assets/vendor/chart.umd.js"} <= scanned


def test_page_loads_data_as_a_js_global_and_the_bundled_chartjs():
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    scripts = re.findall(r'<script\s+src="([^"]+)"', html)
    assert scripts == ["assets/vendor/chart.umd.js", "assets/model_data.js", "assets/app.js"]
    assert all((UNIT_DIR / s).is_file() for s in scripts)
    assert 'lang="zh-Hant-TW"' in html


def test_bundled_chartjs_is_the_pinned_release():
    assert hashlib.sha256(CHARTJS.read_bytes()).hexdigest() == CHARTJS_SHA256
    assert CHARTJS.read_text(encoding="utf-8").startswith("/*!\n * Chart.js v4.4.1")
    assert (ASSETS_DIR / "vendor" / "chart.js.LICENSE.md").is_file()


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
@pytest.mark.parametrize("script", ["assets/app.js", "assets/model_data.js"])
def test_scripts_parse(script):
    subprocess.run(["node", "--check", str(UNIT_DIR / script)], check=True)


# --- the scanner itself, on a temporary unit -------------------------------------------------

def _unit(tmp_path, html, files=None):
    (tmp_path / "assets" / "vendor").mkdir(parents=True)
    (tmp_path / "index.html").write_text(html, encoding="utf-8")
    for name, text in (files or {}).items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return tmp_path


def _rules(tmp_path):
    return sorted(f.rule for f in offline_scan.scan(tmp_path))


CLEAN = '<html><body><a href="https://example.org/doc">doc</a><script src="assets/a.js"></script></body></html>'


def test_scanner_accepts_hyperlinks_banners_and_local_files(tmp_path):
    unit = _unit(tmp_path, CLEAN, {
        "assets/a.js": "document.title = 'x'; // comment\n",
        "assets/s.css": "body { background: url(data:image/png;base64,AAAA); }\n",
        "assets/vendor/lib.js": "/*!\n * Lib v1\n * https://lib.example.org\n */\n!function(){}();\n",
        "assets/model_data.js": "window.MODEL_DATA = {\"url\": \"%s\"};\n"
                                % offline_scan.ALLOWED_DATA_URLS[0],
    })
    assert _rules(unit) == []


@pytest.mark.parametrize("html, files, rule", [
    ('<script src="https://cdn.example.org/chart.js"></script>', {}, "external-reference"),
    ('<link rel="stylesheet" href="//fonts.example.com/css">', {}, "external-reference"),
    ('<img src="assets/missing.png">', {}, "missing-local-file"),
    ('<p>see https://example.org</p>', {}, "external-url"),
    (CLEAN, {"assets/s.css": "@font-face { src: url(https://fonts.example.com/a.woff2); }"},
     "css-url"),
    (CLEAN, {"assets/s.css": "@import 'other.css';"}, "css-import"),
    (CLEAN, {"assets/a.js": "fetch('model_data.json');"}, "network-api"),
    (CLEAN, {"assets/a.js": "var x = new XMLHttpRequest();"}, "network-api"),
    (CLEAN, {"assets/a.js": "var u = 'https://api.example.org/v1';"}, "external-url"),
    (CLEAN, {"assets/vendor/lib.js": "/*! x */ var u = 'https://cdn.example.org/x.js';"},
     "external-url"),
    (CLEAN, {"assets/model_data.js": "window.MODEL_DATA = {\"u\": \"https://other.example.org\"};"},
     "external-url"),
])
def test_scanner_reports_external_resources(tmp_path, html, files, rule):
    files = {"assets/a.js": "", **files}
    assert rule in _rules(_unit(tmp_path, html, files))
