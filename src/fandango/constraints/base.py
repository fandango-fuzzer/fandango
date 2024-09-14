import abc
import enum
import itertools
from typing import Tuple, List, Dict, Any, Optional

from fandango.language.grammar import DerivationTree
from fandango.language.search import NonTerminalSearch


class Fitness:
    def __init__(
        self,
        solved: int,
        total: int,
        success: bool,
        failing_trees: List[DerivationTree] = None,
    ):
        self.solved = solved
        self.total = total
        self.success = success
        self.failing_trees = failing_trees or []

    def fitness(self):
        return self.solved / self.total


class Constraint(abc.ABC):
    def __init__(
        self,
        searches: Dict[str, NonTerminalSearch],
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.searches = searches
        self.local_variables = local_variables or dict()
        self.global_variables = global_variables or dict()

    @abc.abstractmethod
    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        raise NotImplementedError("Fitness function not implemented")

    def combinations(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[str, DerivationTree]] = None,
    ):
        nodes: List[List[Tuple[str, DerivationTree]]] = []
        for name, search in self.searches.items():
            nodes.append([(name, node) for node in search.find_all(trees, scope=scope)])
        return itertools.product(*nodes)

    def check(self, tree: DerivationTree):
        return self.fitness(tree).success

    def get_failing_nodes(self, tree: DerivationTree):
        return self.fitness(tree).failing_trees


class ExpressionConstraint(Constraint):
    def __init__(self, expression: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expression = expression

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        solved = 0
        total = 0
        failing_trees = []
        if tree is None:
            return Fitness(0, 0, False)
        for combination in self.combinations(tree.children, scope):
            local_variables = self.local_variables.copy()
            local_variables.update({name: str(node) for name, node in combination})
            try:
                if eval(self.expression, self.global_variables, local_variables):
                    solved += 1
                else:
                    for _, node in combination:
                        if node not in failing_trees:
                            failing_trees.append(node)
            except:
                pass
            total += 1
        return Fitness(solved, total, solved == total, failing_trees=failing_trees)


class Comparison(enum.Enum):
    EQUAL = "=="
    NOT_EQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="


class ComparisonConstraint(Constraint):
    def __init__(self, operator: Comparison, left: str, right: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operator = operator
        self.left = left
        self.right = right

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        solved = 0
        total = 0
        failing_trees = []
        for combination in self.combinations(tree.children, scope):
            local_variables = self.local_variables.copy()
            local_variables.update({name: str(node) for name, node in combination})
            try:
                left = eval(self.left, self.global_variables, local_variables)
                right = eval(self.right, self.global_variables, local_variables)
                is_solved = False
                match self.operator:
                    case Comparison.EQUAL:
                        if left == right:
                            is_solved = True
                    case Comparison.NOT_EQUAL:
                        if left != right:
                            is_solved = True
                    case Comparison.GREATER:
                        if left > right:
                            is_solved = True
                    case Comparison.GREATER_EQUAL:
                        if left >= right:
                            is_solved = True
                    case Comparison.LESS:
                        if left < right:
                            is_solved = True
                    case Comparison.LESS_EQUAL:
                        if left <= right:
                            is_solved = True
                if is_solved:
                    solved += 1
                else:
                    for _, node in combination:
                        if node not in failing_trees:
                            failing_trees.append(node)
            except:
                pass
            total += 1
        return Fitness(solved, total, solved == total, failing_trees=failing_trees)


class ConjunctionConstraint(Constraint):
    def __init__(self, constraints: List[Constraint], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constraints = constraints

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        fitness_values = [
            constraint.fitness(tree, scope) for constraint in self.constraints
        ]
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = any(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if len(self.constraints) > 1:
            total += 1
            if overall:
                solved += 1
        return Fitness(
            solved,
            total,
            overall,
            failing_trees=failing_trees,
        )


class DisjunctionConstraint(Constraint):
    def __init__(self, constraints: List[Constraint], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constraints = constraints

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        fitness_values = [
            constraint.fitness(tree, scope) for constraint in self.constraints
        ]
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = any(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if len(self.constraints) > 1:
            total += 1
            if overall:
                solved = total + 1
        return Fitness(
            solved,
            total,
            overall,
            failing_trees=failing_trees,
        )



"""
Don't have them
class NotConstraint(Constraint):
    def __init__(self, constraint: Constraint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.constraint = constraint
        
    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> Fitness:
        fitness = self.constraint.fitness(tree, scope)
        return Fitness(
            fitness.total - fitness.solved,
            fitness.total,
            not fitness.success,
        )
"""
