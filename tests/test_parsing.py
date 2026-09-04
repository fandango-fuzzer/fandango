#!/usr/bin/env pytest

import unittest
from typing import Optional

from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.repetition import Star
from fandango.language.grammar.parser.iterative_parser import IterativeParser
from fandango.language.grammar.parser.parser import Parser
from fandango.language.parse.parse import parse
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

from .utils import DOCS_ROOT, RESOURCES_ROOT, run_command


class IterParsingTester(Parser):
    def _parse_forest(
        self,
        word: str | bytes,
        start: str | NonTerminal = "<start>",
        *,
        mode: ParsingMode = ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        starter_bit=-1,
    ):
        self._iter_parser.new_parse(start, mode, hookin_parent, starter_bit)
        for char in word:
            self._iter_parser.consume(char)
        if not word:
            self._iter_parser.consume(word)
        for tree, _is_complete in self._iter_parser.tree_at(
            self._iter_parser.consumed_length(),
            incomplete=mode == ParsingMode.INCOMPLETE,
        ):
            yield tree


class ParserTests(unittest.TestCase):
    # Type annotation for instance attribute set in setUp
    grammar: Grammar

    def setUp(self):
        with open(RESOURCES_ROOT / "fandango.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar

    def test_rules(self):
        self.assertEqual(
            len(self.grammar._parser._iter_parser._rules),
            9,
            len(self.grammar._parser._iter_parser._rules),
        )
        self.assertEqual(
            len(self.grammar._parser._iter_parser._implicit_rules),
            1,
            len(self.grammar._parser._iter_parser._implicit_rules),
        )
        self.assertEqual(
            {((NonTerminal("<number>"), frozenset()),)},
            self.grammar._parser._iter_parser._rules[NonTerminal("<start>")],
        )
        alt_1 = self.grammar.rules[NonTerminal("<number>")]
        assert isinstance(alt_1, Alternative)
        alt_2 = self.grammar.rules[NonTerminal("<non_zero>")]
        assert isinstance(alt_2, Alternative)
        alt_3 = self.grammar.rules[NonTerminal("<digit>")]
        assert isinstance(alt_3, Alternative)
        concat_1 = alt_1.children()[0]
        assert isinstance(concat_1, Concatenation)
        star_1 = concat_1.children()[1]
        assert isinstance(star_1, Star)

        self.assertEqual(
            {((NonTerminal(f"<__{alt_1.id}>"), frozenset()),)},
            self.grammar._parser._iter_parser._rules[NonTerminal("<number>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{alt_2.id}>"), frozenset()),)},
            self.grammar._parser._iter_parser._rules[NonTerminal("<non_zero>")],
        )
        self.assertEqual(
            {((NonTerminal(f"<__{alt_3.id}>"), frozenset()),)},
            self.grammar._parser._iter_parser._rules[NonTerminal("<digit>")],
        )
        self.assertEqual(
            {((NonTerminal("<*0*>"), frozenset()),)},
            self.grammar._parser._iter_parser._rules[NonTerminal(f"<__{star_1.id}>")],
        )
        self.assertEqual(
            {
                (
                    (NonTerminal("<non_zero>"), frozenset()),
                    (NonTerminal(f"<__{star_1.id}>"), frozenset()),
                )
            },
            self.grammar._parser._iter_parser._rules[NonTerminal(f"<__{concat_1.id}>")],
        )
        self.assertEqual(
            {
                ((Terminal("0"), frozenset()),),
                (
                    (
                        NonTerminal(f"<__{concat_1.id}>"),
                        frozenset(),
                    ),
                ),
            },
            self.grammar._parser._iter_parser._rules[NonTerminal(f"<__{alt_1.id}>")],
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
            self.grammar._parser._iter_parser._rules[NonTerminal(f"<__{alt_2.id}>")],
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
            self.grammar._parser._iter_parser._rules[NonTerminal(f"<__{alt_3.id}>")],
        )


class TestComplexParsing(unittest.TestCase):
    # Type annotation for instance attribute set in setUp
    grammar: Grammar

    def setUp(self):
        with open(RESOURCES_ROOT / "constraints.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar
            self.parser = Parser(grammar.rules)
            self.iter_parser = IterParsingTester(grammar.rules)

    def _test(self, example, tree):
        for parser in [self.parser, self.iter_parser]:
            actual_tree = parser.parse(example, "<ab>")
            self.assertEqual(tree, actual_tree, actual_tree)

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


class TestAmbiguousParsing(unittest.TestCase):
    def _forest(self, grammar_spec: str, word: str) -> list[DerivationTree]:
        grammar, _ = parse(grammar_spec, use_stdlib=False, use_cache=False)
        assert grammar is not None
        trees = list(Parser(grammar.rules).parse_multiple(word))
        return sorted(trees, key=repr)

    def test_two_alternatives(self):
        forest = self._forest("<start> ::= <b> | <a>\n<b> ::= '0'\n<a> ::= '0'\n", "0")
        self.assertEqual(2, len(forest), forest)
        self.assertEqual(
            [NonTerminal("<a>"), NonTerminal("<b>")],
            [tree.children[0].symbol for tree in forest],
        )

    def test_ambiguity_below_the_root(self):
        forest = self._forest(
            "<start> ::= 'x' <mid> 'y'\n"
            "<mid> ::= <b> | <a>\n"
            "<b> ::= '0'\n"
            "<a> ::= '0'\n",
            "x0y",
        )
        self.assertEqual(2, len(forest), forest)

    def test_unambiguous_yields_one_tree(self):
        forest = self._forest("<start> ::= <a><a>\n<a> ::= '0'\n", "00")
        self.assertEqual(1, len(forest), forest)

    def test_first_tree_is_not_truncated_by_the_cache(self):
        grammar, _ = parse(
            "<start> ::= <b> | <a>\n<b> ::= '0'\n<a> ::= '0'\n",
            use_stdlib=False,
            use_cache=False,
        )
        assert grammar is not None
        parser = Parser(grammar.rules)
        self.assertIsNotNone(parser.parse("0"))
        self.assertEqual(2, len(list(parser.parse_multiple("0"))))


class TestIncompleteParsing(unittest.TestCase):
    # Type annotation for instance attribute set in setUp
    grammar: Grammar

    def setUp(self):
        with open(RESOURCES_ROOT / "incomplete.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar
            self.parser = Parser(grammar.rules)
            self.iter_parser = IterParsingTester(grammar.rules)

    def _test(self, example, tree):
        for parser in [self.parser, self.iter_parser]:
            parsed = False
            for actual_tree in parser.parse_multiple(
                example, "<start>", mode=ParsingMode.INCOMPLETE
            ):
                self.assertEqual(tree, actual_tree, actual_tree)
                parsed = True
                break
            self.assertTrue(parsed)

    def test_a(self):
        self._test(
            "aa",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(
                        NonTerminal("<ab>"),
                        [
                            DerivationTree(Terminal("a")),
                            DerivationTree(
                                NonTerminal("<ab>"), [DerivationTree(Terminal("a"))]
                            ),
                        ],
                    )
                ],
            ),
        )

    def test_regex(self):
        self._test(
            "ii",
            DerivationTree(
                NonTerminal("<start>"),
                [
                    DerivationTree(
                        NonTerminal("<c>"),
                        [
                            DerivationTree(Terminal("ii")),
                        ],
                    ),
                ],
            ),
        )


class TestDynamicRepetitionParsing(unittest.TestCase):
    # Type annotation for instance attribute set in setUp
    grammar: Grammar

    def setUp(self):
        with open(RESOURCES_ROOT / "dynamic_repetition.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar
            self.parser = Parser(grammar.rules)
            self.iter_parser = IterParsingTester(grammar.rules)

    def _test(self, example, tree):
        for parser in [self.parser, self.iter_parser]:
            parsed = False
            for actual_tree in parser.parse_multiple(
                example, mode=ParsingMode.COMPLETE
            ):
                self.assertEqual(tree, actual_tree, actual_tree)
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
    # Type annotation for instance attribute set in setUp
    grammar: Grammar

    def setUp(self):
        with open(RESOURCES_ROOT / "empty.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar
            self.parser = Parser(grammar.rules)
            self.iter_parser = IterParsingTester(grammar.rules)

    def _test(self, example: str, tree: DerivationTree):
        parsers: list[Parser] = [self.parser, self.iter_parser]
        for parser in parsers:
            actual_tree = parser.parse(example)
            print(type(parser), type(actual_tree))
            self.assertEqual(tree, actual_tree, actual_tree)

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


class TestCanContinueParsing(unittest.TestCase):
    def setUp(self):
        with open(RESOURCES_ROOT / "rgb.fan") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
            self.grammar = grammar
            self.iter_parser = IterativeParser(self.grammar.rules)

    def test_1(self):
        self.iter_parser.new_parse()
        self.iter_parser.consume(b"r")
        self.assertTrue(self.iter_parser.can_continue())
        self.iter_parser.consume(b"g")
        self.assertTrue(self.iter_parser.can_continue())
        self.iter_parser.consume(b"b")
        self.assertTrue(self.iter_parser.can_continue())
        self.iter_parser.consume(b"d")
        self.assertTrue(self.iter_parser.can_continue())
        self.iter_parser.consume(b";")
        self.assertFalse(self.iter_parser.can_continue())

        self.iter_parser.new_parse()
        self.iter_parser.consume(b"rgbd;")


class TestIncrementalParsing(unittest.TestCase):
    REPEATING = "<start> ::= 'a'+\n"
    PACKETS = "<start> ::= <msg>\n<msg> ::= 'ping\\n' | 'pong\\n'\n"
    AMBIGUOUS = "<start> ::= <x>\n<x> ::= 'ab' | <a> <b>\n<a> ::= 'a'\n<b> ::= 'b'\n"
    BINARY = "<start> ::= <byte>+\n<byte> ::= b'\\x01' | b'\\x02'\n"
    BITS = "<start> ::= <bit>+\n<bit> ::= 0 | 1\n"
    WIDE = "<start> ::= <c>+\n<c> ::= '\u00e4' | 'b'\n"
    NULLABLE = "<start> ::= <a>*\n<a> ::= 'x'\n"

    def _parser(self, spec: str) -> IterativeParser:
        grammar, _ = parse(spec, use_stdlib=False, use_cache=False)
        assert grammar is not None
        parser = IterativeParser(grammar.rules)
        parser.new_parse(NonTerminal("<start>"), ParsingMode.COMPLETE)
        return parser

    def _bytewise(self, spec: str, word: str | bytes) -> list[tuple[int, list[str]]]:
        """Consume given input one byte/char at a time."""
        parser = self._parser(spec)
        found = []
        for index in range(len(word)):
            parser.consume(word[index : index + 1])
            trees = [
                str(parser.collapse(tree)) for tree, _ in parser.tree_at(index + 1)
            ]
            if trees:
                found.append((index + 1, trees))
        return found

    def _blockwise(
        self, spec: str, word: str | bytes, sizes: Optional[list[int]] = None
    ) -> list[tuple[int, list[str]]]:
        """The same, fed in blocks and read back with `tree_at`."""
        parser = self._parser(spec)
        found = []
        start = 0
        for size in sizes or [len(word)]:
            parser.consume(word[start : start + size])
            start += size
        for offset in parser.parsed_positions():
            found.append(
                (
                    offset,
                    [str(parser.collapse(tree)) for tree, _ in parser.tree_at(offset)],
                )
            )
        return found

    CASES: list[tuple[str, str, str | bytes]] = [
        ("repeating", REPEATING, "aaaa"),
        ("packets", PACKETS, "ping\n"),
        ("ambiguous", AMBIGUOUS, "ab"),
        ("binary", BINARY, b"\x01\x02\x01"),
        ("bits", BITS, b"\x01\x02"),
        ("wide characters", WIDE, "\u00e4b\u00e4"),
    ]

    def test_blockwise_matches_bytewise(self):
        for label, spec, word in self.CASES:
            with self.subTest(label):
                self.assertEqual(
                    self._bytewise(spec, word), self._blockwise(spec, word)
                )

    def test_block_sizes_do_not_matter(self):
        expected = self._bytewise(self.REPEATING, "aaaa")
        for sizes in ([1, 3], [2, 2], [3, 1], [1, 1, 1, 1]):
            with self.subTest(sizes=sizes):
                self.assertEqual(
                    expected, self._blockwise(self.REPEATING, "aaaa", sizes)
                )

    def test_an_offset_is_the_length_of_its_parse(self):
        for label, spec, word in self.CASES:
            with self.subTest(label):
                parser = self._parser(spec)
                parser.consume(word)
                for offset in parser.parsed_positions():
                    for tree, _ in parser.tree_at(offset):
                        self.assertEqual(offset, len(str(parser.collapse(tree))))

    def test_nullable_grammar_empty_parse(self):
        parser = self._parser(self.NULLABLE)
        parser.consume("xx")
        self.assertEqual([0, 1, 2], parser.parsed_positions())
        self.assertEqual([""], [str(parser.collapse(t)) for t, _ in parser.tree_at(0)])

    def test_parsing_on_overshooting_input(self):
        parser = self._parser(self.PACKETS)
        parser.consume("ping\npong\n")
        self.assertEqual([5], parser.parsed_positions())
        self.assertEqual(
            ["ping\n"], [str(parser.collapse(tree)) for tree, _ in parser.tree_at(5)]
        )

    def test_parse_multiple_consumes(self):
        parser = self._parser(self.REPEATING)
        parser.consume("aa")
        self.assertEqual([1, 2], parser.parsed_positions())
        parser.consume("aa")
        self.assertEqual([1, 2, 3, 4], parser.parsed_positions())
        self.assertEqual(
            ["a"], [str(parser.collapse(tree)) for tree, _ in parser.tree_at(1)]
        )
        self.assertEqual(
            ["aaaa"], [str(parser.collapse(tree)) for tree, _ in parser.tree_at(4)]
        )

    def test_tree_emit_at_no_parse_position(self):
        parser = self._parser(self.PACKETS)
        parser.consume("ping\n")
        self.assertEqual([], list(parser.tree_at(3)))

    def test_a_bit_grammar_reports_whole_bytes_only(self):
        parser = self._parser(self.BITS)
        parser.consume(b"\x01\x02")
        self.assertEqual([1, 2], parser.parsed_positions())
        self.assertEqual(
            ["\x01"], [str(parser.collapse(tree)) for tree, _ in parser.tree_at(1)]
        )
        self.assertEqual(
            ["\x01\x02"], [str(parser.collapse(tree)) for tree, _ in parser.tree_at(2)]
        )


class TestIncompleteFlag(unittest.TestCase):
    """
    What `consume` reports as `is_complete` in INCOMPLETE mode.

    A tree that completes the input and could still grow comes out once under
    each flag; one that cannot grow only as complete; one that is not yet a
    parse only as incomplete. The empty parse follows the same rule.
    """

    def _flagged(self, spec: str, word: str) -> list[tuple[str, bool]]:
        grammar, _ = parse(spec, use_stdlib=False, use_cache=False)
        assert grammar is not None
        parser = IterativeParser(grammar.rules)
        parser.new_parse(NonTerminal("<start>"), ParsingMode.INCOMPLETE)
        parser.consume(word)
        return sorted(
            {
                (str(parser.collapse(tree)), is_complete)
                for tree, is_complete in parser.tree_at(len(word), incomplete=True)
            }
        )

    def test_empty_parse_that_can_grow(self):
        self.assertEqual(
            [("", False), ("", True)],
            self._flagged("<start> ::= <a>*\n<a> ::= '0'\n", ""),
        )

    def test_empty_parse_from_an_empty_alternative(self):
        self.assertEqual(
            [("", False), ("", True)],
            self._flagged("<start> ::= <a>\n<a> ::= '' | 'a'\n", ""),
        )

    def test_empty_parse_from_an_empty_repetition(self):
        self.assertEqual(
            [("", False), ("", True)],
            self._flagged("<start> ::= <a>*\n<a> ::= ''\n", ""),
        )

    def test_empty_parse_that_is_incomplete(self):
        self.assertEqual(
            [("", False)],
            self._flagged("<start> ::= <a>+\n<a> ::= 'a'\n", ""),
        )

    def test_parse_that_can_grow(self):
        self.assertEqual(
            [("00", False), ("00", True)],
            self._flagged("<start> ::= <a>*\n<a> ::= '0'\n", "00"),
        )

    def test_parse_that_cannot_grow(self):
        self.assertEqual([("a", True)], self._flagged("<start> ::= 'a'\n", "a"))

    def test_prefix_of_a_parse(self):
        self.assertEqual([("a", False)], self._flagged("<start> ::= 'ab'\n", "a"))


class TestCLIParsing(unittest.TestCase):
    pass


class TestRegexParsing(TestCLIParsing):
    def test_infinity_abc(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "infinity.fan"),
            "--validate",
            str(RESOURCES_ROOT / "abc.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_infinity_abcabc(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "infinity.fan"),
            "--validate",
            str(RESOURCES_ROOT / "abcabc.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_infinity_abcd(self):
        # This should be rejected by the grammar
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "infinity.fan"),
            str(RESOURCES_ROOT / "abcd.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual(1, code, code)

    REGEX_STAR_SPEC = "<start> ::= '220 ' <rest> '\\r\\n'\n<rest> ::= r'.*'\n"
    WORD = "220 mail.example.com ESMTP\r\n"

    def test_a_later_terminal_wins_against_a_greedy_regex(self):
        grammar, _ = parse(self.REGEX_STAR_SPEC, use_stdlib=False, use_cache=False)
        assert grammar is not None
        parser = Parser(grammar.rules)
        tree = parser.parse(self.WORD)
        self.assertIsNotNone(tree)
        self.assertEqual(self.WORD, str(tree))

    def test_one_block_parses_like_unit_by_unit(self):
        grammar, _ = parse(self.REGEX_STAR_SPEC, use_stdlib=False, use_cache=False)
        assert grammar is not None
        parser = IterativeParser(grammar.rules)
        parser.new_parse()
        parser.consume(self.WORD)
        self.assertEqual([len(self.WORD)], parser.parsed_positions())

        half = len(self.WORD) // 2
        parser.new_parse()
        parser.consume(self.WORD[:half])
        parser.consume(self.WORD[half:])
        self.assertEqual([len(self.WORD)], parser.parsed_positions())


class TestBitParsing(TestCLIParsing):
    def _test(self, example, tree, parsers, start_symbol="<start>"):
        for parser in parsers:
            parsed = False
            for actual_tree in parser.parse_multiple(example, start_symbol):
                if tree is None:
                    self.fail("Expected None")
                self.assertEqual(tree, actual_tree, actual_tree)
                parsed = True
                break
            if tree is None:
                self.assertTrue(True)
                return
            self.assertTrue(parsed)

    def test_bits_a(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "bits.fan"),
            str(RESOURCES_ROOT / "a.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_alternative_bits(self):
        with open(RESOURCES_ROOT / "byte_alternative.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        parser = Parser(grammar.rules)
        iter_parser = IterParsingTester(grammar.rules)
        self._test(b"\x00", None, [parser, iter_parser])
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
            [parser, iter_parser],
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
            [parser, iter_parser],
        )

    def test_single_bit(self):
        with open(RESOURCES_ROOT / "bit_special.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        parser = Parser(grammar.rules)
        iter_parser = IterParsingTester(grammar.rules)
        bit_tree_0 = DerivationTree(
            NonTerminal("<bit>"),
            [DerivationTree(Terminal(0))],
        )
        bit_tree_1 = DerivationTree(
            NonTerminal("<bit>"),
            [DerivationTree(Terminal(1))],
        )
        bit_tree_10 = DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(1))]),
                DerivationTree(NonTerminal("<bit>"), [DerivationTree(Terminal(0))]),
            ],
        )
        self._test(bit_tree_0, bit_tree_0, [parser, iter_parser], "<bit>")
        self._test(bit_tree_1, bit_tree_1, [parser, iter_parser], "<bit>")
        self._test(bit_tree_10, bit_tree_10, [parser, iter_parser], "<start>")


class TestGIFParsing(TestCLIParsing):
    def test_gif(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "gif89a.fan"),
            str(DOCS_ROOT / "tinytrans.gif"),
            "--validate",
            "--no-cache",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)


class TestBitstreamParsing(TestCLIParsing):
    def test_bitstream(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(RESOURCES_ROOT / "bitstream.fan"),
            str(RESOURCES_ROOT / "abcd.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        # Warns that the number of bits (1..5) may not be a multiple of eight, # which is correct
        # self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_bitstream_a(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(RESOURCES_ROOT / "bitstream-a.fan"),
            str(RESOURCES_ROOT / "a.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual("", err, err)
        self.assertEqual("", out, out)
        self.assertEqual(0, code, code)

    def test_bitstream_b(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(RESOURCES_ROOT / "bitstream-a.fan"),
            str(RESOURCES_ROOT / "b.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        # This should fail
        self.assertNotEqual("", err)
        self.assertEqual("", out, out)
        self.assertEqual(1, code, code)

    def test_rgb(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(RESOURCES_ROOT / "rgb.fan"),
            str(RESOURCES_ROOT / "rgb.txt"),
            "--validate",
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code, f"Command failed with code {code}: {err}")
        self.assertEqual("", out, out)
        self.assertEqual("", err, err)


class TestImportParsing(TestCLIParsing):
    def test_local_import(self):
        command = [
            "fandango",
            "fuzz",
            "-f",
            str(RESOURCES_ROOT / "import.fan"),
            "-n",
            "1",
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code, code)
        self.assertEqual("import\n", out, out)


class TestISO8601Parsing(TestCLIParsing):
    def test_parse_iso8601(self):
        command = [
            "fandango",
            "parse",
            "-f",
            str(DOCS_ROOT / "iso8601.fan"),
            str(RESOURCES_ROOT / "iso8601.txt"),
        ]
        out, err, code = run_command(command)
        self.assertEqual(0, code, err)
        self.assertEqual("", err, err)
