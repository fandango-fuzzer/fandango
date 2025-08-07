import math
from typing import Any, Optional

from tdigest import TDigest as BaseTDigest

from fandango.constraints.fitness import (
    FailingTree,
    GeneticBase,
    ValueFitness,
)
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import print_exception


class TDigest(BaseTDigest):
    def __init__(self, optimization_goal: str):
        super().__init__()
        self._min = None
        self._max = None
        self.contrast = 200.0
        if optimization_goal == "min":
            self.transform = self.amplify_near_0
        else:
            self.transform = self.amplify_near_1

    def update(self, x, w=1):
        super().update(x, w)
        if self._min is None or x < self._min:
            self._min = x
        if self._max is None or x > self._max:
            self._max = x

    def amplify_near_0(self, q):
        return 1 - math.exp(-self.contrast * q)

    def amplify_near_1(self, q):
        return math.exp(self.contrast * (q - 1))

    def score(self, x):
        if self._min is None or self._max is None:
            return 0
        if self._min == self._max:
            return self.transform(self.cdf(x))
        if x <= self._min:
            return 0
        if x >= self._max:
            return 1
        else:
            return self.transform(self.cdf(x))


class Value(GeneticBase):
    """
    Represents a value that can be used for fitness evaluation.
    In contrast to a constraint, a value is not calculated based on the constraints solved by a tree,
    but rather by a user-defined expression.
    """

    def __init__(self, expression: str, *args, **kwargs):
        """
        Initializes the value with the given expression.
        :param str expression: The expression to evaluate.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.expression = expression
        self.cache: dict[int, ValueFitness] = dict()

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ValueFitness:
        """
        Calculate the fitness of the tree based on the given expression.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ValueFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
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
            for combination in self.combinations(tree, scope, population):
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

    def get_symbols(self):
        """
        Get the placeholders of the constraint.
        """
        return self.searches.values()


class SoftValue(Value):
    """
    A `Value`, which is not mandatory, but aimed to be optimized.
    """

    def __init__(self, optimization_goal: str, expression: str, *args, **kwargs):
        super().__init__(expression, *args, **kwargs)
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
