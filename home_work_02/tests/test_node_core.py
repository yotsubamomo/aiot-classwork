"""Runs the Node test of the dashboard core (tests/js/core.test.js) against a synthetic fixture
model_data (Spec rev 5 主 seam, JS side; DA TR-01: fixture only, written to a temporary path)."""
import os
import shutil
import subprocess

import pytest

from hw2.paths import UNIT_DIR

NODE = shutil.which("node")


@pytest.mark.skipif(NODE is None, reason="node not installed")
def test_node_core_reproduces_the_fixture_contract(fixture_model_data):
    _, json_path = fixture_model_data
    env = dict(os.environ, HW2_FIXTURE_MODEL_DATA=str(json_path))
    result = subprocess.run([NODE, "--test", "--test-reporter=tap", "tests/js/core.test.js"],
                            cwd=UNIT_DIR, env=env, capture_output=True, text=True,
                            encoding="utf-8")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "# skipped 0" in result.stdout and "# fail 0" in result.stdout
