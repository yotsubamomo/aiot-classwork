"""Static scan of the dashboard for external resource references (BR-04; OV-1 precondition).

Every ``.html``, ``.css`` and ``.js`` file of the dashboard (``index.html`` and ``assets/``) is
scanned. A finding is any of:

- ``http://``, ``https://`` or a protocol-relative ``//host`` reference, except
  (a) the ``href`` of an ``<a>`` element in HTML (a document hyperlink, not a resource; Brief §7),
  (b) inside a ``/*! ... */`` license comment of a file under ``assets/vendor/``, and
  (c) in a generated data file (``assets/model_data.js``), a URL listed in
  :data:`ALLOWED_DATA_URLS` (data shown as a hyperlink, never requested);
- in CSS and HTML, ``url(`` whose target is not a ``data:`` URI or an existing relative file of the
  unit, and ``@import``;
- in the unit's own scripts (not ``assets/vendor/``), a network API: ``fetch(``,
  ``XMLHttpRequest``, ``WebSocket``, ``EventSource``, ``sendBeacon``, ``importScripts``, ``import(``;
- in HTML, a ``src``/``href``/``srcset``/``poster``/``data``/``action`` reference (other than
  ``<a href>``) that is absolute or names a file missing from the unit.
"""
import re
from dataclasses import dataclass
from pathlib import Path

from .paths import UNIT_DIR

ALLOWED_DATA_URLS = ("https://www.kaggle.com/datasets/harlfoxem/housesalesprediction",)
DATA_FILES = ("assets/model_data.js",)
SCANNED_SUFFIXES = (".html", ".css", ".js")

_URL = re.compile(r"""(?:https?:)?//[A-Za-z0-9][A-Za-z0-9.-]*\.[A-Za-z]{2,}[^\s"'<>)]*""", re.I)
_CSS_URL = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)
_IMPORT = re.compile(r"@import\b", re.I)
_NETWORK_API = re.compile(
    r"\bfetch\s*\(|\bXMLHttpRequest\b|\bWebSocket\b|\bEventSource\b|\bsendBeacon\b"
    r"|\bimportScripts\b|\bimport\s*\(", re.I)
_TAG = re.compile(r"<([A-Za-z][A-Za-z0-9-]*)\b([^>]*)>", re.S)
_ATTR = re.compile(r"""\b(src|href|srcset|poster|data|action)\s*=\s*(["'])(.*?)\2""", re.I | re.S)
_LICENSE_COMMENT = re.compile(r"/\*!.*?\*/", re.S)


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.text}"


def dashboard_files(unit_dir: Path = UNIT_DIR) -> list[Path]:
    files = [unit_dir / "index.html"]
    assets = unit_dir / "assets"
    if assets.is_dir():
        files += sorted(p for p in assets.rglob("*") if p.suffix.lower() in SCANNED_SUFFIXES)
    return [p for p in files if p.is_file()]


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def _blank(text: str, start: int, end: int) -> str:
    """Replace a span by spaces, keeping newlines so line numbers stay right."""
    return text[:start] + re.sub(r"[^\n]", " ", text[start:end]) + text[end:]


def scan_file(path: Path, unit_dir: Path = UNIT_DIR) -> list[Finding]:
    rel = path.relative_to(unit_dir).as_posix()
    text = path.read_text(encoding="utf-8")
    findings: list[Finding] = []
    vendored = rel.startswith("assets/vendor/")
    suffix = path.suffix.lower()
    work = text

    if vendored:
        for comment in list(_LICENSE_COMMENT.finditer(work)):
            work = _blank(work, comment.start(), comment.end())

    if suffix == ".html":
        for tag in _TAG.finditer(text):
            name = tag.group(1).lower()
            for attr in _ATTR.finditer(tag.group(2)):
                key, value = attr.group(1).lower(), attr.group(3).strip()
                start = tag.start(2) + attr.start(3)
                if name == "a" and key == "href":
                    work = _blank(work, start, start + len(attr.group(3)))
                    continue
                for ref in [v.split()[0] for v in value.split(",") if v.strip()] \
                        if key == "srcset" else [value]:
                    if _is_external(ref):
                        findings.append(Finding(rel, _line(text, start), "external-reference", ref))
                    elif ref and not ref.startswith(("#", "data:")):
                        target = (path.parent / ref.split("#")[0].split("?")[0]).resolve()
                        if not target.is_file() or unit_dir.resolve() not in target.parents:
                            findings.append(Finding(rel, _line(text, start), "missing-local-file",
                                                    ref))
                work = _blank(work, start, start + len(attr.group(3)))

    if rel in DATA_FILES:
        for allowed in ALLOWED_DATA_URLS:
            for m in re.finditer(re.escape(allowed), work):
                work = _blank(work, m.start(), m.end())

    for m in _URL.finditer(work):
        findings.append(Finding(rel, _line(text, m.start()), "external-url", m.group(0)))
    for m in (_CSS_URL.finditer(work) if suffix in (".css", ".html") else ()):
        target = m.group(2).strip()
        if target.startswith("data:"):
            continue
        if _is_external(target) or not target:
            findings.append(Finding(rel, _line(text, m.start()), "css-url", m.group(0)))
        else:
            resolved = (path.parent / target).resolve()
            if not resolved.is_file() or unit_dir.resolve() not in resolved.parents:
                findings.append(Finding(rel, _line(text, m.start()), "css-url", m.group(0)))
    for m in (_IMPORT.finditer(work) if suffix in (".css", ".html") else ()):
        findings.append(Finding(rel, _line(text, m.start()), "css-import", m.group(0)))
    if suffix in (".js", ".html") and not vendored and rel not in DATA_FILES:
        for m in _NETWORK_API.finditer(work):
            findings.append(Finding(rel, _line(text, m.start()), "network-api", m.group(0)))
    if vendored:
        for m in _NETWORK_API.finditer(work):
            if m.group(0).lower().startswith(("fetch", "xmlhttprequest", "websocket",
                                              "eventsource", "sendbeacon", "importscripts")):
                findings.append(Finding(rel, _line(text, m.start()), "network-api", m.group(0)))
    return findings


def _is_external(ref: str) -> bool:
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:)?//", ref, re.I)) or \
        bool(re.match(r"^(?:https?|ftp|wss?):", ref, re.I))


def scan(unit_dir: Path = UNIT_DIR, files: list[Path] | None = None) -> list[Finding]:
    """All findings over the dashboard files (empty list means the scan passed)."""
    files = dashboard_files(unit_dir) if files is None else files
    out: list[Finding] = []
    for path in files:
        out.extend(scan_file(path, unit_dir))
    return out


if __name__ == "__main__":       # python -m hw2.offline_scan
    found = scan()
    for finding in found:
        print(finding)
    scanned = dashboard_files()
    print(f"scanned {len(scanned)} files: {'PASS' if not found else 'FAIL'} "
          f"({len(found)} findings)")
    raise SystemExit(1 if found else 0)
