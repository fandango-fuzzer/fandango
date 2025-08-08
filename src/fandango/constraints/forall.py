from copy import copy
import itertools
from typing import Any, Optional
from fandango.constraints import LEGACY
from fandango.constraints.constraint import Constraint
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.fitness import ConstraintFitness
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


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

    def format_as_spec(self) -> str:
        bound = (
            self.bound if isinstance(self.bound, str) else self.bound.format_as_spec()
        )
        if LEGACY:
            return f"(forall {bound} in {self.search.format_as_spec()}: {self.statement.format_as_spec()})"
        else:
            return f"all({self.statement.format_as_spec()} for {bound} in {self.search.format_as_spec()})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_forall_constraint(self)
        if visitor.do_continue(self):
            self.statement.accept(visitor)

    def invert(self) -> "Constraint":
        """
        Return an inverted version of this forall constraint.
        Using logical equivalence: not forall x: P(x) = exists x: not P(x)
        """
        from fandango.constraints.exists import ExistsConstraint

        # Invert the statement
        inverted_statement = self.statement.invert()

        # Return an exists constraint with the inverted statement
        return ExistsConstraint(
            inverted_statement,
            self.bound,
            self.search,
            lazy=self.lazy,
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )
