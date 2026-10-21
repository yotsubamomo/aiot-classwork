"""V2 Exploratory run: the Node tests of the browser files, driven from pytest (Spec V2 Testing
Decisions; #74 V2-T1, #75 V2-T2).

- 主 seam: :func:`test_node_explore_contract_matches_the_python_reference` generates the reference
  results **now**, with the generic Python reference :mod:`hw2.explore_reference`, for 50 Startups,
  a synthetic non-degenerate dataset (numeric and categorical columns), the small edge cases of
  Spec 主 seam (d) (exactly 20 rows, a single categorical column, all numeric; DA G-2), the A-1
  cases (rank deficiency on one fold's training rows, df_resid < 3, collinear columns, no feature
  group) and the synthetic degenerate dataset of #75 (a column that is the sum of two others, two
  identical columns whose Lasso entries tie, All-in invalid), writes them with the CSV files to a
  pytest temporary directory (nothing is tracked), and runs ``tests/js/explore_contract.test.js`` on
  them. Since #75 every case runs all five methods, so an All-in that is invalid no longer rejects
  the run when a smaller subset is valid (Spec: the run is rejected only when every candidate is
  invalid); the A-1 reasons are checked on the All-in candidate.
- The winner rules are also compared on injected candidate lists (``winner_cases.json``): equal CV
  RMSE within a method → the smaller k; equal CV RMSE between methods → the method order.
- 次 seam: the load contract, the three-layer boundary, the request isolation / predictor tests and
  the #75 method tests (hand-computed aggregation, freezing, Lasso degeneracy, fold boundary of
  the paths, the view helpers) need no reference and run as they are.

Every run must report ``# skipped 0`` and ``# fail 0``.
"""
import json
import os
import shutil
import subprocess

import numpy as np
import pytest

from hw2 import explore_reference as R
from hw2.paths import ASSETS_DIR, UNIT_DIR

NODE = shutil.which("node")
STARTUPS_CSV = ASSETS_DIR / "data" / "50_Startups.csv"


def _num(v: float) -> str:
    return repr(float(v))


def _csv(header, rows) -> bytes:
    lines = [",".join(header)] + [",".join(r) for r in rows]
    return ("\n".join(lines) + "\n").encode("utf-8")


def synthetic_mixed(n=120, seed=74) -> bytes:
    """Non-degenerate: three numeric columns of different scales, two categorical columns."""
    rng = np.random.default_rng(seed)
    a = rng.uniform(0, 100, n)
    b = rng.normal(5000, 1500, n)
    c = rng.uniform(-3, 3, n)
    cat_a = rng.choice(["north", "south", "east", "west"], n)
    cat_b = rng.choice(["low", "mid", "high"], n)
    eff_a = {"north": 0.0, "south": 12.0, "east": -7.0, "west": 3.0}
    eff_b = {"low": -5.0, "mid": 0.0, "high": 9.0}
    y = 2.5 * a + 0.01 * b - 4.0 * c + np.array([eff_a[v] for v in cat_a]) \
        + np.array([eff_b[v] for v in cat_b]) + rng.normal(0, 8, n)
    rows = [[_num(round(a[i], 3)), _num(round(b[i], 2)), _num(round(c[i], 4)), cat_a[i], cat_b[i],
             _num(round(y[i], 3))] for i in range(n)]
    return _csv(["a", "b", "c", "region", "tier", "target"], rows)


def edge_twenty_rows(seed=75) -> bytes:
    rng = np.random.default_rng(seed)
    x1, x2 = rng.uniform(0, 10, 20), rng.uniform(0, 5, 20)
    y = 3 * x1 - x2 + rng.normal(0, 1, 20)
    return _csv(["x1", "x2", "y"], [[_num(round(x1[i], 3)), _num(round(x2[i], 3)),
                                     _num(round(y[i], 3))] for i in range(20)])


def edge_single_categorical(seed=76) -> bytes:
    rng = np.random.default_rng(seed)
    cat = rng.choice(["A", "B", "C"], 40)
    y = np.array([{"A": 10.0, "B": 14.0, "C": 7.0}[v] for v in cat]) + rng.normal(0, 1.5, 40)
    return _csv(["group", "y"], [[cat[i], _num(round(y[i], 3))] for i in range(40)])


def edge_all_numeric(seed=77) -> bytes:
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (60, 4)) * [1, 10, 100, 0.1]
    y = X @ [1.5, -0.2, 0.03, 8.0] + rng.normal(0, 0.5, 60)
    rows = [[_num(round(v, 5)) for v in X[i]] + [_num(round(y[i], 4))] for i in range(60)]
    return _csv(["p", "q", "r", "s", "y"], rows)


def a1_fold_rank_deficient(seed=78, fold=2) -> bytes:
    """`spike` is non-zero only on the validation rows of one fold: it is constant (0) on that
    fold's training rows, so the All-in design is rank deficient there and only there."""
    rng = np.random.default_rng(seed)
    n = 60
    split = R.make_split(n, R.SEED)
    spike_rows = {r for r, f in zip(split["train"], split["folds"]) if f == fold}
    x = rng.uniform(0, 10, n)
    spike = np.array([rng.uniform(1, 2) if i in spike_rows else 0.0 for i in range(n)])
    y = 2 * x + 5 * spike + rng.normal(0, 1, n)
    return _csv(["x", "spike", "y"], [[_num(round(x[i], 3)), _num(round(spike[i], 3)),
                                       _num(round(y[i], 3))] for i in range(n)])


def a1_small_df(seed=79) -> bytes:
    """20 rows, 11 numeric features: every fold's training rows leave df_resid < 3."""
    rng = np.random.default_rng(seed)
    X = rng.normal(0, 1, (20, 11))
    y = X.sum(axis=1) + rng.normal(0, 0.3, 20)
    return _csv([f"f{j}" for j in range(11)] + ["y"],
                [[_num(round(v, 4)) for v in X[i]] + [_num(round(y[i], 4))] for i in range(20)])


def a1_collinear(seed=80) -> bytes:
    """x3 = x1 + x2 exactly (as doubles): rank deficient on every fold and on the training set."""
    rng = np.random.default_rng(seed)
    x1, x2 = np.round(rng.uniform(0, 10, 50), 2), np.round(rng.uniform(0, 10, 50), 2)
    x3 = x1 + x2
    y = x1 - x2 + rng.normal(0, 1, 50)
    return _csv(["x1", "x2", "x3", "y"], [[_num(x1[i]), _num(x2[i]), _num(x3[i]),
                                           _num(round(y[i], 3))] for i in range(50)])


def a1_no_groups() -> bytes:
    """The only feature is constant: no feature group, so no candidate can be valid."""
    return _csv(["k", "y"], [["1", _num(i * 1.5)] for i in range(30)])


def degenerate_mixed(n=80, seed=81) -> bytes:
    """Synthetic degenerate data (Spec 主 seam (c)): ``x_sum = x1 + x2`` exactly (as doubles), and
    ``dup_b`` identical to ``dup_a`` (perfectly collinear; their Lasso entries tie exactly). The
    two identical columns are the weakest predictors, so the Lasso path meets them last and its
    stop does not depend on how a floating-point tie elsewhere is resolved."""
    rng = np.random.default_rng(seed)
    x1, x2 = np.round(rng.uniform(0, 10, n), 2), np.round(rng.uniform(0, 10, n), 2)
    x_sum = x1 + x2
    x4 = np.round(rng.normal(0, 5, n), 3)
    dup = np.round(rng.uniform(-1, 1, n), 3)
    cat = rng.choice(["p", "q", "r"], n)
    eff = {"p": 0.0, "q": 6.0, "r": -4.0}
    y = 3 * x1 - 2 * x2 + 4 * x4 + 0.5 * dup + np.array([eff[c] for c in cat]) \
        + rng.normal(0, 2, n)
    rows = [[_num(x1[i]), _num(x2[i]), _num(x_sum[i]), _num(x4[i]), _num(dup[i]), _num(dup[i]),
             cat[i], _num(round(y[i], 3))] for i in range(n)]
    return _csv(["x1", "x2", "x_sum", "x4", "dup_a", "dup_b", "cat", "y"], rows)


# name -> (CSV bytes, expected run status, degenerate: compared modulo exactly tied twin columns)
CASES = {
    "startups50": (lambda: STARTUPS_CSV.read_bytes(), "COMPLETED"),
    "synthetic_mixed": (synthetic_mixed, "COMPLETED"),
    "edge_twenty_rows": (edge_twenty_rows, "COMPLETED"),
    "edge_single_categorical": (edge_single_categorical, "COMPLETED"),
    "edge_all_numeric": (edge_all_numeric, "COMPLETED"),
    "a1_fold_rank_deficient": (a1_fold_rank_deficient, "COMPLETED"),
    "a1_small_df": (a1_small_df, "COMPLETED"),
    "a1_collinear": (a1_collinear, "COMPLETED"),
    "a1_no_groups": (a1_no_groups, "REJECTED"),
    "degenerate_mixed": (degenerate_mixed, "COMPLETED"),
}
DEGENERATE = {"a1_collinear", "degenerate_mixed"}


def _cand(key, method, k, rmse, groups):
    return {"key": key, "method": method, "k": k, "status": "VALID" if rmse is not None else
            "INVALID_MODEL", "cv": None if rmse is None else {"mean": {"rmse": rmse}},
            "canonical_groups": groups}


# Injected candidate lists for the winner rules (hw2.models.determine_winners), compared Node vs Python.
WINNER_CASES = {
    "method_tie_smaller_k": [
        _cand("allin", "allin", 3, 9.0, ["a", "b", "c"]),
        _cand("forward_sfs_k01", "forward_sfs", 1, 5.0, ["a"]),
        _cand("forward_sfs_k02", "forward_sfs", 2, 4.0, ["a", "b"]),
        _cand("forward_sfs_k03", "forward_sfs", 3, 4.0, ["a", "b", "c"]),
        _cand("backward_sfs_k01", "backward_sfs", 1, 4.5, ["b"]),
        _cand("backward_sfs_k02", "backward_sfs", 2, 4.5, ["b", "c"]),
        _cand("backward_sfs_k03", "backward_sfs", 3, 9.0, ["a", "b", "c"]),
        _cand("rfe_k01", "rfe", 1, None, ["c"]),
        _cand("rfe_k02", "rfe", 2, None, ["a", "c"]),
        _cand("lasso_path_k01", "lasso_path", 1, 6.0, ["a"]),
        _cand("lasso_path_k02", "lasso_path", 2, None, None),
    ],
    "overall_tie_method_order": [
        _cand("allin", "allin", 2, 3.0, ["a", "b"]),
        _cand("forward_sfs_k01", "forward_sfs", 1, 3.0, ["b"]),
        _cand("forward_sfs_k02", "forward_sfs", 2, 3.0, ["a", "b"]),
        _cand("backward_sfs_k01", "backward_sfs", 1, 3.0, ["a"]),
        _cand("rfe_k01", "rfe", 1, 7.0, ["a"]),
        _cand("lasso_path_k01", "lasso_path", 1, 3.0, ["a"]),
    ],
    "allin_invalid_overall_from_paths": [
        _cand("allin", "allin", 2, None, ["a", "b"]),
        _cand("forward_sfs_k01", "forward_sfs", 1, 2.0, ["b"]),
        _cand("backward_sfs_k01", "backward_sfs", 1, 2.0, ["b"]),
        _cand("rfe_k01", "rfe", 1, 1.5, ["a"]),
        _cand("lasso_path_k01", "lasso_path", 1, None, ["a"]),
    ],
}

# Load-contract parity: tricky texts whose Python and JS LoadResults must be identical.
LOAD_CASES = {
    "bom_quotes_space": "﻿\"a\" , b ,\"y, v\"\r\n" + "\r\n".join(
        f" {i}e1 ,\"x, \"\"{i % 3}\"\"\", -{i}.5 " for i in range(22)) + "\r\n\r\n",
    "missing_cells": "a,b,y\n" + "\n".join(f"{i if i % 4 else ''},{'c' if i % 2 else 'd'},{i}"
                                           for i in range(30)),
    "literal_quote_and_multiline": "name,y\n" + "\n".join(f"n{i},{i}" for i in range(22))
                                   + "\n12\" pipe,1\n\"two\nlines\",2\n",
    "not_csv_unterminated": "a,y\n\"x,1\n" + "\n".join(f"{i},{i}" for i in range(25)),
    "no_header": "1,2,3\n" + "\n".join(f"{i},{i},{i}" for i in range(25)),
    "ragged": "a,b,y\n" + "\n".join(f"{i},x,{i}" for i in range(25)) + "\n1,2\n",
    "duplicate": "a, a ,y\n" + "\n".join(f"{i},x,{i}" for i in range(25)),
    "too_few": "a,y\n" + "\n".join(f"{i},{i}" for i in range(19)),
    "target_not_numeric": "a,y\n" + "\n".join(f"{i},v{i}" for i in range(25)),
    "hex_is_categorical": "a,y\n" + "\n".join(("0x1A" if i == 3 else str(i)) + f",{i}"
                                              for i in range(25)),
    "single_column": "only\n" + "\n".join(str(i) for i in range(25)),
}


def _jsonable(obj):
    return json.loads(json.dumps(obj, allow_nan=False))


def write_reference(out):
    """Generate every reference case into the directory `out` (also usable outside pytest)."""
    manifest = {"reference_version": R.REFERENCE_VERSION, "cases": [], "load_cases": [],
                "prng": {"seed": R.SEED, "first": []}, "winner_cases": []}
    nxt = R.mulberry32(R.SEED)
    manifest["prng"]["first"] = [nxt() for _ in range(8)]
    for name, (make, expected) in CASES.items():
        raw = make()
        (out / f"{name}.csv").write_bytes(raw)
        load = R.load_csv(raw)
        assert load["ok"], (name, load)
        result = R.run(load, problem=name)
        assert result["run"]["status"] == expected, (name, result["run"])
        (out / f"{name}.json").write_text(json.dumps(_jsonable({"load": load, "result": result})),
                                          encoding="utf-8")
        manifest["cases"].append({"name": name, "csv": f"{name}.csv", "reference": f"{name}.json",
                                  "expected_status": expected, "degenerate": name in DEGENERATE})
    for name, text in LOAD_CASES.items():
        raw = text.encode("utf-8")
        (out / f"load_{name}.csv").write_bytes(raw)
        manifest["load_cases"].append({"name": name, "csv": f"load_{name}.csv",
                                       "reference": _jsonable(R.load_csv(raw))})
    for name, candidates in WINNER_CASES.items():
        manifest["winner_cases"].append({"name": name, "candidates": candidates,
                                         "winners": _jsonable(R.determine_winners(candidates))})
    (out / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return out


@pytest.fixture(scope="module")
def reference_dir(tmp_path_factory):
    return write_reference(tmp_path_factory.mktemp("explore_reference"))


def _node(script, env=None):
    result = subprocess.run([NODE, "--test", "--test-reporter=tap", script], cwd=UNIT_DIR,
                            env=dict(os.environ, **(env or {})), capture_output=True, text=True,
                            encoding="utf-8")
    assert result.returncode == 0, result.stdout[-6000:] + result.stderr[-3000:]
    assert "# skipped 0" in result.stdout and "# fail 0" in result.stdout, result.stdout[-3000:]
    return result.stdout


@pytest.mark.skipif(NODE is None, reason="node not installed")
def test_node_explore_contract_matches_the_python_reference(reference_dir):
    out = _node("tests/js/explore_contract.test.js", {"HW2_EXPLORE_REFERENCE": str(reference_dir)})
    assert "# pass 0" not in out


@pytest.mark.skipif(NODE is None, reason="node not installed")
@pytest.mark.parametrize("script", ["tests/js/explore_load.test.js",
                                    "tests/js/explore_boundary.test.js",
                                    "tests/js/explore_app.test.js",
                                    "tests/js/explore_methods.test.js"])
def test_node_explore_secondary_seams(script):
    _node(script)


# ---- the reference itself (Python side) --------------------------------------------------------

def _result(reference_dir, name):
    return json.loads((reference_dir / f"{name}.json").read_text(encoding="utf-8"))["result"]


def test_reference_cases_meet_the_contract_invariants(reference_dir):
    """VALID <=> fit <=> CV metrics; covered = lower <= actual <= upper; coverage = covered /
    n_test; test only for the winners (one result per canonical subset); every winner VALID; one
    candidate per (method, k) plus All-in; Lasso k beyond its path is INVALID; REJECTED results
    have no candidates, winners or test."""
    for name in CASES:
        res = _result(reference_dir, name)
        if res["run"]["status"] == "REJECTED":
            assert not {"candidates", "winners", "test"} & set(res), name
            assert res["run"]["reason"] == "ALL_CANDIDATES_INVALID"
            assert all(c["status"] == "INVALID_MODEL" and c["reasons"]
                       for c in res["run"]["invalid_candidates"])
            continue
        p = len(res["groups"])
        keys = [c["key"] for c in res["candidates"]]
        assert keys == ["allin"] + [f"{m}_k{k:02d}" for m in R.PATH_METHODS
                                    for k in range(1, p + 1)], name
        by_key = {c["key"]: c for c in res["candidates"]}
        for c in res["candidates"]:
            assert c["status"] in ("VALID", "INVALID_MODEL")
            assert (c["status"] == "VALID") == (c["fit"] is not None) == (c["cv"] is not None)
            assert (c["status"] == "VALID") == (not c["reasons"])
        w = res["winners"]
        winner_keys = [v["key"] for v in w["method_winners"].values() if v] + [w["overall"]["key"]]
        assert all(by_key[k]["status"] == "VALID" for k in winner_keys)
        assert set(w["test_key_of"]) == set(winner_keys)
        for key, rep in w["test_key_of"].items():
            assert by_key[key]["canonical_groups"] == by_key[rep]["canonical_groups"]
        assert set(res["test"]) == set(w["test_keys"]) == set(w["test_key_of"].values())
        for t in res["test"].values():
            cov = [lo <= a <= hi for a, lo, hi in zip(t["actual"], t["lower"], t["upper"])]
            assert cov == t["covered"]
            assert t["coverage"] == sum(cov) / t["n_test"]
        canon = res["lasso_path"]["canonical"]
        for k in range(1, p + 1):
            c = by_key[f"lasso_path_k{k:02d}"]
            if canon["degenerate"] and k >= canon["first_invalid_k"]:
                assert c["status"] == "INVALID_MODEL" and c["canonical_groups"] is None
                assert {"rule": "lasso_path_degenerate", "scope": "training_set", "fold": None,
                        "n_groups_entered": canon["n_entered"],
                        "cause": canon["cause"]} in c["reasons"]


def test_cv_metrics_are_the_arithmetic_mean_of_the_fold_metrics(reference_dir):
    for name in CASES:
        res = _result(reference_dir, name)
        for c in res.get("candidates", []):
            if c["status"] != "VALID":
                continue
            for m in R.METRICS:
                vals = [f["metrics"][m] for f in c["folds"]]
                if any(v is None for v in vals):
                    continue
                assert c["cv"]["mean"][m] == pytest.approx(sum(vals) / len(vals), rel=1e-12)
                assert c["cv"]["std"][m] == pytest.approx(float(np.std(vals, ddof=1)), rel=1e-12)


def test_changing_test_targets_moves_only_the_test_numbers():
    """Freezing (SR-V2-02): the test rows are read after every decision, for the winners only."""
    raw = synthetic_mixed()
    load = R.load_csv(raw)
    a = R.run(load)
    changed = json.loads(json.dumps(load))
    t = changed["target"]["index"]
    for r in a["split"]["test"]:
        changed["rows"][r][t] = changed["rows"][r][t] * 3 + 1000.0
    b = R.run(changed)
    for key in ("columns", "groups", "split", "dependencies", "lasso_path", "winners"):
        assert _jsonable(b[key]) == _jsonable(a[key]), key
    for ca, cb in zip(a["candidates"], b["candidates"]):
        assert _jsonable({k: v for k, v in cb.items()}) == _jsonable(ca)
    assert all(a["test"][k]["metrics"] != b["test"][k]["metrics"] for k in a["test"])


def test_a1_reasons_name_the_rule_and_the_fold(reference_dir):
    def reasons(name):
        res = _result(reference_dir, name)
        if res["run"]["status"] == "REJECTED":
            return res["run"]["invalid_candidates"][0]["reasons"]
        assert res["candidates"][0]["key"] == "allin"
        return res["candidates"][0]["reasons"]
    assert reasons("a1_fold_rank_deficient") == [
        {"rule": "rank_deficient", "scope": "fold", "fold": 2, "rank": 2, "n_columns": 3,
         "df_resid": reasons("a1_fold_rank_deficient")[0]["df_resid"]}]
    small = reasons("a1_small_df")
    assert small and all(r["rule"] == "df_resid_lt_3" and r["scope"] == "fold" for r in small)
    assert len(small) == 5
    coll = reasons("a1_collinear")
    assert [r["fold"] for r in coll] == [0, 1, 2, 3, 4, None]
    assert all(r["rule"] == "rank_deficient" for r in coll)
    assert reasons("a1_no_groups") == [{"rule": "no_feature_groups", "scope": "training_set",
                                        "fold": None}]
    # All-in invalid, the exploration still completes from the valid smaller subsets
    for name in ("a1_fold_rank_deficient", "a1_small_df", "a1_collinear"):
        res = _result(reference_dir, name)
        assert res["run"]["status"] == "COMPLETED"
        assert res["winners"]["method_winners"]["allin"] is None
        assert res["winners"]["overall"]["method"] != "allin"


def test_startups50_every_candidate_is_valid_and_the_split_is_80_20(reference_dir):
    """Brief V2 §8 第 2 條 / A-1: 「50 Startups 全部 k 有效」 shown by the candidate states."""
    res = _result(reference_dir, "startups50")
    assert res["run"]["status"] == "COMPLETED"
    assert len(res["split"]["test"]) == 10 and len(res["split"]["train"]) == 40
    assert [c["status"] for c in res["columns"]] == ["KEPT", "KEPT", "KEPT", "KEPT", "TARGET"]
    allin = res["candidates"][0]
    assert allin["status"] == "VALID" and allin["k"] == 4
    assert allin["fit"]["levels"]["State"]["baseline"] == "New York"
    states = {c["key"]: c["status"] for c in res["candidates"]}
    assert len(states) == 1 + 4 * 4
    assert set(states.values()) == {"VALID"}, states
    assert res["lasso_path"]["canonical"]["degenerate"] is False
    assert all(not f["degenerate"] for f in res["lasso_path"]["folds"])
    assert res["dependencies"]["relations"] == []


def test_degenerate_fixture_semantics(reference_dir):
    """Spec 主 seam (c), A-2, A-3: Lasso stops after the five groups it can enter; k = 6, 7 are
    INVALID_MODEL / lasso_path_degenerate in every fold and on the training set; the collinear
    subsets are INVALID_MODEL / rank_deficient; the two relations and their feature groups are
    reported; All-in is invalid and the run completes with VALID winners only. No numbers of the
    degenerate situation are asserted."""
    res = _result(reference_dir, "degenerate_mixed")
    assert res["run"]["status"] == "COMPLETED"
    by_key = {c["key"]: c for c in res["candidates"]}
    assert by_key["allin"]["status"] == "INVALID_MODEL"
    assert {r["rule"] for r in by_key["allin"]["reasons"]} == {"rank_deficient"}
    for info in [res["lasso_path"]["canonical"]] + res["lasso_path"]["folds"]:
        assert info["degenerate"] and info["n_entered"] == 5 and info["first_invalid_k"] == 6
        assert "x_sum" in info["not_entered"]
        entered = [e["group"] for e in info["entries"]]
        assert entered[:4] == ["x4", "x1", "x2", "cat"]
        assert len({"dup_a", "dup_b"} & set(entered)) == 1       # one of the tied twins
    for k in (6, 7):
        c = by_key[f"lasso_path_k{k:02d}"]
        assert c["status"] == "INVALID_MODEL"
        assert [(r["rule"], r["fold"]) for r in c["reasons"]] == \
            [("lasso_path_degenerate", f) for f in range(5)] + [("lasso_path_degenerate", None)]
    for c in res["candidates"]:
        groups = set(c["canonical_groups"] or [])
        collinear = {"x1", "x2", "x_sum"} <= groups or {"dup_a", "dup_b"} <= groups
        if collinear:
            assert c["status"] == "INVALID_MODEL"
            assert {r["rule"] for r in c["reasons"]} == {"rank_deficient"}
    rel = res["dependencies"]["relations"]
    assert res["dependencies"]["rank"] == res["dependencies"]["n_columns"] - 2
    assert [r["feature_groups"] for r in rel] == [["x1", "x2", "x_sum"], ["dup_a", "dup_b"]]
    assert [sorted(round(c["coef"], 9) for c in r["columns"]) for r in rel] == [[-1, 1, 1], [-1, 1]]
    assert not any(r["includes_intercept"] for r in rel)
    w = res["winners"]
    assert w["method_winners"]["allin"] is None
    assert all(by_key[v["key"]]["status"] == "VALID" for v in w["method_winners"].values() if v)


def test_winner_rules_on_injected_candidates():
    w = R.determine_winners(WINNER_CASES["method_tie_smaller_k"])
    assert w["method_winners"] == {"allin": {"key": "allin", "k": 3},
                                   "forward_sfs": {"key": "forward_sfs_k02", "k": 2},
                                   "backward_sfs": {"key": "backward_sfs_k01", "k": 1},
                                   "rfe": None, "lasso_path": {"key": "lasso_path_k01", "k": 1}}
    assert w["overall"] == {"method": "forward_sfs", "key": "forward_sfs_k02", "k": 2}
    w = R.determine_winners(WINNER_CASES["overall_tie_method_order"])
    assert w["overall"] == {"method": "allin", "key": "allin", "k": 2}
    assert w["method_winners"]["forward_sfs"] == {"key": "forward_sfs_k01", "k": 1}
    # backward k1 and lasso k1 share the subset ["a"]: one model, scored once under the first key
    assert w["test_keys"] == ["allin", "forward_sfs_k01", "backward_sfs_k01"]
    assert w["test_key_of"]["lasso_path_k01"] == "backward_sfs_k01"
    assert w["test_key_of"]["rfe_k01"] == "backward_sfs_k01"
    w = R.determine_winners(WINNER_CASES["allin_invalid_overall_from_paths"])
    assert w["overall"] == {"method": "rfe", "key": "rfe_k01", "k": 1}
    assert w["method_winners"]["allin"] is None and w["method_winners"]["lasso_path"] is None
    assert w["test_keys"] == ["forward_sfs_k01", "rfe_k01"]


def test_lars_segment_is_the_full_sklearn_path_when_nothing_degenerates():
    """The reference cuts sklearn's path only at a degeneracy; otherwise it is lars_path itself."""
    from sklearn.linear_model import lars_path
    load = R.load_csv(STARTUPS_CSV.read_bytes())
    split = R.make_split(len(load["rows"]))
    groups = R.train_decisions(load, split["train"])["groups"]
    enc = R.fit_encoding(load, groups, split["train"])
    X, _, _ = R.encode_rows(load, enc, split["train"])
    y = R._target(load, split["train"])
    Xs = R.lasso_design(X, [c["level"] is not None for c in enc["columns"]])
    seg = R.lars_segment(Xs, y - y.mean())
    alphas, _, coefs = lars_path(Xs, y - y.mean(), method="lasso")
    assert seg["cause"] is None
    assert np.array_equal(seg["alphas"], alphas) and np.array_equal(seg["coefs"], coefs)


def test_reference_reuses_the_formal_constants():
    from hw2 import models, ols, selection
    assert R.CV_STD_DDOF == models.CV_STD_DDOF
    assert R.PI_LEVEL == ols.PI_LEVEL
    assert R.METHOD_ORDER == models.METHOD_ORDER and R.PATH_METHODS == models.PATH_METHODS
    assert R.TIE_RTOL == selection.TIE_RTOL
