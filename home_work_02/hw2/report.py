"""Report build (#65): ``report/report.md`` (zh-TW Markdown with placeholders) -> Markdown, HTML and PDF.

Every number and table of this project's results is injected at build time from the tracked
exported results (``results/model_data.json`` and ``results/tables/*.csv``); every analysis figure
is a file of ``results/figures/``. The template holds no hand-typed result number (checked by
``tests/test_report.py``). Teacher quotations are copied verbatim from the requirement transcripts
in ``doc/requirement/``; the public solutions compared in the report come from
``report/external_sources.json`` (values reported by those sources, each with its locator).

The build refuses to run unless the exported test results are the one formal test evaluation
(DA §9.3 condition 2; ``decision-20261018-issue64-notebook-rerun.md`` N-1, N-5): the
``result_digest`` of ``test_inputs`` and ``test`` and the frozen selection digest must equal the
values recorded for that evaluation. Reading the exported results is not a test evaluation: no
model is fitted or scored here.

Placeholders of the template:

- ``{{name}}``: a value of :func:`build_context` (formatted text).
- ``{{table:name}}``: a Markdown table of :func:`build_tables`.
- ``{{quote:src1|src2t:fragment}}``: the requirement-transcript line that contains *fragment*
  (exactly one line must match); ``{{quote:src:fragment|n}}`` takes that line and the next n - 1.
- ``{{evidence:key}}``: a section built from the author's material (#66), read at build time from
  the untracked ``acceptor_materials/`` (never tracked, Brief §9): ``gpt`` (the ChatGPT part of
  「GPT 輔助內容」), ``notebooklm`` (「NotebookLM 摘要」 with its source list) and ``chatgpt_pdf``
  (the appendix that introduces the ChatGPT conversation PDF); ``status`` is the report-status
  line. A section whose material is missing is a clearly marked pending slot, never example text;
  the other sections build as usual.
- ``![caption](fig:file.png)``: a figure of ``results/figures/``.
- ``![caption](shot:name)``: a screenshot of the dashboard taken at build time from ``index.html``.

The author's material is checked against the sha256 recorded when it was received (a different file
stops the build). The two sections written from it by Claude Code (``acceptor_materials/derived/``,
untracked as well) are checked mechanically: the NotebookLM summary must have at least 100 Han
characters (DA B-15) and every sentence must appear, in order, in its trace table to the NotebookLM
report. A final build from the author's material (``--final``) also requires the derived sections
to be the reviewed versions (:data:`DERIVED_REVIEWED`, #66 R1 F-1). The PDF build appends the pages
of the ChatGPT conversation PDF unchanged after the report pages (:mod:`hw2.pdf_append`).

Usage (from ``home_work_02/``)::

    python -m hw2.report                 # dist/report/hw2_report.{md,html,pdf}
    python -m hw2.report --no-pdf        # Markdown and HTML only (no browser needed)
    python -m hw2.report --final         # fail while any acceptor-material section is still pending
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from . import pdf_append
from .paths import ACCEPTOR_MATERIALS_DIR, DIST_DIR, FIGURES_DIR, MODEL_DATA_JSON, TABLES_DIR, UNIT_DIR

REPORT_DIR = UNIT_DIR / "report"
TEMPLATE = REPORT_DIR / "report.md"
EXTERNAL_SOURCES = REPORT_DIR / "external_sources.json"
CAPTURE_SCRIPT = REPORT_DIR / "chrome_capture.js"
BUILD_DIR = DIST_DIR / "report"
REQUIREMENT_DIR = UNIT_DIR / "doc" / "requirement"
REQUIREMENT_SOURCES = {
    "src1": REQUIREMENT_DIR / "HW2-requirements-Multiple Linear regression.txt",
    "src2t": REQUIREMENT_DIR / "HW2-requirements-Multiple Linear regression_SRC-2_2026-10-18.txt",
}
DASHBOARD_URL = "https://yotsubamomo.github.io/aiot-classwork/home_work_02/"
REPO_URL = "https://github.com/yotsubamomo/aiot-classwork/tree/main/home_work_02"

# The one formal test evaluation (#63; authoritative record doc/governance/worklog/issue-63.md §5).
# A full notebook re-run reproduces it and must give the same result digest (bit-exact); the
# manifest inside model_data then records the re-run, not this evaluation (DA N-5).
FORMAL_EVALUATION = {
    "run_id": "fe76019b9af84b1e8ff46095d5ac0fb2",
    "result_digest": "b53ff286ae0734add8b272089aba904a1cb7f5aca444a62d356420b25dc3cfc6",
    "selection_digest": "44f7723e4023afc3e8e997f42bf4eb59db392af81cced11743757a9857cb4b28",
    "record": "doc/governance/worklog/issue-63.md §5",
}

METHOD_ORDER = ("forward_sfs", "backward_sfs", "rfe", "lasso_path")
METHOD_LABELS = {"allin": "All-in baseline", "forward_sfs": "Forward SFS",
                 "backward_sfs": "Backward SFS", "rfe": "RFE", "lasso_path": "Lasso 路徑排序",
                 "ridge": "Ridge", "lasso": "Lasso", "pvalue_backward": "p-value backward"}
FIGURES = ("eval_actual_vs_predicted_pi.png", "diag_linearity_residuals_vs_fitted.png",
           "diag_independence_residuals_by_date_and_repeat_sales.png",
           "diag_homoscedasticity_scale_location.png", "diag_normality_qq.png",
           "diag_multicollinearity_gvif.png", "explain_coefficients_percent_effects.png",
           "explain_permutation_importance.png")
SHOTS = ("overview", "model", "compare", "test", "methods")
PENDING = {
    "gpt": ("GPT 輔助內容（ChatGPT）",
            "本節依作業要求揭露 ChatGPT 的用途，內容取自作者本人的 ChatGPT "
            "對話匯出 PDF。材料尚未提供，本節尚未撰寫；這裡沒有任何範例或代擬文字。"),
    "notebooklm": ("NotebookLM 摘要",
                   "本節是作者以 NotebookLM 研究網路上同主題解法後的摘要（依作業要求的字數），"
                   "只整理、摘要或翻譯作者提供的原始輸出與來源清單，不新增內容或來源。"
                   "材料尚未提供，本節尚未撰寫；這裡沒有任何範例或代擬文字。"),
    "chatgpt_pdf": ("附錄 B：ChatGPT 對話 PDF",
                    "作者本人與 ChatGPT 的對話匯出 PDF 將原樣附於本報告最後（並放入繳交 ZIP）。"
                    "檔案尚未提供；這裡沒有任何替代內容。"),
}
LABEL_CLASSES = {"老師要求": "teacher", "依老師補充建議": "suggest", "專案延伸": "project"}

# --- the author's material (#66; Brief §9: untracked, provided by the author only) ---------------
# Files under acceptor_materials/ and the sha256 recorded when they were received (run record
# run-20261018-hw2-formal §17; doc/governance/worklog/issue-66.md). A different file stops the build.
ACCEPTOR_MATERIALS = {
    "chatgpt_pdf": ("ChatGPT_logs.pdf",
                    "0a5d29e30802270af6a7ff02b692e2bf26e808a5102c6b787adf1ee36a3ca194"),
    "notebooklm_report": ("notebooklm/notebooklm_report_v2_2026-10-19.docx",
                          "77b8f7e7841418e3187a76bede66b63ca0a284d4e91b6e317f9728feb47e4a96"),
    "notebooklm_sources": ("notebooklm/sources.md",
                           "141c211b8993e889b171eb34ecc524c85c44fe83aef962ad64a4a5cb557f5e2b"),
}
# Sections written from that material by Claude Code (#66); untracked like the material itself.
DERIVED = {"gpt": "derived/gpt_assist.md", "notebooklm": "derived/notebooklm_summary.md",
           "notebooklm_trace": "derived/notebooklm_trace.md"}
# sha256 of those sections as reviewed (#66 R1, doc/governance/audit/issue-66-c1-r1.md, subject
# table; #66 R1 F-1). The final build from the author's material refuses any other version: a
# changed section is a post-review delta and goes back to review first.
DERIVED_REVIEWED = {
    "gpt": "1a9663f750253d983934034b360acce91a85e11730ce4c25bf416f1cc8976023",
    "notebooklm": "358c78f2d3b735e437c10e365ef66b238a8d56bc01d39472a70b70687ac2731d",
    "notebooklm_trace": "5cae03568339075430c4e2d5eb9ad791ef955897a04adcc6c55849e30aeeb7b4",
}
EVIDENCE_NEEDS = {"gpt": ("chatgpt_pdf",), "notebooklm": ("notebooklm_report", "notebooklm_sources"),
                  "chatgpt_pdf": ("chatgpt_pdf",)}
NOTEBOOKLM_MIN_HANZI = 100        # assignment page "100 字以上", counted as Han characters (DA B-15)
_HAN = re.compile("[㐀-䶿一-鿿豈-﫿\U00020000-\U0002ebef\U00030000-\U0003134f]")
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_SENTENCE = re.compile(r"[^。！？\n]+[。！？]")
REPORT_STATUS = {
    "final": "**報告狀態：final。** 本報告的數字、表格與分析圖都在建置時（`python -m hw2.report`）"
             "從主程式 `hw2.ipynb` 匯出的結果（`results/model_data.json`、`results/tables/`、"
             "`results/figures/`）注入，沒有手抄數字。「GPT 輔助內容」的 ChatGPT 部分、「NotebookLM "
             "摘要」與附錄 B 的 ChatGPT 對話 PDF 取自作者本人提供的原始材料（材料不進 git）。",
    "draft": "**報告狀態：draft。** 本報告的數字、表格與分析圖都在建置時（`python -m hw2.report`）"
             "從主程式 `hw2.ipynb` 匯出的結果（`results/model_data.json`、`results/tables/`、"
             "`results/figures/`）注入，沒有手抄數字。「GPT 輔助內容」的 ChatGPT 部分、「NotebookLM "
             "摘要」與附錄 B 的 ChatGPT 對話 PDF 必須由作者本人提供原始材料；尚未提供的部分以【待填】"
             "標示，尚未撰寫。",
}

_PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")
_IMAGE = re.compile(r"!\[([^\]]*)\]\((fig|shot):([^)\s]+)\)")


class ReportError(RuntimeError):
    """The exported results or the template do not support the report."""


# --- loading ----------------------------------------------------------------------------------

def load_model_data(path: Path = MODEL_DATA_JSON) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def read_csv(name: str, tables_dir: Path = TABLES_DIR) -> list[dict]:
    with (Path(tables_dir) / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_tables(tables_dir: Path = TABLES_DIR) -> dict[str, list[dict]]:
    names = ("cv_by_method_k", "comparison", "alpha_cv", "diagnostics_summary",
             "diagnostics_vif_by_group", "diagnostics_vif_by_column", "final_model_coefficients",
             "permutation_importance_training")
    return {n: read_csv(f"{n}.csv", tables_dir) for n in names}


def check_formal_evaluation(md: dict) -> None:
    """The exported test results must be the one formal evaluation (DA §9.3 condition 2)."""
    from .export import result_digest
    digest = result_digest(md)
    manifest = md["meta"]["test_evaluation"]["manifest"]
    problems = []
    if md["meta"].get("fixture"):
        problems.append("model_data is a synthetic fixture")
    if digest != FORMAL_EVALUATION["result_digest"]:
        problems.append(f"result_digest {digest} != {FORMAL_EVALUATION['result_digest']}")
    if manifest["selection_digest"] != FORMAL_EVALUATION["selection_digest"]:
        problems.append("selection_digest differs from the formal evaluation")
    if not manifest.get("official_data"):
        problems.append("the evaluation did not use the official data")
    if problems:
        raise ReportError("the exported test results are not the formal evaluation: "
                          + "; ".join(problems) + " (stop and route to the Design Authority)")


# --- formatting -------------------------------------------------------------------------------

def f_int(v) -> str:
    return f"{int(round(float(v))):,}"


def f_usd(v) -> str:
    return f"{float(v):,.0f}"


def f_dec(v, n: int = 3) -> str:
    return f"{float(v):.{n}f}"


def f_pct(v, n: int = 1) -> str:
    return f"{100 * float(v):.{n}f}%"


def f_signed_pct(v, n: int = 1) -> str:
    return f"{float(v):+.{n}f}%"


def f_signed_pct_sig(v, n: int = 3) -> str:
    """Signed percentage with n significant digits (tiny per-unit effects stay readable)."""
    return f"{float(v):+.{n}g}%"


def f_p(v) -> str:
    if v in ("", None):
        return "—"
    p = float(v)
    if p == 0.0:
        return "< 1e-300"
    return f"{p:.3g}" if p >= 1e-3 else f"{p:.2e}"


def f_stat(v) -> str:
    x = float(v)
    if x.is_integer() and abs(x) >= 1:
        return f"{int(x):,}"
    if abs(x) >= 1000:
        return f"{x:,.0f}"
    if abs(x) >= 1:
        return f"{x:.3f}"
    return f"{x:.4f}"


def code(v) -> str:
    return f"`{v}`"


def code_list(items) -> str:
    return "、".join(code(i) for i in items)


def md_table(header: list[str], rows: list[list[str]]) -> str:
    def cell(c):
        return str(c).replace("|", "\\|").replace("\n", " ")
    lines = ["| " + " | ".join(cell(h) for h in header) + " |",
             "| " + " | ".join("---" for _ in header) + " |"]
    lines += ["| " + " | ".join(cell(c) for c in r) + " |" for r in rows]
    return "\n".join(lines)


# --- values -----------------------------------------------------------------------------------

def _model_label(method: str, k) -> str:
    return METHOD_LABELS[method] + ("" if method == "allin" else f" k = {k}")


def _entry(md: dict, model_key: str) -> dict:
    if model_key == "allin":
        return md["baselines"]["allin"]
    for method in METHOD_ORDER:
        for e in md["methods"][method]:
            if e["model_key"] == model_key:
                return e
    raise KeyError(model_key)


def shared_winners(md: dict) -> dict[str, list[str]]:
    """{test_model_key: [winner labels sharing that evaluated model]} (DA D-2)."""
    w = md["winners"]
    out: dict[str, list[str]] = {}
    out.setdefault(w["allin"]["test_model_key"], []).append(METHOD_LABELS["allin"])
    for method in METHOD_ORDER:
        mw = w["method_winners"][method]
        out.setdefault(mw["test_model_key"], []).append(_model_label(method, mw["k"]))
    return out


def build_context(md: dict, tables: dict[str, list[dict]]) -> dict[str, str]:
    meta, w, test = md["meta"], md["winners"], md["test"]
    ctx: dict[str, str] = {}
    ds = meta["dataset"]
    ctx.update(dataset_name=ds["name"], dataset_slug=code(ds["kaggle_slug"]), dataset_url=ds["url"],
               dataset_license=ds["license"], dataset_file=code(ds["file"]),
               csv_sha256=code(meta["csv_sha256"]), n_rows=f_int(meta["n_rows"]),
               n_columns=f_int(meta["n_columns"]), n_unique_ids=f_int(meta["n_unique_ids"]),
               n_repeat_full=f_int(meta["n_repeat_sales"]),
               n_source=f_int(meta["n_source_features"]), n_groups=f_int(meta["n_feature_groups"]),
               source_features=code_list(meta["source_features"]),
               feature_groups=code_list(meta["feature_groups"]), target=code(meta["target"]))
    excluded = md["preprocess"]["excluded_source_features"]
    ctx["excluded_features"] = code_list(e["name"] for e in excluded)
    tf = md["preprocess"]["training_fit"]
    ctx.update(n_zip_categories=f_int(len(tf["zipcode_categories"])),
               n_zip_onehot=f_int(len(tf["group_columns"]["zipcode"])),
               zip_baseline=code(tf["zipcode_baseline"]),
               n_encoded_columns=f_int(len(tf["encoded_columns"])),
               base_date=code(md["preprocess"]["date"]["base_date"]))
    sp, cv = meta["split"], meta["cv"]
    ctx.update(seed=code(meta["seed"]), test_pct=f"{100 * sp['test_fraction']:.0f}",
               train_pct=f"{100 * (1 - sp['test_fraction']):.0f}", n_train=f_int(sp["n_train"]),
               n_test=f_int(sp["n_test"]), n_train_houses=f_int(sp["n_train_houses"]),
               n_folds=f_int(cv["n_folds"]),
               fold_rows="、".join(f_int(r) for r in cv["fold_rows"]))
    ks = sorted({e["k"] for e in md["methods"][METHOD_ORDER[0]]})
    ctx.update(k_min=str(ks[0]), k_max=str(ks[-1]), k_range=f"{ks[0]}…{ks[-1]}",
               n_methods=f_int(len(METHOD_ORDER)))
    dr = md["inputs"]["date_range"]
    ctx.update(date_min=dr["min"], date_max=dr["max"])
    target = md["preprocess"]["target"]
    ctx.update(model_scale=code(target["model_scale"]), report_scale=target["report_scale"])
    allin = md["baselines"]["allin"]
    ctx.update(pi_level_pct=f"{100 * allin['fit']['pi_level']:.0f}%")
    # CV winners
    ov = w["overall"]
    ctx.update(overall_label=_model_label(ov["method"], _entry(md, ov["model_key"])["k"]),
               overall_cv_rmse=f_usd(ov["cv_rmse"]), overall_key=code(ov["model_key"]),
               overall_test_key=code(ov["test_model_key"]), allin_cv_rmse=f_usd(w["allin"]["cv_rmse"]),
               selection_metric=w["selection_metric"])
    for method in METHOD_ORDER:
        mw = w["method_winners"][method]
        ctx[f"winner_{method}"] = _model_label(method, mw["k"])
        ctx[f"winner_{method}_cv_rmse"] = f_usd(mw["cv_rmse"])
    overall_entry = _entry(md, ov["model_key"])
    ctx["overall_k"] = str(overall_entry["k"])
    ctx["overall_groups_dropped"] = code_list(
        g for g in meta["feature_groups"] if g not in overall_entry["canonical_groups"])
    ctx["overall_cv_rmse_std"] = f_usd(overall_entry["cv"]["std"]["rmse"])
    ctx["overall_cv_r2"] = f_dec(overall_entry["cv"]["mean"]["r2"])
    shared = shared_winners(md)
    ctx["shared_with_overall"] = "、".join(x for x in shared[ov["test_model_key"]] if x != ctx["overall_label"])
    authorized = w["authorized_test_models"]
    n_metric_only = sum(1 for v in test.values() if v["kind"] == "metric_only")
    ctx.update(n_authorized_ols=f_int(len(authorized)), n_metric_only=f_int(n_metric_only),
               n_evaluated_models=f_int(len(authorized) + n_metric_only),
               n_winners=f_int(1 + len(METHOD_ORDER)),
               authorized_keys=code_list(authorized))
    # test results
    for key, entry in test.items():
        p = f"test_{key}_"
        ctx.update({p + "rmse": f_usd(entry["rmse"]), p + "mae": f_usd(entry["mae"]),
                    p + "r2": f_dec(entry["r2"])})
        if entry["kind"] == "ols_subset":
            cu = entry["coverage_uncertainty"]
            ctx.update({p + "coverage": f_pct(entry["coverage"], 2), p + "n_covered": f_int(entry["n_covered"]),
                        p + "mean_width": f_usd(entry["mean_width"]),
                        p + "half_width": f_pct(cu["half_width_95"], 2),
                        p + "band_low": f_pct(cu["interval"][0], 2),
                        p + "band_high": f_pct(cu["interval"][1], 2),
                        p + "nominal_in_band": "落在" if cu["interval"][0] <= entry["pi_level"] <= cu["interval"][1] else "不落在"})
    tw = test[ov["test_model_key"]]
    ctx["overall_nominal_in_band"] = ctx[f"test_{ov['test_model_key']}_nominal_in_band"]
    low, high = feature_rule()
    if not low <= meta["n_source_features"] <= high:
        raise ReportError(f"{meta['n_source_features']} source features are outside {low}..{high}")
    ctx.update(feature_rule_low=str(low), feature_rule_high=str(high))
    gap = tw["rmse"] - ov["cv_rmse"]
    ctx.update(overall_test_rmse=f_usd(tw["rmse"]), overall_test_mae=f_usd(tw["mae"]),
               overall_test_r2=f_dec(tw["r2"]), overall_test_coverage=f_pct(tw["coverage"], 2),
               overall_test_n_covered=f_int(tw["n_covered"]),
               overall_test_mean_width=f_usd(tw["mean_width"]),
               overall_test_minus_cv=f_usd(gap),
               overall_gap_in_fold_sd=f"{gap / overall_entry['cv']['std']['rmse']:.2f}",
               overall_test_higher="高於" if gap > 0 else "低於")
    ti = md["test_inputs"]
    ctx.update(test_n_houses=f_int(ti["n_houses"]), test_n_repeat=f_int(ti["n_repeat_sales"]),
               test_n_unseen_zip=f_int(ti["n_unseen_zipcode"]))
    # Adjusted R² (OLS subsets, log scale, whole-training fit)
    wfit = _entry(md, ov["test_model_key"])["fit"]
    ctx.update(allin_r2_log=f_dec(allin["fit"]["r2_log"], 4), allin_adj_r2_log=f_dec(allin["fit"]["adj_r2_log"], 4),
               allin_rank=f_int(allin["fit"]["rank"]), allin_df_resid=f_int(allin["fit"]["df_resid"]),
               overall_r2_log=f_dec(wfit["r2_log"], 4), overall_adj_r2_log=f_dec(wfit["adj_r2_log"], 4),
               overall_rank=f_int(wfit["rank"]), overall_t_crit=f_dec(wfit["t_crit"], 4))
    # Ridge / Lasso (metric-only)
    for name in ("ridge", "lasso"):
        b = md["baselines"][name]
        grid = b["alpha_grid"]
        ctx.update({f"{name}_alpha": f"{b['alpha']:g}", f"{name}_grid_min": f"{min(grid):g}",
                    f"{name}_grid_max": f"{max(grid):g}", f"{name}_grid_n": f_int(len(grid)),
                    f"{name}_cv_rmse": f_usd(b["cv"]["mean"]["rmse"]),
                    f"{name}_edge": {"lower": "網格下緣（最小的 alpha）", "upper": "網格上緣（最大的 alpha）"}.get(
                        b.get("alpha_at_grid_edge"), "網格內部")})
    # p-value backward (lecture comparison)
    pv = md["baselines"]["pvalue_backward"]
    ctx.update(pvalue_threshold=f"{pv['threshold']:g}", pvalue_k=str(pv["k"]),
               pvalue_removed=code_list(s["removed"] for s in pv["elimination"]),
               pvalue_cv_rmse=f_usd(pv["cv"]["mean"]["rmse"]), pvalue_folds_agree=f_int(pv["folds_agree"]),
               pvalue_adj_r2_log=f_dec(pv["fit_summary"]["adj_r2_log"], 4))
    # diagnostics (training residuals of the final model)
    diag = {(r["assumption"], r["statistic"]): r for r in tables["diagnostics_summary"]}

    def dval(assumption, prefix):
        hits = [r for (a, s), r in diag.items() if a == assumption and s.startswith(prefix)]
        if len(hits) != 1:
            raise ReportError(f"diagnostics_summary.csv: expected one {assumption}/{prefix} row")
        return hits[0]

    reset = dval("linearity", "RESET")
    dw = dval("independence", "Durbin-Watson")
    rep = dval("independence", "repeat sales in the training set")
    rep_houses = dval("independence", "houses with repeat sales")
    corr = dval("independence", "residual correlation")
    bp = dval("homoscedasticity", "Breusch-Pagan (Koenker) LM on all")
    jb = dval("normality", "Jarque-Bera")
    kurt = dval("normality", "excess kurtosis")
    skew = dval("normality", "skewness")
    tail = dval("normality", "share |studentized residual| > 1.96")
    vif = dval("multicollinearity", "max column VIF")
    cond = dval("multicollinearity", "condition number of the correlation")
    ctx.update(reset_f=f_stat(reset["value"]), reset_p=f_p(reset["p_value"]),
               dw=f_dec(dw["value"]), train_repeat=f_int(rep["value"]),
               train_repeat_houses=f_int(rep_houses["value"]), repeat_corr=f_dec(corr["value"]),
               repeat_corr_p=f_p(corr["p_value"]), repeat_pairs=corr["detail"].split()[0],
               bp_lm=f_stat(bp["value"]), bp_p=f_p(bp["p_value"]), jb=f_stat(jb["value"]),
               jb_p=f_p(jb["p_value"]), kurtosis=f_dec(kurt["value"], 2), skewness=f_dec(skew["value"], 2),
               tail_share=f_pct(tail["value"], 2), max_vif=f_stat(vif["value"]), max_vif_column=code(vif["detail"]),
               cond_corr=f_stat(cond["value"]),
               n_violations=f_int(len({r["assumption"] for r in tables["diagnostics_summary"]
                                       if r["assumption_violated"] == "True"})),
               n_assumptions=f_int(len({r["assumption"] for r in tables["diagnostics_summary"]})))
    gvif = tables["diagnostics_vif_by_group"]
    high = [r["group"] for r in gvif if float(r["gvif_adjusted"]) > math.sqrt(10)]
    ctx["gvif_high_groups"] = code_list(high) if high else "（無）"
    # explanation (training only)
    perm = tables["permutation_importance_training"]
    ctx.update(perm_first=code(perm[0]["group"]), perm_second=code(perm[1]["group"]),
               perm_third=code(perm[2]["group"]), perm_n_repeats=f_int(perm[0]["n_repeats"]),
               perm_first_pct=f"{float(perm[0]['log_rmse_increase_pct_of_baseline']):.1f}%")
    coef = {r["column"]: r for r in tables["final_model_coefficients"]}
    for col in ("sqft_living", "grade", "waterfront"):
        if col in coef:
            ctx[f"coef_{col}_pct"] = f_signed_pct(coef[col]["pct_per_unit"], 2)
            if coef[col]["pct_per_train_sd"]:
                ctx[f"coef_{col}_pct_sd"] = f_signed_pct(coef[col]["pct_per_train_sd"], 2)
                ctx[f"coef_{col}_sd"] = f_stat(coef[col]["train_sd"])
    # timing and reproduction
    tm = meta["timing_s"]
    ctx.update({f"time_{m}": f"{tm['path_' + m]:.1f}" for m in METHOD_ORDER})
    ctx.update(versions="、".join(f"{k} {v}" for k, v in meta["versions"].items()),
               formal_run_id=code(FORMAL_EVALUATION["run_id"]),
               formal_result_digest=code(FORMAL_EVALUATION["result_digest"]),
               formal_selection_digest=code(FORMAL_EVALUATION["selection_digest"]),
               formal_record=code(FORMAL_EVALUATION["record"]),
               file_run_id=code(md["meta"]["test_evaluation"]["manifest"]["run_id"]),
               file_run_is_formal="是" if md["meta"]["test_evaluation"]["manifest"]["run_id"] == FORMAL_EVALUATION["run_id"]
               else "不是（是對同一評估的重現）",
               dashboard_url=DASHBOARD_URL, repo_url=REPO_URL)
    return ctx


# --- claims: qualitative sentences of the template, checked against the data ------------------

def check_claims(md: dict, tables: dict[str, list[dict]]) -> None:
    """Fail the build when a qualitative statement of the template no longer holds."""
    problems = []
    for name in ("ridge", "lasso"):
        rows = [r for r in tables["alpha_cv"] if r["model"] == name]
        rows.sort(key=lambda r: float(r["alpha"]))
        rmse = [float(r["cv_rmse_usd"]) for r in rows]
        if any(b < a for a, b in zip(rmse, rmse[1:])):
            problems.append(f"{name}: CV RMSE is not non-decreasing in alpha")
        if md["baselines"][name].get("alpha_at_grid_edge") != "lower":
            problems.append(f"{name}: the selected alpha is not at the lower grid edge")
        if md["baselines"][name]["cv"]["mean"]["rmse"] < md["baselines"]["allin"]["cv"]["mean"]["rmse"]:
            problems.append(f"{name}: CV RMSE below the All-in OLS")
    ov = md["winners"]["overall"]
    if md["test"][ov["test_model_key"]]["rmse"] <= ov["cv_rmse"]:
        problems.append("the overall winner's test RMSE is not above its CV RMSE")
    if tables["permutation_importance_training"][0]["group"] != "zipcode":
        problems.append("zipcode is not the first group of the permutation importance")
    violated = {r["assumption"] for r in tables["diagnostics_summary"] if r["assumption_violated"] == "True"}
    if len(violated) != 5:
        problems.append("not all five assumptions show a departure")
    if "no missing values" not in md["meta"]["structural_checks"]:
        problems.append("the structural checks do not include 'no missing values'")
    if any(e["status"]["state"] != "valid" for m in METHOD_ORDER for e in md["methods"][m]):
        problems.append("some (method, k) candidates are invalid")
    if problems:
        raise ReportError("the template's statements no longer match the results: " + "; ".join(problems))


# --- the author's material and the sections written from it (#66) -----------------------------

def count_hanzi(text: str) -> int:
    """Han characters only: punctuation, spaces, Latin letters and digits do not count (DA B-15)."""
    return len(_HAN.findall(text))


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass
class Evidence:
    """Report sections built from the author's material; a key missing from ``blocks`` is pending."""
    blocks: dict[str, str] = field(default_factory=dict)
    info: dict = field(default_factory=dict)
    chatgpt_pdf: bytes | None = None


def _read_materials(root: Path, pins: dict) -> dict[str, bytes]:
    """The material files that exist, by key; one whose sha256 differs from its receipt stops."""
    found = {}
    for key, (rel, expected) in pins.items():
        path = root / rel
        if not path.is_file():
            continue
        data = path.read_bytes()
        actual = sha256_hex(data)
        if actual != expected:
            raise ReportError(f"acceptor material {rel}: sha256 {actual} differs from the recorded receipt "
                              f"{expected} (stop and route to the acceptor)")
        found[key] = data
    return found


def check_derived_reviewed(materials_dir: Path = ACCEPTOR_MATERIALS_DIR,
                           pins: dict = DERIVED_REVIEWED) -> dict[str, str]:
    """The derived sections under ``materials_dir`` are the reviewed versions (sha256 by key)."""
    root = Path(materials_dir)
    found, problems = {}, []
    for key, rel in DERIVED.items():
        path = root / rel
        if not path.is_file():
            problems.append(f"{rel} is missing")
            continue
        found[key] = sha256_hex(path.read_bytes())
        if found[key] != pins[key]:
            problems.append(f"{rel}: sha256 {found[key]} differs from the reviewed {pins[key]}")
    if problems:
        raise ReportError("derived sections are not the reviewed versions: " + "; ".join(problems)
                          + " (stop and route the change to review before a final build)")
    return found


def _read_derived(path: Path) -> str | None:
    """A section written from the material, without its provenance comment; None when absent."""
    if not path.is_file():
        return None
    text = _COMMENT.sub("", path.read_text(encoding="utf-8")).strip()
    return text or None


def parse_notebooklm_summary(text: str) -> tuple[str, list[int], str]:
    """(report title, numbers of the sources the NotebookLM report cites, summary body)."""
    lines = text.splitlines()
    meta = {}
    while lines and re.match(r"^(title|cited-sources):", lines[0]):
        key, value = lines.pop(0).split(":", 1)
        meta[key] = value.strip()
    if not meta.get("title") or not meta.get("cited-sources"):
        raise ReportError("NotebookLM summary: the title and cited-sources lines are required")
    body = "\n".join(lines).strip()
    if not body:
        raise ReportError("NotebookLM summary: empty body")
    return meta["title"], [int(n) for n in meta["cited-sources"].split()], body


def summary_sentences(body: str) -> list[str]:
    """The sentences of the summary body; text that is not inside a complete sentence is an error."""
    sentences = [s.strip() for s in _SENTENCE.findall(body)]
    if re.sub(r"\s", "", "".join(sentences)) != re.sub(r"\s", "", body):
        raise ReportError("NotebookLM summary: text outside complete sentences (。！？)")
    return sentences


def check_notebooklm_trace(sentences: list[str], trace_text: str) -> int:
    """Every summary sentence appears, in order, in the trace table with a report location, the
    quoted basis and its source numbers (H-4, A-5). Returns the number of traced sentences."""
    rows = []
    for line in _COMMENT.sub("", trace_text).splitlines():
        m = re.match(r"^\| (N\d+) \| (.*) \|$", line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split(" | ")]
        if len(cells) != 4:
            raise ReportError(f"NotebookLM trace row {m.group(1)}: expected 5 cells")
        rows.append((m.group(1), *cells))
    traced = [r[1] for r in rows]
    if traced != sentences:
        missing = [n for n, s in enumerate(sentences, 1) if s not in traced]
        extra = [r[0] for r in rows if r[1] not in sentences]
        raise ReportError("NotebookLM summary and trace differ: sentences not traced "
                          f"{missing}, trace rows without a summary sentence {extra}, or order")
    empty = [r[0] for r in rows if not (r[2] and r[3] and r[4])]
    if empty:
        raise ReportError(f"NotebookLM trace rows without location, basis or source: {empty}")
    return len(rows)


def parse_sources(text: str) -> list[tuple[int, str, str]]:
    """(number, title and authors, URL) of every row of the author's NotebookLM source list."""
    rows = []
    for line in text.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|(.*)\|\s*$", line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        if len(cells) != 3 or not cells[2].startswith("https://"):
            raise ReportError(f"NotebookLM sources: malformed row {m.group(1)}")
        rows.append((int(m.group(1)), cells[1], cells[2]))
    if [r[0] for r in rows] != list(range(1, len(rows) + 1)):
        raise ReportError("NotebookLM sources: rows must be numbered 1..n")
    return rows


def _notebooklm_block(summary_text: str, trace_text: str, sources_text: str) -> tuple[str, dict]:
    title, cited, body = parse_notebooklm_summary(summary_text)
    sentences = summary_sentences(body)
    n_traced = check_notebooklm_trace(sentences, trace_text)
    hanzi = count_hanzi(body)
    if hanzi < NOTEBOOKLM_MIN_HANZI:
        raise ReportError(f"NotebookLM summary: {hanzi} Han characters (at least {NOTEBOOKLM_MIN_HANZI})")
    sources = parse_sources(sources_text)
    if not cited or any(n not in {s[0] for s in sources} for n in cited):
        raise ReportError("NotebookLM summary: cited-sources must be numbers of the source list")
    table = md_table(["#", "標題（作者）", "網址", "報告引用"],
                     [[str(n), t, f"<{u}>", "是" if n in cited else "—"] for n, t, u in sources])
    block = (f"**依 NotebookLM 研究整理。** 作者以 NotebookLM 研究網路上同主題的解法：筆記本收錄 "
             f"{len(sources)} 個來源（列於本節最後），NotebookLM 依此產生研究報告〈{title}〉，"
             f"該報告的文獻清單引用其中 {len(cited)} 個。以下摘要由 Claude Code 依該報告整理，只整理與"
             f"摘要，不新增該報告沒有的論點、數字或來源；摘要本文的漢字數為 {hanzi} 字（不含標點、空白、"
             f"拉丁字母與數字）。\n\n{body}\n\n**NotebookLM 筆記本的來源**（作者提供的來源清單；"
             f"「報告引用」標示該報告文獻清單引用的來源）：\n\n{table}")
    return block, {"notebooklm_hanzi": hanzi, "notebooklm_sentences": n_traced,
                   "notebooklm_sources": len(sources), "notebooklm_cited": cited}


def _pdf_date(value: str) -> str:
    m = re.match(r"D:(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})(\d{2})(?:([+-])(\d{2})'?(\d{2}))?", value)
    if not m:
        return value
    date = f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}:{m.group(5)}:{m.group(6)}"
    return date + (f" {m.group(7)}{m.group(8)}:{m.group(9)}" if m.group(7) else "")


def _chatgpt_block(data: bytes, name: str) -> tuple[str, dict]:
    pages = pdf_append.page_count(data)
    meta = pdf_append.document_info(data)
    lines = [f"- 檔案：`{name}`（{len(data):,} bytes，{pages} 頁）",
             f"- sha256：`{sha256_hex(data)}`（與收件紀錄相同）"]
    if meta.get("CreationDate") or meta.get("Producer"):
        lines.append(f"- PDF 建立時間：{_pdf_date(meta.get('CreationDate', '—'))}；"
                     f"產生方式（PDF Producer）：{meta.get('Producer', '—')}")
    block = (f"以下 {pages} 頁是作者本人與 ChatGPT 的對話匯出 PDF，原樣附於本報告的最後：沒有修改、"
             "刪減或重新排版，頁面上的頁首、頁尾與頁碼都是原 PDF 的內容。這段對話的用途見第十章。\n\n"
             + "\n".join(lines))
    return block, {"chatgpt_pdf_pages": pages, "chatgpt_pdf_sha256": sha256_hex(data)}


def load_evidence(materials_dir: Path = ACCEPTOR_MATERIALS_DIR, pins: dict = ACCEPTOR_MATERIALS) -> Evidence:
    """The report sections whose material is present under ``materials_dir`` (untracked)."""
    root = Path(materials_dir)
    found = _read_materials(root, pins)
    ev = Evidence()

    def have(key):
        return all(k in found for k in EVIDENCE_NEEDS[key])

    if have("gpt"):
        text = _read_derived(root / DERIVED["gpt"])
        if text:
            ev.blocks["gpt"] = text
    if have("notebooklm"):
        summary = _read_derived(root / DERIVED["notebooklm"])
        trace_path = root / DERIVED["notebooklm_trace"]
        if summary and trace_path.is_file():
            block, info = _notebooklm_block(summary, trace_path.read_text(encoding="utf-8"),
                                            found["notebooklm_sources"].decode("utf-8"))
            ev.blocks["notebooklm"] = block
            ev.info.update(info)
    if have("chatgpt_pdf"):
        block, info = _chatgpt_block(found["chatgpt_pdf"], Path(pins["chatgpt_pdf"][0]).name)
        ev.blocks["chatgpt_pdf"] = block
        ev.info.update(info)
        ev.chatgpt_pdf = found["chatgpt_pdf"]
    return ev


# --- tables -----------------------------------------------------------------------------------

def build_tables(md: dict, tables: dict[str, list[dict]]) -> dict[str, str]:
    out: dict[str, str] = {}
    # k path: CV RMSE (USD) of every method and k (training CV)
    rows = {}
    winners = {m: md["winners"]["method_winners"][m]["k"] for m in METHOD_ORDER}
    for r in tables["cv_by_method_k"]:
        if r["method"] == "allin":
            continue
        mark = " ★" if int(r["k"]) == winners[r["method"]] else ""
        if r["status"] != "valid":
            mark += f"（invalid：{r['reason']}）"
        rows.setdefault(int(r["k"]), {})[r["method"]] = f_usd(r["cv_rmse_usd"]) + mark
    out["kpath"] = md_table(["k"] + [f"{METHOD_LABELS[m]} 訓練 CV RMSE（USD）" for m in METHOD_ORDER],
                            [[str(k)] + [rows[k].get(m, "—") for m in METHOD_ORDER] for k in sorted(rows)])
    # comparison: training CV and test in separate columns (G-4); identities per winner (DA D-2)
    def num(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return None

    roles = {"All-in baseline": "All-in baseline", "method CV winner": "方法的 CV winner",
             "metric-only comparison": "metric-only 對照", "lecture comparison": "講義方法對照"}
    shared = shared_winners(md)
    overall = md["winners"]["overall"]["model_key"]
    comp = []
    for r in tables["comparison"]:
        if r["role"] not in roles:
            raise ReportError(f"comparison.csv: unknown role {r['role']!r}")
        method, label = r["method"], METHOD_LABELS[r["method"]]
        if method in METHOD_ORDER:
            label = _model_label(method, int(r["k"]))
        if method == "allin" or method in METHOD_ORDER:
            others = [x for x in shared[r["test_model_key"]] if x != label]
            note = ("整體 CV winner；" if r["model_key"] == overall else "") +                    (f"與 {'、'.join(others)} 為同一模型，Test 只評估一次" if others else "Test 評估一次")
        elif method in ("ridge", "lasso"):
            label = f"{label}（alpha {md['baselines'][method]['alpha']:g}）"
            note = "alpha 只以訓練 CV 選擇；不參與 CV winner；Test 只報 MAE、MSE、RMSE、R²"
        else:
            label = f"{label}（k = {r['k']}）"
            note = f"group partial F 檢定，門檻 {md['baselines']['pvalue_backward']['threshold']:g}；不參與 CV winner"
        tested = num(r["test_rmse_usd"]) is not None
        adj = num(r["adj_r2_log_full_training_fit"])
        cov = num(r["test_coverage"])
        comp.append([label, roles[r["role"]], f_usd(r["cv_rmse_usd"]), f_usd(r["cv_rmse_std_usd"]),
                     f_dec(r["cv_r2_usd_scale"]), f_dec(adj, 4) if adj is not None else "不適用",
                     f_usd(r["test_rmse_usd"]) if tested else "不在 Test 上評估",
                     f_usd(r["test_mae_usd"]) if tested else "—",
                     f_dec(r["test_r2_usd_scale"]) if tested else "—",
                     f_pct(cov, 2) if cov is not None else ("不適用" if tested else "—"), note])
    out["comparison"] = md_table(
        ["模型", "角色", "訓練 CV RMSE（USD）", "訓練 CV RMSE 各折標準差", "訓練 CV R²（USD）",
         "Adjusted R²（log，全訓練集擬合）", "Test RMSE（USD）", "Test MAE（USD）", "Test R²（USD）",
         "Test 預測區間涵蓋率", "備註"], comp)
    # alpha CV summary (Ridge / Lasso)
    arows = []
    for name in ("ridge", "lasso"):
        b = md["baselines"][name]
        sel = [r for r in tables["alpha_cv"] if r["model"] == name and r["selected"] == "True"]
        grid = [float(r["alpha"]) for r in tables["alpha_cv"] if r["model"] == name]
        arows.append([METHOD_LABELS[name], f"{min(grid):g} ～ {max(grid):g}", f_int(len(grid)),
                      f"{float(sel[0]['alpha']):g}", f_usd(sel[0]["cv_rmse_usd"]),
                      {"lower": "下緣", "upper": "上緣"}.get(b.get("alpha_at_grid_edge"), "內部")])
    arows.append([METHOD_LABELS["allin"] + "（OLS，參考）", "—", "—", "—",
                  f_usd(md["baselines"]["allin"]["cv"]["mean"]["rmse"]), "—"])
    out["alpha"] = md_table(["模型", "alpha 網格", "網格點數", "選出的 alpha（訓練 CV）",
                             "訓練 CV RMSE（USD）", "位於網格"], arows)
    # p-value backward elimination steps
    pv = md["baselines"]["pvalue_backward"]
    out["pvalue"] = md_table(["步驟", "移除的 group", "partial F", "df", "p-value", "移除後的 k"],
                             [[str(i), code(s["removed"]), f_dec(s["f"]), f"{s['df_num']}, {s['df_den']}",
                               f_p(s["p_value"]), str(s["k_after"])] for i, s in enumerate(pv["elimination"], 1)])
    # interval validation (OLS subset models evaluated on the test set)
    irows = []
    shared = shared_winners(md)
    for key in md["winners"]["authorized_test_models"]:
        e = md["test"][key]
        cu = e["coverage_uncertainty"]
        irows.append(["、".join(shared[key]), f_int(e["n_test"]), f_int(e["n_covered"]), f_pct(e["coverage"], 2),
                      f"± {f_pct(cu['half_width_95'], 2)}（{f_pct(cu['interval'][0], 2)} ～ {f_pct(cu['interval'][1], 2)}）",
                      f_usd(e["mean_width"]), f_int(e["n_unseen_zipcode"])])
    out["interval"] = md_table(["Test 評估的模型（共用同一模型的 CV winner）", "n_test", "涵蓋筆數", "經驗涵蓋率",
                                "二項近似 ±1.96·√(p(1−p)/n)", "平均寬度（USD）", "未見 zipcode 筆數"], irows)
    # metric-only test rows (Ridge / Lasso): only in comparison tables (BR-01 point 4)
    out["metric_only"] = md_table(
        ["模型（metric-only）", "alpha（訓練 CV）", "Test RMSE（USD）", "Test MAE（USD）", "Test R²（USD）"],
        [[METHOD_LABELS[k], f"{v['alpha']:g}", f_usd(v["rmse"]), f_usd(v["mae"]), f_dec(v["r2"])]
         for k, v in md["test"].items() if v["kind"] == "metric_only"])
    # diagnostics summary
    zh = {"linearity": "線性", "independence": "誤差獨立", "homoscedasticity": "同質變異",
          "normality": "殘差常態", "multicollinearity": "多重共線性"}
    out["diagnostics"] = md_table(
        ["假設", "統計量", "數值", "p-value", "說明"],
        [[zh[r["assumption"]], _zh_statistic(r["statistic"]), f_stat(r["value"]), f_p(r["p_value"]),
          _zh_detail(r["detail"])] for r in tables["diagnostics_summary"]])
    out["gvif"] = md_table(
        ["feature group", "欄數", "GVIF", "GVIF^(1/(2·df))", "group 內最大 VIF"],
        [[code(r["group"]), r["n_columns"], f_stat(r["gvif"]), f_dec(r["gvif_adjusted"]),
          f_stat(r["within_group_max_vif"]) if r["within_group_max_vif"] else "—"]
         for r in sorted(tables["diagnostics_vif_by_group"], key=lambda r: -float(r["gvif_adjusted"]))])
    # coefficients of the final model (non-zipcode columns) and the zipcode summary
    crow = []
    for r in tables["final_model_coefficients"]:
        if r["kind"] == "intercept" or r["group"] == "zipcode":
            continue
        crow.append([code(r["column"]), f"{float(r['coef_log']):.3g}", f_p(r["p_value"]),
                     f_signed_pct_sig(r["pct_per_unit"]),
                     f"{f_signed_pct_sig(r['pct_per_unit_ci95_low'])} ～ {f_signed_pct_sig(r['pct_per_unit_ci95_high'])}",
                     f_stat(r["train_sd"]) if r["train_sd"] else "—",
                     f_signed_pct(r["pct_per_train_sd"], 2) if r["pct_per_train_sd"] else "—"])
    out["coefficients"] = md_table(
        ["欄位", "係數（ln(price)）", "p-value", "每增加 1 單位（%）", "95% 信賴區間（%）",
         "training 標準差 sd", "每增加 1 個 sd（%）"], crow)
    zip_pct = sorted(float(r["pct_per_unit"]) for r in tables["final_model_coefficients"] if r["group"] == "zipcode")
    zrow = [[f_int(len(zip_pct)), f_signed_pct(zip_pct[0], 1), f_signed_pct(statistics.median(zip_pct), 1),
             f_signed_pct(zip_pct[-1], 1)]]
    out["zipcode"] = md_table(["zipcode one-hot 欄數", "最小（相對基準）", "中位數", "最大"], zrow)
    out["permutation"] = md_table(
        ["名次", "feature group", "欄數", "重複次數", "ln(price) RMSE 增加（平均 ± 標準差）",
         "相對 baseline RMSE", "USD RMSE 增加（參考）"],
        [[r["rank"], code(r["group"]), r["n_columns"], r["n_repeats"],
          f"{float(r['log_rmse_increase_mean']):.4f} ± {float(r['log_rmse_increase_std']):.4f}",
          f"{float(r['log_rmse_increase_pct_of_baseline']):.1f}%", f_usd(r["usd_rmse_increase_mean_reference"])]
         for r in tables["permutation_importance_training"]])
    # timing (Q34)
    tm, pt = md["meta"]["timing_s"], md["meta"]["path_timing_s"]
    out["timing"] = md_table(["方法", "子集計算（5 折＋整個 training set，秒）", "k 路徑的 CV 與擬合（秒）", "合計（秒）"],
                             [[METHOD_LABELS[m], f"{pt[m]['selection']:.2f}", f"{pt[m]['evaluation']:.2f}",
                               f"{tm['path_' + m]:.2f}"] for m in METHOD_ORDER])
    out["versions"] = md_table(["套件", "版本"], [[k, v] for k, v in md["meta"]["versions"].items()])
    # public solutions (values reported by the sources)
    ext = json.loads(EXTERNAL_SOURCES.read_text(encoding="utf-8"))
    srows, notes = [], []
    for i, s in enumerate(ext["sources"], 1):
        reported = "；".join(f"{r['metric']}：{r['value']}（{r['locator']}）" for r in s["reported"])
        srows.append([f"[{i}]", f"{s['authors']}〈{s['title']}〉", s["target"], s["split"], s["method"], reported])
        notes.append(f"- **[{i}]** {s['authors']}，〈{s['title']}〉，{s['venue']}。<{s['url']}>（{s['kind']}；"
                     f"{ext['accessed']} 讀取）\n  - 資料：{s['data']}\n  - 不可比之處：{s['not_comparable']}\n"
                     f"  - 重點：{s['takeaway']}")
    out["sources"] = md_table(["#", "來源", "目標尺度", "切分", "方法", "來源自報的指標（位置）"], srows)
    out["source_notes"] = "\n".join(notes)
    return out


DIAG_STATISTICS = (
    ("RESET F", "RESET F 檢定（擬合值的平方、立方）"),
    ("max |binned mean residual|", "依擬合值分 20 箱的殘差平均，絕對值最大者"),
    ("Durbin-Watson", "Durbin–Watson（依交易日期排序）"),
    ("repeat sales in the training set", "training set 的重複交易筆數（列數 − 唯一 id 數）"),
    ("houses with repeat sales", "training set 中有重複交易的房屋數"),
    ("residual correlation of consecutive sales", "同一房屋相鄰兩次交易的殘差相關係數"),
    ("mean residual change", "同一房屋下一次交易的殘差平均變化"),
    ("repeat sales in the full data set", "全資料的重複交易筆數（背景；全資料層級）"),
    ("Breusch-Pagan (Koenker) LM on all", "Breusch–Pagan（Koenker）LM，全部模型欄位"),
    ("Breusch-Pagan (Koenker) LM on the fitted", "Breusch–Pagan（Koenker）LM，只對擬合值"),
    ("Jarque-Bera", "Jarque–Bera"),
    ("skewness", "偏態"),
    ("excess kurtosis", "超額峰態"),
    ("share |studentized residual| > 1.96", "studentized 殘差絕對值 > 1.96 的比例"),
    ("share |studentized residual| > 2.576", "studentized 殘差絕對值 > 2.576 的比例"),
    ("max column VIF", "各欄 VIF 的最大值"),
    ("condition number of the correlation", "相關矩陣的條件數"),
    ("condition number, unit-length design", "含截距、欄單位化設計矩陣的條件數（Belsley）"),
)


def _zh_statistic(name: str) -> str:
    for prefix, zh in DIAG_STATISTICS:
        if name.startswith(prefix):
            return zh
    return name


def _zh_detail(detail: str) -> str:
    out = detail.replace("log scale", "log 尺度").replace("rows", "列").replace("houses", "棟房屋")
    out = out.replace("pairs", "對").replace("unique id", "唯一 id").replace("reference", "參考值")
    out = out.replace("under normality", "（常態下）").replace("about", "約")
    return out


# --- rendering --------------------------------------------------------------------------------

def feature_rule() -> tuple[int, int]:
    """The intersection of the two feature-count conditions, parsed from the teacher's texts:
    the body ("10 至 20 個特徵") and the supplement ("features > 13, < 40", exclusive)."""
    body = re.search(r"具有\s*(\d+)\s*至\s*(\d+)\s*個特徵", REQUIREMENT_SOURCES["src1"].read_text(encoding="utf-8"))
    supp_text = REQUIREMENT_SOURCES["src2t"].read_text(encoding="utf-8")
    supp = re.search(r"choose features\s*>\s*(\d+),\s*<\s*(\d+)", " ".join(supp_text.split()))
    if not body or not supp:
        raise ReportError("the feature-count conditions were not found in the requirement transcripts")
    low = max(int(body.group(1)), int(supp.group(1)) + 1)
    high = min(int(body.group(2)), int(supp.group(2)) - 1)
    return low, high


def requirement_quote(spec: str) -> str:
    src, rest = spec.split(":", 1)
    fragment, _, count = rest.partition("|")
    n = int(count) if count else 1
    lines = REQUIREMENT_SOURCES[src].read_text(encoding="utf-8").splitlines()
    hits = [i for i, line in enumerate(lines) if fragment in line]
    if len(hits) != 1:
        raise ReportError(f"quote {spec!r}: {len(hits)} matching lines in {src}")
    return " ".join(line.strip() for line in lines[hits[0]:hits[0] + n])


def pending_block(key: str) -> str:
    title, text = PENDING[key]
    return f'<div class="pending" data-pending="{key}">\n\n**【待填：作者提供的材料】** {text}\n\n</div>'


def render_markdown(md: dict | None = None, tables: dict | None = None, template: str | None = None,
                    check: bool = True, evidence: Evidence | None = None) -> tuple[str, dict]:
    """Return (resolved Markdown, info) where info lists used placeholders, figures, shots, pending
    and the evidence sections built from the author's material."""
    md = load_model_data() if md is None else md
    tables = load_tables() if tables is None else tables
    template = TEMPLATE.read_text(encoding="utf-8") if template is None else template
    evidence = load_evidence() if evidence is None else evidence
    if check:
        check_formal_evaluation(md)
        check_claims(md, tables)
    ctx, tabs = build_context(md, tables), build_tables(md, tables)
    info = {"values": set(), "tables": set(), "quotes": [], "pending": [], "figures": [], "shots": [],
            "evidence": []}
    status = "final" if all(k in evidence.blocks for k in PENDING) else "draft"

    def sub(m):
        token = m.group(1).strip()
        if token.startswith("table:"):
            name = token[6:]
            if name not in tabs:
                raise ReportError(f"unknown table {name!r}")
            info["tables"].add(name)
            return tabs[name]
        if token.startswith("quote:"):
            info["quotes"].append(token[6:])
            return requirement_quote(token[6:])
        if token.startswith("evidence:"):
            key = token[9:]
            if key == "status":
                return REPORT_STATUS[status]
            if key not in PENDING:
                raise ReportError(f"unknown evidence section {key!r}")
            if key in evidence.blocks:
                info["evidence"].append(key)
                return evidence.blocks[key]
            info["pending"].append(key)
            return pending_block(key)
        if token not in ctx:
            raise ReportError(f"unknown value {token!r}")
        info["values"].add(token)
        return ctx[token]

    text = _PLACEHOLDER.sub(sub, template)
    for cap, kind, name in _IMAGE.findall(text):
        if kind == "fig":
            if not (FIGURES_DIR / name).is_file():
                raise ReportError(f"figure {name} is not in results/figures/")
            info["figures"].append(name)
        else:
            if name not in SHOTS:
                raise ReportError(f"unknown dashboard screenshot {name!r}")
            info["shots"].append(name)
    return text, info


_INLINE_CODE = re.compile(r"`([^`]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_AUTOLINK = re.compile(r"&lt;(https?://[^\s&]+)&gt;")
_LABEL = re.compile(r"〔(老師要求|依老師補充建議|專案延伸)([^〕]*)〕")


def _inline(text: str) -> str:
    parts = _INLINE_CODE.split(text)
    out = []
    for i, part in enumerate(parts):
        if i % 2:
            out.append(f"<code>{html.escape(part)}</code>")
            continue
        s = html.escape(part, quote=False)
        s = _BOLD.sub(r"<strong>\1</strong>", s)
        s = _LINK.sub(lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
        s = _AUTOLINK.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', s)
        s = _LABEL.sub(lambda m: f'<span class="tag tag--{LABEL_CLASSES[m.group(1)]}">{m.group(1)}{m.group(2)}</span>', s)
        out.append(s)
    return "".join(out)


def markdown_to_html(text: str, image_src) -> str:
    """A small Markdown subset: headings, paragraphs, lists (one nesting level), tables,
    blockquotes, raw HTML block lines, images on their own line, inline code/bold/links."""
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    def para(buf):
        if buf:
            out.append(f"<p>{_inline(' '.join(s.strip() for s in buf))}</p>")
            buf.clear()

    buf: list[str] = []
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            para(buf)
            i += 1
            continue
        h = re.match(r"^(#{1,4})\s+(.*)$", line)
        img = re.match(r"^!\[([^\]]*)\]\((fig|shot):([^)\s]+)\)\s*$", stripped)
        if h:
            para(buf)
            level = len(h.group(1))
            anchor = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", h.group(2)).strip("-").lower()
            out.append(f'<h{level} id="{anchor}">{_inline(h.group(2))}</h{level}>')
            i += 1
        elif img:
            para(buf)
            out.append(f'<figure><img src="{image_src(img.group(2), img.group(3))}" alt="{html.escape(img.group(1))}">'
                       f"<figcaption>{_inline(img.group(1))}</figcaption></figure>")
            i += 1
        elif stripped.startswith("<"):
            para(buf)
            out.append(stripped)
            i += 1
        elif stripped.startswith("|"):
            para(buf)
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [re.split(r"(?<!\\)\|", r.strip("|")) for r in rows]
            cells = [[c.strip().replace("\\|", "|") for c in r] for r in cells]
            head, body = cells[0], [r for r in cells[2:]]
            out.append('<table><thead><tr>' + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                       + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in body)
                       + "</tbody></table>")
        elif stripped.startswith(">"):
            para(buf)
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "".join(f"<p>{_inline(q)}</p>" for q in quote if q) + "</blockquote>")
        elif re.match(r"^(\d+\.|-)\s+", stripped):
            para(buf)
            ordered = bool(re.match(r"^\d+\.", stripped))
            items: list[list[str]] = []
            while i < len(lines) and lines[i].strip():
                cur = lines[i]
                m_top = re.match(r"^(\d+\.|-)\s+(.*)$", cur)
                m_sub = re.match(r"^\s{2,}-\s+(.*)$", cur)
                if m_sub and items:
                    items[-1].append(m_sub.group(1))
                elif m_top:
                    items.append([m_top.group(2)])
                elif items:
                    items[-1][0] += " " + cur.strip()
                i += 1
            tag = "ol" if ordered else "ul"
            html_items = []
            for it in items:
                sub = "".join(f"<li>{_inline(s)}</li>" for s in it[1:])
                html_items.append(f"<li>{_inline(it[0])}" + (f"<ul>{sub}</ul>" if sub else "") + "</li>")
            out.append(f"<{tag}>" + "".join(html_items) + f"</{tag}>")
        else:
            buf.append(line)
            i += 1
    para(buf)
    return "\n".join(out)


CSS = """
@page { size: A4; margin: 16mm 14mm 18mm 14mm; }
:root { color-scheme: light; }
body { font-family: "Microsoft JhengHei", "Noto Sans TC", "PingFang TC", "Heiti TC", sans-serif;
       font-size: 10.5pt; line-height: 1.6; color: #1f2328; background: #fff; margin: 0; }
h1 { font-size: 20pt; margin: 0 0 6pt; } h2 { font-size: 15pt; margin: 18pt 0 6pt; border-bottom: 1px solid #d0d7de; padding-bottom: 3pt; break-after: avoid; }
h3 { font-size: 12pt; margin: 12pt 0 4pt; break-after: avoid; } h4 { font-size: 11pt; margin: 10pt 0 4pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 8.5pt; break-inside: auto; }
th, td { border: 1px solid #d0d7de; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #f3f5f7; } tr { break-inside: avoid; }
code { font-family: Consolas, "Courier New", monospace; font-size: 0.92em; background: #f3f5f7; padding: 0 2pt; border-radius: 2pt; word-break: break-all; }
figure { margin: 8pt 0 12pt; text-align: center; break-inside: avoid; }
figure img { max-width: 100%; max-height: 210mm; border: 1px solid #d0d7de; }
figcaption { font-size: 9pt; color: #57606a; margin-top: 3pt; }
blockquote { margin: 6pt 0; padding: 4pt 10pt; border-left: 3pt solid #8c959f; background: #f6f8fa; color: #24292f; }
.pending { border: 2px dashed #bf8700; background: #fff8c5; padding: 2pt 10pt; margin: 8pt 0; }
.tag { display: inline-block; font-size: 8.5pt; font-weight: normal; padding: 0 5pt; border-radius: 8pt; margin-left: 4pt; vertical-align: middle; border: 1px solid; }
.tag--teacher { color: #0a3069; border-color: #54aeff; background: #ddf4ff; }
.tag--suggest { color: #4d2d00; border-color: #d4a72c; background: #fff8c5; }
.tag--project { color: #1a4d2e; border-color: #4ac26b; background: #dafbe1; }
a { color: #0969da; text-decoration: none; word-break: break-all; }
"""


def to_html(markdown_text: str, title: str, image_src) -> str:
    body = markdown_to_html(markdown_text, image_src)
    return ("<!doctype html>\n<html lang=\"zh-Hant-TW\">\n<head>\n<meta charset=\"utf-8\">\n"
            f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n</head>\n<body>\n{body}\n</body>\n</html>\n")


# --- browser steps (dashboard screenshots, PDF) ------------------------------------------------

def find_browser() -> str | None:
    env = os.environ.get("HW2_BROWSER")
    if env and Path(env).is_file():
        return env
    candidates = [Path(os.environ.get(v, "")) / rel for v in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA")
                  for rel in ("Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe")]
    for c in candidates:
        if str(c) and c.is_file():
            return str(c)
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge"):
        found = shutil.which(name)
        if found:
            return found
    return None


def run_capture(mode: str, browser: str, *args: str) -> dict:
    node = shutil.which("node")
    if not node:
        raise ReportError("Node.js (node) is required for the dashboard screenshots and the PDF")
    with tempfile.TemporaryDirectory(prefix="hw2-report-browser-") as profile:
        proc = subprocess.run([node, str(CAPTURE_SCRIPT), mode, browser, profile, *args],
                              capture_output=True, text=True, encoding="utf-8", timeout=300)
    if proc.returncode != 0:
        raise ReportError(f"{CAPTURE_SCRIPT.name} {mode} failed: {proc.stderr.strip() or proc.stdout.strip()}")
    return json.loads(proc.stdout.strip().splitlines()[-1])


# --- build ------------------------------------------------------------------------------------

def build(out_dir: Path = BUILD_DIR, pdf: bool = True, final: bool = False,
          evidence: Evidence | None = None) -> dict:
    if final and evidence is None:
        check_derived_reviewed()          # #66 R1 F-1: only the reviewed derived text is built
    evidence = load_evidence() if evidence is None else evidence
    text, info = render_markdown(evidence=evidence)
    if final and info["pending"]:
        raise ReportError("pending acceptor-material sections: " + ", ".join(info["pending"]))
    out_dir = Path(out_dir)
    (out_dir / "figures").mkdir(parents=True, exist_ok=True)
    (out_dir / "shots").mkdir(parents=True, exist_ok=True)
    for name in info["figures"]:
        shutil.copyfile(FIGURES_DIR / name, out_dir / "figures" / name)
    title = text.splitlines()[0].lstrip("# ").strip()
    (out_dir / "hw2_report.md").write_text(text, encoding="utf-8")
    html_text = to_html(text, title, lambda kind, name: f"{'figures' if kind == 'fig' else 'shots'}/"
                                                        f"{name if kind == 'fig' else name + '.png'}")
    html_path = out_dir / "hw2_report.html"
    html_path.write_text(html_text, encoding="utf-8")
    result = {"markdown": str(out_dir / "hw2_report.md"), "html": str(html_path), "pending": info["pending"],
              "evidence": info["evidence"], **evidence.info,
              "figures": info["figures"], "shots": info["shots"], "pdf": None}
    if pdf:
        browser = find_browser()
        if not browser:
            raise ReportError("no Chrome/Edge found (set HW2_BROWSER to the browser executable)")
        shots = run_capture("shots", browser, str(UNIT_DIR / "index.html"), str(out_dir / "shots"))
        missing = [s for s in info["shots"] if s not in shots["shots"]]
        if missing:
            raise ReportError(f"dashboard screenshots missing: {missing}")
        printed = run_capture("pdf", browser, str(html_path), str(out_dir / "hw2_report.pdf"))
        result.update(pdf=printed["pdf"], pdf_pages=printed.get("pages"), browser=shots["browser"],
                      external_requests=shots["external_requests"] + printed["external_requests"],
                      first_draw_ms=shots.get("first_draw_ms"))
        if result["external_requests"]:
            raise ReportError(f"non-file requests during the build: {result['external_requests']}")
        if evidence.chatgpt_pdf is not None:
            result.update(attach_chatgpt_appendix(Path(printed["pdf"]), evidence.chatgpt_pdf))
    return result


def attach_chatgpt_appendix(pdf_path: Path, chatgpt_pdf: bytes) -> dict:
    """Appendix B: append the pages of the author's ChatGPT PDF, unchanged, after the report pages."""
    report_pdf = Path(pdf_path).read_bytes()
    try:
        merged = pdf_append.append_pages(report_pdf, chatgpt_pdf)
        n_report = pdf_append.page_count(report_pdf)
        n_appendix = pdf_append.page_count(chatgpt_pdf)
        n_total = pdf_append.page_count(merged)
    except pdf_append.PdfError as exc:
        raise ReportError(f"cannot append the ChatGPT PDF: {exc}") from exc
    if n_total != n_report + n_appendix:
        raise ReportError(f"appending the ChatGPT PDF gave {n_total} pages, not {n_report} + {n_appendix}")
    Path(pdf_path).write_bytes(merged)
    return {"report_pages": n_report, "appendix_pages": n_appendix, "pdf_pages": n_total,
            "pdf_sha256": sha256_hex(merged)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=BUILD_DIR)
    parser.add_argument("--no-pdf", action="store_true", help="Markdown and HTML only")
    parser.add_argument("--final", action="store_true", help="fail while acceptor-material slots are pending")
    args = parser.parse_args(argv)
    try:
        result = build(args.out, pdf=not args.no_pdf, final=args.final)
    except ReportError as exc:
        print(f"report build failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["pending"]:
        print("draft: pending acceptor-material slots: " + ", ".join(result["pending"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
