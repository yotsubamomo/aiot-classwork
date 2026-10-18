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
    assert set(md) == {"meta", "preprocess", "inputs", "test_inputs"}


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
