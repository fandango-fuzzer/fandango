import abc
import copy
from typing import Optional
from fandango.constraints.failing_tree import FailingTree, Suggestion


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

    def __repr__(self) -> str:
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
        values: Optional[list[float | int]] = None,
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

    def __repr__(self) -> str:
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
        suggestion: Suggestion,
        failing_trees: list[FailingTree] = [],
    ):
        """
        Initialize the ConstraintFitness with the given solved, total, success, and failing trees.
        :param int solved: The number of constraints solved by the tree.
        :param int total: The total number of constraints.
        :param bool success: The success of the fitness.
        :param list[FailingTree] failing_trees: The list of failing trees.
        :param Optional[Suggestion] suggestion: The suggestion to fix the failing trees.
        """
        super().__init__(success, failing_trees)
        self.suggestion = suggestion
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
            suggestion=copy.deepcopy(self.suggestion),
        )

    def __repr__(self) -> str:
        return f"ConstraintFitness(solved={self.solved}, total={self.total}, success={self.success})"


class DistanceAwareConstraintFitness(ConstraintFitness):
    """
    Class to represent the fitness of a tree based on distance-aware constraints.
    The fitness is calculated as the average of the values.
    """

    def __init__(
        self,
        values: list[float],
        suggestion: Suggestion,
        success: bool = True,
        failing_trees: list[FailingTree] = [],
    ):
        super().__init__(
            solved=sum(1 for it in values if it == 1.0),
            total=len(values),
            success=success,
            suggestion=suggestion,
            failing_trees=failing_trees,
        )
        self.values = values

    def fitness(self) -> float:
        """
        Calculates the fitness of the tree based on the values.
        This is the same as `ValueFitness`.
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
        return DistanceAwareConstraintFitness(
            values=self.values[:],
            suggestion=self.suggestion,
            success=self.success,
            failing_trees=self.failing_trees,
        )

    def __repr__(self) -> str:
        return f"DistanceAwareConstraintFitness(values={self.values})"
