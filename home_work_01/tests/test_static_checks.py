"""Static checks for the Python presentation side (AC-04 a/c/d, AC-26).

These read source text and the import graph — they do not execute the app — so
they hold regardless of runtime data. Scope of this ticket: ``app.py`` and the
shared query module it imports (the Flask backend and its checks arrive in the
next ticket). Fully offline (R-TC-5).

The checks inspect *code*, not documentation: the import graph, and string
literals other than module/function/class docstrings. A docstring that merely
describes a prohibition (for example, "imports no HTTP client") must not itself
trip the check — only real code would.

Coverage:
* AC-04(a) ``app.py`` and the shared module import no HTTP client and use no
           ``opendata.cwa.gov.tw`` or ``CWA_API_KEY`` in code
* AC-04(c) SQL statements live only in the shared module (none in ``app.py``)
* AC-04(d) ``app.py`` imports the shared module and re-implements no query or
           derivation (no direct ``sqlite3`` use in ``app.py``)
* AC-26   ``app.py`` and its imports use no map / ``Select Date`` / folium in
          code; ``requirements.txt`` does not list folium
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

_UNIT_DIR = Path(__file__).resolve().parent.parent
_APP = _UNIT_DIR / "app.py"
_SHARED = _UNIT_DIR / "weather_query.py"
_REQUIREMENTS = _UNIT_DIR / "requirements.txt"

# Python-side files this ticket owns: the app and the shared module it imports.
_PYTHON_SIDE = (_APP, _SHARED)

# HTTP client top-level packages that must never appear on the presentation side
# (R-SHR-5). ``urllib.request`` / ``http.client`` are matched as dotted names too.
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


def _tree(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _imported_modules(path: Path) -> set[str]:
    modules: set[str] = set()
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


def _code_string_literals(path: Path) -> list[str]:
    """All string-literal values in the file except docstrings.

    Docstrings (the first statement of a module, function, or class) are
    documentation, not code, so they are excluded — a docstring naming a
    forbidden token must not fail the check.
    """
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


def _imports_http_client(modules: set[str]) -> set[str]:
    offending = {m for m in modules if m in _HTTP_CLIENT_DOTTED}
    offending |= {m for m in modules if m.split(".")[0] in _HTTP_CLIENT_ROOTS}
    return offending


# --- AC-04(a) no HTTP client, no CWA URL / key ---------------------------------


def test_python_side_imports_no_http_client() -> None:
    for path in _PYTHON_SIDE:
        offending = _imports_http_client(_imported_modules(path))
        assert not offending, f"{path.name} imports HTTP client(s): {offending}"


def test_python_side_has_no_cwa_url_or_key_in_code() -> None:
    for path in _PYTHON_SIDE:
        for literal in _code_string_literals(path):
            assert "opendata.cwa.gov.tw" not in literal, path.name
            assert "CWA_API_KEY" not in literal, path.name


# --- AC-04(c) SQL only in the shared module ------------------------------------


def test_no_sql_statements_in_app() -> None:
    for literal in _code_string_literals(_APP):
        assert not _SQL_STATEMENT.search(literal), f"app.py has SQL: {literal!r}"


def test_shared_module_holds_the_sql() -> None:
    # Sanity: the single SQL owner is where the SQL actually lives.
    assert any(_SQL_STATEMENT.search(s) for s in _code_string_literals(_SHARED))


# --- AC-04(d) app imports the shared module, re-implements no query -------------


def test_app_imports_shared_module() -> None:
    assert "weather_query" in _imported_modules(_APP)


def test_app_does_not_touch_sqlite_directly() -> None:
    assert "sqlite3" not in _imported_modules(_APP), (
        "app.py must not open the database itself"
    )


# --- AC-26 no map / Select Date / folium on the app side -----------------------


def test_app_side_imports_no_folium() -> None:
    for path in _PYTHON_SIDE:
        modules = _imported_modules(path)
        assert not any(
            m.split(".")[0] in {"folium", "streamlit_folium"} for m in modules
        ), f"{path.name} must not import folium"


def test_app_side_uses_no_select_date_or_folium_in_code() -> None:
    for path in _PYTHON_SIDE:
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
    # The comment was rewritten (finding F-10), so the substring is absent
    # everywhere and a naive substring check also passes.
    assert "folium" not in text.lower()
