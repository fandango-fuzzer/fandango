import random
import typing
import unittest
from typing import Set, Tuple

from fandango.language.grammar import Disambiguator, Node, NonTerminalNode, Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree
from fandango.evolution.algorithm import Fandango


class ConstraintTest(unittest.TestCase):
    GRAMMAR = """
<start> ::= <ab>;
<ab> ::= 
      "a" <ab> 
    | <ab> "b"
    | ""
    ;
"""

    def test_generate_k_paths(self):
        grammar = parse(self.GRAMMAR)[0]

        kpaths = grammar._generate_all_k_paths(3)
        print(len(kpaths))

        for path in grammar._generate_all_k_paths(3):
            print(tuple(path))

    def test_derivation_k_paths(self):
        grammar = parse(self.GRAMMAR)[0]

        random.seed(0)
        tree = grammar.fuzz()
        print([t.symbol for t in tree.flatten()])

    def test_parse(self):
        grammar = parse(self.GRAMMAR)[0]
        tree = grammar.parse("aabb")

        for path in grammar.traverse_derivation(tree):
            print(path)

    def get_solutions(self, grammar):
        grammar, constraints = parse(grammar)
        fandango = Fandango(grammar=grammar, constraints=constraints, desired_solutions=10)
        return fandango.evolve()

    def test_generators(self):
        GRAMMAR = """
<start> ::= <foo>* := test();
<foo> ::= "a" | "b" | "c" | "r";

def test():
    return "bar"
"""
        expected = ["bar" for _ in range(10)]
        actual = self.get_solutions(GRAMMAR)

        self.assertEqual(expected, actual)

    def test_repetitions(self):
        GRAMMAR = """
<start> ::= <a>{3};
<a> ::= "a";
"""
        expected = ["aaa" for _ in range(10)]
        actual = self.get_solutions(GRAMMAR)

        self.assertEqual(expected, actual)

    def test_repetitions_slice(self):
        GRAMMAR = """
<start> ::= <a>{3, 10};
<a> ::= "a";
"""
        solutions = self.get_solutions(GRAMMAR)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 3)
            self.assertLessEqual(len(str(solution)), 10)
    
    def test_repetition_min(self):
        GRAMMAR = """
<start> ::= <a>{3, };
<a> ::= "a";
"""
        solutions = self.get_solutions(GRAMMAR)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 3)


