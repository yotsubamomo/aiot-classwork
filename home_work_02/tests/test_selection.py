"""Feature-group selection paths and the selection boundary (Spec rev 5 次 seam「特徵選擇」「選擇邊界」,
SR-01; #60 R1 F-2: the boundary is tested at the call point that receives both the training and the
validation rows of a fold). Synthetic rows only (DA TR-01)."""
import numpy as np
import pytest

from hw2 import data, fixture, models, preprocess, selection

GROUPS = preprocess.FEATURE_GROUPS
METHODS = models.PATH_METHODS


def _prepared(tmp_path_factory, name, frame):
    path = tmp_path_factory.mktemp(name) / "s.csv"
    frame.to_csv(path, index=False)
    return data.load_and_split(path, expected_sha256=data.file_sha256(path),
                               expected_rows=len(frame), expected_unique_ids=frame["id"].nunique())


@pytest.fixture(scope="module")
def training(tmp_path_factory):
    frame = fixture.synthetic_sales(n_houses=700, n_repeats=20, seed=23, n_zipcodes=10)
    return _prepared(tmp_path_factory, "sel", frame).training


def _ols_rss(rows, groups):
    """RSS of the OLS on ln(price) with an intercept, straight from the encoded design."""
    y = np.log(rows["price"].to_numpy(dtype=float))
    if not groups:
        return float(((y - y.mean()) ** 2).sum())
    pre = preprocess.fit_preprocessor(rows, groups)
    D = np.hstack([np.ones((len(rows), 1)), pre.transform(rows).X])
    beta = np.linalg.lstsq(D, y, rcond=None)[0]
    return float(((y - D @ beta) ** 2).sum())


# --- each method: 18 nested subsets, one group per step ----------------------------------------

@pytest.mark.parametrize("method", METHODS)
def test_every_step_changes_exactly_one_group(training, method):
    path = selection.PATH_FUNCTIONS[method](training)
    selection.check_path(path.subsets)
    assert [len(s) for s in path.subsets] == list(range(1, 19))
    assert set(path.subsets[-1]) == set(GROUPS)
    for small, big in zip(path.subsets, path.subsets[1:]):
        assert set(small) < set(big) and len(set(big) - set(small)) == 1
        assert list(big) == [g for g in GROUPS if g in big]          # canonical order


def test_check_path_rejects_a_step_that_swaps_groups():
    subsets = [tuple(GROUPS[:k]) for k in range(1, 19)]
    selection.check_path(subsets)
    broken = list(subsets)
    broken[3] = tuple(GROUPS[1:5])                     # k=4 drops 'date', adds two
    with pytest.raises(ValueError, match="differ by more than one group"):
        selection.check_path(broken)


def test_group_gram_rss_equals_a_direct_ols(training):
    gram = selection.GroupGram(training)
    for groups in [(), ("sqft_living",), ("zipcode",), ("date", "yr_renovated", "zipcode"), GROUPS]:
        assert gram.rss(groups) == pytest.approx(_ols_rss(training, groups), rel=1e-8)


def test_forward_and_backward_follow_the_rss_criterion(training):
    fwd = selection.forward_path(training)
    first = min(GROUPS, key=lambda g: (_ols_rss(training, (g,)), GROUPS.index(g)))
    assert fwd.subsets[0] == (first,)
    second = min((g for g in GROUPS if g != first),
                 key=lambda g: _ols_rss(training, selection.canonical((first, g))))
    assert set(fwd.subsets[1]) == {first, second}
    bwd = selection.backward_path(training)
    removed = min(GROUPS, key=lambda g: _ols_rss(training, [h for h in GROUPS if h != g]))
    assert set(GROUPS) - set(bwd.subsets[16]) == {removed}


def test_rfe_removes_the_group_with_the_smallest_contribution_spread(training):
    rfe = selection.rfe_path(training)
    pre = preprocess.fit_preprocessor(training, GROUPS)
    X = pre.transform(training).X
    D = np.hstack([np.ones((len(training), 1)), X])
    beta = np.linalg.lstsq(D, np.log(training["price"].to_numpy(dtype=float)), rcond=None)[0][1:]
    spread = {}
    for g in GROUPS:
        cols = [j for j, c in enumerate(pre.columns) if pre.group_of_column[c] == g]
        spread[g] = float(np.std(X[:, cols] @ beta[cols]))
    assert set(GROUPS) - set(rfe.subsets[16]) == {min(spread, key=spread.get)}
    imp = selection.GroupGram(training).importance(GROUPS)
    for g in GROUPS:
        assert imp[g] == pytest.approx(spread[g], rel=1e-6, abs=1e-12)


# --- ties follow canonical order ---------------------------------------------------------------

def test_pick_breaks_ties_by_canonical_order():
    scores = [(1.0, "lat"), (1.0 + 1e-15, "bedrooms"), (2.0, "date")]
    assert selection._pick(scores, prefer_late=False) == "bedrooms"
    assert selection._pick(scores, prefer_late=True) == "lat"


def test_lasso_ties_follow_canonical_order(monkeypatch, training):
    """Groups entering at the same point of the path, and groups that never enter, are ranked by
    canonical order (Spec: Lasso 路徑排序平手依 canonical order)."""
    entry = {g: (5, 0.1) for g in GROUPS}
    entry.update({"zipcode": (1, 0.9), "grade": (2, 0.5), "lat": (2, 0.5),
                  "bedrooms": (float("inf"), None), "date": (float("inf"), None)})
    entry["_warnings"] = []
    monkeypatch.setattr(selection, "lasso_entry", lambda rows: entry)
    order = [st["added"] for st in selection.lasso_path_order(training).steps]
    assert order[:3] == ["zipcode", "grade", "lat"]
    middle = [g for g in GROUPS if g not in ("zipcode", "grade", "lat", "bedrooms", "date")]
    assert order[3:-2] == middle
    assert order[-2:] == ["date", "bedrooms"]


def test_lasso_groups_that_never_enter_come_last_in_canonical_order(training):
    t = training.copy()
    t["bedrooms"] = 3
    t["floors"] = 1.0
    entry = selection.lasso_entry(t)
    assert entry["bedrooms"][0] == float("inf") and entry["floors"][0] == float("inf")
    order = [st["added"] for st in selection.lasso_path_order(t).steps]
    assert order[-2:] == ["bedrooms", "floors"]


def test_lasso_entry_is_the_first_nonzero_coefficient_of_any_group_column(training):
    entry = selection.lasso_entry(training)
    alphas = [entry[g][1] for g in GROUPS]
    assert all(a is not None and a > 0 for a in alphas)
    order = [st["added"] for st in selection.lasso_path_order(training).steps]
    assert [entry[g][1] for g in order] == sorted(alphas, reverse=True)


def test_duplicate_groups_tie_and_canonical_order_decides(training):
    """sqft_lot15 is an exact copy of sqft_lot that drives the price: forward adds the earlier
    one first; backward removes the later one first (its removal costs nothing)."""
    t = training.copy()
    t["sqft_lot15"] = t["sqft_lot"]
    t["price"] = t["price"] * np.exp(2.0 * (np.log(t["sqft_lot"]) - np.log(t["sqft_lot"]).mean()))
    fwd = selection.forward_path(t)
    assert fwd.subsets[0] == ("sqft_lot",)
    bwd = selection.backward_path(t)
    assert set(GROUPS) - set(bwd.subsets[16]) == {"sqft_lot15"}


def test_rank_deficient_groups_do_not_stop_or_skip_a_step(training):
    """SR-04: a group constant on the given rows is worth nothing, but every step still happens
    and every group appears on the path."""
    t = training.copy()
    t["waterfront"] = 0
    for method in METHODS:
        path = selection.PATH_FUNCTIONS[method](t)
        selection.check_path(path.subsets)
    assert selection.rfe_path(t).steps[0]["removed"] == "waterfront"
    assert selection.forward_path(t).subsets[-2] == tuple(g for g in GROUPS if g != "waterfront")


# --- selection boundary ------------------------------------------------------------------------

@pytest.mark.parametrize("method", METHODS)
def test_changing_a_folds_validation_rows_does_not_change_that_folds_subsets(training, method):
    """Fold-internal selection: fold 0's path is computed on the other folds' rows only, so
    scrambling fold 0's prices and features leaves it unchanged (the call point receives the
    training and the validation rows of every fold)."""
    before = selection.method_paths(training, method)
    t = training.copy()
    rows = t["fold"] == 0
    rng = np.random.default_rng(1)
    t.loc[rows, "price"] = t.loc[rows, "price"].to_numpy() * rng.uniform(0.2, 5.0, rows.sum())
    for col in ("sqft_living", "grade", "lat", "view"):
        t.loc[rows, col] = rng.permutation(t.loc[rows, col].to_numpy())
    after = selection.method_paths(t, method)
    assert after.fold_ids == before.fold_ids == [0, 1, 2, 3, 4]
    assert after.folds[0].subsets == before.folds[0].subsets
    # the other folds and the canonical path did see the changed rows (sanity: the change matters)
    changed = [after.folds[f].subsets != before.folds[f].subsets for f in range(1, 5)]
    assert any(changed) or after.canonical.subsets != before.canonical.subsets


@pytest.mark.parametrize("method", METHODS)
def test_canonical_subsets_depend_only_on_the_whole_training_set(training, method):
    paths = selection.method_paths(training, method)
    assert paths.canonical.subsets == selection.PATH_FUNCTIONS[method](training).subsets
    shuffled = training.copy()
    shuffled["fold"] = (shuffled["fold"] + 2) % 5            # other fold labels, same rows
    assert selection.method_paths(shuffled, method).canonical.subsets == paths.canonical.subsets
    for f, path in zip(paths.fold_ids, paths.folds):
        assert path.subsets == selection.PATH_FUNCTIONS[method](
            training[training["fold"] != f]).subsets


def test_candidates_use_each_folds_own_subset_and_the_canonical_fit(training):
    paths = selection.method_paths(training, "forward_sfs")
    cands = selection.evaluate_method(training, paths)
    assert [c.k for c in cands] == list(range(1, 19))
    for c in cands:
        assert c.canonical_groups == paths.canonical.subsets[c.k - 1]
        assert c.fold_groups == paths.fold_groups(c.k)
        assert [f["groups"] for f in c.folds] == [list(g) for g in c.fold_groups]
        assert list(c.model.groups) == list(c.canonical_groups)
    entry = cands[2].to_entry()
    assert entry["folds_agree"] == sum(g == cands[2].canonical_groups for g in cands[2].fold_groups)


def test_a_wrong_number_of_fold_subsets_is_refused(training):
    """#61 R1 F-2: never truncate the fold subsets silently."""
    with pytest.raises(ValueError, match="3 fold subsets for 5 folds"):
        models.evaluate_candidate(training, "rfe", 1, ("grade",), fold_groups=[("grade",)] * 3)
    with pytest.raises(ValueError, match="k = 2"):
        models.evaluate_candidate(training, "rfe", 2, ("grade", "lat"),
                                  fold_groups=[("grade",)] * 5)


def test_run_path_methods_times_every_method(training):
    cands, paths, timing = selection.run_path_methods(training, methods=("rfe", "lasso_path"))
    assert set(cands) == set(timing) == {"rfe", "lasso_path"}
    for t in timing.values():
        assert len(t["selection_folds"]) == 5 and t["selection_training"] >= 0
        assert t["total"] >= t["selection"] >= 0 and t["evaluation"] >= 0
