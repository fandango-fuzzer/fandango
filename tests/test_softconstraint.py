#!/usr/bin/env pytest

import unittest
import unittest
from typing import List

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree

class TestSoft(unittest.TestCase):
    def get_solutions(
        self,
        specification_file,
        desired_solutions,
        random_seed,
    ):
        file = open(specification_file, "r")
        grammar_int, constraints_int = parse(file, use_stdlib=False, use_cache=False)
        fandango = Fandango(
            grammar=grammar_int,
            constraints=constraints_int,
            desired_solutions=desired_solutions,
            random_seed=random_seed,
        )
        solutions: List[DerivationTree] = fandango.evolve()
        return [s.to_string() for s in solutions]


class TestSoftValue(TestSoft):
    def test_soft_value(self):
        solutions = self.get_solutions(
            "tests/resources/softvalue.fan", desired_solutions=100, random_seed=1
        )
        self.assertEqual(solutions[-1], "999999-999999")

class TestSoftConstraint(TestSoft):
    def test_soft_constraint(self):
        solutions = self.get_solutions(
            "tests/resources/softconstraint.fan",
            desired_solutions=10,
            random_seed=1,
        )
        sol: str
        best_matches = 0
        for sol in solutions:
            assert len(sol) == 5
            matches = 0
            s = set(int(digit) for digit in sol)
            for digit in sol:
                if int(digit)+1 in s:
                    matches += 1
            best_matches = max(best_matches, matches)
        self.assertEqual(best_matches, 4) 