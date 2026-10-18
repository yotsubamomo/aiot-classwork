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
    md, _ = fixture_model_data
    assert md["meta"]["fixture"] is True
    assert {"meta", "preprocess", "inputs", "test_inputs", "baselines", "winners", "test"} <= set(md)
    assert contract.test_field_paths(md["baselines"]) == []
    assert contract.test_field_paths(md.get("methods", {})) == []
    contract.validate_model_data(md)


def test_allin_entry_has_cv_in_usd_and_fit_on_the_log_scale(fixture_model_data):
    md, _ = fixture_model_data
    allin = md["baselines"]["allin"]
    assert allin["cv"]["scale"] == "USD" and allin["fit"]["scale"] == "log"
    fit = allin["fit"]
    assert len(fit["xtx_inv"]) == fit["n_columns"] == len(fit["coef"]) == fit["rank"]
    assert fit["adj_r2_log"] == pytest.approx(
        1 - (1 - fit["r2_log"]) * (fit["n_train"] - 1) / (fit["n_train"] - fit["rank"]))
    assert fit["zipcode_baseline"] == fit["zipcode_categories"][0]


def test_ols_subset_keys_equal_the_authorized_set_and_metric_only_is_absent(fixture_model_data):
    md, _ = fixture_model_data
    w = md["winners"]
    assert w["complete"] and w["overall"]["model_key"] in w["authorized_test_models"]
    ols_keys = {k for k, v in md["test"].items() if v["kind"] == "ols_subset"}
    assert ols_keys == set(w["authorized_test_models"])
    assert "allin" in ols_keys
    assert {m["model_key"] for m in w["method_winners"].values()} <= ols_keys
    assert all(md["test"][k]["kind"] == "ols_subset" for k in md["test"])   # no Ridge/Lasso yet


def test_independent_recomputation_of_every_test_row(fixture_model_data):
    md, _ = fixture_model_data
    actual = np.array([r[-1] for r in md["test_inputs"]["rows"]], dtype=float)
    assert md["test_inputs"]["fields"][-1] == "actual_price"
    for key, entry in md["test"].items():
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
])
def test_contract_violations_are_rejected(fixture_model_data, tamper, needle):
    md = copy.deepcopy(fixture_model_data[0])
    tamper(md)
    with pytest.raises(contract.ContractError, match=needle):
        contract.validate_model_data(md)
