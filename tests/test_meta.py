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
    # Pop cached experimental imports so repeated import_module matches a fresh load;
    # restore afterward so later tests on this worker see the same sys.modules as before.
    saved = {}
    for name in list(sys.modules):
        if name == "fandango.experimental" or name.startswith("fandango.experimental."):
            saved[name] = sys.modules.pop(name)

    try:
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
                "`fandango.experimental.execution.trace_types` is experimental"
                in message
                for message in experimental_warnings
            )
            == 1
        )
    finally:
        for name in list(sys.modules):
            if name == "fandango.experimental" or name.startswith(
                "fandango.experimental."
            ):
                del sys.modules[name]
        sys.modules.update(saved)
