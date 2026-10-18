"""Report draft, unit README and ACCEPTANCE.md (#65).

Single source of numbers: the report template holds no hand-typed result number, every placeholder
resolves from the tracked exported results, every analysis figure is a file of results/figures/,
and every number of the README's results section equals the exported value. The checks read only
tracked exports (model_data.json and the result CSVs); nothing here fits or scores a model, and no
official test row is loaded."""
import copy
import json
import re

import pytest

from hw2 import report
from hw2.paths import FIGURES_DIR, UNIT_DIR

TEMPLATE = report.TEMPLATE.read_text(encoding="utf-8")
README = (UNIT_DIR / "README.md").read_text(encoding="utf-8")
ACCEPTANCE = (UNIT_DIR / "doc" / "acceptance" / "ACCEPTANCE.md").read_text(encoding="utf-8")
PHASES = ["Business Understanding", "Data Understanding", "Data Preparation", "Modeling",
          "Evaluation", "Deployment"]
_NUMBER = re.compile(r"(?<![A-Za-z_\d.\-])\d+(?:[.,]\d+)*")


@pytest.fixture(scope="module")
def md():
    return report.load_model_data()


@pytest.fixture(scope="module")
def tables():
    return report.load_tables()


@pytest.fixture(scope="module")
def rendered(md, tables):
    return report.render_markdown(md, tables)


def _prose(text: str) -> str:
    """The text a reader sees as prose: no placeholders, code spans, link targets or autolinks."""
    text = re.sub(r"\{\{[^{}]+\}\}", " ", text)
    text = re.sub(r"`[^`]*`", " ", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return re.sub(r"<https?://[^>]+>", " ", text)


# Structural references that are not results: notebook and report section numbers, source
# numbers of the comparison table, and the reading conventions of the formulas.
_STRUCTURAL = [
    r"^#+\s+\d+(?:\.\d+)*\.?\s",
    r"notebook\s+(?:第\s*)?\d+(?:\.\d+)*(?:\s*章)?(?:、\d+(?:\.\d+)*)*",
    r"第\s*\d+(?:\.\d+)*\s*[章節]",
    r"\[\d\]",
    r"GVIF\^\(1/\(2·df\)\)",
    r"√10",
]
# "1" appears only in unit readings and the PI formula ("增加 1 單位", "s²(1 + …)", "exp(b) − 1").
_ALLOWED_LITERALS = {"1"}


def test_template_has_no_hand_typed_result_numbers():
    found = []
    for n, line in enumerate(_prose(TEMPLATE).splitlines(), 1):
        for pattern in _STRUCTURAL:
            line = re.sub(pattern, " ", line)
        found += [(n, m.group()) for m in _NUMBER.finditer(line) if m.group() not in _ALLOWED_LITERALS]
    assert found == [], f"hand-typed numbers in report/report.md: {found}"


def test_every_placeholder_resolves_and_every_figure_is_a_results_file(rendered):
    text, info = rendered
    assert "{{" not in text and "}}" not in text
    assert set(info["figures"]) == set(report.FIGURES)
    assert set(report.FIGURES) == {p.name for p in FIGURES_DIR.glob("*.png")}, \
        "every figure of results/figures/ is cited by the report (DA TK-2)"
    assert set(info["shots"]) == set(report.SHOTS)
    assert sorted(info["pending"]) == ["chatgpt_pdf", "gpt", "notebooklm"]


def test_pending_slots_are_marked_and_hold_no_example_text(rendered, tmp_path):
    text, _ = rendered
    blocks = re.findall(r'<div class="pending" data-pending="(\w+)">(.*?)</div>', text, re.S)
    assert [k for k, _ in blocks] == ["gpt", "notebooklm", "chatgpt_pdf"]
    for _, body in blocks:
        assert "【待填" in body and "尚未" in body and "沒有任何" in body
    with pytest.raises(report.ReportError):
        report.build(out_dir=tmp_path, pdf=False, final=True)


def test_key_values_equal_the_exported_results(rendered, md):
    text, _ = rendered
    ov = md["winners"]["overall"]
    t = md["test"][ov["test_model_key"]]
    expected = [f"{t['rmse']:,.0f} USD", f"MAE {t['mae']:,.0f} USD", f"R² {t['r2']:.3f}",
                f"{100 * t['coverage']:.2f}%（{t['n_covered']:,}／{t['n_test']:,}）",
                f"{md['meta']['n_rows']:,} 列 × {md['meta']['n_columns']} 欄",
                md["meta"]["csv_sha256"], f"（{ov['cv_rmse']:,.0f} USD）"]
    for s in expected:
        assert s in text, s
    for key, entry in md["test"].items():
        assert f"{entry['rmse']:,.0f}" in text, key


def test_teacher_quotes_are_verbatim_from_the_requirement_transcripts(rendered):
    text, info = rendered
    src1 = report.REQUIREMENT_SOURCES["src1"].read_text(encoding="utf-8")
    assert "至 Kaggle 選擇一個具有 10 至 20 個特徵 (features) 的公開資料集。" in src1
    assert "> 至 Kaggle 選擇一個具有 10 至 20 個特徵 (features) 的公開資料集。" in text
    assert "> list kaggle multiple linear regression problems , choose features > 13, < 40" in text
    assert "> 呈現出Kaggle名次(若有)/預測結果評估(預測圖、評估指標)（10%）" in text
    assert report.feature_rule() == (14, 20)
    assert len(info["quotes"]) >= 8


def test_report_chapters_labels_and_required_statements(rendered):
    text, _ = rendered
    headings = re.findall(r"^## (.+)$", text, re.M)
    phase_heads = [h for h in headings if any(p in h for p in PHASES)]
    assert [next(p for p in PHASES if p in h) for h in phase_heads] == PHASES
    for h in phase_heads + [h for h in headings if re.match(r"\d+\. ", h)]:
        assert re.search(r"〔(老師要求|依老師補充建議|專案延伸)", h), h
    for title in ("GPT 輔助內容", "NotebookLM 摘要"):
        assert any(h.split(" 〔")[0].endswith(title) for h in headings), title
    for required in ("條件中位數", "不是條件平均", "樂觀偏誤", "獨立的估計", "不宣稱保證",
                     "Kaggle 名次」不適用", "預測結果評估", "二項近似假設各筆的涵蓋事件彼此獨立",
                     "非因果提醒", "課堂口頭"):
        assert required in text, required
    table = text.split("## 標示說明與對照表", 1)[1].split("## 1.", 1)[0]
    for item, label in (("Adjusted R²", "依老師補充建議"), ("五大回歸假設診斷", "依老師補充建議"),
                        ("Ridge／Lasso 對照", "依老師補充建議"), ("Permutation importance", "專案延伸"),
                        ("互動 dashboard", "老師要求（課堂口頭")):
        row = next(line for line in table.splitlines() if line.startswith(f"| {item}"))
        assert label in row, item
    assert "OC v2" not in text and "S-08" not in text and "表 A" not in text


def test_no_ridge_or_lasso_coefficients_in_the_report(rendered, tables):
    text, _ = rendered
    coef_table = text.split("| 欄位 | 係數（ln(price)）", 1)[1].split("\n\n", 1)[0]
    final_cols = {r["column"] for r in tables["final_model_coefficients"]}
    for col in re.findall(r"^\| `([^`]+)`", coef_table, re.M):
        assert col in final_cols
    assert not re.search(r"(Ridge|Lasso)\s*(的)?係數", text.replace("係數不匯出", ""))


def test_build_refuses_results_that_are_not_the_formal_evaluation(md, tables):
    tampered = copy.deepcopy(md)
    key = md["winners"]["overall"]["test_model_key"]
    tampered["test"][key]["rmse"] += 1.0
    with pytest.raises(report.ReportError, match="formal evaluation"):
        report.render_markdown(tampered, tables)
    fixture = copy.deepcopy(md)
    fixture["meta"]["fixture"] = True
    with pytest.raises(report.ReportError):
        report.render_markdown(fixture, tables)


def test_build_refuses_when_a_qualitative_statement_no_longer_holds(md, tables):
    t = copy.deepcopy(tables)
    t["permutation_importance_training"] = list(reversed(t["permutation_importance_training"]))
    with pytest.raises(report.ReportError, match="permutation"):
        report.render_markdown(md, t)
    m = copy.deepcopy(md)
    m["baselines"]["ridge"]["alpha_at_grid_edge"] = None
    with pytest.raises(report.ReportError, match="grid edge"):
        report.render_markdown(m, tables)


def test_external_sources_are_complete_and_cited():
    ext = json.loads(report.EXTERNAL_SOURCES.read_text(encoding="utf-8"))
    assert 3 <= len(ext["sources"]) <= 5
    for s in ext["sources"]:
        assert s["url"].startswith("https://"), s["id"]
        assert s["reported"] and all(r["locator"] and r["value"] for r in s["reported"]), s["id"]
        for field in ("title", "authors", "venue", "data", "target", "split", "method", "not_comparable"):
            assert s[field].strip(), (s["id"], field)


def test_markdown_to_html_subset():
    html = report.markdown_to_html(
        "## 標題 〔專案延伸〕\n\n段落 **粗體** `code` [連結](https://example.org)\n\n| a | b |\n| --- | --- |\n| 1 | 2 \\| 3 |\n\n"
        "- 項目\n  - 子項\n\n> 引文\n\n![圖](fig:x.png)\n",
        lambda kind, name: f"{kind}/{name}")
    assert '<span class="tag tag--project">專案延伸</span>' in html
    assert "<strong>粗體</strong>" in html and "<code>code</code>" in html
    assert '<a href="https://example.org">連結</a>' in html
    assert "<td>2 | 3</td>" in html and "<ul><li>子項</li></ul>" in html
    assert "<blockquote><p>引文</p></blockquote>" in html
    assert '<img src="fig/x.png" alt="圖">' in html


# --- README (Brief §8 Q39; DA F-4; N-5) ---------------------------------------------------------

def test_readme_has_every_required_item():
    heads = re.findall(r"^#{2,3} (.+)$", README, re.M)
    for required in ("目的", "資料來源與授權", "流程（CRISP-DM）", "成果", "Dashboard", "重跑步驟",
                     "學號設定（打包用）", "檔案配置"):
        assert any(h.startswith(required) for h in heads), required
    assert ".local/packaging.json" in README and "<學號>" in README
    assert "https://yotsubamomo.github.io/aiot-classwork/home_work_02/" in README
    assert "python -m hw2.report" in README
    for phase in PHASES:
        assert phase in README


def test_readme_states_the_one_formal_evaluation_and_reruns_as_reproduction():
    assert report.FORMAL_EVALUATION["run_id"] in README
    assert report.FORMAL_EVALUATION["result_digest"] in README
    assert "doc/governance/worklog/issue-63.md" in README
    assert "重現" in README and "不是新的評估" in README
    assert "第一次正式評估記錄的結果" not in README
    assert "含唯一一次的 Test 評估" not in README


def test_readme_results_numbers_equal_the_exports(md):
    results = README.split("## 成果", 1)[1].split("\n## ", 1)[0]
    ov = md["winners"]["overall"]
    t = md["test"][ov["test_model_key"]]
    winner = md["methods"][ov["method"]]
    k = next(e["k"] for e in winner if e["model_key"] == ov["model_key"])
    expected = {
        "n_test": f"{t['n_test']:,}", "rmse": f"{t['rmse']:,.0f}", "mae": f"{t['mae']:,.0f}",
        "r2": f"{t['r2']:.3f}", "coverage": f"{100 * t['coverage']:.2f}", "n_covered": f"{t['n_covered']:,}",
        "k": str(k), "pi": f"{100 * md['baselines']['allin']['fit']['pi_level']:.0f}",
    }
    for name, value in expected.items():
        assert value in results, name
    assert f"{report.METHOD_LABELS[ov['method']]} k = {k}" in results
    tokens = set(_NUMBER.findall(re.sub(r"`[^`]*`", " ", results)))
    assert tokens <= set(expected.values()), tokens - set(expected.values())
    data = README.split("## 資料來源與授權", 1)[1].split("\n## ", 1)[0]
    assert f"{md['meta']['n_rows']:,} 列 × {md['meta']['n_columns']} 欄" in data
    assert md["meta"]["csv_sha256"] in data


# --- ACCEPTANCE.md (Brief §8 Q41, §10; Spec 人工檢查表; DA §5, F-4, AD-1, AD-3) ------------------

def test_acceptance_covers_the_brief_spec_and_ov_items():
    for item in ("T-資料", "T-模型", "T-預測圖", "T-CRISP-DM：**notebook**", "T-CRISP-DM：**報告**",
                 "T-AI", "T-繳交", "T-GitHub", "T-評分", "主流或更優解法",
                 "Dashboard（課堂口頭要求）", "Adjusted R²", "五大回歸假設診斷", "預測新樣本與模型解釋",
                 "Ridge／Lasso 對照", "三種標示"):
        assert item in ACCEPTANCE, item
    for check in ("必要區塊", "zh-TW", "方法與 k 切換", "比較全部", "預測器", "未見 zipcode", "來源標示",
                  "提示", "`invalid`", "SR-09 (a)～(e)", "離線", "GitHub Pages", "章節完整", "三種標示",
                  "數字與匯出一致", "附錄 ChatGPT PDF", "NotebookLM 摘要字數", "來源連結可開啟",
                  "`git grep` 無實際學號", "acceptor 材料", "乾淨環境", "分欄"):
        assert check in ACCEPTANCE, check
    rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| (OV-\d) \|.*$", ACCEPTANCE, re.M)}
    assert sorted(rows) == [f"OV-{i}" for i in range(1, 7)]
    assert "硬性 PASS／FAIL gate" in rows["OV-1"] and "硬性 PASS／FAIL gate" in rows["OV-6"]
    for ov in ("OV-2", "OV-3", "OV-4", "OV-5"):
        assert "Required gate" in rows[ov], ov
    for ov in ("OV-2", "OV-3", "OV-4"):
        assert "best effort" in rows[ov] and "NOT TESTED" in rows[ov], ov
    assert "best-effort 項目沒有證據時一律記 NOT TESTED，不得標 PASS" in ACCEPTANCE.replace("Best-effort", "best-effort")
    assert "NOT TESTED（pending merge）" in ACCEPTANCE


def test_acceptance_marks_nothing_pass_before_it_is_verified():
    statuses = [row.rstrip("|").split("|")[-1].strip()
                for row in ACCEPTANCE.splitlines()
                if re.match(r"^\| (?:[A-E]-\d+|OV-\d) \|", row)]
    assert statuses and all(not s.startswith(("PASS", "FAIL")) for s in statuses), statuses


# --- section-level labels (R1 F-1, F-2) --------------------------------------------------------

def _headings(text):
    return [(n, line) for n, line in enumerate(text.splitlines()) if re.match(r"^#{2,4} ", line)]


def _section(text, prefix):
    lines = text.splitlines()
    start = next(n for n, line in enumerate(lines) if re.match(rf"^#{{2,4}} {re.escape(prefix)}", line))
    level = len(lines[start].split(" ", 1)[0])
    end = next((n for n in range(start + 1, len(lines))
                if re.match(r"^#{2,4} ", lines[n]) and len(lines[n].split(" ", 1)[0]) <= level), len(lines))
    return lines[start], "\n".join(lines[start:end])


@pytest.mark.parametrize("prefix", ["5.2 ", "6.4 ", "7.2 ", "7.3 "])
def test_adopted_supplement_sections_carry_the_supplement_label(prefix):
    heading, _ = _section(TEMPLATE, prefix)
    assert "〔依老師補充建議〕" in heading and "〔老師要求" not in heading, heading


def test_adjusted_r2_in_6_2_is_labelled_as_a_supplement():
    heading, body = _section(TEMPLATE, "6.2 ")
    assert "Adjusted R² 為依老師補充建議" in heading
    for line in body.splitlines():
        if "Adjusted R²" in line and not line.startswith(("#", "|", "{{")):
            assert "〔依老師補充建議〕" in line, line


@pytest.mark.parametrize("prefix", ["7.1 ", "9. "])
def test_dashboard_headings_say_classroom_oral_requirement(prefix):
    heading, _ = _section(TEMPLATE, prefix)
    assert "課堂口頭" in heading, heading


def test_every_supplement_quote_is_attributed_to_the_supplement():
    """No text of the assignment page's supplement is presented as a written requirement: each
    src2t quotation sits under a supplement-labelled heading or right after a sentence that names
    the supplement as its source (R1 F-1)."""
    lines = TEMPLATE.splitlines()
    for n, line in enumerate(lines):
        if "{{quote:src2t:" not in line:
            continue
        heading = next(lines[i] for i in range(n, -1, -1) if re.match(r"^#{2,4} ", lines[i]))
        before = next(lines[i] for i in range(n - 1, -1, -1)
                      if lines[i].strip() and not lines[i].lstrip().startswith(">"))
        assert "〔依老師補充建議〕" in heading or "「補充」段" in before or "補充段" in before, (n + 1, line)


def test_teacher_body_quotes_are_attributed_to_the_body():
    lines = TEMPLATE.splitlines()
    for n, line in enumerate(lines):
        if "{{quote:src1:" in line:
            before = next(lines[i] for i in range(n - 1, -1, -1)
                          if lines[i].strip() and not lines[i].lstrip().startswith(">"))
            assert "補充" not in before, (n + 1, before)


def test_readme_does_not_present_the_method_comparison_as_a_requirement():
    purpose = README.split("## 目的", 1)[1].split("\n## ", 1)[0]
    assert "依作業要求比較" not in purpose
    assert "依作業要求執行特徵選擇" in purpose and "補充" in purpose
