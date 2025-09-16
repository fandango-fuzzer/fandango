# Copyright 2024 Michael Samoglyadov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Pytest plugin to set PYTHONHASHSEED env var - Windows compatible version."""

import os
import sys
import subprocess

__version__ = "1.0.1"
__author__ = "Michael Samoglyadov"
__license__ = "Apache License, Version 2.0"
__website__ = "https://github.com/mr-mixas/pytest-pythonhashseed"


def pytest_addoption(parser):
    """Add plugin-specific options to pytest."""
    group = parser.getgroup("general")
    group.addoption(
        "--pythonhashseed",
        help="set exact PYTHONHASHSEED env var value",
        type=int,
    )


def pytest_configure(config):
    """Reexec process with correct PYTHONHASHSEED env var."""
    opt_hashseed = config.getoption("pythonhashseed") or 1

    if opt_hashseed is None:
        return

    env_hashseed = os.environ.get("PYTHONHASHSEED")

    if env_hashseed is not None and int(env_hashseed) == opt_hashseed:
        return

    module_spec = sys.modules["__main__"].__spec__

    if module_spec is None:  # run as standalone script
        argv = sys.argv
    else:  # run as `python -m ...`
        # abspath to module instead of binary in argv[0] in this case
        # see details in https://bugs.python.org/issue23427#msg371022
        module_name = module_spec.name.rsplit(".", 1)[0]
        argv = [sys.executable, "-m", module_name, *sys.argv[1:]]

    os.environ["PYTHONHASHSEED"] = str(opt_hashseed)

    if sys.platform == "win32":
        # Print to stderr for debugging (won't interfere with pytest's logging)
        def debug_print(msg):
            print(f"[PYTHONHASHSEED_DEBUG] {msg}", file=sys.stderr)

        debug_print("Windows platform detected, using subprocess.run()")
        # On Windows, use subprocess to spawn a new process and wait for it to complete
        debug_print(f"Spawning subprocess with command: {argv}")
        debug_print(f"Environment PYTHONHASHSEED: {os.environ.get('PYTHONHASHSEED')}")

        # Capture both stdout and stderr for better debugging
        result = subprocess.run(
            argv,
            env=os.environ,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
        )

        debug_print(f"Subprocess completed with return code: {result.returncode}")
        debug_print(f"Subprocess stdout: {result.stdout[:500]}...")  # First 500 chars
        debug_print(f"Subprocess stderr: {result.stderr[:500]}...")  # First 500 chars

        # Don't call sys.exit() when running under pytest as it causes SystemExit errors
        # The subprocess will have already run with the correct PYTHONHASHSEED
        if result.returncode != 0:
            # If the subprocess failed, we should indicate this to pytest
            # but not by calling sys.exit() which causes pytest internal errors
            debug_print(f"Subprocess failed with return code {result.returncode}")
            debug_print(f"Full stdout: {result.stdout}")
            debug_print(f"Full stderr: {result.stderr}")
            raise RuntimeError(
                f"Subprocess failed with return code {result.returncode}. "
                f"stdout: {result.stdout}, stderr: {result.stderr}"
            )
        else:
            debug_print("Subprocess completed successfully")
    else:
        # On Unix-like systems, use os.execvpe to replace the current process
        os.execvpe(argv[0], argv, os.environ)  # noqa: S606
