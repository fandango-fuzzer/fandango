"""Unit tests for the selection module."""

import pytest

from fandango.evolution.chromosomes.base import Chromosome
from fandango.evolution.selection import RandomSelection, TournamentSelection
from fandango.language.tree import DerivationTree


class _FakeChromosome(Chromosome):
    """Minimal Chromosome stub for selection tests."""

    def __init__(self, value: int) -> None:
        self.value = value

    def size(self) -> int:
        return self.value

    def clone(self) -> "_FakeChromosome":
        return _FakeChromosome(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _FakeChromosome) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

    def to_derivation_trees(self) -> list[DerivationTree]:
        return []


def _pop(n: int) -> list[_FakeChromosome]:
    return [_FakeChromosome(i) for i in range(n)]


@pytest.mark.parametrize("number", [1, 3, 5])
def test_select_returns_correct_number(number: int) -> None:
    pop = _pop(10)
    result: list[_FakeChromosome] = RandomSelection[_FakeChromosome]().select(
        pop, number
    )
    assert len(result) == number


def test_select_elements_come_from_population() -> None:
    pop = _pop(10)
    result: list[_FakeChromosome] = RandomSelection[_FakeChromosome]().select(
        pop, number=20
    )
    assert all(item in pop for item in result)


@pytest.mark.parametrize("size", [1, 2, 10])
def test_random_selection_index_in_range(size: int) -> None:
    pop = _pop(size)
    idx = RandomSelection[_FakeChromosome]().get_index(pop)
    assert 0 <= idx < size


def test_tournament_selects_best_with_key() -> None:
    """With tournament_size == population size the best individual is always chosen."""
    pop = _pop(5)  # values 0..4; higher value = better
    sel: TournamentSelection[_FakeChromosome] = TournamentSelection(
        tournament_size=len(pop), key=lambda c: c.value
    )
    for _ in range(20):
        chosen = sel.select(pop)[0]
        assert chosen.value == 4


def test_tournament_selects_worst_with_inverted_key() -> None:
    """Inverted key always picks the individual with the lowest value."""
    pop = _pop(5)
    sel: TournamentSelection[_FakeChromosome] = TournamentSelection(
        tournament_size=len(pop), key=lambda c: -c.value
    )
    for _ in range(20):
        chosen = sel.select(pop)[0]
        assert chosen.value == 0


def test_tournament_without_key_returns_valid_index() -> None:
    pop = _pop(10)
    sel: TournamentSelection[_FakeChromosome] = TournamentSelection(tournament_size=3)
    idx = sel.get_index(pop)
    assert 0 <= idx < len(pop)


def test_tournament_size_larger_than_population_does_not_raise() -> None:
    """tournament_size is capped at population length; no error raised."""
    pop = _pop(3)
    sel: TournamentSelection[_FakeChromosome] = TournamentSelection(
        tournament_size=100, key=lambda c: c.value
    )
    chosen = sel.select(pop)[0]
    assert chosen in pop


@pytest.mark.parametrize("tournament_size", [1, 2, 5])
def test_tournament_result_always_in_population(tournament_size: int) -> None:
    pop = _pop(10)
    sel: TournamentSelection[_FakeChromosome] = TournamentSelection(
        tournament_size=tournament_size, key=lambda c: c.value
    )
    assert sel.select(pop)[0] in pop
