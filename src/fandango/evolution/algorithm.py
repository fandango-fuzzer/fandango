# fandango/evolution/algorithm.py
import enum
import itertools
import logging
import random
import time
import warnings
from collections.abc import Callable, Generator
from typing import Iterable, Optional

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.crossover import SimpleSubtreeCrossover, CrossoverOperator
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.hyperparameter import HyperparameterManager
from fandango.evolution.mutation import SimpleMutation, MutationOperator
from fandango.evolution.population import IoPopulationManager, PopulationManager
from fandango.io import FandangoIO
from fandango.io.packetforecaster import ForcastingPacket, PacketForecaster
from fandango.io.packetparser import parse_next_remote_packet
from fandango.language.grammar import FuzzingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree
from fandango.logger import (
    LOGGER,
    clear_visualization,
    log_message_transfer,
    visualize_evaluation,
)


class LoggerLevel(enum.Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Fandango:
    def __init__(
        self,
        grammar: Grammar,
        # TODO: can we rename SoftValue to SoftConstraint to be more consistent? and Constraint to HardConstraint? Both inherit from BaseConstraint?
        constraints: list[Constraint | SoftValue],
        population_size: int = 100,
        initial_population: Optional[list[DerivationTree | str]] = None,
        elitism_rate: float = 0.1,
        crossover_method: CrossoverOperator = SimpleSubtreeCrossover(),
        crossover_rate: float = 0.8,
        tournament_size: float = 0.1,
        mutation_method: MutationOperator = SimpleMutation(),
        mutation_rate: float = 0.2,
        destruction_rate: float = 0.0,
        logger_level: Optional[LoggerLevel] = None,
        random_seed: Optional[int] = None,
        max_nodes: Optional[int] = 100,
        max_repetitions: Optional[int] = 100,
    ):
        if 0 >= tournament_size > 1:
            raise FandangoValueError(
                f"Parameter tournament_size must be in range (0, 1], but is {tournament_size}."
            )
        if random_seed is not None:
            random.seed(random_seed)
        if logger_level is not None:
            LOGGER.setLevel(logger_level.value)
        LOGGER.info("---------- Initializing FANDANGO algorithm ---------- ")

        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size

        self.hyperparameter_manager = HyperparameterManager(
            elitism_rate,
            tournament_size,
            crossover_rate,
            mutation_rate,
            destruction_rate,
            max_nodes,
            max_repetitions,
        )

        self.crossover_operator = crossover_method
        self.mutation_method = mutation_method

        # Instantiate managers
        if self.grammar.fuzzing_mode == FuzzingMode.COMPLETE:
            self.population_manager: PopulationManager = PopulationManager(
                grammar,
            )
        elif self.grammar.fuzzing_mode == FuzzingMode.IO:
            self.population_manager: PopulationManager = IoPopulationManager(
                grammar,
            )
            self.remote_response_timeout = 15.0
        else:
            raise FandangoValueError(
                f"Invalid fuzzing mode: {self.grammar.fuzzing_mode}"
            )

        self.evaluator = Evaluator(
            grammar,
            constraints,
        )

        self.population = self._parse_and_deduplicate(population=initial_population)
        self._initial_solutions, self.evaluation = GeneratorWithReturn(
            self.evaluator.evaluate_population(self.population)
        ).collect()

        self.crossovers_made = 0
        self.fixes_made = 0
        self.mutations_made = 0
        self.time_taken = 0.0

    def _parse_and_deduplicate(
        self, population: Optional[list[DerivationTree | str]]
    ) -> list[DerivationTree]:
        """
        Parses and deduplicates the initial population along unique parse trees. If no initial population is provided, an empty list is returned.

        :param population: The initial population to parse and deduplicate.
        :return: A list of unique parse trees.
        """
        if population is None:
            return []
        LOGGER.info("Deduplicating the provided initial population...")
        unique_population: list[DerivationTree] = []
        unique_hashes: set[int] = set()
        for individual in population:
            if isinstance(individual, str):
                tree = self.grammar.parse(individual)
                if not tree:
                    position = self.grammar.max_position()
                    raise FandangoParseError(
                        message=f"Failed to parse initial individual{individual!r}",
                        position=position,
                    )
            elif isinstance(individual, DerivationTree):
                tree = individual
            else:
                raise TypeError("Initial individuals must be DerivationTree or String")
            PopulationManager.add_unique_individual(
                population=unique_population, candidate=tree, unique_set=unique_hashes
            )
        return unique_population

    def generate_initial_population(self) -> Generator[DerivationTree, None, None]:
        """
        Extends the population to the target size. Does not perform fixes.

        `.generate` will call this if necessary. If you don't know what you're doing, you probably don't need to call this.

        Since this is a generator, it will only do its job if the generator is actually used. Call `list(fandango.generate_initial_population())` to ensure the generator runs until the end.

        :return: A generator of DerivationTree objects, all of which are valid solutions to the grammar (or satisify the minimum fitness threshold).
        """
        LOGGER.info(
            f"Generating (additional) initial population (size: {self.population_size - len(self.population)})..."
        )

        yield from self.population_manager.refill_population(
            current_population=self.population,
            eval_individual=self.evaluator.evaluate_individual,
            max_nodes=self.hyperparameter_manager.max_nodes,
            target_population_size=self.population_size,
        )

        # Evaluate initial population
        self.evaluation = yield from self.evaluator.evaluate_population(self.population)

    def _perform_selection(self) -> tuple[list[DerivationTree], set[int]]:
        """
        Performs selection of the elites from the population.

        :return: A tuple containing the new population and the set of unique hashes of the individuals in the new population.
        """
        new_population = self.evaluator.select_elites(
            self.evaluation,
            self.hyperparameter_manager.elitism_rate,
            self.population_size,
        )

        unique_hashes = {hash(ind) for ind in new_population}
        return new_population, unique_hashes

    def _perform_crossover(
        self, new_population: list[DerivationTree], unique_hashes: set[int]
    ) -> Generator[DerivationTree, None, None]:
        """
        Performs crossover of the population.

        :param new_population: The new population to perform crossover on.
        :param unique_hashes: The set of unique hashes of the individuals in the new population.
        """
        if len(self.evaluation) < 2:
            return None
        try:
            parent1, parent2 = self.evaluator.tournament_selection(
                evaluation=self.evaluation,
                tournament_size=max(
                    2,
                    int(
                        self.population_size
                        * self.hyperparameter_manager.tournament_size
                    ),
                ),
            )

            crossovers = self.crossover_operator.crossover(
                self.grammar, parent1, parent2
            )
            if crossovers is None:
                return None

            to_add = [
                tree
                for tree in crossovers
                if tree.size() <= self.hyperparameter_manager.max_nodes
            ]

            for i, child in enumerate(to_add):
                if i == 0:
                    PopulationManager.add_unique_individual(
                        new_population, child, unique_hashes
                    )
                    yield from self.evaluator.evaluate_individual(child)
                else:
                    if len(new_population) < self.population_size:
                        PopulationManager.add_unique_individual(
                            new_population, child, unique_hashes
                        )
                    yield from self.evaluator.evaluate_individual(child)
                self.crossovers_made += 1

        except Exception as e:
            LOGGER.error(f"Error during crossover: {e}")

    def _perform_mutation(
        self, population: list[DerivationTree]
    ) -> Generator[DerivationTree, None, None]:
        """
        Performs mutation of the population.

        :param population: The new population to perform mutation on.

        :return: A generator of mutated DerivationTree objects.
        """
        mutated_population: list[DerivationTree] = []
        for individual in population:
            if random.random() < self.hyperparameter_manager.mutation_rate:
                try:
                    mutated_individual = yield from self.mutation_method.mutate(
                        individual,
                        self.grammar,
                        self.evaluator.evaluate_individual,
                        self.hyperparameter_manager.max_nodes,
                    )
                    mutated_population.append(mutated_individual)
                except Exception as e:
                    LOGGER.error(f"Error during mutation: {e}")
            else:
                mutated_population.append(individual)

    def _perform_destruction(
        self, new_population: list[DerivationTree]
    ) -> list[DerivationTree]:
        """
        Randomly destroys a portion of the population.

        :param new_population: The new population to perform destruction on.
        :return: The new population after destruction.
        """
        LOGGER.debug(
            f"Destroying {self.hyperparameter_manager.destruction_rate * 100:.2f}% of the population"
        )
        random.shuffle(new_population)
        return new_population[
            : int(
                self.population_size
                * (1 - self.hyperparameter_manager.destruction_rate)
            )
        ]

    def evolve(
        self,
        max_generations: Optional[int] = None,
        desired_solutions: Optional[int] = None,
        solution_callback: Callable[[DerivationTree, int], None] = lambda _a, _b: None,
    ) -> list[DerivationTree]:
        """
        Evolves the population of the grammar.

        If both max_generations and desired_solutions are provided, the generation will run until either the maximum number of generations is reached or the desired number of solutions is found. If neither is provided, the generation will run indefinitely.

        TODO: go into more details about Fandango IO mode.

        :param max_generations: The maximum number of generations to evolve.
        :param desired_solutions: The number of solutions to evolve.
        :param solution_callback: A callback function to be called for each solution.
        :return: A list of DerivationTree objects, all of which are valid solutions to the grammar (or satisify the minimum fitness threshold). The function may run indefinitely if neither max_generations nor desired_solutions are provided.
        """
        warnings.warn("Use .generate instead", DeprecationWarning)
        if self.grammar.fuzzing_mode == FuzzingMode.COMPLETE:
            return self._evolve_single(
                max_generations, desired_solutions, solution_callback
            )
        elif self.grammar.fuzzing_mode == FuzzingMode.IO:
            return self._evolve_io(max_generations)
        else:
            raise FandangoValueError(f"Invalid mode: {self.grammar.fuzzing_mode}")

    def _evolve_io(self, max_generations: Optional[int] = None) -> list[DerivationTree]:
        warnings.warn("Use .generate instead", DeprecationWarning)
        return list(self._generate_io(max_generations=max_generations))

    def generate(
        self,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
    ) -> Generator[DerivationTree, None, None]:
        match mode:
            case FuzzingMode.COMPLETE:
                yield from self._generate_simple(max_generations=max_generations)
            case FuzzingMode.IO:
                yield from self._generate_io(max_generations=max_generations)
            case _:
                raise RuntimeError(f"Fuzzing Mode {mode} is not implemented")

    def _generate_simple(
        self, max_generations: Optional[int] = None
    ) -> Generator[DerivationTree, None, None]:
        """
        Generates solutions for the grammar.

        :param max_generations: The maximum number of generations to generate. If None, the generation will run indefinitely.
        :return: A generator of DerivationTree objects, all of which are valid solutions to the grammar (or satisify the minimum fitness threshold).
        """
        while self._initial_solutions:
            yield self._initial_solutions.pop(0)

        if len(self.population) < self.population_size:
            yield from self.generate_initial_population()

        generation = 0

        while True:
            if max_generations is not None and generation >= max_generations:
                break
            generation += 1

            avg_fitness = sum(e[1] for e in self.evaluation) / self.population_size

            LOGGER.info(f"Generation {generation} - Average Fitness: {avg_fitness:.2f}")

            # Selection
            new_population, unique_hashes = self._perform_selection()

            # Crossover
            for _ in range(self.population_size):
                if len(new_population) >= self.population_size:
                    break
                if random.random() < self.hyperparameter_manager.crossover_rate:
                    yield from self._perform_crossover(new_population, unique_hashes)

            # Truncate if necessary
            if len(new_population) > self.population_size:
                new_population = new_population[: self.population_size]

            # Mutation
            yield from self._perform_mutation(new_population)

            # Destruction
            if self.hyperparameter_manager.destruction_rate > 0:
                new_population = self._perform_destruction(new_population)

            # Ensure Uniqueness & Fill Population
            new_population = list(set(new_population))
            yield from self.population_manager.refill_population(
                new_population,
                self.evaluator.evaluate_individual,
                self.hyperparameter_manager.max_nodes,
                self.population_size,
            )

            self.population = []
            for ind in new_population:
                _fitness, failing_trees = yield from self.evaluator.evaluate_individual(
                    ind
                )
                ind, num_fixes = self.population_manager.fix_individual(
                    ind, failing_trees
                )
                self.population.append(ind)
                self.fixes_made += num_fixes

            # For soft constraints, the normalized fitness may change over time as we observe more inputs.
            # Hence, we periodically flush the fitness cache to re-evaluate the population if the grammar contains soft constraints.
            self.evaluator.flush_fitness_cache()

            self.evaluation = yield from self.evaluator.evaluate_population(
                self.population
            )
            # Keep only the fittest individuals
            self.evaluation = sorted(self.evaluation, key=lambda x: x[1], reverse=True)[
                : self.population_size
            ]

            self.hyperparameter_manager.adjust_hyperparameters()

            visualize_evaluation(generation, max_generations, self.evaluation)
        clear_visualization()

    def _generate_io(
        self, max_generations: Optional[int] = None
    ) -> Generator[DerivationTree, None, None]:
        if len(self.population) < self.population_size:
            list(
                self.generate_initial_population()
            )  # ensure the generator runs until the end

        spec_env_global, _ = self.grammar.get_spec_env()
        io_instance: FandangoIO = spec_env_global["FandangoIO"].instance()
        history_tree: DerivationTree = random.choice(self.population)
        forecaster = PacketForecaster(self.grammar)

        while True:
            forecast = forecaster.predict(history_tree)

            if len(forecast.get_msg_parties()) == 0:
                if len(history_tree.protocol_msgs()) == 0:
                    raise FandangoFailedError("Could not forecast next packet")
                yield history_tree
                return
                # TODO: Reset for next iteration

            msg_parties = list(
                filter(
                    lambda x: io_instance.parties[x].is_fuzzer_controlled(),
                    forecast.get_msg_parties(),
                )
            )
            if len(msg_parties) != 0 and not io_instance.received_msg():
                fuzzable_packets: list[ForcastingPacket] = []
                for party in msg_parties:
                    fuzzable_packets.extend(forecast[party].nt_to_packet.values())
                assert isinstance(self.population_manager, IoPopulationManager)
                self.population_manager.fuzzable_packets = fuzzable_packets

                self.population.clear()
                solutions = list(
                    self.population_manager.refill_population(
                        current_population=self.population,
                        eval_individual=self.evaluator.evaluate_individual,
                        max_nodes=self.hyperparameter_manager.max_nodes,
                        target_population_size=self.population_size,
                    )
                )
                if not solutions:
                    solutions, self.evaluation = GeneratorWithReturn(
                        self.evaluator.evaluate_population(self.population)
                    ).collect()

                if not solutions:
                    try:
                        evolve_result = next(
                            self.generate(max_generations=max_generations)
                        )
                    except StopIteration:
                        nonterminals_str = " | ".join(
                            map(lambda x: str(x.node.symbol), fuzzable_packets)
                        )
                        raise FandangoFailedError(
                            f"Couldn't find solution for any packet: {nonterminals_str}"
                        )
                    next_tree = evolve_result
                else:
                    next_tree = solutions[0]
                if io_instance.received_msg():
                    # Abort if we received a message during fuzzing
                    continue
                new_packet = next_tree.protocol_msgs()[-1]
                if (
                    new_packet.recipient is None
                    or not io_instance.parties[
                        new_packet.recipient
                    ].is_fuzzer_controlled()
                ):
                    io_instance.transmit(
                        new_packet.sender, new_packet.recipient, new_packet.msg
                    )
                    log_message_transfer(
                        new_packet.sender, new_packet.recipient, new_packet.msg, True
                    )
                history_tree = next_tree
            else:
                wait_start = time.time()
                while not io_instance.received_msg():
                    if time.time() - wait_start > self.remote_response_timeout:
                        raise FandangoFailedError(
                            f"Timed out while waiting for message from remote party. Expected message from party: {', '.join(forecast.get_msg_parties())}"
                        )
                    time.sleep(0.025)
                forecast_packet, packet_tree = parse_next_remote_packet(
                    self.grammar, forecast, io_instance
                )
                assert forecast_packet is not None
                assert packet_tree is not None
                assert packet_tree.sender is not None
                log_message_transfer(
                    packet_tree.sender,
                    packet_tree.recipient,
                    packet_tree,
                    False,
                )

                hookin_option = next(iter(forecast_packet.paths))
                assert hookin_option.tree is not None
                history_tree = hookin_option.tree
                history_tree.append(hookin_option.path[1:], packet_tree)
                solutions, (fitness, _failing_trees) = GeneratorWithReturn(
                    self.evaluator.evaluate_individual(history_tree)
                ).collect()
                if fitness < 0.99:
                    raise FandangoParseError(
                        "Remote response does not match constraints"
                    )
            history_tree.set_all_read_only(True)

    def _evolve_single(
        self,
        max_generations: Optional[int] = None,
        desired_solutions: Optional[int] = None,
        solution_callback: Callable[[DerivationTree, int], None] = lambda _a, _b: None,
    ) -> list[DerivationTree]:
        LOGGER.info("---------- Starting evolution ----------")

        solutions: list[DerivationTree] = []

        start_time = time.time()
        gen: Iterable[DerivationTree] = self.generate(max_generations)
        if desired_solutions is not None:
            gen = itertools.islice(gen, desired_solutions)

        for solution in gen:
            solutions.append(solution)
            solution_callback(solution, len(solutions))
        LOGGER.info(f"Time taken: {(time.time() - start_time):.2f} seconds")

        return solutions
