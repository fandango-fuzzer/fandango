import random
from collections.abc import Callable, Generator

from fandango.errors import FandangoValueError
from fandango.constraints.fitness import Comparison, ComparisonSide, FailingTree
from fandango.io.packetforecaster import PacketForecaster
from fandango.language.grammar import DerivationTree, Grammar
from fandango.language.symbol import NonTerminal
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

    def _generate_population_entry(self, max_nodes: int):
        return self._grammar.fuzz(self._start_symbol, max_nodes)

    @staticmethod
    def add_unique_individual(
        population: list[DerivationTree],
        candidate: DerivationTree,
        unique_set: set[int],
    ) -> bool:
        """
        Adds individual to the population if it is unique, according to its hash.

        :param population: The population to potentially add the individual to.
        :param candidate: The individual to potentially add to the population.
        :param unique_set: The set of unique individuals.
        :return: True if the individual was added, False otherwise.
        """
        h = hash(candidate)
        if h not in unique_set:
            unique_set.add(h)
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
            Generator[DerivationTree, None, tuple[float, list[FailingTree]]],
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
        unique_hashes = {hash(ind) for ind in current_population}
        attempts = 0
        max_attempts = (target_population_size - len(current_population)) * 10

        while (
            not self._is_population_complete(current_population, target_population_size)
            and attempts < max_attempts
        ):
            individual = self._generate_population_entry(max_nodes)
            _fitness, failing_trees = yield from eval_individual(individual)
            candidate, _fixes_made = self.fix_individual(
                individual,
                failing_trees,
            )
            _new_fitness, _new_failing_trees = yield from eval_individual(candidate)
            if not PopulationManager.add_unique_individual(
                current_population, candidate, unique_hashes
            ):
                attempts += 1

        if not self._is_population_complete(current_population, target_population_size):
            LOGGER.warning(
                f"Could not generate a full population of unique individuals. Population size reduced to {len(current_population)}."
            )

    def fix_individual(
        self,
        individual: DerivationTree,
        failing_trees: list[FailingTree],
    ) -> tuple[DerivationTree, int]:
        fixes_made = 0
        replacements = dict()
        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue
            for operator, value, side in failing_tree.suggestions:
                if operator == Comparison.EQUAL and side == ComparisonSide.LEFT:
                    # LOGGER.debug(f"Parsing {value} into {failing_tree.tree.symbol.symbol!s}")
                    if (
                        isinstance(value, DerivationTree)
                        and failing_tree.tree.symbol == value.symbol
                    ):
                        suggested_tree = value.deepcopy(
                            copy_children=True, copy_params=False, copy_parent=False
                        )
                        suggested_tree.set_all_read_only(False)
                    else:
                        assert isinstance(failing_tree.tree.symbol.symbol, str)
                        suggested_tree = self._grammar.parse(
                            value, start=failing_tree.tree.symbol.symbol
                        )
                    if suggested_tree is None:
                        continue
                    replacements[failing_tree.tree] = suggested_tree
                    fixes_made += 1
        if len(replacements) > 0:
            # Prevent circular replacements
            deleted = set()
            for value in set(replacements.values()):
                if value in deleted:
                    continue
                if value in replacements.keys():
                    if replacements[value] not in replacements.keys():
                        deleted.add(replacements[value])
                        del replacements[value]
                        continue
                    if random.random() < 0.5:
                        deleted.add(replacements[value])
                        del replacements[value]
                    else:
                        deleted.add(replacements[replacements[value]])
                        del replacements[replacements[value]]

            individual = individual.replace_multiple(self._grammar, replacements)
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
        self.fuzzable_packets: list[PacketForecaster.ForcastingPacket] | None = None

    def _generate_population_entry(self, max_nodes: int):
        if self.fuzzable_packets is None or len(self.fuzzable_packets) == 0:
            return DerivationTree(NonTerminal(self._start_symbol))

        current_idx = (self._prev_packet_idx + 1) % len(self.fuzzable_packets)
        current_pck = random.choice(self.fuzzable_packets)
        mounting_option = random.choice(list(current_pck.paths))

        tree = self._grammar.collapse(mounting_option.tree)
        if tree is None:
            raise FandangoValueError(
                f"Could not collapse tree for {mounting_option.path} in packet {current_pck.node}"
            )
        tree.set_all_read_only(True)
        dummy = DerivationTree(NonTerminal("<hookin>"))
        tree.append(mounting_option.path[1:], dummy)

        fuzz_point = dummy.parent
        assert fuzz_point is not None
        fuzz_point.set_children(fuzz_point.children[:-1])
        current_pck.node.fuzz(fuzz_point, self._grammar, max_nodes)

        self._prev_packet_idx = current_idx
        return tree
