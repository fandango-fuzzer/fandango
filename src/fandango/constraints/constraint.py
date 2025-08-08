from abc import ABC, abstractmethod
from typing import Any, Optional
from fandango.language.tree import DerivationTree
from fandango.constraints.fitness import ConstraintFitness, GeneticBase
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal


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

    @abstractmethod
    def format_as_spec(self) -> str:
        """
        Format the constraint as a string that can be used in a spec file.
        """

    @abstractmethod
    def invert(self) -> "Constraint":
        """
        Return an inverted version of this constraint.
        The inverted constraint should have the opposite logical meaning.
        """
        raise NotImplementedError("Invert function not implemented")

    def __repr__(self):
        raise NotImplementedError(
            "Repr not implemented, use method specific to your usecase"
        )
