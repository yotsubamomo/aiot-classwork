"""Report, unit README and ACCEPTANCE.md (#65), and the sections built from the author's material (#66).

Single source of numbers: the report template holds no hand-typed result number, every placeholder
resolves from the tracked exported results, every analysis figure is a file of results/figures/,
and every number of the README's results section equals the exported value. The checks read only
tracked exports (model_data.json and the result CSVs); nothing here fits or scores a model, and no
official test row is loaded.

The author's material (ChatGPT PDF, NotebookLM output and sources) is never tracked; the tests of
the evidence sections use synthetic material written to a temporary directory, so they do not
depend on whether the real material is present on this machine (one test checks it when it is)."""
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


NO_EVIDENCE = report.Evidence()          # the author's material is absent: every evidence section pending


@pytest.fixture(scope="module")
def rendered(md, tables):
    return report.render_markdown(md, tables, evidence=NO_EVIDENCE)


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
    assert "**報告狀態：draft。**" in text and "**報告狀態：final。**" not in text
    with pytest.raises(report.ReportError):
        report.build(out_dir=tmp_path, pdf=False, final=True, evidence=NO_EVIDENCE)


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
        report.render_markdown(tampered, tables, evidence=NO_EVIDENCE)
    fixture = copy.deepcopy(md)
    fixture["meta"]["fixture"] = True
    with pytest.raises(report.ReportError):
        report.render_markdown(fixture, tables, evidence=NO_EVIDENCE)


def test_build_refuses_when_a_qualitative_statement_no_longer_holds(md, tables):
    t = copy.deepcopy(tables)
    t["permutation_importance_training"] = list(reversed(t["permutation_importance_training"]))
    with pytest.raises(report.ReportError, match="permutation"):
        report.render_markdown(md, t, evidence=NO_EVIDENCE)
    m = copy.deepcopy(md)
    m["baselines"]["ridge"]["alpha_at_grid_edge"] = None
    with pytest.raises(report.ReportError, match="grid edge"):
        report.render_markdown(m, tables, evidence=NO_EVIDENCE)


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
    # AD-3 ran after the merge (DA decision-20261019-post-merge-ad3-readme.md P-1 T-1): no status column of
    # sections A-E or the OV rows may still carry the pre-merge placeholder (this covers D-12 and B-1;
    # the explanatory text of the status-rule table is not a status column).
    statuses = {m.group(1): m.group(0).rstrip().rstrip("|").split("|")[-1].strip()
                for m in re.finditer(r"^\| ((?:[A-E]-\d+|OV-\d)) \|.*$", ACCEPTANCE, re.M)}
    assert "B-1" in statuses and "D-12" in statuses
    for key, status in statuses.items():
        assert "pending merge" not in status, (key, status)


def test_acceptance_statuses_are_filled_with_evidence():
    """After #67 (the verification ticket) every row has a status: a PASS or FAIL names its evidence,
    nothing is left PENDING, and the subject the checks ran on is a commit. (Until #67 the rule was
    the reverse: nothing could be PASS before it was verified.)"""
    rows = {m.group(1): m.group(0) for m in re.finditer(r"^\| ((?:[A-E]-\d+|OV-\d)) \|.*$", ACCEPTANCE, re.M)}
    statuses = {k: row.rstrip().rstrip("|").split("|")[-1].strip() for k, row in rows.items()}
    assert len(statuses) >= 60
    for key, status in statuses.items():
        assert status.lstrip("*").startswith(("PASS", "FAIL", "NOT TESTED")), (key, status)
        assert "PENDING" not in status, key
        if status.lstrip("*").startswith(("PASS", "FAIL")):
            assert re.search(r"worklog|見 [A-E]-\d+|見 OV-\d|下表|pytest", status), (key, status)
    # D-12 is the post-merge GitHub Pages check (AD-3; DA decision-20261019-post-merge-ad3-readme.md
    # P-1 T-2..T-4): a PASS that names the AD-3 worklog, the full 40-hex SHA of the checked `main`
    # commit, and the github-pages deployment that commit triggered.
    d12 = statuses["D-12"]
    assert d12.startswith("**PASS**"), d12
    assert "doc/governance/worklog/20261019-ad3-pages-check.md" in d12, d12
    assert re.search(r"`main` @ `[0-9a-f]{40}`", d12), d12
    assert "github-pages" in d12, d12
    for ov, item in (("OV-2", "真實觸控裝置"), ("OV-3", "Safari"), ("OV-4", "螢幕閱讀器")):
        assert f"{item} **NOT TESTED**" in statuses[ov], ov
    assert re.search(r"核對的 subject（#67 填寫）：branch `home_work_02-regrill` @ `[0-9a-f]{40}`", ACCEPTANCE)
    assert "（#67 填寫） |" not in ACCEPTANCE          # the OV-6 measurement record is filled


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


# --- sections built from the author's material (#66; Brief §9; DA B-15; H-1, H-2, H-4) ----------

SYNTHETIC_SENTENCES = [
    "這是自動化測試使用的合成摘要第一句，內容只用來檢查報告建置的行為，不是任何真實研究的結論。",
    "第二句同樣是合成文字，用來確認每一句摘要都能在對照表中找到對應的位置與來源編號。",
    "第三句說明合成材料只寫在暫存目錄中，測試不讀取作者本人的對話紀錄或研究材料。",
    "第四句讓摘要的漢字數超過作業要求的一百字下限，並且以句號結尾。",
]


def _synthetic_pdf(n_pages: int) -> bytes:
    from test_pdf_append import make_pdf
    return make_pdf(n_pages, "synthetic chat")


def _write_material(root, *, sentences=SYNTHETIC_SENTENCES, traced=None, sources_ok=True,
                    parts=("chatgpt_pdf", "notebooklm_report", "notebooklm_sources", "gpt", "notebooklm")):
    """Synthetic material under root (a temporary directory) and the pins for its sha256."""
    files = {
        "chatgpt_pdf": _synthetic_pdf(3),
        "notebooklm_report": b"synthetic NotebookLM report (stands in for the .docx)",
        "notebooklm_sources": ("〔轉錄說明〕合成的來源清單。\n\n| # | 類型 | 標題（作者） | 網址 |\n| --- | --- | --- | --- |\n"
                               "| 1 | 網頁 | 合成來源一（作者甲） | https://example.org/one |\n"
                               "| 2 | 網頁 | 合成來源二（作者乙） | "
                               + ("https://example.org/two" if sources_ok else "not-a-url") + " |\n").encode("utf-8"),
    }
    pins = {}
    for key, (rel, _) in report.ACCEPTOR_MATERIALS.items():
        pins[key] = (rel, report.sha256_hex(files[key]))
        if key in parts:
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / rel).write_bytes(files[key])
    (root / "derived").mkdir(parents=True, exist_ok=True)
    if "gpt" in parts:
        (root / report.DERIVED["gpt"]).write_text(
            "<!-- provenance comment, not rendered -->\n合成的 ChatGPT 用途說明（測試用）。\n", encoding="utf-8")
    if "notebooklm" in parts:
        body = "\n\n".join(sentences)
        (root / report.DERIVED["notebooklm"]).write_text(
            f"<!-- provenance -->\ntitle: 合成研究報告\ncited-sources: 1\n\n{body}\n", encoding="utf-8")
        rows = "\n".join(f"| N{i:02d} | {s} | §{i}（合成） | 「合成依據」 | #1 |"
                         for i, s in enumerate(sentences if traced is None else traced, 1))
        (root / report.DERIVED["notebooklm_trace"]).write_text(
            "<!-- trace -->\n\n| 句 | 摘要句 | 位置 | 依據 | 來源清單 |\n| --- | --- | --- | --- | --- |\n" + rows + "\n",
            encoding="utf-8")
    return pins


def test_count_hanzi_counts_han_characters_only():
    assert report.count_hanzi("漢字 abc 123，。、！？「」（）—…ＡＢ１") == 2
    assert report.count_hanzi("".join(SYNTHETIC_SENTENCES)) >= report.NOTEBOOKLM_MIN_HANZI


def test_evidence_sections_are_built_from_the_material(tmp_path, md, tables):
    pins = _write_material(tmp_path)
    ev = report.load_evidence(tmp_path, pins)
    text, info = report.render_markdown(md, tables, evidence=ev)
    assert info["pending"] == [] and info["evidence"] == ["gpt", "notebooklm", "chatgpt_pdf"]
    assert "**報告狀態：final。**" in text and "【待填" not in text
    _, gpt = _section(text, "10. GPT 輔助內容")
    assert "合成的 ChatGPT 用途說明（測試用）。" in gpt and "provenance" not in text
    assert "### 10.1 ChatGPT" in gpt and "### 10.2 Claude Code" in gpt
    _, nlm = _section(text, "11. NotebookLM 摘要")
    body = "\n\n".join(SYNTHETIC_SENTENCES)
    assert "**依 NotebookLM 研究整理。**" in nlm and body in nlm
    assert f"摘要本文的漢字數為 {report.count_hanzi(body)} 字" in nlm
    assert ev.info["notebooklm_sentences"] == len(SYNTHETIC_SENTENCES)
    assert "| 1 | 合成來源一（作者甲） | <https://example.org/one> | 是 |" in nlm
    assert "| 2 | 合成來源二（作者乙） | <https://example.org/two> | — |" in nlm
    _, appendix = _section(text, "附錄 B：ChatGPT 對話 PDF")
    assert pins["chatgpt_pdf"][1] in appendix and "以下 3 頁" in appendix and "原樣附於本報告的最後" in appendix
    assert ev.chatgpt_pdf is not None and ev.info["chatgpt_pdf_pages"] == 3
    result = report.build(out_dir=tmp_path / "out", pdf=False, final=True, evidence=ev)
    assert result["pending"] == [] and result["notebooklm_hanzi"] >= report.NOTEBOOKLM_MIN_HANZI


def test_appendix_b_is_the_last_section_so_the_pdf_pages_follow_it(rendered):
    text, _ = rendered
    headings = re.findall(r"^## (.+)$", text, re.M)
    assert headings[-2].startswith("附錄 A：重現資訊") and headings[-1].startswith("附錄 B：ChatGPT 對話 PDF")


def test_a_material_file_that_differs_from_its_receipt_stops_the_build(tmp_path):
    pins = _write_material(tmp_path)
    pins["notebooklm_sources"] = (pins["notebooklm_sources"][0], "0" * 64)
    with pytest.raises(report.ReportError, match="recorded receipt"):
        report.load_evidence(tmp_path, pins)


def test_missing_material_stops_only_its_own_section(tmp_path, md, tables):
    no_nlm = tmp_path / "a"
    pins = _write_material(no_nlm, parts=("chatgpt_pdf", "gpt"))
    _, info = report.render_markdown(md, tables, evidence=report.load_evidence(no_nlm, pins))
    assert info["pending"] == ["notebooklm"] and info["evidence"] == ["gpt", "chatgpt_pdf"]
    no_pdf = tmp_path / "b"
    pins = _write_material(no_pdf, parts=("notebooklm_report", "notebooklm_sources", "gpt", "notebooklm"))
    ev = report.load_evidence(no_pdf, pins)
    _, info = report.render_markdown(md, tables, evidence=ev)
    assert info["pending"] == ["gpt", "chatgpt_pdf"] and info["evidence"] == ["notebooklm"]
    assert ev.chatgpt_pdf is None
    no_summary = tmp_path / "c"
    pins = _write_material(no_summary, parts=("chatgpt_pdf", "notebooklm_report", "notebooklm_sources", "gpt"))
    _, info = report.render_markdown(md, tables, evidence=report.load_evidence(no_summary, pins))
    assert info["pending"] == ["notebooklm"]


def test_every_summary_sentence_must_be_traced_in_order(tmp_path):
    pins = _write_material(tmp_path / "a", traced=SYNTHETIC_SENTENCES[:-1])
    with pytest.raises(report.ReportError, match="not traced"):
        report.load_evidence(tmp_path / "a", pins)
    pins = _write_material(tmp_path / "b", traced=list(reversed(SYNTHETIC_SENTENCES)))
    with pytest.raises(report.ReportError, match="differ"):
        report.load_evidence(tmp_path / "b", pins)
    pins = _write_material(tmp_path / "c", sentences=SYNTHETIC_SENTENCES[:2] + ["沒有句號結尾的殘句"],
                           traced=SYNTHETIC_SENTENCES[:2])
    with pytest.raises(report.ReportError, match="outside complete sentences"):
        report.load_evidence(tmp_path / "c", pins)


def test_a_summary_below_one_hundred_han_characters_stops_the_build(tmp_path):
    short = ["只有幾個字的摘要。"]
    pins = _write_material(tmp_path, sentences=short, traced=short)
    with pytest.raises(report.ReportError, match="Han characters"):
        report.load_evidence(tmp_path, pins)


def test_a_trace_row_without_location_or_source_stops_the_build(tmp_path):
    pins = _write_material(tmp_path)
    trace = tmp_path / report.DERIVED["notebooklm_trace"]
    trace.write_text(trace.read_text(encoding="utf-8").replace("| #1 |", "|  |", 1), encoding="utf-8")
    with pytest.raises(report.ReportError, match="without location"):
        report.load_evidence(tmp_path, pins)


def test_a_malformed_source_list_stops_the_build(tmp_path):
    pins = _write_material(tmp_path, sources_ok=False)
    with pytest.raises(report.ReportError, match="sources"):
        report.load_evidence(tmp_path, pins)


def test_the_author_material_on_this_machine_when_present():
    """The real material is untracked; this runs only where the author has placed it (H-1)."""
    root = report.ACCEPTOR_MATERIALS_DIR
    if not all((root / rel).is_file() for rel, _ in report.ACCEPTOR_MATERIALS.values()):
        pytest.skip("the author's material is not on this machine (untracked, Brief §9)")
    ev = report.load_evidence()
    assert sorted(ev.blocks) == ["chatgpt_pdf", "gpt", "notebooklm"]
    assert ev.info["notebooklm_hanzi"] >= report.NOTEBOOKLM_MIN_HANZI
    assert ev.info["chatgpt_pdf_sha256"] == report.ACCEPTOR_MATERIALS["chatgpt_pdf"][1]


def test_a_final_build_refuses_derived_sections_other_than_the_reviewed_ones(tmp_path):
    """#66 R1 F-1: a changed derived section is a post-review delta; the final build stops."""
    _write_material(tmp_path)
    reviewed = report.check_derived_reviewed(tmp_path, pins={
        k: report.sha256_hex((tmp_path / rel).read_bytes()) for k, rel in report.DERIVED.items()})
    assert sorted(reviewed) == sorted(report.DERIVED)
    pins = dict(reviewed)
    (tmp_path / report.DERIVED["gpt"]).write_text("合成的 ChatGPT 用途說明（審查後被改動）。\n", encoding="utf-8")
    with pytest.raises(report.ReportError, match="reviewed"):
        report.check_derived_reviewed(tmp_path, pins)
    (tmp_path / report.DERIVED["notebooklm_trace"]).unlink()
    with pytest.raises(report.ReportError, match="missing"):
        report.check_derived_reviewed(tmp_path, pins)


def test_the_final_build_checks_the_reviewed_derived_sections(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(report, "check_derived_reviewed", lambda *a, **k: calls.append(1) or {})
    monkeypatch.setattr(report, "load_evidence", lambda *a, **k: report.Evidence())
    with pytest.raises(report.ReportError, match="pending"):
        report.build(out_dir=tmp_path, pdf=False, final=True)
    assert calls == [1]
    report.build(out_dir=tmp_path, pdf=False, final=False)
    assert calls == [1]                     # a draft build does not require the reviewed versions


def test_the_reviewed_derived_sections_on_this_machine_when_present():
    """The derived sections are untracked; this runs only where the author's material is (H-1, H-4)."""
    root = report.ACCEPTOR_MATERIALS_DIR
    if not all((root / rel).is_file() for rel in report.DERIVED.values()):
        pytest.skip("the derived sections are not on this machine (untracked, Brief §9)")
    assert report.check_derived_reviewed() == report.DERIVED_REVIEWED


def test_the_summary_threshold_is_one_hundred_han_characters(tmp_path):
    at_limit = ["字" * 99 + "。"]
    pins = _write_material(tmp_path / "a", sentences=at_limit, traced=at_limit)
    with pytest.raises(report.ReportError, match="99 Han characters"):
        report.load_evidence(tmp_path / "a", pins)
    enough = ["字" * 100 + "abc 123。"]
    pins = _write_material(tmp_path / "b", sentences=enough, traced=enough)
    assert report.load_evidence(tmp_path / "b", pins).info["notebooklm_hanzi"] == 100


def test_the_appendix_pages_follow_the_report_pages_unchanged(tmp_path):
    from test_pdf_append import _content, _pages_in_order, make_pdf
    pdf_path = tmp_path / "hw2_report.pdf"
    pdf_path.write_bytes(make_pdf(2, "report"))
    chat = make_pdf(3, "chat")
    result = report.attach_chatgpt_appendix(pdf_path, chat)
    assert (result["report_pages"], result["appendix_pages"], result["pdf_pages"]) == (2, 3, 5)
    merged = pdf_path.read_bytes()
    assert result["pdf_sha256"] == report.sha256_hex(merged)
    pages = _pages_in_order(merged)
    assert [_content(merged, n) for n in pages[2:]] == [_content(chat, n) for n in _pages_in_order(chat)]
    pdf_path.write_bytes(make_pdf(1, "report"))
    with pytest.raises(report.ReportError, match="cannot append"):
        report.attach_chatgpt_appendix(pdf_path, b"%PDF-1.4 broken")


def test_a_page_count_mismatch_after_appending_stops_the_build(tmp_path, monkeypatch):
    from test_pdf_append import make_pdf
    pdf_path = tmp_path / "hw2_report.pdf"
    pdf_path.write_bytes(make_pdf(2, "report"))
    monkeypatch.setattr(report.pdf_append, "append_pages", lambda base, extra: base)
    with pytest.raises(report.ReportError, match="pages"):
        report.attach_chatgpt_appendix(pdf_path, make_pdf(3, "chat"))
