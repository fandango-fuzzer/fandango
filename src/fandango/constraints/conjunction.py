import itertools
from copy import copy
from typing import Any, Optional, Unpack

from fandango.constraints.base import GeneticBaseInitArgs
from fandango.constraints.comparison import ComparisonConstraint
from fandango.constraints.constraint import Constraint
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.disjunct import DisjunctionConstraint
from fandango.constraints.failing_tree import ApplyAllSuggestions
from fandango.constraints.fitness import ConstraintFitness
from fandango.constraints.implication import ImplicationConstraint
from fandango.language.search import NonTerminalSearch, resolve_searches
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class ConjunctionConstraint(Constraint):
    """
    Represents a conjunction constraint that can be used for fitness evaluation.
    """

    def __init__(
        self,
        constraints: list[Constraint],
        lazy: bool = False,
        **kwargs: Unpack[GeneticBaseInitArgs],
    ):
        """
        Initializes the conjunction constraint with the given constraints.
        :param list[Constraint] constraints: The constraints to use.
        :param args: Additional arguments.
        :param bool lazy: If True, the conjunction is lazily evaluated.
        """
        super().__init__(**kwargs)
        self.constraints = constraints
        self.lazy = lazy

    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Calculate the fitness of the tree based on the given conjunction.
        :param DerivationTree tree: The tree to evaluate.
        :param Optional[dict[str, DerivationTree]] scope: The scope of the tree.
        :param Optional[dict[str, Any]] local_variables: Local variables to use in the evaluation.
        :return ConstraintFitness: The fitness of the tree.
        """
        tree_hash = self.get_hash(tree, scope, local_variables)
        # If the fitness has already been calculated, return the cached value
        if tree_hash in self.cache:
            return copy(self.cache[tree_hash])
        if self.lazy:
            # If the conjunction is lazy, evaluate the constraints one by one and stop if one fails
            fitness_values = list()
            for constraint in self.constraints:
                fitness = constraint.fitness(tree, scope, local_variables)
                fitness_values.append(fitness)
                if not fitness.success:
                    break
        else:
            # If the conjunction is not lazy, evaluate all constraints at once
            fitness_values = [
                constraint.fitness(tree, scope, local_variables)
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
        suggestion = ApplyAllSuggestions([e.suggestion for e in fitness_values])
        if len(self.constraints) > 1:
            if overall:
                solved += 1
            total += 1
        # Create the fitness object
        fitness = ConstraintFitness(
            solved=solved,
            total=total,
            success=overall,
            suggestion=suggestion,
            failing_trees=failing_trees,
        )
        # Cache the fitness
        self.cache[tree_hash] = fitness
        return fitness

    def _format_as_comparison_chain(self) -> Optional[str]:
        """
        Format as `a < b <= c` if this conjunction was parsed from such a
        chain, i.e. each comparison continues with the operand the previous
        one ended with.
        """
        comparisons = [
            c for c in self.constraints if isinstance(c, ComparisonConstraint)
        ]
        if len(comparisons) < 2 or len(comparisons) != len(self.constraints):
            return None
        if any(
            previous._right != following._left
            for previous, following in itertools.pairwise(comparisons)
        ):
            return None
        chain = comparisons[0]._left
        searches: dict[str, NonTerminalSearch] = {}
        for comparison in comparisons:
            chain += f" {comparison._operator.value} {comparison._right}"
            searches.update(comparison.searches)
        return resolve_searches(chain, searches)

    def format_as_spec(self) -> str:
        chain = self._format_as_comparison_chain()
        if chain is not None:
            return chain
        # No parentheses around the conjunction: a parenthesised formula is
        # parsed as a single Python expression. Only a disjunction needs them,
        # as it binds less tightly.
        return " and ".join(
            (
                f"({c.format_as_spec()})"
                if isinstance(c, (DisjunctionConstraint, ImplicationConstraint))
                else c.format_as_spec()
            )
            for c in self.constraints
        )

    def accept(self, visitor: ConstraintVisitor) -> None:
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_conjunction_constraint(self)
        if visitor.do_continue(self):
            for constraint in self.constraints:
                constraint.accept(visitor)

    def clear_cache(self) -> None:
        super().clear_cache()
        for constraint in self.constraints:
            constraint.clear_cache()

    def invert(self) -> "Constraint":
        """
        Return an inverted version of this conjunction constraint.
        Using De Morgan's law: not (A and B) = not A or not B
        """
        from fandango.constraints.disjunct import DisjunctionConstraint

        # Invert each sub-constraint
        inverted_constraints = [constraint.invert() for constraint in self.constraints]

        # Return a disjunction of the inverted constraints
        return DisjunctionConstraint(
            inverted_constraints,
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
            lazy=self.lazy,
        )
