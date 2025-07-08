#!/usr/bin/env pytest

import unittest

from fandango.language.parse import parse

from .utils import DOCS_ROOT, PROJECT_ROOT, run_command


class test_convert(unittest.TestCase):
    def _check_output(self, grammar: str, start_symbol: str) -> None:
        parsed_grammar, _constraints = parse(grammar, start_symbol=start_symbol)
        self.assertIsNotNone(parsed_grammar, grammar)

    def test_convert_fan(self):
        command = ["fandango", "convert", str(DOCS_ROOT / "persons.fan")]
        out, err, code = run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")
        self._check_output(out, "<start>")

    def test_convert_antlr(self):
        calculator = (
            PROJECT_ROOT / "src" / "fandango" / "converters" / "antlr" / "Calculator.g4"
        )
        command = [
            "fandango",
            "convert",
            str(calculator),
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
        self._check_output(out, "<expression>")

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
        out, err, code = run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual(err, "")
        self._check_output(out, "<svg>")

    def test_convert_bt(self):
        gif = PROJECT_ROOT / "src" / "fandango" / "converters" / "bt" / "gif.bt"
        command = [
            "fandango",
            "convert",
            "--endianness=little",
            "--bitfield-order=left-to-right",
            str(gif),
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
        self._check_output(out, "<start>")

    def test_convert_bt_again(self):
        gif = PROJECT_ROOT / "src" / "fandango" / "converters" / "bt" / "gif.bt"
        command = [
            "fandango",
            "convert",
            "--endianness=big",
            "--bitfield-order=right-to-left",
            str(gif),
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code)
        self.assertEqual(err, "")
        self._check_output(out, "<start>")
