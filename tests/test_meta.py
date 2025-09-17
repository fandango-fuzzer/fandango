import os


def test_pythonhashseed():
    assert os.environ.get("PYTHONHASHSEED", None)
