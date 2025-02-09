#!/usr/bin/env pytest

import os
import shlex
import shutil
import subprocess
import unittest

from fandango.cli import get_parser


class test_slices(unittest.TestCase):

    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

    def test_startswith(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>.startswith("6")' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_0(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>[0] == "6"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_0plus(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>[0:] == "66"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_1plus(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>[1:] == "6"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_str0plus(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c 'str(<start>[0:1]) == "6"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_plus1(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>[:1] == "6"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_plus(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c '<start>[:] == "66"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_slice_str0(self):
        command = shlex.split(
            """fandango fuzz -f tests/resources/twodigits.fan -n 1 -c 'str(<start>)[0] == "6"' --format=none --validate --random-seed 426912 --population-size 10"""
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

