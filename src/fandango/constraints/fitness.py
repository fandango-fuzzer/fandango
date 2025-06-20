"""
The `fitness` module provides the `Fitness` class and its subclasses `ValueFitness` and `ConstraintFitness`.
"""

import abc
import enum
import itertools
from typing import Optional, Any

from fandango.language.search import NonTerminalSearch, Container
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


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


class ComparisonSide(enum.Enum):
    """
    Enum class for comparison side.
    """

    LEFT = "left"
    RIGHT = "right"


class FailingTree:
    """
    Class to represent a failing tree, i.e., a tree that does not satisfy a given constraint.
    """

    def __init__(
        self,
        tree: DerivationTree,
        cause: "GeneticBase",
        suggestions: Optional[list[tuple[Comparison, Any, ComparisonSide]]] = None,
    ):
        """
        Initialize the FailingTree with the given tree, cause, and suggestions.

        :param DerivationTree tree: The tree that failed to satisfy the constraint.
        :param GeneticBase cause: The cause of the failure.
        :param Optional[list[tuple[Comparison, Any, ComparisonSide]]] suggestions: The list of suggestions to
        which causes the cause to fail.
        """
        self.tree = tree
        self.cause = cause
        self.suggestions = suggestions or []

    def __hash__(self):
        return hash((self.tree, self.cause))

    def __eq__(self, other):
        return self.tree == other.tree and self.cause == other.cause

    def __repr__(self):
        return f"FailingTree({self.tree}, {self.cause}, {self.suggestions})"

    def __str__(self):
        return self.__repr__()


class Fitness(abc.ABC):
    """
    Abstract class to represent the fitness of a tree.
    """

    def __init__(
        self, success: bool, failing_trees: Optional[list[FailingTree]] = None
    ):
        """
        Initialize the Fitness with the given success and failing trees.

        :param bool success: The success of the fitness.
        :param Optional[list[FailingTree]] failing_trees: The list of failing trees.
        """
        self.success = success
        self.failing_trees = failing_trees or []

    @abc.abstractmethod
    def fitness(self) -> float:
        """
        Abstract method to calculate the fitness of the tree.
        :return float: The fitness of the tree.
        """
        pass

    @abc.abstractmethod
    def __copy__(self) -> "Fitness":
        pass

    def __repr__(self):
        return f"Fitness(success={self.success})"


class ValueFitness(Fitness):
    """
    Class to represent the fitness of a tree based on calculated values.
    The fitness is calculated as the average of the values.
    This class contrast the `ConstraintFitness` class, which calculates the fitness based on the number of
    constraints satisfied.
    """

    def __init__(
        self,
        values: Optional[list[float]] = None,
        failing_trees: Optional[list[FailingTree]] = None,
    ):
        """
        Initialize the ValueFitness with the given values and failing trees.
        :param Optional[list[float]] values: The list of values.
        :param Optional[list[FailingTree]] failing_trees: The list of failing trees.
        """
        super().__init__(True, failing_trees)
        self.values = values or []

    def fitness(self) -> float:
        """
        Calculate the fitness of the tree as the average of the values.
        :return float: The fitness of the tree.
        """
        if self.values:
            try:
                return sum(self.values) / len(self.values)
            except OverflowError:
                # OverflowError: integer division result too large for a float
                return sum(self.values) // len(self.values)
        else:
            return 0

    def __copy__(self) -> Fitness:
        return ValueFitness(self.values[:])

    def __repr__(self):
        return f"ValueFitness(values={self.values})"


class ConstraintFitness(Fitness):
    """
    Class to represent the fitness of a tree based on constraints.
    The fitness is calculated as the number of constraints solved by the tree divided by the total number of
    constraints.
    """

    def __init__(
        self,
        solved: int,
        total: int,
        success: bool,
        failing_trees: Optional[list[FailingTree]] = None,
    ):
        """
        Initialize the ConstraintFitness with the given solved, total, success, and failing trees.
        :param int solved: The number of constraints solved by the tree.
        :param int total: The total number of constraints.
        :param bool success: The success of the fitness.
        :param Optional[list[FailingTree]] failing_trees: The list of failing trees.
        """
        super().__init__(success, failing_trees)
        self.solved = solved
        self.total = total

    def fitness(self) -> float:
        """
        Calculate the fitness of the tree as the number of constraints solved by the tree divided by the total number of
        constraints.
        :return float: The fitness of the tree.
        """
        if self.total:
            return self.solved / self.total
        else:
            return 0

    def __copy__(self) -> Fitness:
        return ConstraintFitness(
            solved=self.solved,
            total=self.total,
            success=self.success,
            failing_trees=self.failing_trees[:],
        )

    def __repr__(self):
        return f"ConstraintFitness(solved={self.solved}, total={self.total}, success={self.success})"


class GeneticBase(abc.ABC):
    """
    Abstract class to represent a genetic base.
    """

    def __init__(
        self,
        searches: Optional[dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize the GeneticBase with the given searches, local variables, and global variables.
        :param Optional[dict[str, NonTerminalSearch]] searches: The dictionary of searches.
        :param Optional[dict[str, Any]] local_variables: The dictionary of local variables.
        :param Optional[dict[str, Any]] global_variables: The dictionary of global variables.
        """
        self.searches = searches or dict()
        self.local_variables = local_variables or dict()
        self.global_variables = global_variables or dict()

    def get_access_points(self):
        """
        Get the access points of the genetic base, i.e., the non-terminal that are considered in this genetic base.
        :return list[NonTerminal]: The list of access points.
        """
        return sum(
            [search.get_access_points() for search in self.searches.values()], []
        )

    @abc.abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> Fitness:
        """
        Abstract method to calculate the fitness of the tree.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return Fitness: The fitness of the tree.
        """
        raise NotImplementedError("Fitness function not implemented")

    @staticmethod
    def get_hash(
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ):
        return hash(
            (
                tree,
                tuple((scope or {}).items()),
                tuple(population or []),
                tuple((local_variables or {}).items()),
            )
        )

    def combinations(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
    ):
        """
        Get all possible combinations of trees that satisfy the searches.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :return list[list[tuple[str, DerivationTree]]]: The list of combinations of trees that fill all non-terminals
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        in the genetic base.
        """
        nodes: list[list[tuple[str, Container]]] = []
        for name, search in self.searches.items():
            nodes.append(
                [
                    (name, container)
                    for container in search.find(
                        tree, scope=scope, population=population
                    )
                ]
            )
        return itertools.product(*nodes)

    def check(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Check if the tree satisfies the genetic base.
        :param DerivationTree tree: The tree to check.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return bool: True if the tree satisfies the genetic base, False otherwise.
        """
        return self.fitness(tree, scope, population, local_variables).success

    def get_failing_nodes(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> list[FailingTree]:
        """
        Get the failing nodes of the tree.
        :param DerivationTree tree: The tree to check.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return list[FailingTree]: The list of failing trees
        """
        return self.fitness(tree, scope, population, local_variables).failing_trees

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self.__repr__()
