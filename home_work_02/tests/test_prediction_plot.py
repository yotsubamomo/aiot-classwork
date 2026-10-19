"""The actual vs predicted figure with every test row's 95% PI (#65; DA
``decision-20261019-issue65-labels-figures.md`` F-4 point 6): it only draws the exported results.

(i) fixture or unofficial model_data is never written inside the unit; (ii) every test row has one
PI segment and one point, coloured by its exported ``covered``; (iii) drawing calls neither the test
gate nor the data loader, fits nothing and scores nothing. The tracked PNG is regenerated
byte-identically from the tracked model_data (N-3 precondition)."""
import ast
import inspect
import json

import numpy as np
import pytest

from hw2 import data, prediction_plot, testgate
from hw2.paths import FIGURES_DIR, MODEL_DATA_JSON, UNIT_DIR

OFFICIAL = json.loads(MODEL_DATA_JSON.read_text(encoding="utf-8"))


def _check_panels(md, info):
    keys = md["winners"]["authorized_test_models"]
    assert [i["key"] for i in info] == keys
    for item in info:
        entry = md["test"][item["key"]]
        assert item["n_segments"] == item["n_points"] == entry["n_test"] == len(entry["covered"])
        expected = [prediction_plot.COVERED_COLOR if c else prediction_plot.MISSED_COLOR for c in entry["covered"]]
        assert item["segment_colors"] == expected
        assert sum(item["covered"]) == entry["n_covered"]


def test_every_official_test_row_is_drawn_and_coloured_by_covered():
    fig, info = prediction_plot.prediction_figure(OFFICIAL)
    _check_panels(OFFICIAL, info)
    for ax in fig.axes[:len(info)]:
        assert ax.get_xscale() == "log" and ax.get_yscale() == "log"
        assert ax.get_xlabel().startswith("Predicted") and ax.get_ylabel().startswith("Actual")


def test_segments_are_the_exported_bounds_at_the_exported_prediction():
    fig, info = prediction_plot.prediction_figure(OFFICIAL)
    from matplotlib.collections import LineCollection
    for ax, item in zip(fig.axes, info):
        entry = OFFICIAL["test"][item["key"]]
        segs = next(c for c in ax.collections if isinstance(c, LineCollection)).get_segments()
        segs = np.array(segs)
        assert np.array_equal(segs[:, 0, 0], np.array(entry["predicted"]))
        assert np.array_equal(segs[:, 0, 1], np.array(entry["lower"]))
        assert np.array_equal(segs[:, 1, 1], np.array(entry["upper"]))


def test_titles_name_the_shared_winners_and_the_overall_winner():
    fig, info = prediction_plot.prediction_figure(OFFICIAL)
    titles = [ax.get_title() for ax in fig.axes[:len(info)]]
    shared = prediction_plot.winners_by_test_key(OFFICIAL)
    for title, item in zip(titles, info):
        for label in shared[item["key"]]:
            assert label in title
    overall_key = OFFICIAL["winners"]["overall"]["test_model_key"]
    overall_title = titles[[i["key"] for i in info].index(overall_key)]
    assert "overall CV winner: Lasso path ranking k=17" in overall_title


def test_fixture_results_are_drawn_but_never_written_inside_the_unit(fixture_model_data, tmp_path):
    md, _ = fixture_model_data
    _, info = prediction_plot.prediction_figure(md)
    _check_panels(md, info)
    assert not prediction_plot.is_formal(md)
    with pytest.raises(prediction_plot.PredictionPlotError):
        prediction_plot.save_prediction_figure(md, FIGURES_DIR)
    with pytest.raises(prediction_plot.PredictionPlotError):
        prediction_plot.save_prediction_figure(md, UNIT_DIR / "results" / "scratch")
    assert prediction_plot.save_prediction_figure(md, tmp_path).is_file()


def test_tampered_official_results_are_not_written_inside_the_unit():
    md = json.loads(json.dumps(OFFICIAL))
    key = md["winners"]["authorized_test_models"][0]
    md["test"][key]["covered"][0] = not md["test"][key]["covered"][0]
    assert not prediction_plot.is_formal(md)
    with pytest.raises(prediction_plot.PredictionPlotError):
        prediction_plot.save_prediction_figure(md, FIGURES_DIR)


def test_drawing_never_calls_the_gate_or_the_data_loader_and_fits_nothing(monkeypatch):
    def refuse(*args, **kwargs):
        raise AssertionError("the figure must only read the exported results")
    for module in (data, testgate):
        for name, obj in vars(module).items():
            if inspect.isfunction(obj) and obj.__module__ == module.__name__:
                monkeypatch.setattr(module, name, refuse)
    monkeypatch.setattr(testgate, "TestGate", refuse, raising=False)
    prediction_plot.prediction_figure(OFFICIAL)
    assert testgate._official_test_rows_loaded is False
    tree = ast.parse(inspect.getsource(prediction_plot))
    imported = {(n.module or "") for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
    imported |= {a.name for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) for a in n.names}
    imported |= {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
    forbidden = {"testgate", "data", "models", "ols", "selection", "comparison", "metrics", "preprocess",
                 "deployment", "sklearn", "pandas"}
    assert not {m.rsplit(".", 1)[-1] for m in imported} & forbidden, imported
    calls = {n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", "")
             for n in ast.walk(tree) if isinstance(n, ast.Call)}
    assert not calls & {"fit", "evaluate", "open", "read_csv", "predict", "load_and_split", "score"}, calls


def test_the_tracked_png_is_regenerated_byte_identically(tmp_path):
    tracked = FIGURES_DIR / prediction_plot.FIGURE_FILE
    assert tracked.is_file()
    assert prediction_plot.is_formal(OFFICIAL)
    regenerated = prediction_plot.save_prediction_figure(OFFICIAL, tmp_path)
    assert regenerated.read_bytes() == tracked.read_bytes()


def test_the_notebook_draws_the_figure_after_5_5_without_touching_the_evaluation():
    cells = json.loads((UNIT_DIR / "hw2.ipynb").read_text(encoding="utf-8"))["cells"]
    sources = ["".join(c["source"]) for c in cells]
    i = next(n for n, s in enumerate(sources) if "prediction_plot.prediction_figure(model_data)" in s)
    h55 = next(n for n, s in enumerate(sources) if s.startswith("### 5.5 "))
    h56 = next(n for n, s in enumerate(sources) if s.startswith("### 5.6 "))
    assert h55 < i < h56 and sources[i - 1].startswith("#### 5.5.1 ")
    assert "gate." not in sources[i] and "evaluate" not in sources[i]
    outputs = cells[i]["outputs"]
    assert not any(o["output_type"] == "error" for o in outputs)
    assert any("image/png" in o.get("data", {}) for o in outputs)
    text = "".join("".join(o.get("text", "")) for o in outputs)
    n = OFFICIAL["test"][OFFICIAL["winners"]["authorized_test_models"][0]]["n_test"]
    assert f"{n} PI segments and {n} points drawn" in text
    assert "written: results/figures/" + prediction_plot.FIGURE_FILE in text
