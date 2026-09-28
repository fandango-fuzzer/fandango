import os

import pytest


def pytest_configure(config: pytest.Config):
    # fail fast in exceptions, don't just print them
    os.environ["FANDANGO_RAISE_ALL_EXCEPTIONS"] = "1"
    os.environ["FANDANGO_DISABLE_UPDATE_CHECK"] = "1"

    if os.environ.get("FANDANGO_FORCE_SKIP_BEARTYPE", False):
        print("Skipping beartype because FANDANGO_FORCE_SKIP_BEARTYPE is set")
        return
    if config.option.benchmark_enable and config.option.benchmark_only:
        print("Skipping beartype because this run only measures benchmarks")
        return
    if config.option.benchmark_enable:
        print(
            "beartype stays on because this run holds tests besides the "
            "benchmarks, so the timings include its overhead. Add "
            "--benchmark-only to measure without it."
        )

    os.environ["FANDANGO_RUN_BEARTYPE"] = "1"
    # Static code in the main __init__.py triggers beartype activation.
    # This needs to happen after the environment variable is set.
    import fandango  # noqa: F401 # by definition an unused import


def pytest_collection_modifyitems(items: list[pytest.Item]):
    # ensure long-running tests are run first to balance loading across cores
    # so we have to wait less for a single long test to finish running because it was scheduled last
    order = [
        "benchmark",
        "evaluation",
        "cli",
        "softconstraint",
        "execution_feedback",
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
