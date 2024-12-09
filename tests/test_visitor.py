import unittest
from collections import defaultdict

from fandango.language.parse import parse
from fandango.constraints.visitor import LoggingVisitor
from fandango.constraints.base import *


class CountingVisitor(ConstraintVisitor):
    def __init__(self):
        super().__init__()
        self.counts = defaultdict(int)

    def visit_expression_constraint(self, constraint: "ExpressionConstraint"):
        self.counts["ExpressionConstraint"] += 1

    def visit_comparison_constraint(self, constraint: "ComparisonConstraint"):
        self.counts["ComparisonConstraint"] += 1

    def visit_forall_constraint(self, constraint: "ForallConstraint"):
        self.counts["ForallConstraint"] += 1

    def visit_exists_constraint(self, constraint: "ExistsConstraint"):
        self.counts["ExistsConstraint"] += 1

    def visit_disjunction_constraint(self, constraint: "DisjunctionConstraint"):
        self.counts["DisjunctionConstraint"] += 1

    def visit_conjunction_constraint(self, constraint: "ConjunctionConstraint"):
        self.counts["ConjunctionConstraint"] += 1

    def visit_implication_constraint(self, constraint: "ImplicationConstraint"):
        self.counts["ImplicationConstraint"] += 1


class TestConstraintVisitor(unittest.TestCase):

    def get_constraint(self, constraint):
        _, constraints = parse(constraint)
        self.assertEqual(1, len(constraints))
        return constraints[0]

    def test_something(self):
        constraint = self.get_constraint("forall <x> in <ab>: 'a' not in str(<x>);")
        visitor = LoggingVisitor()

        constraint.accept(visitor)

    def test_counting_visitor(self):
        # Parse the constraint
        constraint = self.get_constraint("forall <x> in <ab>: 'a' not in str(<x>);")

        visitor = CountingVisitor()
        constraint.accept(visitor)

        # Validate counts
        self.assertEqual(visitor.counts["ForallConstraint"], 1)
        self.assertEqual(visitor.counts["ExpressionConstraint"], 1)
        self.assertEqual(visitor.counts["ComparisonConstraint"], 0)
        self.assertEqual(visitor.counts["ExistsConstraint"], 0)
        self.assertEqual(visitor.counts["ConjunctionConstraint"], 0)

    def test_nested_constraints(self):
        constraint = self.get_constraint(
            "forall <x> in <ab>: exists <y> in <cd>: str(<x>) == str(<y>) or str(<y>) != 'test';"
        )
        visitor = CountingVisitor()
        constraint.accept(visitor)

        self.assertEqual(visitor.counts["ForallConstraint"], 1)
        self.assertEqual(visitor.counts["ExistsConstraint"], 1)
        self.assertEqual(visitor.counts["ComparisonConstraint"], 2)
        self.assertEqual(visitor.counts["DisjunctionConstraint"], 1)


if __name__ == "__main__":
    unittest.main()
