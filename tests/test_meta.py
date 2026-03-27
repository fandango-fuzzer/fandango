import os
import sys
import importlib
import warnings

from beartype.roar import BeartypeCallHintParamViolation
import pytest

from fandango.meta import dummy_function_to_check_if_beartype_is_active


def test_pythonhashseed():
    assert os.environ.get("PYTHONHASHSEED", None)


def test_beartype_is_active():
    assert os.environ.get("FANDANGO_RUN_BEARTYPE", False)
    assert 1 == dummy_function_to_check_if_beartype_is_active(1)
    with pytest.raises(BeartypeCallHintParamViolation):
        dummy_function_to_check_if_beartype_is_active("1")  # type: ignore[arg-type] # well, we are testing this


def test_experimental_submodule_warning_once_per_module():
    # Re-import experimental modules from a clean state to make warning counts deterministic.
    for module_name in sys.modules:
        assert not module_name.startswith(
            "fandango.experimental."
        ), f"Module {module_name} should not be in sys.modules"

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        importlib.import_module("fandango.experimental.execution.trace_types")
        importlib.import_module("fandango.experimental.execution.trace_types")

    experimental_warnings = [
        str(w.message)
        for w in caught
        if "is experimental and may change without notice" in str(w.message)
    ]

    assert (
        sum(
            "`fandango.experimental.execution.trace_types` is experimental" in message
            for message in experimental_warnings
        )
        == 1
    )
