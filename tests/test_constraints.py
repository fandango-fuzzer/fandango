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
        cls.grammar, _ = parse(cls.GRAMMAR)

    def get_constraint(self, constraint):
        _, constraints = parse(constraint)
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

    def test_comparison_constraint(self):
        constraint = self.get_constraint("|<ab>| > 2;")
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
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertFalse(constraint.check(counter_example))

    def test_conjunction_constraint(self):
        constraint = self.get_constraint("'a' not in str(<ab>) and |<ab>| > 2;")
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
        counter_example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertFalse(constraint.check(counter_example))

    def test_disjunction_constraint(self):
        constraint = self.get_constraint("'a' not in str(<ab>) or |<ab>| > 2;")
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
        example = DerivationTree(
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
        self.assertTrue(constraint.check(example))
        example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertTrue(constraint.check(example))
        counter_example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(Terminal("a")),
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
            ],
        )
        self.assertFalse(constraint.check(counter_example))

    def test_implication_constraint(self):
        constraint = self.get_constraint("|<ab>| > 2 -> 'a' not in str(<ab>);")
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
        example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
                DerivationTree(Terminal("b")),
            ],
        )
        self.assertTrue(constraint.check(example))
        example = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(Terminal("a")),
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
            ],
        )
        self.assertTrue(constraint.check(example))

    def test_forall_constrain(self):
        constraint = self.get_constraint("forall <x> in <ab>: 'a' not in str(<x>);")
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

    def test_exists_constrain(self):
        constraint = self.get_constraint("exists <x> in <ab>: 'a' == str(<x>);")
        counter_example = DerivationTree(
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
        self.assertFalse(constraint.check(counter_example))
        example = DerivationTree(
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
        self.assertTrue(constraint.check(example))
