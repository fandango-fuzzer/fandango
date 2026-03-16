"""MIO (Many Independent Objective) algorithm."""

import math
import random
from dataclasses import dataclass
from typing import cast

from beartype.typing import List, Optional, Any

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.evolution.algorithms.archive import MIOArchive
from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.algorithms.random import _generate_individual
from fandango.evolution.chromosomes import Suite
from fandango.evolution.chromosomes.individual import Individual
from fandango.language.grammar.grammar import Grammar

_DEFAULT_MAX_GENERATIONS = 1000


def _mutate_individual(individual: Individual, grammar: Grammar) -> Individual:
    """Produce a mutant by replacing a random non-terminal subtree with a fresh fuzz."""
    tree = individual.clone().tree
    non_terminals = list(tree.get_non_terminal_symbols())
    if not non_terminals:
        return _generate_individual(grammar)
    symbol = random.choice(non_terminals)
    nodes = tree.find_all_nodes(symbol)
    if not nodes:
        return _generate_individual(grammar)
    node = random.choice(nodes)
    new_subtree = grammar.fuzz(str(node.symbol))
    new_tree = tree.replace(grammar, node, new_subtree)
    return Individual(new_tree)


@dataclass
class _MIOParameters:
    """Adaptive parameters for MIO search phases."""

    pr: float  # probability of generating a random individual vs. from archive
    n: int  # max candidates per uncovered goal in archive
    m: int  # max mutations of current solution before switching


class MIOAlgorithm(GenerationAlgorithm[Individual]):
    """
    Many Independent Objective algorithm (MIO).

    MIO maintains an archive of solutions covering different goals
    and uses focused search to explore each goal independently.
    Parameters transition from exploration (high pr, large n, small m)
    to exploitation (low pr, small n, large m) over the search budget.

    https://arxiv.org/pdf/1901.01541
    """

    def __init__(
        self,
        grammar: Grammar,
        constraints: List[Constraint | SoftValue],
        population_size: int = 10,
        k: int = 2,
        initial_pr: float = 0.5,
        focused_pr: float = 0.0,
        initial_n: int = 10,
        focused_n: int = 1,
        initial_m: int = 1,
        focused_m: int = 10,
        exploitation_starts_at: float = 0.5,
        **kwargs: Any,
    ) -> None:
        super().__init__(grammar, constraints, population_size, **kwargs)
        self._k = k
        self._initial_pr = initial_pr
        self._focused_pr = focused_pr
        self._initial_n = initial_n
        self._focused_n = focused_n
        self._initial_m = initial_m
        self._focused_m = focused_m
        self._exploitation_starts_at = exploitation_starts_at
        self._parameters = _MIOParameters(pr=initial_pr, n=initial_n, m=initial_m)
        self._current_solution: Optional[Individual] = None
        self._current_mutations: int = 0
        self._focused: bool = False
        self._mio_archive = MIOArchive(grammar, n=initial_n, k=k)
        self.archive = self._mio_archive

    def _update_parameters(self, generation: int, max_generations: int) -> None:
        """Linearly interpolate parameters from exploration to exploitation phase."""
        if self._focused:
            return
        progress = generation / max_generations
        if progress >= self._exploitation_starts_at:
            self._focused = True
            self._parameters.pr = self._focused_pr
            n_before = self._parameters.n
            self._parameters.n = self._focused_n
            self._parameters.m = self._focused_m
        else:
            t = progress / self._exploitation_starts_at
            n_before = self._parameters.n
            self._parameters.pr = self._initial_pr + t * (
                self._focused_pr - self._initial_pr
            )
            self._parameters.n = math.ceil(
                self._initial_n + t * (self._focused_n - self._initial_n)
            )
            self._parameters.m = math.ceil(
                self._initial_m + t * (self._focused_m - self._initial_m)
            )
        if self._parameters.n < n_before:
            self._mio_archive.shrink_solutions(self._parameters.n)

    def _evolve(self) -> None:
        """Run one step of the MIO loop: generate or mutate, then update archive."""
        if (
            self._current_solution is not None
            and self._current_mutations < self._parameters.m
        ):
            offspring = _mutate_individual(self._current_solution, self.grammar)
            self._current_mutations += 1
        elif random.random() < self._parameters.pr:
            offspring = _generate_individual(self.grammar)
            self._current_mutations = 1
            self._current_solution = None
        else:
            maybe = self._mio_archive.get_solution()
            base = (
                maybe
                if isinstance(maybe, Individual)
                else _generate_individual(self.grammar)
            )
            offspring = _mutate_individual(base, self.grammar)
            self._current_mutations = 1
            self._current_solution = None

        if self._mio_archive.update([offspring]):
            self._current_solution = offspring

    def generate(self, max_generations: Optional[int] = None) -> Suite:
        """Run MIO search and return a Suite of covering individuals."""
        effective_max = (
            max_generations if max_generations is not None else _DEFAULT_MAX_GENERATIONS
        )
        generation = 0
        while generation < effective_max and self._mio_archive.uncovered_goals:
            self._evolve()
            self._update_parameters(generation, effective_max)
            generation += 1
        solutions = self._mio_archive.solutions
        if not solutions:
            solutions = [_generate_individual(self.grammar)]
        return Suite(
            [s for s in solutions if isinstance(s, Individual)]
            or [_generate_individual(self.grammar)]
        )
