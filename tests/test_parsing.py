#!/usr/bin/env pytest

import shlex
import subprocess
import unittest

from fandango.language.grammar import NodeType, Grammar
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from .utils import RESOURCES_ROOT, DOCS_ROOT


class ParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(RESOURCES_ROOT / "fandango.fan") as file:
            cls.grammar, _ = parse(file, use_stdlib=False, use_cache=False)

    def test_rules(self):
        self.assertEqual(len(self.grammar._parser._rules), 9)
        self.assertEqual(len(self.grammar._parser._implicit_rules), 1)
        self.assertEqual(
            {((NonTerminal("<number>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<start>")],
        )
        alt_1 = self.grammar.rules[NonTerminal("<number>")]
        alt_2 = self.grammar.rules[NonTerminal("<non_zero>")]
        alt_3 = self.grammar.rules[NonTerminal("<digit>")]
        concat_1 = alt_1.children()[0]
        star_1 = concat_1.children()[1]

        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_1.id}>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<number>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_2.id}>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<non_zero>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_3.id}>"), frozenset()),)},
            self.grammar._parser._rules[NonTerminal("<digit>")],
        )
        self.assertEqual(
            {((NonTerminal("<*0*>"), frozenset()),)},
            self.grammar._parser._rules[
                NonTerminal(f"<__{NodeType.STAR}:{star_1.id}>")
            ],
        )
        self.assertEqual(
            {
                (
                    (NonTerminal("<non_zero>"), frozenset()),
                    (NonTerminal(f"<__{NodeType.STAR}:{star_1.id}>"), frozenset()),
                )
            },
            self.grammar._parser._rules[
                NonTerminal(f"<__{NodeType.CONCATENATION}:{concat_1.id}>")
            ],
        )
        self.assertEqual(
            {
                ((Terminal("0"), frozenset()),),
                (
                    (
                        NonTerminal(f"<__{NodeType.CONCATENATION}:{concat_1.id}>"),
                        frozenset(),
                    ),
                ),
            },
            self.grammar._parser._rules[
                NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_1.id}>")
            ],
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
            self.grammar._parser._rules[
                NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_2.id}>")
            ],
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
            self.grammar._parser._rules[
                NonTerminal(f"<__{NodeType.ALTERNATIVE}:{alt_3.id}>")
            ],
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
        with open(RESOURCES_ROOT / "constraints.fan") as file:
            cls.grammar, _ = parse(file, use_stdlib=False, use_cache=False)

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
                                NonTerminal("<ab>"), [DerivationTree(Terminal(""))]
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
        with open(RESOURCES_ROOT / "incomplete.fan") as file:
            cls.grammar, _ = parse(file, use_stdlib=False, use_cache=False)

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
        with open(RESOURCES_ROOT / "dynamic_repetition.fan") as file:
            cls.grammar, _ = parse(file, use_stdlib=False, use_cache=False)

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
        with open(RESOURCES_ROOT / "empty.fan") as file:
            cls.grammar, _ = parse(file, use_stdlib=False, use_cache=False)

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
    @staticmethod
    def run_command(command):
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
            "fandango parse -f "
            f"{DOCS_ROOT / 'infinity.fan'} --validate {RESOURCES_ROOT / 'abc.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcabc(self):
        command = shlex.split(
            "fandango parse -f "
            f"{DOCS_ROOT / 'infinity.fan'} --validate {RESOURCES_ROOT / 'abcabc.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_infinity_abcd(self):
        # This should be rejected by the grammar
        command = shlex.split(
            "fandango parse -f "
            f"{DOCS_ROOT / 'infinity.fan'} {RESOURCES_ROOT / 'abcd.txt'} --validate"
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
            "fandango parse -f "
            f"{DOCS_ROOT / 'bits.fan'} {RESOURCES_ROOT / 'a.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_alternative_bits(self):
        with open(RESOURCES_ROOT / "byte_alternative.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
        self._test(b"\x00", None, grammar)
        self._test(
            b"\x01",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
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
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                    DerivationTree(Terminal(1)),
                    DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
                ],
            ),
            grammar,
        )


class TestGIFParsing(TestCLIParsing):
    def test_gif(self):
        command = shlex.split(
            "fandango parse -f "
            f"{DOCS_ROOT / 'gif89a.fan'} {DOCS_ROOT / 'tinytrans.gif'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)


class TestBitstreamParsing(TestCLIParsing):
    def test_bitstream(self):
        command = shlex.split(
            "fandango parse -f "
            f"{RESOURCES_ROOT / 'bitstream.fan'} {RESOURCES_ROOT / 'abcd.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        # Warns that the number of bits (1..5) may not be a multiple of eight, # which is correct
        # self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_bitstream_a(self):
        command = shlex.split(
            "fandango parse -f "
            f"{RESOURCES_ROOT / 'bitstream-a.fan'} {RESOURCES_ROOT / 'a.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(0, code)

    def test_bitstream_b(self):
        command = shlex.split(
            "fandango parse -f "
            f"{RESOURCES_ROOT / 'bitstream-a.fan'} {RESOURCES_ROOT / 'b.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        # This should fail
        self.assertNotEqual("", err)
        self.assertEqual("", out)
        self.assertEqual(1, code)

    def test_rgb(self):
        command = shlex.split(
            "fandango parse -f "
            f"{RESOURCES_ROOT / 'rgb.fan'} {RESOURCES_ROOT / 'rgb.txt'} --validate"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual("", out)
        self.assertEqual("", err)


class TestImportParsing(TestCLIParsing):
    def test_local_import(self):
        command = shlex.split(f"fandango fuzz -f {RESOURCES_ROOT / 'import.fan'} -n 1")
        out, err, code = self.run_command(command)
        self.assertEqual(0, code)
        self.assertEqual("import\n", out)


class TestISO8601Parsing(TestCLIParsing):
    def test_parse_iso8601(self):
        command = shlex.split(
            f"fandango parse -f {DOCS_ROOT / 'iso8601.fan'} {RESOURCES_ROOT / 'iso8601.txt'}"
        )
        out, err, code = self.run_command(command)
        self.assertEqual(0, code, err)
        self.assertEqual("", err)
