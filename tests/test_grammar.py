import random
import typing
import unittest
from typing import Set, Tuple

from fandango.language.grammar import Disambiguator, Node, NonTerminalNode, Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


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

