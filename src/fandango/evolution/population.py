import random
from collections.abc import Callable, Generator
from typing import Optional

from fandango.constraints.failing_tree import FailingTree, Suggestion
from fandango.errors import FandangoValueError
from fandango.evolution import GeneratorWithReturn
from fandango.io.navigation.packetforecaster import ForecastingPacket
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER


class PopulationManager:
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
        warnings_are_errors: bool = False,
    ):
        self._grammar = grammar
        self._start_symbol = start_symbol
        self._warnings_are_errors = warnings_are_errors

    def _generate_population_entry(self, max_nodes: int) -> DerivationTree:
        return self._grammar.fuzz(self._start_symbol, max_nodes)

    @staticmethod
    def _generate_population_hashes(
        current_population: list[DerivationTree]
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
        unique_hashes = self._generate_population_hashes(current_population)
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
            candidate, _fixes_made = self.fix_individual(
                individual,
                failing_trees,
            )
            new_found_solution, (_new_fitness, _new_failing_trees, suggestion) = (
                GeneratorWithReturn(eval_individual(candidate)).collect()
            )
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
        suggestion: Optional[Suggestion] = None,
    ) -> tuple[DerivationTree, int]:
        fixes_made = 0
        if suggestion:
            suggested_replacements = suggestion.get_replacements(
                individual, self._grammar
            )
            individual = individual.replace_multiple(
                self._grammar, suggested_replacements
            )
            fixes_made += len(suggested_replacements)

        return individual, fixes_made


class IoPopulationManager(PopulationManager):
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
        warnings_are_errors: bool = False,
    ):
        super().__init__(grammar, start_symbol, warnings_are_errors)
        self._prev_packet_idx = 0
        self.fuzzable_packets: list[ForecastingPacket] = []
        self.fallback_packets: list[ForecastingPacket] = []
        self.allow_fallback_packets = False

    def _generate_population_entry(self, max_nodes: int) -> DerivationTree:
        if self.fuzzable_packets is None or len(self.fuzzable_packets) == 0:
            return DerivationTree(NonTerminal(self._start_symbol))
        packet_selection = list(self.fuzzable_packets)
        if self.allow_fallback_packets:
            packet_selection.extend(self.fallback_packets)

        current_idx = (self._prev_packet_idx + 1) % len(packet_selection)
        current_pck = random.choice(packet_selection)
        mounting_option = random.choice(list(current_pck.paths))

        tree = self._grammar.collapse(mounting_option.tree)
        if tree is None:
            raise FandangoValueError(
                f"Could not collapse tree for {mounting_option.path} in packet {current_pck.node}"
            )
        tree.set_all_read_only(True)
        dummy = DerivationTree(NonTerminal("<hookin>"))
        tree.append(mounting_option.path[1:-1], dummy)

        fuzz_point = dummy.parent
        assert fuzz_point is not None
        fuzz_point.set_children(fuzz_point.children[:-1])
        current_pck.node.fuzz(fuzz_point, self._grammar, max_nodes)

        self._prev_packet_idx = current_idx
        return tree

    def add_unique_individual(
        self,
        population: list[DerivationTree],
        candidate: DerivationTree,
        unique_set: set[int],
    ) -> bool:
        new_hashes = self._generate_population_hashes([candidate])
        if len(new_hashes.intersection(unique_set)) == 0:
            # If the candidate has is new, we can add it to the population
            unique_set.update(new_hashes)
            population.append(candidate)
            return True
        return False
