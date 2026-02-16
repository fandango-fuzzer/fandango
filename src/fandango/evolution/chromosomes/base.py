"""Base classes for evolutionary units."""

from __future__ import annotations

from abc import ABC, abstractmethod

from beartype.typing import List

from fandango.language.tree import DerivationTree


class Chromosome(ABC):
    """
    Abstract base class for evolutionary units.

    A unit is either an Individual == DerivationTree or a Suite == a collection
    of Individuals.
    """

    @abstractmethod
    def size(self) -> int:
        """Return the size/complexity of this chromosome."""
        pass

    @abstractmethod
    def clone(self) -> Chromosome:
        """Create a deep copy of this chromosome."""
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        """Structural equality comparison."""
        pass

    @abstractmethod
    def __hash__(self) -> int:
        """Hash for deduplication in populations."""
        pass

    @abstractmethod
    def to_derivation_trees(self) -> List[DerivationTree]:
        """Return all trees from this chromosome."""
        pass
