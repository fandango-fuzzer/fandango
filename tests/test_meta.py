import os
import sys
import importlib
import warnings
from contextlib import contextmanager
from collections.abc import Generator

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


@contextmanager
def _cleared_experimental_modules() -> Generator[None, None, None]:
    """Drop cached experimental imports; restore on exit so other tests are unaffected."""
    saved = {
        n: sys.modules.pop(n)
        for n in list(sys.modules)
        if n == "fandango.experimental" or n.startswith("fandango.experimental.")
    }
    try:
        yield
    finally:
        for n in list(sys.modules):
            if n == "fandango.experimental" or n.startswith("fandango.experimental."):
                del sys.modules[n]
        sys.modules.update(saved)


def test_experimental_submodule_warning_once_per_module():
    """Repeated imports of the same direct child still emit only one warning for it."""
    mod = "fandango.experimental.execution"
    with _cleared_experimental_modules():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            for _ in range(5):
                importlib.import_module(mod)

        needle = "`fandango.experimental.execution` is experimental"
        assert sum(needle in str(w.message) for w in caught) == 1


def test_experimental_dynamic_import_no_duplicate_warnings():
    """``from ...fcc import FCC`` warns for the direct child ``execution`` only, not ``fcc``."""
    with _cleared_experimental_modules():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")

            def load_fcc():
                from fandango.experimental.execution.fcc import FCC

                return FCC

            load_fcc()
            load_fcc()

        needle = "`fandango.experimental.execution` is experimental"
        assert sum(needle in str(w.message) for w in caught) == 1
        assert (
            sum(
                "`fandango.experimental.execution.fcc` is experimental"
                in str(w.message)
                for w in caught
            )
            == 0
        )


def test_experimental_warning_message_contains_expected_text():
    with _cleared_experimental_modules():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.import_module("fandango.experimental.execution")

        needle = "`fandango.experimental.execution` is experimental"
        assert sum(needle in str(w.message) for w in caught) == 1
        assert "is experimental and may change without notice" in str(caught[0].message)
        assert "Avoid relying on its public API in production code" in str(
            caught[0].message
        )


def test_experimental_deep_submodule_import_warns_direct_child_only():
    """Importing ``...execution.trace_types`` only warns for the direct child ``execution``."""
    with _cleared_experimental_modules():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.import_module("fandango.experimental.execution.trace_types")

        needle = "`fandango.experimental.execution` is experimental"
        assert sum(needle in str(w.message) for w in caught) == 1
        assert not any("trace_types" in str(w.message) for w in caught)


def test_experimental_submodule_warning_category():
    with _cleared_experimental_modules():
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.import_module("fandango.experimental.execution")

        from fandango.experimental import ExperimentalWarning

        exp = [
            w
            for w in caught
            if "is experimental and may change without notice" in str(w.message)
        ]
        assert exp
        assert all(issubclass(w.category, ExperimentalWarning) for w in exp)
