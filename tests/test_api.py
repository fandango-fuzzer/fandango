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
            print(f"tree = {repr(str(tree))}")
            print(tree.to_grammar())

    def test_incomplete_parse(self):
        fan = Fandango(self.SPEC_abcd)
        word = "ab"

        for tree in fan.parse(word, prefix=True):
            print(f"tree = {repr(str(tree))}")
            print(tree.to_grammar())

    def test_failing_incomplete_parse(self):
        fan = Fandango(self.SPEC_abcd)
        invalid_word = "ab"

        try:
            fan.parse(invalid_word)
            self.assertTrue(False, "Expected FandangoParseError")
        except FandangoParseError as exc:
            print(f"Syntax error at {exc.position} in word {invalid_word!r}")

    def test_failing_parse(self):
        fan = Fandango(self.SPEC_abcd)
        invalid_word = "abcdef"

        try:
            fan.parse(invalid_word)
            self.assertTrue(False, "Expected FandangoParseError")
        except FandangoParseError as exc:
            print(f"Syntax error at {exc.position} in word {invalid_word!r}")

    def ensure_capped_generation(self):
        fan = Fandango(self.SPEC_abcd, logging_level=logging.INFO)
        solutions = fan.fuzz()
        self.assertLess(
            100,
            len(solutions),
            f"Expected more than 100 trees, only received {len(solutions)}",
        )


if __name__ == "__main__":
    unittest.main()
