import random
import typing
import unittest
from typing import Set, Tuple

from fandango.language.grammar import Disambiguator, Node, NonTerminalNode, Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree
from fandango.evolution.algorithm import Fandango


class ConstraintTest(unittest.TestCase):

    def test_generate_k_paths(self):

        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False, use_cache=False)

        kpaths = GRAMMAR._generate_all_k_paths(3)
        print(len(kpaths))

        for path in GRAMMAR._generate_all_k_paths(3):
            print(tuple(path))

    def test_derivation_k_paths(self):
        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False, use_cache=False)

        random.seed(0)
        tree = GRAMMAR.fuzz()
        print([t.symbol for t in tree.flatten()])

    def test_parse(self):
        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False, use_cache=False)
        tree = GRAMMAR.parse("aabb")

        for path in GRAMMAR.traverse_derivation(tree):
            print(path)

    def get_solutions(self, grammar, constraints):
        fandango = Fandango(grammar=grammar, constraints=constraints, desired_solutions=10)
        return fandango.evolve()

    def test_generators(self):
        file = open("tests/resources/bar.fan", "r")
        GRAMMAR, constraints = parse(file, use_stdlib=False, use_cache=False)
        expected = ["bar" for _ in range(10)]
        actual = self.get_solutions(GRAMMAR, constraints)

        self.assertEqual(expected, actual)

    def test_repetitions(self):
        file = open("tests/resources/repetitions.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=False, use_cache=False)
        expected = ["aaa" for _ in range(10)]
        actual = self.get_solutions(GRAMMAR, c)

        self.assertEqual(expected, actual)

    def test_repetitions_slice(self):
        file = open("tests/resources/slicing.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=False, use_cache=False)
        solutions = self.get_solutions(GRAMMAR, c)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 3)
            self.assertLessEqual(len(str(solution)), 10)
    
    def test_repetition_min(self):
        file = open("tests/resources/min_reps.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=False, use_cache=False)
        solutions = self.get_solutions(GRAMMAR, c)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 3)


