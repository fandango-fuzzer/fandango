#!/usr/bin/env pytest

import unittest


from fandango.constraints.constraint import Constraint
from fandango.constraints.comparison import ComparisonConstraint
from fandango.constraints.conjunction import ConjunctionConstraint
from fandango.constraints.disjunct import DisjunctionConstraint
from fandango.constraints.exists import ExistsConstraint
from fandango.constraints.forall import ForallConstraint
from fandango.constraints.expression import ExpressionConstraint
from fandango.constraints.implication import ImplicationConstraint
from fandango.constraints.failing_tree import Comparison
from fandango.language.symbols import NonTerminal, Terminal
from fandango.language.tree import DerivationTree
from fandango.language.parse import parse
from fandango.language.search import RuleSearch
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
            grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None

        self.assertEqual(1, len(constraints))
        constraint = constraints[0]
        assert isinstance(constraint, Constraint)

        counter_example = grammar.parse("19")
        assert counter_example is not None
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("11")
        self.assertTrue(constraint.check(example))

    def test_accessing_children(self):
        with open(RESOURCES_ROOT / "children.fan", "r") as file:
            grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
            assert grammar is not None
        constraint = constraints[0]
        assert isinstance(constraint, Constraint)

        counter_example = grammar.parse("11")
        self.assertFalse(constraint.check(counter_example))

        example = grammar.parse("01")
        self.assertTrue(constraint.check(example))

    def test_eval_constraint(self):
        with open(RESOURCES_ROOT / "eval.fan") as file:
            grammar, constraints = parse(file, use_stdlib=True, use_cache=False)
            assert grammar is not None
        constraint = constraints[0]

        counter_example = grammar.parse("+05 * 0 / 96 + 10")
        self.assertIsNone(counter_example)

        example = grammar.parse("+5 * 0 / 96 + 10")
        self.assertTrue(constraint.check(example))

    def test_complex_constraint(self):
        constraint_str = """
where int(<number>) % 2 == 0
where int(<number>) > 10000
where int(<number>) < 100000
"""

        with open(RESOURCES_ROOT / "complex_constraints.fan", "r") as file:
            _, constraints = parse(
                file, constraints=[constraint_str], use_stdlib=False, use_cache=False
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
                assert isinstance(constraint, Constraint)
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
        self.assertEqual(bytes(tree), b"5")
        self.assertEqual(str(tree), "5")
        self.assertEqual(tree.value(), "5")

    def test_byte_converters(self):
        tree = DerivationTree(Terminal(b"\x05"))
        self.assertEqual(bytes(tree), b"\x05")
        self.assertEqual(str(tree), "\x05")
        self.assertEqual(tree.value(), b"\x05")

    def test_bit_converters(self):
        tree = DerivationTree(Terminal(1))
        self.assertEqual(int(tree), 1)
        self.assertEqual(tree.to_bits(), "1")


class InvertConstraintTest(unittest.TestCase):
    """Test class for the invert functionality of constraints."""

    def test_comparison_constraint_invert(self):
        """Test that comparison constraints are correctly inverted."""
        # Test all comparison operators
        test_cases = [
            (Comparison.EQUAL, Comparison.NOT_EQUAL),
            (Comparison.NOT_EQUAL, Comparison.EQUAL),
            (Comparison.GREATER, Comparison.LESS_EQUAL),
            (Comparison.GREATER_EQUAL, Comparison.LESS),
            (Comparison.LESS, Comparison.GREATER_EQUAL),
            (Comparison.LESS_EQUAL, Comparison.GREATER),
        ]

        for original_op, expected_inverted_op in test_cases:
            constraint = ComparisonConstraint(original_op, "x", "y")
            inverted = constraint.invert()

            assert isinstance(inverted, ComparisonConstraint)
            self.assertEqual(inverted.operator, expected_inverted_op)
            self.assertEqual(inverted.left, "x")
            self.assertEqual(inverted.right, "y")

    def test_comparison_enum_invert(self):
        """Test that the Comparison enum's invert method works correctly."""
        # Test all comparison operators
        test_cases = [
            (Comparison.EQUAL, Comparison.NOT_EQUAL),
            (Comparison.NOT_EQUAL, Comparison.EQUAL),
            (Comparison.GREATER, Comparison.LESS_EQUAL),
            (Comparison.GREATER_EQUAL, Comparison.LESS),
            (Comparison.LESS, Comparison.GREATER_EQUAL),
            (Comparison.LESS_EQUAL, Comparison.GREATER),
        ]

        for original_op, expected_inverted_op in test_cases:
            inverted_op = original_op.invert()
            self.assertEqual(inverted_op, expected_inverted_op)

            # Test double inversion returns the original
            double_inverted = inverted_op.invert()
            self.assertEqual(double_inverted, original_op)

    def test_expression_constraint_invert(self):
        """Test that expression constraints are correctly inverted."""
        constraint = ExpressionConstraint("x > 5")
        inverted = constraint.invert()

        assert isinstance(inverted, ExpressionConstraint)
        self.assertEqual(inverted.expression, "not (x > 5)")

    def test_conjunction_constraint_invert(self):
        """Test that conjunction constraints are correctly inverted using De Morgan's law."""
        # Create two simple constraints
        c1 = ExpressionConstraint("x > 5")
        c2 = ExpressionConstraint("y < 10")

        conjunction = ConjunctionConstraint([c1, c2])
        inverted = conjunction.invert()

        assert isinstance(inverted, DisjunctionConstraint)
        self.assertEqual(len(inverted.constraints), 2)

        # Check that the sub-constraints are inverted
        assert isinstance(inverted.constraints[0], ExpressionConstraint)
        self.assertEqual(inverted.constraints[0].expression, "not (x > 5)")

        assert isinstance(inverted.constraints[1], ExpressionConstraint)
        self.assertEqual(inverted.constraints[1].expression, "not (y < 10)")

    def test_disjunction_constraint_invert(self):
        """Test that disjunction constraints are correctly inverted using De Morgan's law."""
        # Create two simple constraints
        c1 = ExpressionConstraint("x > 5")
        c2 = ExpressionConstraint("y < 10")

        disjunction = DisjunctionConstraint([c1, c2])
        inverted = disjunction.invert()

        assert isinstance(inverted, ConjunctionConstraint)

        self.assertEqual(len(inverted.constraints), 2)

        # Check that the sub-constraints are inverted
        assert isinstance(inverted.constraints[0], ExpressionConstraint)
        self.assertEqual(inverted.constraints[0].expression, "not (x > 5)")

        assert isinstance(inverted.constraints[1], ExpressionConstraint)
        self.assertEqual(inverted.constraints[1].expression, "not (y < 10)")

    def test_implication_constraint_invert(self):
        """Test that implication constraints are correctly inverted."""
        antecedent = ExpressionConstraint("x > 5")
        consequent = ExpressionConstraint("y < 10")

        implication = ImplicationConstraint(antecedent, consequent)
        inverted = implication.invert()

        assert isinstance(inverted, ConjunctionConstraint)
        self.assertEqual(len(inverted.constraints), 2)

        # The antecedent should remain the same
        self.assertEqual(inverted.constraints[0], antecedent)

        # The consequent should be inverted
        assert isinstance(inverted.constraints[1], ExpressionConstraint)
        self.assertEqual(inverted.constraints[1].expression, "not (y < 10)")

    def test_exists_constraint_invert(self):
        """Test that exists constraints are correctly inverted."""
        statement = ExpressionConstraint("x > 5")
        bound = "item"
        search = RuleSearch(NonTerminal("<items>"))

        exists_constraint = ExistsConstraint(statement, bound, search)
        inverted = exists_constraint.invert()

        assert isinstance(inverted, ForallConstraint)
        self.assertEqual(inverted.bound, bound)
        self.assertEqual(inverted.search, search)

        # The statement should be inverted
        assert isinstance(inverted.statement, ExpressionConstraint)
        self.assertEqual(inverted.statement.expression, "not (x > 5)")

    def test_forall_constraint_invert(self):
        """Test that forall constraints are correctly inverted."""
        statement = ExpressionConstraint("x > 5")
        bound = "item"
        search = RuleSearch(NonTerminal("<items>"))

        forall_constraint = ForallConstraint(statement, bound, search)
        inverted = forall_constraint.invert()

        assert isinstance(inverted, ExistsConstraint)
        self.assertEqual(inverted.bound, bound)
        self.assertEqual(inverted.search, search)

        # The statement should be inverted
        assert isinstance(inverted.statement, ExpressionConstraint)
        self.assertEqual(inverted.statement.expression, "not (x > 5)")

    def test_double_invert_identity(self):
        """Test that inverting a constraint twice returns the original constraint."""
        # Test with a comparison constraint
        original = ComparisonConstraint(Comparison.EQUAL, "x", "y")
        inverted = original.invert()
        double_inverted = inverted.invert()

        self.assertEqual(double_inverted.operator, original.operator)
        self.assertEqual(double_inverted.left, original.left)
        self.assertEqual(double_inverted.right, original.right)

        # Test with an expression constraint - double negation is preserved
        original_expr = ExpressionConstraint("x > 5")
        inverted_expr = original_expr.invert()
        double_inverted_expr = inverted_expr.invert()

        # The double negation should be preserved: not (not (x > 5))
        self.assertEqual(double_inverted_expr.expression, "not (not (x > 5))")

    def test_complex_nested_invert(self):
        """Test that complex nested constraints are correctly inverted."""
        # Create a complex constraint: (x > 5 and y < 10) or (z == 0)
        c1 = ExpressionConstraint("x > 5")
        c2 = ExpressionConstraint("y < 10")
        c3 = ExpressionConstraint("z == 0")

        conjunction = ConjunctionConstraint([c1, c2])
        disjunction = DisjunctionConstraint([conjunction, c3])

        inverted = disjunction.invert()

        # The result should be: not (x > 5 and y < 10) and not (z == 0)
        # Which is: (not (x > 5) or not (y < 10)) and not (z == 0)
        assert isinstance(inverted, ConjunctionConstraint)
        self.assertEqual(len(inverted.constraints), 2)

        # First constraint should be a disjunction
        assert isinstance(inverted.constraints[0], DisjunctionConstraint)
        self.assertEqual(len(inverted.constraints[0].constraints), 2)

        # Second constraint should be an inverted expression
        assert isinstance(inverted.constraints[1], ExpressionConstraint)
        self.assertEqual(inverted.constraints[1].expression, "not (z == 0)")
