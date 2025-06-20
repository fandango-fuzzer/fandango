#!/usr/bin/env pytest

import unittest


from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.parse import parse
from .utils import RESOURCES_ROOT


class ConstraintTest(unittest.TestCase):
    def get_constraint(self, constraint):
        with open(RESOURCES_ROOT / "constraints.fan", "r") as file:
            _, constraints = parse(
                file, constraints=[constraint], use_stdlib=False, use_cache=False
            )
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
            [DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal("b"), [])])],
        )

        self.assertFalse(constraint.check(counter_example))
        example = DerivationTree(
            NonTerminal("<start>"),
            [DerivationTree(NonTerminal("<ab>"), [DerivationTree(Terminal("a"), [])])],
        )
        self.assertTrue(constraint.check(example))

    def test_indirect_children(self):
        with open(RESOURCES_ROOT / "indirect_children.fan", "r") as file:
            grammar, constraint = parse(file, use_stdlib=False, use_cache=False)

        self.assertEqual(1, len(constraint))
        constraint = constraint[0]

        counter_example = grammar.parse("19")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("11")
        self.assertTrue(constraint.check(example))

    def test_accessing_children(self):
        with open(RESOURCES_ROOT / "children.fan", "r") as file:
            grammar, constraint = parse(file, use_stdlib=False, use_cache=False)
        constraint = constraint[0]

        counter_example = grammar.parse("11")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("01")
        self.assertTrue(constraint.check(example))

    def test_eval_constraint(self):
        with open(RESOURCES_ROOT / "eval.fan") as file:
            grammar, constraints = parse(file, use_stdlib=True, use_cache=False)
        constraint = constraints[0]

        counter_example = grammar.parse("+05 * 0 / 96 + 10")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("+5 * 0 / 96 + 10")
        self.assertTrue(constraint.check(example))

    def test_complex_constraint(self):
        constraint = """
where int(<number>) % 2 == 0
where int(<number>) > 10000
where int(<number>) < 100000
"""

        with open(RESOURCES_ROOT / "complex_constraints.fan", "r") as file:
            _, constraints = parse(
                file, constraints=[constraint], use_stdlib=False, use_cache=False
            )
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


class ConverterTest(unittest.TestCase):
    def test_standards(self):
        # Earlier Fandango versions overloaded int(); so check if it still works
        self.assertEqual(int(45), 45)
        self.assertEqual(int.from_bytes(b"\x01"), 1)

    def test_string_converters(self):
        tree = DerivationTree(Terminal("5"))
        self.assertEqual(int(tree), 5)
        self.assertEqual(float(tree), 5.0)
        self.assertEqual(complex(tree), 5 + 0j)
        self.assertEqual(bytes(tree), b"5")
        self.assertEqual(str(tree), "5")
        self.assertTrue(bool(tree))
        self.assertEqual(tree.value(), "5")

    def test_byte_converters(self):
        tree = DerivationTree(Terminal(b"\x05"))
        self.assertEqual(bytes(tree), b"\x05")
        self.assertEqual(str(tree), "\x05")
        self.assertTrue(bool(tree))
        self.assertEqual(tree.value(), b"\x05")

    def test_bit_converters(self):
        tree = DerivationTree(Terminal(1))
        self.assertEqual(int(tree), 1)
        self.assertEqual(float(tree), 1.0)
        self.assertEqual(complex(tree), 1 + 0j)
        self.assertEqual(bytes(tree), b"\x01")
        self.assertEqual(str(tree), "\x01")
        self.assertTrue(bool(tree))
        self.assertEqual(tree.value(), 1)
