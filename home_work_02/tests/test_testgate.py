"""The test-evaluation gate G-3 (DA TR-01, §11 G-3; Spec rev 5 次 seam「選模」: test 評估函式在同一執行內
第二次呼叫時報錯).

Official data: only the closed state is exercised; nothing here opens the official gate or loads an
official test row. Every opening and evaluation uses synthetic fixtures."""
import copy
import dataclasses

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


ALPHAS = {"ridge": 1.0, "lasso": 0.01}      # stand-in fixed alphas (Ridge/Lasso arrive in #63)


def stubs():
    return {name: StubMetricOnly(alpha) for name, alpha in ALPHAS.items()}


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


def test_the_official_gate_is_open_in_the_program_and_closed_in_every_test():
    """TR-01: #63 opened the official gate for the notebook (after the selection was fixed); every
    test runs with it closed (conftest), so no test can load an official test row."""
    import re
    from pathlib import Path
    source = Path(testgate.__file__).read_text(encoding="utf-8")
    assert re.search(r"^OFFICIAL_TEST_GATE_ENABLED = True$", source, re.M)
    assert testgate.OFFICIAL_TEST_GATE_ENABLED is False


@pytest.fixture(scope="module")
def official_gate_flag_in_a_module_fixture():
    return testgate.OFFICIAL_TEST_GATE_ENABLED


def test_the_official_gate_is_closed_for_session_and_module_fixtures_too(
        official_gate_flag_at_session_start, official_gate_flag_in_a_module_fixture):
    """#63 R1 F-2: fixtures of every scope run with the official gate closed."""
    assert official_gate_flag_at_session_start is False
    assert official_gate_flag_in_a_module_fixture is False


def test_official_test_rows_cannot_be_loaded_while_the_gate_is_closed(prepared_real, small_run):
    gate = testgate.TestGate(prepared_real)
    assert gate.official and gate.state == testgate.CLOSED
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()
    with pytest.raises(testgate.TestGateClosed, match="TR-01"):
        gate.open(small_run["winners"], ALPHAS)          # even with complete winners and alphas
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
        gate.open(partial, ALPHAS)
    with pytest.raises(testgate.TestGateError, match="alpha of ridge is not fixed"):
        gate.open(small_run["winners"], {"ridge": None, "lasso": 0.01})
    with pytest.raises(testgate.TestGateError, match="metric-only"):
        gate.open(small_run["winners"], {**ALPHAS, "elasticnet": 1.0})
    assert gate.state == testgate.CLOSED


def test_rows_load_only_inside_the_one_time_evaluation(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    with pytest.raises(testgate.TestGateClosed):
        gate.evaluate(small_run["ols"], stubs())         # not open yet
    gate.open(small_run["winners"], ALPHAS)
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()                            # open, but outside evaluate
    result = gate.evaluate(small_run["ols"], stubs())
    assert gate.state == testgate.EVALUATED
    assert sorted(result.test) == sorted(small_run["winners"]["authorized_test_models"]
                                         + ["lasso", "ridge"])
    assert result.test_inputs["n_rows"] == small_run["prepared"].n_test
    with pytest.raises(testgate.TestGateError, match="already ran"):
        gate.evaluate(small_run["ols"], stubs())         # second call in the same run
    with pytest.raises(testgate.TestGateClosed):
        gate.load_test_rows()
    with pytest.raises(testgate.TestGateError, match="opens once"):
        gate.open(small_run["winners"], ALPHAS)


def test_test_rows_are_the_split_test_rows_of_the_data_file(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], ALPHAS)
    result = gate.evaluate(small_run["ols"], stubs())
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
    gate.open(winners, ALPHAS)
    winners_after = copy.deepcopy(winners)
    winners["authorized_test_models"].append("forward_sfs_k01")   # mutate after freezing
    try:
        extra = dict(small_run["ols"])
        extra["forward_sfs_k01"] = extra["allin"]
        with pytest.raises(testgate.TestGateError, match="differ from the authorized set"):
            gate.evaluate(extra, stubs())
    finally:
        winners["authorized_test_models"] = winners_after["authorized_test_models"]
    assert gate.state == testgate.OPEN                  # a refused call did not consume the run


def test_missing_authorized_model_is_refused(small_run):
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], ALPHAS)
    fewer = dict(small_run["ols"])
    fewer.pop("allin")
    with pytest.raises(testgate.TestGateError, match="authorized set"):
        gate.evaluate(fewer, stubs())


def test_metric_only_models_go_through_the_same_gate_once(small_run):
    """CC-1 / G-3: Ridge and Lasso are scored once, behind the same gate, with frozen alphas."""
    gate = testgate.TestGate(small_run["prepared"])
    gate.open(small_run["winners"], {"ridge": 1.0, "lasso": 0.01})
    with pytest.raises(testgate.TestGateError, match="frozen alphas"):
        gate.evaluate(small_run["ols"], {"ridge": StubMetricOnly(1.0)})     # lasso missing
    with pytest.raises(testgate.TestGateError, match="frozen alphas"):
        gate.evaluate(small_run["ols"])                                    # both missing
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
        gate.open(small_run["winners"], ALPHAS)
        with pytest.raises(data.DataIntegrityError):
            gate.evaluate(small_run["ols"], stubs())
        assert gate.state == testgate.EVALUATED          # a failed evaluation still ends the run
    finally:
        path.write_bytes(original)


@pytest.mark.parametrize("alphas", [
    {},                                      # both omitted
    {"ridge": 1.0},                          # Lasso omitted
    {"lasso": 0.01},                         # Ridge omitted
    {"ridge": 1.0, "lasso": None},           # Lasso not fixed
    {"ridge": float("nan"), "lasso": 0.01},  # Ridge not fixed
    {"ridge": 0.0, "lasso": 0.01},           # not a valid alpha
], ids=["none", "ridge-only", "lasso-only", "lasso-none", "ridge-nan", "ridge-zero"])
def test_gate_refuses_to_open_unless_both_metric_only_alphas_are_fixed(small_run, alphas):
    """#61 R1 F-1 (CC-1, G-3): omitting Ridge or Lasso is refused, so no OLS test result can be
    seen before both alphas are fixed by training CV."""
    gate = testgate.TestGate(small_run["prepared"])
    with pytest.raises(testgate.TestGateError, match="is not fixed"):
        gate.open(small_run["winners"], alphas)
    assert gate.state == testgate.CLOSED
    with pytest.raises(testgate.TestGateClosed):
        gate.evaluate(small_run["ols"], stubs())        # nothing was scored
    gate.open(small_run["winners"], ALPHAS)             # the run is not consumed by the refusals
    assert gate.state == testgate.OPEN


def test_fixture_run_scores_ridge_and_lasso_once_with_their_training_cv_alphas(fixture_run):
    """CC-1 (1)(3): the metric-only models are scored once, with the alpha chosen by training CV."""
    test = fixture_run["evaluation"].test
    assert sorted(k for k, v in test.items() if v["kind"] == "metric_only") == ["lasso", "ridge"]
    for name in ("ridge", "lasso"):
        assert test[name]["alpha"] == fixture_run["selections"][name].alpha
        assert fixture_run["metric_only"][name].alpha == fixture_run["selections"][name].alpha
    manifest = fixture_run["evaluation"].manifest
    assert manifest["metric_only_alphas"] == {n: s.alpha for n, s in fixture_run["selections"].items()}
    assert manifest["evaluations_in_this_run"] == 1


class CountingModel:
    """Wraps a model and counts predict_usd calls (G-3: each model is scored once)."""

    def __init__(self, model):
        self.model = model
        self.alpha = getattr(model, "alpha", None)
        self.calls = 0

    def predict_usd(self, rows):
        self.calls += 1
        return self.model.predict_usd(rows)


def test_every_authorized_model_is_scored_exactly_once_after_the_selection_is_frozen(small_run):
    """G-3 (DA §11; D-1 D-4 (5)): opening freezes winners and alphas; the one evaluation scores each
    authorized OLS model and each metric-only model exactly once; the manifest records the frozen
    selection, and later changes to the caller's objects do not reach the gate."""
    gate = testgate.TestGate(small_run["prepared"])
    winners = copy.deepcopy(small_run["winners"])
    alphas = dict(ALPHAS)
    gate.open(winners, alphas)
    digest = testgate.selection_digest(small_run["winners"], ALPHAS)
    winners["authorized_test_models"].clear()           # after freezing: no effect
    alphas["ridge"] = 99.0
    ols = {k: CountingModel(m) for k, m in small_run["ols"].items()}
    metric = {n: CountingModel(m) for n, m in stubs().items()}
    result = gate.evaluate(ols, metric)
    assert all(m.calls == 1 for m in ols.values()) and all(m.calls == 1 for m in metric.values())
    manifest = result.manifest
    assert manifest["selection_digest"] == digest
    assert manifest["authorized_test_models"] == small_run["winners"]["authorized_test_models"]
    assert manifest["metric_only_alphas"] == ALPHAS
    assert manifest["opened_at"] <= manifest["evaluated_at"]
    assert manifest["n_test"] == small_run["prepared"].n_test
    assert manifest["official_data"] is False and len(manifest["run_id"]) == 32
    with pytest.raises(testgate.TestGateError, match="already ran"):
        gate.evaluate(ols, metric)
    assert all(m.calls == 1 for m in ols.values()) and all(m.calls == 1 for m in metric.values())


def test_selection_digest_changes_with_any_frozen_choice(small_run):
    w = small_run["winners"]
    base = testgate.selection_digest(w, ALPHAS)
    assert base == testgate.selection_digest(copy.deepcopy(w), dict(ALPHAS))
    assert base != testgate.selection_digest(w, {**ALPHAS, "lasso": 0.02})
    other = copy.deepcopy(w)
    other["overall"]["model_key"] = "x"
    assert base != testgate.selection_digest(other, ALPHAS)


# --- #61 R1 F-4: the official gate itself, on synthetic data identified as official ---------------

@pytest.fixture
def official_like(small_run, monkeypatch):
    """small_run's synthetic data treated as the official file (EXPECTED_SHA256 monkeypatched), with
    the per-process flag reset: nothing here touches the real CSV."""
    monkeypatch.setattr(data, "EXPECTED_SHA256", small_run["prepared"].sha256)
    monkeypatch.setattr(testgate, "_official_test_rows_loaded", False)
    return small_run


def test_official_data_cannot_be_opened_while_the_flag_is_off(official_like):
    gate = testgate.TestGate(official_like["prepared"])
    assert gate.official
    with pytest.raises(testgate.TestGateClosed, match="TR-01"):
        gate.open(official_like["winners"], ALPHAS)
    assert gate.state == testgate.CLOSED


def test_official_test_rows_load_at_most_once_per_process(official_like, monkeypatch):
    """With the flag on, the first gate evaluates; a second gate in the same process cannot load
    the official test rows again (it is refused and its run is consumed)."""
    monkeypatch.setattr(testgate, "OFFICIAL_TEST_GATE_ENABLED", True)
    first = testgate.TestGate(official_like["prepared"])
    first.open(official_like["winners"], ALPHAS)
    result = first.evaluate(official_like["ols"], stubs())
    assert result.manifest["official_data"] is True
    second = testgate.TestGate(official_like["prepared"])
    second.open(official_like["winners"], ALPHAS)
    with pytest.raises(testgate.TestGateError, match="already loaded"):
        second.evaluate(official_like["ols"], stubs())
    assert second.state == testgate.EVALUATED
    assert testgate._official_test_rows_loaded is True


def test_official_identity_does_not_rest_on_the_sha256_alone(tmp_path):
    """A modified copy of the official file stays official: by its path, or by its structure
    (21,613 rows, 21,436 unique ids). Synthetic data of another size is not."""
    frame = fixture.synthetic_sales(n_houses=data.EXPECTED_UNIQUE_IDS,
                                    n_repeats=data.EXPECTED_ROWS - data.EXPECTED_UNIQUE_IDS, seed=3)
    path = tmp_path / "copy.csv"
    frame.to_csv(path, index=False)
    prepared = data.load_and_split(path, expected_sha256=data.file_sha256(path),
                                   expected_rows=len(frame),
                                   expected_unique_ids=frame["id"].nunique())
    assert prepared.sha256 != data.EXPECTED_SHA256
    assert testgate.is_official(prepared)                            # by structure
    gate = testgate.TestGate(prepared)
    with pytest.raises(testgate.TestGateClosed):
        gate.open({"complete": True, "overall": {}}, ALPHAS)
    by_path = dataclasses.replace(prepared, facts={**prepared.facts, "n_rows": 1},
                                  source_path=data.DATA_CSV)
    assert testgate.is_official(by_path)                             # by path
    other = dataclasses.replace(prepared, facts={**prepared.facts, "n_rows": 1})
    assert not testgate.is_official(other)
