"""Vercel serverless entry point for the Flask dashboard (brief §5.2).

Vercel's Python builder imports the top-level ``app`` object from this file and
hands every request to it. The application itself lives in ``server.py`` one level
up, so this shim adds the unit directory to ``sys.path`` and re-exports ``app``.
This keeps a single Python function serving both the API and the page, matching
the teacher-verified single-function pattern; the Vercel project's Root Directory
is ``home_work_01`` and ``data.db`` is packaged beside ``server.py`` (R-DS-8).

No environment variable or secret is read here or in ``server.py`` (R-SEC-3).
"""

from __future__ import annotations

import os
import sys

_UNIT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _UNIT_DIR not in sys.path:
    sys.path.insert(0, _UNIT_DIR)

from server import app  # noqa: E402  (import after sys.path is set)

__all__ = ["app"]
