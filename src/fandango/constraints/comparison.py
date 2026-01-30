from copy import copy
import math
from typing import Any, Optional, Unpack, cast
from fandango.constraints.base import GeneticBaseInitArgs
from fandango.constraints.failing_tree import (
    ApplyAllSuggestions,
    ApplyFirstSuggestion,
    Comparison,
    FailingTree,
    NopSuggestion,
    Suggestion,
)
from fandango.language.grammar.grammar import Grammar
from fandango.language.search import (
    AnnotatedContainer,
    AnnotatedSearch,
    NonTerminalSearch,
)
from fandango.language.tree import DerivationTree
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import (
    ConstraintFitness,
    DistanceAwareConstraintFitness,
)
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.logger import LOGGER, print_exception


class EqualComparisonSuggestion(Suggestion):
    def __init__(self, target: DerivationTree, source: Any):
        """
        Try parsing source into target.

        :param target: The target to parse into.
        :param source: What to parse.
        """
        assert isinstance(target.symbol, NonTerminal)
        self._target = target
        self._source = source

    def get_replacements(
        self, individual: DerivationTree, grammar: Grammar
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        """
        Get the replacements for the failing tree.

        :param individual: The individual to get the replacements for.
        :param grammar: The grammar to use for parsing.
        :return: Replacements (target, source) pairs.
        """
        symbol = self._target.symbol
        assert isinstance(symbol, NonTerminal)

        # don't parse if same symbol
        if isinstance(self._source, DerivationTree) and symbol == self._source.symbol:
            return [
                (
                    self._target,
                    self._source.deepcopy(
                        copy_children=True, copy_params=False, copy_parent=False
                    ),
                )
            ]

        elif suggested_tree := grammar.parse(self._source, start=symbol):
            return [(self._target, suggested_tree)]

        return []


class ComparisonConstraint(Constraint):
    """
    Represents a comparison constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        operator: Comparison,
        left: str,
        right: str,
        left_searches: dict[str, NonTerminalSearch] = dict(),
        right_searches: dict[str, NonTerminalSearch] = dict(),
        **kwargs: Unpack[GeneticBaseInitArgs],
    ) -> None:
        """
        Initializes the comparison constraint with the given operator, left side, and right side.
        :param Comparison operator: The operator to use.
        :param str left: The left side of the comparison.
        :param str right: The right side of the comparison.
        :param dict[str, NonTerminalSearch] left_searches: The searches to use for the left side.
        :param dict[str, NonTerminalSearch] right_searches: The searches to use for the right side.
        :param kwargs: Additional keyword arguments.
        """
        assert (
            "searches" not in kwargs
        ), "don't provide searches combination, instead provide left_searches and right_searches"
        searches: dict[str, NonTerminalSearch] = {}
        searches.update(
            {
                k: AnnotatedSearch(annotation="l", inner=v)
                for k, v in left_searches.items()
            }
        )
        searches.update(
            {
                k: AnnotatedSearch(annotation="r", inner=v)
                for k, v in right_searches.items()
            }
        )
        kwargs["searches"] = searches
        super().__init__(**kwargs)

        self._left_searches = left_searches
        self._right_searches = right_searches
        self._operator = operator
        self._left = left
        self._right = right
        self._types_checked = False

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given comparison.
        """
        tree_hash = self.get_hash(tree, scope, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Initialize the fitness values
        fitness_values = []
        failing_trees: list[FailingTree] = []
        has_combinations = False
        suggestions = []
        # If the tree is None, the fitness is 0
        if tree is None:
            return DistanceAwareConstraintFitness([], False)
        # Iterate over all combinations of the tree and the scope
        for untyped_combination in self.combinations(tree, scope):
            # this only holds if all searches are wrapped in AnnotatedSearches
            # and here this is done in the constructor of this class
            combination = cast(
                tuple[tuple[str, AnnotatedContainer[str]], ...], untyped_combination
            )
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_vars = self.local_variables.copy()
            if local_variables:
                local_vars.update(local_variables)

            var_evals = {
                name: (container.annotation, container.evaluate())
                for name, container in combination
            }
            local_vars.update({k: v[1] for k, v in var_evals.items()})
            left_trees = []
            right_trees = []

            for annotation, tree in filter(
                lambda x: isinstance(x[1], DerivationTree), var_evals.values()
            ):
                match annotation:
                    case "l":
                        left_trees.append(tree)
                    case "r":
                        right_trees.append(tree)

            single_left_tree = None if len(left_trees) != 1 else left_trees[0]
            single_right_tree = None if len(right_trees) != 1 else right_trees[0]

            # Evaluate the left and right side of the comparison
            try:
                left = self.eval(self._left, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self._left}")
                continue

            try:
                right = self.eval(self._right, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self._right}")
                continue

            if not hasattr(self, "types_checked") or not self._types_checked:
                self._types_checked = self.check_type_compatibility(left, right)

            fitness_value, suggestion = self._evaluate_comparison(
                left, right, single_left_tree, single_right_tree
            )
            if fitness_value < 1.0:
                # If the comparison is not solved, add the failing trees to the list
                for _, container in combination:
                    failing_trees.extend(
                        FailingTree(node, self) for node in container.get_trees()
                    )

            fitness_values.append(fitness_value)
            if suggestion is not None:
                suggestions.append(suggestion)

        if not has_combinations:
            fitness_values.append(1.0)

        fitness = DistanceAwareConstraintFitness(
            fitness_values,
            success=all(it == 1.0 for it in fitness_values),
            failing_trees=failing_trees,
            suggestion=ApplyAllSuggestions(suggestions),
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
            f"{self.format_as_spec()}: {self._operator.value!r}: Cannot compare {type(left).__name__!r} and {type(right).__name__!r}"
        )
        return True

    def format_as_spec(self) -> str:
        representation = f"{self._left} {self._operator.value} {self._right}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, self.searches[identifier].format_as_spec()
            )
        return representation

    def accept(self, visitor: ConstraintVisitor) -> None:
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
            self._operator.invert(),
            self._left,
            self._right,
            left_searches=self._left_searches,
            right_searches=self._right_searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )

    def _evaluate_comparison(
        self,
        left: Any,
        right: Any,
        single_left_tree: Optional[DerivationTree],
        single_right_tree: Optional[DerivationTree],
    ) -> tuple[float, Suggestion]:
        """
        Evaluate the comparison.
        :param left: The left side of the comparison.
        :param right: The right side of the comparison.
        :param single_left_tree: If the left side depends on exactly one non-terminal, the tree below it.
        :param single_right_tree: If the right side depends on exactly one non-terminal, the tree below it.
        :return: The fitness and combined suggestion.
        """
        if self._operator.compare(left, right):
            return 1.0, NopSuggestion()

        dist_norm = _distance_norm(left, right)
        fitness = (1.0 - dist_norm) if dist_norm is not None else 0.0
        if self._operator == Comparison.NOT_EQUAL:
            # NOT_EQUAL does not span a range to the fitness is immediately zero if they are equal (introduced by @henryhchchc, moved by @riesentoaster)
            fitness = 0.0

        suggestions = []

        match self._operator:
            case Comparison.EQUAL:
                # only suggest fixes if there is a single nt on one side and that nt linearizes to exactly the value
                # otherwise, it is messed with and attempts at parsing it will have unexpected consequences
                # e.g. <len> % 2 == 0
                # this will always fix <len> to 0
                # or <first_name> + "Doe" == "John Doe"
                # this will try to parse "John Doe" into <first_name>, which is not what we want
                # we need to make sure we can actually parse the value into the tree type-wise, before comparing the actual values
                if (
                    single_left_tree is not None
                    and isinstance(single_left_tree.symbol, NonTerminal)
                    and single_left_tree.parseable_from(left)
                    and single_left_tree == left
                ):
                    suggestions.append(
                        EqualComparisonSuggestion(single_left_tree, right)
                    )
                if (
                    single_right_tree is not None
                    and isinstance(single_right_tree.symbol, NonTerminal)
                    and single_right_tree.parseable_from(right)
                    and single_right_tree == right
                ):
                    suggestions.append(
                        EqualComparisonSuggestion(single_right_tree, left)
                    )

        return fitness, ApplyFirstSuggestion(suggestions)


def _distance_norm(left: Any, right: Any) -> Optional[float]:
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


def _sigmoid(x: float | int) -> float:
    return 1 / (1 + math.exp(-x))
