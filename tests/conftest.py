import os
from fandango.beartype import activate_beartype
import pytest

# Register the pytest_pythonhashseed_fix plugin
pytest_plugins = ["fandango.pytest_pythonhashseed_fix"]


def pytest_configure(config: pytest.Config):
    # ensure beartype activation if a subprocess is invoked from a unit test
    os.environ["FANDANGO_RUN_BEARTYPE"] = "1"
    # fail fast in exceptions, don't just print them
    os.environ["FANDANGO_RAISE_ALL_EXCEPTIONS"] = "1"
    activate_beartype()


def pytest_collection_modifyitems(items: list[pytest.Item]):
    # ensure long-running tests are run first to balance loading across cores
    # so we have to wait less for a single long test to finish running because it was scheduled last
    order = ["evaluation", "cli", "softconstraint", "optimizer", "fan_parsers"]
    priority = [f"tests/test_{test}.py" for test in order]
    items.sort(
        key=lambda x: (
            priority.index(x.location[0])
            if x.location[0] in priority
            else len(priority)
        )
    )
