#!/usr/bin/env pytest

import unittest
from collections import defaultdict
import logging

from fandango.language.parse import parse
from fandango.constraints.base import *
from fandango.logger import LOGGER
from .utils import RESOURCES_ROOT


class CountingVisitor(ConstraintVisitor):
    """
    A simple visitor that counts the occurrences of each constraint type.
    Stores counts in a defaultdict for easy access during testing.
    """

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


class LoggingVisitor(ConstraintVisitor):

    def __init__(self):
        super().__init__()
        LOGGER.setLevel(logging.DEBUG)

    def do_continue(self, constraint: "Constraint") -> bool:
        return True

    def visit_expression_constraint(self, constraint: "ExpressionConstraint"):
        LOGGER.info("Visiting expression constraint")

    def visit_comparison_constraint(self, constraint: "ComparisonConstraint"):
        LOGGER.info("Visiting comparison constraint")

    def visit_forall_constraint(self, constraint: "ForallConstraint"):
        LOGGER.info("Visiting forall constraint")

    def visit_exists_constraint(self, constraint: "ExistsConstraint"):
        LOGGER.info("Visiting exists constraint")

    def visit_disjunction_constraint(self, constraint: "DisjunctionConstraint"):
        LOGGER.info("Visiting disjunction constraint")

    def visit_conjunction_constraint(self, constraint: "ConjunctionConstraint"):
        LOGGER.info("Visiting conjunction constraint")

    def visit_implication_constraint(self, constraint: "ImplicationConstraint"):
        LOGGER.info("Visiting implication constraint")


class TestConstraintVisitor(unittest.TestCase):

    def get_constraint(self, constraint):
        with open(RESOURCES_ROOT / "constraints.fan", "r") as file:
            _, constraints = parse(
                file, constraints=[constraint], use_stdlib=False, use_cache=False
            )
        self.assertEqual(1, len(constraints))
        return constraints[0]

    def test_something(self):
        """
        Tests the LoggingVisitor by visiting a simple forall constraint.
        Validates that no errors occur during visitation.
        """
        constraint = self.get_constraint("forall <x> in <ab>: 'a' not in str(<x>);")
        visitor = LoggingVisitor()
        constraint.accept(visitor)

    def test_counting_visitor(self):
        """
        Tests the CountingVisitor by counting constraint types in a simple forall constraint.
        Validates that the counts are correct for each constraint type.
        """
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
        """
        Tests the CountingVisitor with nested constraints.
        Validates correct counts for nested forall, exists, and comparison constraints.
        """
        constraint = self.get_constraint(
            "forall <x> in <ab>: exists <y> in <cd>: str(<x>) == str(<y>) or str(<y>) != 'test';"
        )
        visitor = CountingVisitor()
        constraint.accept(visitor)

        # Validate counts for nested structure
        self.assertEqual(visitor.counts["ForallConstraint"], 1)
        self.assertEqual(visitor.counts["ExistsConstraint"], 1)
        self.assertEqual(visitor.counts["ComparisonConstraint"], 2)
        self.assertEqual(visitor.counts["DisjunctionConstraint"], 1)


if __name__ == "__main__":
    unittest.main()
