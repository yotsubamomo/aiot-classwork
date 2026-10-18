"""Comparison models (Spec rev 5 「對照模型」; CC-1; DA §11 G-1, G-2): Ridge and Lasso choose their
alpha by training CV only and stay metric-only; the lecture's p-value backward elimination selects
one subset by group partial F tests, fold-internal like the path methods.

Synthetic data only (DA TR-01)."""
import numpy as np
import pandas as pd
import pytest
from scipy import stats
from sklearn.linear_model import Lasso, Ridge

from hw2 import comparison, contract, data, fixture, models, ols, preprocess, selection

GRID_R = (0.01, 0.1, 1.0, 10.0, 100.0)
GRID_L = (1e-5, 1e-4, 1e-3, 1e-2)


def _load(path, frame):
    return data.load_and_split(path, expected_sha256=data.file_sha256(path),
                               expected_rows=len(frame),
                               expected_unique_ids=frame["id"].nunique())


@pytest.fixture(scope="module")
def synth(tmp_path_factory):
    frame = fixture.synthetic_sales(n_houses=900, n_repeats=20, seed=11)
    path = tmp_path_factory.mktemp("cmp") / "s.csv"
    frame.to_csv(path, index=False)
    return frame, path, _load(path, frame)


# --- G-1: test rows never reach the alpha selection (nor any other selection) --------------------

def test_changing_the_test_rows_changes_no_alpha_cv_metric_or_selection(synth, tmp_path):
    """G-1 (CC-1 (1)(4)): with every feature and price of the test rows changed, the Ridge/Lasso
    alphas and CV metrics, the p-value subsets and the CV winners are all unchanged."""
    frame, _, prepared = synth
    changed = frame.copy()
    rng = np.random.default_rng(0)
    pos = prepared.test_rows
    changed.loc[pos, "price"] = rng.uniform(80_000, 5_000_000, size=pos.size).round(-2)
    for col in ("bedrooms", "grade", "view", "sqft_lot15", "yr_built"):
        changed.loc[pos, col] = changed[col].sample(pos.size, random_state=1).to_numpy()
    changed.loc[pos, "zipcode"] = "98999"                          # unseen category
    path = tmp_path / "changed.csv"
    changed.to_csv(path, index=False)
    other = _load(path, changed)
    assert other.sha256 != prepared.sha256
    assert np.array_equal(other.test_rows, prepared.test_rows)
    pd.testing.assert_frame_equal(other.training, prepared.training)

    for name, grid in (("ridge", GRID_R), ("lasso", GRID_L)):
        a = comparison.select_alpha(prepared.training, name, grid)
        b = comparison.select_alpha(other.training, name, grid)
        assert a.alpha == b.alpha and a.cv_by_alpha == b.cv_by_alpha
        assert a.cv()["mean"] == b.cv()["mean"]
    pa = comparison.evaluate_pvalue_backward(prepared.training)
    pb = comparison.evaluate_pvalue_backward(other.training)
    assert (pa["canonical_groups"], pa["fold_groups"], pa["cv"]["mean"]) == \
        (pb["canonical_groups"], pb["fold_groups"], pb["cv"]["mean"])
    wa = models.determine_winners(models.fit_allin(prepared.training), {})
    wb = models.determine_winners(models.fit_allin(other.training), {})
    assert wa == wb


def test_the_alpha_search_sees_only_the_training_rows_and_the_shared_folds(synth, monkeypatch):
    """Every fit inside the alpha search receives fold-training rows of the training set only."""
    _, _, prepared = synth
    train_ids = set(prepared.training["row"])
    seen = []
    original = preprocess.fit_preprocessor

    def spy(rows, *a, **k):
        seen.append(set(rows["row"]))
        return original(rows, *a, **k)

    monkeypatch.setattr(comparison.preprocess, "fit_preprocessor", spy)
    comparison.select_alpha(prepared.training, "ridge", GRID_R)
    folds = sorted(prepared.training["fold"].unique())
    assert len(seen) == len(folds)
    for f, rows in zip(folds, seen):
        assert rows <= train_ids
        assert rows == set(prepared.training.loc[prepared.training["fold"] != f, "row"])


# --- alpha rule, the fits, metric-only -----------------------------------------------------------

def test_alpha_is_the_lowest_cv_rmse_and_ties_go_to_the_larger_alpha(synth):
    _, _, prepared = synth
    sel = comparison.select_alpha(prepared.training, "ridge", GRID_R)
    best = min(sel.cv_by_alpha, key=lambda r: (r["rmse"], -r["alpha"]))
    assert sel.alpha == best["alpha"]
    sel.cv_by_alpha = [dict(r, rmse=1.0) for r in sel.cv_by_alpha]           # all tied
    assert min(sel.cv_by_alpha, key=lambda r: (r["rmse"], -r["alpha"]))["alpha"] == max(GRID_R)
    entry = comparison.select_alpha(prepared.training, "lasso", GRID_L).to_entry()
    contract.validate_metric_only_entry(entry, "lasso", prepared.n_folds)


def test_cv_metrics_at_the_alpha_equal_a_direct_fold_by_fold_fit(synth):
    """The recorded CV of the chosen alpha equals sklearn fits on each fold's training rows."""
    _, _, prepared = synth
    tr = prepared.training
    for name, grid in (("ridge", GRID_R), ("lasso", GRID_L)):
        sel = comparison.select_alpha(tr, name, grid)
        rmse = []
        for f in sorted(tr["fold"].unique()):
            a, v = tr[tr["fold"] != f], tr[tr["fold"] == f]
            pre = preprocess.fit_preprocessor(a, standardize=True)
            X, y = pre.transform(a).X, np.log(a["price"].to_numpy(float))
            model = (Ridge(alpha=sel.alpha) if name == "ridge"
                     else Lasso(alpha=sel.alpha, max_iter=500_000, tol=1e-12)).fit(X, y)
            pred = np.exp(model.predict(pre.transform(v).X))
            rmse.append(np.sqrt(np.mean((pred - v["price"].to_numpy(float)) ** 2)))
        assert sel.cv()["mean"]["rmse"] == pytest.approx(np.mean(rmse), rel=1e-6), name


def test_refit_on_the_training_set_matches_sklearn_and_is_metric_only(synth):
    _, _, prepared = synth
    tr = prepared.training
    for name in comparison.METRIC_ONLY:
        alpha = 1.0 if name == "ridge" else 1e-3
        m = comparison.fit_metric_only(tr, name, alpha)
        pre = preprocess.fit_preprocessor(tr, standardize=True)
        X, y = pre.transform(tr).X, np.log(tr["price"].to_numpy(float))
        ref = (Ridge(alpha=alpha) if name == "ridge"
               else Lasso(alpha=alpha, max_iter=500_000, tol=1e-12)).fit(X, y)
        np.testing.assert_allclose(m.predict_usd(tr.head(50)), np.exp(ref.predict(X[:50])),
                                   rtol=1e-6)
        assert not hasattr(m, "predict_interval") and not hasattr(m, "fit")
    entry = comparison.select_alpha(tr, "ridge", GRID_R).to_entry()
    assert "fit" not in entry and "coef" not in entry and entry["adj_r2_log"] is None
    assert entry["offers"] == {"prediction_interval": False, "coverage_statistics": False,
                               "live_prediction": False}
    assert contract.test_field_paths(entry) == []


def test_metric_only_models_never_compete_for_the_cv_winners(synth):
    """G-2: determine_winners accepts only the path methods; Ridge/Lasso cannot enter."""
    _, _, prepared = synth
    allin = models.fit_allin(prepared.training)
    with pytest.raises(ValueError, match="unknown path methods"):
        models.determine_winners(allin, {"ridge": []})


@pytest.mark.parametrize("name, field", [("ridge", "alpha"), ("lasso", "cv_by_alpha"),
                                         ("ridge", "coef"), ("lasso", "adj_r2_log"),
                                         ("ridge", "offers"), ("ridge", "is_cv_winner_candidate")])
def test_metric_only_entry_violations_are_rejected(synth, name, field):
    _, _, prepared = synth
    entry = comparison.select_alpha(prepared.training, name,
                                    GRID_R if name == "ridge" else GRID_L).to_entry()
    if field == "alpha":
        entry["alpha"] = entry["alpha_grid"][-1] if entry["alpha"] != entry["alpha_grid"][-1] \
            else entry["alpha_grid"][0]
    elif field == "cv_by_alpha":
        entry["cv_by_alpha"][0]["rmse"] = 0.0
    elif field == "coef":
        entry["coef"] = [0.0]
    elif field == "adj_r2_log":
        entry["adj_r2_log"] = 0.9
    elif field == "offers":
        entry["offers"]["live_prediction"] = True
    else:
        entry["is_cv_winner_candidate"] = True
    with pytest.raises(contract.ContractError):
        contract.validate_metric_only_entry(entry, name, prepared.n_folds)


# --- p-value backward elimination ----------------------------------------------------------------

def _direct_f(rows, groups, g):
    """Partial F test of dropping group g, from two direct OLS fits (hw2.ols with the intercept)."""
    def fit(gs):
        pre = preprocess.fit_preprocessor(rows, gs)
        return ols.fit_ols(pre.transform(rows).X, np.log(rows["price"].to_numpy(float)),
                           pre.columns)
    full, rest = fit(groups), fit([h for h in groups if h != g])
    sse_full, sse_rest = full.s2 * full.df_resid, rest.s2 * rest.df_resid
    q = full.rank - rest.rank
    f = ((sse_rest - sse_full) / q) / (sse_full / full.df_resid)
    return f, q, full.df_resid, stats.f.sf(f, q, full.df_resid)


def test_group_f_tests_equal_direct_ols_fits(synth):
    _, _, prepared = synth
    tr = prepared.training
    gram = selection.GroupGram(tr)
    groups = list(preprocess.FEATURE_GROUPS)
    tests = comparison.group_f_tests(gram, groups)
    for g in ("bedrooms", "zipcode", "yr_renovated", "grade"):
        f, q, df, p = _direct_f(tr, groups, g)
        assert tests[g]["df_num"] == q and tests[g]["df_den"] == df
        assert tests[g]["f"] == pytest.approx(f, rel=1e-6)
        assert tests[g]["p_value"] == pytest.approx(p, rel=1e-5, abs=1e-300)


def test_pvalue_backward_removes_one_group_per_step_only_above_the_threshold(synth):
    _, _, prepared = synth
    path = comparison.pvalue_backward(prepared.training)
    current = list(preprocess.FEATURE_GROUPS)
    for step in path.steps:
        assert step["p_value"] > comparison.PVALUE_THRESHOLD
        current.remove(step["removed"])
        assert step["k_after"] == len(current)
    assert tuple(current) == path.subset
    assert all(t["p_value"] <= comparison.PVALUE_THRESHOLD for t in path.final_tests.values())
    # every removed group had the largest p-value among the groups present at that step
    gram = selection.GroupGram(prepared.training)
    present = list(preprocess.FEATURE_GROUPS)
    for step in path.steps:
        tests = comparison.group_f_tests(gram, present)
        assert step["p_value"] == pytest.approx(max(t["p_value"] for t in tests.values()))
        present.remove(step["removed"])


def test_a_pure_noise_group_is_removed_and_strong_groups_stay(synth):
    frame, _, _ = synth
    rows = frame.copy()
    rng = np.random.default_rng(5)
    rows["sqft_lot15"] = rng.integers(1000, 20000, size=len(rows))       # unrelated to price
    path = comparison.pvalue_backward(rows)
    assert "sqft_living" in path.subset and "grade" in path.subset
    assert "sqft_lot15" not in path.subset


def test_pvalue_selection_boundary_is_fold_internal(synth):
    """SR-11: a fold's subset depends on that fold's training rows only; the canonical subset on
    the whole training set only."""
    _, _, prepared = synth
    tr = prepared.training
    entry = comparison.evaluate_pvalue_backward(tr)
    for f, groups in zip(sorted(tr["fold"].unique()), entry["fold_groups"]):
        assert list(comparison.pvalue_backward(tr[tr["fold"] != f]).subset) == groups
    assert entry["canonical_groups"] == list(comparison.pvalue_backward(tr).subset)
    changed = tr.copy()
    is0 = changed["fold"] == 0
    changed.loc[is0, "price"] = changed.loc[is0, "price"][::-1].to_numpy() * 3
    changed.loc[is0, "grade"] = 4
    other = comparison.evaluate_pvalue_backward(changed)
    assert other["fold_groups"][0] == entry["fold_groups"][0]
    contract.validate_pvalue_entry(entry, prepared.n_folds)
    assert entry["is_cv_winner_candidate"] is False and "fit" not in entry
    assert contract.test_field_paths(entry) == []
