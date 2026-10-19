"""Packaging the submission (Brief §8; Spec rev 5 「報告與打包」): ``<學號>_hw2.ipynb`` and ``<學號>_hw2.zip``.

Usage (from ``home_work_02/``, after the full notebook run and the tests)::

    python -m hw2.package

Every check runs before anything is written to ``dist/``; the first failing check stops the
packaging (nothing is packaged from a state that was not checked):

1. the student id is read from the untracked ``.local/packaging.json`` (placeholder refused). It only
   appears in the names of the two submitted files (and the ZIP's top folder); it is never printed,
   logged or written to a tracked file: every name this module prints or records uses ``<學號>``;
2. the packaged tracked files are exactly the committed ones (``git status`` clean for them), so the
   ZIP can be traced to one commit;
3. the notebook is one complete run (DA ``decision-20261018-issue64-notebook-rerun.md`` N-3): every
   code cell executed, execution counts 1…N in order, no error output, and the run id printed by the
   test-evaluation cell equals the manifest of the exported ``model_data``; the exported test results
   are the one formal evaluation (:func:`hw2.report.check_formal_evaluation`);
4. the final report is built from the exported results (:func:`hw2.report.build` with
   ``final=True``; it refuses pending AI-evidence sections and unreviewed derived text);
5. ``hw2.ipynb`` is copied byte for byte to ``dist/<學號>_hw2.ipynb`` (one source, Brief §8);
6. ``dist/<學號>_hw2.zip`` is written (one top folder ``<學號>_hw2/``; fixed entry order and time
   stamps) and read back: every entry's sha256 must equal its source.

The ZIP holds (Brief §8 Q28): the main program ``<學號>_hw2.ipynb``, the report PDF, the author's
ChatGPT PDF, the analysis package ``hw2/``, ``requirements.txt``, the data CSV, ``README.md``, the
result files ``results/`` and the dashboard (``index.html``, ``assets/``). A manifest (names with the
placeholder, sizes, sha256) is written to ``dist/hw2_package_manifest.json``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

import nbformat

from . import local_config, report
from .paths import ACCEPTOR_MATERIALS_DIR, DIST_DIR, MODEL_DATA_JSON, UNIT_DIR

PLACEHOLDER = local_config.PLACEHOLDER
NOTEBOOK = UNIT_DIR / "hw2.ipynb"
MANIFEST_NAME = "hw2_package_manifest.json"
REPORT_PDF_NAME = "hw2_report.pdf"
# Tracked paths packaged as they are committed (directories expand to their tracked files).
TRACKED_ITEMS = ("README.md", "requirements.txt", "index.html", "data/kc_house_data.csv",
                 "hw2", "results", "assets")
ZIP_TIME = (2026, 1, 1, 0, 0, 0)          # fixed entry time stamps: the same inputs give the same ZIP
EVALUATION_CELL_MARK = "gate.open("     # the 5.4 cell that opens the gate and evaluates once


class PackagingError(RuntimeError):
    """A packaging check failed (the message never contains the student id)."""


@dataclass(frozen=True)
class Entry:
    arcname: str          # path inside the ZIP, below the top folder (no student id except the notebook)
    source: Path


def notebook_name(student_id: str) -> str:
    return f"{student_id}_hw2.ipynb"


def zip_name(student_id: str) -> str:
    return f"{student_id}_hw2.zip"


def mask(text: str, student_id: str) -> str:
    """The text with the student id replaced by the placeholder."""
    return text.replace(student_id, PLACEHOLDER)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def _git(*args: str) -> str:
    try:
        return subprocess.run(["git", *args], cwd=UNIT_DIR, capture_output=True, text=True,
                              encoding="utf-8", check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise PackagingError(f"git {' '.join(args)} failed: packaging needs the git checkout") from exc


def tracked_files(items=TRACKED_ITEMS) -> list[str]:
    """The tracked files under ``items`` (unit-relative, '/' separators, sorted)."""
    out = _git("ls-files", "--", *items)
    files = sorted(p for p in out.splitlines() if p)
    missing = [i for i in items if not any(f == i or f.startswith(i + "/") for f in files)]
    if missing:
        raise PackagingError(f"nothing tracked under {missing}")
    return files


def check_committed(items=TRACKED_ITEMS + ("hw2.ipynb",)) -> None:
    """The packaged tracked files equal the committed ones (no modified or untracked file)."""
    dirty = [line for line in _git("status", "--porcelain", "--untracked-files=all", "--", *items)
             .splitlines() if line and "__pycache__" not in line]
    if dirty:
        raise PackagingError(f"uncommitted changes in packaged paths: {dirty[:10]}")


def check_single_run(nb, model_data: dict) -> dict:
    """DA N-3: the notebook is one complete run that produced the exported ``model_data``."""
    code = [c for c in nb.cells if c.cell_type == "code"]
    counts = [c.get("execution_count") for c in code]
    if counts != list(range(1, len(code) + 1)):
        raise PackagingError(f"execution counts are not 1..{len(code)} in order (mixed or partial run)")
    for i, c in enumerate(code):
        if any(o.get("output_type") == "error" for o in c.get("outputs", [])):
            raise PackagingError(f"code cell {i + 1} has an error output")
    run_id = model_data["meta"]["test_evaluation"]["manifest"]["run_id"]
    marked = [c for c in code if EVALUATION_CELL_MARK in c.source]
    if len(marked) != 1:
        raise PackagingError(f"expected one test-evaluation cell, found {len(marked)}")
    text = "".join(o.get("text", "") for o in marked[0].get("outputs", [])
                   if o.get("output_type") == "stream")
    if f"'run_id': '{run_id}'" not in text:
        raise PackagingError("the notebook's test-evaluation output is not the run that wrote model_data")
    report.check_formal_evaluation(model_data)
    return {"code_cells": len(code), "run_id": run_id}


def entries(student_id: str, report_pdf: Path, chatgpt_pdf: Path, files: list[str]) -> list[Entry]:
    out = [Entry(notebook_name(student_id), NOTEBOOK), Entry(REPORT_PDF_NAME, report_pdf),
           Entry(chatgpt_pdf.name, chatgpt_pdf)]
    out += [Entry(f, UNIT_DIR / f) for f in files]
    names = [e.arcname for e in out]
    if len(set(names)) != len(names):
        raise PackagingError("duplicate ZIP entry names")
    return out


def write_zip(path: Path, top: str, items: list[Entry]) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for e in items:
            info = zipfile.ZipInfo(f"{top}/{e.arcname}", date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, e.source.read_bytes())


def verify_zip(path: Path, top: str, items: list[Entry]) -> list[dict]:
    """Read the ZIP back: the entry names and every entry's sha256 equal the sources."""
    rows = []
    with zipfile.ZipFile(path) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise PackagingError("a ZIP entry failed its CRC check")
        names = zf.namelist()
        expected = [f"{top}/{e.arcname}" for e in items]
        if names != expected:
            raise PackagingError("the ZIP entries differ from the packaged list")
        for e in items:
            digest = hashlib.sha256(zf.read(f"{top}/{e.arcname}")).hexdigest()
            if digest != sha256_file(e.source):
                raise PackagingError("a ZIP entry differs from its source")
            rows.append({"path": e.arcname, "size": e.source.stat().st_size, "sha256": digest})
    return rows


def package(dist_dir: Path = DIST_DIR, materials_dir: Path = ACCEPTOR_MATERIALS_DIR) -> dict:
    student_id = local_config.read_student_id()
    check_committed()
    nb = nbformat.read(NOTEBOOK, as_version=4)
    model_data = json.loads(MODEL_DATA_JSON.read_text(encoding="utf-8"))
    run = check_single_run(nb, model_data)
    rel, expected = report.ACCEPTOR_MATERIALS["chatgpt_pdf"]
    chatgpt_pdf = Path(materials_dir) / rel
    if not chatgpt_pdf.is_file() or sha256_file(chatgpt_pdf) != expected:
        raise PackagingError(f"the author's ChatGPT PDF ({rel}) is missing or differs from its receipt")
    files = tracked_files()
    dist_dir = Path(dist_dir)
    report_dir = dist_dir / "report"
    built = report.build(report_dir, pdf=True, final=True)
    if built.get("pending"):
        raise PackagingError(f"report sections pending: {built['pending']}")
    report_pdf = report_dir / REPORT_PDF_NAME
    if not report_pdf.is_file():
        raise PackagingError("the report PDF was not built")

    dist_dir.mkdir(parents=True, exist_ok=True)
    nb_out = dist_dir / notebook_name(student_id)
    shutil.copyfile(NOTEBOOK, nb_out)
    if sha256_file(nb_out) != sha256_file(NOTEBOOK):
        raise PackagingError("the submitted notebook differs from hw2.ipynb")
    items = entries(student_id, report_pdf, chatgpt_pdf, files)
    top = f"{student_id}_hw2"
    zip_path = dist_dir / zip_name(student_id)
    write_zip(zip_path, top, items)
    rows = verify_zip(zip_path, top, items)
    result = {
        "zip": mask(zip_path.name, student_id), "zip_sha256": sha256_file(zip_path),
        "zip_bytes": zip_path.stat().st_size, "top_folder": mask(top, student_id),
        "notebook": mask(nb_out.name, student_id), "notebook_sha256": sha256_file(nb_out),
        "commit": _git("rev-parse", "HEAD").strip(), "run": run,
        "result_digest": report.FORMAL_EVALUATION["result_digest"],
        "entries": [dict(r, path=mask(r["path"], student_id)) for r in rows],
    }
    (dist_dir / MANIFEST_NAME).write_text(json.dumps(result, ensure_ascii=False, indent=1),
                                          encoding="utf-8")
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.parse_args(argv)
    try:
        result = package()
    except (PackagingError, report.ReportError, local_config.LocalConfigError) as exc:
        print(f"packaging failed: {exc}", file=sys.stderr)
        return 1
    summary = {k: v for k, v in result.items() if k != "entries"}
    summary["n_entries"] = len(result["entries"])
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
