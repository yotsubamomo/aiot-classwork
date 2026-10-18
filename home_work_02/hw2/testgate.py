"""The test-evaluation gate (G-3; DA TR-01; Spec rev 5 「特徵選擇與模型」、CC-1).

The features and ``price`` of the test rows can be loaded **only** through this gate, and the test
evaluation can run **only** through it:

1. A gate belongs to one run (one :class:`~hw2.data.PreparedData`). It starts ``closed``.
2. :meth:`TestGate.open` freezes the selection: the complete ``winners`` (every path method's CV
   winner, the All-in baseline and the overall CV winner fixed) and the training-CV alpha of
   **both** metric-only models (Ridge and Lasso; CC-1). An incomplete selection — including a
   missing Ridge or Lasso alpha — is refused.
3. :meth:`TestGate.evaluate` loads the test rows once, scores exactly the authorized OLS subset
   models (``kind = "ols_subset"``) and both frozen metric-only models (``kind = "metric_only"``),
   each once, and returns ``test_inputs`` and ``test`` together. A second call raises, so does a
   call for a model outside the frozen selection.
4. For the official data file (identified by its sha256), the gate cannot be opened while
   :data:`OFFICIAL_TEST_GATE_ENABLED` is false. It stays false until #63 (TR-01: the gate opens
   only there, after every training-CV selection and alpha is fixed). Independently of that flag,
   the official test rows can be loaded at most once per Python process.

Synthetic fixtures go through the same gate and the same code path; only their data file differs.
"""
import time
from dataclasses import dataclass
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import contract, data, metrics, ols

# DA TR-01: opened only in #63, after every training-CV selection and alpha is fixed.
OFFICIAL_TEST_GATE_ENABLED = False
METRIC_ONLY_MODELS = ("ridge", "lasso")
CLOSED, OPEN, EVALUATED = "closed", "open", "evaluated"

_official_test_rows_loaded = False          # once per process for the official data file


class TestGateError(RuntimeError):
    """The test gate refuses the request."""


class TestGateClosed(TestGateError):
    """The gate is closed: the test rows cannot be loaded."""


def is_official(prepared: data.PreparedData) -> bool:
    return prepared.sha256 == data.EXPECTED_SHA256


@dataclass(frozen=True)
class TestEvaluation:
    test_inputs: dict
    test: dict
    opened_at: str
    evaluated_at: str
    timing_s: dict


class TestGate:
    def __init__(self, prepared: data.PreparedData):
        self._prepared = prepared
        self._state = CLOSED
        self._winners = None
        self._alphas = None
        self._opened_at = None
        self._evaluating = False

    @property
    def state(self) -> str:
        return self._state

    @property
    def official(self) -> bool:
        return is_official(self._prepared)

    def status(self) -> dict:
        return {"state": self._state, "official_data": self.official,
                "official_gate_enabled": OFFICIAL_TEST_GATE_ENABLED}

    # -- opening -----------------------------------------------------------------------------
    def open(self, winners: dict, alphas: dict) -> None:
        """Freeze the selection and open the gate (once)."""
        if self._state != CLOSED:
            raise TestGateError(f"the test gate is already {self._state}; it opens once per run")
        if self.official and not OFFICIAL_TEST_GATE_ENABLED:
            raise TestGateClosed("the official test gate stays closed until every training-CV "
                                 "selection and alpha is fixed (DA TR-01; opened in #63)")
        if not winners or not winners.get("complete") or winners.get("overall") is None:
            raise TestGateError("winners are not fixed: every path method's CV winner and the "
                                "overall CV winner must be determined before the test gate opens")
        if winners.get("pending_methods"):
            raise TestGateError(f"winners pending for {winners['pending_methods']}")
        alphas = dict(alphas or {})
        unknown = set(alphas) - set(METRIC_ONLY_MODELS)
        if unknown:
            raise TestGateError(f"only {METRIC_ONLY_MODELS} are metric-only models, not "
                                f"{sorted(unknown)}")
        # CC-1 / G-3 (#61 R1 F-1): every metric-only alpha must be fixed by training CV before
        # the gate opens; omitting Ridge or Lasso (or both) is refused, not treated as "none".
        for name in METRIC_ONLY_MODELS:
            alpha = alphas.get(name)
            if alpha is None or not np.isfinite(float(alpha)) or float(alpha) <= 0:
                raise TestGateError(f"alpha of {name} is not fixed: the alphas of all metric-only "
                                    f"models {METRIC_ONLY_MODELS} must be fixed before the test "
                                    "gate opens")
        self._winners = _freeze(winners)
        self._alphas = {k: float(v) for k, v in alphas.items()}
        self._opened_at = _now()
        self._state = OPEN

    # -- loading -----------------------------------------------------------------------------
    def load_test_rows(self) -> pd.DataFrame:
        """The test rows (``row``, raw CSV columns, ``price``), sorted by CSV row position.

        Only inside :meth:`evaluate` of an open gate; any other call raises :class:`TestGateClosed`.
        """
        global _official_test_rows_loaded
        if self._state != OPEN or not self._evaluating:
            raise TestGateClosed(f"the test gate is {self._state}: test rows can be loaded only "
                                 "by the one-time test evaluation")
        if self.official:
            if not OFFICIAL_TEST_GATE_ENABLED:
                raise TestGateClosed("the official test gate is closed (DA TR-01)")
            if _official_test_rows_loaded:
                raise TestGateError("the official test rows were already loaded in this run")
            _official_test_rows_loaded = True
        prepared = self._prepared
        if prepared.source_path is None:
            raise TestGateError("the run does not record its data file")
        data.verify_sha256(prepared.source_path, prepared.sha256)
        full = data._read_csv(prepared.source_path)
        rows = full.iloc[prepared.test_rows].copy()
        del full
        rows.insert(0, "row", prepared.test_rows)
        if not np.array_equal(rows["id"].to_numpy(), prepared.test_ids):
            raise TestGateError("test rows do not match the split's test identifiers")
        return rows.sort_values("row", kind="stable").reset_index(drop=True)

    # -- evaluation --------------------------------------------------------------------------
    def evaluate(self, ols_models: dict, metric_only: dict | None = None) -> TestEvaluation:
        """Score the frozen selection once.

        `ols_models` maps each authorized model key to its :class:`~hw2.models.OLSModel`
        (canonical fit on the whole training set); `metric_only` maps ``ridge``/``lasso`` to an
        object with ``alpha`` and ``predict_usd(rows) -> ndarray``.
        """
        if self._state == EVALUATED:
            raise TestGateError("the test evaluation already ran in this run; it runs once")
        if self._state != OPEN:
            raise TestGateClosed("the test gate is closed: open it with the fixed winners and "
                                 "alphas first")
        metric_only = dict(metric_only or {})
        authorized = list(self._winners["authorized_test_models"])
        if sorted(ols_models) != sorted(authorized):
            raise TestGateError(f"OLS models {sorted(ols_models)} differ from the authorized set "
                                f"{sorted(authorized)}")
        if sorted(metric_only) != sorted(self._alphas):
            raise TestGateError(f"metric-only models {sorted(metric_only)} differ from the frozen "
                                f"alphas {sorted(self._alphas)}")
        for name, model in metric_only.items():
            if float(getattr(model, "alpha", np.nan)) != self._alphas[name]:
                raise TestGateError(f"alpha of {name} differs from the frozen alpha")
        t0 = time.perf_counter()
        self._evaluating = True
        try:
            rows = self.load_test_rows()
        finally:
            self._evaluating = False
            self._state = EVALUATED                 # no second evaluation, even on error
        t1 = time.perf_counter()
        actual = rows["price"].to_numpy(dtype=float)
        test_inputs = contract.build_test_inputs(rows)
        test = {}
        for key in authorized:
            model = ols_models[key]
            point, lower, upper, n_unseen = model.predict_usd(rows)
            cov = metrics.coverage_stats(actual, lower, upper)
            entry = {"kind": "ols_subset", "model_key": key, "scale": "USD",
                     "n_test": int(actual.size), **metrics.usd_metrics(actual, point),
                     "coverage": cov["coverage"], "n_covered": cov["n_covered"],
                     "mean_width": cov["mean_width"],
                     "coverage_uncertainty": cov["coverage_uncertainty"],
                     "pi_level": ols.PI_LEVEL,
                     "n_unseen_zipcode": int(n_unseen),
                     "predicted": [float(v) for v in point],
                     "lower": [float(v) for v in lower],
                     "upper": [float(v) for v in upper],
                     "covered": [bool(v) for v in cov["covered"]]}
            test[key] = entry
        for name in sorted(metric_only):
            model = metric_only[name]
            point = np.asarray(model.predict_usd(rows), dtype=float)
            test[name] = {"kind": "metric_only", "model_key": name, "scale": "USD",
                          "alpha": self._alphas[name], "n_test": int(actual.size),
                          **metrics.usd_metrics(actual, point)}
        t2 = time.perf_counter()
        return TestEvaluation(test_inputs=test_inputs, test=test, opened_at=self._opened_at,
                              evaluated_at=_now(),
                              timing_s={"load_test_rows": round(t1 - t0, 4),
                                        "score": round(t2 - t1, 4)})


def _freeze(winners: dict) -> dict:
    import copy
    return copy.deepcopy(winners)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def ols_models_for(winners: dict, candidates) -> dict:
    """Map each authorized key to the canonical OLS model of its candidate."""
    by_key = {c.key: c for c in candidates}
    out = {}
    for key in winners["authorized_test_models"]:
        c = by_key.get(key)
        if c is None or c.model is None or not c.valid:
            raise TestGateError(f"authorized model {key} has no valid canonical fit")
        out[key] = c.model
    return out
