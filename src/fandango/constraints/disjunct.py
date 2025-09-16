from copy import copy
import itertools
from typing import Any, Optional
from fandango.language.tree import DerivationTree
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import ConstraintFitness
from fandango.language.symbols.non_terminal import NonTerminal


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

    def format_as_spec(self) -> str:
        return "(" + " or ".join(c.format_as_spec() for c in self.constraints) + ")"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_disjunction_constraint(self)
        if visitor.do_continue(self):
            for constraint in self.constraints:
                constraint.accept(visitor)

    def invert(self) -> "Constraint":
        """
        Return an inverted version of this disjunction constraint.
        Using De Morgan's law: not (A or B) = not A and not B
        """
        from fandango.constraints.conjunction import ConjunctionConstraint

        # Invert each sub-constraint
        inverted_constraints = [constraint.invert() for constraint in self.constraints]

        # Return a conjunction of the inverted constraints
        return ConjunctionConstraint(
            inverted_constraints,
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
            lazy=self.lazy,
        )
