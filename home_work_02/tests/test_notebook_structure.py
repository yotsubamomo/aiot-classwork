"""The main program's CRISP-DM structure (T-CRISP-DM; DA T-義務: six chapters, filled per ticket)."""
import json
import re

from hw2.paths import UNIT_DIR

NOTEBOOK = UNIT_DIR / "hw2.ipynb"
PHASES = ["Business Understanding", "Data Understanding", "Data Preparation",
          "Modeling", "Evaluation", "Deployment"]
FILLED = PHASES[:5]          # chapters with content at this stage (Deployment follows in #64)


def _cells():
    return json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]


def _chapters():
    """{phase: cells after its '## n. Phase' heading cell, up to the next chapter}."""
    chapters, current = {}, None
    for cell in _cells():
        source = "".join(cell["source"])
        heading = re.match(r"^## (\d)\. (.+)$", source.splitlines()[0]) if source else None
        if cell["cell_type"] == "markdown" and heading:
            current = heading.group(2).strip()
            chapters[current] = [source[len(source.splitlines()[0]):].strip()]
        elif current:
            chapters[current].append(source.strip())
    return chapters


def test_six_crisp_dm_chapters_in_order():
    headings = []
    for cell in _cells():
        first = "".join(cell["source"]).splitlines()[:1]
        if cell["cell_type"] == "markdown" and first and re.match(r"^## \d\. ", first[0]):
            headings.append(first[0])
    assert headings == [f"## {i}. {p}" for i, p in enumerate(PHASES, 1)]


def test_first_three_chapters_have_content_and_code():
    chapters = _chapters()
    for phase in FILLED:
        body = [c for c in chapters[phase] if c]
        assert len(body) >= 2, phase
    code_cells = {phase: 0 for phase in FILLED}
    current = None
    for cell in _cells():
        source = "".join(cell["source"])
        first = source.splitlines()[0] if source else ""
        match = re.match(r"^## \d\. (.+)$", first)
        if cell["cell_type"] == "markdown" and match:
            current = match.group(1)
        elif cell["cell_type"] == "code" and current in code_cells:
            code_cells[current] += 1
    assert all(n >= 1 for n in code_cells.values()), code_cells


def test_notebook_has_no_student_id_and_is_executed_without_errors():
    cells = _cells()
    text = NOTEBOOK.read_text(encoding="utf-8")
    assert "<學號>" in text                       # placeholder only (BR-03)
    for cell in cells:
        if cell["cell_type"] == "code":
            assert cell.get("execution_count") is not None
            assert all(o.get("output_type") != "error" for o in cell.get("outputs", []))


def test_evaluation_states_the_interval_assumptions_and_limits():
    """#61 AC (SR-12, DA TK-3, I-3): the notebook carries the report-draft wording."""
    text = "\n".join(_chapters()["Evaluation"])
    for phrase in ("不宣稱保證 95% 的經驗涵蓋率", "條件中位數", "不是條件平均", "二項近似",
                   "不陳述偏差的方向或幅度", "殘差常態、同質變異、彼此獨立", "樂觀偏誤"):
        assert phrase in text, phrase


def test_modeling_and_evaluation_state_the_selection_protocol_and_its_bias():
    """#62 AC (DA TK-3; Spec 「分割與交叉驗證」): fold-internal selection, canonical subset, the RFE
    group-importance rule, and the selection bias of the CV winner's CV score."""
    modeling = "\n".join(_chapters()["Modeling"])
    for phrase in ("fold-internal selection", "canonical subset", "Group 重要度的彙總規則",
                   "驗證列不參與任何子集的選擇", "平手", "canonical order"):
        assert phrase in modeling, phrase
    evaluation = "\n".join(_chapters()["Evaluation"])
    for phrase in ("選擇偏誤", "樂觀偏誤", "不是它表現的不偏估計", "Test 評估才是 CV winner 表現的獨立估計",
                   "同一模型只評估一次"):
        assert phrase in evaluation, phrase


def test_comparison_models_adjusted_r2_and_the_one_time_evaluation_are_stated():
    """#63 AC: Ridge/Lasso (training-CV alpha, metric-only), the p-value comparison, Adjusted R²
    only for OLS subsets, and the one-time Test evaluation with training-CV and Test kept apart."""
    modeling = "\n".join(_chapters()["Modeling"])
    for phrase in ("Ridge 與 Lasso", "alpha 只以 training CV 選", "metric-only", "不參與 CV winner",
                   "p-value backward", "group 層級的 partial F 檢定", "門檻 0.05", "不在 Test 上評估",
                   "fold-internal selection"):
        assert phrase in modeling, phrase
    evaluation = "\n".join(_chapters()["Evaluation"])
    for phrase in ("Adjusted R²", "只對 OLS 子集模型", "不適用", "唯一一次的 Test 評估",
                   "第二次呼叫會報錯", "Test 結果不回饋任何選擇", "訓練 CV（USD）", "Test 評估（USD）",
                   "Test 只評估一次"):
        assert phrase in evaluation, phrase


def test_the_executed_notebook_ran_the_test_evaluation_once():
    """G-3: one evaluate call scores; the only other call is the refused second call."""
    code = [c for c in _cells() if c["cell_type"] == "code"]
    calls = [c for c in code if "gate.evaluate(" in "".join(c["source"])]
    assert len(calls) == 2
    def text(cell):
        return "".join("".join(o["text"]) if isinstance(o.get("text"), list) else o.get("text", "")
                       for o in cell.get("outputs", []))
    assert "manifest:" in text(calls[0]) and "'evaluations_in_this_run': 1" in text(calls[0])
    assert "second evaluation refused: the test evaluation already ran in this run" in text(calls[1])
    assert sum("gate.open(" in "".join(c["source"]) for c in code) == 1
