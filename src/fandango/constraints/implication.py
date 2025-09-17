from copy import copy
from fandango.constraints.constraint_visitor import ConstraintVisitor
from typing import Any, Optional
from fandango import DerivationTree
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import ConstraintFitness
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


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

    def format_as_spec(self) -> str:
        return f"({self.antecedent.format_as_spec()} -> {self.consequent.format_as_spec()})"

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_implication_constraint(self)
        if visitor.do_continue(self):
            self.antecedent.accept(visitor)
            self.consequent.accept(visitor)

    def invert(self) -> "Constraint":
        """
        Return an inverted version of this implication constraint.
        Using logical equivalence: not (A -> B) = A and not B
        """
        from fandango.constraints.conjunction import ConjunctionConstraint

        # Invert the consequent
        inverted_consequent = self.consequent.invert()

        # Return a conjunction of the antecedent and inverted consequent
        return ConjunctionConstraint(
            [self.antecedent, inverted_consequent],
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )
