"""Packaging (#67): the checks of :mod:`hw2.package` and the ZIP round trip.

The real packaging (student id, report build, the ZIP in ``dist/``) runs on the author's machine
with ``python -m hw2.package``; these tests use synthetic notebooks and files in ``tmp_path`` and a
made-up id, never the real one."""
import json
import zipfile
from pathlib import Path

import nbformat
import pytest

from hw2 import package, report
from hw2.paths import MODEL_DATA_JSON

FAKE_ID = "Z98765432"


def _notebook(counts, run_id="r1", error_at=None):
    nb = nbformat.v4.new_notebook()
    for i, n in enumerate(counts):
        src = ("gate.open(winners, alphas)\nevaluation = gate.evaluate(models)" if i == 1
               else "gate.evaluate(models)  # second call, refused" if i == 2 else f"x = {i}")
        cell = nbformat.v4.new_code_cell(src, execution_count=n)
        if i == 1:
            cell.outputs = [nbformat.v4.new_output("stream", name="stdout",
                                                   text=f"manifest: {{'run_id': '{run_id}'}}\n")]
        if error_at == i:
            cell.outputs.append(nbformat.v4.new_output("error", ename="E", evalue="x", traceback=[]))
        nb.cells.append(cell)
    return nb


def _model_data(run_id="r1"):
    return {"meta": {"test_evaluation": {"manifest": {"run_id": run_id}}}}


@pytest.fixture
def no_formal_check(monkeypatch):
    monkeypatch.setattr(report, "check_formal_evaluation", lambda md: None)


def test_single_run_accepts_counts_one_to_n(no_formal_check):
    assert package.check_single_run(_notebook([1, 2, 3]), _model_data()) == {"code_cells": 3, "run_id": "r1"}


@pytest.mark.parametrize("counts", [[1, 2, 2], [1, 3, 2], [1, None, 3], [2, 3, 4], [1, 2, 3, 25]])
def test_single_run_refuses_a_mixed_or_partial_run(no_formal_check, counts):
    with pytest.raises(package.PackagingError, match="execution counts"):
        package.check_single_run(_notebook(counts), _model_data())


def test_single_run_refuses_an_error_output(no_formal_check):
    with pytest.raises(package.PackagingError, match="error output"):
        package.check_single_run(_notebook([1, 2, 3], error_at=2), _model_data())


def test_single_run_refuses_a_model_data_from_another_run(no_formal_check):
    with pytest.raises(package.PackagingError, match="not the run"):
        package.check_single_run(_notebook([1, 2, 3], run_id="r1"), _model_data("r2"))


def test_single_run_needs_exactly_one_gate_opening_cell(no_formal_check):
    nb = _notebook([1, 2, 3])
    nb.cells[0].source = "gate.open(winners, alphas)"
    with pytest.raises(package.PackagingError, match="one test-evaluation cell"):
        package.check_single_run(nb, _model_data())


def test_single_run_applies_the_formal_evaluation_check(monkeypatch):
    def refuse(md):
        raise report.ReportError("not the formal evaluation")
    monkeypatch.setattr(report, "check_formal_evaluation", refuse)
    with pytest.raises(report.ReportError):
        package.check_single_run(_notebook([1, 2, 3]), _model_data())


def test_the_tracked_model_data_passes_the_formal_evaluation_check():
    report.check_formal_evaluation(json.loads(MODEL_DATA_JSON.read_text(encoding="utf-8")))


def _files(tmp_path):
    a = tmp_path / "a.txt"
    a.write_bytes(b"alpha\n")
    b = tmp_path / "b.pdf"
    b.write_bytes(b"%PDF-1.7 beta")
    nb = tmp_path / "nb.ipynb"
    nb.write_bytes(b"{}")
    return [package.Entry(package.notebook_name(FAKE_ID), nb), package.Entry("report.pdf", b),
            package.Entry("dir/a.txt", a)]


def test_zip_round_trip_and_fixed_layout(tmp_path):
    items = _files(tmp_path)
    top = f"{FAKE_ID}_hw2"
    z1, z2 = tmp_path / "1.zip", tmp_path / "2.zip"
    package.write_zip(z1, top, items)
    package.write_zip(z2, top, items)
    assert package.sha256_file(z1) == package.sha256_file(z2)        # same inputs, same ZIP
    rows = package.verify_zip(z1, top, items)
    assert [r["path"] for r in rows] == [e.arcname for e in items]
    with zipfile.ZipFile(z1) as zf:
        assert zf.namelist()[0] == f"{top}/{FAKE_ID}_hw2.ipynb"
        assert all(n.startswith(top + "/") for n in zf.namelist())


def test_verify_zip_detects_a_changed_source(tmp_path):
    items = _files(tmp_path)
    z = tmp_path / "p.zip"
    package.write_zip(z, "t", items)
    items[2].source.write_bytes(b"changed\n")
    with pytest.raises(package.PackagingError, match="differs"):
        package.verify_zip(z, "t", items)


def test_verify_zip_detects_a_missing_entry(tmp_path):
    items = _files(tmp_path)
    z = tmp_path / "p.zip"
    package.write_zip(z, "t", items[:2])
    with pytest.raises(package.PackagingError, match="entries differ"):
        package.verify_zip(z, "t", items)


def test_names_and_masking():
    assert package.notebook_name(FAKE_ID) == f"{FAKE_ID}_hw2.ipynb"
    assert package.zip_name(FAKE_ID) == f"{FAKE_ID}_hw2.zip"
    assert package.mask(f"dist/{FAKE_ID}_hw2.zip", FAKE_ID) == "dist/<學號>_hw2.zip"


def test_duplicate_entry_names_are_refused(tmp_path):
    with pytest.raises(package.PackagingError, match="duplicate"):
        package.entries(FAKE_ID, tmp_path / "x.pdf", tmp_path / "hw2_report.pdf", [])


def test_the_packaged_tracked_files_cover_the_brief_contents():
    files = package.tracked_files()
    for required in ("README.md", "requirements.txt", "index.html", "data/kc_house_data.csv",
                     "hw2/package.py", "results/model_data.json", "assets/model_data.js",
                     "assets/vendor/chart.umd.js"):
        assert required in files
    assert not any("__pycache__" in f or f.startswith(("tests/", "doc/", "acceptor_materials/",
                                                         ".local/", "dist/")) for f in files)
    assert any(f.startswith("results/figures/") and f.endswith(".png") for f in files)
    assert any(f.startswith("results/tables/") and f.endswith(".csv") for f in files)
