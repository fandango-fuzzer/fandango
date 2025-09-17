from copy import copy
import enum
from typing import Any, Optional
from fandango.constraints.failing_tree import Comparison, ComparisonSide
from fandango.language.tree import DerivationTree
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import (
    ConstraintFitness,
    FailingTree,
)
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.logger import LOGGER, print_exception


class ComparisonConstraint(Constraint):
    """
    Represents a comparison constraint that can be used for fitness evaluation.
    """

    def __init__(self, operator: Comparison, left: str, right: str, *args, **kwargs):
        """
        Initializes the comparison constraint with the given operator, left side, and right side.
        :param Comparison operator: The operator to use.
        :param str left: The left side of the comparison.
        :param str right: The right side of the comparison.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.operator = operator
        self.left = left
        self.right = right
        self.types_checked = False

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given comparison.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Initialize the fitness values
        solved = 0
        total = 0
        failing_trees = []
        has_combinations = False
        # If the tree is None, the fitness is 0
        if tree is None:
            return ConstraintFitness(0, 0, False)
        # Iterate over all combinations of the tree and the scope
        for combination in self.combinations(tree, scope, population):
            total += 1
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_vars = self.local_variables.copy()
            if local_variables:
                local_vars.update(local_variables)
            local_vars.update(
                {name: container.evaluate() for name, container in combination}
            )
            # Evaluate the left and right side of the comparison
            try:
                left = self.eval(self.left, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self.left}")
                continue

            try:
                right = self.eval(self.right, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self.right}")
                continue

            if not hasattr(self, "types_checked") or not self.types_checked:
                self.types_checked = self.check_type_compatibility(left, right)

            # Initialize the suggestions
            suggestions = []
            is_solved = False
            match self.operator:
                case Comparison.EQUAL:
                    # If the left and right side are equal, the constraint is solved
                    if left == right:
                        is_solved = True
                    else:
                        # If the left and right side are not equal, add suggestions to the list
                        if not self.right.strip().startswith("len("):
                            suggestions.append(
                                (Comparison.EQUAL, left, ComparisonSide.RIGHT)
                            )
                        if not self.left.strip().startswith("len("):
                            suggestions.append(
                                (Comparison.EQUAL, right, ComparisonSide.LEFT)
                            )
                case Comparison.NOT_EQUAL:
                    # If the left and right side are not equal, the constraint is solved
                    if left != right:
                        is_solved = True
                    else:
                        # If the left and right side are equal, add suggestions to the list
                        suggestions.append(
                            (Comparison.NOT_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.NOT_EQUAL, right, ComparisonSide.LEFT)
                        )
                case Comparison.GREATER:
                    # If the left side is greater than the right side, the constraint is solved
                    if left > right:
                        is_solved = True
                    else:
                        # If the left side is not greater than the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.LESS, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.GREATER, right, ComparisonSide.LEFT)
                        )
                case Comparison.GREATER_EQUAL:
                    # If the left side is greater than or equal to the right side, the constraint is solved
                    if left >= right:
                        is_solved = True
                    else:
                        # If the left side is not greater than or equal to the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.LESS_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.GREATER_EQUAL, right, ComparisonSide.LEFT)
                        )
                case Comparison.LESS:
                    # If the left side is less than the right side, the constraint is solved
                    if left < right:
                        is_solved = True
                    else:
                        # If the left side is not less than the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.GREATER, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.LESS, right, ComparisonSide.LEFT)
                        )
                case Comparison.LESS_EQUAL:
                    # If the left side is less than or equal to the right side, the constraint is solved
                    if left <= right:
                        is_solved = True
                    else:
                        # If the left side is not less than or equal to the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.GREATER_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.LESS_EQUAL, right, ComparisonSide.LEFT)
                        )
            if is_solved:
                solved += 1
            else:
                # If the comparison is not solved, add the failing trees to the list
                for _, container in combination:
                    for node in container.get_trees():
                        ft = FailingTree(node, self, suggestions=suggestions)
                        # if ft not in failing_trees:
                        # failing_trees.append(ft)
                        failing_trees.append(ft)

        if not has_combinations:
            solved += 1
            total += 1

        # Create the fitness object
        fitness = ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def check_type_compatibility(self, left: Any, right: Any) -> bool:
        """
        Check the types of `left` and `right` are compatible in a comparison.
        Return True iff check was actually performed
        """
        if left is None and right is None:
            return True

        if left is None or right is None:
            # Cannot check - value does not exist
            return False

        if isinstance(left, type(right)):
            return True

        if isinstance(left, DerivationTree):
            return left.value().can_compare_with(right)
        if isinstance(right, DerivationTree):
            return right.value().can_compare_with(left)

        if isinstance(left, (bool, int, float)) and isinstance(
            right, (bool, int, float)
        ):
            return True

        LOGGER.warning(
            f"{self.format_as_spec()}: {self.operator.value!r}: Cannot compare {type(left).__name__!r} and {type(right).__name__!r}"
        )
        return True

    def format_as_spec(self) -> str:
        representation = f"{self.left} {self.operator.value} {self.right}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, self.searches[identifier].format_as_spec()
            )
        return representation

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        return visitor.visit_comparison_constraint(self)

    def invert(self) -> "ComparisonConstraint":
        """
        Return an inverted version of this comparison constraint.
        The inverted constraint has the opposite comparison operator.
        """
        return ComparisonConstraint(
            self.operator.invert(),
            self.left,
            self.right,
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )
