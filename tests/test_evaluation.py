import sys
import pytest

from evaluation.run_evaluation import run_evaluation


def test_run_evaluation_success():
    if sys.platform.startswith("win") or sys.platform.startswith("linux"):
        pytest.skip("bsdtar not supported on Windows and Ubuntu")

    sys.setrecursionlimit(100000)
    run_evaluation(time="1")
