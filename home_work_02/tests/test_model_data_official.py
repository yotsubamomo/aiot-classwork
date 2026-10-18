"""The tracked official model_data after the data stage (run the notebook first).

Checks the sections written so far against the data stage, which itself returns only training rows
and test identifiers. Nothing here loads an official test row (DA TR-01)."""
import json

import pandas as pd
import pytest

from hw2 import contract, data, export, preprocess
from hw2.paths import MODEL_DATA_JS, MODEL_DATA_JSON, SPLIT_ASSIGNMENT_CSV


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


def test_no_test_rows_and_no_test_results_are_tracked(official):
    md = official[0]
    assert "test" not in md
    assert md["test_inputs"]["rows"] == [] and md["test_inputs"]["written"] is False
    contract.validate_test_inputs(md["test_inputs"], n_test=md["meta"]["split"]["n_test"])
    assert set(md) == {"meta", "preprocess", "inputs", "test_inputs", "methods", "baselines",
                       "winners"}
    assert contract.test_field_paths(md["baselines"]) == []
    assert contract.test_field_paths(md["methods"]) == []
    contract.validate_model_data(md)


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
