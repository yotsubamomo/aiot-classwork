"""The tracked official model_data (run the notebook first).

Training-side sections are checked against fresh computations on the training rows (the data stage
returns only training rows and test identifiers). The ``test_inputs`` rows and ``test`` come from
the one-time official evaluation of #63 (DA TR-01): they are checked here as exported data —
identifiers against the split, contract invariants, and the independent numpy recomputation of
every row of every ``ols_subset`` model (SR-02) — and nothing here loads an official test row from
the data file or scores any model on it."""
import csv
import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from hw2 import comparison, contract, data, export, preprocess, testgate
from hw2.paths import MODEL_DATA_JS, MODEL_DATA_JSON, SPLIT_ASSIGNMENT_CSV
from test_test_section import _design

TOL = 1e-6


@pytest.fixture(scope="module")
def official():
    assert MODEL_DATA_JSON.is_file() and MODEL_DATA_JS.is_file(), "run hw2.ipynb first"
    from_json = json.loads(MODEL_DATA_JSON.read_text(encoding="utf-8"))
    from_js = export.parse_js(MODEL_DATA_JS.read_text(encoding="utf-8"))
    return from_json, from_js


def test_json_and_js_hold_the_same_object(official):
    from_json, from_js = official
    assert from_json == from_js


def test_meta_reproduction_fields(official):
    meta = official[0]["meta"]
    assert meta["fixture"] is False
    assert meta["csv_sha256"] == data.EXPECTED_SHA256
    assert meta["seed"] == 42
    assert meta["split"]["test_fraction"] == 0.2
    assert meta["split"]["n_train"] + meta["split"]["n_test"] == 21613
    assert meta["cv"]["n_folds"] == 5 and sum(meta["cv"]["fold_rows"]) == meta["split"]["n_train"]
    assert {"python", "numpy", "pandas", "scipy", "scikit-learn"} <= set(meta["versions"])
    assert all(meta["versions"][k] for k in meta["versions"])
    assert set(meta["timing_s"]) >= {"data_load_validate", "split_and_folds"}
    assert all(v >= 0 for v in meta["timing_s"].values())
    assert (meta["n_rows"], meta["n_unique_ids"], meta["n_repeat_sales"]) == (21613, 21436, 177)
    assert meta["n_source_features"] == 19 and meta["n_feature_groups"] == 18
    assert meta["source_features"] == list(preprocess.SOURCE_FEATURES)
    assert meta["feature_groups"] == list(preprocess.FEATURE_GROUPS)
    assert meta["dataset"]["url"] and meta["dataset"]["license"]


def test_sections_and_no_test_field_outside_test(official):
    """TK-4: `methods` and every `baselines` entry hold no test field; the contract holds."""
    md = official[0]
    assert set(md) == {"meta", "preprocess", "inputs", "test_inputs", "methods", "baselines",
                       "winners", "test"}
    assert set(md["baselines"]) == {"allin", "ridge", "lasso", "pvalue_backward"}
    assert contract.test_field_paths(md["baselines"]) == []
    assert contract.test_field_paths(md["methods"]) == []
    contract.validate_model_data(md)


def test_test_keys_are_the_authorized_set_plus_ridge_and_lasso(official):
    """Spec invariants: ols_subset keys = the authorized list; metric_only = Ridge and Lasso only;
    PI fields present exactly for ols_subset; Ridge/Lasso scored with their training-CV alpha."""
    md = official[0]
    test = md["test"]
    ols_keys = {k for k, v in test.items() if v["kind"] == "ols_subset"}
    metric = {k for k, v in test.items() if v["kind"] == "metric_only"}
    assert ols_keys == set(md["winners"]["authorized_test_models"])
    assert metric == {"ridge", "lasso"} and set(test) == ols_keys | metric
    for k in ols_keys:
        assert {"predicted", "lower", "upper", "covered", "coverage"} <= set(test[k])
    for k in metric:
        assert set(test[k]) == contract.METRIC_ONLY_TEST_KEYS
        assert test[k]["alpha"] == md["baselines"][k]["alpha"]
        assert test[k]["scale"] == "USD" and test[k]["n_test"] == md["meta"]["split"]["n_test"]


def test_test_inputs_are_the_split_test_rows(official, prepared_real):
    """SR-02, SR-08, SR-07: one row per test sale in CSV row order, identifiers equal to the split;
    house and repeat-sale counts; rows encoded with an unseen zipcode counted."""
    ti = official[0]["test_inputs"]
    assert ti["written"] is True and ti["n_rows"] == prepared_real.n_test
    assert ti["fields"] == list(contract.TEST_INPUT_FIELDS)
    rows = [dict(zip(ti["fields"], r)) for r in ti["rows"]]
    assert [r["row"] for r in rows] == sorted(prepared_real.test_rows.tolist())
    order = np.argsort(prepared_real.test_rows)
    assert [r["id"] for r in rows] == prepared_real.test_ids[order].tolist()
    ids = [r["id"] for r in rows]
    assert ti["n_houses"] == len(set(ids)) and ti["n_repeat_sales"] == len(ids) - len(set(ids))
    known = set(prepared_real.training["zipcode"].astype(str))
    assert ti["n_unseen_zipcode"] == sum(1 for r in rows if r["zipcode"] not in known)
    assert all(r["actual_price"] > 0 for r in rows)
    assert not set(ids) & set(prepared_real.training["id"])          # grouped split


def test_independent_recomputation_of_every_official_test_row(official):
    """SR-02 (Spec 主 seam): numpy from the raw test_inputs values, the preprocess rules and each
    model's fit reproduces every point prediction and PI (1e-6 USD) and every covered flag; the
    coverage statistics follow. This path calls no hw2 prediction function."""
    md = official[0]
    entries = contract.model_entries(md)
    actual = np.array([r[-1] for r in md["test_inputs"]["rows"]], dtype=float)
    n_models = 0
    for key, t in md["test"].items():
        if t["kind"] != "ols_subset":
            continue
        fit = entries[key]["fit"]
        D = _design(md, fit)
        yhat = D @ np.array(fit["coef"])
        lev = np.einsum("ij,jk,ik->i", D, np.array(fit["xtx_inv"]), D)
        half = fit["t_crit"] * np.sqrt(fit["s2"] * (1.0 + lev))
        point, lower, upper = np.exp(yhat), np.exp(yhat - half), np.exp(yhat + half)
        np.testing.assert_allclose(t["predicted"], point, rtol=0, atol=TOL)
        np.testing.assert_allclose(t["lower"], lower, rtol=0, atol=TOL)
        np.testing.assert_allclose(t["upper"], upper, rtol=0, atol=TOL)
        covered = (lower <= actual) & (actual <= upper)
        assert t["covered"] == covered.tolist()
        assert t["n_covered"] == int(covered.sum()) and t["n_test"] == actual.size
        assert t["coverage"] == pytest.approx(covered.mean(), abs=1e-12)
        assert t["mean_width"] == pytest.approx(np.mean(upper - lower), rel=1e-12)
        p = covered.mean()
        assert t["coverage_uncertainty"]["half_width_95"] == pytest.approx(
            1.96 * np.sqrt(p * (1 - p) / actual.size))
        err = point - actual
        assert t["rmse"] == pytest.approx(np.sqrt(np.mean(err ** 2)), rel=1e-9)
        assert t["mae"] == pytest.approx(np.mean(np.abs(err)), rel=1e-9)
        assert t["r2"] == pytest.approx(
            1 - np.sum(err ** 2) / np.sum((actual - actual.mean()) ** 2), rel=1e-9)
        n_models += 1
    assert n_models == len(md["winners"]["authorized_test_models"])


def test_the_one_time_evaluation_is_recorded(official, prepared_real):
    """G-3: the manifest names the frozen selection (its digest recomputed from the exported
    winners and alphas), the official data, the test rows and one evaluation."""
    md = official[0]
    te = md["meta"]["test_evaluation"]
    m = te["manifest"]
    alphas = {k: md["baselines"][k]["alpha"] for k in ("ridge", "lasso")}
    assert m["official_data"] is True and m["data_sha256"] == data.EXPECTED_SHA256
    assert m["selection_digest"] == testgate.selection_digest(md["winners"], alphas)
    assert m["authorized_test_models"] == md["winners"]["authorized_test_models"]
    assert m["metric_only_alphas"] == alphas
    assert m["n_test"] == prepared_real.n_test and m["evaluations_in_this_run"] == 1
    positions = ",".join(str(int(r)) for r in sorted(prepared_real.test_rows))
    assert m["test_rows_digest"] == hashlib.sha256(positions.encode("ascii")).hexdigest()
    assert te["opened_at"] == m["opened_at"] <= m["evaluated_at"] == te["evaluated_at"]
    assert te["code_revision"]["commit"] and te["code_revision"]["package_modified"] is False
    timing = md["meta"]["timing_s"]
    assert {"ridge_total", "lasso_total", "pvalue_backward_total", "test_load_test_rows",
            "test_score"} <= set(timing)


def test_ridge_lasso_and_pvalue_are_reproduced_from_the_training_rows(official, prepared_real):
    """G-1 on the official data: the alphas, their CV curves and the p-value comparison come from
    the training rows only (a fresh computation on the training rows reproduces them)."""
    base = official[0]["baselines"]
    for name in comparison.METRIC_ONLY:
        fresh = json.loads(json.dumps(
            comparison.select_alpha(prepared_real.training, name).to_entry()))
        assert base[name]["alpha"] == fresh["alpha"]
        assert base[name]["alpha_grid"] == fresh["alpha_grid"]
        for a, b in zip(base[name]["cv_by_alpha"], fresh["cv_by_alpha"]):
            assert a["rmse"] == pytest.approx(b["rmse"], rel=1e-9)
        assert base[name]["cv"]["mean"] == pytest.approx(fresh["cv"]["mean"], rel=1e-9)
        assert base[name]["adj_r2_log"] is None                       # not applicable
    pv = json.loads(json.dumps(comparison.evaluate_pvalue_backward(prepared_real.training)))
    tracked = base["pvalue_backward"]
    assert tracked["canonical_groups"] == pv["canonical_groups"]
    assert tracked["fold_groups"] == pv["fold_groups"]
    assert tracked["cv"]["mean"] == pytest.approx(pv["cv"]["mean"], rel=1e-9)
    assert "pvalue_backward" not in official[0]["winners"]["authorized_test_models"]


def _read_csv(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _same(cell, value):
    if isinstance(value, bool):
        return cell == str(value)
    if isinstance(value, (int, float)):
        return float(cell) == pytest.approx(float(value), rel=1e-12, abs=0)
    return cell == ("" if value is None else str(value))


def test_result_tables_equal_model_data(official):
    """DA TK-2: the CSV result tables are the model_data numbers, training CV (``cv_*``) and Test
    (``test_*``) in separate columns (G-4)."""
    md = official[0]
    for name, rows in (("cv_by_method_k.csv", export.cv_rows(md)),
                       ("comparison.csv", export.comparison_rows(md)),
                       ("alpha_cv.csv", export.alpha_rows(md))):
        table = _read_csv(export.TABLES_DIR / name)
        assert len(table) == len(rows), name
        for got, want in zip(table, rows):
            assert list(got) == list(want), name
            for k, v in want.items():
                assert _same(got[k], v), (name, k, got[k], v)
    comp = _read_csv(export.TABLES_DIR / "comparison.csv")
    metric_cols = [c for c in comp[0] if any(m in c for m in ("mae", "mse", "rmse", "r2_usd"))]
    assert metric_cols and all(c.startswith(("cv_", "test_")) for c in metric_cols)
    by_method = {r["method"]: r for r in comp}
    for name in ("ridge", "lasso"):
        assert by_method[name]["adj_r2_log_full_training_fit"] == "not applicable"
        assert by_method[name]["test_coverage"].startswith("not applicable")
    assert by_method["pvalue_backward"]["test_rmse_usd"].startswith("not evaluated")


def test_meta_matches_the_data_stage(official, prepared_real):
    meta = official[0]["meta"]
    assert meta["split"]["n_train"] == prepared_real.n_train
    assert meta["split"]["n_test"] == prepared_real.n_test
    folds = prepared_real.training["fold"].value_counts().sort_index().tolist()
    assert meta["cv"]["fold_rows"] == folds


def test_inputs_and_fit_come_from_the_training_rows(official, prepared_real):
    md = official[0]
    assert md["inputs"] == json.loads(json.dumps(
        preprocess.training_input_ranges(prepared_real.training)))
    fit = preprocess.fit_preprocessor(prepared_real.training).to_dict()
    assert md["preprocess"]["training_fit"] == fit
    assert md["inputs"]["n_rows"] == prepared_real.n_train


def test_split_assignment_holds_identifiers_only(prepared_real):
    assert SPLIT_ASSIGNMENT_CSV.is_file(), "split assignment missing: run hw2.ipynb"
    table = pd.read_csv(SPLIT_ASSIGNMENT_CSV, dtype={"id": "str"})
    assert list(table.columns) == ["row", "id", "set", "fold"]
    assert table["row"].tolist() == list(range(21613))
    test = table[table["set"] == "test"]
    assert test["row"].tolist() == prepared_real.test_rows.tolist()
    assert test["fold"].isna().all()
    train = table[table["set"] == "train"]
    assert train["fold"].astype(int).tolist() == prepared_real.training["fold"].tolist()


def test_allin_baseline_is_reproduced_from_the_training_rows(official, prepared_real):
    """baselines.allin equals a fresh fit on the training rows (no test row is involved)."""
    from hw2 import models
    tracked = official[0]["baselines"]["allin"]
    fresh = json.loads(json.dumps(models.fit_allin(prepared_real.training).to_entry()))
    assert tracked["canonical_groups"] == fresh["canonical_groups"]
    assert tracked["status"] == fresh["status"] == {"state": "valid", "reason": None}
    for m in ("mae", "mse", "rmse", "r2"):
        assert tracked["cv"]["mean"][m] == pytest.approx(fresh["cv"]["mean"][m], rel=1e-9)
    for key in ("n_train", "n_columns", "rank", "df_resid", "encoded_columns",
                "zipcode_categories", "zipcode_baseline"):
        assert tracked["fit"][key] == fresh["fit"][key], key
    assert tracked["fit"]["n_train"] == prepared_real.n_train
    assert tracked["fit"]["coef"] == pytest.approx(fresh["fit"]["coef"], rel=1e-9, abs=1e-12)


def test_methods_hold_every_k_for_every_path_method(official):
    md = official[0]
    assert list(md["methods"]) == list(models_mod().PATH_METHODS)
    for method, items in md["methods"].items():
        assert [e["k"] for e in items] == list(range(1, 19))
        assert all(len(e["canonical_groups"]) == e["k"] for e in items)
        assert all(len(g) == e["k"] for e in items for g in e["fold_groups"])
        assert all(e["cv"]["n_folds"] == md["meta"]["cv"]["n_folds"] for e in items)
    assert set(md["meta"]["path_timing_s"]) == set(md["methods"])
    for m, t in md["meta"]["path_timing_s"].items():
        assert len(t["selection_folds"]) == 5 and t["total"] > 0
        assert md["meta"]["timing_s"][f"path_{m}"] == t["total"]


def test_winners_are_complete_and_never_metric_only(official):
    """G-2 (CC-1 (2)): neither a method winner nor the overall winner is Ridge or Lasso."""
    w = official[0]["winners"]
    assert w["complete"] is True and w["pending_methods"] == []
    assert set(w["method_winners"]) == {"forward_sfs", "backward_sfs", "rfe", "lasso_path"}
    named = {x["model_key"] for x in w["method_winners"].values()}
    named |= {x["test_model_key"] for x in w["method_winners"].values()}
    named |= {w["overall"]["model_key"], w["overall"]["test_model_key"]}
    named |= set(w["authorized_test_models"])
    assert not named & {"ridge", "lasso"}
    assert "allin" in w["authorized_test_models"]


def models_mod():
    from hw2 import models
    return models


def test_canonical_paths_are_reproduced_from_the_training_rows(official, prepared_real):
    """The canonical subsets equal a fresh selection on the training rows (no test row)."""
    from hw2 import selection
    md = official[0]
    for method, items in md["methods"].items():
        fresh = selection.PATH_FUNCTIONS[method](prepared_real.training).subsets
        assert [tuple(e["canonical_groups"]) for e in items] == list(fresh), method


def test_overall_winner_cv_is_reproduced_from_the_training_rows(official, prepared_real):
    """Re-run the overall CV winner's method on the folds (fold-internal) and re-evaluate it."""
    from hw2 import models, selection
    md = official[0]
    overall = md["winners"]["overall"]
    if overall["method"] == "allin":
        pytest.skip("the overall CV winner is the All-in baseline (reproduced elsewhere)")
    paths = selection.method_paths(prepared_real.training, overall["method"])
    entry = contract.model_entries(md)[overall["model_key"]]
    k = entry["k"]
    assert [list(g) for g in paths.fold_groups(k)] == entry["fold_groups"]
    fresh = models.evaluate_candidate(prepared_real.training, overall["method"], k,
                                      paths.canonical.subsets[k - 1], paths.fold_groups(k))
    for m in ("mae", "mse", "rmse", "r2"):
        assert entry["cv"]["mean"][m] == pytest.approx(fresh.cv()["mean"][m], rel=1e-9)
    assert overall["cv_rmse"] == pytest.approx(fresh.cv_rmse, rel=1e-9)
