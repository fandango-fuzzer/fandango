#!/usr/bin/env pytest

import random
import unittest

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree
from .utils import RESOURCES_ROOT


class ConstraintTest(unittest.TestCase):
    def count_g_params(self, tree: DerivationTree):
        count = 0
        if len(tree.sources) > 0:
            count += 1
        assert tree.children is not None
        for child in tree.children:
            count += self.count_g_params(child)
        for child in tree.sources:
            count += self.count_g_params(child)
        return count

    def test_generate_k_paths(self):
        with open(RESOURCES_ROOT / "grammar.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None

        k_paths = grammar._generate_all_k_paths(3)
        print(len(k_paths))

        for path in grammar._generate_all_k_paths(3):
            print(tuple(path))

    def test_derivation_k_paths(self):
        with open(RESOURCES_ROOT / "grammar.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None

        random.seed(0)
        tree = grammar.fuzz()
        print([t.symbol for t in tree.flatten()])

    def test_parse(self):
        with open(RESOURCES_ROOT / "grammar.fan", "r") as file:
            grammar, _ = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        tree = grammar.parse("aabb")

        for path in grammar.traverse_derivation(tree):
            print(path)

    @staticmethod
    def get_solutions(grammar, constraints):
        fandango = Fandango(grammar=grammar, constraints=constraints)
        return [next(fandango.generate())]

    def test_generators(self):
        with open(RESOURCES_ROOT / "bar.fan", "r") as file:
            grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        expected = ["bar" for _ in range(1)]
        actual = self.get_solutions(grammar, constraints)

        self.assertEqual(expected, actual)

    def test_nested_generators(self):
        with open(RESOURCES_ROOT / "nested_grammar_parameters.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None

        for solution in self.get_solutions(grammar, c):
            self.assertEqual(self.count_g_params(solution), 4)
            converted_inner = solution.children[0].sources[0]
            self.assertEqual(self.count_g_params(converted_inner), 3)
            dummy_inner_2 = converted_inner.children[0].sources[0]
            self.assertEqual(self.count_g_params(dummy_inner_2), 2)
            dummy_inner = dummy_inner_2.children[0].sources[0]
            self.assertEqual(self.count_g_params(dummy_inner), 1)
            source_nr = dummy_inner.children[0].children[1].sources[0]
            self.assertEqual(self.count_g_params(source_nr), 0)

    def test_repetitions(self):
        with open(RESOURCES_ROOT / "repetitions.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None

        expected = ["aaa" for _ in range(1)]
        actual = self.get_solutions(grammar, c)

        self.assertEqual(expected, actual)

    def test_repetitions_slice(self):
        with open(RESOURCES_ROOT / "slicing.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        solutions = self.get_solutions(grammar, c)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 3)
            self.assertLessEqual(len(str(solution)), 10)

    def test_repetition_min(self):
        with open(RESOURCES_ROOT / "min_reps.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        solutions = self.get_solutions(grammar, c)
        for solution in solutions:
            self.assertGreaterEqual(len(str(solution)), 1)

    def test_repetition_computed(self):
        with open(RESOURCES_ROOT / "dynamic_repetition.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        solutions = self.get_solutions(grammar, c)
        for solution in solutions:
            len_outer = solution.children[0].to_int()
            self.assertEqual(len_outer, len(solution.children) - 3)
            for tree in solution.children[2:-1]:
                len_inner = tree.children[0].to_int()
                self.assertEqual(len_inner, len(tree.children) - 1)

    def test_generator_redefinition(self):
        with open(RESOURCES_ROOT / "generator_remove.fan", "r") as file:
            grammar, c = parse(file, use_stdlib=True, use_cache=False)
            assert grammar is not None
        solutions = self.get_solutions(grammar, c)
        for solution in solutions:
            self.assertNotEqual(solution, "10")

    def test_max_nodes(self):
        with open(RESOURCES_ROOT / "gen_number.fan", "r") as file:
            grammar, c = parse(file, use_cache=False, use_stdlib=True)
        solution = self.get_solutions(grammar, c)
        for sol in solution:
            s = str(sol).split(".")
            self.assertEqual(s[0], "a" * 50)
            self.assertTrue(len(s[1]) >= 10)
