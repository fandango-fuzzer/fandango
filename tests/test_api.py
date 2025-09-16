#!/usr/bin/env pytest

import itertools
import random
import unittest
import logging

import pytest

from fandango import Fandango
from .utils import DOCS_ROOT, RESOURCES_ROOT


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

        assert len(list(fan.parse(invalid_word))) == 0

    def test_failing_parse(self):
        fan = Fandango(self.SPEC_abcd)
        invalid_word = "abcdef"

        assert len(list(fan.parse(invalid_word))) == 0

    def ensure_capped_generation(self):
        fan = Fandango(self.SPEC_abcd, logging_level=logging.INFO)
        solutions = fan.fuzz()
        self.assertLess(
            100,
            len(solutions),
            f"Expected more than 100 trees, only received {len(solutions)}",
        )


@pytest.mark.parametrize("even_number", ["0", "1", "10", "11", "12", "123", "1234"])
def test_even_number(even_number):
    with open(RESOURCES_ROOT / "even_numbers.fan", "r") as file:
        fan = Fandango(file)

    parses = list(fan.parse(even_number))

    is_even = int(even_number) % 2 == 0
    successful_parse = len(parses) > 0

    assert (
        successful_parse == is_even
    ), f"parsed for {even_number} the following: {parses}"

    assert all(
        all(c.check(p) for c in fan.constraints) for p in parses
    ), f"some parses did not match the constraints for {even_number}"


if __name__ == "__main__":
    unittest.main()
