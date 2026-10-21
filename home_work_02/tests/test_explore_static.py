"""V2 static seam (Spec V2 「靜態 seam」; #74 V2-T1): King County unchanged, the bundled 50 Startups data,
the problem drop-down, and the V2 files' isolation rules.

- **King County unchanged**: the V1 blocks of ``index.html`` (DOM structure, attributes and static text;
  the exploratory subtree and the problem bar are not part of them) are compared with a structural
  snapshot taken from the page before this ticket (``tests/snapshots/v1_dashboard_blocks.json``, built
  from ``index.html`` at the accepted baseline ``d7f02d4``; when git is available the snapshot itself is
  re-derived from that commit). The V1 scripts, the core module, the stylesheet and ``model_data``
  keep their sha256 (DA ``derivation-SPEC-V2.md`` A-3 values; content with line ends normalised to LF,
  which is the git blob — a Windows checkout may turn LF into CRLF).
- **Bundled data**: the text embedded in ``assets/data/startups50.js`` equals ``50_Startups.csv`` byte
  for byte, and both have the recorded sha256.
- **Isolation**: no V2 page file names ``model_data`` / ``MODEL_DATA`` / ``test_inputs`` (DA B-9, A-3),
  none writes markup from strings (DA D-2), the V2 ids are namespaced, and the generic Python reference is
  imported by no formal path.
"""
import hashlib
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path

import pytest

from hw2.paths import ASSETS_DIR, DASHBOARD_HTML, RESULTS_DIR, UNIT_DIR

SNAPSHOT = UNIT_DIR / "tests" / "snapshots" / "v1_dashboard_blocks.json"
BASELINE = "d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907"
STARTUPS_SHA256 = "c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d"
V2_SCRIPTS = ["assets/data/startups50.js", "assets/explore_load.js", "assets/explore_engine.js",
              "assets/explore_plot.js", "assets/explore_app.js", "assets/explore_ui.js"]
V2_FILES = V2_SCRIPTS + ["assets/explore.css"]
# A-3 (derivation-SPEC-V2.md §7.3) plus the V1 stylesheet, all at the accepted baseline d7f02d4.
V1_SHA256 = {
    "assets/app.js": "c1ab3f21cd9cc324ad820c46621c985bf8728a511d6db9a7f286fd7e57c982ad",
    "assets/hw2core.js": "e75c5d48b84031ebfcb01bcd41ef6dfa84ba3edf3d5f6a554f97e67b3af22c14",
    "assets/model_data.js": "6cf0c11eec941c210a263bceaed7deede482181f99d74cae933f872d09c3a7ac",
    "results/model_data.json": "69dc1465ac5f2b067056aa4690fe607876761d9e0f340a0eccb9f37afcc18e61",
    "assets/style.css": "60a270164ef6f84353c386fb17e7f188579a9753b83eb5be167e364b2a6d5f3f",
}

# ---- a small DOM builder and the V1 snapshot ---------------------------------------------------

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track",
        "wbr"}


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "#document", "attrs": [], "children": []}
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": sorted([k, v] for k, v in attrs), "children": []}
        self.stack[-1]["children"].append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1]["children"].append({"tag": tag, "attrs": sorted([k, v] for k, v in attrs),
                                           "children": []})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1]["children"].append({"text": data})

    def handle_comment(self, data):
        self.stack[-1]["children"].append({"comment": data})


def parse(html: str) -> dict:
    b = _Builder()
    b.feed(html.replace("\r\n", "\n"))
    b.close()
    return b.root


def _walk(node):
    yield node
    for child in node.get("children", []):
        if "tag" in child:
            yield from _walk(child)


def _attr(node, name):
    return next((v for k, v in node["attrs"] if k == name), None)


# The V1 blocks: everything a King County user sees, except the V2 problem bar and #explore.
V1_SELECTORS = [
    ("title", lambda n: n["tag"] == "title"),
    ("a.skip", lambda n: n["tag"] == "a" and _attr(n, "class") == "skip"),
    ("div.brand", lambda n: n["tag"] == "div" and _attr(n, "class") == "brand"),
    ("#nav-toggle", lambda n: _attr(n, "id") == "nav-toggle"),
    ("#topnav", lambda n: _attr(n, "id") == "topnav"),
    ("#load-error", lambda n: _attr(n, "id") == "load-error"),
    ("#overview", lambda n: _attr(n, "id") == "overview"),
    ("#model", lambda n: _attr(n, "id") == "model"),
    ("#predictor", lambda n: _attr(n, "id") == "predictor"),
    ("#test", lambda n: _attr(n, "id") == "test"),
    ("#methods", lambda n: _attr(n, "id") == "methods"),
    ("footer", lambda n: n["tag"] == "footer"),
]


def v1_snapshot(html: str) -> dict:
    root = parse(html)
    nodes = list(_walk(root))
    out = {"html_lang": _attr(next(n for n in nodes if n["tag"] == "html"), "lang"),
           "order": [], "blocks": {}}
    for name, pick in V1_SELECTORS:
        found = [i for i, n in enumerate(nodes) if pick(n)]
        assert len(found) == 1, (name, len(found))
        out["blocks"][name] = nodes[found[0]]
        out["order"].append([name, found[0]])
    out["order"] = [name for name, _ in sorted(out["order"], key=lambda x: x[1])]
    return out


def _lf_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _git(*args):
    return subprocess.run(["git", *args], cwd=UNIT_DIR, capture_output=True, check=False)


# ---- King County unchanged ---------------------------------------------------------------------

def test_v1_blocks_match_the_pre_ticket_snapshot():
    stored = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    current = v1_snapshot(DASHBOARD_HTML.read_text(encoding="utf-8"))
    assert current["html_lang"] == stored["snapshot"]["html_lang"]
    assert current["order"] == stored["snapshot"]["order"]
    for name in stored["snapshot"]["blocks"]:
        assert current["blocks"][name] == stored["snapshot"]["blocks"][name], name


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_the_snapshot_is_the_accepted_baseline_page():
    shown = _git("show", f"{BASELINE}:home_work_02/index.html")
    if shown.returncode != 0:
        pytest.skip(f"baseline commit {BASELINE[:7]} is not in this clone")
    stored = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    assert stored["source"]["commit"] == BASELINE
    assert stored["source"]["sha256"] == hashlib.sha256(shown.stdout).hexdigest()
    assert v1_snapshot(shown.stdout.decode("utf-8")) == stored["snapshot"]


def test_v1_blocks_carry_no_exploratory_label_and_v2_ids_are_namespaced():
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    snap = v1_snapshot(html)
    assert "探索" not in json.dumps(snap, ensure_ascii=False)
    root = parse(html)
    explore = next(n for n in _walk(root) if _attr(n, "id") == "explore")
    ids = [_attr(n, "id") for n in _walk(explore) if _attr(n, "id")]
    assert ids[0] == "explore" and all(i.startswith("ex-") for i in ids[1:]), ids
    v1_ids = {_attr(n, "id") for b in snap["blocks"].values() for n in _walk(b) if _attr(n, "id")}
    assert not v1_ids & set(ids)
    # the exploratory subtree sits before the V1 blocks so that V1's section slices stay as they were
    assert html.index('id="explore"') < html.index('id="overview"')


def test_every_exploratory_block_is_labelled():
    root = parse(DASHBOARD_HTML.read_text(encoding="utf-8"))
    explore = next(n for n in _walk(root) if _attr(n, "id") == "explore")
    blocks = [n for n in _walk(explore) if "ex-block" in (_attr(n, "class") or "")]
    assert [_attr(b, "id") for b in blocks] == ["ex-custom", "ex-data", "ex-model", "ex-predictor",
                                                 "ex-test"]

    def text(n):
        return "".join(c.get("text", "") if "text" in c else text(c) for c in n["children"]
                       if "comment" not in c)
    for b in blocks:
        heading = next(n for n in _walk(b) if n["tag"] == "h2")
        assert "探索執行，非正式評估" in text(heading), _attr(b, "id")
    model = next(b for b in blocks if _attr(b, "id") == "ex-model")
    assert "訓練 CV" in text(next(n for n in _walk(model) if n["tag"] == "h2"))
    test_block = next(b for b in blocks if _attr(b, "id") == "ex-test")
    assert "探索 test（非正式評估）" in text(next(n for n in _walk(test_block) if n["tag"] == "h2"))
    assert "探索執行，非正式評估" in text(next(n for n in _walk(explore) if n["tag"] == "p"))


@pytest.mark.parametrize("rel", sorted(V1_SHA256))
def test_v1_scripts_core_stylesheet_and_model_data_are_unchanged(rel):
    assert _lf_sha256(UNIT_DIR / rel) == V1_SHA256[rel]


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_v1_files_have_no_diff_from_the_accepted_baseline():
    if _git("cat-file", "-e", BASELINE).returncode != 0:
        pytest.skip("baseline commit not in this clone")
    paths = ["assets/app.js", "assets/hw2core.js", "assets/model_data.js", "assets/style.css",
             "assets/vendor", "results", "hw2.ipynb"]
    out = _git("diff", "--name-only", BASELINE, "--", *paths).stdout.decode()
    assert out.strip() == "", out


def test_problem_drop_down_has_the_three_problems_in_order():
    root = parse(DASHBOARD_HTML.read_text(encoding="utf-8"))
    select = next(n for n in _walk(root) if _attr(n, "id") == "problem-select")
    assert select["tag"] == "select"
    options = [n for n in select["children"] if n.get("tag") == "option"]
    assert [_attr(o, "value") for o in options] == ["king_county", "startups50", "custom"]
    labels = ["".join(c.get("text", "") for c in o["children"]) for o in options]
    assert labels == ["King County 房價（正式分析）", "50 Startups 利潤（探索）", "自訂資料集（探索）"]
    assert ["selected", None] in options[0]["attrs"]
    label = next(n for n in _walk(root) if n["tag"] == "label" and _attr(n, "for") == "problem-select")
    assert "Problem" in "".join(c.get("text", "") for c in label["children"])
    explore = next(n for n in _walk(root) if _attr(n, "id") == "explore")
    assert ["hidden", None] in explore["attrs"]                # King County is what the page opens with


# ---- bundled 50 Startups data ------------------------------------------------------------------

def _embedded():
    text = (ASSETS_DIR / "data" / "startups50.js").read_text(encoding="utf-8")
    marker = "window.HW2_STARTUPS50 = "
    return json.loads(text[text.index(marker) + len(marker):].strip().rstrip(";"))


def test_embedded_50_startups_text_equals_the_csv_and_the_recorded_sha256():
    raw = (ASSETS_DIR / "data" / "50_Startups.csv").read_bytes()
    data = _embedded()
    assert data["csv"].encode("utf-8") == raw
    assert hashlib.sha256(raw).hexdigest() == STARTUPS_SHA256 == data["sha256"]
    assert data["bytes"] == len(raw) == 2436
    source = (ASSETS_DIR / "data" / "50_Startups.SOURCE.md").read_text(encoding="utf-8")
    assert STARTUPS_SHA256 in source
    assert "https://raw.githubusercontent.com/Avik-Jain/100-Days-Of-ML-Code/master/datasets/50_Startups.csv" in source
    license_text = (ASSETS_DIR / "data" / "50_Startups.LICENSE.md").read_text(encoding="utf-8")
    assert "MIT License" in license_text and "Copyright (c) 2018 Avik Jain" in license_text
    assert "The above copyright notice and this permission notice shall be included" in license_text


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_bundled_data_is_byte_pinned():
    out = _git("check-attr", "text", "--", "assets/data/50_Startups.csv").stdout.decode().strip()
    assert out.endswith(": text: unset"), out


# ---- isolation rules of the V2 page files ------------------------------------------------------

def _code(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", text)


@pytest.mark.parametrize("rel", V2_SCRIPTS)
def test_exploratory_files_never_read_model_data_or_test_inputs(rel):
    code = _code(UNIT_DIR / rel)
    for name in ("MODEL_DATA", "model_data", "test_inputs", "HW2Core"):
        assert name not in code, name


@pytest.mark.parametrize("rel", V2_SCRIPTS)
def test_exploratory_files_write_no_markup_and_run_no_strings(rel):
    """DA D-2 / A-9: strings from a dataset reach the page as text only."""
    code = _code(UNIT_DIR / rel)
    for api in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "DOMParser",
                "createContextualFragment", "srcdoc", "eval(", "new Function", "import(", "Worker(",
                "importScripts", "XMLHttpRequest", "WebSocket", "EventSource", "sendBeacon",
                ".src =", ".href =", "location", "localStorage", "sessionStorage", "indexedDB",
                "document.cookie"):
        assert api not in code, api
    assert not re.search(r"set(?:Timeout|Interval)\(\s*['\"]", code)
    assert not re.search(r"\bfetch\s*\(", code)                 # #74 has no network path at all


def test_the_reference_module_is_not_imported_by_any_formal_path():
    hits = []
    for path in sorted((UNIT_DIR / "hw2").glob("*.py")):
        if path.name == "explore_reference.py":
            continue
        if "explore_reference" in path.read_text(encoding="utf-8"):
            hits.append(path.name)
    notebook = (UNIT_DIR / "hw2.ipynb").read_text(encoding="utf-8")
    assert hits == [] and "explore_reference" not in notebook


def test_v2_files_are_on_the_page_and_parse():
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    assert '<link rel="stylesheet" href="assets/explore.css">' in html
    for rel in V2_FILES:
        assert (UNIT_DIR / rel).is_file(), rel
    node = shutil.which("node")
    if node is None:
        pytest.skip("node not installed")
    for rel in V2_SCRIPTS:
        subprocess.run([node, "--check", str(UNIT_DIR / rel)], check=True)
