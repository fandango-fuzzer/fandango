#!/usr/bin/env pytest

import itertools
import random
import unittest
import logging

from fandango import Fandango, FandangoParseError
from .utils import DOCS_ROOT


class APITest(unittest.TestCase):
    SPEC_abc = r"""
    <start> ::= ('a' | 'b' | 'c')+
    where str(<start>) != 'd'
    """

    SPEC_abcd = r"""
    <start> ::= ('a' | 'b' | 'c')+ 'd'
    where str(<start>) != 'd'
    """

    def test_fuzz(self):
        with open(DOCS_ROOT / "persons-faker.fan") as persons:
            fan = Fandango(persons)

        random.seed(0)
        for tree in itertools.islice(fan.generate_solutions(), 10):
            print(str(tree))

    def test_fuzz_from_string(self):
        fan = Fandango(self.SPEC_abc, logging_level=logging.INFO)
        random.seed(0)
        for tree in itertools.islice(fan.generate_solutions(), 10):
            print(str(tree))

    def test_parse(self):
        fan = Fandango(self.SPEC_abc)
        word = "abc"

        for tree in fan.parse(word):
            assert tree is not None
            print(f"tree = {repr(str(tree))}")
            print(tree.to_grammar())

    def test_incomplete_parse(self):
        fan = Fandango(self.SPEC_abcd)
        word = "ab"

        for tree in fan.parse(word, prefix=True):
            assert tree is not None
            print(f"tree = {repr(str(tree))}")
            print(tree.to_grammar())

    def test_failing_incomplete_parse(self):
        fan = Fandango(self.SPEC_abcd)
        invalid_word = "ab"

        with self.assertRaises(FandangoParseError):
            list(fan.parse(invalid_word))  # force generator evaluation

    def test_failing_parse(self):
        fan = Fandango(self.SPEC_abcd)
        invalid_word = "abcdef"

        with self.assertRaises(FandangoParseError):
            list(fan.parse(invalid_word))  # force generator evaluation


class FlippedConstraintTest(unittest.TestCase):
    SPEC_ab = """
    <start> ::= 'a' | 'b'
    where str(<start>) != 'b'
    """

    def test_no_flips(self):
        fan = Fandango(self.SPEC_ab)
        # assume any solution was found in 10 generations for such a simple spec
        solutions = fan.fuzz(inverted_constraint_depth=0, max_generations=10)
        self.assertEqual(len(solutions), 1)
        self.assertEqual(str(solutions[0]), "a")

    def test_one_flip(self):
        fan = Fandango(self.SPEC_ab)
        # assume any solution was found in 10 generations for such a simple spec
        solutions = fan.fuzz(inverted_constraint_depth=1, max_generations=10)
        solutions_str = [str(s) for s in solutions]
        self.assertEqual(len(solutions), 2)
        self.assertIn("a", solutions_str)
        self.assertIn("b", solutions_str)

    def test_multiple_flips(self):
        spec = """
<start> ::= <a> <b> <c>
<a> ::= 'a'
<b> ::= 'b'?
<c> ::= 'c'?

where <b> != 'b'
where <c> != 'c'
"""
        fan = Fandango(spec)
        # assume any solution was found in 10 generations for such a simple spec
        solutions = fan.fuzz(inverted_constraint_depth=3, max_generations=10)
        solutions_str = [str(s) for s in solutions]
        self.assertEqual(len(solutions), 4)
        expected_solutions = (
            "a",  # no flips
            "ab",  # flip first constraint
            "ac",  # flip second constraint
            "abc",  # flip both constraints
        )
        for s in expected_solutions:
            self.assertIn(s, solutions_str)


if __name__ == "__main__":
    unittest.main()
