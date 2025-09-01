import random
from collections.abc import Callable, Generator

from fandango.constraints.failing_tree import Comparison, ComparisonSide
from fandango.constraints.failing_tree import FailingTree, BoundsFailingTree
from fandango.constraints.repetition_bounds import RepetitionBoundsConstraint
from fandango.errors import FandangoValueError
from fandango.evolution import GeneratorWithReturn
from fandango.io.navigation.packetforecaster import ForecastingPacket
from fandango.language.grammar.grammar import Grammar
from fandango.language.symbols import NonTerminal
from fandango.language.symbols import Slice
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

    def _generate_population_entry(self, max_nodes: int):
        return self._grammar.fuzz(self._start_symbol, max_nodes)

    def _generate_population_hashes(
        self, current_population: list[DerivationTree]
    ) -> set[int]:
        return {hash(ind) for ind in current_population}

    def add_unique_individual(
        self,
        population: list[DerivationTree],
        candidate: DerivationTree,
        unique_set: set[int],
    ) -> bool:
        new_hashes = self._generate_population_hashes([candidate])
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
        unique_hashes = self._generate_population_hashes(current_population)
        attempts = 0
        max_attempts = (target_population_size - len(current_population)) * 10

        while (
            not self._is_population_complete(current_population, target_population_size)
            and attempts < max_attempts
        ):
            individual = self._generate_population_entry(max_nodes)
            found_solution, (_fitness, failing_trees) = GeneratorWithReturn(
                eval_individual(individual)
            ).collect()
            candidate, _fixes_made = self.fix_individual(
                individual,
                failing_trees,
            )
            new_found_solution, (_new_fitness, _new_failing_trees) = (
                GeneratorWithReturn(eval_individual(candidate)).collect()
            )
            if attempts < max_attempts:
                if self.add_unique_individual(
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
    ) -> tuple[DerivationTree, int]:
        fixes_made = 0
        replacements: list[tuple[DerivationTree, DerivationTree]] = list()

        allow_repetition_full_delete = (
            len(
                list(
                    filter(
                        lambda x: not isinstance(x.cause, RepetitionBoundsConstraint),
                        failing_trees,
                    )
                )
            )
            == 0
        )
        # We only allow BoundsConstraints to delete all iterations of a repetition if all other non-boundconstraints constraints are satisfied.
        # Otherwise, we would lose the reference point to re-add the repetitions in the tree, which might be needed,
        # if the referenced length field changes its value.
        # This is a workaround for the fact that we cannot delete all repetitions in a tree, if there

        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue

            if isinstance(failing_tree, BoundsFailingTree):
                assert isinstance(failing_tree.cause, RepetitionBoundsConstraint)
                bounds_constraint: RepetitionBoundsConstraint = failing_tree.cause
                replacements.extend(
                    bounds_constraint.fix_individual(
                        self._grammar,
                        failing_tree,
                        allow_repetition_full_delete=allow_repetition_full_delete,
                    )
                )
                continue

            for operator, value, side in failing_tree.suggestions:
                if operator == Comparison.EQUAL and side == ComparisonSide.LEFT:
                    # LOGGER.debug(f"Parsing {value} into {failing_tree.tree.symbol.symbol!s}")
                    symbol = failing_tree.tree.symbol
                    suggested_tree = None
                    if isinstance(value, DerivationTree) and symbol == value.symbol:
                        suggested_tree = value.deepcopy(
                            copy_children=True, copy_params=False, copy_parent=False
                        )
                        suggested_tree.set_all_read_only(False)
                    elif isinstance(symbol, NonTerminal):
                        suggested_tree = self._grammar.parse(value, start=symbol)
                    elif isinstance(symbol, Slice):
                        # slices don't have a symbol associated with them — I think
                        suggested_tree = self._grammar.parse(value, start="")
                    if suggested_tree is None:
                        continue
                    replacements.append((failing_tree.tree, suggested_tree))
                    fixes_made += 1
        if len(replacements) > 0:
            # Prevent circular replacements
            # deleted = set()
            # for value in set(replacements.values()):
            #    if value in deleted:
            #        continue
            #    if value in replacements.keys():
            #        if replacements[value] not in replacements.keys():
            #            deleted.add(replacements[value])
            #            del replacements[value]
            #            continue
            #        if random.random() < 0.5:
            #            deleted.add(replacements[value])
            #            del replacements[value]
            #        else:
            #            deleted.add(replacements[replacements[value]])
            #            del replacements[replacements[value]]

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
        self.fuzzable_packets: list[ForecastingPacket] | None = None
        self.fallback_packets: list[ForecastingPacket] | None = None
        self.allow_fallback_packets = False

    def _generate_population_hashes(self, population: list[DerivationTree]) -> set[int]:
        hashes: set[int] = set()
        for pop_entry in population:
            deduplicate_tree = pop_entry
            if len(pop_entry.protocol_msgs()) != 0:
                deduplicate_tree = pop_entry.protocol_msgs()[-1].msg
            hashes.add(hash(deduplicate_tree))
        return hashes

    def _generate_population_entry(self, max_nodes: int):
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
