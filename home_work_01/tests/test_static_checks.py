"""Static checks for the presentation side (AC-04 a/b/c/d, AC-26).

These read source text and the import graph — they do not execute the app — so
they hold regardless of runtime data. Fully offline (R-TC-5).

Scope: the Python presentation side is now the Streamlit ``app.py``, the shared
query module, **and the Flask dashboard backend** (``server.py`` and the Vercel
entry ``api/index.py``); the browser side is the static frontend under
``static/``.

The checks inspect *code*, not documentation: the import graph, and string
literals other than module/function/class docstrings. A docstring that merely
describes a prohibition (for example, "imports no HTTP client") must not itself
trip the check — only real code would.

Coverage:
* AC-04(a) ``app.py``, the shared module and the Flask backend import no HTTP
           client and use no ``opendata.cwa.gov.tw`` / ``CWA_API_KEY`` in code.
           The import check catches dotted forms too — ``import urllib.request``,
           ``from urllib import request`` and ``from urllib.request import ...``
           (Issue #19 finding F-4, owner #20), plus ``from http import client``.
* AC-04(b) the static frontend contains no CWA URL / key and its data requests
           target only ``/api/`` (no external absolute-URL requests).
* AC-04(c) SQL statements live only in the shared module (none in ``app.py`` or
           the Flask backend).
* AC-04(d) ``app.py`` and the Flask backend import the shared module and
           re-implement no query (no direct ``sqlite3`` use).
* AC-26   ``app.py`` and its imports use no map / ``Select Date`` / folium in
          code; ``requirements.txt`` does not list folium (Grading App scope).
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

_UNIT_DIR = Path(__file__).resolve().parent.parent
_APP = _UNIT_DIR / "app.py"
_SHARED = _UNIT_DIR / "weather_query.py"
_SERVER = _UNIT_DIR / "server.py"
_API_ENTRY = _UNIT_DIR / "api" / "index.py"
_REQUIREMENTS = _UNIT_DIR / "requirements.txt"
_STATIC_DIR = _UNIT_DIR / "static"

# The Flask backend files (single function serving the page and the API).
_BACKEND = (_SERVER, _API_ENTRY)

# The Streamlit Grading App side (Issue #19), used by the AC-26 checks.
_APP_SIDE = (_APP, _SHARED)

# Every Python file on the presentation side that must be CWA-free and hold no
# HTTP client (AC-04(a): app.py, shared module, Flask backend).
_PYTHON_SIDE = (_APP, _SHARED, _SERVER, _API_ENTRY)

# Python files that must contain no SQL and must not open the database directly
# (AC-04(c)/(d)): everything except the single SQL owner (the shared module).
_NON_SHARED_PYTHON = (_APP, _SERVER, _API_ENTRY)

# HTTP client top-level packages that must never appear on the presentation side
# (R-SHR-5). Dotted modules are matched exactly as well.
_HTTP_CLIENT_ROOTS = {"requests", "httpx", "aiohttp", "urllib3"}
_HTTP_CLIENT_DOTTED = {"urllib.request", "http.client"}

# SQL *statements* (structural), so a UI label such as "Select Region" never
# matches — only real SQL that touches the tables does.
_SQL_STATEMENT = re.compile(
    r"(SELECT\b[\s\S]*?\bFROM\b)"
    r"|(INSERT\s+INTO\b)"
    r"|(DELETE\s+FROM\b)"
    r"|(UPDATE\s+\w+\s+SET\b)"
    r"|(CREATE\s+TABLE\b)"
    r"|(DROP\s+TABLE\b)",
    re.IGNORECASE,
)

# Absolute URLs found in the frontend, other than these known non-request
# constants, are forbidden — data requests must be same-origin under /api/.
_ALLOWED_FRONTEND_URLS = {"http://www.w3.org/2000/svg"}
_URL_RE = re.compile(r"https?://[^\s'\"`)]+")


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _import_targets(path: Path) -> set[str]:
    """Return every importable name the file pulls in, including dotted forms.

    ``import a.b``            -> {"a.b"}
    ``from x.y import z``     -> {"x.y", "x.y.z"}
    ``from urllib import request`` -> {"urllib", "urllib.request"}

    Recording ``module + "." + name`` for ``ImportFrom`` is what lets the HTTP
    client check see ``from urllib import request`` (finding F-4); recording only
    ``node.module`` (``urllib``) would miss it.
    """
    targets: set[str] = set()
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                targets.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            targets.add(node.module)
            for alias in node.names:
                targets.add(f"{node.module}.{alias.name}")
    return targets


def _code_string_literals(path: Path) -> list[str]:
    """All string-literal values in the file except docstrings."""
    tree = _tree(path)
    docstring_ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            body = getattr(node, "body", [])
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                docstring_ids.add(id(body[0].value))
    return [
        node.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and id(node) not in docstring_ids
    ]


def _imports_http_client(targets: set[str]) -> set[str]:
    offending = {t for t in targets if t in _HTTP_CLIENT_DOTTED}
    offending |= {t for t in targets if t.split(".")[0] in _HTTP_CLIENT_ROOTS}
    return offending


# --- AC-04(a) no HTTP client, no CWA URL / key (app + shared + backend) ---------


def test_python_side_imports_no_http_client() -> None:
    for path in _PYTHON_SIDE:
        offending = _imports_http_client(_import_targets(path))
        assert not offending, f"{path.name} imports HTTP client(s): {offending}"


def test_import_check_catches_from_urllib_import_request() -> None:
    """Regression guard for finding F-4: the ``from urllib import request`` form
    (and the dotted ``from urllib.request import ...``) must be detected."""
    assert _imports_http_client({"urllib", "urllib.request"})
    assert _imports_http_client({"urllib.request", "urllib.request.urlopen"})
    assert _imports_http_client({"http", "http.client"})
    # A benign urllib submodule is not an HTTP client.
    assert not _imports_http_client({"urllib", "urllib.parse"})


def test_python_side_has_no_cwa_url_or_key_in_code() -> None:
    for path in _PYTHON_SIDE:
        for literal in _code_string_literals(path):
            assert "opendata.cwa.gov.tw" not in literal, path.name
            assert "CWA_API_KEY" not in literal, path.name


# --- AC-04(b) frontend: no CWA URL / key, data requests only to /api/ ----------


def _static_files() -> list[Path]:
    return sorted(p for p in _STATIC_DIR.iterdir() if p.is_file())


def test_frontend_has_no_cwa_url_or_key() -> None:
    for path in _static_files():
        text = path.read_text(encoding="utf-8")
        assert "opendata.cwa.gov.tw" not in text, path.name
        assert "CWA_API_KEY" not in text, path.name


def test_frontend_makes_no_external_absolute_url_requests() -> None:
    """The frontend must not reach any absolute URL (so no CWA, no third-party
    weather API); every data request is same-origin under /api/."""
    for path in _static_files():
        text = path.read_text(encoding="utf-8")
        for url in _URL_RE.findall(text):
            assert url in _ALLOWED_FRONTEND_URLS, f"{path.name} references {url!r}"


def test_frontend_requests_use_the_api_prefix() -> None:
    """Positive check: the frontend's request helper is fed only /api/ paths."""
    app_js = (_STATIC_DIR / "app.js").read_text(encoding="utf-8")
    calls = re.findall(r"fetch(?:Json)?\(\s*([`'\"])([^`'\"]*)", app_js)
    literal_targets = [text for _q, text in calls if text]
    assert literal_targets, "no fetch/fetchJson string-literal targets found"
    for target in literal_targets:
        assert target.startswith("/api/"), f"non-/api/ request target: {target!r}"


# --- AC-04(c) SQL only in the shared module ------------------------------------


def test_no_sql_statements_outside_shared_module() -> None:
    for path in _NON_SHARED_PYTHON:
        for literal in _code_string_literals(path):
            assert not _SQL_STATEMENT.search(literal), f"{path.name} has SQL: {literal!r}"


def test_shared_module_holds_the_sql() -> None:
    # Sanity: the single SQL owner is where the SQL actually lives.
    assert any(_SQL_STATEMENT.search(s) for s in _code_string_literals(_SHARED))


# --- AC-04(d) app and backend import the shared module, re-implement no query ---


def test_app_imports_shared_module() -> None:
    assert "weather_query" in _import_targets(_APP)


def test_backend_imports_shared_module() -> None:
    # The Flask backend reads data.db only through the shared module.
    assert "weather_query" in _import_targets(_SERVER), (
        "server.py must import the shared query module"
    )


def test_python_side_does_not_touch_sqlite_directly() -> None:
    for path in _NON_SHARED_PYTHON:
        assert "sqlite3" not in _import_targets(path), (
            f"{path.name} must not open the database itself"
        )


# --- AC-26 no map / Select Date / folium on the Grading App side ---------------


def test_app_side_imports_no_folium() -> None:
    for path in _APP_SIDE:
        targets = _import_targets(path)
        assert not any(
            t.split(".")[0] in {"folium", "streamlit_folium"} for t in targets
        ), f"{path.name} must not import folium"


def test_app_side_uses_no_select_date_or_folium_in_code() -> None:
    for path in _APP_SIDE:
        for literal in _code_string_literals(path):
            assert "Select Date" not in literal, f"{path.name} has Select Date"
            assert "folium" not in literal, f"{path.name} references folium"


def test_requirements_does_not_list_folium() -> None:
    text = _REQUIREMENTS.read_text(encoding="utf-8")
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        assert "folium" not in stripped.lower(), f"folium listed: {line!r}"
    assert "folium" not in text.lower()
