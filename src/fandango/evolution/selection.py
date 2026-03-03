import random
from abc import ABC, abstractmethod
from beartype.typing import Any, Callable, Generic, List, Optional, TypeVar

from fandango.evolution.chromosomes.base import Chromosome

T = TypeVar("T", bound=Chromosome)


class SelectionOperator(ABC, Generic[T]):
    @abstractmethod
    def get_index(self, population: List[T]) -> int:
        """Return the index of the selected individual."""

    def select(self, population: List[T], number: int = 1) -> List[T]:
        """Select `number` individuals by calling get_index repeatedly."""
        return [population[self.get_index(population)] for _ in range(number)]


class RandomSelection(SelectionOperator[T]):
    def get_index(self, population: List[T]) -> int:
        return random.randrange(len(population))


class TournamentSelection(SelectionOperator[T]):
    def __init__(
        self,
        tournament_size: int = 2,
        key: Optional[Callable[[T], Any]] = None,
    ) -> None:
        self._tournament_size = tournament_size
        self._key = key

    def get_index(self, population: List[T]) -> int:
        n = min(self._tournament_size, len(population))
        indices = random.sample(range(len(population)), n)
        key_func = self._key
        if callable(key_func):
            return max(indices, key=lambda i: key_func(population[i]))
        return indices[0]
