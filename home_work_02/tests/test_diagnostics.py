"""Five-assumption diagnostics and the model explanation of the final model (#64; Spec rev 5
「診斷與解釋」; H-3: training rows only).

Every statistic is checked against a direct computation, and the inputs are shown to come only from
the training rows: changing every feature and price of the test rows leaves every diagnostic, the
coefficient table and the permutation importance unchanged (the functions receive the data stage's
training rows, which hold no test feature or price). Synthetic data, plus the real training rows for
the official outputs; no test row is used (DA TR-01)."""
import dataclasses

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from hw2 import data, deployment, diagnostics, explain, fixture, ols
from hw2.paths import FIGURES_DIR, TABLES_DIR
from test_deployment import _load, small_selection


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    """The same synthetic sales twice: as generated, and with every test row's features and price
    changed (and an unseen zipcode). The training rows are identical."""
    frame = fixture.synthetic_sales(n_houses=900, n_repeats=40, seed=13)
    tmp = tmp_path_factory.mktemp("diag")
    path = tmp / "s.csv"
    frame.to_csv(path, index=False)
    prepared = _load(path, frame)
    changed = frame.copy()
    rng = np.random.default_rng(3)
    pos = prepared.test_rows
    changed.loc[pos, "price"] = rng.uniform(80_000, 5_000_000, size=pos.size).round(-2)
    for col in ("sqft_living", "sqft_above", "sqft_basement", "grade", "view", "lat", "yr_built"):
        changed.loc[pos, col] = changed[col].sample(pos.size, random_state=2).to_numpy()   # one row order: sqft identity holds
    changed.loc[pos, "zipcode"] = "98999"
    changed.loc[pos, "date"] = "20150101T000000"
    path2 = tmp / "changed.csv"
    changed.to_csv(path2, index=False)
    other = _load(path2, changed)
    out = {}
    for name, prep in (("base", prepared), ("changed", other)):
        allin, cands, winners = small_selection(prep)
        pipe = deployment.final_model(prep, winners, allin, cands)
        out[name] = {"prepared": prep, "pipe": pipe, "diag": diagnostics.run(prep, pipe),
                     "coef": explain.coefficient_table(prep, pipe),
                     "perm": explain.permutation_importance(prep, pipe)}
    return out


def _numbers(diag):
    return [(r["assumption"], r["statistic"], r["value"], r["p_value"])
            for r in diagnostics.summary_rows(diag)]


def test_changing_the_test_rows_changes_no_diagnostic_or_explanation(runs):
    """H-3 / AC: the diagnostics and the permutation importance take training rows only."""
    a, b = runs["base"], runs["changed"]
    assert a["prepared"].sha256 != b["prepared"].sha256
    assert np.array_equal(a["prepared"].test_rows, b["prepared"].test_rows)
    pd.testing.assert_frame_equal(a["prepared"].training, b["prepared"].training)
    assert a["pipe"].model_key == b["pipe"].model_key
    assert np.array_equal(a["pipe"].fit.coef, b["pipe"].fit.coef)
    assert _numbers(a["diag"]) == _numbers(b["diag"])
    pd.testing.assert_frame_equal(a["diag"].residuals, b["diag"].residuals)
    pd.testing.assert_frame_equal(a["diag"].vif_by_group, b["diag"].vif_by_group)
    pd.testing.assert_frame_equal(a["coef"], b["coef"])
    pd.testing.assert_frame_equal(a["perm"][0], b["perm"][0])
    assert a["perm"][1] == b["perm"][1]


def test_the_residuals_are_those_of_the_training_rows_only(runs):
    r = runs["base"]
    res = r["diag"].residuals
    training = r["prepared"].training
    assert res["row"].tolist() == training["row"].tolist()
    assert not np.isin(res["row"], r["prepared"].test_rows).any()
    assert r["diag"].n_train == len(training)


def test_the_diagnostics_refuse_rows_that_are_not_the_pipelines_training_rows(runs):
    r = runs["base"]
    prepared = r["prepared"]
    bad = prepared.training.copy()
    bad.loc[bad.index[0], "row"] = int(prepared.test_rows[0])
    with pytest.raises(deployment.DeploymentError):
        diagnostics.run(dataclasses.replace(prepared, training=bad), r["pipe"])
    with pytest.raises(deployment.DeploymentError):
        explain.permutation_importance(dataclasses.replace(prepared, training=bad), r["pipe"])
    fewer = dataclasses.replace(prepared, training=prepared.training.iloc[:-5])
    with pytest.raises(diagnostics.DiagnosticsError, match="not fitted on these training rows"):
        diagnostics.run(fewer, r["pipe"])


# --- each statistic against a direct computation -------------------------------------------

def _design(r):
    pipe, training = r["pipe"], r["prepared"].training
    return ols.design(pipe.preprocessor.transform(training).X), np.log(training["price"].to_numpy(float))


def test_residuals_leverage_and_studentized_residuals(runs):
    r = runs["base"]
    D, y = _design(r)
    beta, *_ = np.linalg.lstsq(D, y, rcond=None)
    e = y - D @ beta
    H = D @ np.linalg.pinv(D)
    s2 = e @ e / (len(y) - np.linalg.matrix_rank(D))
    res = r["diag"].residuals
    np.testing.assert_allclose(res["resid"], e, rtol=1e-6, atol=1e-9)
    np.testing.assert_allclose(res["leverage"], np.diag(H), rtol=1e-6, atol=1e-10)
    np.testing.assert_allclose(res["studentized"], e / np.sqrt(s2 * (1 - np.diag(H))), rtol=1e-6,
                               atol=1e-9)


def test_reset_f_test_equals_a_direct_nested_fit(runs):
    r = runs["base"]
    D, y = _design(r)
    fitted = r["diag"].residuals["fitted"].to_numpy()
    z = (fitted - fitted.mean()) / fitted.std()
    rss = lambda M: float(np.sum((y - M @ np.linalg.lstsq(M, y, rcond=None)[0]) ** 2))
    U = np.column_stack([D, z ** 2, z ** 3])
    df = len(y) - np.linalg.matrix_rank(U)
    f = ((rss(D) - rss(U)) / 2) / (rss(U) / df)
    lin = r["diag"].results["linearity"]
    assert lin["reset_f"] == pytest.approx(f, rel=1e-6)
    assert lin["reset_df"] == [2, df]
    assert lin["reset_p_value"] == pytest.approx(stats.f.sf(f, 2, df), rel=1e-5, abs=1e-300)


def test_durbin_watson_and_the_repeat_sales():
    assert diagnostics.durbin_watson(np.array([1.0, -1.0, 1.0, -1.0])) == pytest.approx(3.0)
    assert diagnostics.durbin_watson(np.array([1.0, 1.0, 1.0])) == 0.0
    rows = pd.DataFrame({"id": ["a", "b", "a", "c", "a", "b"], "row": [0, 1, 2, 3, 4, 5],
                         "sale_days": [30, 10, 5, 7, 60, 2], "resid": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]})
    rs = diagnostics.repeat_sales(rows)
    assert rs == {"n_rows": 6, "n_houses": 3, "n_repeat_sales": 3, "n_houses_with_repeat_sales": 2,
                  "n_rows_of_houses_with_repeat_sales": 5}
    pairs = diagnostics.repeat_sale_pairs(rows)
    # house a by date: rows 2 (day 5), 0 (day 30), 4 (day 60); house b: rows 5 (day 2), 1 (day 10)
    assert pairs[["row_first", "row_second"]].values.tolist() == [[2, 0], [0, 4], [5, 1]]
    assert pairs["days_between"].tolist() == [25, 30, 8]


def test_the_independence_counts_come_from_the_training_rows(runs):
    """TR-02: the training repeat sales are rows − unique id of the training rows, computed; the
    full-data figure is background from the structural facts, labelled as such."""
    r = runs["base"]
    ind = r["diag"].results["independence"]
    training = r["prepared"].training
    assert ind["repeat_sales_training"]["n_repeat_sales"] == len(training) - training["id"].nunique()
    bg = ind["full_data_repeat_sales_background"]
    assert bg["n_repeat_sales"] == r["prepared"].facts["n_repeat_sales"]
    assert "full data" in bg["level"] and "background" in bg["level"]
    pairs = ind["pairs"]
    assert len(pairs) == ind["repeat_sale_pairs"]
    rr, p = stats.pearsonr(pairs["resid_first"], pairs["resid_second"])
    assert ind["pair_resid_corr"] == pytest.approx(rr) and ind["pair_resid_corr_p_value"] == pytest.approx(p)
    by_date = r["diag"].residuals.sort_values(["sale_days", "row"], kind="stable")["resid"].to_numpy()
    assert ind["durbin_watson_by_date"] == pytest.approx(np.sum(np.diff(by_date) ** 2) / np.sum(by_date ** 2))


def test_breusch_pagan_is_n_times_r2_of_the_squared_residuals(runs):
    r = runs["base"]
    D, _ = _design(r)
    e2 = r["diag"].residuals["resid"].to_numpy() ** 2
    fitted = D @ np.linalg.lstsq(D, e2, rcond=None)[0]
    r2 = 1 - np.sum((e2 - fitted) ** 2) / np.sum((e2 - e2.mean()) ** 2)
    hom = r["diag"].results["homoscedasticity"]
    assert hom["bp_lm"] == pytest.approx(len(e2) * r2, rel=1e-6)
    assert hom["bp_df"] == np.linalg.matrix_rank(D) - 1
    assert hom["bp_p_value"] == pytest.approx(stats.chi2.sf(len(e2) * r2, hom["bp_df"]), rel=1e-5,
                                              abs=1e-300)


def test_normality_statistics(runs):
    r = runs["base"]
    e = r["diag"].residuals["resid"].to_numpy()
    s = r["diag"].residuals["studentized"].to_numpy()
    nor = r["diag"].results["normality"]
    jb = stats.jarque_bera(e)
    assert nor["jarque_bera"] == pytest.approx(jb.statistic)
    assert nor["skewness"] == pytest.approx(stats.skew(e))
    assert nor["excess_kurtosis"] == pytest.approx(stats.kurtosis(e))
    assert nor["share_abs_studentized_gt_1_96"] == pytest.approx(np.mean(np.abs(s) > 1.96))


def test_vif_gvif_and_within_group_vif_equal_direct_regressions(runs):
    r = runs["base"]
    pipe, training = r["pipe"], r["prepared"].training
    X = pipe.preprocessor.transform(training).X
    cols = list(pipe.preprocessor.columns)
    by_col = r["diag"].vif_by_column.set_index("column")["vif"]
    for name in [c for c in ("grade", "sqft_living", "lat") if c in cols]:
        j = cols.index(name)
        others = ols.design(np.delete(X, j, axis=1))
        pred = others @ np.linalg.lstsq(others, X[:, j], rcond=None)[0]
        r2 = 1 - np.sum((X[:, j] - pred) ** 2) / np.sum((X[:, j] - X[:, j].mean()) ** 2)
        assert by_col[name] == pytest.approx(1 / (1 - r2), rel=1e-6)
    by_group = r["diag"].vif_by_group.set_index("group")
    single = [g for g in pipe.groups if by_group.loc[g, "n_columns"] == 1]
    column_of = r["diag"].vif_by_column.set_index("group")["column"]
    for g in single:
        vif = by_col[column_of[g]]              # e.g. the date group's column is sale_days
        assert by_group.loc[g, "gvif"] == pytest.approx(vif, rel=1e-8)
        assert by_group.loc[g, "gvif_adjusted"] == pytest.approx(np.sqrt(vif), rel=1e-8)
        assert pd.isna(by_group.loc[g, "within_group_max_vif"])
    if "yr_renovated" in pipe.groups:
        a, b = cols.index("is_renovated"), cols.index("yr_renovated_effective")
        rho = np.corrcoef(X[:, a], X[:, b])[0, 1]
        assert by_group.loc["yr_renovated", "within_group_max_vif"] == pytest.approx(1 / (1 - rho ** 2))
    R = np.corrcoef(X, rowvar=False)
    ev = np.linalg.eigvalsh(R)
    assert r["diag"].results["multicollinearity"]["correlation_condition_number"] == \
        pytest.approx(np.sqrt(ev.max() / ev.min()))


def test_violations_are_disclosed_never_failures(runs):
    table = diagnostics.summary_table(runs["base"]["diag"])
    assert list(table["假設"]) == ["線性", "誤差獨立", "同質變異", "殘差常態", "多重共線性"]
    for verdict in table["結果"]:
        assert verdict in ("違反（揭露，不判失敗）", "未偵測到違反")


# --- the explanation ----------------------------------------------------------------------

def test_coefficient_table_readings(runs):
    r = runs["base"]
    pipe = r["pipe"]
    coef = r["coef"]
    assert coef["column"].tolist() == list(pipe.fit.column_names)
    np.testing.assert_array_equal(coef["coef_log"], pipe.fit.coef)
    np.testing.assert_allclose(coef["std_error"], np.sqrt(pipe.fit.s2 * np.diag(pipe.fit.xtx_inv)))
    rest = coef.iloc[1:]
    np.testing.assert_allclose(rest["pct_per_unit"], 100 * np.expm1(rest["coef_log"]))
    numeric = rest[rest["kind"] == "numeric"]
    np.testing.assert_allclose(numeric["pct_per_train_sd"],
                               100 * np.expm1(numeric["coef_log"] * numeric["train_sd"]))
    X = pipe.preprocessor.transform(r["prepared"].training).X
    j = list(pipe.preprocessor.columns).index(numeric["column"].iloc[0])
    assert numeric["train_sd"].iloc[0] == pytest.approx(X[:, j].std())
    zips = rest[rest["column"].str.startswith("zipcode_")]
    assert (zips["kind"] == f"one-hot vs baseline zipcode {pipe.preprocessor.zipcode_baseline}").all()
    assert zips["train_sd"].isna().all()


def test_permutation_importance_is_reproducible_and_reads_the_model(runs):
    r = runs["base"]
    table, baseline = r["perm"]
    again, baseline2 = explain.permutation_importance(r["prepared"], r["pipe"])
    pd.testing.assert_frame_equal(table, again)
    assert baseline == baseline2
    assert set(table["group"]) == set(r["pipe"].groups)
    assert table["log_rmse_increase_mean"].is_monotonic_decreasing
    assert (table["n_repeats"] == explain.N_REPEATS).all()
    # the synthetic price depends strongly on sqft_living and grade, not on bedrooms
    top = table["group"].head(4).tolist()
    present = [g for g in ("sqft_living", "grade") if g in r["pipe"].groups]
    assert all(g in top for g in present)
    if "bedrooms" in r["pipe"].groups:
        noise = table.set_index("group").loc["bedrooms", "log_rmse_increase_mean"]
        assert noise < 0.1 * table["log_rmse_increase_mean"].max()
    assert baseline["n_rows"] == r["prepared"].n_train


# --- the official outputs (written by the notebook from the real training rows) -------------

def test_official_diagnostic_and_explanation_files(prepared_real):
    """TK-2: the figures (PNG) and tables (CSV) exist; the training repeat sales are the real
    training rows' rows − unique id (TR-02), the full-data figure is background only."""
    for name in list(diagnostics.FIGURE_FILES.values()) + list(explain.FIGURE_FILES.values()):
        path = FIGURES_DIR / name
        assert path.is_file(), f"run hw2.ipynb first: {path}"
        assert path.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    for name in list(diagnostics.TABLE_FILES.values()) + list(explain.TABLE_FILES.values()):
        assert (TABLES_DIR / name).is_file(), name
    summary = pd.read_csv(TABLES_DIR / diagnostics.TABLE_FILES["summary"], dtype=str)
    training = prepared_real.training
    row = summary[summary["statistic"] == "repeat sales in the training set (rows - unique id)"]
    assert row["value"].tolist() == [str(len(training) - training["id"].nunique())]
    bg = summary[summary["statistic"].str.contains("full data set")]
    assert bg["value"].tolist() == [str(prepared_real.facts["n_repeat_sales"])]
    assert set(summary["assumption"]) == set(diagnostics.SUMMARY_LABELS)
    perm = pd.read_csv(TABLES_DIR / explain.TABLE_FILES["permutation"])
    assert perm["rank"].tolist() == list(range(1, len(perm) + 1))
    coef = pd.read_csv(TABLES_DIR / explain.TABLE_FILES["coefficients"])
    assert coef["column"].iloc[0] == "(intercept)"
