import abc
from typing import List

from fandango.language.grammar import DerivationTree


class Fitness(abc.ABC):
    def __init__(self, success: bool, failing_trees: List[DerivationTree] = None):
        self.success = success
        self.failing_trees = failing_trees or []

    @abc.abstractmethod
    def fitness(self) -> float:
        pass

    @abc.abstractmethod
    def __copy__(self) -> "Fitness":
        pass


class ValueFitness(Fitness):
    def __init__(
        self, values: List[float] = None, failing_trees: List[DerivationTree] = None
    ):
        super().__init__(True, failing_trees)
        self.values = values or []

    def fitness(self) -> float:
        if self.values:
            return sum(self.values) / len(self.values)
        else:
            return 0

    def __copy__(self) -> Fitness:
        return ValueFitness(self.values[:])


class ConstraintFitness(Fitness):
    def __init__(
        self,
        solved: int,
        total: int,
        success: bool,
        failing_trees: List[DerivationTree] = None,
    ):
        super().__init__(success, failing_trees)
        self.solved = solved
        self.total = total

    def fitness(self) -> float:
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
