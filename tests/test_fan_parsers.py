#!/usr/bin/env pytest

import glob
import random
import shutil
import tempfile
import unittest
from pathlib import Path

import pytest

from .utils import DOCS_ROOT, RESOURCES_ROOT, run_command

files = glob.glob(str(RESOURCES_ROOT / "*.fan")) + glob.glob(str(DOCS_ROOT / "*.fan"))
diff_probability = 5 / len(files)  # Randomly test about 5 files


@pytest.mark.parametrize("fan_file", files)
def test_file(fan_file):
    """Test the C++ and python .fan parsers for `fan_file`."""

    if random.random() > diff_probability:
        pytest.skip("Skipping file due to diff probability")

    command = ["fandango", "-v", "--parser=python", "convert", fan_file]
    python_out, err, return_code = run_command(command)
    assert return_code == 0, err
    assert err == ""

    command = ["fandango", "--parser=cpp", "convert", fan_file]
    cpp_out, err, return_code = run_command(command)
    assert return_code == 0, err
    assert err == ""

    msg = f"{fan_file} produced different outputs for Python and C++ parsers:\n\nPython output:\n{python_out}\n\nC++ output:\n{cpp_out}"
    assert python_out == cpp_out, msg


def test_includes():
    tmp_dir = tempfile.mkdtemp()
    outer_file = Path(tmp_dir) / "include_outer.fan"
    inner_file = Path(tmp_dir) / "include_inner.fan"
    outer_file.write_text('include("include_inner.fan")\n')
    inner_file.write_text('<start> ::= "Hello, World"\n')
    command = ["fandango", "fuzz", "-n", "1", "-f", outer_file]
    out, err, return_code = run_command(command)
    assert return_code == 0, err
    assert err == ""
    assert out == "Hello, World\n"
    shutil.rmtree(tmp_dir)


@pytest.mark.parametrize(
    "include_path",
    [
        "relative/include_inner.fan",
        "./relative/include_inner.fan",
        "r1/r2/r3/include_inner.fan",
        "./r1/../r1/r2/../r2/r3/../r3/include_inner.fan",
    ],
)
def test_relative_includes(include_path):
    tmp_dir = tempfile.mkdtemp()
    outer_file = Path(tmp_dir) / "include_outer.fan"
    inner_file = Path(tmp_dir) / include_path
    inner_file.parent.mkdir(parents=True, exist_ok=True)
    outer_file.write_text(f'include("{include_path}")\n')
    inner_file.write_text('<start> ::= "Hello, World"\n')
    command = ["fandango", "fuzz", "-n", "1", "-f", outer_file]
    out, err, return_code = run_command(command)
    assert return_code == 0, err
    assert err == ""
    assert out == "Hello, World\n"
    shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()
