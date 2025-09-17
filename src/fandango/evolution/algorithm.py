# fandango/evolution/algorithm.py
import enum
import itertools
import logging
import random
import time
import warnings
from collections.abc import Callable, Generator
from typing import Iterable, Optional, Union

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.errors import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.evolution import GeneratorWithReturn
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.evolution.crossover import CrossoverOperator, SimpleSubtreeCrossover
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator, SimpleMutation
from fandango.evolution.population import IoPopulationManager, PopulationManager
from fandango.evolution.profiler import Profiler
from fandango.io import FandangoIO, FandangoParty
from fandango.io.packetforecaster import PacketForecaster
from fandango.io.packetparser import parse_next_remote_packet
from fandango.language.grammar import FuzzingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree
from fandango.logger import (
    LOGGER,
    clear_visualization,
    log_message_transfer,
    print_exception,
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
        constraints: list[Union[Constraint, SoftValue]],
        population_size: int = 100,
        initial_population: Optional[list[Union[DerivationTree, str]]] = None,
        expected_fitness: float = 1.0,
        elitism_rate: float = 0.1,
        crossover_method: CrossoverOperator = SimpleSubtreeCrossover(),
        crossover_rate: float = 0.8,
        tournament_size: float = 0.1,
        mutation_method: MutationOperator = SimpleMutation(),
        mutation_rate: float = 0.2,
        destruction_rate: float = 0.0,
        logger_level: Optional[LoggerLevel] = None,
        warnings_are_errors: bool = False,
        best_effort: bool = False,
        random_seed: Optional[int] = None,
        start_symbol: str = "<start>",
        diversity_k: int = 5,
        diversity_weight: float = 1.0,
        max_repetition_rate: float = 0.5,
        max_repetitions: Optional[int] = None,
        max_nodes: int = 200,
        max_nodes_rate: float = 0.5,
        profiling: bool = False,
    ):
        if tournament_size > 1:
            raise FandangoValueError(
                f"Parameter tournament_size must be in range ]0, 1], but is {tournament_size}."
            )
        if random_seed is not None:
            random.seed(random_seed)
        if logger_level is not None:
            LOGGER.setLevel(logger_level.value)
        LOGGER.info("---------- Initializing FANDANGO algorithm ---------- ")

        self.grammar = grammar
        self.constraints = constraints
        self.population_size = population_size
        self.elitism_rate = elitism_rate
        self.destruction_rate = destruction_rate
        self.start_symbol = start_symbol
        self.tournament_size = tournament_size
        self.warnings_are_errors = warnings_are_errors
        self.best_effort = best_effort
        self.remote_response_timeout = 15.0

        # Instantiate managers
        if self.grammar.fuzzing_mode == FuzzingMode.IO:
            self.population_manager: PopulationManager = IoPopulationManager(
                grammar,
                start_symbol,
                warnings_are_errors,
            )
        else:
            self.population_manager = PopulationManager(
                grammar,
                start_symbol,
                warnings_are_errors,
            )
        self.evaluator = Evaluator(
            grammar,
            constraints,
            expected_fitness,
            diversity_k,
            diversity_weight,
            warnings_are_errors,
        )
        self.adaptive_tuner = AdaptiveTuner(
            mutation_rate,
            crossover_rate,
            grammar.get_max_repetition(),
            max_nodes,
            max_repetitions,
            max_repetition_rate,
            max_nodes,
            max_nodes_rate,
        )

        self.profiler = Profiler(enabled=profiling)

        self.crossover_operator = crossover_method
        self.mutation_method = mutation_method

        self.population = self._parse_and_deduplicate(population=initial_population)
        self._initial_solutions, self.evaluation = GeneratorWithReturn(
            self.evaluator.evaluate_population(self.population)
        ).collect()

        self.crossovers_made = 0
        self.fixes_made = 0
        self.mutations_made = 0
        self.time_taken = 0.0

    def _parse_and_deduplicate(
        self, population: Optional[list[Union[DerivationTree, str]]]
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
        st_time = time.time()

        with self.profiler.timer("initial_population") as timer:
            yield from self.population_manager.refill_population(
                current_population=self.population,
                eval_individual=self.evaluator.evaluate_individual,
                max_nodes=self.adaptive_tuner.current_max_nodes,
                target_population_size=self.population_size,
            )

            timer.increment(len(self.population))

        LOGGER.info(
            f"Initial population generated in {time.time() - st_time:.2f} seconds"
        )

        # Evaluate initial population
        with self.profiler.timer("evaluate_population", increment=self.population):
            self.evaluation = yield from self.evaluator.evaluate_population(
                self.population
            )

    def _perform_selection(self) -> tuple[list[DerivationTree], set[int]]:
        """
        Performs selection of the elites from the population.

        :return: A tuple containing the new population and the set of unique hashes of the individuals in the new population.
        """
        # defer increment until data is available
        with self.profiler.timer("select_elites") as timer:
            new_population = self.evaluator.select_elites(
                self.evaluation,
                self.elitism_rate,
                self.population_size,
            )
            timer.increment(len(new_population))

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
            with self.profiler.timer("tournament_selection", increment=2):
                parent1, parent2 = self.evaluator.tournament_selection(
                    evaluation=self.evaluation,
                    tournament_size=max(
                        2, int(self.population_size * self.tournament_size)
                    ),
                )

            with self.profiler.timer("crossover", increment=2):
                crossovers = self.crossover_operator.crossover(
                    self.grammar, parent1, parent2
                )
                to_add = [
                    tree
                    for tree in crossovers
                    if tree.size() <= self.adaptive_tuner.current_max_nodes
                ]

            for i, child in enumerate(to_add):
                if i == 0:
                    PopulationManager.add_unique_individual(
                        new_population, child, unique_hashes
                    )
                    yield from self.evaluator.evaluate_individual(child)
                else:
                    count = len(new_population)
                    with self.profiler.timer("filling") as timer:
                        if len(new_population) < self.population_size:
                            PopulationManager.add_unique_individual(
                                new_population, child, unique_hashes
                            )
                        yield from self.evaluator.evaluate_individual(child)
                        timer.increment(len(new_population) - count)
                self.crossovers_made += 1

        except Exception as e:
            print_exception(e, "Error during crossover")

    def _perform_mutation(
        self, new_population: list[DerivationTree]
    ) -> Generator[DerivationTree, None, None]:
        """
        Performs mutation of the population.

        :param new_population: The new population to perform mutation on.
        """
        mutation_pool = self.evaluator.compute_mutation_pool(new_population)
        mutated_population = []
        for individual in mutation_pool:
            if random.random() < self.adaptive_tuner.mutation_rate:
                try:
                    with self.profiler.timer("mutation", increment=1):
                        mutated_individual = yield from self.mutation_method.mutate(
                            individual,
                            self.grammar,
                            self.evaluator.evaluate_individual,
                        )
                    mutated_population.append(mutated_individual)
                    self.mutations_made += 1
                except Exception as e:
                    LOGGER.error(f"Error during mutation: {e}")
                    print_exception(e, "Error during mutation")
                    mutated_population.append(individual)
            else:
                mutated_population.append(individual)
        new_population.extend(mutated_population)

    def _perform_destruction(
        self, new_population: list[DerivationTree]
    ) -> list[DerivationTree]:
        """
        Randomly destroys a portion of the population.

        :param new_population: The new population to perform destruction on.
        :return: The new population after destruction.
        """
        LOGGER.debug(f"Destroying {self.destruction_rate * 100:.2f}% of the population")
        random.shuffle(new_population)
        return new_population[: int(self.population_size * (1 - self.destruction_rate))]

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

        prev_best_fitness = 0.0
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
            while (
                len(new_population) < self.population_size
                and random.random() < self.adaptive_tuner.crossover_rate
            ):
                yield from self._perform_crossover(new_population, unique_hashes)

            # Truncate if necessary
            if len(new_population) > self.population_size:
                new_population = new_population[: self.population_size]

            # Mutation
            yield from self._perform_mutation(new_population)

            # Destruction
            if self.destruction_rate > 0:
                new_population = self._perform_destruction(new_population)

            # Ensure Uniqueness & Fill Population
            new_population = list(set(new_population))
            yield from self.population_manager.refill_population(
                new_population,
                self.evaluator.evaluate_individual,
                self.adaptive_tuner.current_max_nodes,
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

            with self.profiler.timer("evaluate_population", increment=self.population):
                self.evaluation = yield from self.evaluator.evaluate_population(
                    self.population
                )
                # Keep only the fittest individuals
                self.evaluation = sorted(
                    self.evaluation, key=lambda x: x[1], reverse=True
                )[: self.population_size]

            current_best_fitness = max(e[1] for e in self.evaluation)
            current_max_repetitions = self.grammar.get_max_repetition()
            self.adaptive_tuner.update_parameters(
                generation,
                prev_best_fitness,
                current_best_fitness,
                self.population,
                self.evaluator,
                current_max_repetitions,
            )

            if self.adaptive_tuner.current_max_repetition > current_max_repetitions:
                self.grammar.set_max_repetition(
                    self.adaptive_tuner.current_max_repetition
                )

            prev_best_fitness = current_best_fitness

            self.adaptive_tuner.log_generation_statistics(
                generation, self.evaluation, self.population, self.evaluator
            )
            visualize_evaluation(generation, max_generations, self.evaluation)
        clear_visualization()
        self._log_statistics()

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
                fuzzable_packets = []
                for party in msg_parties:
                    fuzzable_packets.extend(forecast[party].nt_to_packet.values())
                assert isinstance(self.population_manager, IoPopulationManager)
                self.population_manager.fuzzable_packets = fuzzable_packets

                self.population.clear()
                solutions = list(
                    self.population_manager.refill_population(
                        current_population=self.population,
                        eval_individual=self.evaluator.evaluate_individual,
                        max_nodes=self.adaptive_tuner.current_max_nodes,
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
                forecast, packet_tree = parse_next_remote_packet(
                    self.grammar, forecast, io_instance
                )
                log_message_transfer(
                    packet_tree.sender,
                    packet_tree.recipient,
                    packet_tree,
                    False,
                )

                hookin_option = next(iter(forecast.paths))
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

    @property
    def average_population_fitness(self) -> float:
        return sum(e[1] for e in self.evaluation) / self.population_size

    def _log_statistics(self) -> None:
        LOGGER.debug("---------- FANDANGO statistics ----------")
        LOGGER.info(
            f"Average fitness of population: {self.average_population_fitness:.2f}"
        )
        LOGGER.debug(f"Fixes made: {self.fixes_made}")
        LOGGER.debug(f"Fitness checks: {self.evaluator.get_fitness_check_count()}")
        LOGGER.debug(f"Crossovers made: {self.crossovers_made}")
        LOGGER.debug(f"Mutations made: {self.mutations_made}")
        self.profiler.log_results()

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
