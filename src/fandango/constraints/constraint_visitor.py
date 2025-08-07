from typing import TYPE_CHECKING

from fandango.constraints.constraint import Constraint

if TYPE_CHECKING:
    from fandango.constraints.comparison import ComparisonConstraint
    from fandango.constraints.conjunction import ConjunctionConstraint
    from fandango.constraints.disjunct import DisjunctionConstraint
    from fandango.constraints.expression import ExpressionConstraint
    from fandango.constraints.forall import ForallConstraint
    from fandango.constraints.exists import ExistsConstraint
    from fandango.constraints.implication import ImplicationConstraint
    from fandango.constraints.repetition_bounds import (
        RepetitionBoundsConstraint,
    )


class ConstraintVisitor:
    """
    A base class for visiting and processing different types of constraints.

    This class uses the visitor pattern to traverse constraint structures. Each method
    corresponds to a specific type of constraint, allowing implementations to define
    custom behavior for processing or interacting with that type.
    """

    def __init__(self):
        pass

    def do_continue(self, constraint: "Constraint") -> bool:
        """If this returns False, this formula should not call the visit methods for
        its children."""
        return True

    def visit(self, constraint: "Constraint"):
        """Visits a constraint."""
        return constraint.accept(self)

    def visit_expression_constraint(self, constraint: "ExpressionConstraint"):
        """Visits an expression constraint."""
        pass

    def visit_comparison_constraint(self, constraint: "ComparisonConstraint"):
        """Visits a comparison constraint."""
        pass

    def visit_forall_constraint(self, constraint: "ForallConstraint"):
        """Visits a forall constraint."""
        pass

    def visit_exists_constraint(self, constraint: "ExistsConstraint"):
        """Visits an exists constraint."""
        pass

    def visit_disjunction_constraint(self, constraint: "DisjunctionConstraint"):
        """Visits a disjunction constraint."""
        pass

    def visit_conjunction_constraint(self, constraint: "ConjunctionConstraint"):
        """Visits a conjunction constraint."""
        pass

    def visit_implication_constraint(self, constraint: "ImplicationConstraint"):
        """Visits an implication constraint."""
        pass

    def visit_repetition_bounds_constraint(
        self, constraint: "RepetitionBoundsConstraint"
    ):
        """Visits a repetition bounds constraint."""
        pass
