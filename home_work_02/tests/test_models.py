"""Candidates, the three rank-deficiency classes, the All-in baseline and the CV winners
(Spec rev 5 「指標與推論」 SR-04／SR-10；次 seam「模型與推論」「選模」). Synthetic rows only."""
import numpy as np
import pytest

from hw2 import data, fixture, models, preprocess


@pytest.fixture(scope="module")
def training(tmp_path_factory):
    """Training rows (with folds) of a small synthetic data set."""
    frame = fixture.synthetic_sales(n_houses=900, n_repeats=20, seed=11, n_zipcodes=12)
    path = tmp_path_factory.mktemp("models") / "s.csv"
    frame.to_csv(path, index=False)
    prepared = data.load_and_split(path, expected_sha256=data.file_sha256(path),
                                   expected_rows=len(frame),
                                   expected_unique_ids=frame["id"].nunique())
    return prepared.training


def test_allin_is_one_model_on_all_18_groups(training):
    allin = models.fit_allin(training)
    entry = allin.to_entry()
    assert entry["model_key"] == "allin" and entry["k"] == 18 and entry["is_method_winner"]
    assert entry["canonical_groups"] == list(preprocess.FEATURE_GROUPS)
    assert entry["folds_agree"] == 5 and entry["status"]["state"] == "valid"
    fit = entry["fit"]
    assert fit["n_train"] == len(training) and fit["rank"] == fit["n_columns"]
    assert fit["df_resid"] == fit["n_train"] - fit["rank"]
    assert fit["coef_names"][0] == "(intercept)" and fit["coef_names"][1:] == fit["encoded_columns"]
    assert fit["uses_source_features"][-1] == "sqft_lot15" and "yr_built" in fit["uses_source_features"]
    cv = entry["cv"]
    assert cv["scale"] == "USD" and len(cv["folds"]) == 5
    for m in ("mae", "mse", "rmse", "r2"):
        assert cv["mean"][m] == pytest.approx(np.mean([f[m] for f in cv["folds"]]))
        assert cv["std"][m] == pytest.approx(np.std([f[m] for f in cv["folds"]], ddof=1))
    assert all(f["rmse"] == pytest.approx(np.sqrt(f["mse"])) for f in cv["folds"])


def test_cv_fold_uses_only_its_training_rows(training):
    """Fold 0's model is fitted only on the rows outside fold 0: changing fold 0's prices changes
    its validation metrics but not its fitted coefficients or rank."""
    a = models.evaluate_candidate(training, "forward_sfs", 2, ("sqft_living", "grade"))
    changed = training.copy()
    rows = changed["fold"] == 0
    changed.loc[rows, "price"] = changed.loc[rows, "price"] * 1.5
    b = models.evaluate_candidate(changed, "forward_sfs", 2, ("sqft_living", "grade"))
    assert a.folds[0]["rmse"] != b.folds[0]["rmse"]
    # folds 1..4 train on rows that include fold 0, so their fits change; fold 0's fit does not:
    assert a.folds[0]["rank"] == b.folds[0]["rank"]
    fa = models.fit_model(training[training["fold"] != 0], ("sqft_living", "grade"))
    fb = models.fit_model(changed[changed["fold"] != 0], ("sqft_living", "grade"))
    np.testing.assert_array_equal(fa.fit.coef, fb.fit.coef)


def test_legal_encoding_a_zipcode_missing_from_a_fold_has_no_column(training):
    """SR-04 class 1: not a defect. The fold's design lacks that zipcode's column, the fit
    succeeds, and validation rows with that zipcode are encoded as the baseline and counted."""
    t = training.copy()
    fold0 = t["fold"] == 0
    t.loc[fold0, "zipcode"] = np.where(np.arange(fold0.sum()) % 7 == 0, "99999",
                                       t.loc[fold0, "zipcode"])
    c = models.evaluate_candidate(t, "rfe", 2, ("sqft_living", "zipcode"))
    assert c.valid
    f0 = c.folds[0]
    assert f0["valid"] and "99999" not in f0["zipcode_categories"]
    assert f0["n_valid_unseen_zipcode"] == int((t.loc[fold0, "zipcode"] == "99999").sum()) > 0
    assert all(f["n_valid_unseen_zipcode"] == 0 for f in c.folds[1:])
    others = c.folds[1]
    assert "99999" in others["zipcode_categories"]
    assert f0["n_columns"] == others["n_columns"] - 1
    assert "99999" in c.model.preprocessor.zipcode_categories      # canonical fit sees all rows


def test_invalid_candidate_when_a_fold_design_is_rank_deficient(training):
    """SR-04 class 2: waterfront constant on fold 2's training rows -> that fold invalid ->
    the whole (method, k) invalid, excluded from the CV winners; no column is dropped."""
    t = training.copy()
    t["waterfront"] = np.where(t["fold"] == 2, 1, 0)       # constant 0 outside fold 2
    c = models.evaluate_candidate(t, "rfe", 2, ("sqft_living", "waterfront"))
    bad = [f for f in c.folds if not f["valid"]]
    assert [f["fold"] for f in bad] == [2]
    assert bad[0]["reason"].startswith("fold_rank_deficient") and bad[0]["rmse"] is None
    assert c.status == {"state": "invalid", "reason": "fold_rank_deficient", "folds": [2]}
    entry = c.to_entry()
    assert entry["cv"]["mean"] is None and entry["fit"] is not None   # canonical fit is fine
    good = models.evaluate_candidate(t, "rfe", 1, ("sqft_living",))
    allin = models.fit_allin(training)
    winners = models.determine_winners(allin, {"rfe": [good, c]})
    assert winners["method_winners"]["rfe"]["model_key"] == "rfe_k01"
    assert not c.is_method_winner and "rfe_k02" not in winners["authorized_test_models"]


def test_canonical_rank_deficient_non_winner_is_invalid_without_fit_and_the_run_continues(
        training, tmp_path):
    """SR-10: the canonical subset is collinear on the whole training set (fold subsets fine)."""
    t = training.copy()
    t["sqft_living15"] = t["sqft_living"] * 2
    c = models.evaluate_candidate(t, "backward_sfs", 2, ("sqft_living", "sqft_living15"),
                                  fold_groups=[("sqft_living", "grade")] * 5)
    assert all(f["valid"] for f in c.folds)
    assert c.status["state"] == "invalid" and c.status["reason"] == "canonical_rank_deficient"
    assert c.model is None and c.to_entry()["fit"] is None
    other = models.evaluate_candidate(t, "backward_sfs", 1, ("grade",))
    allin = models.fit_allin(training)
    winners = models.determine_winners(allin, {"backward_sfs": [other, c]})
    assert winners["method_winners"]["backward_sfs"]["model_key"] == "backward_sfs_k01"
    assert not c.is_method_winner


def test_allin_rank_deficiency_is_an_experiment_level_failure(training):
    """SR-04 class 3: stop with an error that lists the invalid candidates."""
    t = training.copy()
    t["sqft_lot15"] = t["sqft_lot"]
    with pytest.raises(models.ExperimentFailure, match="All-in") as err:
        models.fit_allin(t)
    assert [c["model_key"] for c in err.value.invalid_candidates] == ["allin"]
    assert "allin" in str(err.value) and "rank" in str(err.value)


def test_a_method_without_any_valid_candidate_stops_the_run(training):
    t = training.copy()
    t["waterfront"] = 0
    bad = models.evaluate_candidate(t, "lasso_path", 1, ("waterfront",))
    assert not bad.valid
    allin = models.fit_allin(training)
    with pytest.raises(models.ExperimentFailure, match="lasso_path has no valid candidate") as err:
        models.determine_winners(allin, {"lasso_path": [bad]})
    assert err.value.invalid_candidates[0]["model_key"] == "lasso_path_k01"


# --- winners from candidates with given CV RMSE ------------------------------------------------

def _cand(method, k, rmse, valid=True):
    groups = preprocess.FEATURE_GROUPS[:k]
    folds = [{"fold": f, "valid": valid, "mae": rmse, "mse": rmse ** 2, "rmse": rmse, "r2": 0.5}
             for f in range(5)]
    status = {"state": "valid", "reason": None} if valid else \
        {"state": "invalid", "reason": "fold_rank_deficient", "folds": [0]}
    return models.Candidate(method=method, k=k, canonical_groups=groups, fold_groups=[groups] * 5,
                            folds=folds, model=None, status=status)


def _complete(allin_rmse=10.0, **overrides):
    rmse = {"forward_sfs": 20.0, "backward_sfs": 20.0, "rfe": 20.0, "lasso_path": 20.0}
    rmse.update(overrides)
    paths = {m: [_cand(m, 3, r + 1), _cand(m, 5, r), _cand(m, 7, r)] for m, r in rmse.items()}
    return _cand("allin", 18, allin_rmse), paths


def test_method_winner_ties_go_to_the_smaller_k():
    allin, paths = _complete()
    winners = models.determine_winners(allin, paths)
    assert {m: w["k"] for m, w in winners["method_winners"].items()} == dict.fromkeys(paths, 5)
    assert [c.is_method_winner for c in paths["rfe"]] == [False, True, False]


def test_overall_winner_and_its_tie_break_follow_the_fixed_method_order():
    allin, paths = _complete(allin_rmse=25.0, backward_sfs=15.0, rfe=15.0)
    winners = models.determine_winners(allin, paths)
    assert winners["complete"] and winners["overall"]["model_key"] == "backward_sfs_k05"
    allin, paths = _complete(allin_rmse=15.0, forward_sfs=15.0)
    assert models.determine_winners(allin, paths)["overall"]["model_key"] == "allin"


def test_authorized_set_is_method_winners_allin_and_overall_without_duplicates():
    allin, paths = _complete(allin_rmse=30.0, lasso_path=12.0)
    winners = models.determine_winners(allin, paths)
    assert winners["authorized_test_models"] == [
        "allin", "forward_sfs_k05", "backward_sfs_k05", "rfe_k05", "lasso_path_k05"]
    assert winners["overall"]["model_key"] == "lasso_path_k05"
    assert not set(winners["authorized_test_models"]) & {"ridge", "lasso"}


def test_invalid_candidates_never_win_even_with_the_lowest_rmse():
    allin, paths = _complete()
    paths["rfe"].append(_cand("rfe", 9, 1.0, valid=False))
    winners = models.determine_winners(allin, paths)
    assert winners["method_winners"]["rfe"]["k"] == 5 and not paths["rfe"][-1].is_method_winner


def test_incomplete_methods_leave_the_overall_winner_undetermined():
    allin, paths = _complete()
    del paths["rfe"]
    winners = models.determine_winners(allin, paths)
    assert not winners["complete"] and winners["overall"] is None
    assert winners["pending_methods"] == ["rfe"]


def test_overall_winner_cannot_be_determined_without_a_finite_cv_rmse():
    allin, paths = _complete(allin_rmse=float("nan"))
    with pytest.raises(models.ExperimentFailure, match="cannot be determined"):
        models.determine_winners(allin, paths)
