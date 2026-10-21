"""King County consistency of the generic Python reference (#75 V2-T2; Spec V2 主 seam
「King County 一致性」).

The generic reference :mod:`hw2.explore_reference` is fed the formal analysis's King County training
table as the formal analysis builds it — the training rows of the formal split, the 18 feature groups
encoded by :func:`hw2.preprocess.fit_preprocessor` on those rows (zipcode one-hot columns marked as
one-hot), and ln(price) as the target — and must reproduce:

- the four canonical paths (Forward SFS, Backward SFS, RFE, Lasso path, k = 1…18) recorded by the
  formal analysis in ``results/tables/cv_by_method_k.csv``;
- the All-in fit: the reference's OLS on the full table has the coefficients of the formal
  :func:`hw2.models.fit_model` on all 18 groups, and the R² / Adjusted R² recorded for ``allin``.

This shows that the two problems share one set of selection criteria; it does **not** replace the
independent Node-vs-Python checks of ``tests/test_node_explore.py``. Training rows only (DA TR-01):
no official test row is read. The formal path never imports the reference
(``tests/test_explore_static.py::test_the_reference_module_is_not_imported_by_any_formal_path``).
"""
import csv

import numpy as np
import pytest

from hw2 import explore_reference as R
from hw2 import models, preprocess
from hw2.paths import RESULTS_DIR

TABLE = RESULTS_DIR / "tables" / "cv_by_method_k.csv"


@pytest.fixture(scope="module")
def kc_table(prepared_real):
    training = prepared_real.training
    pre = preprocess.fit_preprocessor(training, preprocess.FEATURE_GROUPS)
    X = pre.transform(training).X
    y = np.log(training["price"].to_numpy(dtype=float))
    column_groups = [pre.group_of_column[c] for c in pre.columns]
    dummy = [c.startswith(preprocess.ZIPCODE_PREFIX) for c in pre.columns]
    return {"training": training, "pre": pre, "X": X, "y": y, "column_groups": column_groups,
            "dummy": dummy, "names": list(preprocess.FEATURE_GROUPS)}


@pytest.fixture(scope="module")
def recorded():
    with TABLE.open(encoding="utf-8", newline="") as fh:
        return {(row["method"], int(row["k"])): row for row in csv.DictReader(fh)}


def test_the_reference_reproduces_the_four_formal_canonical_paths(kc_table, recorded):
    t = kc_table
    paths = R.canonical_paths(t["X"], t["y"], t["column_groups"], t["dummy"], t["names"])
    for method in models.PATH_METHODS:
        got = paths[method]
        assert len(got) == 18
        for k in range(1, 19):
            assert got[k - 1] == recorded[(method, k)]["canonical_groups"].split(), (method, k)
    lasso = paths["_lasso"]
    assert lasso["degenerate"] is False and lasso["n_entered"] == 18 and lasso["cause"] is None
    alphas = [e["entry_alpha"] for e in lasso["entries"]]
    assert alphas == sorted(alphas, reverse=True)


def test_the_reference_reproduces_the_formal_all_in_fit(kc_table, recorded):
    t = kc_table
    res = R._fit(t["X"], t["y"], list(t["pre"].columns))
    assert res["ok"]
    fit = res["fit"]
    formal = models.fit_model(t["training"], preprocess.FEATURE_GROUPS).fit
    assert fit.rank == formal.rank and fit.df_resid == formal.df_resid
    np.testing.assert_allclose(fit.coef, formal.coef, rtol=1e-12, atol=0)
    np.testing.assert_allclose(fit.xtx_inv, formal.xtx_inv, rtol=1e-9, atol=0)
    row = recorded[("allin", 18)]
    assert row["canonical_groups"].split() == t["names"]
    assert fit.r2 == pytest.approx(float(row["r2_log_full_training_fit"]), rel=1e-12)
    assert fit.adj_r2 == pytest.approx(float(row["adj_r2_log_full_training_fit"]), rel=1e-12)
