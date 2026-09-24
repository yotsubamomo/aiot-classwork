"""Vercel serverless entry point for the Flask dashboard (brief §5.2).

Vercel's Python builder imports the top-level ``app`` object from this file and
hands every request to it. The application itself lives in ``server.py`` one level
up, so this shim adds the unit directory to ``sys.path`` and builds ``app`` from it.
This keeps a single Python function serving both the API and the page, matching
the teacher-verified single-function pattern; the Vercel project's Root Directory
is ``home_work_01`` and ``data.db`` is packaged beside ``server.py`` (R-DS-8).

No environment variable or secret is read here or in ``server.py`` (R-SEC-3).

**Percent-encoded PATH_INFO on Vercel (#21 F-1).** Vercel delivers ``PATH_INFO``
to the WSGI app **still percent-encoded** — it does not URL-decode the path the
way a PEP 3333 server does. So a non-ASCII path segment such as a Chinese Region
name arrives as ``%E4%B8%AD...`` and never matches ``<region>``: every
``/api/regions/<Region>/series`` returned 404 on the live deployment (the whole
dashboard showed "That Region is not available…" with an empty table) while
passing locally, where Werkzeug decodes the path so the Flask test client cannot
reproduce it. This entry point therefore wraps the app in a thin WSGI middleware
that restores the decoded, PEP 3333 ``PATH_INFO`` before Flask routing. The fix
lives at the deployment boundary; ``server.py`` keeps standard Flask semantics.
"""

from __future__ import annotations

import os
import sys
from urllib.parse import unquote_to_bytes

_UNIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _UNIT_DIR not in sys.path:
    sys.path.insert(0, _UNIT_DIR)

from server import create_app  # noqa: E402  (import after sys.path is set)


class PercentDecodedPathInfo:
    """WSGI middleware that percent-decodes ``PATH_INFO`` when it is still encoded.

    A PEP 3333 server delivers the request path already URL-decoded, as the raw
    path bytes carried in a latin-1 ``str`` (so a router does
    ``PATH_INFO.encode("latin-1").decode("utf-8")`` to recover text). Vercel skips
    that decode and passes the percent-encoded path through verbatim. This
    middleware reconstructs the expected form — ``unquote_to_bytes`` turns
    ``%E4%B8%AD`` back into the UTF-8 bytes, and ``.decode("latin-1")`` carries
    those bytes as the ``str`` Werkzeug expects — so routing resolves a Chinese
    Region name (or any non-ASCII segment) correctly.

    It only acts when ``PATH_INFO`` actually contains a ``%`` escape, so an ASCII
    path and the already-decoded latin-1 form a compliant server produces are both
    left untouched. That makes it idempotent and safe even if the platform ever
    starts decoding the path itself. (Our routes carry no literal ``%`` in a valid
    Region name or date, so a decoded value is never re-processed.)
    """

    def __init__(self, wsgi_app):
        self._wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        raw = environ.get("PATH_INFO", "")
        if "%" in raw:
            environ["PATH_INFO"] = unquote_to_bytes(raw).decode("latin-1")
        return self._wsgi_app(environ, start_response)


# One Python function serves both the API and the page (R-DS-8). ``app`` stays a
# Flask instance so Vercel's builder still detects a WSGI application; only its
# WSGI entry (``app.wsgi_app``) is wrapped, so the PATH_INFO fix applies to every
# request the deployed function handles.
app = create_app()
app.wsgi_app = PercentDecodedPathInfo(app.wsgi_app)

__all__ = ["app"]
