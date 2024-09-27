import unittest

from fandango.language.grammar import DerivationTree, Terminal, NonTerminal
from fandango.language.parse import parse


class ConstraintTest(unittest.TestCase):
    GRAMMAR = """
<ab> ::= 
      "a" <ab> 
    | <ab> "b"
    | ""
    ;
"""

    @classmethod
    def setUpClass(cls):
        cls.grammar, _, cls.locals = parse(cls.GRAMMAR)

    def get_constraint(self, constraint):
        _, constraints, _ = parse(constraint)
        self.assertEqual(1, len(constraints))
        return constraints[0]

    def test_expression_constraint(self):
        constraint = self.get_constraint("'a' not in str(<ab>);")
        example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(
                            NonTerminal("<ab>"), [DerivationTree(Terminal(""))]
                        ),
                        DerivationTree(Terminal("b")),
                    ],
                ),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertTrue(constraint.check(example))
        counter_example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(Terminal("a")),
                        DerivationTree(
                            NonTerminal("<ab>"), [DerivationTree(Terminal(""))]
                        ),
                    ],
                ),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertFalse(constraint.check(counter_example))
