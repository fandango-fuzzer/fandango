import time
import unittest

from antlr4 import InputStream, CommonTokenStream
from fuzzingbook.GrammarFuzzer import GrammarFuzzer, EvenFasterGrammarFuzzer, FasterGrammarFuzzer

from fandango.language.convert import FandangoSplitter, GrammarProcessor
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

    def test_fuzzing(self):
        lexer = FandangoLexer(InputStream(self.FANDANGO_GRAMMAR))
        token = CommonTokenStream(lexer)
        parser = FandangoParser(token)
        tree = parser.fandango()

        splitter = FandangoSplitter()
        splitter.visit(tree)

        processor = GrammarProcessor()
        grammar = processor.get_grammar(splitter.productions)

        fuzzer = GrammarFuzzer(self.FUZZINGBOOK_GRAMMAR)

        for _ in range(10000):
            # check if none
            inp_ = fuzzer.fuzz_tree()
            if inp_ is None:
                self.fail("None found")

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
        for _ in range(10000):
            grammar.fuzz()
        print(f"\n{time.time() - start} seconds (ours)")

        fuzzer = GrammarFuzzer(self.FUZZINGBOOK_GRAMMAR)

        fuzzingbook_time = time.time()
        for _ in range(10000):
            fuzzer.fuzz_tree()
        print(f"{time.time() - fuzzingbook_time} seconds (oks)")

        fuzzer = FasterGrammarFuzzer(self.FUZZINGBOOK_GRAMMAR)

        fuzzingbook_time = time.time()
        for _ in range(10000):
            fuzzer.fuzz_tree()
        print(f"{time.time() - fuzzingbook_time} seconds (faster)")

        fuzzer = EvenFasterGrammarFuzzer(self.FUZZINGBOOK_GRAMMAR)

        fuzzingbook_time = time.time()
        for _ in range(10000):
            fuzzer.fuzz_tree()
        print(f"{time.time() - fuzzingbook_time} seconds (even faster)")


if __name__ == "__main__":
    TestLanguage().test_fuzzing()
