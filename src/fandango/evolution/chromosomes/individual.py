"""Defines the Individual class."""

from __future__ import annotations
from beartype.typing import List
from fandango.evolution.chromosomes.base import Chromosome
from fandango.language.tree import DerivationTree


class Individual(Chromosome):
    """
    Wraps a single DerivationTree as an evolutionary unit.

    Represents one test case in the population.
    """

    def __init__(self, tree: DerivationTree):
        """Initialize with a DerivationTree."""
        self._tree = tree

    def size(self) -> int:
        """Return the size of the underlying DerivationTree."""
        return self._tree.size()

    def clone(self) -> Individual:
        """Return a deep copy of this Individual."""
        return Individual(self._tree.deepcopy())

    def __eq__(self, other: object) -> bool:
        """Structural equality comparison."""
        if not isinstance(other, Individual):
            return False
        return self._tree == other._tree

    def __hash__(self) -> int:
        """Hash based on hash of underlying DerivationTree."""
        return hash(self._tree)

    def to_derivation_trees(self) -> List[DerivationTree]:
        """Return a list containing only this tree."""
        return [self._tree]

    @property
    def tree(self) -> DerivationTree:
        """Access the underlying DerivationTree."""
        return self._tree
