import random
import typing
import unittest
from typing import Set, Tuple

from fandango.language.grammar import Disambiguator, Node, NonTerminalNode, Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


class ConstraintTest(unittest.TestCase):

    def test_generate_k_paths(self):

        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False)

        kpaths = GRAMMAR._generate_all_k_paths(3)
        print(len(kpaths))

        for path in GRAMMAR._generate_all_k_paths(3):
            print(tuple(path))

    def test_derivation_k_paths(self):
        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False)

        random.seed(0)
        tree = GRAMMAR.fuzz()
        print([t.symbol for t in tree.flatten()])

    def test_parse(self):
        file = open("tests/resources/grammar.fan", "r")
        GRAMMAR, _ = parse(file, use_stdlib=False)
        tree = GRAMMAR.parse("aabb")

        for path in GRAMMAR.traverse_derivation(tree):
            print(path)

