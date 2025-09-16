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

"""Pytest plugin to set PYTHONHASHSEED env var."""

import os
import sys

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
    opt_hashseed = config.getoption("pythonhashseed")

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

    # Use execvpe on Unix-like systems, execv on Windows
    if sys.platform == "win32":
        os.execv(argv[0], argv)  # noqa: S606
    else:
        os.execvpe(argv[0], argv, os.environ)  # noqa: S606
