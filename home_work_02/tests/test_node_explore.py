"""V2 Exploratory run: the Node tests of the browser files, driven from pytest (Spec V2 Testing
Decisions; #74 V2-T1).

- 主 seam: :func:`test_node_explore_contract_matches_the_python_reference` generates the reference
  results **now**, with the generic Python reference :mod:`hw2.explore_reference`, for 50 Startups,
  a synthetic non-degenerate dataset (numeric and categorical columns), the small edge cases of
  Spec 主 seam (d) (exactly 20 rows, a single categorical column, all numeric; DA G-2) and the A-1
  cases (rank deficiency on one fold's training rows, df_resid < 3, every candidate invalid, no
  feature group), writes them with the CSV files to a pytest temporary directory (nothing is
  tracked), and runs ``tests/js/explore_contract.test.js`` on them.
- 次 seam: the load contract, the three-layer boundary and the request isolation / predictor tests
  need no reference and run as they are.

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


CASES = {
    "startups50": (lambda: STARTUPS_CSV.read_bytes(), "COMPLETED"),
    "synthetic_mixed": (synthetic_mixed, "COMPLETED"),
    "edge_twenty_rows": (edge_twenty_rows, "COMPLETED"),
    "edge_single_categorical": (edge_single_categorical, "COMPLETED"),
    "edge_all_numeric": (edge_all_numeric, "COMPLETED"),
    "a1_fold_rank_deficient": (a1_fold_rank_deficient, "REJECTED"),
    "a1_small_df": (a1_small_df, "REJECTED"),
    "a1_collinear": (a1_collinear, "REJECTED"),
    "a1_no_groups": (a1_no_groups, "REJECTED"),
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
                "prng": {"seed": R.SEED, "first": []}}
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
                                  "expected_status": expected})
    for name, text in LOAD_CASES.items():
        raw = text.encode("utf-8")
        (out / f"load_{name}.csv").write_bytes(raw)
        manifest["load_cases"].append({"name": name, "csv": f"load_{name}.csv",
                                       "reference": _jsonable(R.load_csv(raw))})
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
                                    "tests/js/explore_app.test.js"])
def test_node_explore_secondary_seams(script):
    _node(script)


# ---- the reference itself (Python side) --------------------------------------------------------

def test_reference_cases_meet_the_contract_invariants(reference_dir):
    """VALID <=> fit; covered = lower <= actual <= upper; coverage = covered / n_test; test only
    for winners; REJECTED results have no candidates, winners or test."""
    for name in CASES:
        res = json.loads((reference_dir / f"{name}.json").read_text(encoding="utf-8"))["result"]
        if res["run"]["status"] == "REJECTED":
            assert not {"candidates", "winners", "test"} & set(res), name
            assert res["run"]["reason"] == "ALL_CANDIDATES_INVALID"
            assert all(c["status"] == "INVALID_MODEL" and c["reasons"]
                       for c in res["run"]["invalid_candidates"])
            continue
        for c in res["candidates"]:
            assert (c["status"] == "VALID") == (c["fit"] is not None) == (c["cv"] is not None)
        assert set(res["test"]) == set(res["winners"]["test_keys"])
        for t in res["test"].values():
            cov = [lo <= a <= hi for a, lo, hi in zip(t["actual"], t["lower"], t["upper"])]
            assert cov == t["covered"]
            assert t["coverage"] == sum(cov) / t["n_test"]


def test_a1_reasons_name_the_rule_and_the_fold(reference_dir):
    def reasons(name):
        res = json.loads((reference_dir / f"{name}.json").read_text(encoding="utf-8"))["result"]
        return res["run"]["invalid_candidates"][0]["reasons"]
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


def test_startups50_all_in_is_valid_and_the_split_is_80_20(reference_dir):
    res = json.loads((reference_dir / "startups50.json").read_text(encoding="utf-8"))["result"]
    assert res["run"]["status"] == "COMPLETED"
    assert len(res["split"]["test"]) == 10 and len(res["split"]["train"]) == 40
    assert [c["status"] for c in res["columns"]] == ["KEPT", "KEPT", "KEPT", "KEPT", "TARGET"]
    allin = res["candidates"][0]
    assert allin["status"] == "VALID" and allin["k"] == 4
    assert allin["fit"]["levels"]["State"]["baseline"] == "New York"


def test_reference_reuses_the_formal_constants():
    from hw2 import models, ols
    assert R.CV_STD_DDOF == models.CV_STD_DDOF
    assert R.PI_LEVEL == ols.PI_LEVEL
