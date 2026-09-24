#!/usr/bin/env python3
"""Deployment smoke check for the Taiwan Weather Forecast dashboard (Spec R-TC-7).

Given the public deployment URL, this script verifies the two observable
conditions of R-DS-9 / AC-15 against the *live* Vercel deployment:

* ``GET /``          -> HTTP 200 and the body contains ``Taiwan Weather Forecast``.
* ``GET /api/health`` -> HTTP 200 and the JSON body has ``status == "ok"``.

A freshly built serverless function can take a few seconds to warm up, so the
check retries until **both** conditions pass or a total warm-up budget of
``--timeout`` seconds (default 90, the R-DS-9 limit) is exhausted. Every attempt
prints a UTC timestamp, the URL and the two HTTP status codes; the script exits
``0`` on success and non-zero on failure, so it works as the pass/fail gate for
both a local run and the ``workflow_dispatch`` smoke workflow (Issue #22), which
reuses this exact file.

The URL is taken from the first command-line argument, or, when that is omitted,
from the ``HW01_DEPLOY_URL`` environment variable (the repository variable the
smoke workflow injects). Only the Python standard library is used, so no
dependency has to be installed in CI.

Usage::

    python smoke.py https://<public-deployment-host>
    HW01_DEPLOY_URL=https://<host> python smoke.py
    python smoke.py https://<host> --timeout 90 --interval 5
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

# The exact page title the dashboard must serve (Spec R-DS-9 / high-risk H-2 text).
_PAGE_MARKER = "Taiwan Weather Forecast"
# Name of the repository variable / environment variable that carries the URL when
# no CLI argument is given. Documented in the README so the workflow and a local
# run agree on it.
_URL_ENV_VAR = "HW01_DEPLOY_URL"


def _now() -> str:
    """Return the current time as a UTC ISO-8601 timestamp (seconds resolution)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get(url: str, timeout: float) -> tuple[int | None, bytes]:
    """Fetch ``url`` and return ``(status_code, body)``.

    A transport-level failure (DNS, connection, read timeout) is reported as
    ``(None, b"")`` so the caller can keep retrying during warm-up; an HTTP error
    response (4xx/5xx) still yields its real status code and body.
    """
    request = urllib.request.Request(url, headers={"User-Agent": "hw01-smoke/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:  # a real HTTP status (e.g. 503, 404)
        return exc.code, exc.read()
    except (urllib.error.URLError, TimeoutError, OSError):
        return None, b""


def _check_once(base_url: str, deadline: float) -> tuple[bool, int | None, int | None]:
    """Run one round of both checks; return ``(passed, root_code, health_code)``.

    ``passed`` is true only when ``GET /`` is 200 with the page marker present and
    ``GET /api/health`` is 200 with ``status == "ok"``.

    ``deadline`` is the ``time.monotonic()`` instant the total budget ends. Each of
    the two requests is capped by the time still left before it (never more than
    15 s), so a slow first request cannot let one attempt overrun the budget (#22
    N-2): the two GETs together stay bounded by the remaining budget.
    """

    def _budget() -> float:
        # At least 0.1 s so a request past the deadline still fails fast rather than
        # raising on a non-positive timeout.
        return max(0.1, min(15.0, deadline - time.monotonic()))

    root_code, root_body = _get(base_url + "/", _budget())
    root_ok = root_code == 200 and _PAGE_MARKER.encode() in root_body

    health_code, health_body = _get(base_url + "/api/health", _budget())
    health_ok = False
    if health_code == 200:
        try:
            health_ok = json.loads(health_body).get("status") == "ok"
        except (ValueError, AttributeError):
            health_ok = False

    return (root_ok and health_ok), root_code, health_code


def run_smoke(base_url: str, total_timeout: float, interval: float) -> bool:
    """Retry the smoke check until it passes or ``total_timeout`` seconds elapse.

    The total elapsed budget is enforced (R-TC-7 / AC-15: "≤ 90 s"): each request's
    own timeout is capped by the time left, and a check that only succeeds *after*
    the budget is spent is reported as a failure — so a slow deployment can never
    yield a PASS past the limit. Returns ``True`` on success. Each attempt and the
    final verdict are printed with a timestamp, the URL and the two status codes.
    """
    base_url = base_url.rstrip("/")
    start = time.monotonic()
    deadline = start + total_timeout
    attempt = 0
    root_code = health_code = None
    while True:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        attempt += 1
        # Both requests in this attempt are capped by the time left before the
        # deadline (see _check_once), so one attempt cannot overrun the budget.
        passed, root_code, health_code = _check_once(base_url, deadline)
        elapsed = time.monotonic() - start
        print(
            f"[{_now()}] attempt {attempt}  url={base_url}  "
            f"GET / -> {root_code}  GET /api/health -> {health_code}  "
            f"({elapsed:.1f}s elapsed)  {'PASS' if passed else 'not-ready'}"
        )
        if passed:
            if time.monotonic() <= deadline:
                print(f"[{_now()}] SMOKE PASS  url={base_url}  ({elapsed:.1f}s)")
                return True
            # Passed, but only after the budget was already spent -> fail.
            print(
                f"[{_now()}] SMOKE FAIL  url={base_url}  "
                f"passed after the {total_timeout:.0f}s budget ({elapsed:.1f}s elapsed)"
            )
            return False
        if time.monotonic() + interval >= deadline:
            break
        time.sleep(interval)

    print(
        f"[{_now()}] SMOKE FAIL  url={base_url}  "
        f"last GET / -> {root_code}  last GET /api/health -> {health_code}  "
        f"(no success within {total_timeout:.0f}s)"
    )
    return False


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Smoke-check the deployed Taiwan Weather Forecast dashboard.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=os.environ.get(_URL_ENV_VAR),
        help=(
            "Public deployment base URL (e.g. https://<host>). "
            f"Defaults to the {_URL_ENV_VAR} environment variable."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=90.0,
        help="Total warm-up retry budget in seconds (default: 90, the R-DS-9 limit).",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=5.0,
        help="Seconds to wait between attempts (default: 5).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(sys.argv[1:] if argv is None else argv)
    if not args.url:
        print(
            f"error: no URL given (pass it as an argument or set {_URL_ENV_VAR})",
            file=sys.stderr,
        )
        return 2
    return 0 if run_smoke(args.url, args.timeout, args.interval) else 1


if __name__ == "__main__":
    raise SystemExit(main())
