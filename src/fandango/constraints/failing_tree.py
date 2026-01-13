import abc
import enum
from typing import TYPE_CHECKING, Any
from collections.abc import Sequence
from fandango.language.tree import DerivationTree
from fandango.constraints.base import GeneticBase

if TYPE_CHECKING:
    import fandango


class Comparison(enum.Enum):
    """
    Enum class for comparison operations.
    """

    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="

    def invert(self) -> "Comparison":
        """
        Return the inverse comparison operator.
        """
        inverse_operators = {
            Comparison.EQUAL: Comparison.NOT_EQUAL,
            Comparison.NOT_EQUAL: Comparison.EQUAL,
            Comparison.GREATER: Comparison.LESS_EQUAL,
            Comparison.GREATER_EQUAL: Comparison.LESS,
            Comparison.LESS: Comparison.GREATER_EQUAL,
            Comparison.LESS_EQUAL: Comparison.GREATER,
        }
        return inverse_operators[self]

    def compare(self, left: Any, right: Any) -> bool:
        """
        Compare two values using the comparison operator.
        """
        match self:
            case Comparison.EQUAL:
                return bool(left == right)
            case Comparison.NOT_EQUAL:
                return bool(left != right)
            case Comparison.GREATER:
                return bool(left > right)
            case Comparison.GREATER_EQUAL:
                return bool(left >= right)
            case Comparison.LESS:
                return bool(left < right)
            case Comparison.LESS_EQUAL:
                return bool(left <= right)
        raise ValueError(f"Invalid comparison operator: {self}")


class ComparisonSide(enum.Enum):
    """
    Enum class for comparison side.
    """

    LEFT = "left"
    RIGHT = "right"


class Suggestion:
    """
    Possible solution to fix a failing tree.
    """

    @abc.abstractmethod
    def get_replacements(
        self,
        individual: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        """
        Get the replacements for the failing tree.

        :param individual: The individual to get the replacements for.
        :param grammar: The grammar to use for parsing.
        :return: Replacements (target, source) pairs.
        """

    @abc.abstractmethod
    def rec_set_allow_repetition_full_delete(self, allow_repetition_full_delete: bool):
        """
        Recursively set the allow_repetition_full_delete flag for all RepetitionBoundsConstraints.

        :param allow_repetition_full_delete: Whether to allow repetition full delete.
        """
        pass


class ApplyAllSuggestions(Suggestion):
    """
    Merge all replacements from the sub-suggestions.
    """

    def __init__(self, suggestions: Sequence[Suggestion]):
        """
        Initialize the ApplyAllSuggestions with the given suggestions.
        """
        self.suggestions = suggestions

    def rec_set_allow_repetition_full_delete(self, allow_repetition_full_delete: bool):
        for s in self.suggestions:
            s.rec_set_allow_repetition_full_delete(allow_repetition_full_delete)

    def get_replacements(
        self,
        individual: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        """
        Get the replacements for the failing tree.

        :param individual: The individual to get the replacements for.
        :param grammar: The grammar to use for parsing.
        :return: Replacements (target, source) pairs.
        """

        return [
            replacement
            for suggestion in self.suggestions
            for replacement in suggestion.get_replacements(
                individual=individual, grammar=grammar
            )
        ]


class ApplyFirstSuggestion(Suggestion):
    """
    Iterate over the sub-suggestions and return the replacements from the first suggestion that provides any replacements.
    """

    def __init__(self, suggestions: Sequence[Suggestion]):
        """
        Initialize the ApplyFirstSuggestion with the given suggestions.
        """
        self.suggestions = suggestions

    def rec_set_allow_repetition_full_delete(self, allow_repetition_full_delete: bool):
        for s in self.suggestions:
            s.rec_set_allow_repetition_full_delete(allow_repetition_full_delete)

    def get_replacements(
        self,
        individual: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        """
        Get the replacements for the failing tree.

        :param individual: The individual to get the replacements for.
        :param grammar: The grammar to use for parsing.
        :return: Replacements (target, source) pairs.
        """
        for suggestion in self.suggestions:
            if replacements := suggestion.get_replacements(
                individual=individual, grammar=grammar
            ):
                return replacements
        return []


class NopSuggestion(Suggestion):
    """
    When there is no hope left.
    """

    def get_replacements(
        self,
        individual: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        return []

    def rec_set_allow_repetition_full_delete(self, allow_repetition_full_delete: bool):
        pass


class FailingTree:
    """
    Class to represent a failing tree, i.e., a tree that does not satisfy a given constraint.
    """

    def __init__(
        self,
        tree: DerivationTree,
        cause: GeneticBase,
    ):
        """
        Initialize the FailingTree with the given tree, cause, and suggestions.

        :param DerivationTree tree: The tree that failed to satisfy the constraint.
        :param GeneticBase cause: The cause of the failure.
        """
        self.tree = tree
        self.cause = cause

    def __hash__(self) -> int:
        return hash((self.tree, self.cause))

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, FailingTree)
            and self.tree == other.tree
            and self.cause == other.cause
        )

    def __repr__(self) -> str:
        return f"FailingTree({self.tree}, {self.cause})"

    def __str__(self) -> str:
        return self.__repr__()
