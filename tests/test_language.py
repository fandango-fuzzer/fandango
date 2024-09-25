import ast
import time
import unittest

from parameterized import parameterized
from antlr4 import InputStream, CommonTokenStream
from fuzzingbook.GrammarFuzzer import (
    GrammarFuzzer,
    EvenFasterGrammarFuzzer,
    FasterGrammarFuzzer,
)

from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    SearchProcessor,
)
from fandango.language.grammar import Alternative, Grammar
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser


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
        return getattr(parser, start)()

    def test_indents(self):
        tree = self.get_tree(
            """
<a> ::= 
    "a"
    | "a" <a>
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
        tree = ast.parse(expression, mode="eval")
        fandango_tree: FandangoParser.ExpressionContext = self.get_tree(
            expression, start="expression", ignore_eof=True
        )
        processor = SearchProcessor(Grammar({}))
        fandango_tree, searches, search_map = processor.visit(fandango_tree)
        self.assertEqual(0, len(searches))
        self.assertEqual(0, len(search_map))
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
            "x <> y",
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
