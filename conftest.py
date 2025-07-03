import os
from fandango.beartype import activate_beartype


def pytest_configure(config):
    os.environ["FANDANGO_RUN_BEARTYPE"] = "1"
    activate_beartype()


def pytest_collection_modifyitems(items):
    # ensure long-running tests are run first to balance loading across cores
    # so we have to wait less for a single long test to finish running because it was scheduled last
    order = ["cli", "softconstraint", "optimizer", "fan_parsers"]
    priority = [f"tests/{test}.py" for test in order]
    items.sort(
        key=lambda x: (
            priority.index(x.location[0])
            if x.location[0] in priority
            else len(priority)
        )
    )
