"""Synthetic fixtures for the test-evaluation flow, the dashboard and the OV-6 measurement.

DA TR-01: until #63 the test flow, the gate and the dashboard's Test block are verified only with
synthetic data. Everything here is synthetic: a CSV with the 21 King County columns is generated
from a fixed seed (no value comes from the real file, least of all from its test rows), and it is
run through **the same code path as the official data** — :func:`hw2.data.load_and_split`,
:func:`hw2.models.fit_allin`, :func:`hw2.selection.run_path_methods` (which uses
:func:`hw2.models.evaluate_candidate`), :func:`hw2.models.determine_winners`,
:func:`hw2.comparison.run_metric_only` (Ridge and Lasso: training-CV alpha and refit),
:func:`hw2.comparison.evaluate_pvalue_backward`, :class:`hw2.testgate.TestGate` and
:func:`hw2.export.build_model_data` — with ``meta.fixture = true``.

Since #62 the four path methods run the real selection code (:func:`hw2.selection.run_path_methods`)
on the synthetic training rows; one candidate is artificially invalidated
(:func:`inject_invalid_candidate`) so that the invalid display and the winner rule are exercised.
:data:`FIXTURE_SUBSETS` (a few fixed subsets, not selections) remains only for small gate tests
that need complete winners quickly. Since #63 the metric-only models are the real Ridge and Lasso
(alpha by training CV on the synthetic training rows) and the p-value comparison runs too; the
gate opens only with both metric-only alphas fixed (CC-1, G-3).
Fixture ``model_data`` is never written inside the unit directory
(:func:`write_fixture`), so it cannot reach the tracked official paths or be used as a result.

``python -m hw2.fixture OUT_DIR [--houses N]`` writes a fixture copy of the dashboard to OUT_DIR
(outside the unit) for the OV-6 measurement.
"""
import argparse
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from . import comparison, data, export, models, selection, testgate
from .paths import ASSETS_DIR, DASHBOARD_HTML, MODEL_DATA_JS_GLOBAL, UNIT_DIR

FIXTURE_SEED = 20261018
FIXTURE_SUBSETS = {
    "forward_sfs": [("sqft_living",), ("sqft_living", "grade"),
                    ("sqft_living", "grade", "zipcode")],
    "backward_sfs": [("grade", "zipcode", "lat"), ("sqft_living", "grade", "zipcode", "lat")],
    "rfe": [("sqft_living", "zipcode"), ("sqft_living", "view", "zipcode")],
    "lasso_path": [("grade",), ("grade", "sqft_living15")],
}
_ZIPCODES = tuple(f"98{v:03d}" for v in range(1, 71))          # 70 synthetic labels


class FixtureError(RuntimeError):
    pass


def synthetic_sales(n_houses: int = 3000, n_repeats: int = 30, seed: int = FIXTURE_SEED,
                    n_zipcodes: int = 70) -> pd.DataFrame:
    """A frame with the 21 CSV columns; ln(price) depends on the features plus noise."""
    rng = np.random.default_rng(seed)
    ids = [f"{v:010d}" for v in rng.choice(9_000_000_000, size=n_houses, replace=False)
           + 1_000_000_000]
    repeat = list(rng.choice(ids, size=n_repeats, replace=False)) if n_repeats else []
    ids = ids + repeat
    n = len(ids)
    start = date(2014, 5, 2)
    dates = [(start + timedelta(days=int(d))).strftime("%Y%m%dT000000")
             for d in rng.integers(0, 391, size=n)]
    zips = np.array(_ZIPCODES[:n_zipcodes])
    zip_effect = dict(zip(zips, rng.normal(0.0, 0.25, size=zips.size)))
    zipcode = rng.choice(zips, size=n)
    grade = rng.integers(4, 13, size=n)
    above = np.round(np.exp(rng.normal(7.3, 0.35, size=n)) + 120 * (grade - 7)).clip(400, 9000)
    basement = np.where(rng.random(n) < 0.4, rng.integers(100, 1500, size=n), 0)
    living = above + basement
    built = rng.integers(1900, 2015, size=n)
    renovated = np.where(rng.random(n) < 0.05,
                         np.minimum(built + rng.integers(5, 60, size=n), 2015), 0)
    view = np.where(rng.random(n) < 0.1, rng.integers(1, 5, size=n), 0)
    waterfront = (rng.random(n) < 0.008).astype(int)
    condition = rng.integers(1, 6, size=n)
    lat = np.round(rng.uniform(47.16, 47.78, size=n), 4)
    log_price = (7.6 + 0.55 * np.log(living) + 0.12 * grade + 0.05 * view + 0.4 * waterfront
                 + 0.03 * condition + 0.6 * (lat - 47.5)
                 + np.array([zip_effect[z] for z in zipcode]) + rng.normal(0.0, 0.18, size=n))
    frame = pd.DataFrame({
        "id": ids,
        "date": dates,
        "price": np.round(np.exp(log_price), -2).clip(75_000, None),
        "bedrooms": rng.integers(1, 7, size=n),
        "bathrooms": rng.choice([1.0, 1.5, 1.75, 2.0, 2.25, 2.5, 3.0, 3.5], size=n),
        "sqft_living": living.astype(int),
        "sqft_lot": np.round(np.exp(rng.normal(8.9, 0.8, size=n))).astype(int),
        "floors": rng.choice([1.0, 1.5, 2.0, 2.5, 3.0], size=n),
        "waterfront": waterfront,
        "view": view,
        "condition": condition,
        "grade": grade,
        "sqft_above": above.astype(int),
        "sqft_basement": basement,
        "yr_built": built,
        "yr_renovated": renovated,
        "zipcode": zipcode,
        "lat": lat,
        "long": np.round(rng.uniform(-122.52, -121.31, size=n), 3),
        "sqft_living15": np.round(living * rng.uniform(0.7, 1.3, size=n)).astype(int),
        "sqft_lot15": np.round(np.exp(rng.normal(8.9, 0.7, size=n))).astype(int),
    })
    assert tuple(frame.columns) == data.EXPECTED_COLUMNS
    return frame


def _outside_unit(path: Path) -> Path:
    path = Path(path).resolve()
    unit = UNIT_DIR.resolve()
    if path == unit or unit in path.parents:
        raise FixtureError(f"fixture output must stay outside the unit directory ({unit}); "
                           f"got {path}")
    return path


def run_fixture(workdir: Path, n_houses: int = 3000, n_repeats: int = 30,
                seed: int = FIXTURE_SEED, n_folds: int = 5, inject_invalid: bool = True) -> dict:
    """Generate a synthetic CSV in `workdir` and run it through the official code path.

    Returns ``{"csv", "prepared", "allin", "candidates", "winners", "selections",
    "metric_only", "pvalue", "gate", "evaluation", "model_data", "injected_invalid"}``. The four
    path methods run the real selection code (:func:`hw2.selection.run_path_methods`); Ridge and
    Lasso choose their alpha by training CV (:func:`hw2.comparison.run_metric_only`). With
    `inject_invalid` one candidate is artificially invalidated (:func:`inject_invalid_candidate`).
    """
    workdir = _outside_unit(workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    frame = synthetic_sales(n_houses, n_repeats, seed)
    csv = workdir / "synthetic_sales.csv"
    frame.to_csv(csv, index=False, lineterminator="\n")
    sha = data.file_sha256(csv)
    prepared = data.load_and_split(csv, expected_sha256=sha, expected_rows=len(frame),
                                   expected_unique_ids=frame["id"].nunique(), n_folds=n_folds)
    allin = models.fit_allin(prepared.training)
    candidates, _, path_timing = selection.run_path_methods(prepared.training)
    injected = inject_invalid_candidate(prepared.training, candidates) if inject_invalid else None
    winners = models.determine_winners(allin, candidates)
    selections, metric_only, cmp_timing = comparison.run_metric_only(prepared.training)
    pvalue = comparison.evaluate_pvalue_backward(prepared.training)
    cmp_timing[comparison.PVALUE_KEY] = pvalue["timing_s"]
    gate = testgate.TestGate(prepared)
    gate.open(winners, {name: sel.alpha for name, sel in selections.items()})
    pool = [allin] + [c for cs in candidates.values() for c in cs]
    evaluation = gate.evaluate(testgate.ols_models_for(winners, pool), metric_only)
    timings = dict(prepared.timings_s)
    timings.update({f"path_{m}": t["total"] for m, t in path_timing.items()})
    timings.update({f"{m}_total": t["total"] for m, t in cmp_timing.items()})
    md = export.build_model_data(prepared, timings_s=timings, fixture=True, allin=allin,
                                 winners=winners, methods=candidates, evaluation=evaluation,
                                 path_timing=path_timing, metric_only=selections, pvalue=pvalue,
                                 comparison_timing=cmp_timing)
    subsets_note = "the path-method subsets come from the real selection code (hw2.selection)"
    injected_note = (f"; {injected} is artificially invalidated (a column made constant on fold "
                     "0's training rows) to exercise the invalid display" if injected else "")
    md["meta"]["fixture_note"] = ("SYNTHETIC FIXTURE: generated data, not the King County file; "
                                  f"{subsets_note}{injected_note}. Never a result.")
    return {"csv": csv, "prepared": prepared, "allin": allin, "candidates": candidates,
            "winners": winners, "selections": selections, "metric_only": metric_only,
            "pvalue": pvalue, "gate": gate, "evaluation": evaluation, "model_data": md,
            "injected_invalid": injected}


def inject_invalid_candidate(training: pd.DataFrame, candidates: dict,
                             method: str = "rfe") -> str | None:
    """Fixture only: replace the lowest-CV-RMSE candidate of `method` whose subset holds a
    pass-through numeric group by a re-evaluation on a copy of the rows where that group is
    constant outside fold 0. Fold 0's training rows then have a constant column, so that fold is
    rank deficient and the candidate is invalid (SR-04 class 2). In a real run this cannot happen
    while the All-in baseline is valid (a subset's columns are a subset of All-in's columns), so
    the fixture forces it to exercise the invalid display and the winner rule. Returns its key."""
    passthrough = [g for g in models.preprocess.FEATURE_GROUPS
                   if g not in ("date", "yr_renovated", "zipcode")]
    pool = [c for c in candidates[method] if c.valid
            and any(g in passthrough for g in c.canonical_groups)]
    if not pool:
        return None
    target = min(pool, key=lambda c: (c.cv_rmse, c.k))
    group = next(g for g in target.canonical_groups if g in passthrough)
    rows = training.copy()
    outside = rows["fold"] != 0
    rows.loc[outside, group] = rows.loc[outside, group].iloc[0]
    replaced = models.evaluate_candidate(rows, method, target.k, target.canonical_groups,
                                         target.fold_groups)
    if replaced.valid:
        return None
    candidates[method][candidates[method].index(target)] = replaced
    return replaced.key


def write_fixture(model_data: dict, out_dir: Path) -> tuple[Path, Path]:
    """Write fixture model_data (``model_data.json`` and ``assets/model_data.js``) to `out_dir`."""
    if not model_data["meta"].get("fixture"):
        raise FixtureError("only fixture model_data is written by hw2.fixture")
    out_dir = _outside_unit(out_dir)
    return export.write_model_data(model_data, out_dir / "model_data.json",
                                   out_dir / "assets" / "model_data.js")


def write_fixture_dashboard(model_data: dict, out_dir: Path) -> Path:
    """A copy of the dashboard in `out_dir` (outside the unit) that loads fixture model_data."""
    out_dir = _outside_unit(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "assets").mkdir(parents=True)
    shutil.copy2(DASHBOARD_HTML, out_dir / "index.html")
    for path in ASSETS_DIR.rglob("*"):
        rel = path.relative_to(ASSETS_DIR)
        if path.is_file() and rel.as_posix() != "model_data.js":
            target = out_dir / "assets" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    write_fixture(model_data, out_dir)
    return out_dir / "index.html"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--houses", type=int, default=21_250)
    parser.add_argument("--repeats", type=int, default=180)
    args = parser.parse_args(argv)
    out = _outside_unit(args.out_dir)
    run = run_fixture(out.parent / (out.name + "_work"), args.houses, args.repeats)
    html = write_fixture_dashboard(run["model_data"], out)
    md = run["model_data"]
    print(f"fixture dashboard: {html}")
    print(f"window.{MODEL_DATA_JS_GLOBAL}: n_train {md['meta']['split']['n_train']}, "
          f"n_test {md['meta']['split']['n_test']}, test models {sorted(md['test'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
