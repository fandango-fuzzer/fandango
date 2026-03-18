from __future__ import annotations

from beartype.typing import Iterator, List

from fandango.evolution.chromosomes import Individual
from fandango.evolution.chromosomes.base import Chromosome
from fandango.language.tree import DerivationTree


class Suite(Chromosome):
    """
    Collection of Individuals representing a Suite.

    Used in whole-suite algorithms where the population consists of Suites.
    """

    def __init__(self, individuals: List[Individual]):
        """Initialize with a list of Individuals."""
        self._individuals = individuals

    def size(self) -> int:
        """Total size of all individuals in the suite."""
        return sum(ind.size() for ind in self._individuals)

    def clone(self) -> Suite:
        """Return a deep copy of this suite."""
        return Suite([ind.clone() for ind in self._individuals])

    def __eq__(self, other: object) -> bool:
        """Structural equality comparison."""
        if not isinstance(other, Suite):
            return False
        if len(self._individuals) != len(other._individuals):
            return False
        return all(a == b for a, b in zip(self._individuals, other._individuals))

    def __hash__(self) -> int:
        """Hash based on hash of all individuals."""
        return hash(tuple(hash(ind) for ind in self._individuals))

    def to_derivation_trees(self) -> List[DerivationTree]:
        """Return all trees from all individuals."""
        return [ind.tree for ind in self._individuals]

    def __len__(self) -> int:
        """Return the number of individuals in the suite."""
        return len(self._individuals)

    def __iter__(self) -> Iterator[Individual]:
        """Iterate over all individuals in the suite."""
        return iter(self._individuals)

    def __getitem__(self, index: int) -> Individual:
        """Get individual at index."""
        return self._individuals[index]

    def add_individual(self, individual: Individual) -> None:
        """Add an individual to the suite."""
        self._individuals.append(individual)

    def remove_individual(self, index: int) -> Individual:
        """Remove and return individual at index."""
        return self._individuals.pop(index)
