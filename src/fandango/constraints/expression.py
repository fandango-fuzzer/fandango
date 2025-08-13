from copy import copy
from typing import Any, Optional
from fandango.constraints.constraint_visitor import ConstraintVisitor
from fandango.constraints.constraint import Constraint
from fandango.constraints.fitness import ConstraintFitness, FailingTree
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import print_exception


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

    def format_as_spec(self) -> str:
        representation = self.expression
        for identifier in self.searches:
            representation = representation.replace(
                identifier, self.searches[identifier].format_as_spec()
            )
        return representation

    def accept(self, visitor: "ConstraintVisitor"):
        """
        Accepts a visitor to traverse the constraint structure.
        :param ConstraintVisitor visitor: The visitor to accept.
        """
        visitor.visit_expression_constraint(self)

    def invert(self) -> "ExpressionConstraint":
        """
        Return an inverted version of this expression constraint.
        The inverted constraint negates the expression using "not".
        """
        # Negate the expression by wrapping it with "not"
        inverted_expression = f"not ({self.expression})"

        # Create a new ExpressionConstraint with the negated expression
        return ExpressionConstraint(
            inverted_expression,
            searches=self.searches,
            local_variables=self.local_variables,
            global_variables=self.global_variables,
        )
