import abc
import itertools
from copy import copy
from typing import List, Dict, Any, Optional

from fandango.constraints.fitness import (
    ConstraintFitness,
    ValueFitness,
    GeneticBase,
    FailingTree,
    Comparison,
    ComparisonSide,
)
from fandango.language.search import NonTerminalSearch
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


class Value(GeneticBase):
    def __init__(self, expression: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expression = expression
        self.cache: Dict[int, ValueFitness] = dict()

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ValueFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if tree is None:
            fitness = ValueFitness()
        else:
            trees = []
            values = []
            for combination in self.combinations(tree, scope):
                local_variables = self.local_variables.copy()
                local_variables.update({name: node for name, node in combination})
                for _, node in combination:
                    if node not in trees:
                        trees.append(FailingTree(node, self))
                try:
                    values.append(
                        eval(self.expression, self.global_variables, local_variables)
                    )
                except:
                    values.append(0)
            fitness = ValueFitness(values, failing_trees=trees)
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return f"fitness {representation}"


class Constraint(GeneticBase, abc.ABC):
    def __init__(
        self,
        searches: Optional[Dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(searches, local_variables, global_variables)
        self.cache: Dict[int, ConstraintFitness] = dict()

    @abc.abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ConstraintFitness:
        raise NotImplementedError("Fitness function not implemented")


class ExpressionConstraint(Constraint):
    def __init__(self, expression: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expression = expression

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        solved = 0
        total = 0
        failing_trees = []
        if tree is None:
            return ConstraintFitness(0, 0, False)
        has_combinations = False
        for combination in self.combinations(tree, scope):
            has_combinations = True
            local_variables = self.local_variables.copy()
            local_variables.update({name: node for name, node in combination})
            try:
                if eval(self.expression, self.global_variables, local_variables):
                    solved += 1
                else:
                    for _, node in combination:
                        if node not in failing_trees:
                            failing_trees.append(FailingTree(node, self))
            except:
                pass
            total += 1
        if not has_combinations:
            solved += 1
            total += 1
        fitness = ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return representation


class ComparisonConstraint(Constraint):
    def __init__(self, operator: Comparison, left: str, right: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operator = operator
        self.left = left
        self.right = right

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        solved = 0
        total = 0
        failing_trees = []
        has_combinations = False
        for combination in self.combinations(tree, scope):
            has_combinations = True
            local_variables = self.local_variables.copy()
            local_variables.update({name: node for name, node in combination})
            try:
                left = eval(self.left, self.global_variables, local_variables)
                right = eval(self.right, self.global_variables, local_variables)
                suggestions = []
                is_solved = False
                match self.operator:
                    case Comparison.EQUAL:
                        if left == right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.EQUAL, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.EQUAL, right, ComparisonSide.LEFT)
                            )
                    case Comparison.NOT_EQUAL:
                        if left != right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.NOT_EQUAL, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.NOT_EQUAL, right, ComparisonSide.LEFT)
                            )
                    case Comparison.GREATER:
                        if left > right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.LESS, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.GREATER, right, ComparisonSide.LEFT)
                            )
                    case Comparison.GREATER_EQUAL:
                        if left >= right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.LESS_EQUAL, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.GREATER_EQUAL, right, ComparisonSide.LEFT)
                            )
                    case Comparison.LESS:
                        if left < right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.GREATER, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.LESS, right, ComparisonSide.LEFT)
                            )
                    case Comparison.LESS_EQUAL:
                        if left <= right:
                            is_solved = True
                        else:
                            suggestions.append(
                                (Comparison.GREATER_EQUAL, left, ComparisonSide.RIGHT)
                            )
                            suggestions.append(
                                (Comparison.LESS_EQUAL, right, ComparisonSide.LEFT)
                            )
                if is_solved:
                    solved += 1
                else:
                    for _, node in combination:
                        if node not in failing_trees:
                            failing_trees.append(
                                FailingTree(node, self, suggestions=suggestions)
                            )
            except:
                pass
            total += 1
        if not has_combinations:
            solved += 1
            total += 1
        fitness = ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        representation = f"{self.left} {self.operator.value} {self.right}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return representation


class ConjunctionConstraint(Constraint):
    def __init__(
        self, constraints: List[Constraint], *args, lazy: bool = False, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope)
                fitness_values.append(fitness)
                if not fitness.success:
                    break
        else:
            fitness_values = [
                constraint.fitness(tree, scope) for constraint in self.constraints
            ]
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = all(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if len(self.constraints) > 1:
            total += 1
            if overall:
                solved += 1
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " and ".join(repr(c) for c in self.constraints) + ")"


class DisjunctionConstraint(Constraint):
    def __init__(
        self, constraints: List[Constraint], *args, lazy: bool = False, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope)
                fitness_values.append(fitness)
                if fitness.success:
                    break
        else:
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
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " or ".join(repr(c) for c in self.constraints) + ")"


class ImplicationConstraint(Constraint):
    def __init__(self, antecedent: Constraint, consequent: Constraint, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.antecedent = antecedent
        self.consequent = consequent

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        antecedent_fitness = self.antecedent.fitness(tree, scope)
        if antecedent_fitness.success:
            fitness = copy(self.consequent.fitness(tree, scope))
            if fitness.success:
                fitness.solved += 1
            fitness.total += 1
        else:
            fitness = ConstraintFitness(
                1,
                1,
                True,
            )
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"({repr(self.antecedent)} -> {repr(self.consequent)})"


class ExistsConstraint(Constraint):
    def __init__(
        self,
        statement: Constraint,
        bound: NonTerminal,
        search: NonTerminalSearch,
        *args,
        lazy: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.statement = statement
        self.bound = bound
        self.search = search
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        for dt in self.search.find(tree, scope=scope):
            scope[self.bound] = dt
            fitness = self.statement.fitness(tree, scope)
            fitness_values.append(fitness)
            if self.lazy and fitness.success:
                break
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = any(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        total += 1
        if overall:
            solved = total + 1
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"(exists {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"


class ForallConstraint(Constraint):
    def __init__(
        self,
        statement: Constraint,
        bound: NonTerminal,
        search: NonTerminalSearch,
        *args,
        lazy: bool = False,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.statement = statement
        self.bound = bound
        self.search = search
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ConstraintFitness:
        tree_hash = self.get_hash(tree, scope)
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        for dt in self.search.find(tree, scope=scope):
            scope[self.bound] = dt
            fitness = self.statement.fitness(tree, scope)
            fitness_values.append(fitness)
            if self.lazy and not fitness.success:
                break
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = all(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        total += 1
        if overall:
            solved = total + 1
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"(forall {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"
