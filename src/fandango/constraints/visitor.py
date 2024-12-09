import logging
from fandango.logger import LOGGER
from fandango.constraints.base import (
    Constraint,
    ExpressionConstraint,
    ComparisonConstraint,
    ForallConstraint,
    ExistsConstraint,
    DisjunctionConstraint,
    ConjunctionConstraint,
    ImplicationConstraint,
    ConstraintVisitor,
)


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
