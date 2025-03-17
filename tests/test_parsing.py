#!/usr/bin/env pytest

import unittest
import shlex
import subprocess

from fandango.language.grammar import ParseState, Grammar, NodeType
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree


class ParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/fandango.fan")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def test_rules(self):
        self.assertEqual(len(self.grammar._parser._rules), 9)
        self.assertEqual(len(self.grammar._parser._implicit_rules), 1)
        self.assertEqual(
            {((NonTerminal("<number>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<start>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:0>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<number>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:1>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<non_zero>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:2>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<digit>")],
        )
        self.assertEqual(
            {((NonTerminal("<*0*>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal(f"<__{NodeType.STAR}:0>")],
        )
        self.assertEqual(
            {
                (
                    (NonTerminal("<non_zero>"), frozenset()),
                    (NonTerminal(f"<__{NodeType.STAR}:0>"), frozenset()),
                )
            },
            self.grammar._parser._rules[NonTerminal(f"<__{NodeType.CONCATENATION}:0>")],
        )
        self.assertEqual(
            {
                ((Terminal("0"), frozenset()),),
                ((NonTerminal(f"<__{NodeType.CONCATENATION}:0>"), frozenset()),),
            },
            self.grammar._parser._rules[NonTerminal(f"<__{NodeType.ALTERNATIVE}:0>")],
        )
        self.assertEqual(
            {
                ((Terminal("1"), frozenset()),),
                ((Terminal("2"), frozenset()),),
                ((Terminal("3"), frozenset()),),
                ((Terminal("4"), frozenset()),),
                ((Terminal("5"), frozenset()),),
                ((Terminal("6"), frozenset()),),
                ((Terminal("7"), frozenset()),),
                ((Terminal("8"), frozenset()),),
                ((Terminal("9"), frozenset()),),
            },
            self.grammar._parser._rules[NonTerminal(f"<__{NodeType.ALTERNATIVE}:1>")],
        )
        self.assertEqual(
            {
                ((Terminal("0"), frozenset()),),
                ((Terminal("1"), frozenset()),),
                ((Terminal("2"), frozenset()),),
                ((Terminal("3"), frozenset()),),
                ((Terminal("4"), frozenset()),),
                ((Terminal("5"), frozenset()),),
                ((Terminal("6"), frozenset()),),
                ((Terminal("7"), frozenset()),),
                ((Terminal("8"), frozenset()),),
                ((Terminal("9"), frozenset()),),
            },
            self.grammar._parser._rules[NonTerminal(f"<__{NodeType.ALTERNATIVE}:2>")],
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
        for actual_tree in self.grammar.parse_multiple(
            example, "<ab>", mode=Grammar.Parser.ParsingMode.INCOMPLETE
        ):
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


class TestDynamicRepetitionParsing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = open("tests/resources/dynamic_repetition.fan", "r")
        cls.grammar, _ = parse(cls.file, use_stdlib=False, use_cache=False)

    def _test(self, example, tree):
        parsed = False
        for actual_tree in self.grammar.parse_multiple(
            example, mode=Grammar.Parser.ParsingMode.COMPLETE
        ):
            self.assertEqual(tree, actual_tree)
            parsed = True
            break
        self.assertTrue(parsed)

    def test_nested(self):
        self._test(
            "2(3aaa2bb)",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(
                        NonTerminal("<len>"),
                        [
                            DerivationTree(
                                NonTerminal("<number>"),
                                [
                                    DerivationTree(
                                        NonTerminal("<number_start>"),
                                        [DerivationTree(Terminal("2"))],
                                    )
                                ],
                            )
                        ],
                    ),
                    DerivationTree(Terminal("(")),
                    DerivationTree(
                        NonTerminal("<inner>"),
                        [
                            DerivationTree(
                                NonTerminal("<len>"),
                                [
                                    DerivationTree(
                                        NonTerminal("<number>"),
                                        [
                                            DerivationTree(
                                                NonTerminal("<number_start>"),
                                                [DerivationTree(Terminal("3"))],
                                            )
                                        ],
                                    )
                                ],
                            ),
                            DerivationTree(
                                NonTerminal("<letter>"), [DerivationTree(Terminal("a"))]
                            ),
                            DerivationTree(
                                NonTerminal("<letter>"), [DerivationTree(Terminal("a"))]
                            ),
                            DerivationTree(
                                NonTerminal("<letter>"), [DerivationTree(Terminal("a"))]
                            ),
                        ],
                    ),
                    DerivationTree(
                        NonTerminal("<inner>"),
                        [
                            DerivationTree(
                                NonTerminal("<len>"),
                                [
                                    DerivationTree(
                                        NonTerminal("<number>"),
                                        [
                                            DerivationTree(
                                                NonTerminal("<number_start>"),
                                                [DerivationTree(Terminal("2"))],
                                            )
                                        ],
                                    )
                                ],
                            ),
                            DerivationTree(
                                NonTerminal("<letter>"), [DerivationTree(Terminal("b"))]
                            ),
                            DerivationTree(
                                NonTerminal("<letter>"), [DerivationTree(Terminal("b"))]
                            ),
                        ],
                    ),
                    DerivationTree(Terminal(")")),
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
                    DerivationTree(
                        NonTerminal("<digit>"), [DerivationTree(Terminal("4"))]
                    ),
                ],
            ),
        )

    def test_b(self):
        self._test(
            "123456",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(Terminal("12345")),
                    DerivationTree(Terminal("")),
                    DerivationTree(
                        NonTerminal("<digit>"), [DerivationTree(Terminal("6"))]
                    ),
                ],
            ),
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
        command = shlex.split(
            "fandango parse -f docs/infinity.fan --validate tests/resources/abc.txt --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcabc(self):
        command = shlex.split(
            "fandango parse -f docs/infinity.fan --validate tests/resources/abcabc.txt --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcd(self):
        # This should be rejected by the grammar
        command = shlex.split(
            "fandango parse -f docs/infinity.fan tests/resources/abcd.txt --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(1, code)


class TestBitParsing(TestCLIParsing):

    def _test(self, example, tree, grammar):
        parsed = False
        for actual_tree in grammar.parse_multiple(example, "<start>"):
            if tree is None:
                self.fail("Expected None")
            self.assertEqual(tree, actual_tree)
            parsed = True
            break
        if tree is None:
            self.assertTrue(True)
            return
        self.assertTrue(parsed)

    def test_bits_a(self):
        command = shlex.split(
            "fandango parse -f docs/bits.fan tests/resources/a.txt --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_alternative_bits(self):
        file = open("tests/resources/byte_alternative.fan", "r")
        grammar, _ = parse(file, use_stdlib=False, use_cache=False)
        self._test(b"\x00", None, grammar)
        self._test(
            b"\x01",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    *[
                        DerivationTree(
                            NonTerminal("<bit>"), [DerivationTree(Terminal(0))]
                        )
                        for _ in range(7)
                    ],
                    DerivationTree(Terminal(1)),
                ],
            ),
            grammar,
        )
        self._test(
            b"\x02",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    *[
                        DerivationTree(
                            NonTerminal("<bit>"), [DerivationTree(Terminal(0))]
                        )
                        for _ in range(6)
                    ],
                    DerivationTree(Terminal(1)),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                ],
            ),
            grammar,
        )


class TestGIFParsing(TestCLIParsing):
    def test_gif(self):
        command = shlex.split(
            "fandango parse -f docs/gif89a.fan docs/tinytrans.gif --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)


class TestBitstreamParsing(TestCLIParsing):
    def test_bitstream(self):
        command = shlex.split(
            "fandango parse -f tests/resources/bitstream.fan tests/resources/abcd.txt --validate"
        )
        out, err, code = self.run_command(command)
        # Warns that the number of bits (1..5) may not be a multiple of eight, # which is correct
        # self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_bitstream_a(self):
        command = shlex.split(
            "fandango parse -f tests/resources/bitstream-a.fan tests/resources/a.txt --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_bitstream_b(self):
        command = shlex.split(
            "fandango parse -f tests/resources/bitstream-a.fan tests/resources/b.txt --validate"
        )
        out, err, code = self.run_command(command)
        # This should fail
        self.assertNotEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(1, code)

    def test_rgb(self):
        command = shlex.split(
            "fandango parse -f tests/resources/rgb.fan tests/resources/rgb.txt  --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("", out)
        self.assertEqual("", err)

    def test_local_import(self):
        command = shlex.split("fandango fuzz -f tests/resources/import.fan -n 1")
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("import\n", out)
