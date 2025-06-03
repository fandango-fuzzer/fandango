import random
from typing import Callable, List, Set

from fandango.evolution.evaluation import Evaluator
from fandango.language.grammar import DerivationTree, Grammar
from fandango.language.packetforecaster import PacketForecaster
from fandango.language.symbol import NonTerminal
from fandango.logger import LOGGER


class PopulationManager:
    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str,
        population_size: int,
        max_nodes: int,
        warnings_are_errors: bool = False,
    ):
        self.grammar = grammar
        self.start_symbol = start_symbol
        self.population_size = population_size
        self.warnings_are_errors = warnings_are_errors
        self.max_nodes = max_nodes

    def _generate_population_entry(self):
        return self.grammar.fuzz(self.start_symbol, self.max_nodes)

    def add_unique_individual(
        self,
        population: List[DerivationTree],
        candidate: DerivationTree,
        unique_set: Set[int],
    ) -> bool:
        h = hash(candidate)
        if h not in unique_set:
            unique_set.add(h)
            population.append(candidate)
            return True
        return False

    def _is_population_complete(self, unique_population: List[DerivationTree]) -> bool:
        return len(unique_population) >= self.population_size

    def generate_random_initial_population(
        self, fix_func: Callable[[DerivationTree], DerivationTree]
    ) -> List[DerivationTree]:
        unique_population = []
        unique_hashes = set()
        attempts = 0
        max_attempts = self.population_size * 10

        while (
            not self._is_population_complete(unique_population)
            and attempts < max_attempts
        ):
            candidate = fix_func(self._generate_population_entry())
            self.add_unique_individual(unique_population, candidate, unique_hashes)
            attempts += 1

        if attempts >= max_attempts:
            LOGGER.warning(
                f"Could not generate a full population of unique individuals. Population size reduced to {len(unique_population)}."
            )
        return unique_population

    def refill_population(
        self,
        current_population: List[DerivationTree],
        fix_func: Callable[[DerivationTree], DerivationTree],
    ) -> List[DerivationTree]:
        unique_hashes = {hash(ind) for ind in current_population}
        attempts = 0
        max_attempts = (self.population_size - len(current_population)) * 10

        while (
            not self._is_population_complete(current_population)
            and attempts < max_attempts
        ):
            candidate = fix_func(self._generate_population_entry())
            if hash(candidate) not in unique_hashes:
                unique_hashes.add(hash(candidate))
                current_population.append(candidate)
            attempts += 1

        if attempts > max_attempts:
            LOGGER.warning(
                "Could not generate full unique new population, filling remaining slots with duplicates."
            )
            while len(current_population) < self.population_size:
                current_population.append(self._generate_population_entry())

        return current_population


class IoPopulationManager(PopulationManager):

    def __init__(
        self,
        grammar: Grammar,
        evaluator: Evaluator,
        start_symbol: str,
        population_size: int,
        warnings_are_errors: bool = False,
    ):
        super().__init__(grammar, start_symbol, population_size, warnings_are_errors)
        self.evaluator = evaluator
        self.prev_packet_idx = 0
        self.fuzzable_packets: list[PacketForecaster.ForcastingPacket] | None = None

    def _is_population_complete(self, unique_population: List[DerivationTree]) -> bool:
        for entry in unique_population:
            if self.evaluator.evaluate_individual(entry)[0] >= 0.99:
                return True
        return super()._is_population_complete(unique_population)

    def _generate_population_entry(self):
        if self.fuzzable_packets is None or len(self.fuzzable_packets) == 0:
            return DerivationTree(NonTerminal(self.start_symbol))

        current_idx = (self.prev_packet_idx + 1) % len(self.fuzzable_packets)
        current_pck = random.choice(self.fuzzable_packets)
        mounting_option = random.choice(list(current_pck.paths))

        tree = self.grammar.collapse(mounting_option.tree)
        tree.set_all_read_only(True)
        dummy = DerivationTree(NonTerminal("<hookin>"))
        tree.append(mounting_option.path[1:], dummy)

        fuzz_point = dummy.parent
        fuzz_point.set_children(fuzz_point.children[:-1])
        current_pck.node.fuzz(fuzz_point, self.grammar, max_nodes=999999)

        self.prev_packet_idx = current_idx
        return tree
