#!/usr/bin/env pytest

import os
import re
import shlex
import shutil
import subprocess
import unittest
import time

from fandango.cli import get_parser


class test_convert(unittest.TestCase):
    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

    def test_convert_fan(self):
        command = shlex.split("fandango convert docs/persons.fan")
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_antlr(self):
        command = shlex.split(
            "fandango convert src/fandango/converters/antlr/Calculator.g4"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_dtd(self):
        command = shlex.split(
            "fandango convert src/fandango/converters/dtd/svg11-flat-20110816.dtd"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_bt(self):
        command = shlex.split("fandango convert src/fandango/converters/bt/gif.bt")
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
