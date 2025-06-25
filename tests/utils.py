import subprocess
from pathlib import Path

TEST_ROOT = Path(__file__).parent
RESOURCES_ROOT = TEST_ROOT / "resources"
PROJECT_ROOT = TEST_ROOT.parent
DOCS_ROOT = PROJECT_ROOT / "docs"


def run_command(command_list, input=None):
    """Run a command and return normalized output with consistent line endings.

    Args:
        command_list: List of command arguments

    Returns:
        tuple: (stdout, stderr, return_code) with line endings normalized to \n
    """
    stdin = subprocess.PIPE if input else None
    proc = subprocess.Popen(
        command_list,
        stdin=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if input is None:
        input_bytes = None
    elif isinstance(input, str):
        input_bytes = input.encode()
    else:
        input_bytes = input

    out, err = proc.communicate(input=input_bytes)

    # Decode bytes to str with UTF-8 encoding and error handling
    out_normalized = out.decode("utf-8") if isinstance(out, bytes) else out
    err_normalized = err.decode("utf-8") if isinstance(err, bytes) else err

    # Normalize line endings for cross-platform compatibility
    out_normalized = out_normalized.replace("\r\n", "\n")
    err_normalized = err_normalized.replace("\r\n", "\n")
    return out_normalized, err_normalized, proc.returncode
