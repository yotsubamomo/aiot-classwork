"""Main seam: the ``baselines.allin``, ``winners`` and ``test[kind=ols_subset]`` structure of
``model_data``, and the independent recomputation of every test row (SR-02, SR-03; Spec rev 5
Testing Decisions 主 seam).

The recomputation below rebuilds each design row with numpy from the raw values in
``test_inputs``, the rules in ``preprocess`` and the model's ``fit`` (coefficients, categories,
s², df_resid, t, (XᵀX)⁻¹). It does not import or call any hw2 prediction or preprocessing function.
Data: a synthetic fixture written to disk and read back from JSON (DA TR-01)."""
import copy
from datetime import date

import numpy as np
import pandas as pd
import pytest

from hw2 import contract

TOL = 1e-6          # USD, on every row (Spec: 容差 1e-6)


def _days(text: str, base_iso: str) -> int:
    y, m, d = int(text[:4]), int(text[4:6]), int(text[6:8])
    by, bm, bd = map(int, base_iso.split("-"))
    return (date(y, m, d) - date(by, bm, bd)).days


def _design(md: dict, fit: dict) -> np.ndarray:
    """Design rows [1, encoded columns] for every test_inputs row, from the contract only."""
    ti, rules = md["test_inputs"], md["preprocess"]
    base = rules["date"]["base_date"]
    rows = [dict(zip(ti["fields"], r)) for r in ti["rows"]]
    out = np.empty((len(rows), len(fit["coef"])))
    for i, raw in enumerate(rows):
        x = [1.0]
        for col in fit["encoded_columns"]:
            if col == "sale_days":
                x.append(_days(raw["date"], base))
            elif col == "is_renovated":
                x.append(1.0 if raw["yr_renovated"] > 0 else 0.0)
            elif col == "yr_renovated_effective":
                x.append(raw["yr_renovated"] if raw["yr_renovated"] > 0 else raw["yr_built"])
            elif col.startswith("zipcode_"):
                x.append(1.0 if raw["zipcode"] == col[len("zipcode_"):] else 0.0)
            else:
                x.append(float(raw[col]))
        out[i] = x
    return out


def _fit_of(md, key):
    return contract.model_entries(md)[key]["fit"]


def test_sections_and_their_layers(fixture_model_data):
    """TK-4: neither `methods` nor any `baselines` entry (All-in, Ridge, Lasso, p-value) holds a
    test field."""
    md, _ = fixture_model_data
    assert md["meta"]["fixture"] is True
    assert {"meta", "preprocess", "inputs", "test_inputs", "baselines", "winners", "test"} <= set(md)
    assert set(md["baselines"]) == {"allin", "ridge", "lasso", "pvalue_backward"}
    assert contract.test_field_paths(md["baselines"]) == []
    for entry in md["baselines"].values():
        assert contract.test_field_paths(entry) == []
    assert contract.test_field_paths(md.get("methods", {})) == []
    contract.validate_model_data(md)


def test_metric_only_test_metrics_are_the_usd_metrics_of_the_frozen_models(fixture_run,
                                                                         fixture_model_data):
    """CC-1 (5): Ridge/Lasso report MAE, MSE, RMSE, R² in USD only, from the models refitted with
    the training-CV alpha (recomputed here from the in-memory fixture models; their coefficients
    are not exported). No PI, coverage or per-row field."""
    md, _ = fixture_model_data
    ti = md["test_inputs"]
    rows = pd.DataFrame([dict(zip(ti["fields"], r)) for r in ti["rows"]])
    actual = rows["actual_price"].to_numpy(float)
    for name in ("ridge", "lasso"):
        entry = md["test"][name]
        model = fixture_run["metric_only"][name]
        assert model.alpha == entry["alpha"] == md["baselines"][name]["alpha"]
        point = model.predict_usd(rows)
        err = point - actual
        assert entry["rmse"] == pytest.approx(np.sqrt(np.mean(err ** 2)), rel=1e-12)
        assert entry["mae"] == pytest.approx(np.mean(np.abs(err)), rel=1e-12)
        assert entry["r2"] == pytest.approx(
            1 - np.sum(err ** 2) / np.sum((actual - actual.mean()) ** 2), rel=1e-12)
        assert not {"predicted", "lower", "upper", "covered", "coverage"} & set(entry)


def test_unseen_zipcodes_are_counted_per_model(fixture_model_data):
    """SR-07: models with the zipcode group report the test rows encoded as the baseline."""
    md, _ = fixture_model_data
    entries = contract.model_entries(md)
    for key, t in md["test"].items():
        if t["kind"] != "ols_subset":
            continue
        uses = "zipcode" in entries[key]["fit"]["groups"]
        assert t["n_unseen_zipcode"] == (md["test_inputs"]["n_unseen_zipcode"] if uses else 0)


def test_allin_entry_has_cv_in_usd_and_fit_on_the_log_scale(fixture_model_data):
    md, _ = fixture_model_data
    allin = md["baselines"]["allin"]
    assert allin["cv"]["scale"] == "USD" and allin["fit"]["scale"] == "log"
    fit = allin["fit"]
    assert len(fit["xtx_inv"]) == fit["n_columns"] == len(fit["coef"]) == fit["rank"]
    assert fit["adj_r2_log"] == pytest.approx(
        1 - (1 - fit["r2_log"]) * (fit["n_train"] - 1) / (fit["n_train"] - fit["rank"]))
    assert fit["zipcode_baseline"] == fit["zipcode_categories"][0]


def test_ols_subset_keys_equal_the_authorized_set_and_metric_only_is_ridge_and_lasso(
        fixture_model_data):
    md, _ = fixture_model_data
    w = md["winners"]
    assert w["complete"] and w["overall"]["model_key"] in w["authorized_test_models"]
    ols_keys = {k for k, v in md["test"].items() if v["kind"] == "ols_subset"}
    assert ols_keys == set(w["authorized_test_models"])
    assert "allin" in ols_keys
    # each method winner is scored under its test_model_key (a shared model once)
    assert {m["test_model_key"] for m in w["method_winners"].values()} <= ols_keys
    assert w["overall"]["test_model_key"] in ols_keys
    metric = {k: v for k, v in md["test"].items() if v["kind"] == "metric_only"}
    assert sorted(metric) == ["lasso", "ridge"]            # CC-1: exactly Ridge and Lasso
    assert all(set(v) == contract.METRIC_ONLY_TEST_KEYS for v in metric.values())
    assert all(v["alpha"] == md["baselines"][k]["alpha"] for k, v in metric.items())
    assert set(md["test"]) == ols_keys | set(metric)
    assert "pvalue_backward" not in md["test"]


def test_independent_recomputation_of_every_test_row(fixture_model_data):
    md, _ = fixture_model_data
    actual = np.array([r[-1] for r in md["test_inputs"]["rows"]], dtype=float)
    assert md["test_inputs"]["fields"][-1] == "actual_price"
    for key, entry in md["test"].items():
        if entry["kind"] != "ols_subset":
            continue
        fit = _fit_of(md, key)
        D = _design(md, fit)
        yhat = D @ np.array(fit["coef"])
        lev = np.einsum("ij,jk,ik->i", D, np.array(fit["xtx_inv"]), D)
        half = fit["t_crit"] * np.sqrt(fit["s2"] * (1.0 + lev))
        point, lower, upper = np.exp(yhat), np.exp(yhat - half), np.exp(yhat + half)
        np.testing.assert_allclose(entry["predicted"], point, rtol=0, atol=TOL)
        np.testing.assert_allclose(entry["lower"], lower, rtol=0, atol=TOL)
        np.testing.assert_allclose(entry["upper"], upper, rtol=0, atol=TOL)
        covered = (lower <= actual) & (actual <= upper)
        assert entry["covered"] == covered.tolist()
        assert entry["n_covered"] == int(covered.sum()) and entry["n_test"] == actual.size
        assert entry["coverage"] == pytest.approx(covered.mean(), abs=1e-12)
        assert entry["mean_width"] == pytest.approx(np.mean(upper - lower), rel=1e-12)
        err = point - actual
        assert entry["mae"] == pytest.approx(np.mean(np.abs(err)), rel=1e-12)
        assert entry["mse"] == pytest.approx(np.mean(err ** 2), rel=1e-12)
        assert entry["rmse"] == pytest.approx(np.sqrt(np.mean(err ** 2)), rel=1e-12)
        assert entry["r2"] == pytest.approx(
            1 - np.sum(err ** 2) / np.sum((actual - actual.mean()) ** 2), rel=1e-12)
        p = covered.mean()
        half95 = 1.96 * np.sqrt(p * (1 - p) / actual.size)
        assert entry["coverage_uncertainty"]["half_width_95"] == pytest.approx(half95)
        assert "independent" in entry["coverage_uncertainty"]["method"]


def test_test_inputs_counts_houses_and_repeat_sales(fixture_model_data):
    md, _ = fixture_model_data
    ti = md["test_inputs"]
    ids = [r[1] for r in ti["rows"]]
    assert ti["n_rows"] == md["meta"]["split"]["n_test"] == len(ids)
    assert ti["n_houses"] == len(set(ids)) and ti["n_repeat_sales"] == len(ids) - len(set(ids))


@pytest.mark.parametrize("tamper, needle", [
    (lambda md: md["test"]["allin"]["covered"].__setitem__(0, not md["test"]["allin"]["covered"][0]),
     "covered"),
    (lambda md: md["test"]["allin"].__setitem__("coverage", 0.5), "coverage"),
    (lambda md: md["test"].__setitem__("forward_sfs_k01", copy.deepcopy(md["test"]["allin"])),
     "authorized"),
    (lambda md: md["test"].pop("allin"), "authorized"),
    (lambda md: md["test"].__setitem__("ridge", {**copy.deepcopy(md["test"]["allin"]),
                                                 "kind": "metric_only"}), "metric_only"),
    (lambda md: md["baselines"]["allin"]["cv"].__setitem__("test_rmse", 1.0), "test fields"),
    (lambda md: md["baselines"]["allin"]["fit"].__setitem__("predicted", [1.0]), "test fields"),
    (lambda md: md["test"]["allin"]["lower"].__setitem__(0, md["test"]["allin"]["upper"][0] * 2),
     "lower"),
    (lambda md: md["winners"]["authorized_test_models"].append("ridge"), "metric-only"),
    (lambda md: md.pop("test"), "only together with test"),
    (lambda md: md["test"].pop("lasso"), "metric_only entries"),
    (lambda md: [md["test"].pop(k) for k in ("ridge", "lasso")], "metric_only entries"),
    (lambda md: md["test"]["ridge"].__setitem__("alpha", md["test"]["ridge"]["alpha"] * 10),
     "training-CV alpha"),
    (lambda md: md["test"].__setitem__("pvalue_backward", {**copy.deepcopy(md["test"]["ridge"]),
                                                           "model_key": "pvalue_backward"}),
     "metric_only entries|never scored"),
    (lambda md: md["test"]["allin"].__setitem__("n_unseen_zipcode",
                                                md["test"]["allin"]["n_unseen_zipcode"] + 1),
     "SR-07"),
    (lambda md: md["baselines"]["ridge"].__setitem__("fit", {}), "must not hold"),
    (lambda md: md["baselines"]["lasso"]["cv"].__setitem__("test_rmse", 1.0), "test fields"),
    (lambda md: md["baselines"]["pvalue_backward"]["cv"]["folds"][0].__setitem__("n_test", 9),
     "test fields"),
    (lambda md: md["baselines"]["pvalue_backward"].__setitem__("is_cv_winner_candidate", True),
     "never a CV winner"),
])
def test_contract_violations_are_rejected(fixture_model_data, tamper, needle):
    md = copy.deepcopy(fixture_model_data[0])
    tamper(md)
    with pytest.raises(contract.ContractError, match=needle):
        contract.validate_model_data(md)


def test_comparison_rows_keep_training_cv_and_test_apart(fixture_model_data, tmp_path):
    """DA TK-2, G-4, D-2: one row per CV winner under its own identity with the Test numbers of its
    test_model_key (shared models named), then Ridge, Lasso and the p-value comparison; training-CV
    columns come from `cv`, Test columns from `test`; the CSV holds exactly these rows."""
    from hw2 import export
    md, _ = fixture_model_data
    rows = export.comparison_rows(md)
    entries = contract.model_entries(md)
    w = md["winners"]
    winners = [("allin", w["allin"]["model_key"])] + [(m, x["model_key"])
                                                      for m, x in w["method_winners"].items()]
    assert [r["model_key"] for r in rows] == [k for _, k in winners] + \
        ["ridge", "lasso", "pvalue_backward"]
    for r in rows[:len(winners)]:
        e = entries[r["model_key"]]
        t = md["test"][r["test_model_key"]]
        assert r["cv_rmse_usd"] == e["cv"]["mean"]["rmse"] and r["test_rmse_usd"] == t["rmse"]
        assert r["test_coverage"] == t["coverage"] and r["test_n"] == t["n_test"]
        assert e["canonical_groups"] == entries[r["test_model_key"]]["canonical_groups"]
        sharing = [k for _, k in winners if k != r["model_key"] and
                   entries[k]["canonical_groups"] == e["canonical_groups"]]
        assert bool(sharing) == ("same model as" in r["notes"])
    for r, name in zip(rows[len(winners):], ("ridge", "lasso")):
        assert r["cv_rmse_usd"] == md["baselines"][name]["cv"]["mean"]["rmse"]
        assert r["test_rmse_usd"] == md["test"][name]["rmse"]
        assert r["adj_r2_log_full_training_fit"] == "not applicable"
        assert str(r["test_coverage"]).startswith("not applicable")
    assert all(str(v).startswith("not evaluated") for k, v in rows[-1].items()
               if k.startswith("test_") and k != "test_model_key")
    paths = export.write_result_tables(md, tmp_path / "tables")
    assert [p.name for p in paths] == ["cv_by_method_k.csv", "comparison.csv", "alpha_cv.csv"]
    with pytest.raises(export.ExportError):
        export.write_result_tables(md)                    # fixture tables never inside the unit
