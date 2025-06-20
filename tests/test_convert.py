#!/usr/bin/env pytest

import shlex
import subprocess
import unittest

from .utils import DOCS_ROOT, PROJECT_ROOT


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
        command = shlex.split(f"fandango convert {DOCS_ROOT / 'persons.fan'}")
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")

    def test_convert_antlr(self):
        command = shlex.split(
            f"fandango convert {PROJECT_ROOT / 'src' / 'fandango' / 'converters' / 'antlr' / 'Calculator.g4'}"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_dtd(self):
        command = shlex.split(
            f"fandango convert {PROJECT_ROOT / 'src' / 'fandango' / 'converters'/ 'dtd' / 'svg11-flat-20110816.dtd'}"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")

    def test_convert_bt(self):
        command = shlex.split(
            "fandango convert --endianness=little --bitfield-order=left-to-right "
            f"{PROJECT_ROOT / 'src' / 'fandango' / 'converters' / 'bt' / 'gif.bt'}"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")

    def test_convert_bt_again(self):
        command = shlex.split(
            "fandango convert --endianness=big --bitfield-order=right-to-left "
            f"{PROJECT_ROOT / 'src' / 'fandango' / 'converters' / 'bt' / 'gif.bt'}"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
