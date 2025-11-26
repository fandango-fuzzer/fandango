import abc
import itertools
from typing import TYPE_CHECKING, Any, Optional, TypedDict
import warnings

from fandango.language.search import Container, NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    from fandango.constraints.fitness import Fitness


class GeneticBaseInitArgs(TypedDict, total=False):
    searches: Optional[dict[str, NonTerminalSearch]]
    local_variables: Optional[dict[str, Any]]
    global_variables: Optional[dict[str, Any]]


class GeneticBase(abc.ABC):
    """
    Abstract class to represent a genetic base.
    """

    def __init__(
        self,
        searches: Optional[dict[str, NonTerminalSearch]] = None,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        """
        Initialize the GeneticBase with the given searches, local variables, and global variables.
        :param Optional[dict[str, NonTerminalSearch]] searches: The dictionary of searches.
        :param Optional[dict[str, Any]] local_variables: The dictionary of local variables.
        :param Optional[dict[str, Any]] global_variables: The dictionary of global variables.
        """
        self.searches = searches or dict()
        self.local_variables = local_variables or dict()
        self.global_variables = global_variables or dict()

    def get_access_points(self) -> list[NonTerminal]:
        """
        Get the access points of the genetic base, i.e., the non-terminal that are considered in this genetic base.
        :return list[NonTerminal]: The list of access points.
        """
        return sum(
            [search.get_access_points() for search in self.searches.values()], []
        )

    @abc.abstractmethod
    def fitness(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> "Fitness":
        """
        Abstract method to calculate the fitness of the tree.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return Fitness: The fitness of the tree.
        """
        raise NotImplementedError("Fitness function not implemented")

    @staticmethod
    def get_hash(
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> int:
        return hash(
            (
                tree,
                tuple((scope or {}).items()),
                tuple((local_variables or {}).items()),
            )
        )

    def combinations(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
    ) -> list[tuple[tuple[str, Container], ...]]:
        """
        Get all possible combinations of trees that satisfy the searches.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :return list[list[tuple[str, DerivationTree]]]: The list of combinations of trees that fill all non-terminals
        in the genetic base.
        """
        nodes: list[list[tuple[str, Container]]] = []
        for name, search in self.searches.items():
            nodes.append(
                [(name, container) for container in search.find(tree, scope=scope)]
            )
        return list(itertools.product(*nodes))

    def check(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Check if the tree satisfies the genetic base.
        :param DerivationTree tree: The tree to check.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return bool: True if the tree satisfies the genetic base, False otherwise.
        """
        return self.fitness(tree, scope, local_variables).success

    def __str__(self) -> str:
        warnings.warn("Don't rely on this, use method specific to your usecase")
        return self.format_as_spec()

    def __repr__(self) -> str:
        warnings.warn("Don't rely on this, use method specific to your usecase")
        return f"{self.__class__.__name__}({self.format_as_spec()})"

    @abc.abstractmethod
    def format_as_spec(self) -> str:
        """
        Format as a string that can be used in a spec file.
        """
