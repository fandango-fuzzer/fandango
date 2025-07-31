import abc
import itertools
from typing import TYPE_CHECKING, Any, Optional

from fandango.language.search import Container, NonTerminalSearch
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    from fandango.constraints.fitness import FailingTree, Fitness


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

    def get_access_points(self):
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
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> "Fitness":
        """
        Abstract method to calculate the fitness of the tree.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return Fitness: The fitness of the tree.
        """
        raise NotImplementedError("Fitness function not implemented")

    @staticmethod
    def get_hash(
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ):
        return hash(
            (
                tree,
                tuple((scope or {}).items()),
                tuple(population or []),
                tuple((local_variables or {}).items()),
            )
        )

    def combinations(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
    ):
        """
        Get all possible combinations of trees that satisfy the searches.
        :param DerivationTree tree: The tree to calculate the fitness.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :return list[list[tuple[str, DerivationTree]]]: The list of combinations of trees that fill all non-terminals
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        in the genetic base.
        """
        nodes: list[list[tuple[str, Container]]] = []
        for name, search in self.searches.items():
            nodes.append(
                [
                    (name, container)
                    for container in search.find(
                        tree, scope=scope, population=population
                    )
                ]
            )
        return itertools.product(*nodes)

    def check(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> bool:
        """
        Check if the tree satisfies the genetic base.
        :param DerivationTree tree: The tree to check.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return bool: True if the tree satisfies the genetic base, False otherwise.
        """
        return self.fitness(tree, scope, population, local_variables).success

    def get_failing_nodes(
        self,
        tree: DerivationTree,
        scope: Optional[dict[NonTerminal, DerivationTree]] = None,
        population: Optional[list[DerivationTree]] = None,
        local_variables: Optional[dict[str, Any]] = None,
    ) -> list["FailingTree"]:
        """
        Get the failing nodes of the tree.
        :param DerivationTree tree: The tree to check.
        :param Optional[dict[NonTerminal, DerivationTree]] scope: The scope of non-terminals matching to trees.
        :param Optional[list[DerivationTree]] population: The population of trees to calculate the fitness.
        :param Optional[dict[str, Any]] local_variables: The local variables to use in the fitness calculation.
        :return list[FailingTree]: The list of failing trees
        """
        return self.fitness(tree, scope, population, local_variables).failing_trees

    def __str__(self) -> str:
        raise RuntimeError("Not implemented, use method specific to your usecase")

    def __repr__(self) -> str:
        raise RuntimeError("Not implemented, use method specific to your usecase")

    @abc.abstractmethod
    def format_as_spec(self) -> str:
        """
        Format as a string that can be used in a spec file.
        """
