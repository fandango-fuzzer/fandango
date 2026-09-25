from collections.abc import Callable, Generator
from typing import Optional

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.evolution import GeneratorWithReturn
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER


class PopulationManager:
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
    ):
        self._grammar = grammar
        self._start_symbol = start_symbol

    def _generate_population_entry(self, max_nodes: int) -> DerivationTree:
        return self._grammar.fuzz(self._start_symbol, max_nodes)

    @staticmethod
    def _generate_population_hashes(
        current_population: list[DerivationTree],
    ) -> set[int]:
        return {hash(ind) for ind in current_population}

    @staticmethod
    def add_unique_individual(
        population: list[DerivationTree],
        candidate: DerivationTree,
        unique_set: set[int],
    ) -> bool:
        new_hashes = PopulationManager._generate_population_hashes([candidate])
        if len(new_hashes.intersection(unique_set)) == 0:
            # If the candidate has a new hash, we can add it to the population
            unique_set.update(new_hashes)
            population.append(candidate)
            return True
        return False

    def _is_population_complete(
        self, unique_population: list[DerivationTree], population_size: int
    ) -> bool:
        return len(unique_population) >= population_size

    def refill_population(
        self,
        current_population: list[DerivationTree],
        eval_individual: Callable[
            [DerivationTree],
            Generator[
                DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
            ],
        ],
        max_nodes: int,
        target_population_size: int,
    ) -> Generator[DerivationTree, None, None]:
        """
        Refills the population with unique individuals in place.

        Does not deduplicate the current population.

        If after 10 times the difference between the current population size and the target population size
        the required population size is still not met, a warning is logged and the incomplete population is returned.

        :param current_population: The current population of individuals.
        :param eval_individual: The function to evaluate the fitness of an individual.
        :param max_nodes: The maximum number of nodes in an individual.
        :param target_population_size: The target size of the population.
        :return: A generator that yields solutions. The population is modified in place.
        """
        unique_hashes = PopulationManager._generate_population_hashes(
            current_population
        )
        attempts = 0
        max_attempts = (target_population_size - len(current_population)) * 10

        while (
            not self._is_population_complete(current_population, target_population_size)
            and attempts < max_attempts
        ):
            individual = self._generate_population_entry(max_nodes)
            found_solution, (_fitness, failing_trees, suggestion) = GeneratorWithReturn(
                eval_individual(individual)
            ).collect()
            new_found_solution, (candidate, _fixes_made) = GeneratorWithReturn(
                self.fix_individual(
                    individual, failing_trees, suggestion, eval_individual
                )
            ).collect()
            if attempts < max_attempts:
                if PopulationManager.add_unique_individual(
                    current_population, candidate, unique_hashes
                ):
                    yield from found_solution
                    yield from new_found_solution
                else:
                    attempts += 1

        if not self._is_population_complete(current_population, target_population_size):
            LOGGER.warning(
                f"Could not generate a full population of unique individuals. Population size reduced to {len(current_population)}."
            )

    def fix_individual(
        self,
        individual: DerivationTree,
        failing_trees: list[FailingTree],
        suggestion: Suggestion,
        eval_individual: Callable[
            [DerivationTree],
            Generator[
                DerivationTree, None, tuple[float, list[FailingTree], Suggestion]
            ],
        ],
    ) -> Generator[DerivationTree, None, tuple[DerivationTree, int]]:
        fixes_made = 0
        fix_round_count = 0
        failing_constraints = frozenset(tree.cause for tree in failing_trees)
        involved_constraints = set(failing_constraints)
        seen_failing_constraints = {failing_constraints}
        while failing_constraints and fix_round_count < len(involved_constraints):
            fixed, round_fixes_made = self._apply_suggestion(individual, suggestion)
            if round_fixes_made == 0:
                break
            fix_round_count += 1
            fixes_made += round_fixes_made
            _fitness, failing_trees, suggestion = yield from eval_individual(fixed)
            individual = fixed
            failing_constraints = frozenset(tree.cause for tree in failing_trees)
            if failing_constraints in seen_failing_constraints:
                break
            seen_failing_constraints.add(failing_constraints)
            involved_constraints |= failing_constraints
        return individual, fixes_made

    def _apply_suggestion(
        self, individual: DerivationTree, suggestion: Optional[Suggestion]
    ) -> tuple[DerivationTree, int]:
        if not suggestion:
            return individual, 0
        suggested_replacements = suggestion.get_replacements(individual, self._grammar)
        return (
            individual.replace_multiple(self._grammar, suggested_replacements),
            len(suggested_replacements),
        )
