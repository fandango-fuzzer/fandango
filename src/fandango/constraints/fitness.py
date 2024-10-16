import abc
import enum
import itertools
from typing import List, Optional, Dict, Any, Tuple

from fandango.language.search import NonTerminalSearch
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


class Comparison(enum.Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="


class ComparisonSide(enum.Enum):
    LEFT = "left"
    RIGHT = "right"


class FailingTree:
    def __init__(
        self,
        tree: DerivationTree,
        cause: "GeneticBase",
        suggestions: Optional[List[Tuple[Comparison, Any, ComparisonSide]]] = None,
    ):
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
    def __init__(self, success: bool, failing_trees: List[FailingTree] = None):
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
        self, values: List[float] = None, failing_trees: List[FailingTree] = None
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
        failing_trees: List[FailingTree] = None,
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


class GeneticBase(abc.ABC):
    def __init__(
        self,
        searches: Optional[Dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.searches = searches or dict()
        self.local_variables = local_variables or dict()
        self.global_variables = global_variables or dict()

    def get_access_points(self):
        return sum(
            [search.get_access_points() for search in self.searches.values()], []
        )

    @abc.abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> Fitness:
        raise NotImplementedError("Fitness function not implemented")

    @staticmethod
    def get_hash(
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ):
        return hash((tree, tuple((scope or {}).items())))

    def combinations(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ):
        nodes: List[List[Tuple[str, DerivationTree]]] = []
        for name, search in self.searches.items():
            nodes.append(
                [(name, container) for container in search.find(tree, scope=scope)]
            )
        return itertools.product(*nodes)

    def check(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ):
        return self.fitness(tree, scope).success

    def get_failing_nodes(self, tree: DerivationTree):
        return self.fitness(tree).failing_trees

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self.__repr__()
