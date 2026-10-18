"""Synthetic fixtures for the test-evaluation flow, the dashboard and the OV-6 measurement.

DA TR-01: until #63 the test flow, the gate and the dashboard's Test block are verified only with
synthetic data. Everything here is synthetic: a CSV with the 21 King County columns is generated
from a fixed seed (no value comes from the real file, least of all from its test rows), and it is
run through **the same code path as the official data** — :func:`hw2.data.load_and_split`,
:func:`hw2.models.fit_allin`, :func:`hw2.models.evaluate_candidate`,
:func:`hw2.models.determine_winners`, :class:`hw2.testgate.TestGate` and
:func:`hw2.export.build_model_data` — with ``meta.fixture = true``.

The four path methods do not exist before #62, so the fixture stands in a few fixed subsets per
path method (:data:`FIXTURE_SUBSETS`; not selected by any method) so that the winners are complete
and the gate can open. Fixture ``model_data`` is never written inside the unit directory
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

from . import data, export, models, testgate
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
                seed: int = FIXTURE_SEED, n_folds: int = 5, metric_only: dict | None = None,
                alphas: dict | None = None) -> dict:
    """Generate a synthetic CSV in `workdir` and run it through the official code path.

    Returns ``{"csv", "prepared", "allin", "candidates", "winners", "gate", "evaluation",
    "model_data"}``. `metric_only`/`alphas` may stand in metric-only models for gate tests.
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
    candidates = {m: [models.evaluate_candidate(prepared.training, m, len(s), s)
                      for s in subsets] for m, subsets in FIXTURE_SUBSETS.items()}
    winners = models.determine_winners(allin, candidates)
    gate = testgate.TestGate(prepared)
    gate.open(winners, alphas or {})
    pool = [allin] + [c for cs in candidates.values() for c in cs]
    evaluation = gate.evaluate(testgate.ols_models_for(winners, pool), metric_only or {})
    md = export.build_model_data(prepared, fixture=True, allin=allin, winners=winners,
                                 methods=candidates, evaluation=evaluation)
    md["meta"]["fixture_note"] = ("SYNTHETIC FIXTURE: generated data, not the King County file; "
                                  "the path-method subsets are fixed stand-ins, not selections. "
                                  "Never a result.")
    return {"csv": csv, "prepared": prepared, "allin": allin, "candidates": candidates,
            "winners": winners, "gate": gate, "evaluation": evaluation, "model_data": md}


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
