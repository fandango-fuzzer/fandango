import subprocess
import sys

import pytest


def test_run_evaluation_success():
    if sys.platform.startswith("win") or sys.platform.startswith("linux"):
        pytest.skip("bsdtar not supported on Windows and Ubuntu")

    """Test that running `python -m evaluation.run_evaluation 1` exits with code 0."""
    result = subprocess.run(
        [sys.executable, "-m", "evaluation.run_evaluation", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("STDOUT:\n", result.stdout.decode())
    print("STDERR:\n", result.stderr.decode())

    assert result.returncode == 0, "Script did not exit cleanly"
