import unittest


from fandango.language.grammar import DerivationTree, Terminal, NonTerminal
from fandango.language.parse import parse


class ConstraintTest(unittest.TestCase):
    GRAMMAR = """
<start> ::= <ab>;
<ab> ::= 
      "a" <ab> 
    | <ab> "b"
    | ""
    ;
"""

    def test_k_paths(self):
        grammar = parse(self.GRAMMAR)[0]

        for i in range(5):
            print(grammar.k_paths(i+1))