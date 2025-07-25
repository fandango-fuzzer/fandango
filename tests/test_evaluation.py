import subprocess
import sys


def test_run_evaluation_success():
    """Test that running `python -m evaluation.vs_isla.run_evaluation 1` exits with code 0."""
    result = subprocess.run(
        [sys.executable, "-m", "evaluation.vs_isla.run_evaluation", "1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    print("STDOUT:\n", result.stdout.decode())
    print("STDERR:\n", result.stderr.decode())

    assert result.returncode == 0, "Script did not exit cleanly"
