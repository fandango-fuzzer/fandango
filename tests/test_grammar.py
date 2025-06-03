#!/usr/bin/env pytest

import random
import unittest

from scipy.linalg import solve_lyapunov

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


class ConstraintTest(unittest.TestCase):

    def count_g_params(self, tree: DerivationTree):
        count = 0
        if len(tree.sources) > 0:
            count += 1
        for child in tree.children:
            count += self.count_g_params(child)
        for child in tree.sources:
            count += self.count_g_params(child)
        return count

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
        fandango = Fandango(
            grammar=grammar, constraints=constraints, desired_solutions=1
        )
        return fandango.evolve()

    def test_generators(self):
        file = open("tests/resources/bar.fan", "r")
        GRAMMAR, constraints = parse(file, use_stdlib=False, use_cache=False)
        expected = ["bar" for _ in range(1)]
        actual = self.get_solutions(GRAMMAR, constraints)

        self.assertEqual(expected, actual)

    def test_nested_generators(self):
        file = open("tests/resources/nested_grammar_parameters.fan", "r")
        grammar, c = parse(file, use_stdlib=False, use_cache=False)

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
        file = open("tests/resources/repetitions.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=False, use_cache=False)
        expected = ["aaa" for _ in range(1)]
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
            self.assertGreaterEqual(len(str(solution)), 1)

    def test_repetition_computed(self):
        file = open("tests/resources/dynamic_repetition.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=False, use_cache=False)
        solutions = self.get_solutions(GRAMMAR, c)
        for solution in solutions:
            len_outer = solution.children[0].to_int()
            self.assertEqual(len_outer, len(solution.children) - 3)
            for tree in solution.children[2:-1]:
                len_inner = tree.children[0].to_int()
                self.assertEqual(len_inner, len(tree.children) - 1)

    def test_generator_redefinition(self):
        file = open("tests/resources/generator_remove.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=True, use_cache=False)
        solutions = self.get_solutions(GRAMMAR, c)
        for solution in solutions:
            self.assertNotEqual(solution, "10")

    def test_num_solutions(self):
        file = open("docs/digits.fan", "r")
        GRAMMAR, c = parse(file, use_stdlib=True, use_cache=False)
        fan = Fandango(grammar=GRAMMAR, constraints=c, desired_solutions=1000)
        sol = fan.evolve()
        self.assertEqual(len(sol), 1000)

    def test_max_nodes(self):
        file = open("tests/resources/gen_number.fan", "r")
        GRAMMAR, c = parse(file, use_cache=False, use_stdlib=True)
        solution = self.get_solutions(GRAMMAR, c)
        for sol in solution:
            s = str(sol).split(".")
            self.assertEqual(s[0], "a" * 50)
            self.assertTrue(len(s[1]) >= 10)
