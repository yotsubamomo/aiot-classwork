"""Tracked-file hygiene for the unit (H-1; A-4; BR-03).

The student-id check reads the value from the untracked packaging configuration and never prints
it; when the configuration is absent the check is skipped and says so."""
import shutil
import subprocess

import pytest

from hw2 import local_config
from hw2.paths import PACKAGING_CONFIG, UNIT_DIR

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="git not installed")


def _git(*args, check=True):
    return subprocess.run(["git", *args], cwd=UNIT_DIR, capture_output=True, text=True,
                          encoding="utf-8", check=check)


def _tracked():
    return [p for p in _git("ls-files", "--", ".").stdout.splitlines() if p]


def test_no_forbidden_files_are_tracked():
    bad = []
    for path in _tracked():
        lower = path.lower()
        if lower.endswith(".zip") or lower.endswith("kaggle.json") or "/.env" in "/" + lower:
            bad.append(path)
        if lower.endswith(".pdf") and not lower.startswith("doc/requirement/"):
            bad.append(path)
        if lower.startswith((".local/", "acceptor_materials/", "dist/", ".venv/")) \
                or ".ipynb_checkpoints/" in lower:
            bad.append(path)
    assert bad == []


@pytest.mark.parametrize("probe", [
    ".local/packaging.json",
    "acceptor_materials/chatgpt.pdf",
    "acceptor_materials/notebooklm/sources.txt",
    "acceptor_materials/derived/notebooklm_summary.md",
    "dist/hw2.zip",
    "dist/report.pdf",
    ".venv/Scripts/python.exe",
    ".ipynb_checkpoints/hw2-checkpoint.ipynb",
    "report.pdf",
    "bundle.zip",
    "doc/requirement/HW2-requirements-Multiple Linear regression.pdf",
])
def test_untracked_locations_are_ignored(probe):
    result = _git("check-ignore", "-q", "--no-index", probe, check=False)
    assert result.returncode == 0, f"{probe} is not ignored"


@pytest.mark.parametrize("path", ["data/kc_house_data.csv", "assets/vendor/chart.umd.js"])
def test_byte_pinned_files_have_no_eol_conversion(path):
    out = _git("check-attr", "text", "--", path).stdout.strip()
    assert out.endswith(": text: unset"), out


def test_teacher_documents_stay_trackable():
    probe = "doc/requirement/50 Startups_ Multiple Linear Regression & Feature Selection Explorer.pdf"
    assert _git("check-ignore", "-q", "--no-index", probe, check=False).returncode == 1


def test_no_tracked_file_contains_the_student_id():
    try:
        student_id = local_config.read_student_id()
    except local_config.LocalConfigError:
        pytest.skip(f"packaging configuration {PACKAGING_CONFIG.name} not provided yet")
    result = subprocess.run(["git", "grep", "-q", "-F", "-e", student_id, "--", ":/"],
                            cwd=UNIT_DIR, capture_output=True, check=False)
    assert result.returncode == 1, "a tracked file contains the student id (value not printed)"


def test_read_student_id_rejects_missing_and_placeholder(tmp_path):
    with pytest.raises(local_config.LocalConfigError):
        local_config.read_student_id(tmp_path / "missing.json")
    path = tmp_path / "packaging.json"
    path.write_text('{"student_id": "<學號>"}', encoding="utf-8")
    with pytest.raises(local_config.LocalConfigError) as err:
        local_config.read_student_id(path)
    path.write_text('{"student_id": "A1234567"}', encoding="utf-8")
    assert local_config.read_student_id(path) == "A1234567"
    path.write_text("not json", encoding="utf-8")
    with pytest.raises(local_config.LocalConfigError) as err:
        local_config.read_student_id(path)
    assert "A1234567" not in str(err.value)
