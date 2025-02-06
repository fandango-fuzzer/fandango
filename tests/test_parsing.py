#!/usr/bin/env pytest

import unittest
import shlex
import subprocess

from fandango.language.grammar import ParseState
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree


class ParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/fandango.fan")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def test_rules(self):
        self.assertEqual(len(self.grammar._parser._rules), 4)
        self.assertEqual(len(self.grammar._parser._implicit_rules), 1)
        self.assertEqual(
            {(NonTerminal("<number>"),)},
            self.grammar._parser._rules[NonTerminal("<start>")],
        )
        self.assertEqual(
            {
                (
                    NonTerminal("<non_zero>"),
                    NonTerminal("<*0*>"),
                ),
                (Terminal("0"),),
            },
            self.grammar._parser._rules[NonTerminal("<number>")],
        )
        self.assertEqual(
            {
                (Terminal("1"),),
                (Terminal("2"),),
                (Terminal("3"),),
                (Terminal("4"),),
                (Terminal("5"),),
                (Terminal("6"),),
                (Terminal("7"),),
                (Terminal("8"),),
                (Terminal("9"),),
            },
            self.grammar._parser._rules[NonTerminal("<non_zero>")],
        )
        self.assertEqual(
            {
                (Terminal("0"),),
                (Terminal("1"),),
                (Terminal("2"),),
                (Terminal("3"),),
                (Terminal("4"),),
                (Terminal("5"),),
                (Terminal("6"),),
                (Terminal("7"),),
                (Terminal("8"),),
                (Terminal("9"),),
            },
            self.grammar._parser._rules[NonTerminal("<digit>")],
        )
        self.assertEqual(
            {
                (),
                (
                    NonTerminal("<digit>"),
                    NonTerminal("<*0*>"),
                ),
            },
            self.grammar._parser._implicit_rules[NonTerminal("<*0*>")],
        )

    # def test_parse_table(self):
    #     table = self.grammar._parser.parse_table("1")
    #     self.assertIn(
    #         ParseState(NonTerminal("<*start*>"), 0, (NonTerminal("<start>"),), dot=1),
    #         table[1],
    #     )


class TestComplexParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/constraints.fan", "r")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def _test(self, example, tree):
        actual_tree = self.grammar.parse(example, "<ab>")
        self.assertEqual(tree, actual_tree)

    def test_bb(self):
        self._test(
            "bb",
            DerivationTree(
                NonTerminal("<ab>"),
                [
                    DerivationTree(
                        NonTerminal("<ab>"),
                        [
                            DerivationTree(
                                NonTerminal("<ab>"),
                                [DerivationTree(Terminal(""))],
                            ),
                            DerivationTree(Terminal("b")),
                        ],
                    ),
                    DerivationTree(Terminal("b")),
                ],
            ),
        )

    def test_b(self):
        self._test(
            "b",
            DerivationTree(
                NonTerminal("<ab>"),
                [
                    DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                    DerivationTree(Terminal("b")),
                ],
            ),
        )

    def test_ab(self):
        self._test(
            "ab",
            DerivationTree(
                NonTerminal("<ab>"),
                [
                    DerivationTree(
                        NonTerminal("<ab>"),
                        [
                            DerivationTree(Terminal("a")),
                            DerivationTree(
                                NonTerminal("<ab>"), [DerivationTree(Terminal(""))]
                            ),
                        ],
                    ),
                    DerivationTree(Terminal("b")),
                ],
            ),
        )

    def test_a(self):
        self._test(
            "a",
            DerivationTree(
                NonTerminal("<ab>"),
                [
                    DerivationTree(Terminal("a")),
                    DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                ],
            ),
        )


class TestIncompleteParsing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/incomplete.fan", "r")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def _test(self, example, tree):
        parsed = False
        for actual_tree in self.grammar.parse_incomplete(example, "<ab>"):
            self.assertEqual(tree, actual_tree)
            parsed = True
            break
        self.assertTrue(parsed)

    def test_a(self):
        self._test(
            "aa",
            DerivationTree(
                NonTerminal("<ab>"),
                [
                    DerivationTree(Terminal("a")),
                    DerivationTree(
                        NonTerminal("<ab>"), [DerivationTree(Terminal("a"))]
                    ),
                ],
            ),
        )


class TestEmptyParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/empty.fan", "r")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def _test(self, example, tree):
        actual_tree = self.grammar.parse(example)
        self.assertEqual(tree, actual_tree)

    def test_a(self):
        self._test(
            "1234",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(Terminal("123")),
                    DerivationTree(NonTerminal("<digit>"),
                            [DerivationTree(Terminal("4"))]
                    ),
                ],
            ),
        )

    def test_b(self):
        self._test(
            "123456",
            DerivationTree(
                NonTerminal('<start>'),
                [
                    DerivationTree(Terminal('12345')),
                    DerivationTree(Terminal('')),
                    DerivationTree(NonTerminal('<digit>'),
                                    [DerivationTree(Terminal('6'))]),
                ]
            )
        )

class TestCLIParsing(unittest.TestCase):
    def run_command(self, command):
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        return out.decode(), err.decode(), proc.returncode

class TestRegexParsing(TestCLIParsing):
    def test_infinity_abc(self):
        command = shlex.split("fandango parse -f docs/infinity.fan --validate tests/resources/abc.txt --validate")
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcabc(self):
        command = shlex.split("fandango parse -f docs/infinity.fan --validate tests/resources/abcabc.txt --validate")
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcd(self):
        # This should be rejected by the grammar
        command = shlex.split("fandango parse -f docs/infinity.fan tests/resources/abcd.txt --validate")
        out, err, code = self.run_command(command)
        self.assertEqual(1, code)

class TestBitParsing(TestCLIParsing):
    def test_bits_a(self):
        command = shlex.split("fandango parse -f docs/bits.fan tests/resources/a.txt --validate")
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

class TestGIFParsing(TestCLIParsing):
    def test_gif(self):
        command = shlex.split("fandango parse -f docs/gif89a.fan docs/tinytrans.gif --validate")
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)
