#!/usr/bin/env pytest

import subprocess
import unittest

from .utils import DOCS_ROOT, PROJECT_ROOT


class test_convert(unittest.TestCase):
    def run_command(self, command_list):
        proc = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

    def test_convert_fan(self):
        command = ["fandango", "convert", str(DOCS_ROOT / "persons.fan")]
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")

    def test_convert_antlr(self):
        calculator = (
            PROJECT_ROOT / "src" / "fandango" / "converters" / "antlr" / "Calculator.g4"
        )
        command = [
            "fandango",
            "convert",
            str(calculator),
        ]
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_dtd(self):
        svg = (
            PROJECT_ROOT
            / "src"
            / "fandango"
            / "converters"
            / "dtd"
            / "svg11-flat-20110816.dtd"
        )
        command = [
            "fandango",
            "convert",
            str(svg),
        ]
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")

    def test_convert_bt(self):
        gif = PROJECT_ROOT / "src" / "fandango" / "converters" / "bt" / "gif.bt"
        command = [
            "fandango",
            "convert",
            "--endianness=little",
            "--bitfield-order=left-to-right",
            str(gif),
        ]
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_bt_again(self):
        gif = PROJECT_ROOT / "src" / "fandango" / "converters" / "bt" / "gif.bt"
        command = [
            "fandango",
            "convert",
            "--endianness=big",
            "--bitfield-order=right-to-left",
            str(gif),
        ]
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
