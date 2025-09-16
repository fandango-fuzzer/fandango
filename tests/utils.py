import os
import subprocess
from pathlib import Path
import sys

TEST_ROOT = Path(__file__).parent
RESOURCES_ROOT = TEST_ROOT / "resources"
PROJECT_ROOT = TEST_ROOT.parent
DOCS_ROOT = PROJECT_ROOT / "docs"

IS_BEARTYPE_ACTIVE = os.environ.get("FANDANGO_RUN_BEARTYPE", False)


def run_command(command_list, input=None):
    """Run a command and return normalized output with consistent line endings.

    Args:
        command_list: List of command arguments
        input: Optional input to pass to stdin

    Returns:
        tuple: (stdout, stderr, return_code) with line endings normalized to \n
    """
    stdin = subprocess.PIPE if input else None

    env = os.environ.copy()
    if sys.platform.startswith("win"):
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

    if IS_BEARTYPE_ACTIVE:
        env["FANDANGO_RUN_BEARTYPE"] = "1"

    env["PYTHONHASHSEED"] = "0"  # ensure reproducability

    proc = subprocess.Popen(
        command_list,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        env=env,
    )

    # When using encoding, pass text input directly
    input_text = (
        input if input is None or isinstance(input, str) else input.decode("utf-8")
    )

    out, err = proc.communicate(input=input_text)

    # Normalize line endings for cross-platform compatibility
    out_normalized = out.replace("\r\n", "\n")
    err_normalized = err.replace("\r\n", "\n")
    return out_normalized, err_normalized, proc.returncode
