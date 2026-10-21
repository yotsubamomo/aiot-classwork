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
    assert scripts == ["assets/vendor/chart.umd.js", "assets/model_data.js", "assets/hw2core.js",
                       "assets/app.js", "assets/data/startups50.js", "assets/explore_load.js",
                       "assets/explore_engine.js", "assets/explore_plot.js", "assets/explore_app.js",
                       "assets/explore_ui.js"]
    assert all((UNIT_DIR / s).is_file() for s in scripts)
    assert 'lang="zh-Hant-TW"' in html


def test_bundled_chartjs_is_the_pinned_release():
    assert hashlib.sha256(CHARTJS.read_bytes()).hexdigest() == CHARTJS_SHA256
    assert CHARTJS.read_text(encoding="utf-8").startswith("/*!\n * Chart.js v4.4.1")
    assert (ASSETS_DIR / "vendor" / "chart.js.LICENSE.md").is_file()


@pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")
@pytest.mark.parametrize("script", ["assets/app.js", "assets/hw2core.js",
                                    "assets/model_data.js"])
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


# --- BR-01 / DA B-3, G-3: the UI never scores a model on test data ---------------------------

def _code(path):
    """Source without comments (block and line comments)."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$|(?<=[;{}])\s*//.*$", "", text)


def test_ui_predicts_only_from_user_inputs_and_never_from_test_inputs():
    app = _code(ASSETS_DIR / "app.js")
    calls = re.findall(r"Core\.predict\(([^)]*)\)", app)
    assert calls == ["entry.fit, read.raw, MD.preprocess"]
    assert "Core.encode(" not in app and "Core.rowObject(" not in app
    # test_inputs is read in one accessor (identifiers and actual prices for drawing) plus the
    # presence flag and the house / repeat-sale counts shown next to the coverage statistics.
    uses = re.findall(r"test_inputs(?:\.\w+)?", app)
    assert sorted(set(uses)) == ["test_inputs", "test_inputs.n_houses", "test_inputs.n_repeat_sales",
                                 "test_inputs.written"]
    assert app.count("var ti = MD.test_inputs;") == 1


def _function(app, name, next_name):
    return app[app.index(f"function {name}("):app.index(f"function {next_name}(")]


def test_k_chart_reads_training_cv_only_with_allin_ridge_lasso_reference_lines():
    """BR-01 point 1: the metric-vs-k chart uses `cv` only (paths, the All-in line and the Ridge /
    Lasso reference lines at their training-CV alpha), never `test`."""
    app = _code(ASSETS_DIR / "app.js")
    block = app[app.index("function renderKChart("):app.index("function renderCompare(")]
    assert "MD.test" not in block and "test_inputs" not in block and "testResult(" not in block
    assert "cvValue(" in block and "b.cv.mean" in block and "['ridge', 'lasso']" in block
    assert "e.cv.mean" in _function(app, "cvValue", "rgba")
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    for anchor in ('id="kchart-card"', 'id="compare-card"', 'id="compare-all"', 'id="metric-select"'):
        assert anchor in html, anchor
    chart_card = html[html.index('id="kchart-card"'):html.index('id="compare-card"')]
    assert "訓練 CV（USD）" in chart_card
    assert "Test" not in chart_card.replace("不含任何 Test 資料", "")


def test_comparison_table_separates_training_cv_and_test_columns():
    """G-4 / CC-1 (6): the comparison table has a 訓練 CV（USD） and a Test 評估（USD） column group;
    its Test cells are read only through testResult() from the exported `test`; Ridge / Lasso show
    不適用 for Adjusted R² and coverage; the p-value comparison is not scored."""
    app = _code(ASSETS_DIR / "app.js")
    block = _function(app, "renderCompare", "testResult")
    assert "'訓練 CV（USD）'" in block and "'Test 評估（USD）'" in block
    assert "th-group--cv" in block and "th-group--test" in block
    assert "MD.test" not in block and "test_inputs" not in block
    assert block.count("testResult(") == 2           # winners (ols_subset) and Ridge / Lasso
    assert "testResult(w.tKey, 'ols_subset')" in block and "testResult(name, 'metric_only')" in block
    assert "'不適用'" in block and "不適用（metric-only）" in block
    assert "不在 Test 上評估（講義對照）" in block
    accessor = _function(app, "testResult", "renderPredictor")
    assert "t.kind === kind" in accessor
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    compare_card = html[html.index('id="compare-card"'):html.index('id="fit-card"')]
    assert "訓練 CV（USD）" in compare_card and "Test 評估（USD）" in compare_card


def test_test_numbers_are_read_only_from_the_exported_test_section():
    """MD.test is read in exactly two places: the comparison-table accessor and the Test block,
    which shows only the method winner's ols_subset entry (Ridge / Lasso never; BR-01 point 4)."""
    app = _code(ASSETS_DIR / "app.js")
    reads = re.findall(r"MD\.test\[[^\]]+\]", app)
    assert sorted(reads) == ["MD.test[key]", "MD.test[tKey]"]
    block = _function(app, "renderTest", "Scatter")
    assert "MD.test[tKey]" in block and "Core.testEntryKey(MD, state.method)" in block
    assert "ridge" not in block and "lasso" not in block and "metric_only" not in block


def test_test_block_never_keeps_numbers_of_another_model():
    """#61 R1 F-3: without a test entry for the shown model, the Test body is hidden and emptied."""
    app = _code(ASSETS_DIR / "app.js")
    block = app[app.index("if (!tEntry) {"):app.index("var box = byId('kpi-test');")]
    for needle in ("byId('test-body').hidden = true", "byId('kpi-test').textContent = ''",
                   "byId('covstats').textContent = ''", "shownTestKey = null", "return;"):
        assert needle in block, needle


def test_dashboard_core_has_no_metric_coverage_or_selection_code():
    core = _code(ASSETS_DIR / "hw2core.js")
    for name in ("rmse", "mse", "mae", "coverage", "covered", "r2", "winner", "test_inputs.rows"):
        assert not re.search(rf"\b{name}\b", core, re.I), name


# --- #64: methods and limitations (block 9) and the optional coefficient table ---------------

def test_methods_and_limitations_has_four_paragraphs_with_the_three_labels():
    """Spec Dashboard block (9); UI checklist F: four paragraphs (feature selection methods, the
    training-CV / Test protocol, the PI's statistical assumptions, limits and non-causal reading),
    each with one of the three labels, all three labels used."""
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    section = html[html.index('<section class="section" id="methods"'):html.index("</main>")]
    articles = re.findall(r"<article.*?</article>", section, flags=re.S)
    assert len(articles) == 4
    titles = ["特徵選擇方法", "訓練 CV／Test 協定", "預測區間的統計假設", "限制與非因果解讀"]
    labels = {"tag--teacher": "老師要求", "tag--suggest": "依老師補充建議", "tag--project": "專案延伸"}
    used = set()
    for title, article in zip(titles, articles):
        heading = re.search(r"<h3[^>]*>(.*?)</h3>", article, flags=re.S).group(1)
        assert title in heading
        tags = re.findall(r'<span class="tag (tag--teacher|tag--suggest|tag--project)">([^<]+)</span>',
                          heading)
        assert len(tags) == 1, heading
        assert tags[0][1] == labels[tags[0][0]]
        used.add(tags[0][0])
    assert used == set(labels)
    for phrase in ("fold-internal selection", "不宣稱保證 95% 的經驗涵蓋率", "條件中位數",
                   "不是因果效果", "外推", "樂觀的選擇偏誤", "任何操作都不會觸發新的 Test 評估",
                   "不能證明或否定區間的 95% 涵蓋"):
        assert phrase in section, phrase
    assert '<a href="#methods">方法與限制</a>' in html
    assert "http" not in section                            # no URL of any kind in the block


def test_coefficient_table_is_optional_collapsed_and_labelled():
    """UI decision 5: the coefficient table is collapsed by default and labelled
    「全訓練集擬合，R²／Adjusted R² 為 log 尺度」; it reads only the selected model's fit."""
    html = DASHBOARD_HTML.read_text(encoding="utf-8")
    m = re.search(r'<details class="coef" id="coef-details"( open)?>(.*?)</details>', html, flags=re.S)
    assert m and m.group(1) is None                         # no `open` attribute: collapsed
    summary = re.search(r"<summary>(.*?)</summary>", m.group(2), flags=re.S).group(1)
    assert "係數表（選配）" in summary
    assert "全訓練集擬合，R²／Adjusted R² 為 log 尺度" in summary
    app = _code(ASSETS_DIR / "app.js")
    block = _function(app, "renderCoef", "renderMethods")
    assert "entry && entry.fit" in block and "f.xtx_inv[j][j]" in block
    for forbidden in ("MD.test", "test_inputs", "testResult(", "Core.predict("):
        assert forbidden not in block, forbidden
    assert "renderCoef(entry);" in _function(app, "update", "init")
    methods = _function(app, "renderMethods", "renderKChart")
    assert "MD.inputs" in methods and "MD.test" not in methods
