import subprocess
from pathlib import Path

TEST_ROOT = Path(__file__).parent
RESOURCES_ROOT = TEST_ROOT / "resources"
PROJECT_ROOT = TEST_ROOT.parent
DOCS_ROOT = PROJECT_ROOT / "docs"


def run_command(command_list):
    """Run a command and return normalized output with consistent line endings.

    Args:
        command_list: List of command arguments

    Returns:
        tuple: (stdout, stderr, return_code) with line endings normalized to \n
    """
    proc = subprocess.Popen(
        command_list,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    # Normalize line endings for cross-platform compatibility
    # Use errors='replace' to handle encoding issues gracefully
    out_normalized = out.decode(errors="replace").replace("\r\n", "\n")
    err_normalized = err.decode(errors="replace").replace("\r\n", "\n")
    return out_normalized, err_normalized, proc.returncode
