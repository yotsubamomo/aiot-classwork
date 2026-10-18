"""Five regression-assumption diagnostics of the final model on the training residuals (log scale).

Spec rev 5 「診斷與解釋」; Brief §6 (Q9, Q19; 依老師補充建議): linearity, independence of the errors,
homoscedasticity, normality of the residuals and multicollinearity, each with numeric and graphic
evidence and a reading. A violation is disclosed and analysed, never a failure of the work.

- **Inputs: training rows only** (H-3; DA TR-01, I-1). :func:`run` takes the
  :class:`~hw2.data.PreparedData` of the data stage (training rows and test identifiers only) and
  the final model (:class:`hw2.deployment.PricePipeline`, itself fitted on the whole training
  set). Residuals are ``e = ln(price) − ŷ_log`` on those rows.
- **Statistics** (Brief §12 HOW: chosen by the implementation and stated here):

  1. *Linearity* — residuals vs fitted values with binned means; Ramsey's RESET F test (adding the
     squared and cubed standardized fitted values to the model).
  2. *Independence* — Durbin–Watson statistic of the residuals in sale-date order (ties: CSV row
     order); and the repeat sales of the training set (rows − unique ``id``, computed here, not
     written by hand): the Pearson correlation between the residuals of consecutive sales of the
     same house. The full data set's repeat sales are reported only as background, labelled as a
     full-data figure (DA TR-02).
  3. *Homoscedasticity* — scale–location plot (√|studentized residual| vs fitted, binned means);
     the Koenker (studentized) Breusch–Pagan LM test of e² on all model columns, and the same test
     on the fitted value only.
  4. *Normality* — normal Q–Q plot of the internally studentized residuals; Jarque–Bera test,
     skewness, excess kurtosis, and the share of |studentized residual| above 1.96 and 2.576
     (nominal 5% and 1% under normality).
  5. *Multicollinearity* — within each group: the largest column VIF computed among the group's
     own columns (groups with two or more columns); between groups: the generalized VIF of each
     group (Fox & Monette 1992) and GVIF^(1/(2·df)); every column's VIF in the full model; and the
     condition number of the correlation matrix of the model columns and of the unit-length
     scaled design with the intercept (Belsley). Conventional reference values: VIF 10,
     GVIF^(1/(2·df)) √10, condition number 30.

- **Classical OLS assumptions vs the PI's assumptions** (SR-08, SR-12): these checks concern the
  classical regression assumptions on the training residuals. They neither prove nor disprove
  the coverage of the parametric prediction interval: that interval additionally ignores the
  feature-selection step and possible misspecification, so its 95% is not guaranteed whatever
  these diagnostics show (Brief §6).
"""
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from . import data, deployment, ols, preprocess
from .paths import FIGURES_DIR, TABLES_DIR

ALPHA = 0.05
VIF_REFERENCE = 10.0
GVIF_ADJ_REFERENCE = float(np.sqrt(10.0))
CONDITION_REFERENCE = 30.0
N_BINS = 20
FIGURE_DPI = 110
FIGURE_FILES = {
    "linearity": "diag_linearity_residuals_vs_fitted.png",
    "independence": "diag_independence_residuals_by_date_and_repeat_sales.png",
    "homoscedasticity": "diag_homoscedasticity_scale_location.png",
    "normality": "diag_normality_qq.png",
    "multicollinearity": "diag_multicollinearity_gvif.png",
}
TABLE_FILES = {"summary": "diagnostics_summary.csv", "vif": "diagnostics_vif_by_group.csv",
               "column_vif": "diagnostics_vif_by_column.csv"}


class DiagnosticsError(ValueError):
    pass


def fmt_p(p: float) -> str:
    """'= 0.012' or '< 1e-300' (a p-value that underflows to 0 in double precision)."""
    return "< 1e-300" if p == 0 else f"= {p:.2g}"


@dataclass
class Diagnostics:
    """Results of :func:`run` (training rows only)."""
    model_label: str
    n_train: int
    residuals: pd.DataFrame            # row, id, date, sale_days, fitted, resid, leverage, studentized
    results: dict                      # assumption -> statistics and reading
    vif_by_group: pd.DataFrame
    vif_by_column: pd.DataFrame
    figures: dict = field(default_factory=dict)


def _design(pipeline, training: pd.DataFrame) -> np.ndarray:
    return ols.design(pipeline.preprocessor.transform(training).X)


def residual_frame(pipeline, training: pd.DataFrame) -> pd.DataFrame:
    """Fitted values, residuals, leverage and internally studentized residuals (log scale)."""
    D = _design(pipeline, training)
    fit = pipeline.fit
    y = np.log(training["price"].to_numpy(dtype=float))
    fitted = D @ fit.coef
    resid = y - fitted
    leverage = np.einsum("ij,jk,ik->i", D, fit.xtx_inv, D)
    studentized = resid / np.sqrt(fit.s2 * (1.0 - leverage))
    return pd.DataFrame({"row": training["row"].to_numpy(), "id": training["id"].to_numpy(),
                         "date": training["date"].to_numpy(),
                         "sale_days": preprocess.sale_days(training["date"]),
                         "fitted": fitted, "resid": resid, "leverage": leverage,
                         "studentized": studentized})


def _binned_means(x: np.ndarray, y: np.ndarray, n_bins: int = N_BINS) -> pd.DataFrame:
    """Means of y in equal-count bins of x (for the plots and the linearity reading)."""
    order = np.argsort(x, kind="stable")
    chunks = np.array_split(order, n_bins)
    return pd.DataFrame({"x_mean": [float(x[c].mean()) for c in chunks],
                         "y_mean": [float(y[c].mean()) for c in chunks],
                         "n": [int(c.size) for c in chunks]})


def linearity(res: pd.DataFrame, D: np.ndarray) -> dict:
    """Ramsey RESET: F test of adding z², z³ (z: standardized fitted values) to the model."""
    y = res["fitted"].to_numpy() + res["resid"].to_numpy()
    fitted = res["fitted"].to_numpy()
    z = (fitted - fitted.mean()) / fitted.std()
    X = D[:, 1:]
    names = [f"c{j}" for j in range(X.shape[1])]
    restricted = ols.fit_ols(X, y, names)
    unrestricted = ols.fit_ols(np.column_stack([X, z ** 2, z ** 3]), y, names + ["z2", "z3"])
    rss_r = restricted.s2 * restricted.df_resid
    rss_u = unrestricted.s2 * unrestricted.df_resid
    q = unrestricted.rank - restricted.rank
    f = ((rss_r - rss_u) / q) / (rss_u / unrestricted.df_resid)
    p = float(stats.f.sf(f, q, unrestricted.df_resid))
    bins = _binned_means(fitted, res["resid"].to_numpy())
    reading = ("RESET 檢定拒絕「線性函數形式足夠」（p < 0.05）：殘差中仍有擬合值的非線性成分"
               if p < ALPHA else "RESET 檢定未拒絕「線性函數形式足夠」（p ≥ 0.05）")
    return {"reset_f": float(f), "reset_df": [int(q), int(unrestricted.df_resid)],
            "reset_p_value": p,
            "binned_mean_resid_max_abs": float(np.abs(bins["y_mean"]).max()),
            "binned": bins, "violated": bool(p < ALPHA), "reading": reading}


def durbin_watson(resid: np.ndarray) -> float:
    resid = np.asarray(resid, dtype=float)
    return float(np.sum(np.diff(resid) ** 2) / np.sum(resid ** 2))


def repeat_sales(training: pd.DataFrame) -> dict:
    """Repeat sales in the given rows: rows − unique ``id`` and the houses involved."""
    counts = training["id"].value_counts()
    return {"n_rows": int(len(training)), "n_houses": int(counts.size),
            "n_repeat_sales": int(len(training) - counts.size),
            "n_houses_with_repeat_sales": int((counts >= 2).sum()),
            "n_rows_of_houses_with_repeat_sales": int(counts[counts >= 2].sum())}


def repeat_sale_pairs(res: pd.DataFrame) -> pd.DataFrame:
    """Consecutive sales of the same house (sale-date order, ties by CSV row): residual pairs."""
    ordered = res.sort_values(["id", "sale_days", "row"], kind="stable")
    same = ordered["id"].to_numpy()[1:] == ordered["id"].to_numpy()[:-1]
    first, second = ordered.iloc[:-1][same], ordered.iloc[1:][same]
    return pd.DataFrame({"id": first["id"].to_numpy(), "row_first": first["row"].to_numpy(),
                         "row_second": second["row"].to_numpy(),
                         "days_between": second["sale_days"].to_numpy()
                         - first["sale_days"].to_numpy(),
                         "resid_first": first["resid"].to_numpy(),
                         "resid_second": second["resid"].to_numpy()})


def independence(res: pd.DataFrame, training: pd.DataFrame, full_data_facts: dict) -> dict:
    by_date = res.sort_values(["sale_days", "row"], kind="stable")
    dw = durbin_watson(by_date["resid"].to_numpy())
    rs = repeat_sales(training)
    pairs = repeat_sale_pairs(res)
    if len(pairs) >= 3:
        r, p = stats.pearsonr(pairs["resid_first"], pairs["resid_second"])
        r, p = float(r), float(p)
    else:
        r, p = float("nan"), float("nan")
    correlated = bool(np.isfinite(p) and p < ALPHA and r > 0)
    mean_change = (float((pairs["resid_second"] - pairs["resid_first"]).mean())
                   if len(pairs) else float("nan"))
    reading = (f"依交易日期排序的 Durbin–Watson 為 {dw:.3f}（接近 2 表示相鄰殘差沒有明顯的一階自相關）。"
               f"training set 有 {rs['n_repeat_sales']} 筆重複交易（{rs['n_rows']} 列 − "
               f"{rs['n_houses']} 個唯一 id），涉及 {rs['n_houses_with_repeat_sales']} 棟房屋；"
               f"同一房屋相鄰兩次交易的殘差相關係數 r = {r:.3f}（{len(pairs)} 對"
               + (f"，p = {p:.2g}）" if np.isfinite(p) else "）")
               + ("：同一房屋的誤差正相關，這些列的誤差獨立假設不成立（揭露，不判失敗）。"
                  if correlated else "：沒有偵測到同一房屋誤差的正相關。")
               + (f"同一房屋後一次交易的殘差減前一次的平均為 {mean_change:+.3f}（log 尺度）。"
                  if np.isfinite(mean_change) else ""))
    return {"durbin_watson_by_date": dw, "repeat_sales_training": rs,
            "repeat_sale_pairs": int(len(pairs)), "pair_resid_corr": r,
            "pair_resid_corr_p_value": p, "pair_resid_mean_change": mean_change,
            "full_data_repeat_sales_background": {
                "level": "full data set (all rows, before the split); background only",
                "n_rows": full_data_facts.get("n_rows"),
                "n_unique_ids": full_data_facts.get("n_unique_ids"),
                "n_repeat_sales": full_data_facts.get("n_repeat_sales")},
            "pairs": pairs, "violated": correlated, "reading": reading}


def _lm_test(target: np.ndarray, X: np.ndarray) -> tuple[float, int, float]:
    """n·R² of regressing `target` on [1, X]; df = rank − 1; chi-square p-value."""
    fit = ols.fit_ols(X, target, [f"c{j}" for j in range(X.shape[1])])
    lm = len(target) * fit.r2
    df = fit.rank - 1
    return float(lm), int(df), float(stats.chi2.sf(lm, df))


def homoscedasticity(res: pd.DataFrame, D: np.ndarray) -> dict:
    """Koenker (studentized) Breusch–Pagan: e² on all model columns, and on the fitted value."""
    e2 = res["resid"].to_numpy() ** 2
    lm, df, p = _lm_test(e2, D[:, 1:])
    lm_f, df_f, p_f = _lm_test(e2, res["fitted"].to_numpy()[:, None])
    spread = _binned_means(res["fitted"].to_numpy(),
                           np.sqrt(np.abs(res["studentized"].to_numpy())))
    violated = bool(p < ALPHA)
    reading = ("Breusch–Pagan（Koenker）檢定拒絕同質變異（p < 0.05）：殘差的變異隨模型的欄位改變"
               if violated else "Breusch–Pagan（Koenker）檢定未拒絕同質變異（p ≥ 0.05）")
    return {"bp_lm": lm, "bp_df": df, "bp_p_value": p, "bp_fitted_lm": lm_f,
            "bp_fitted_df": df_f, "bp_fitted_p_value": p_f,
            "scale_location_binned_min": float(spread["y_mean"].min()),
            "scale_location_binned_max": float(spread["y_mean"].max()),
            "binned": spread, "violated": violated, "reading": reading}


def normality(res: pd.DataFrame) -> dict:
    e = res["resid"].to_numpy()
    r = res["studentized"].to_numpy()
    jb = stats.jarque_bera(e)
    skew, kurt = float(stats.skew(e)), float(stats.kurtosis(e))
    share_196 = float(np.mean(np.abs(r) > 1.96))
    share_2576 = float(np.mean(np.abs(r) > 2.576))
    violated = bool(jb.pvalue < ALPHA)
    reading = (f"Jarque–Bera 檢定{'拒絕' if violated else '未拒絕'}殘差常態（p "
               f"{'<' if violated else '≥'} 0.05）；偏態 {skew:.3f}、超額峰態 {kurt:.3f}；"
               f"|studentized 殘差| > 1.96 的比例 {100 * share_196:.2f}%（常態下約 5%）、"
               f"> 2.576 的比例 {100 * share_2576:.2f}%（常態下約 1%）。")
    return {"jarque_bera": float(jb.statistic), "jarque_bera_p_value": float(jb.pvalue),
            "skewness": skew, "excess_kurtosis": kurt,
            "share_abs_studentized_gt_1_96": share_196,
            "share_abs_studentized_gt_2_576": share_2576,
            "violated": violated, "reading": reading}


def multicollinearity(pipeline, training: pd.DataFrame) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    """Within-group VIF, between-group GVIF, column VIF and condition numbers."""
    X = pipeline.preprocessor.transform(training).X
    columns = list(pipeline.preprocessor.columns)
    owner = pipeline.preprocessor.group_of_column
    if np.any(X.std(axis=0) == 0):
        raise DiagnosticsError("a model column is constant on the training rows")
    R = np.corrcoef(X, rowvar=False)
    R_inv = np.linalg.inv(R)
    column_vif = np.diag(R_inv)
    _, logdet_all = np.linalg.slogdet(R)
    rows = []
    for g in pipeline.groups:
        idx = [j for j, c in enumerate(columns) if owner[c] == g]
        rest = [j for j in range(len(columns)) if j not in idx]
        _, logdet_g = np.linalg.slogdet(R[np.ix_(idx, idx)])
        _, logdet_rest = np.linalg.slogdet(R[np.ix_(rest, rest)]) if rest else (1.0, 0.0)
        gvif = float(np.exp(logdet_g + logdet_rest - logdet_all))
        within = (float(np.diag(np.linalg.inv(R[np.ix_(idx, idx)])).max())
                  if len(idx) >= 2 else None)
        rows.append({"group": g, "n_columns": len(idx), "gvif": gvif,
                     "gvif_adjusted": gvif ** (1.0 / (2 * len(idx))),
                     "max_column_vif_in_full_model": float(column_vif[idx].max()),
                     "within_group_max_vif": within})
    by_group = pd.DataFrame(rows)
    by_column = pd.DataFrame({"column": columns, "group": [owner[c] for c in columns],
                              "vif": column_vif})
    eig = np.linalg.eigvalsh(R)
    corr_condition = float(np.sqrt(eig.max() / eig.min()))
    D = ols.design(X)
    scaled = D / np.linalg.norm(D, axis=0)
    sv = np.linalg.svd(scaled, compute_uv=False)
    belsley = float(sv.max() / sv.min())
    high_groups = by_group.loc[by_group["gvif_adjusted"] > GVIF_ADJ_REFERENCE, "group"].tolist()
    high_columns = by_column.loc[(by_column["vif"] > VIF_REFERENCE)
                                 & ~by_column["column"].str.startswith(preprocess.ZIPCODE_PREFIX),
                                 "column"].tolist()
    within = by_group.dropna(subset=["within_group_max_vif"])
    violated = bool(high_groups or corr_condition > CONDITION_REFERENCE)
    numeric = [j for j, c in enumerate(columns) if not c.startswith(preprocess.ZIPCODE_PREFIX)]
    variation = {columns[j]: float(X[:, j].std() / abs(X[:, j].mean()))
                 for j in numeric if X[:, j].mean() != 0}
    least_varying = sorted(variation, key=variation.get)[:3]
    reading = (f"group 間：GVIF^(1/(2·df)) 超過 √10 的 group：{', '.join(high_groups) or '無'}；"
               f"欄位 VIF 超過 10 的非 zipcode 欄：{', '.join(high_columns) or '無'}。group 內："
               + ("；".join(f"{r.group} 最大 VIF {r.within_group_max_vif:.2f}"
                           for r in within.itertuples()) or "沒有多欄的 group")
               + f"。相關矩陣條件數 {corr_condition:.1f}（參考值 30）；含截距、欄位單位長度化的"
               f"設計矩陣條件數 {belsley:.0f}——含截距時，相對變異小（標準差遠小於平均）的欄位"
               f"（此模型中最小的是 {', '.join(least_varying)}）與截距近似共線而使它變大，"
               "主要影響截距與這些係數的精度，不影響預測值。")
    return ({"max_column_vif": float(column_vif.max()),
             "max_column_vif_column": columns[int(np.argmax(column_vif))],
             "groups_above_reference": high_groups, "columns_above_reference": high_columns,
             "correlation_condition_number": corr_condition,
             "belsley_condition_number_with_intercept": belsley,
             "violated": violated, "reading": reading}, by_group, by_column)


def run(prepared: data.PreparedData, pipeline) -> Diagnostics:
    """All five diagnostics of the final model on the training rows of `prepared`."""
    training = deployment.training_rows(prepared)
    if pipeline.n_train != len(training) or pipeline.data_sha256 != prepared.sha256:
        raise DiagnosticsError("the pipeline was not fitted on these training rows")
    res = residual_frame(pipeline, training)
    D = _design(pipeline, training)
    multi, by_group, by_column = multicollinearity(pipeline, training)
    results = {"linearity": linearity(res, D),
               "independence": independence(res, training, prepared.facts or {}),
               "homoscedasticity": homoscedasticity(res, D),
               "normality": normality(res),
               "multicollinearity": multi}
    return Diagnostics(model_label=pipeline.label, n_train=int(len(training)), residuals=res,
                       results=results, vif_by_group=by_group, vif_by_column=by_column)


SUMMARY_LABELS = {"linearity": "線性", "independence": "誤差獨立", "homoscedasticity": "同質變異",
                  "normality": "殘差常態", "multicollinearity": "多重共線性"}


def summary_rows(diag: Diagnostics) -> list:
    """One row per statistic (CSV ``diagnostics_summary.csv``)."""
    r = diag.results
    lin, ind, hom, nor, mul = (r["linearity"], r["independence"], r["homoscedasticity"],
                               r["normality"], r["multicollinearity"])
    rs = ind["repeat_sales_training"]
    bg = ind["full_data_repeat_sales_background"]
    rows = [
        ("linearity", "RESET F (z^2, z^3)", lin["reset_f"], lin["reset_p_value"],
         f"df = {lin['reset_df'][0]}, {lin['reset_df'][1]}"),
        ("linearity", "max |binned mean residual| (20 equal-count bins of fitted)",
         lin["binned_mean_resid_max_abs"], "", "log scale"),
        ("independence", "Durbin-Watson (sale-date order)", ind["durbin_watson_by_date"], "", ""),
        ("independence", "repeat sales in the training set (rows - unique id)",
         rs["n_repeat_sales"], "", f"{rs['n_rows']} rows, {rs['n_houses']} houses"),
        ("independence", "houses with repeat sales in the training set",
         rs["n_houses_with_repeat_sales"], "", f"{rs['n_rows_of_houses_with_repeat_sales']} rows"),
        ("independence", "residual correlation of consecutive sales of the same house",
         ind["pair_resid_corr"], ind["pair_resid_corr_p_value"],
         f"{ind['repeat_sale_pairs']} pairs"),
        ("independence", "mean residual change from a sale to the next sale of the same house",
         ind["pair_resid_mean_change"], "", "log scale"),
        ("independence", "repeat sales in the full data set (background; full-data level)",
         bg["n_repeat_sales"], "", f"{bg['n_rows']} rows - {bg['n_unique_ids']} unique id"),
        ("homoscedasticity", "Breusch-Pagan (Koenker) LM on all model columns", hom["bp_lm"],
         hom["bp_p_value"], f"df = {hom['bp_df']}"),
        ("homoscedasticity", "Breusch-Pagan (Koenker) LM on the fitted value",
         hom["bp_fitted_lm"], hom["bp_fitted_p_value"], f"df = {hom['bp_fitted_df']}"),
        ("normality", "Jarque-Bera", nor["jarque_bera"], nor["jarque_bera_p_value"], ""),
        ("normality", "skewness", nor["skewness"], "", ""),
        ("normality", "excess kurtosis", nor["excess_kurtosis"], "", ""),
        ("normality", "share |studentized residual| > 1.96", nor["share_abs_studentized_gt_1_96"],
         "", "about 0.05 under normality"),
        ("normality", "share |studentized residual| > 2.576",
         nor["share_abs_studentized_gt_2_576"], "", "about 0.01 under normality"),
        ("multicollinearity", "max column VIF", mul["max_column_vif"], "",
         mul["max_column_vif_column"]),
        ("multicollinearity", "condition number of the correlation matrix",
         mul["correlation_condition_number"], "", "reference 30"),
        ("multicollinearity", "condition number, unit-length design with intercept (Belsley)",
         mul["belsley_condition_number_with_intercept"], "", ""),
    ]
    return [{"assumption": a, "statistic": s, "value": v, "p_value": p, "detail": d,
             "assumption_violated": r[a]["violated"]} for a, s, v, p, d in rows]


def summary_table(diag: Diagnostics) -> pd.DataFrame:
    """Per assumption: the verdict (disclosed, never a failure) and the reading."""
    return pd.DataFrame([{"假設": SUMMARY_LABELS[a],
                          "結果": "違反（揭露，不判失敗）" if diag.results[a]["violated"] else "未偵測到違反",
                          "解讀": diag.results[a]["reading"]} for a in SUMMARY_LABELS])


def check_output_dir(out_dir: Path, official: bool) -> Path:
    """Only the official run writes inside the unit (fixture outputs never reach tracked paths)."""
    out_dir = Path(out_dir)
    if not official and deployment.is_inside_unit(out_dir):
        raise DiagnosticsError("non-official diagnostics must not be written inside the unit")
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def write_csv(path: Path, frame: pd.DataFrame) -> Path:
    frame = frame.copy()
    for c in frame.columns:
        if frame[c].dtype == float:
            frame[c] = [repr(float(v)) if pd.notna(v) else "" for v in frame[c]]
    frame.to_csv(path, index=False, lineterminator="\n", encoding="utf-8")
    return path


def write_tables(diag: Diagnostics, out_dir: Path = TABLES_DIR, official: bool = False) -> list:
    out_dir = check_output_dir(out_dir, official)
    rows = summary_rows(diag)
    for row in rows:              # counts stay integers; floats keep their full repr
        v = row["value"]
        row["value"] = str(v) if isinstance(v, (int, np.integer)) else repr(float(v))
        row["p_value"] = repr(float(row["p_value"])) if row["p_value"] != "" else ""
    summary = pd.DataFrame(rows)
    return [write_csv(out_dir / TABLE_FILES["summary"], summary),
            write_csv(out_dir / TABLE_FILES["vif"], diag.vif_by_group),
            write_csv(out_dir / TABLE_FILES["column_vif"], diag.vif_by_column)]


# --- figures (English labels: the PNGs are cited by the report; no CJK font dependency) ------

def new_figure(nrows: int = 1, ncols: int = 1, figsize=(8, 4.6), **subplot_kw):
    """A matplotlib Figure that pyplot does not manage (no backend or global state involved; the
    notebook shows it with display(), files are written with savefig)."""
    from matplotlib.figure import Figure
    fig = Figure(figsize=figsize, layout="constrained")
    return fig, fig.subplots(nrows, ncols, **subplot_kw)


def figures(diag: Diagnostics) -> dict:
    """The five diagnostic figures (matplotlib Figure objects)."""
    res = diag.residuals
    r = diag.results
    title = f"Final model: {diag.model_label.replace('Lasso 路徑排序', 'Lasso path ranking')}"
    out = {}

    fig, ax = new_figure(figsize=(8, 4.6))
    ax.scatter(res["fitted"], res["resid"], s=3, alpha=0.25, color="#1E40AF", rasterized=True,
               label="training rows")
    b = r["linearity"]["binned"]
    ax.plot(b["x_mean"], b["y_mean"], color="#C2410C", marker="o", ms=3, lw=1.6,
            label="mean residual in 20 equal-count bins")
    ax.axhline(0, color="#0F172A", lw=1, ls="--")
    ax.set_xlabel("fitted ln(price)")
    ax.set_ylabel("residual (log scale)")
    ax.set_title(f"Linearity: residuals vs fitted (training set)\n{title}; RESET p "
                 f"{fmt_p(r['linearity']['reset_p_value'])}", fontsize=10)
    ax.legend(fontsize=8)
    out["linearity"] = fig

    fig, axes = new_figure(1, 2, figsize=(11, 4.4))
    ordered = res.sort_values(["sale_days", "row"], kind="stable")
    axes[0].scatter(ordered["sale_days"], ordered["resid"], s=3, alpha=0.2, color="#1E40AF",
                    rasterized=True)
    month = pd.to_datetime(ordered["date"].str[:6], format="%Y%m")
    monthly = ordered.groupby(month.to_numpy())[["sale_days", "resid"]].mean()
    axes[0].plot(monthly["sale_days"], monthly["resid"], color="#C2410C", marker="o", ms=3,
                 label="monthly mean")
    axes[0].axhline(0, color="#0F172A", lw=1, ls="--")
    axes[0].set_xlabel(f"sale date (days since {preprocess.BASE_DATE.isoformat()})")
    axes[0].set_ylabel("residual (log scale)")
    axes[0].set_title(f"Residuals in sale-date order; Durbin-Watson "
                      f"{r['independence']['durbin_watson_by_date']:.3f}", fontsize=10)
    axes[0].legend(fontsize=8)
    pairs = r["independence"]["pairs"]
    axes[1].scatter(pairs["resid_first"], pairs["resid_second"], s=10, alpha=0.6,
                    color="#6D28D9")
    lim = float(np.nanmax(np.abs(pairs[["resid_first", "resid_second"]].to_numpy()))) * 1.05 \
        if len(pairs) else 1.0
    axes[1].plot([-lim, lim], [-lim, lim], color="#0F172A", lw=1, ls="--")
    axes[1].set_xlim(-lim, lim)
    axes[1].set_ylim(-lim, lim)
    axes[1].set_xlabel("residual of a sale")
    axes[1].set_ylabel("residual of the next sale of the same house")
    rs = r["independence"]["repeat_sales_training"]
    axes[1].set_title(f"Repeat sales in the training set: {rs['n_repeat_sales']} "
                      f"({len(pairs)} pairs); r = {r['independence']['pair_resid_corr']:.3f}",
                      fontsize=10)
    fig.suptitle(f"Independence of the errors (training set) - {title}", fontsize=10)
    out["independence"] = fig

    fig, ax = new_figure(figsize=(8, 4.6))
    ax.scatter(res["fitted"], np.sqrt(np.abs(res["studentized"])), s=3, alpha=0.25,
               color="#0E7490", rasterized=True, label="training rows")
    b = r["homoscedasticity"]["binned"]
    ax.plot(b["x_mean"], b["y_mean"], color="#C2410C", marker="o", ms=3, lw=1.6,
            label="mean in 20 equal-count bins")
    ax.set_xlabel("fitted ln(price)")
    ax.set_ylabel("sqrt(|studentized residual|)")
    ax.set_title(f"Homoscedasticity: scale-location (training set)\n{title}; Breusch-Pagan "
                 f"(Koenker) p {fmt_p(r['homoscedasticity']['bp_p_value'])}", fontsize=10)
    ax.legend(fontsize=8)
    out["homoscedasticity"] = fig

    fig, axes = new_figure(1, 2, figsize=(11, 4.4))
    s = np.sort(res["studentized"].to_numpy())
    n = s.size
    theo = stats.norm.ppf((np.arange(1, n + 1) - 0.5) / n)
    axes[0].scatter(theo, s, s=3, alpha=0.3, color="#1E40AF", rasterized=True)
    lim = max(abs(theo).max(), abs(s).max()) * 1.02
    axes[0].plot([-lim, lim], [-lim, lim], color="#C2410C", lw=1.2, label="y = x")
    axes[0].set_xlabel("standard normal quantile")
    axes[0].set_ylabel("studentized residual (sorted)")
    axes[0].set_title("Normal Q-Q plot", fontsize=10)
    axes[0].legend(fontsize=8)
    axes[1].hist(res["studentized"], bins=80, density=True, color="#93C5FD",
                 edgecolor="#1E40AF", lw=0.3)
    grid = np.linspace(-lim, lim, 400)
    axes[1].plot(grid, stats.norm.pdf(grid), color="#C2410C", lw=1.2, label="N(0, 1)")
    axes[1].set_xlabel("studentized residual")
    axes[1].set_title(f"Jarque-Bera p {fmt_p(r['normality']['jarque_bera_p_value'])}; skew "
                      f"{r['normality']['skewness']:.2f}, excess kurtosis "
                      f"{r['normality']['excess_kurtosis']:.2f}", fontsize=10)
    axes[1].legend(fontsize=8)
    fig.suptitle(f"Normality of the residuals (training set) - {title}", fontsize=10)
    out["normality"] = fig

    fig, ax = new_figure(figsize=(8, 4.8))
    g = diag.vif_by_group.sort_values("gvif_adjusted")
    colors = ["#B45309" if v > GVIF_ADJ_REFERENCE else "#1E40AF" for v in g["gvif_adjusted"]]
    labels = [f"{a} ({c} col)" if c > 1 else a for a, c in zip(g["group"], g["n_columns"])]
    ax.barh(labels, g["gvif_adjusted"], color=colors)
    ax.axvline(GVIF_ADJ_REFERENCE, color="#0F172A", ls="--", lw=1,
               label="reference sqrt(10) (VIF 10)")
    ax.set_xlabel("GVIF^(1/(2 df)) of the feature group (between groups)")
    ax.set_title(f"Multicollinearity (training set) - {title}\ncondition number of the "
                 f"correlation matrix {r['multicollinearity']['correlation_condition_number']:.1f}",
                 fontsize=10)
    ax.legend(fontsize=8)
    out["multicollinearity"] = fig
    diag.figures = out
    return out


def save_figures(figs: dict, out_dir: Path = FIGURES_DIR, official: bool = False,
                 names: dict = FIGURE_FILES) -> list:
    out_dir = check_output_dir(out_dir, official)
    paths = []
    for key, fig in figs.items():
        path = out_dir / names[key]
        fig.savefig(path, dpi=FIGURE_DPI, metadata={"Software": None})
        paths.append(path)
    return paths
