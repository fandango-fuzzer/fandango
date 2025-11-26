import os

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
