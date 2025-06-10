#!/usr/bin/env pytest

import glob
import shlex
import subprocess
import unittest

import pytest


def run_command(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out.decode(), err.decode(), proc.returncode


files = glob.glob("tests/resources/*.fan") + glob.glob("docs/*.fan")


@pytest.mark.parametrize("fan_file", files)
def test_file(fan_file):
    """Test the C++ and python .fan parsers for `fan_file`."""

    command = shlex.split(
        f"fandango --parser=python dump --no-cache --no-stdlib {fan_file}"
    )
    python_out, err, return_code = run_command(command)
    assert return_code == 0
    assert err == ""

    command = shlex.split(
        f"fandango --parser=cpp dump --no-cache --no-stdlib {fan_file}"
    )
    speedy_out, err, return_code = run_command(command)
    assert return_code == 0
    assert err == ""

    assert (
        python_out == speedy_out
    ), f"{fan_file} produced different outputs for Python and Speedy parsers:\n\nPython output:\n{python_out}\n\nSpeedy output:\n{speedy_out}"


if __name__ == "__main__":
    unittest.main()
