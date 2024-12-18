import unittest

from fandango.language.grammar import ParseState
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree


class ParserTests(unittest.TestCase):
    FANDANGO_GRAMMAR = """
        <start> ::= <number>;
        <number> ::= <non_zero><digit>* | "0";
        <non_zero> ::= 
                      "1" 
                    | "2" 
                    | "3"
                    | "4" 
                    | "5" 
                    | "6" 
                    | "7" 
                    | "8" 
                    | "9"
                    ;
        <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
    """

    @classmethod
    def setUpClass(cls):
        cls.grammar, _ = parse(cls.FANDANGO_GRAMMAR)

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

    def test_parse_table(self):
        table = self.grammar._parser.parse_table("1")
        self.assertIn(
            ParseState(NonTerminal("<*start*>"), 0, (NonTerminal("<start>"),), dot=1),
            table[1],
        )


class TestComplexParsing(unittest.TestCase):
    GRAMMAR = """
    <start> ::= <ab>;
    <ab> ::= 
          "a" <ab> 
        | <ab> "b"
        | ""
        ;
    """

    @classmethod
    def setUpClass(cls):
        cls.grammar, _ = parse(cls.GRAMMAR)

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
    GRAMMAR = """
    <start> ::= <ab>;
    <ab> ::= 
          "a" (<ab> | "b") 
        | <ab> "b"
        | "c"
        ;
    """

    @classmethod
    def setUpClass(cls):
        cls.grammar, _ = parse(cls.GRAMMAR)

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
