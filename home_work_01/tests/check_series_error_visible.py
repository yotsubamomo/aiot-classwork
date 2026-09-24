"""Reproducible browser check for finding F-1 (R-DS-6): a 503 / 404 from the
``/series`` endpoint on first load must produce a *visible* message, never a
silent chart-less page.

This is not part of the offline pytest suite (it needs a real browser and is
named so pytest does not collect it). It wraps the *unmodified* ``server.create_app``
and injects a chosen status into ``/api/regions/<region>/series`` while leaving
``/api/health`` and ``/api/regions`` working, so the page bootstraps and then hits
the failing series request exactly as it would on first load. It renders the page
in headless Chrome and asserts that the region panel is un-hidden and the
``#chart-status`` message element carries visible text.

Usage (from the unit directory, with the venv active and data.db present):

    python tests/check_series_error_visible.py            # checks 503 and 404
    CHROME="/path/to/chrome" python tests/check_series_error_visible.py

Optionally writes a screenshot when ``--shot <path>`` is given. Exit code 0 means
the page is not silent for every injected status; non-zero means it regressed.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from pathlib import Path
from wsgiref.simple_server import make_server

_UNIT_DIR = Path(__file__).resolve().parent.parent
if str(_UNIT_DIR) not in sys.path:
    sys.path.insert(0, str(_UNIT_DIR))

from flask import jsonify, request  # noqa: E402

from server import create_app  # noqa: E402


def _app_injecting(status: int):
    """The real app, but every ``/series`` request returns ``status`` JSON."""
    app = create_app()

    @app.before_request
    def _inject():  # pragma: no cover - exercised via the browser, not pytest
        if request.path.endswith("/series"):
            return jsonify(error=f"injected {status}"), status
        return None

    return app


def _find_chrome() -> str | None:
    env = os.environ.get("CHROME")
    if env and Path(env).exists():
        return env
    for cand in (
        "google-chrome",
        "chromium",
        "chrome",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ):
        found = shutil.which(cand) if not cand.endswith(".exe") else cand
        if found and Path(found).exists():
            return found
    return None


# The rendered DOM must show the panel un-hidden with a non-empty message.
_PANEL_RE = re.compile(r"<section[^>]*id=\"region-panel\"([^>]*)>")
_STATUS_RE = re.compile(
    r"<div[^>]*id=\"chart-status\"([^>]*)>(.*?)</div>", re.DOTALL
)


def _assert_visible_message(dom: str, status: int) -> None:
    panel = _PANEL_RE.search(dom)
    assert panel, f"[{status}] #region-panel not found in DOM"
    assert "hidden" not in panel.group(1), (
        f"[{status}] #region-panel is still hidden — the message is swallowed"
    )
    stat = _STATUS_RE.search(dom)
    assert stat, f"[{status}] #chart-status not found in DOM"
    assert "hidden" not in stat.group(1), f"[{status}] #chart-status is hidden"
    text = re.sub(r"<[^>]+>", "", stat.group(2)).strip()
    assert text, f"[{status}] #chart-status has no visible text"
    print(f"  [{status}] visible message: {text!r}")


def _check(chrome: str, status: int, shot: str | None) -> None:
    app = _app_injecting(status)
    httpd = make_server("127.0.0.1", 0, app)
    port = httpd.server_address[1]
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    profile = tempfile.mkdtemp()
    try:
        url = f"http://127.0.0.1:{port}/"
        args = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            f"--user-data-dir={profile}",
            "--virtual-time-budget=8000",
            "--window-size=1280,1000",
        ]
        if shot:
            args.append(f"--screenshot={shot}")
        args += ["--dump-dom", url]
        # Chrome writes the DOM as UTF-8; decode it explicitly (the Windows
        # console default would choke on the Chinese Region names).
        dom = subprocess.run(
            args, capture_output=True, timeout=60
        ).stdout.decode("utf-8", "replace")
        _assert_visible_message(dom, status)
    finally:
        httpd.shutdown()


def main() -> int:
    chrome = _find_chrome()
    if not chrome:
        print("SKIP: no Chrome/Chromium found (set CHROME=/path/to/chrome).")
        return 3
    shot = None
    if "--shot" in sys.argv:
        shot = sys.argv[sys.argv.index("--shot") + 1]
    print("Checking the /series error state is visible (finding F-1)...")
    _check(chrome, 503, shot)
    _check(chrome, 404, None)
    print("PASS: the page shows a visible message for both 503 and 404.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
