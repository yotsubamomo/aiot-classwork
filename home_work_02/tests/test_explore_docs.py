"""README and report for the V2 Enhance (#78 V2-T5; Spec V2 「文件、README、報告與打包」; Brief V2 §7).

The checks read only tracked text: the unit README, the report template and the exploratory modules'
constants. They hold the documents to what the accepted contract and the Design Authority records ask
of them:

- the README states the load limit, the category-level cap, the per-method budgets, the split, the PI
  level and the URL timeout with the same numbers as the code (Spec V2: the numbers are implementation
  constants recorded in the README and ACCEPTANCE), the feature-count condition as >13 (DA B-8), and
  the two bonus rows of the requirement table;
- no README sentence makes the whole page the subject of "no outside request" any more (DA
  decision-20261022-r1f3-v1-footer R3-6): the zero-request statement names the views it holds for and
  the one GET of a submitted URL;
- README and the report's exploratory chapter disclose the limits the DA records allocate to #78
  (decision-20261022-issue77-resource-limits §6, decision-20261022-issue77-cancel-final-phase §4,
  decision-20261022-issue75-lasso-early-stop R4-5): cancellation at candidate / step boundaries, a
  single candidate may take minutes, no time promised, no file-size limit, very large files may fail;
  the Lasso stop for any early end, the true stop cause and the unit-free stop;
- the report's exploratory chapter is a new chapter before the appendices, carries a scope label, and
  every other part of the template is unchanged from the accepted baseline (#78 AC: 正式分析各章內容與數字不變).
  That the chapter holds no hand-typed number is checked by tests/test_report.py (unchanged).
"""
import re
import shutil
import subprocess

import pytest

from hw2.paths import ASSETS_DIR, UNIT_DIR

README = (UNIT_DIR / "README.md").read_text(encoding="utf-8")
TEMPLATE = (UNIT_DIR / "report" / "report.md").read_text(encoding="utf-8")
BASELINE = "d7f02d4179d2cb5c2ecf0c39a4643a6ef8287907"      # the accepted V2 baseline (OC §5)
CHAPTER = "## 12. 探索模式（加分功能）"


def _js_number(path, pattern):
    m = re.search(pattern, (ASSETS_DIR / path).read_text(encoding="utf-8"))
    assert m, (path, pattern)
    return float(m.group(1))


def _section(text, heading):
    start = text.index(heading)
    end = text.find("\n## ", start + len(heading))
    return text[start:] if end < 0 else text[start:end]


def _git(*args):
    return subprocess.run(["git", *args], cwd=UNIT_DIR, capture_output=True, check=False)


# ---- README ------------------------------------------------------------------------------------

def test_readme_constants_equal_the_code():
    rows = _section(README, "### 載入上限與運算預算（實作常數）")
    max_rows = _js_number("explore_load.js", r"maxRows:\s*(\d+)")
    max_cols = _js_number("explore_load.js", r"maxColumns:\s*(\d+)")
    min_rows = _js_number("explore_load.js", r"minRows:\s*(\d+)")
    timeout_ms = _js_number("explore_load.js", r"URL_TIMEOUT_MS\s*=\s*(\d+)")
    levels = _js_number("explore_engine.js", r"MAX_LEVELS\s*=\s*(\d+)")
    seed = _js_number("explore_engine.js", r"var SEED\s*=\s*(\d+)")
    test_fraction = _js_number("explore_engine.js", r"TEST_FRACTION\s*=\s*([\d.]+)")
    folds = _js_number("explore_engine.js", r"N_FOLDS\s*=\s*(\d+)")
    pi = _js_number("explore_engine.js", r"PI_LEVEL\s*=\s*([\d.]+)")
    budgets = re.search(r"BUDGETS\s*=\s*\{([^}]*)\}", (ASSETS_DIR / "explore_engine.js").read_text(encoding="utf-8"))
    budget = {k: float(v) for k, v in re.findall(r"(\w+):\s*([\d.e]+)", budgets.group(1))}
    assert f"{int(max_rows):,} 列 × {int(max_cols)} 欄" in rows
    assert f"至少 {int(min_rows)} 列" in rows
    assert f"| {int(levels)}（以訓練列計算" in rows
    assert f"seed {int(seed)}；test 占 {round(100 * test_fraction)}%；訓練列 {int(folds)} fold" in rows
    assert f"| {round(100 * pi)}% |" in rows
    assert f"| {round(timeout_ms / 1000)} 秒 |" in rows
    assert budget["forward_sfs"] == budget["backward_sfs"] == budget["rfe"]
    assert f"Forward SFS、Backward SFS、RFE 各 `{budget['rfe']:.0e}`".replace("e+", "e") in rows
    assert f"Lasso 路徑 `{budget['lasso_path']:.0e}`".replace("e+", "e") in rows


def test_readme_requirement_table_has_the_new_page_rows():
    table = _section(README, "## 作業要求對應")
    assert ">13 個特徵" in table and "10–20" not in README
    assert "| 加分：有下拉視窗呈現兩種 problem |" in table
    assert "| 加分：可任意輸入 Dataset" in table
    assert "HW2-req_new-20261021.txt" in table and "新版未載明" in table


def test_readme_names_the_views_that_send_no_request():
    for page_level in ("頁面不發出任何對外請求", "完全離線：`file://` 開啟、零對外請求", "Dashboard 只讀取匯出的結果",
                       "dashboard 只讀取追蹤的匯出結果"):
        assert page_level not in README, page_level
    dash = _section(README, "## Dashboard")
    assert "King County 與 50 Startups 的所有操作" in dash and "唯一的對外請求" in dash
    assert "一次 GET" in dash and "King County 檢視只讀取匯出的結果" in dash


@pytest.mark.parametrize("text", [README, TEMPLATE], ids=["README", "report"])
def test_exploratory_limits_are_disclosed(text):
    body = _section(text, "## 探索模式（加分功能）" if text is README else CHAPTER)
    for phrase in ("下一個候選邊界", "進行中的步驟完成時", "數分鐘", "不承諾任何執行時間", "沒有檔案大小上限",
                   "整份讀入瀏覽器的記憶體", "極大的檔案可能無法讀取", "逐列切分可能洩漏", "不代表正式研究結論",
                   "lasso_path_degenerate", "實際的停止原因", "均方根", "不改變進入順序、停止點與候選狀態",
                   "不是 Test 評估", "不讀取"):
        assert phrase in body, phrase


def test_readme_names_the_50_startups_source_and_licence():
    data = _section(README, "## 資料來源與授權")
    for phrase in ("Avik-Jain/100-Days-Of-ML-Code", "MIT License", "assets/data/50_Startups.LICENSE.md",
                   "c6075ca5a7551243b31193bad9228f0a1b9468cdde2475c6586c56dcfac5630d",
                   "不宣稱符合作業的 >13 特徵條件"):
        assert phrase in data, phrase


# ---- report ------------------------------------------------------------------------------------

def test_the_exploratory_chapter_is_labelled_and_precedes_the_appendices():
    heads = re.findall(r"^## (.+)$", TEMPLATE, re.M)
    chapter = next(h for h in heads if h.startswith(CHAPTER[3:]))
    assert "〔老師要求（新版作業頁的加分）〕" in chapter
    assert heads.index(chapter) == len(heads) - 3        # then Appendix A, Appendix B
    body = _section(TEMPLATE, CHAPTER)
    assert "不含任何探索結果的數字" in body and "第 7.1 節與第九章" in body
    assert "專案延伸（本專案的決定，不是老師的要求）" in body
    assert re.findall(r"\{\{([^{}]+)\}\}", body) == ["k_range"]


@pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")
def test_every_other_part_of_the_report_is_the_accepted_baseline():
    shown = _git("show", f"{BASELINE}:home_work_02/report/report.md")
    assert shown.returncode == 0, "the accepted baseline commit is not in this clone"
    base = shown.stdout.decode("utf-8").replace("\r\n", "\n")
    current = TEMPLATE.replace("\r\n", "\n")
    chapter = _section(current, CHAPTER)                  # up to the blank line before Appendix A
    assert chapter.endswith("\n") and current.count(chapter) == 1
    assert current.replace(chapter + "\n", "", 1) == base
