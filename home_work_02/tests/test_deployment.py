"""Deployment (#64): the final model, ``predict_price()`` and the pickle demonstration.

Spec rev 5 「特徵選擇與模型」 (final model = the overall CV winner refitted on the whole training set);
Brief §8 (Q24, Q25). ``predict_price()`` is checked against a direct computation from the model's
``fit`` (coefficients, s², t, (XᵀX)⁻¹) that encodes the raw rows itself (it does not call any hw2
preprocessing or prediction function). Synthetic data, or the training rows of the real data; no
test row is used (DA TR-01)."""
import dataclasses
import json
import pickle
from datetime import date

import numpy as np
import pandas as pd
import pytest

from hw2 import data, deployment, diagnostics, explain, fixture, models, preprocess
from hw2.paths import FINAL_MODEL_PICKLE, MODEL_DATA_JSON, UNIT_DIR


def _load(path, frame):
    return data.load_and_split(path, expected_sha256=data.file_sha256(path),
                               expected_rows=len(frame),
                               expected_unique_ids=frame["id"].nunique())


def small_selection(prepared):
    """All-in, stand-in path candidates (fixture.FIXTURE_SUBSETS) and complete winners."""
    allin = models.fit_allin(prepared.training)
    cands = {m: [models.evaluate_candidate(prepared.training, m, len(s), s) for s in subsets]
             for m, subsets in fixture.FIXTURE_SUBSETS.items()}
    winners = models.determine_winners(allin, cands)
    return allin, cands, winners


@pytest.fixture(scope="module")
def run(tmp_path_factory):
    frame = fixture.synthetic_sales(n_houses=900, n_repeats=40, seed=13)
    path = tmp_path_factory.mktemp("dep") / "s.csv"
    frame.to_csv(path, index=False)
    prepared = _load(path, frame)
    allin, cands, winners = small_selection(prepared)
    pipe = deployment.final_model(prepared, winners, allin, cands)
    return {"frame": frame, "prepared": prepared, "allin": allin, "cands": cands,
            "winners": winners, "pipe": pipe}


def _days(text: str, base_iso: str) -> int:
    text = str(text)
    if "-" in text:
        y, m, d = map(int, text.split("-"))
    else:
        y, m, d = int(text[:4]), int(text[4:6]), int(text[6:8])
    by, bm, bd = map(int, base_iso.split("-"))
    return (date(y, m, d) - date(by, bm, bd)).days


def direct(fit: dict, rows: list, base_iso: str):
    """Point, lower, upper (USD) straight from `fit` for raw rows (own encoding)."""
    X = []
    for raw in rows:
        x = [1.0]
        for col in fit["encoded_columns"]:
            if col == "sale_days":
                x.append(_days(raw["date"], base_iso))
            elif col == "is_renovated":
                x.append(1.0 if raw["yr_renovated"] > 0 else 0.0)
            elif col == "yr_renovated_effective":
                x.append(raw["yr_renovated"] if raw["yr_renovated"] > 0 else raw["yr_built"])
            elif col.startswith("zipcode_"):
                x.append(1.0 if str(raw["zipcode"]) == col[len("zipcode_"):] else 0.0)
            else:
                x.append(float(raw[col]))
        X.append(x)
    X = np.array(X)
    yhat = X @ np.array(fit["coef"])
    lev = np.einsum("ij,jk,ik->i", X, np.array(fit["xtx_inv"]), X)
    half = fit["t_crit"] * np.sqrt(fit["s2"] * (1.0 + lev))
    return np.exp(yhat), np.exp(yhat - half), np.exp(yhat + half)


BASE = preprocess.preprocess_rules()["date"]["base_date"]


def constructed_rows(pipe):
    """Artificial raw rows: ISO and CSV dates, renovated and not, a seen and an unseen zipcode."""
    seen = pipe.preprocessor.zipcode_categories[-1] if pipe.preprocessor.zipcode_categories else "98001"
    base = {"date": "2015-02-10", "bedrooms": 3, "bathrooms": 2.0, "sqft_living": 1900,
            "sqft_lot": 6000, "floors": 1.0, "waterfront": 0, "view": 0, "condition": 3,
            "grade": 7, "sqft_above": 1500, "yr_built": 1978, "yr_renovated": 0, "zipcode": seen,
            "lat": 47.55, "long": -122.2, "sqft_living15": 1800, "sqft_lot15": 6000}
    return [base,
            dict(base, date="20140720T000000", yr_renovated=2005, grade=9, zipcode="98999"),
            dict(base, sqft_living=40000, sqft_above=38000, waterfront=1, view=4)]


# --- the final model ------------------------------------------------------------------------

def test_final_model_is_the_overall_cv_winner_refitted_on_the_training_rows(run):
    pipe, winners, prepared = run["pipe"], run["winners"], run["prepared"]
    overall = winners["overall"]
    by_key = {run["allin"].key: run["allin"]}
    by_key.update({c.key: c for cs in run["cands"].values() for c in cs})
    cand = by_key[overall["model_key"]]
    assert pipe.model_key == overall["model_key"] and (pipe.method, pipe.k) == (cand.method, cand.k)
    assert pipe.test_model_key == overall["test_model_key"]
    assert pipe.groups == tuple(cand.canonical_groups)
    assert np.array_equal(pipe.fit.coef, cand.model.fit.coef)
    assert np.array_equal(pipe.fit.xtx_inv, cand.model.fit.xtx_inv)
    assert pipe.n_train == prepared.n_train and pipe.data_sha256 == prepared.sha256
    assert pipe.fit_dict() == cand.model.to_fit_dict()
    # D-2: the other winners that are the same fitted model are listed, never merged in
    same = [w for w in winners["method_winners"].values()
            if w["test_model_key"] == overall["test_model_key"] and w["model_key"] != pipe.model_key]
    assert len(pipe.shared_with) >= len(same)
    assert pipe.label.startswith(models.METHOD_LABELS[pipe.method])


def test_final_model_refuses_an_incomplete_selection(run):
    incomplete = dict(run["winners"], complete=False)
    with pytest.raises(deployment.DeploymentError, match="overall CV winner"):
        deployment.final_model(run["prepared"], incomplete, run["allin"], run["cands"])


def test_the_training_rows_guard_rejects_a_test_row(run):
    prepared = run["prepared"]
    bad = prepared.training.copy()
    bad.loc[bad.index[0], "row"] = int(prepared.test_rows[0])
    with pytest.raises(deployment.DeploymentError, match="test row"):
        deployment.training_rows(dataclasses.replace(prepared, training=bad))
    with pytest.raises(deployment.DeploymentError):
        deployment.training_rows(dataclasses.replace(prepared,
                                                     training=prepared.training.drop(columns="fold")))


# --- predict_price() ------------------------------------------------------------------------

def test_predict_price_equals_the_direct_computation_from_fit(run):
    """AC: constructed rows and training rows; point and PI equal the values computed from fit."""
    pipe = run["pipe"]
    fit = pipe.fit_dict()
    rows = constructed_rows(pipe)
    training = run["prepared"].training.head(25)
    train_rows = training.to_dict("records")
    for batch in (rows, train_rows):
        out = deployment.predict_price(batch, pipe)
        point, lower, upper = direct(fit, batch, BASE)
        np.testing.assert_allclose(out["predicted_price"], point, rtol=1e-12, atol=0)
        np.testing.assert_allclose(out["pi_lower"], lower, rtol=1e-12, atol=0)
        np.testing.assert_allclose(out["pi_upper"], upper, rtol=1e-12, atol=0)
        assert (out["pi_lower"] < out["predicted_price"]).all()
        assert (out["predicted_price"] < out["pi_upper"]).all()
        assert (out["pi_level"] == 0.95).all()
    # the same training rows as a DataFrame give the same numbers as the fitted model itself
    same = pipe.predict_price(training)
    point, lower, upper, _ = pipe.model.predict_usd(training)
    np.testing.assert_allclose(same["predicted_price"], point, rtol=1e-15)
    np.testing.assert_allclose(same[["pi_lower", "pi_upper"]].to_numpy().T, [lower, upper], rtol=1e-15)


def test_predict_price_flags_unseen_zipcode_and_extrapolation(run):
    pipe = run["pipe"]
    out = deployment.predict_price(constructed_rows(pipe), pipe)
    if "zipcode" in pipe.groups:
        assert out["unseen_zipcode"].tolist() == [False, True, False]
    assert out["out_of_training_range"].iloc[0] == ""
    assert "sqft_living" in out["out_of_training_range"].iloc[2] or \
        "sqft_living" not in pipe.uses_source_features
    # every row is still predicted (extrapolation is flagged, not refused)
    assert np.isfinite(out[["predicted_price", "pi_lower", "pi_upper"]].to_numpy()).all()


def test_predict_price_flags_values_below_the_training_minimum(run):
    """#64 R1 F-1 (1): extrapolation below the training lower bound is flagged too (still predicted)."""
    pipe = run["pipe"]
    numeric = [f for f in pipe.uses_source_features
               if pipe.input_ranges[f].get("kind") not in ("nominal", "date") and f != "yr_renovated"]
    assert numeric, "the synthetic final model uses at least one numeric source feature"
    base = constructed_rows(pipe)[0]
    for name in numeric:
        low = dict(base, **{name: pipe.input_ranges[name]["min"] - 1})
        out = deployment.predict_price([base, low], pipe)
        assert out["out_of_training_range"].iloc[0] == ""
        assert name in out["out_of_training_range"].iloc[1].split(", ")
        assert np.isfinite(out[["predicted_price", "pi_lower", "pi_upper"]].to_numpy()).all()


def test_shared_with_lists_the_allin_baseline_when_the_overall_winner_is_that_model(run):
    """#64 R1 F-1 (2) / DA D-2: an overall winner that is the All-in model (here RFE k = 18 with
    every group) names All-in among the winners it shares its model with."""
    prepared, allin = run["prepared"], run["allin"]
    full = models.evaluate_candidate(prepared.training, "rfe", len(preprocess.FEATURE_GROUPS),
                                     preprocess.FEATURE_GROUPS)
    assert full.valid and full.key != allin.key
    cands = {m: list(cs) for m, cs in run["cands"].items()}
    cands["rfe"].append(full)
    winners = json.loads(json.dumps(run["winners"]))
    winners["allin"] = dict(winners.get("allin") or {}, model_key=allin.key, test_model_key=allin.key)
    winners["method_winners"]["rfe"] = dict(winners["method_winners"]["rfe"], model_key=full.key,
                                            k=full.k, test_model_key=allin.key)
    winners["overall"] = {"model_key": full.key, "method": "rfe", "cv_rmse": full.cv_rmse,
                          "test_model_key": allin.key}
    pipe = deployment.final_model(prepared, winners, allin, cands)
    assert pipe.model_key == full.key and pipe.test_model_key == allin.key
    assert models.METHOD_LABELS[models.ALLIN] in pipe.shared_with
    # the winner itself is never listed as sharing with itself
    assert pipe.label not in pipe.shared_with


def test_predict_price_input_forms_and_errors(run):
    pipe = run["pipe"]
    rows = constructed_rows(pipe)
    as_list = deployment.predict_price(rows, pipe)
    as_frame = deployment.predict_price(pd.DataFrame(rows).assign(price=1.0, id="x"), pipe)
    one = deployment.predict_price(rows[0], pipe)
    pd.testing.assert_frame_equal(as_list, as_frame)
    pd.testing.assert_frame_equal(one, as_list.iloc[:1])
    iso = deployment.predict_price([dict(rows[0], date="20150210T000000")], pipe)
    pd.testing.assert_frame_equal(iso, as_list.iloc[:1])
    missing = {k: v for k, v in rows[0].items() if k != pipe.uses_source_features[0]}
    with pytest.raises(deployment.DeploymentError, match="missing raw input columns"):
        deployment.predict_price(missing, pipe)
    with pytest.raises(deployment.DeploymentError, match="missing values"):
        deployment.predict_price(dict(rows[0], **{pipe.uses_source_features[0]: None}), pipe)
    with pytest.raises(deployment.DeploymentError, match="no rows"):
        deployment.predict_price(pd.DataFrame(columns=list(pipe.uses_source_features)), pipe)


# --- pickle ---------------------------------------------------------------------------------

def test_pickle_round_trip_reproduces_the_prediction(run, tmp_path):
    pipe = run["pipe"]
    path = deployment.save_pipeline(pipe, tmp_path / "final_model.pkl")
    loaded = deployment.load_pipeline(path)
    rows = constructed_rows(pipe)
    pd.testing.assert_frame_equal(loaded.predict_price(rows), pipe.predict_price(rows))
    assert loaded.model_key == pipe.model_key and loaded.groups == pipe.groups
    other = tmp_path / "other.pkl"
    other.write_bytes(pickle.dumps({"not": "a pipeline"}))
    with pytest.raises(deployment.DeploymentError):
        deployment.load_pipeline(other)


def test_non_official_outputs_never_reach_the_unit(run):
    """Fixture pipelines, tables and figures are refused inside the unit (TR-01: no fixture
    result in tracked paths)."""
    pipe = run["pipe"]
    with pytest.raises(deployment.DeploymentError):
        deployment.save_pipeline(pipe, UNIT_DIR / "results" / "deployment" / "x.pkl")
    diag = diagnostics.run(run["prepared"], pipe)
    with pytest.raises(diagnostics.DiagnosticsError):
        diagnostics.write_tables(diag, UNIT_DIR / "results" / "tables")
    with pytest.raises(diagnostics.DiagnosticsError):
        diagnostics.save_figures({}, UNIT_DIR / "results" / "figures")
    coef = explain.coefficient_table(run["prepared"], pipe)
    with pytest.raises(diagnostics.DiagnosticsError):
        explain.write_tables(coef, coef, UNIT_DIR / "results" / "tables")
    assert deployment.is_official_data(run["prepared"]) is False


# --- the official final model (training rows of the real data; the exported fit) ------------

@pytest.fixture(scope="module")
def official_md():
    assert MODEL_DATA_JSON.is_file(), "run hw2.ipynb first"
    return json.loads(MODEL_DATA_JSON.read_text(encoding="utf-8"))


def _overall_entry(md):
    key = md["winners"]["overall"]["model_key"]
    for entries in md["methods"].values():
        for e in entries:
            if e["model_key"] == key:
                return e
    return md["baselines"]["allin"]


def test_the_official_final_model_refit_equals_the_exported_fit(prepared_real, official_md):
    """The overall CV winner's canonical subset refitted on the real training rows reproduces the
    exported `fit` (the model the dashboard and the Test evaluation use)."""
    entry = _overall_entry(official_md)
    model = models.fit_model(deployment.training_rows(prepared_real), entry["canonical_groups"])
    fit = entry["fit"]
    assert list(model.fit.column_names) == fit["coef_names"]
    np.testing.assert_allclose(model.fit.coef, fit["coef"], rtol=1e-12, atol=0)
    np.testing.assert_allclose(model.fit.xtx_inv, fit["xtx_inv"], rtol=1e-12, atol=1e-300)
    assert model.fit.s2 == pytest.approx(fit["s2"], rel=1e-12)


def test_the_tracked_pickle_is_the_official_final_model(official_md):
    assert FINAL_MODEL_PICKLE.is_file(), "run hw2.ipynb first"
    pipe = deployment.load_pipeline(FINAL_MODEL_PICKLE)
    entry = _overall_entry(official_md)
    assert pipe.model_key == official_md["winners"]["overall"]["model_key"] == entry["model_key"]
    assert pipe.test_model_key == official_md["winners"]["overall"]["test_model_key"]
    assert pipe.data_sha256 == data.EXPECTED_SHA256
    assert list(pipe.groups) == entry["canonical_groups"]
    assert pipe.fit_dict()["coef"] == entry["fit"]["coef"]
    assert pipe.fit_dict()["xtx_inv"] == entry["fit"]["xtx_inv"]
    assert pipe.n_train == official_md["meta"]["split"]["n_train"]
    # D-2: presented as the overall CV winner; the other winners scored under the same key are
    # listed as the same fitted model
    w = official_md["winners"]
    labels = {"forward_sfs": "Forward SFS", "backward_sfs": "Backward SFS", "rfe": "RFE",
              "lasso_path": "Lasso 路徑排序"}
    expected = ([models.METHOD_LABELS["allin"]] if w["allin"]["test_model_key"] == pipe.test_model_key
                and pipe.model_key != "allin" else [])
    expected += [f"{labels[m]} · k = {mw['k']}" for m, mw in w["method_winners"].items()
                 if mw["test_model_key"] == pipe.test_model_key and mw["model_key"] != pipe.model_key]
    assert list(pipe.shared_with) == expected
