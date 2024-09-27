import ast
import os
import time
import unittest

from antlr4.error.Errors import ParseCancellationException
from parameterized import parameterized
from antlr4 import InputStream, CommonTokenStream, BailErrorStrategy
from fuzzingbook.GrammarFuzzer import (
    GrammarFuzzer,
    EvenFasterGrammarFuzzer,
    FasterGrammarFuzzer,
)

from fandango.constraints.base import ComparisonConstraint, Comparison
from fandango.language.parse import parse
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    SearchProcessor,
    PythonProcessor,
)
from fandango.language.grammar import Alternative, Grammar, NonTerminal
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.search import RuleSearch


class TestLanguage(unittest.TestCase):
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
    FUZZINGBOOK_GRAMMAR = {
        "<start>": ["<number>"],
        "<number>": ["<non_zero><digits>", "0"],
        "<digits>": ["", "<digit><digits>"],
        "<non_zero>": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    }

    @staticmethod
    def get_tree(example, start="fandango", ignore_eof=False):
        lexer = FandangoLexer(InputStream(example))
        token = CommonTokenStream(lexer)
        # if ignore_eof:
        #    if token.tokens[-1] == FandangoParser.EOF:
        #        token.tokens = token.tokens[:-1]
        parser = FandangoParser(token)
        parser._errHandler = BailErrorStrategy()
        return getattr(parser, start)()

    def test_indents(self):
        tree = self.get_tree(
            """
<a> ::= 
    "a"
    | "a" <a>;
            """
        )
        splitter = FandangoSplitter()
        splitter.visit(tree)
        processor = GrammarProcessor()
        grammar = processor.get_grammar(splitter.productions)
        self.assertEqual(1, len(grammar.rules))
        rule = list(grammar.rules.values())[0]
        self.assertIsInstance(rule, Alternative)
        self.assertEqual(2, len(rule.alternatives))

    def test_speed(self):
        lexer = FandangoLexer(InputStream(self.FANDANGO_GRAMMAR))
        token = CommonTokenStream(lexer)
        parser = FandangoParser(token)
        tree = parser.fandango()

        splitter = FandangoSplitter()
        splitter.visit(tree)

        processor = GrammarProcessor()
        grammar = processor.get_grammar(splitter.productions)

        start = time.time()
        for _ in range(100):
            grammar.fuzz()
        fandango_fuzzer_time = time.time() - start

        for fuzzer_class in (
            GrammarFuzzer,
            FasterGrammarFuzzer,
            EvenFasterGrammarFuzzer,
        ):
            fuzzer = fuzzer_class(self.FUZZINGBOOK_GRAMMAR)
            start = time.time()
            for _ in range(100):
                fuzzer.fuzz_tree()
            fuzzer_time = time.time() - start
            self.assertLess(fandango_fuzzer_time, fuzzer_time)

    def _test_conversion_without_replace(self, expression):
        try:
            tree = ast.parse(expression, mode="eval")
        except SyntaxError:
            self.assertRaises(
                ParseCancellationException,
                self.get_tree,
                expression,
                start="expression",
                ignore_eof=True,
            )
        else:
            fandango_tree: FandangoParser.ExpressionContext = self.get_tree(
                expression, start="expression", ignore_eof=True
            )
            processor = SearchProcessor(Grammar({}))
            fandango_tree, searches, search_map = processor.visit(fandango_tree)
            self.assertEqual(0, len(searches))
            self.assertEqual(0, len(search_map))
            self.assertNotIsInstance(fandango_tree, list)
            self.assertEqual(ast.unparse(tree), ast.unparse(fandango_tree))

    @parameterized.expand(
        [
            "x",
            "1",
            "x and y",
            "x or y",
            "x + y",
            "x - y",
            "x * y",
            "x / y",
            "x // y",
            "x ** y",
            "x @ y",
            "x << y",
            "x >> y",
            "x | y",
            "x ^ y",
            "~ x",
            "not x",
            "+ x",
            "- x",
            "x if y else z",
            "{x: y, v: w}",
            "{x, y, z}",
            "[x, y, z]",
            "(x, y, z)",
            "{x: y for x in z if x}",
            "{x for x in z if x}",
            "[x for x in z if x]",
            "(x for x in z if x)",
            "await x",
            "yield x",
            "yield from x",
            "x < y",
            "x <= y",
            "x > y",
            "x >= y",
            "x == y",
            # "x <> y",
            "x != y",
            "x is y",
            "x is not y",
            "x in y",
            "x not in y",
            "x()",
            "x(y, z, *a, v=w, **k)",
            "x.y.z",
            "x[y,a:b:c,::]",
            "*x",
        ],
    )
    def test_conversion_without_replace(self, expression):
        self._test_conversion_without_replace(expression)

    @parameterized.expand(
        [
            ("<x>", True, True),
            ("<x> and True", True, True),
            ("<x> or False", True, True),
            ("<x> + 3", 2, 5),
            ("<x> - 3", 2, -1),
            ("<x> * 3", 2, 6),
            ("<x> / 2", 2, 1),
            ("<x> // 2", 3, 1),
            ("<x> ** 3", 2, 8),
            ("<x> << 2", 2, 8),
            ("<x> >> 2", 8, 2),
            ("<x> | 2", 1, 3),
            ("<x> ^ 5", 4, 1),
            ("~ <x>", 1, -2),
            ("not <x>", True, False),
            ("+ <x>", 2, 2),
            ("- <x>", 2, -2),
            ("2 if <x> else 1", True, 2),
            ("{1: <x>, 3: 4}", 2, {1: 2, 3: 4}),
            ("{1, <x>, 3}", 2, {1, 2, 3}),
            ("[1, <x>, 3]", 2, [1, 2, 3]),
            ("(1, <x>, 3)", 2, (1, 2, 3)),
            ("{x: x for x in <x> if x % 2 == 1}", [1, 2, 3], {1: 1, 3: 3}),
            ("{x for x in <x> if x % 2 == 1}", [1, 2, 3], {1, 3}),
            ("[x for x in <x> if x % 2 == 1]", [1, 2, 3], [1, 3]),
            ("tuple(x for x in <x> if x % 2 == 1)", [1, 2, 3], (1, 3)),
            ("<x> < 3", 2, True),
            ("<x> <= 3", 2, True),
            ("<x> > 3", 2, False),
            ("<x> >= 3", 2, False),
            ("<x> == 3", 2, False),
            ("<x> != 3", 2, True),
            ("<x> is 3", 2, False),
            ("<x> is not 3", 2, True),
            ("<x> in [1, 2, 3]", 2, True),
            ("<x> not in [1, 2, 3]", 2, False),
            ("int(<x>)", "2", 2),
            ("<x>.lower()", "AbC", "abc"),
            # ("<x>[0, 2::2]", [1, 2, 3, 4], [1, 2, 4]),
        ]
    )
    def test_conversion_with_replacement(self, expression, value, expected):
        fandango_tree: FandangoParser.ExpressionContext = self.get_tree(
            expression, start="expression", ignore_eof=True
        )
        processor = SearchProcessor(Grammar({}))
        fandango_tree, searches, search_map = processor.visit(fandango_tree)
        self.assertEqual(1, len(search_map))
        self.assertEqual(1, len(searches))
        placeholder = list(search_map.keys())[0]
        self.assertEqual(
            expected, eval(ast.unparse(fandango_tree), {placeholder: value})
        )

    @parameterized.expand(
        [
            ("x = 1", 1),
            ("x: int = 1", 1),
            ("x = 0\nx += 1", 1),
            ("import os\nx = os.path.join('a', 'b')", os.path.join("a", "b")),
            ("try:\n   raise ValueError()\nexcept:\n    x = 1\nelse:\n    x = 1", 1),
            ("a = [0, 1]\ndel a[0]\nx = a[0]", 1),
        ]
    )
    def test_conversion_statement(self, stmt, value):
        fandango_tree: FandangoParser.ExpressionContext = self.get_tree(stmt)
        splitter = FandangoSplitter()
        splitter.visit(fandango_tree)
        code = splitter.python_code
        processor = PythonProcessor()
        fandango_tree = processor.get_code(code)
        tree = ast.parse(stmt)
        self.assertEqual(ast.unparse(tree), ast.unparse(fandango_tree))
        local_vars = {}
        exec(ast.unparse(fandango_tree), {}, local_vars)
        self.assertEqual(value, local_vars["x"])

    def test_parsing(self):
        fan = (
            self.FANDANGO_GRAMMAR
            + """

def f(x):
    return int(x)            

f(<number>) % 2 == 0;        
"""
        )
        grammar, constraints, _ = parse(fan)
        self.assertIsInstance(grammar, Grammar)
        self.assertEqual(4, len(grammar.rules))
        self.assertIn("<start>", grammar)
        self.assertIn("<number>", grammar)
        self.assertIn("<non_zero>", grammar)
        self.assertIn("<digit>", grammar)
        self.assertEqual(1, len(constraints))
        constraint = constraints[0]
        self.assertIsInstance(constraint, ComparisonConstraint)
        self.assertEqual("0", constraint.right)
        self.assertEqual(Comparison.EQUAL, constraint.operator)
        self.assertEqual(1, len(constraint.searches))
        placeholder = list(constraint.searches.keys())[0]
        self.assertEqual(f"f({placeholder}) % 2", constraint.left)
        self.assertIsInstance(constraint.searches[placeholder], RuleSearch)
        search: RuleSearch = constraint.searches[placeholder]
        self.assertEqual(search.symbol, NonTerminal("<number>"))
