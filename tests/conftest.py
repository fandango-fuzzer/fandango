import os
from pathlib import Path
from shutil import which

from fandango.beartype import activate_beartype
import pytest


def pytest_configure(config: pytest.Config):
    # fail fast in exceptions, don't just print them
    os.environ["FANDANGO_RAISE_ALL_EXCEPTIONS"] = "1"

    if not os.environ.get("FANDANGO_FORCE_SKIP_BEARTYPE", False):
        # ensure beartype activation if a subprocess is invoked from a unit test
        os.environ["FANDANGO_RUN_BEARTYPE"] = "1"
        activate_beartype()
    else:
        print("Skipping beartype because FANDANGO_FORCE_SKIP_BEARTYPE is set")

    if which("fan") is None or which("fcc") is None:
        # Ensure we add an absolute path so it works from any cwd
        repo_root = Path(__file__).resolve().parents[1]
        tool_dir = repo_root / "fcc" / "llvm" / "build" / "compiler"
        if not tool_dir.exists():
            raise AssertionError("fcc compiler was not found; run `make test-tools`")
        os.environ["PATH"] = os.environ["PATH"] + os.pathsep + str(tool_dir)

    if which("llvm-config") is None:
        homebrew_llvm_path = Path("/opt/homebrew/opt/llvm@18/bin")
        if homebrew_llvm_path.exists():
            os.environ["PATH"] = (
                str(homebrew_llvm_path) + os.pathsep + os.environ["PATH"]
            )
        else:
            raise AssertionError(
                f"LLVM is required for tests; make sure to add the same version to the PATH as for building fcc"
            )


def pytest_collection_modifyitems(items: list[pytest.Item]):
    # ensure long-running tests are run first to balance loading across cores
    # so we have to wait less for a single long test to finish running because it was scheduled last
    order = [
        "benchmark",
        "evaluation",
        "cli",
        "softconstraint",
        "optimizer",
        "fan_parsers",
    ]
    priority = [f"tests/test_{test}.py" for test in order]
    items.sort(
        key=lambda x: (
            priority.index(x.location[0])
            if x.location[0] in priority
            else len(priority)
        )
    )
