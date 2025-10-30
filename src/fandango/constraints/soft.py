from collections.abc import Callable, Collection
import math
from typing import Any, Optional

from tdigest.tdigest import TDigest as BaseTDigest

from fandango.constraints.failing_tree import FailingTree
from fandango.constraints.fitness import ValueFitness
from fandango.constraints.base import GeneticBase
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import print_exception


class TDigest(BaseTDigest):
    def __init__(self, optimization_goal: str):
        super().__init__()  # type: ignore[no-untyped-call] # TDigest is not typed
        self._min: Optional[float] = None
        self._max: Optional[float] = None
        self.contrast = 200.0
        self.transform: Callable[[float], float] = (
            self.amplify_near_0 if optimization_goal == "min" else self.amplify_near_1
        )

    def update(self, x: float, w: int = 1) -> None:
        super().update(x, w)  # type: ignore[no-untyped-call] # TDigest is not typed
        if self._min is None or x < self._min:
            self._min = x
        if self._max is None or x > self._max:
            self._max = x

    def amplify_near_0(self, q: float | int) -> float:
        return 1 - math.exp(-self.contrast * q)

    def amplify_near_1(self, q: float | int) -> float:
        return math.exp(self.contrast * (q - 1))

    def score(self, x: float | int) -> float | int:
        if self._min is None or self._max is None:
            return 0
        if self._min == self._max:
            cdf = self.cdf(x)  # type: ignore[no-untyped-call] # TDigest is not typed
            return self.transform(cdf)
        if x <= self._min:
            return 0
        if x >= self._max:
            return 1
        else:
            cdf = self.cdf(x)  # type: ignore[no-untyped-call] # TDigest is not typed
            return self.transform(cdf)


class Value(GeneticBase):
    """
    Represents a value that can be used for fitness evaluation.
    In contrast to a constraint, a value is not calculated based on the constraints solved by a tree,
    but rather by a user-defined expression.
    """

    def __init__(
        self,
        expression: str,
        searches: Optional[dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Initializes the value with the given expression.
        :param str expression: The expression to evaluate.
        :param dict[str, NonTerminalSearch] searches: The searches to use.
        :param dict[str, Any] local_variables: The local variables to use.
        :param dict[str, Any] global_variables: The global variables to use.
        """
        super().__init__(
            searches=searches,
            local_variables=local_variables,
            global_variables=global_variables,
        )
        self.expression = expression
        self.cache: dict[int, ValueFitness] = dict()

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ValueFitness:
        """
        Calculate the fitness of the tree based on the given expression.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ValueFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return self.cache[tree_hash]
        # If the tree is None, the fitness is 0
        if tree is None:
            fitness = ValueFitness()
        else:
            trees = []
            values = []
            # Iterate over all combinations of the tree and the scope
            for combination in self.combinations(tree, scope):
                # Update the local variables to initialize the placeholders with the values of the combination
                local_vars = self.local_variables.copy()
                if local_variables:
                    local_vars.update(local_variables)
                local_vars.update(
                    {name: container.evaluate() for name, container in combination}
                )
                for _, container in combination:
                    for node in container.get_trees():
                        if node not in trees:
                            trees.append(node)
                try:
                    # Evaluate the expression
                    result = eval(self.expression, self.global_variables, local_vars)
                    values.append(result)
                except Exception as e:
                    print_exception(e, f"Evaluation failed: {self.expression}")
                    values.append(0)
            # Create the fitness object
            fitness = ValueFitness(
                values, failing_trees=[FailingTree(t, self) for t in trees]
            )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def get_symbols(self) -> Collection[NonTerminalSearch]:
        """
        Get the placeholders of the constraint.
        """
        return self.searches.values()


class SoftValue(Value):
    """
    A `Value`, which is not mandatory, but aimed to be optimized.
    """

    def __init__(
        self,
        optimization_goal: str,
        expression: str,
        searches: Optional[dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        super().__init__(
            expression,
            searches=searches,
            local_variables=local_variables,
            global_variables=global_variables,
        )
        assert optimization_goal in (
            "min",
            "max",
        ), f"Invalid SoftValue optimization goal {type!r}"
        self.optimization_goal = optimization_goal
        self.tdigest = TDigest(optimization_goal)

    def format_as_spec(self) -> str:
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, self.searches[identifier].format_as_spec()
            )

        # noinspection PyUnreachableCode
        match self.optimization_goal:
            case "min":
                return f"minimizing {representation}"
            case "max":
                return f"maximizing {representation}"
            case _:
                return f"{self.optimization_goal} {representation}"
