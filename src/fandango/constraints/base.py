"""
This module contains the base classes for constraints in the fandango library.
"""

import itertools
from abc import ABC, abstractmethod
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
from fandango.logger import print_exception


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
        self.cache: Dict[int, ValueFitness] = dict()

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ValueFitness:
        """
        Calculate the fitness of the tree based on the given expression.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :return ValueFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # If the tree is None, the fitness is 0
        if tree is None:
            fitness = ValueFitness()
        else:
            trees = []
            values = []
            # Iterate over all combinations of the tree and the scope
            for combination in self.combinations(tree, scope):
                # Update the local variables to initialize the placeholders with the values of the combination
                local_variables = self.local_variables.copy()
                local_variables.update(
                    {name: container.evaluate() for name, container in combination}
                )
                for _, container in combination:
                    for node in container.get_trees():
                        if node not in trees:
                            trees.append(node)
                try:
                    # Evaluate the expression
                    values.append(
                        eval(self.expression, self.global_variables, local_variables)
                    )
                except Exception as e:
                    e.add_note("Evaluation failed: " + self.expression)
                    print_exception(e)
                    values.append(0)
            # Create the fitness object
            fitness = ValueFitness(
                values, failing_trees=[FailingTree(t, self) for t in trees]
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
        return f"fitness {representation}"


class Constraint(GeneticBase, ABC):
    """
    Abstract class to represents a constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        searches: Optional[Dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes the constraint with the given searches, local variables, and global variables.
        :param Optional[Dict[str, NonTerminalSearch]] searches: The searches to use.
        :param Optional[Dict[str, Any]] local_variables: The local variables to use.
        :param Optional[Dict[str, Any]] global_variables: The global variables to use.
        """
        super().__init__(searches, local_variables, global_variables)
        self.cache: Dict[int, ConstraintFitness] = dict()

    @abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
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
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on whether the given expression evaluates to True.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[str, DerivationTree]] scope: The scope of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
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
        for combination in self.combinations(tree, scope):
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_variables = self.local_variables.copy()
            local_variables.update(
                {name: container.evaluate() for name, container in combination}
            )
            try:
                result = eval(self.expression, self.global_variables, local_variables)
                if result is None:
                    # fitness is perfect and return
                    # TODO this should not be here. It breaks Python's None semantics
                    return ConstraintFitness(1, 1, True)
                if result:
                    solved += 1
                else:
                    # If the expression evaluates to False, add the failing trees to the list
                    for _, container in combination:
                        for node in container.get_trees():
                            if node not in failing_trees:
                                failing_trees.append(node)
            except Exception as e:
                e.add_note("Evaluation failed: " + self.expression)
                print_exception(e)

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
        self.types_checked = None

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given comparison.
        """
        tree_hash = self.get_hash(tree, scope)
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
        for combination in self.combinations(tree, scope):
            has_combinations = True
            # Update the local variables to initialize the placeholders with the values of the combination
            local_variables = self.local_variables.copy()
            local_variables.update(
                {name: container.evaluate() for name, container in combination}
            )
            # Evaluate the left and right side of the comparison
            try:
                left = eval(self.left, self.global_variables, local_variables)
            except Exception as e:
                e.add_note("Evaluation failed: " + self.left)
                print_exception(e)
                continue
            # Evaluate the left and right side of the comparison
            try:
                right = eval(self.right, self.global_variables, local_variables)
            except Exception as e:
                e.add_note("Evaluation failed: " + self.right)
                print_exception(e)
                continue

            try:
                # TODO: please remove this check. It breaks Python's functionality, e.g., for comparing floats and ints
                # TODO: Just because the types are different doesn't mean they can't be compared
                if self.types_checked is None:
                    if not type(left) == type(right):
                        raise TypeError(
                            f"In constraint {self}, left and right side of comparison don't evaluate to the same type"
                        )
                    else:
                        self.types_checked = True
            except Exception as e:
                self.types_checked = False

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
                        if ft not in failing_trees:
                            failing_trees.append(ft)

            total += 1

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

    def __repr__(self):
        representation = f"{self.left} {self.operator.value} {self.right}"
        for identifier in self.searches:
            representation = representation.replace(
                identifier, repr(self.searches[identifier])
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
        self, constraints: List[Constraint], *args, lazy: bool = False, **kwargs
    ):
        """
        Initializes the conjunction constraint with the given constraints.
        :param List[Constraint] constraints: The constraints to use.
        :param args: Additional arguments.
        :param bool lazy: If True, the conjunction is lazy evaluated.
        """
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given conjunction.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[str, DerivationTree]] scope: The scope of the tree.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            # If the conjunction is lazy, evaluate the constraints one by one and stop if one fails
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope)
                fitness_values.append(fitness)
                if not fitness.success:
                    break
        else:
            # If the conjunction is not lazy, evaluate all constraints at once
            fitness_values = [
                constraint.fitness(tree, scope) for constraint in self.constraints
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
            total += 1
            if overall:
                solved += 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " and ".join(repr(c) for c in self.constraints) + ")"

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
        self, constraints: List[Constraint], *args, lazy: bool = False, **kwargs
    ):
        """
        Initializes the disjunction constraint with the given constraints.
        :param List[Constraint] constraints: The constraints to use.
        :param args: Additional arguments.
        :param bool lazy: If True, the disjunction is lazy evaluated.
        """
        super().__init__(*args, **kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given disjunction.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[str, DerivationTree]] scope: The scope of the tree.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            # If the disjunction is lazy, evaluate the constraints one by one and stop if one succeeds
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope)
                fitness_values.append(fitness)
                if fitness.success:
                    break
        else:
            # If the disjunction is not lazy, evaluate all constraints at once
            fitness_values = [
                constraint.fitness(tree, scope) for constraint in self.constraints
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
            total += 1
            if overall:
                solved = total + 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return "(" + " or ".join(repr(c) for c in self.constraints) + ")"

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
        self, tree: DerivationTree, scope: Optional[Dict[str, DerivationTree]] = None
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given implication.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[str, DerivationTree]] scope: The scope of the tree.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        # Evaluate the antecedent
        antecedent_fitness = self.antecedent.fitness(tree, scope)
        if antecedent_fitness.success:
            # If the antecedent is true, evaluate the consequent
            fitness = copy(self.consequent.fitness(tree, scope))
            if fitness.success:
                fitness.solved += 1
            fitness.total += 1
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
    Represents an exists constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        statement: Constraint,
        bound: NonTerminal,
        search: NonTerminalSearch,
        lazy: bool = False,
        *args,
        **kwargs,
    ):
        """
        Initializes the exists constraint with the given statement, bound, and search.
        :param Constraint statement: The statement to evaluate.
        :param NonTerminal bound: The bound variable.
        :param NonTerminalSearch search: The search to use.
        :param bool lazy: If True, the exists constraint is lazy evaluated.
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
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given exists constraint.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        # Iterate over all containers found by the search
        for container in self.search.find(tree, scope=scope):
            # Update the scope with the bound variable
            scope[self.bound] = container.evaluate()
            # Evaluate the statement
            fitness = self.statement.fitness(tree, scope)
            # Add the fitness to the list
            fitness_values.append(fitness)
            # If the exists constraint is lazy and the statement is successful, stop
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
        total += 1
        if overall:
            solved = total + 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"(exists {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"

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
        bound: NonTerminal,
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
        :param bool lazy: If True, the forall constraint is lazy evaluated.
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
        scope: Optional[Dict[NonTerminal, DerivationTree]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given forall constraint.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[Dict[NonTerminal, DerivationTree]] scope: The scope of the tree.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        fitness_values = list()
        scope = scope or dict()
        # Iterate over all containers found by the search
        for container in self.search.find(tree, scope=scope):
            # Update the scope with the bound variable
            scope[self.bound] = container.evaluate()
            # Evaluate the statement
            fitness = self.statement.fitness(tree, scope)
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
        total += 1
        if overall:
            solved = total + 1
        # Create the fitness object
        fitness = ConstraintFitness(solved, total, overall, failing_trees=failing_trees)
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def __repr__(self):
        return f"(forall {repr(self.bound)} in {repr(self.search)}: {repr(self.statement)})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_forall_constraint(self)
        if visitor.do_continue(self):
            self.statement.accept(visitor)


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
