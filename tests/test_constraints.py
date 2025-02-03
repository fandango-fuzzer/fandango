import unittest


from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.parse import parse


class ConstraintTest(unittest.TestCase):


    def get_constraint(self, constraint):
        file = open("tests/resources/constraints.fan", "r")
        _, constraints = parse(file, constraints=[constraint], use_stdlib=False, use_cache=False)
        self.assertEqual(1, len(constraints))
        return constraints[0]

    def test_explicit_fitness(self):
        constraint = self.get_constraint("len(str(<start>));")
        example = DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(
                            NonTerminal("<ab>"),
                            [
                                DerivationTree(
                                    NonTerminal("<ab>"),
                                    [DerivationTree(Terminal(""))],
                                ),
                                DerivationTree(Terminal("b")),
                            ],
                        ),
                        DerivationTree(Terminal("b")),
                    ],
                )
            ],
        )
        self.assertEqual(1, constraint.fitness(example).fitness())
        example = DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(
                            NonTerminal("<ab>"), [DerivationTree(Terminal(""))]
                        ),
                        DerivationTree(Terminal("b")),
                    ],
                )
            ],
        )
        self.assertEqual(1, constraint.fitness(example).fitness())

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

    def test_forall_constraint(self):
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

    def test_hash(self):
        tree_1 = DerivationTree(
            NonTerminal("<ab>"),
            [
                DerivationTree(Terminal("a")),
                DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))]),
            ],
        )
        tree_2 = DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal(""))])
        self.assertNotEqual(tree_1, tree_2)

    def test_exists_constraint(self):
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

    def test_direct_children(self):
        constraint = self.get_constraint("str(<start>.<ab>) == 'a';")
        counter_example = DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(
                            Terminal("b"),
                            []
                        )
                    ]
                )
            ]
        )

        self.assertFalse(constraint.check(counter_example))
        example = DerivationTree(
            NonTerminal("<start>"),
            [
                DerivationTree(
                    NonTerminal("<ab>"),
                    [
                        DerivationTree(
                            Terminal("a"),
                            []
                        )
                    ]
                )
            ]
        )
        self.assertTrue(constraint.check(example))

    def test_indirect_children(self):
        file = open("tests/resources/indirect_children.fan", "r")
        grammar, constraint = parse(file, use_stdlib=False, use_cache=False)
        
        self.assertEqual(1, len(constraint))
        constraint = constraint[0]
        
        counter_example = grammar.parse("19")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("11")
        self.assertTrue(constraint.check(example))

    def test_accessing_children(self):
        file = open("tests/resources/children.fan", "r")
        grammar, constraint = parse(file, use_stdlib=False, use_cache=False)
        constraint = constraint[0]

        counter_example = grammar.parse("11")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("01")
        self.assertTrue(constraint.check(example))

    def test_complex_constraint(self):
        constraint = """
int(<number>) % 2 == 0;
int(<number>) > 10000;
int(<number>) < 100000;
"""

        file = open("tests/resources/complex_constraints.fan", "r")
        _, constraints = parse(file, constraints=[constraint], use_stdlib=False, use_cache=False)
        self.assertEqual(3, len(constraints))

        def get_tree(x):
            return DerivationTree(
                NonTerminal("<number>"), [DerivationTree(Terminal(str(x)))]
            )

        examples = [
            (get_tree(20002), True, True, True),
            (get_tree(20001), False, True, True),
            (get_tree(2), True, False, True),
            (get_tree(1), False, False, True),
            (get_tree(200002), True, True, False),
            (get_tree(200001), False, True, False),
        ]

        for tree, sat_even, sat_greater, sat_less in examples:
            for sat, constraint in zip((sat_even, sat_greater, sat_less), constraints):
                fitness = constraint.fitness(tree)
                self.assertEqual(sat, fitness.success)
                self.assertEqual(1 if sat else 0, fitness.solved)
                if not sat:
                    self.assertEqual(1, len(fitness.failing_trees))
                    self.assertEqual(tree, fitness.failing_trees[0].tree)
