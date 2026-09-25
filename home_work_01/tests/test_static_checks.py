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

**V2 re-scope (SPEC-V2 R-V2-SEC-4, DV-15, AC-V2-16; Issue #35 — add-only).**
* (a') The set that must hold no HTTP client and no ``opendata.cwa.gov.tw`` /
       ``CWA_API_KEY`` literal is now ``app.py``, ``weather_query.py`` **and their
       unit-local import closure** (computed from the import graph, so any unit
       module the forecast path starts importing is pulled in automatically).
       ``server.py``, ``api/index.py`` and the V2 observation module leave that
       set: the deployed backend may access CWA server-side for the observation
       path. They remain covered by the credential scans (``tests/test_secrets.py``
       and ``tools/credential_scan.py``). The HTTP-client detector itself and its
       regression probes are unchanged.
* (b)  Extended: in the first-party frontend files every request form --
       ``fetch``/``fetchJson``, ``.src =``, ``L.imageOverlay``, ``L.tileLayer``,
       ``new Image``, HTML ``src``/``<link href>``, CSS ``url()`` -- may only have a
       same-origin ``/api/`` or ``/static/`` literal target. The absolute-URL
       whitelist keeps only non-request constants.
* (c)  SQL still lives only in ``weather_query.py``; the V2 observation module is
       added to the no-SQL / no-``sqlite3`` set.
* (d)  Unchanged.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

_UNIT_DIR = Path(__file__).resolve().parent.parent
_APP = _UNIT_DIR / "app.py"
_SHARED = _UNIT_DIR / "weather_query.py"
_SERVER = _UNIT_DIR / "server.py"
_API_ENTRY = _UNIT_DIR / "api" / "index.py"
_REQUIREMENTS = _UNIT_DIR / "requirements.txt"
_STATIC_DIR = _UNIT_DIR / "static"

# The Streamlit Grading App side (Issue #19), used by the AC-26 checks.
_APP_SIDE = (_APP, _SHARED)

# V2 server-side observation module (SPEC-V2 R-V2-SEC-2(a); Issue #35).
_OBSERVATION = _UNIT_DIR / "observation.py"

# Python files that must contain no SQL and must not open the database directly
# (AC-04(c)/(d), R-V2-SEC-4(c)): everything on the presentation side except the
# single SQL owner (the shared module), including the V2 observation module.
# Issue #36 adds the pure representative-station rule module to the same set.
_REPRESENTATIVE = _UNIT_DIR / "representative.py"
_NON_SHARED_PYTHON = (_APP, _SERVER, _API_ENTRY, _OBSERVATION, _REPRESENTATIVE)

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
# constants, are forbidden — data requests must be same-origin under /api/. The
# scan is recursive (see ``_static_files``), so it now also reads the vendored
# Leaflet library and the vendored basemap under ``static/`` (#24 finding F-4).
# The three vendored-Leaflet entries below are EXACT known non-request constants,
# the same class as the SVG namespace: ``leafletjs.com`` is Leaflet's default
# attribution link text and the two bug-tracker URLs are comments in
# ``leaflet.css``. None is a fetch/tile target, so whitelisting the exact strings
# does not weaken AC-04(b) — no request target is ever allowed (DR-20 P-3).
_ALLOWED_FRONTEND_URLS = {
    "http://www.w3.org/2000/svg",
    "https://leafletjs.com",
    "https://bugs.chromium.org/p/chromium/issues/detail?id=600120",
    "https://bugzilla.mozilla.org/show_bug.cgi?id=888319",
}
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


def _unit_module_files(name: str, importer: Path, level: int = 0) -> list[Path]:
    """Resolve an import name to the unit-local source files it loads.

    ``weather_query`` -> ``weather_query.py``; ``pkg.mod`` -> ``pkg/__init__.py``
    and ``pkg/mod.py`` (or ``pkg/mod/__init__.py``). Relative imports (``level``
    > 0) resolve against the importer's package. Names that are not unit-local
    (standard library, third-party) resolve to nothing.
    """
    base = _UNIT_DIR if level == 0 else importer.parent
    for _ in range(max(level - 1, 0)):
        base = base.parent
    files: list[Path] = []
    current = base
    for part in [p for p in name.split(".") if p]:
        package_init = current / part / "__init__.py"
        module_file = current / f"{part}.py"
        if package_init.is_file():
            files.append(package_init)
            current = current / part
        elif module_file.is_file():
            files.append(module_file)
            break
        else:
            break
    return files


def _unit_import_closure(roots: tuple[Path, ...]) -> tuple[Path, ...]:
    """Every unit-local Python file reachable from ``roots`` through imports."""
    seen: set[Path] = set()
    pending = [r.resolve() for r in roots]
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for node in ast.walk(_tree(path)):
            names: list[tuple[str, int]] = []
            if isinstance(node, ast.Import):
                names = [(alias.name, 0) for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                names = [(module, node.level)]
                names += [
                    (f"{module}.{a.name}" if module else a.name, node.level)
                    for a in node.names
                ]
            for name, level in names:
                for found in _unit_module_files(name, path, level):
                    if found.resolve() not in seen:
                        pending.append(found.resolve())
    return tuple(sorted(seen))


# AC-04(a) re-scoped (R-V2-SEC-4(a')): the forecast / Grading-App side that must
# be CWA-free and hold no HTTP client is app.py, the shared module and their
# unit-local import closure.
_PYTHON_SIDE = _unit_import_closure((_APP, _SHARED))


def _imports_http_client(targets: set[str]) -> set[str]:
    offending = {t for t in targets if t in _HTTP_CLIENT_DOTTED}
    offending |= {t for t in targets if t.split(".")[0] in _HTTP_CLIENT_ROOTS}
    return offending


# --- AC-04(a) no HTTP client, no CWA URL / key (app + shared + import closure) --


def test_python_side_is_app_and_shared_module_closure() -> None:
    """R-V2-SEC-4(a'): the checked set is exactly app.py + weather_query.py and
    their unit-local imports; the forecast side does not reach the V2 observation
    module (INV-V2-1)."""
    names = {p.relative_to(_UNIT_DIR.resolve()).as_posix() for p in _PYTHON_SIDE}
    assert {"app.py", "weather_query.py"} <= names
    assert "observation.py" not in names
    assert "server.py" not in names and "api/index.py" not in names


def test_import_closure_follows_unit_local_imports(tmp_path, monkeypatch) -> None:
    """The closure must pull in any unit module the roots import (directly,
    through a package, or relatively), so the (a') check cannot be bypassed by
    moving an HTTP client into a helper module."""
    monkeypatch.setattr(sys.modules[__name__], "_UNIT_DIR", tmp_path)
    (tmp_path / "root.py").write_text("import helper\nfrom pkg import sub\n", encoding="utf-8")
    (tmp_path / "helper.py").write_text("import requests\n", encoding="utf-8")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "pkg" / "sub.py").write_text("from . import leaf\n", encoding="utf-8")
    (tmp_path / "pkg" / "leaf.py").write_text("import json\n", encoding="utf-8")
    closure = _unit_import_closure((tmp_path / "root.py",))
    assert {p.name for p in closure} == {"root.py", "helper.py", "__init__.py", "sub.py", "leaf.py"}
    offending: set[str] = set()
    for path in closure:
        offending |= _imports_http_client(_import_targets(path))
    assert offending == {"requests"}


def test_python_side_imports_no_http_client() -> None:
    for path in _PYTHON_SIDE:
        offending = _imports_http_client(_import_targets(path))
        assert not offending, f"{path.name} imports HTTP client(s): {offending}"


@pytest.mark.parametrize(
    "snippet",
    [
        "from urllib import request",
        "from urllib import request as _r",
        "from urllib.request import urlopen",
        "import urllib.request",
        "from http import client",
        "import requests as r",
    ],
)
def test_import_check_catches_http_client_from_source(snippet, tmp_path) -> None:
    """Regression guard for finding F-4, run through the *real* ``_import_targets``.

    Parsing the actual source is what makes this bite: if ``_import_targets``
    stopped recording ``module + "." + name`` for ``ImportFrom`` (the reverted
    form), ``from urllib import request`` would yield only ``{"urllib"}`` and this
    assertion would fail (finding F-2). A hand-built target set would not.
    """
    probe = tmp_path / "probe.py"
    probe.write_text(snippet + "\n", encoding="utf-8")
    assert _imports_http_client(_import_targets(probe)), snippet


@pytest.mark.parametrize(
    "snippet",
    ["from urllib import parse", "from urllib.parse import quote", "import json"],
)
def test_import_check_allows_benign_imports_from_source(snippet, tmp_path) -> None:
    """Benign standard-library imports must not be flagged (no false positive)."""
    probe = tmp_path / "ok.py"
    probe.write_text(snippet + "\n", encoding="utf-8")
    assert not _imports_http_client(_import_targets(probe)), snippet


def test_python_side_has_no_cwa_url_or_key_in_code() -> None:
    for path in _PYTHON_SIDE:
        for literal in _code_string_literals(path):
            assert "opendata.cwa.gov.tw" not in literal, path.name
            assert "CWA_API_KEY" not in literal, path.name


# --- AC-04(b) frontend: no CWA URL / key, data requests only to /api/ ----------


def _static_files() -> list[Path]:
    """Every file served under ``static/``, RECURSIVELY.

    Recursing into subdirectories (``static/data/``, ``static/vendor/``) closes
    #24 finding F-4: the CWA-URL/key and external-absolute-URL scans now cover the
    vendored Leaflet library and the vendored vector basemap, not just the
    top-level frontend files.
    """
    return sorted(p for p in _STATIC_DIR.rglob("*") if p.is_file())


def test_static_scan_is_recursive_over_subdirectories() -> None:
    """Guard #24 F-4's fix: the frontend scan must reach ``static/`` subdirectories
    (the vendored library and the vendored basemap), not just the top level."""
    scanned = {p.relative_to(_STATIC_DIR).as_posix() for p in _static_files()}
    assert "data/basemap.js" in scanned, "static/data/ is not scanned"
    assert any(p.startswith("vendor/") for p in scanned), "static/vendor/ is not scanned"


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


# R-V2-SEC-4(b): literal targets of every request form in the first-party
# frontend. Vendored third-party files keep the absolute-URL whitelist check above
# (their internal ``.src =`` assignments use variables, not literals).
_FIRST_PARTY_FRONTEND = ("index.html", "app.js", "styles.css", "data/basemap.js")
_Q = "[`'\"]"
_NOT_Q = "[^`'\"]*"
_REQUEST_FORMS = (
    re.compile(r"\bfetch(?:Json)?\(\s*" + _Q + "(?P<target>" + _NOT_Q + ")"),
    re.compile(r"\.src\s*=\s*" + _Q + "(?P<target>" + _NOT_Q + ")"),
    re.compile(r"\bL\.imageOverlay\(\s*" + _Q + "(?P<target>" + _NOT_Q + ")"),
    re.compile(r"\bL\.tileLayer(?:\.\w+)?\(\s*" + _Q + "(?P<target>" + _NOT_Q + ")"),
    re.compile(
        r"<(?:img|script|iframe|source|video|audio|embed)\b[^>]*\bsrc\s*=\s*[\"'](?P<target>[^\"']*)",
        re.IGNORECASE,
    ),
    re.compile(r"<link\b[^>]*\bhref\s*=\s*[\"'](?P<target>[^\"']*)", re.IGNORECASE),
    re.compile(r"url\(\s*[\"']?(?P<target>[^)\"']*)"),
)
_ALLOWED_TARGET_PREFIXES = ("/api/", "/static/")


def _request_targets(text: str) -> list[str]:
    return [m.group("target") for rx in _REQUEST_FORMS for m in rx.finditer(text)]


def test_first_party_request_forms_target_only_api_or_static() -> None:
    found = 0
    for rel in _FIRST_PARTY_FRONTEND:
        path = _STATIC_DIR / rel
        assert path.is_file(), rel
        for target in _request_targets(path.read_text(encoding="utf-8")):
            found += 1
            assert target.startswith(_ALLOWED_TARGET_PREFIXES), (
                f"{rel}: request target {target!r} is not same-origin /api/ or /static/"
            )
    assert found, "no request-form literal targets found at all"


@pytest.mark.parametrize(
    "snippet",
    [
        'new Image().src = "https://example.test/radar.png";',
        'img.src = "//cdn.example.test/x.png";',
        'L.imageOverlay("https://example.test/r.png", bounds);',
        'L.tileLayer("https://{s}.tile.example.test/{z}/{x}/{y}.png");',
        '<img src="https://example.test/a.png">',
        '<script src="https://cdn.example.test/lib.js"></script>',
        '<link rel="stylesheet" href="https://fonts.example.test/css">',
        'fetch("https://example.test/data")',
        'background: url("https://example.test/bg.png");',
        'fetchJson("radar/latest")',
    ],
)
def test_request_form_check_catches_external_targets(snippet) -> None:
    """Regression guard: each request form with a non-/api/, non-/static/
    literal target is caught by the (b) extension."""
    targets = _request_targets(snippet)
    assert targets, snippet
    assert not all(t.startswith(_ALLOWED_TARGET_PREFIXES) for t in targets), snippet


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


def test_observation_module_is_in_the_no_sql_set() -> None:
    """R-V2-SEC-4(c): the new V2 module is checked for SQL / sqlite3 too."""
    assert _OBSERVATION.is_file()
    assert _OBSERVATION in _NON_SHARED_PYTHON


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
