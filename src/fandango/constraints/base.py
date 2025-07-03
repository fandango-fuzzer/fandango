"""
This module contains the base classes for constraints in the fandango library.
"""

import itertools
import math
import random
from abc import ABC, abstractmethod
from copy import copy
from itertools import zip_longest
from typing import Any, Optional

from tdigest import TDigest as BaseTDigest

from fandango.constraints.fitness import (
    BoundsFailingTree,
    Comparison,
    ComparisonSide,
    ConstraintFitness,
    FailingTree,
    GeneticBase,
    ValueFitness,
)
from fandango.errors import FandangoValueError
from fandango.language.grammar import Grammar, Repetition
from fandango.language.search import NonTerminalSearch
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree, index_by_reference
from fandango.logger import LOGGER, print_exception

LEGACY = False


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

    def __str__(self):
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return f"where {representation}"

    def __repr__(self):
        return self.expression


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

    def __repr__(self):
        representation = repr(self.expression)
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return f"SoftValue({self.optimization_goal!r}, {representation})"

    def __str__(self):
        representation = str(self.expression)
        for identifier in self.searches:
            representation = representation.replace(
                identifier, str(self.searches[identifier])
            )

        # noinspection PyUnreachableCode
        match self.optimization_goal:
            case "min":
                return f"minimizing {representation}"
            case "max":
                return f"maximizing {representation}"
            case _:
                return f"{self.optimization_goal} {representation}"


class Constraint(GeneticBase, ABC):
    """
    Abstract class to represent a constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        searches: Optional[dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        """
        Initializes the constraint with the given searches, local variables, and global variables.
        :param Optional[dict[str, NonTerminalSearch]] searches: The searches to use.
        :param Optional[dict[str, Any]] local_variables: The local variables to use.
        :param Optional[dict[str, Any]] global_variables: The global variables to use.
        """
        super().__init__(searches, local_variables, global_variables)
        self.cache: dict[int, ConstraintFitness] = dict()

    @abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Abstract method to calculate the fitness of the tree.
        """
        raise NotImplementedError("Fitness function not implemented")

    @staticmethod
    def is_debug_statement(expression: str) -> bool:
        """
        Determines if the expression is a print statement.
        """
        return expression.startswith("print(")

    @abstractmethod
    def accept(self, visitor):
        """
        Accepts a visitor to traverse the constraint structure.
        """
        pass

    def get_symbols(self):
        """
        Get the placeholders of the constraint.
        """
        return self.searches.values()

    @staticmethod
    def eval(expression: str, global_variables, local_variables):
        """
        Evaluate the tree in the context of local and global variables.
        """
        # LOGGER.debug(f"Evaluating {expression}")
        # for name, value in local_variables.items():
        #     if isinstance(value, DerivationTree):
        #         value = value.value()
        #     LOGGER.debug(f"    {name} = {value!r}")

        result = eval(expression, global_variables, local_variables)

        # res = result
        # if isinstance(res, DerivationTree):
        #     res = res.value()
        # LOGGER.debug(f"Result = {res!r}")

        return result


class ExpressionConstraint(Constraint):
    """
    Represents a python expression constraint that can be used for fitness evaluation.
    """

    def __init__(self, expression: str, *args, **kwargs):
        """
        Initializes the expression constraint with the given expression.
        :param str expression: The expression to evaluate.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.expression = expression

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on whether the given expression evaluates to True.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[str, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Initialize the fitness values
        solved = 0
        total = 0
        failing_trees = []
        # If the tree is None, the fitness is 0
        if tree is None:
            return ConstraintFitness(0, 0, False)
        has_combinations = False
        # Iterate over all combinations of the tree and the scope
        for combination in self.combinations(tree, scope, population):
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_vars = self.local_variables.copy()
            if local_variables:
                local_vars.update(local_variables)
            local_vars.update(
                {name: container.evaluate() for name, container in combination}
            )
            try:
                result = self.eval(self.expression, self.global_variables, local_vars)
                # Commented this out for now, as `None` is a valid result
                # of functions such as `re.match()` -- AZ
                # if result is None:
                #     return ConstraintFitness(1, 1, True)
                if result:
                    solved += 1
                else:
                    # If the expression evaluates to False, add the failing trees to the list
                    for _, container in combination:
                        for node in container.get_trees():
                            if node not in failing_trees:
                                failing_trees.append(node)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self.expression}")

            total += 1
        # If there are no combinations, the fitness is perfect
        if not has_combinations:
            solved += 1
            total += 1
        # Create the fitness object
        fitness = ConstraintFitness(
            solved,
            total,
            solved == total,
            failing_trees=[FailingTree(t, self) for t in failing_trees],
        )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return representation

    def __str__(self):
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, str(self.searches[identifier])
            )
        return representation

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_expression_constraint(self)


class ComparisonConstraint(Constraint):
    """
    Represents a comparison constraint that can be used for fitness evaluation.
    """

    def __init__(self, operator: Comparison, left: str, right: str, *args, **kwargs):
        """
        Initializes the comparison constraint with the given operator, left side, and right side.
        :param Comparison operator: The operator to use.
        :param str left: The left side of the comparison.
        :param str right: The right side of the comparison.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.operator = operator
        self.left = left
        self.right = right
        self.types_checked = False

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given comparison.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Initialize the fitness values
        solved = 0
        total = 0
        failing_trees = []
        has_combinations = False
        # If the tree is None, the fitness is 0
        if tree is None:
            return ConstraintFitness(0, 0, False)
        # Iterate over all combinations of the tree and the scope
        for combination in self.combinations(tree, scope, population):
            total += 1
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_vars = self.local_variables.copy()
            if local_variables:
                local_vars.update(local_variables)
            local_vars.update(
                {name: container.evaluate() for name, container in combination}
            )
            # Evaluate the left and right side of the comparison
            try:
                left = self.eval(self.left, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self.left}")
                continue

            try:
                right = self.eval(self.right, self.global_variables, local_vars)
            except Exception as e:
                print_exception(e, f"Evaluation failed: {self.right}")
                continue

            if not hasattr(self, "types_checked") or not self.types_checked:
                self.types_checked = self.check_type_compatibility(left, right)

            # Initialize the suggestions
            suggestions = []
            is_solved = False
            match self.operator:
                case Comparison.EQUAL:
                    # If the left and right side are equal, the constraint is solved
                    if left == right:
                        is_solved = True
                    else:
                        # If the left and right side are not equal, add suggestions to the list
                        if not self.right.strip().startswith("len("):
                            suggestions.append(
                                (Comparison.EQUAL, left, ComparisonSide.RIGHT)
                            )
                        if not self.left.strip().startswith("len("):
                            suggestions.append(
                                (Comparison.EQUAL, right, ComparisonSide.LEFT)
                            )
                case Comparison.NOT_EQUAL:
                    # If the left and right side are not equal, the constraint is solved
                    if left != right:
                        is_solved = True
                    else:
                        # If the left and right side are equal, add suggestions to the list
                        suggestions.append(
                            (Comparison.NOT_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.NOT_EQUAL, right, ComparisonSide.LEFT)
                        )
                case Comparison.GREATER:
                    # If the left side is greater than the right side, the constraint is solved
                    if left > right:
                        is_solved = True
                    else:
                        # If the left side is not greater than the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.LESS, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.GREATER, right, ComparisonSide.LEFT)
                        )
                case Comparison.GREATER_EQUAL:
                    # If the left side is greater than or equal to the right side, the constraint is solved
                    if left >= right:
                        is_solved = True
                    else:
                        # If the left side is not greater than or equal to the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.LESS_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.GREATER_EQUAL, right, ComparisonSide.LEFT)
                        )
                case Comparison.LESS:
                    # If the left side is less than the right side, the constraint is solved
                    if left < right:
                        is_solved = True
                    else:
                        # If the left side is not less than the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.GREATER, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.LESS, right, ComparisonSide.LEFT)
                        )
                case Comparison.LESS_EQUAL:
                    # If the left side is less than or equal to the right side, the constraint is solved
                    if left <= right:
                        is_solved = True
                    else:
                        # If the left side is not less than or equal to the right side, add suggestions to the list
                        suggestions.append(
                            (Comparison.GREATER_EQUAL, left, ComparisonSide.RIGHT)
                        )
                        suggestions.append(
                            (Comparison.LESS_EQUAL, right, ComparisonSide.LEFT)
                        )
            if is_solved:
                solved += 1
            else:
                # If the comparison is not solved, add the failing trees to the list
                for _, container in combination:
                    for node in container.get_trees():
                        ft = FailingTree(node, self, suggestions=suggestions)
                        # if ft not in failing_trees:
                        # failing_trees.append(ft)
                        failing_trees.append(ft)

        if not has_combinations:
            solved += 1
            total += 1

        # Create the fitness object
        fitness = ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def check_type_compatibility(self, left: Any, right: Any) -> bool:
        """
        Check the types of `left` and `right` are compatible in a comparison.
        Return True iff check was actually performed
        """
        if isinstance(left, DerivationTree):
            left = left.value()
        if isinstance(right, DerivationTree):
            right = right.value()

        if left is None or right is None:
            # Cannot check - value does not exist
            return False

        if isinstance(left, type(right)):
            return True
        if isinstance(left, (bool, int, float)) and isinstance(
            right, (bool, int, float)
        ):
            return True

        LOGGER.warning(
            f"{self}: {self.operator.value!r}: Cannot compare {type(left).__name__!r} and {type(right).__name__!r}"
        )
        return True

    def __repr__(self):
        representation = f"{self.left} {self.operator.value} {self.right}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
            )
        return representation

    def __str__(self):
        representation = f"{self.left!s} {self.operator.value} {self.right!s}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, str(self.searches[identifier])
            )
        return representation

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        return visitor.visit_comparison_constraint(self)


class ConjunctionConstraint(Constraint):
    """
    Represents a conjunction constraint that can be used for fitness evaluation.
    """

    def __init__(
        self, constraints: list[Constraint], *args, lazy: bool = False, **kwargs
    ):
        """
        Initializes the conjunction constraint with the given constraints.
        :param list[Constraint] constraints: The constraints to use.
        :param args: Additional arguments.
        :param bool lazy: If True, the conjunction is lazily evaluated.
        """
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given conjunction.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[str, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            # If the conjunction is lazy, evaluate the constraints one by one and stop if one fails
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope, population, local_variables)
                fitness_values.append(fitness)
                if not fitness.success:
                    break
        else:
            # If the conjunction is not lazy, evaluate all constraints at once
            fitness_values = [
                constraint.fitness(tree, scope, population, local_variables)
                for constraint in self.constraints
            ]
        # Aggregate the fitness values
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = all(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if len(self.constraints) > 1:
            if overall:
                solved += 1
            total += 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " and ".join(repr(c) for c in self.constraints) + ")"

    def __str__(self):
        return "(" + " and ".join(str(c) for c in self.constraints) + ")"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_conjunction_constraint(self)
        if visitor.do_continue(self):
            for constraint in self.constraints:
                constraint.accept(visitor)


class DisjunctionConstraint(Constraint):
    """
    Represents a disjunction constraint that can be used for fitness evaluation.
    """

    def __init__(
        self, constraints: list[Constraint], *args, lazy: bool = False, **kwargs
    ):
        """
        Initializes the disjunction constraint with the given constraints.
        :param list[Constraint] constraints: The constraints to use.
        :param args: Additional arguments.
        :param bool lazy: If True, the disjunction is lazily evaluated.
        """
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given disjunction.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[str, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            # If the disjunction is lazy, evaluate the constraints one by one and stop if one succeeds
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope, population, local_variables)
                fitness_values.append(fitness)
                if fitness.success:
                    break
        else:
            # If the disjunction is not lazy, evaluate all constraints at once
            fitness_values = [
                constraint.fitness(tree, scope, population, local_variables)
                for constraint in self.constraints
            ]
        # Aggregate the fitness values
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = any(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if len(self.constraints) > 1:
            if overall:
                solved = total + 1
            total += 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " or ".join(repr(c) for c in self.constraints) + ")"

    def __str__(self):
        return "(" + " or ".join(str(c) for c in self.constraints) + ")"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_disjunction_constraint(self)
        if visitor.do_continue(self):
            for constraint in self.constraints:
                constraint.accept(visitor)


class ImplicationConstraint(Constraint):
    """
    Represents an implication constraint that can be used for fitness evaluation.
    """

    def __init__(self, antecedent: Constraint, consequent: Constraint, *args, **kwargs):
        """
        Initializes the implication constraint with the given antecedent and consequent.
        :param Constraint antecedent: The antecedent of the implication.
        :param Constraint consequent: The consequent of the implication.
        """
        super().__init__(*args, **kwargs)
        self.antecedent = antecedent
        self.consequent = consequent

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given implication.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[str, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Evaluate the antecedent
        antecedent_fitness = self.antecedent.fitness(
            tree, scope, population, local_variables
        )
        if antecedent_fitness.success:
            # If the antecedent is true, evaluate the consequent
            fitness = copy(
                self.consequent.fitness(tree, scope, population, local_variables)
            )
            fitness.total += 1
            if fitness.success:
                fitness.solved += 1
        else:
            # If the antecedent is false, the fitness is perfect
            fitness = ConstraintFitness(
                1,
                1,
                True,
            )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"({repr(self.antecedent)} -> {repr(self.consequent)})"

    def __str__(self):
        return f"({str(self.antecedent)} -> {str(self.consequent)})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_implication_constraint(self)
        if visitor.do_continue(self):
            self.antecedent.accept(visitor)
            self.consequent.accept(visitor)


class ExistsConstraint(Constraint):
    """
    Represents an exists-constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        statement: Constraint,
        bound: NonTerminal | str,
        search: NonTerminalSearch,
        lazy: bool = False,
        *args,
        **kwargs,
    ):
        """
        Initializes the exists-constraint with the given statement, bound, and search.
        :param Constraint statement: The statement to evaluate.
        :param NonTerminal bound: The bound variable.
        :param NonTerminalSearch search: The search to use.
        :param bool lazy: If True, the exists-constraint is lazily evaluated.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.statement = statement
        self.bound = bound
        self.search = search
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given exists-constraint.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        local_variables = local_variables or dict()
        # Iterate over all containers found by the search
        for container in self.search.quantify(tree, scope=scope, population=population):
            # Update the scope with the bound variable
            if isinstance(self.bound, str):
                local_variables[self.bound] = container.evaluate()
            else:
                scope[self.bound] = container.evaluate()
            # Evaluate the statement
            fitness = self.statement.fitness(tree, scope, population, local_variables)
            # Add the fitness to the list
            fitness_values.append(fitness)
            # If the exists-constraint is lazy and the statement is successful, stop
            if self.lazy and fitness.success:
                break
        # Aggregate the fitness values
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = any(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if overall:
            solved = total + 1
        total += 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        if LEGACY:
            return f"(exists {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"
        else:
            return f"any({repr(self.statement)} for {repr(self.bound)} in {repr(self.search)})"

    def __str__(self):
        if LEGACY:
            return f"(exists {str(self.bound)} in {str(self.search)}: {str(self.statement)})"
        else:
            return f"any({str(self.statement)} for {str(self.bound)} in {str(self.search)})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_exists_constraint(self)
        if visitor.do_continue(self):
            self.statement.accept(visitor)


class ForallConstraint(Constraint):
    """
    Represents a forall constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        statement: Constraint,
        bound: NonTerminal | str,
        search: NonTerminalSearch,
        lazy: bool = False,
        *args,
        **kwargs,
    ):
        """
        Initializes the forall constraint with the given statement, bound, and search.
        :param Constraint statement: The statement to evaluate.
        :param NonTerminal bound: The bound variable.
        :param NonTerminalSearch search: The search to use.
        :param bool lazy: If True, the forall-constraint is lazily evaluated.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.statement = statement
        self.bound = bound
        self.search = search
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given forall constraint.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, population)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        local_variables = local_variables or dict()
        # Iterate over all containers found by the search
        for container in self.search.quantify(tree, scope=scope, population=population):
            # Update the scope with the bound variable
            if isinstance(self.bound, str):
                local_variables[self.bound] = container.evaluate()
            else:
                # If the bound is a NonTerminal, update the scope
                scope[self.bound] = container.evaluate()
            # Evaluate the statement
            fitness = self.statement.fitness(tree, scope, population, local_variables)
            # Add the fitness to the list
            fitness_values.append(fitness)
            # If the forall constraint is lazy and the statement is not successful, stop
            if self.lazy and not fitness.success:
                break
        # Aggregate the fitness values
        solved = sum(fitness.solved for fitness in fitness_values)
        total = sum(fitness.total for fitness in fitness_values)
        overall = all(fitness.success for fitness in fitness_values)
        failing_trees = list(
            itertools.chain.from_iterable(
                fitness.failing_trees for fitness in fitness_values
            )
        )
        if overall:
            solved = total + 1
        total += 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        if LEGACY:
            return f"forall {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"
        else:
            return f"all({repr(self.statement)}) for {repr(self.bound)} in {repr(self.search)})"

    def __str__(self):
        if LEGACY:
            return f"forall {str(self.bound)} in {str(self.search)}: {str(self.statement)})"
        else:
            return f"all({str(self.statement)}) for {str(self.bound)} in {str(self.search)})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_forall_constraint(self)
        if visitor.do_continue(self):
            self.statement.accept(visitor)


class RepetitionBoundsConstraint(Constraint):
    """
    Represents a constraint that checks the number of repetitions of a certain pattern in a tree.
    This is useful for ensuring that certain patterns do not occur too frequently or too infrequently.
    """

    def __init__(
        self,
        repetition_id: str,
        expr_data_min: tuple[str, list, dict],
        expr_data_max: tuple[str, list, dict],
        repetition_node: Repetition,
        *args,
        **kwargs,
    ):
        """
        Initializes the repetition bounds constraint with the given pattern and repetition bounds.
        :param NonTerminalSearch pattern: The pattern to check for repetitions.
        :param int min_reps: The minimum number of repetitions allowed.
        :param int max_reps: The maximum number of repetitions allowed.
        :param args: Additional arguments.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.repetition_id = repetition_id
        self.expr_data_min = expr_data_min
        self.expr_data_max = expr_data_max
        self.search_min: Optional[NonTerminalSearch] = None
        self.search_max: Optional[NonTerminalSearch] = None
        if len(expr_data_min[1]) == 0:
            self.search_min = None
        elif len(expr_data_min[1]) == 1:
            self.search_min = expr_data_min[1][0]
        else:
            raise FandangoValueError(
                "RepetitionBoundsConstraint requires exactly one or zero searches for expr_data_max bound"
            )

        if len(expr_data_max[1]) == 0:
            self.search_max = None
        elif len(expr_data_max[1]) == 1:
            self.search_max = expr_data_max[1][0]
        else:
            raise FandangoValueError(
                "RepetitionBoundsConstraint requires exactly one or zero searches for expr_data_max bound"
            )
        self.repetition_node = repetition_node

    def _compute_rep_bound(
        self, tree_rightmost_relevant_node: "DerivationTree", expr_data
    ):
        expr, _, searches = expr_data
        local_cpy = self.local_variables.copy()

        if len(searches) == 0:
            return eval(expr, self.global_variables, local_cpy)

        nodes = []
        if len(searches) != 1:
            raise FandangoValueError(
                "Computed repetition requires exactly one or zero searches"
            )

        search_name, search = next(iter(searches.items()))
        max_path = tree_rightmost_relevant_node.get_choices_path()
        for container in search.find(tree_rightmost_relevant_node.get_root()):
            container_tree: DerivationTree = container.evaluate()
            search_in_bounds = True
            zip_var = list(zip_longest(max_path, container_tree.get_choices_path()))
            for i, (max_step, search_step) in enumerate(zip_var):
                if max_step is None:
                    break
                if search_step is None:
                    break
                if max_step.index > search_step.index:
                    break
                if max_step.index < search_step.index:
                    search_in_bounds = False
                    break
            if not search_in_bounds:
                continue
            nodes.append(container_tree)

        if len(nodes) == 0:
            raise FandangoValueError(
                f"Couldn't find search target ({search}) in prefixed DerivationTree for computed repetition"
            )

        target = nodes[-1]
        local_cpy[search_name] = target
        return eval(expr, self.global_variables, local_cpy), target

    def min(self, tree_stop_before: DerivationTree):
        return self._compute_rep_bound(tree_stop_before, self.expr_data_min)

    def max(self, tree_stop_before: DerivationTree):
        return self._compute_rep_bound(tree_stop_before, self.expr_data_max)

    def group_by_repetition_id(
        self, id_trees: list[DerivationTree]
    ) -> dict[tuple[str, int], dict[int, list[DerivationTree]]]:
        reference_trees: dict[tuple[str, int], dict[int, list[DerivationTree]]] = {}
        for id_tree in id_trees:
            iteration_ids: list[tuple[str, int, int]] = list(
                filter(lambda x: x[0] == self.repetition_id, id_tree.origin_repetitions)
            )
            for i_id in iteration_ids:
                call_id = tuple[str, int](i_id[:2])
                rep_round = i_id[2]
                # Group by id and repetition round

                if call_id not in reference_trees:
                    reference_trees[call_id] = dict()
                iter_list = reference_trees[call_id]
                if rep_round not in iter_list:
                    iter_list[rep_round] = []
                iter_list[rep_round].append(id_tree)
        return reference_trees

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the number of repetitions of the pattern.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :param Optional[list[DerivationTree]] population: The population of trees.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        id_trees = tree.find_by_origin(self.repetition_id)
        if len(id_trees) == 0:
            # Assume that the field containing the nr of repetitions is zero.
            # This is the case where we might have deleted all repetitions from the tree.
            return ConstraintFitness(1, 1, True)

        reference_trees = self.group_by_repetition_id(id_trees)
        failing_trees: list[FailingTree] = []
        solved = 0
        total = len(reference_trees.keys())

        for call_id in reference_trees.keys():
            iter_list = reference_trees[call_id]
            smallest_rep = min(iter_list.keys())
            highest_rep = max(iter_list.keys())
            first_iteration = iter_list[smallest_rep][0]
            last_iteration = iter_list[highest_rep][-1]

            max_bounds_search = first_iteration
            assert max_bounds_search.parent is not None
            while (
                index_by_reference(max_bounds_search.parent.children, max_bounds_search)
                == 0
            ):
                max_bounds_search = max_bounds_search.parent
                assert max_bounds_search.parent is not None

            parent = max_bounds_search.parent
            assert parent is not None
            index = index_by_reference(parent.children, max_bounds_search)
            assert (
                index is not None and index > 0
            ), "Invalid child index for bounds search"
            max_bounds_search = parent.children[index - 1]

            bound_min, min_ref_tree = self.min(max_bounds_search)
            bound_max, max_ref_tree = self.max(max_bounds_search)
            bound_len = len(iter_list)

            if bound_min <= bound_len <= bound_max:
                solved += 1
            else:
                iter_id = call_id[1]
                suggestions: list[tuple[Comparison, Any, ComparisonSide]] = []
                goal_len = random.randint(bound_min, bound_max)
                suggestions.append(
                    (
                        Comparison.EQUAL,
                        (iter_id, bound_len, goal_len),
                        ComparisonSide.RIGHT,
                    )
                )
                suggestions.append(
                    (
                        Comparison.EQUAL,
                        (iter_id, bound_len, goal_len),
                        ComparisonSide.LEFT,
                    )
                )
                assert first_iteration.parent is not None
                failing_trees.append(
                    BoundsFailingTree(
                        first_iteration.parent,
                        first_iteration,
                        last_iteration,
                        min_ref_tree,
                        max_ref_tree,
                        self,
                        suggestions=suggestions,
                    )
                )

        return ConstraintFitness(
            solved, total, solved == total, failing_trees=failing_trees
        )

    def get_first_common_node(
        self, tree_a: DerivationTree, tree_b: DerivationTree
    ) -> DerivationTree:
        common_node = tree_a.get_root(True)
        for a_path, b_path in zip(tree_a.get_choices_path(), tree_b.get_choices_path()):
            if a_path.index == b_path.index:
                common_node = common_node.children[a_path.index]
            else:
                break
        return common_node

    def fix_individual(
        self,
        grammar: Grammar,
        failing_tree: BoundsFailingTree,
        allow_repetition_full_delete: bool,
    ) -> list[tuple[DerivationTree, DerivationTree]]:
        if failing_tree.tree.read_only:
            return []
        replacements: list[tuple[DerivationTree, DerivationTree]] = list()
        for operator, value, side in failing_tree.suggestions:
            if operator == Comparison.EQUAL and side == ComparisonSide.LEFT:
                iter_id, bound_len, goal_len = value
                if goal_len > bound_len:
                    replacements.append(
                        self.insert_repetitions(
                            nr_to_insert=goal_len - bound_len,
                            rep_iteration=iter_id,
                            grammar=grammar,
                            tree=failing_tree.tree,
                            end_rep=failing_tree.ending_rep_tree,
                        )
                    )
                else:
                    if goal_len == 0 and not allow_repetition_full_delete:
                        if not allow_repetition_full_delete:
                            goal_len = 1
                    if goal_len == bound_len:
                        continue
                    delete_replace_pair = self.delete_repetitions(
                        nr_to_delete=bound_len - goal_len,
                        rep_iteration=iter_id,
                        tree=failing_tree.tree,
                    )
                    if goal_len == 0:
                        delete_replacement: DerivationTree = delete_replace_pair[1]
                        node_a = self.get_first_common_node(
                            failing_tree.tree, failing_tree.starting_rep_value
                        )
                        node_b = self.get_first_common_node(
                            failing_tree.tree, failing_tree.ending_rep_value
                        )
                        node_c = self.get_first_common_node(
                            failing_tree.starting_rep_value,
                            failing_tree.ending_rep_value,
                        )
                        # Get the node that is closest to root
                        first_node = sorted(
                            [node_a, node_b, node_c], key=lambda x: len(x.get_path())
                        )[0]
                        replacement = first_node.deepcopy(
                            copy_children=True, copy_params=False, copy_parent=False
                        )
                        replacement = replacement.replace_multiple(
                            grammar=grammar,
                            replacements=[(failing_tree.tree, delete_replacement)],
                            current_path=first_node.get_choices_path(),
                        )

                        read_only_start_idx = len(first_node.get_path()) - 1
                        current_node = replacement
                        for path_node in failing_tree.tree.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node = replacement
                        for (
                            path_node
                        ) in failing_tree.starting_rep_value.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node.set_all_read_only(True)
                        current_node = replacement
                        for (
                            path_node
                        ) in failing_tree.ending_rep_value.get_choices_path()[
                            read_only_start_idx:
                        ]:
                            current_node = current_node.children[path_node.index]
                            current_node.read_only = True
                        current_node.set_all_read_only(True)
                        replacements.append((first_node, replacement))
                    else:
                        replacements.append(delete_replace_pair)
                continue
        return replacements

    def insert_repetitions(
        self,
        *,
        nr_to_insert: int,
        rep_iteration: int,
        grammar: "Grammar",
        tree: DerivationTree,
        end_rep: DerivationTree,
    ) -> tuple[DerivationTree, DerivationTree]:
        assert end_rep.parent is not None, "end_rep must have a parent"
        index = index_by_reference(end_rep.parent, end_rep)
        if index is None:
            raise ValueError("end_rep not found in its parent's children")
        insertion_index = index + 1

        starting_rep = 0
        for ref in end_rep.origin_repetitions:
            if ref[0] == self.repetition_id and ref[1] == rep_iteration:
                assert ref[2] is not None, "repetition index (ref[2]) must not be None"
                starting_rep = ref[2] + 1

        old_tree_children = tree.children
        tree.set_children([])

        self.repetition_node.fuzz(
            tree,
            grammar,
            override_starting_repetition=starting_rep,
            override_current_iteration=rep_iteration,
            override_iterations_to_perform=starting_rep + nr_to_insert,
        )

        insert_children = tree.children
        tree.set_children(old_tree_children)

        copy_parent = tree.deepcopy(
            copy_children=True,
            copy_parent=False,
            copy_params=False,
        )
        copy_parent.set_children(
            copy_parent.children[:insertion_index]
            + insert_children
            + copy_parent.children[insertion_index:]
        )

        return tree, copy_parent

    def delete_repetitions(
        self, *, nr_to_delete: int, rep_iteration: int, tree: DerivationTree
    ) -> tuple[DerivationTree, DerivationTree]:
        copy_parent = tree.deepcopy(
            copy_children=True, copy_parent=False, copy_params=False
        )
        curr_rep_id = None
        reps_deleted = 0
        new_children: list[DerivationTree] = []
        for child in copy_parent.children[::-1]:
            repetition_node_id = self.repetition_id
            matching_o_nodes = list(
                filter(
                    lambda x: x[0] == repetition_node_id and x[1] == rep_iteration,
                    child.origin_repetitions,
                )
            )
            if len(matching_o_nodes) == 0:
                new_children.insert(0, child)
                continue
            matching_o_node = matching_o_nodes[0]
            rep_id = matching_o_node[2]
            if curr_rep_id != rep_id and reps_deleted >= nr_to_delete:
                # We have deleted enough repetitions iteratively add all remaining children
                new_children.insert(0, child)
                continue
            curr_rep_id = rep_id
            reps_deleted += 1
        copy_parent.set_children(new_children)
        return tree, copy_parent

    def __repr__(self):
        if self.search_min is None:
            print_min, _, _ = self.expr_data_min
        else:
            print_min = str(self.search_min)
        if self.search_max is None:
            print_max, _, _ = self.expr_data_max
        else:
            print_max = str(self.search_max)
        return f"RepetitionBounds({print_min} <= |{repr(self.repetition_node.node)}| <= {print_max})"

    def __str__(self):
        return repr(self)

    def accept(self, visitor: "ConstraintVisitor"):
        """Accepts a visitor to traverse the constraint structure."""
        visitor.visit_repetition_bounds_constraint(self)


class ConstraintVisitor:
    """
    A base class for visiting and processing different types of constraints.

    This class uses the visitor pattern to traverse constraint structures. Each method
    corresponds to a specific type of constraint, allowing implementations to define
    custom behavior for processing or interacting with that type.
    """

    def __init__(self):
        pass

    def do_continue(self, constraint: "Constraint") -> bool:
        """If this returns False, this formula should not call the visit methods for
        its children."""
        return True

    def visit(self, constraint: "Constraint"):
        """Visits a constraint."""
        return constraint.accept(self)

    def visit_expression_constraint(self, constraint: "ExpressionConstraint"):
        """Visits an expression constraint."""
        pass

    def visit_comparison_constraint(self, constraint: "ComparisonConstraint"):
        """Visits a comparison constraint."""
        pass

    def visit_forall_constraint(self, constraint: "ForallConstraint"):
        """Visits a forall constraint."""
        pass

    def visit_exists_constraint(self, constraint: "ExistsConstraint"):
        """Visits an exists constraint."""
        pass

    def visit_disjunction_constraint(self, constraint: "DisjunctionConstraint"):
        """Visits a disjunction constraint."""
        pass

    def visit_conjunction_constraint(self, constraint: "ConjunctionConstraint"):
        """Visits a conjunction constraint."""
        pass

    def visit_implication_constraint(self, constraint: "ImplicationConstraint"):
        """Visits an implication constraint."""
        pass

    def visit_repetition_bounds_constraint(
        self, constraint: "RepetitionBoundsConstraint"
    ):
        """Visits a repetition bounds constraint."""
        pass
