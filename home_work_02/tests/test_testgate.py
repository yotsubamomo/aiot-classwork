"""The test-evaluation gate G-3 (DA TR-01, §11 G-3; Spec rev 5 次 seam「選模」: test 評估函式在同一執行內
第二次呼叫時報錯).

Official data: only the closed state is exercised; nothing here opens the official gate or loads an
official test row. Every opening and evaluation uses synthetic fixtures."""
import copy

import numpy as np
import pytest

from hw2 import data, fixture, models, testgate


class StubMetricOnly:
    """Stands in for a metric-only model (Ridge/Lasso arrive in #63): a constant prediction."""

    def __init__(self, alpha, value=500_000.0):
        self.alpha = alpha
        self.value = value
        self.calls = 0

    def predict_usd(self, rows):
        self.calls += 1
        return np.full(len(rows), self.value)


@pytest.fixture
def small_run(tmp_path):
    """A fixture data set, its All-in and stand-in candidates, complete winners; gate not open."""
    frame = fixture.synthetic_sales(n_houses=700, n_repeats=15, seed=5)
    path = tmp_path / "s.csv"
    frame.to_csv(path, index=False)
    prepared = data.load_and_split(path, expected_sha256=data.file_sha256(path),
                                   expected_rows=len(frame),
                                   expected_unique_ids=frame["id"].nunique())
    allin = models.fit_allin(prepared.training)
    cands = {m: [models.evaluate_candidate(prepared.training, m, len(s), s) for s in subsets]
             for m, subsets in fixture.FIXTURE_SUBSETS.items()}
    winners = models.determine_winners(allin, cands)
    pool = [allin] + [c for cs in cands.values() for c in cs]
    return {"prepared": prepared, "frame": frame, "winners": winners,
            "ols": testgate.ols_models_for(winners, pool)}


def test_the_official_gate_is_closed_in_this_ticket():
    assert testgate.OFFICIAL_TEST_GATE_ENABLED is False


def test_official_test_rows_cannot_be_loaded_while_the_gate_is_closed(prepared_real, small_run):
    gate = testgate.TestGate(prepared_real)
    assert gate.official and gate.state == testgate.CLOSED
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()
    with pytest.raises(testgate.TestGateClosed, match="TR-01"):
        gate.open(small_run["winners"], {})              # even with complete winners
    with pytest.raises(testgate.TestGateClosed):
        gate.evaluate({})
    assert gate.state == testgate.CLOSED


def test_official_winners_are_not_complete_so_the_gate_could_not_open_anyway(prepared_real):
    allin = models.fit_allin(prepared_real.training)
    winners = models.determine_winners(allin, {})
    assert not winners["complete"] and winners["overall"] is None


def test_gate_refuses_incomplete_winners_and_unfixed_alphas(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    assert not gate.official
    partial = copy.deepcopy(small_run["winners"])
    partial.update(complete=False, overall=None, pending_methods=["rfe"])
    with pytest.raises(testgate.TestGateError, match="not fixed"):
        gate.open(partial, {})
    with pytest.raises(testgate.TestGateError, match="alpha of ridge is not fixed"):
        gate.open(small_run["winners"], {"ridge": None})
    with pytest.raises(testgate.TestGateError, match="metric-only"):
        gate.open(small_run["winners"], {"elasticnet": 1.0})
    assert gate.state == testgate.CLOSED


def test_rows_load_only_inside_the_one_time_evaluation(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    with pytest.raises(testgate.TestGateClosed):
        gate.evaluate(small_run["ols"])                  # not open yet
    gate.open(small_run["winners"], {})
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()                            # open, but outside evaluate
    result = gate.evaluate(small_run["ols"])
    assert gate.state == testgate.EVALUATED
    assert sorted(result.test) == sorted(small_run["winners"]["authorized_test_models"])
    assert result.test_inputs["n_rows"] == small_run["prepared"].n_test
    with pytest.raises(testgate.TestGateError, match="already ran"):
        gate.evaluate(small_run["ols"])                  # second call in the same run
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()
    with pytest.raises(testgate.TestGateError, match="opens once"):
        gate.open(small_run["winners"], {})


def test_test_rows_are_the_split_test_rows_of_the_data_file(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], {})
    result = gate.evaluate(small_run["ols"])
    rows = result.test_inputs["rows"]
    prepared = small_run["prepared"]
    assert [r[0] for r in rows] == sorted(prepared.test_rows.tolist())
    frame = small_run["frame"]
    by_row = {r[0]: r for r in rows}
    for pos in prepared.test_rows[:20]:
        assert by_row[int(pos)][-1] == frame["price"].iloc[pos]
        assert by_row[int(pos)][1] == frame["id"].iloc[pos]


def test_only_the_frozen_authorized_set_is_scored(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    winners = small_run["winners"]
    gate.open(winners, {})
    winners_after = copy.deepcopy(winners)
    winners["authorized_test_models"].append("forward_sfs_k01")   # mutate after freezing
    try:
        extra = dict(small_run["ols"])
        extra["forward_sfs_k01"] = extra["allin"]
        with pytest.raises(testgate.TestGateError, match="differ from the authorized set"):
            gate.evaluate(extra)
    finally:
        winners["authorized_test_models"] = winners_after["authorized_test_models"]
    assert gate.state == testgate.OPEN                  # a refused call did not consume the run


def test_missing_authorized_model_is_refused(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], {})
    fewer = dict(small_run["ols"])
    fewer.pop("allin")
    with pytest.raises(testgate.TestGateError, match="authorized set"):
        gate.evaluate(fewer)


def test_metric_only_models_go_through_the_same_gate_once(small_run):
    """CC-1 / G-3: Ridge and Lasso are scored once, behind the same gate, with frozen alphas."""
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], {"ridge": 1.0, "lasso": 0.01})
    with pytest.raises(testgate.TestGateError, match="frozen alphas"):
        gate.evaluate(small_run["ols"], {"ridge": StubMetricOnly(1.0)})
    with pytest.raises(testgate.TestGateError, match="differs from the frozen alpha"):
        gate.evaluate(small_run["ols"], {"ridge": StubMetricOnly(2.0),
                                         "lasso": StubMetricOnly(0.01)})
    ridge, lasso = StubMetricOnly(1.0), StubMetricOnly(0.01)
    result = gate.evaluate(small_run["ols"], {"ridge": ridge, "lasso": lasso})
    assert ridge.calls == 1 and lasso.calls == 1
    for name in ("ridge", "lasso"):
        entry = result.test[name]
        assert entry["kind"] == "metric_only"
        assert set(entry) == {"kind", "model_key", "scale", "alpha", "n_test", "mae", "mse", "rmse",
                              "r2"}
    with pytest.raises(testgate.TestGateError, match="already ran"):
        gate.evaluate(small_run["ols"], {"ridge": ridge, "lasso": lasso})
    assert ridge.calls == 1


def test_the_gate_reads_the_file_it_split(small_run, tmp_path):
    """A data file changed after the split is refused (sha256 of the run)."""
    prepared = small_run["prepared"]
    path = prepared.source_path
    original = path.read_bytes()
    try:
        path.write_bytes(original.replace(b"\n", b"\r\n", 1))
        gate = testgate.TestGate(prepared)
        gate.open(small_run["winners"], {})
        with pytest.raises(data.DataIntegrityError):
            gate.evaluate(small_run["ols"])
        assert gate.state == testgate.EVALUATED          # a failed evaluation still ends the run
    finally:
        path.write_bytes(original)
