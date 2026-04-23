import os
import socket
import subprocess
from functools import lru_cache
from pathlib import Path
import sys

TEST_ROOT = Path(__file__).parent
RESOURCES_ROOT = TEST_ROOT / "resources"
PROJECT_ROOT = TEST_ROOT.parent
DOCS_ROOT = PROJECT_ROOT / "docs"
EVALUATION_ROOT = PROJECT_ROOT / "evaluation"
VENV_BIN = (
    PROJECT_ROOT / ".venv" / ("Scripts" if sys.platform.startswith("win") else "bin")
)
FANDANGO_CLI = VENV_BIN / (
    "fandango.exe" if sys.platform.startswith("win") else "fandango"
)

IS_BEARTYPE_ACTIVE = os.environ.get("FANDANGO_RUN_BEARTYPE", False)


def command_env():
    env = os.environ.copy()
    if sys.platform.startswith("win"):
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONUTF8"] = "1"

    if IS_BEARTYPE_ACTIVE:
        env["FANDANGO_RUN_BEARTYPE"] = "1"

    env["PYTHONHASHSEED"] = "0"  # ensure reproducibility
    if VENV_BIN.is_dir():
        env["PATH"] = os.pathsep.join([str(VENV_BIN), env.get("PATH", "")])
    return env


def resolve_command(command_list):
    if command_list and command_list[0] == "fandango" and FANDANGO_CLI.is_file():
        return [str(FANDANGO_CLI), *command_list[1:]]
    return command_list


@lru_cache(maxsize=1)
def can_bind_local_tcp_socket() -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("127.0.0.1", 0))
    except OSError:
        return False
    return True


def run_command(command_list, input=None):
    """Run a command and return normalized output with consistent line endings.

    Args:
        command_list: List of command arguments
        input: Optional input to pass to stdin

    Returns:
        tuple: (stdout, stderr, return_code) with line endings normalized to \n
    """
    stdin = subprocess.PIPE if input else None

    env = command_env()

    proc = subprocess.Popen(
        resolve_command(command_list),
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
