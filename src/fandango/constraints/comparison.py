from copy import copy
import math
from typing import Any, Optional, Unpack
from fandango.constraints.base import GeneticBaseInitArgs
from fandango.constraints.failing_tree import Comparison, ComparisonSide
from fandango.language.tree import DerivationTree
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import (
    ConstraintFitness,
    DistanceAwareConstraintFitness,
    FailingTree,
)
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.logger import LOGGER, print_exception


class ComparisonConstraint(Constraint):
    """
    Represents a comparison constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        operator: Comparison,
        left: str,
        right: str,
        **kwargs: Unpack[GeneticBaseInitArgs],
    ) -> None:
        """
        Initializes the comparison constraint with the given operator, left side, and right side.
        :param Comparison operator: The operator to use.
        :param str left: The left side of the comparison.
        :param str right: The right side of the comparison.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)
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
        fitness_values = []
        failing_trees = []
        has_combinations = False
        # If the tree is None, the fitness is 0
        if tree is None:
            return DistanceAwareConstraintFitness([], False)
        # Iterate over all combinations of the tree and the scope
        for combination in self.combinations(tree, scope, population):
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
            (fitness_value, suggestions) = self._evaluate_comparison(left, right)
            if fitness_value < 1.0:
                # If the comparison is not solved, add the failing trees to the list
                for _, container in combination:
                    for node in container.get_trees():
                        ft = FailingTree(node, self, suggestions=suggestions)
                        # if ft not in failing_trees:
                        # failing_trees.append(ft)
                        failing_trees.append(ft)

            fitness_values.append(fitness_value)

        if not has_combinations:
            fitness_values.append(1.0)

        fitness = DistanceAwareConstraintFitness(
            fitness_values,
            success=all(it == 1.0 for it in fitness_values),
            failing_trees=failing_trees,
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

    def accept(self, visitor: "ConstraintVisitor") -> None:
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

    def _evaluate_comparison(
        self, left: Any, right: Any
    ) -> tuple[float, list[tuple[Comparison, Any, ComparisonSide]]]:
        suggestions = []
        is_solved = self.operator.compare(left, right)
        fitness = 1.0
        if not is_solved:
            dist_norm = _distance_norm(left, right)
            fitness = (1.0 - dist_norm) if dist_norm is not None else 0.0
            match self.operator:
                case Comparison.EQUAL:
                    if not self.right.strip().startswith("len("):
                        suggestions.append(
                            (Comparison.EQUAL, left, ComparisonSide.RIGHT)
                        )
                    if not self.left.strip().startswith("len("):
                        suggestions.append(
                            (Comparison.EQUAL, right, ComparisonSide.LEFT)
                        )
                case Comparison.NOT_EQUAL:
                    # NOT_EQUAL does not span a range to the fitness is immediately zero if they are equal
                    fitness = 0.0

                    suggestions.append(
                        (Comparison.NOT_EQUAL, left, ComparisonSide.RIGHT)
                    )
                    suggestions.append(
                        (Comparison.NOT_EQUAL, right, ComparisonSide.LEFT)
                    )
                case Comparison.GREATER:
                    suggestions.append((Comparison.LESS, left, ComparisonSide.RIGHT))
                    suggestions.append((Comparison.GREATER, right, ComparisonSide.LEFT))
                case Comparison.GREATER_EQUAL:
                    suggestions.append(
                        (Comparison.LESS_EQUAL, left, ComparisonSide.RIGHT)
                    )
                    suggestions.append(
                        (Comparison.GREATER_EQUAL, right, ComparisonSide.LEFT)
                    )
                case Comparison.LESS:
                    suggestions.append((Comparison.GREATER, left, ComparisonSide.RIGHT))
                    suggestions.append((Comparison.LESS, right, ComparisonSide.LEFT))
                case Comparison.LESS_EQUAL:
                    suggestions.append(
                        (Comparison.GREATER_EQUAL, left, ComparisonSide.RIGHT)
                    )
                    suggestions.append(
                        (Comparison.LESS_EQUAL, right, ComparisonSide.LEFT)
                    )
        return fitness, suggestions


def _distance_norm(left: Any, right: Any) -> float | None:
    """
    Generates a normalized distance between two values.
    The values if calculated by `2*sigmoid(|left - right|)`
    The resulting value is a float between 0 and 1.
    """

    # Although left and right can be used for comparison, they may not support minus.
    try:
        dist = left - right
    except Exception:
        try:
            dist = right - left
        except Exception:
            return None

    if dist is float | int:
        dist = 2 * (_sigmoid(abs(dist)) - 0.5)
        return dist
    else:
        return None


def _sigmoid(x: float | int):
    return 1 / (1 + math.exp(-x))
