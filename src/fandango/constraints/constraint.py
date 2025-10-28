from abc import ABC, abstractmethod
from collections.abc import Collection
from typing import TYPE_CHECKING, Any, Optional
import warnings
from fandango.constraints.base import GeneticBase
from fandango.language.tree import DerivationTree
from fandango.constraints.fitness import ConstraintFitness
from fandango.language.search import NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal

if TYPE_CHECKING:
    from fandango.constraints.constraint_visitor import ConstraintVisitor


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
        local_variables: Optional[dict[str, Any]] = None,
    ) -> ConstraintFitness:
        """
        Abstract method to calculate the fitness of the tree.
        """
        raise NotImplementedError("Fitness function not implemented")

    @abstractmethod
    def accept(self, visitor: "ConstraintVisitor") -> None:
        """
        Accepts a visitor to traverse the constraint structure.
        """
        pass

    def get_symbols(self) -> Collection[NonTerminalSearch]:
        """
        Get the placeholders of the constraint.
        """
        return self.searches.values()

    @staticmethod
    def eval(
        expression: str,
        global_variables: dict[str, Any],
        local_variables: dict[str, Any],
    ) -> Any:
        """
        Evaluate the tree in the context of local and global variables.
        """
        return eval(expression, global_variables, local_variables)

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

    def __repr__(self) -> str:
        warnings.warn("Don't rely on this, use method specific to your usecase")
        return f"{self.__class__.__name__}({self.format_as_spec()})"
