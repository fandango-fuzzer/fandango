# fandango/evolution/algorithm.py
import enum
import logging
import random
import time
from typing import List, Union

from fandango import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.constraints.base import Constraint, SoftValue
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.evolution.crossover import CrossoverOperator, SimpleSubtreeCrossover
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator, SimpleMutation
from fandango.evolution.population import PopulationManager, IoPopulationManager
from fandango.language.io import FandangoIO, FandangoParty
from fandango.evolution.profiler import Profiler
from fandango.language.grammar import (
    DerivationTree,
    Grammar,
    FuzzingMode,
)
from fandango.language.packetforecaster import PacketForecaster
from fandango.logger import LOGGER, clear_visualization, visualize_evaluation


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
        constraints: List[Constraint],
        population_size: int = 100,
        desired_solutions: int = 0,
        initial_population: List[Union[DerivationTree, str]] = None,
        max_generations: int = 500,
        expected_fitness: float = 1.0,
        elitism_rate: float = 0.1,
        crossover_method: CrossoverOperator = SimpleSubtreeCrossover(),
        crossover_rate: float = 0.8,
        tournament_size: float = 0.1,
        mutation_method: MutationOperator = SimpleMutation(),
        mutation_rate: float = 0.2,
        destruction_rate: float = 0.0,
        logger_level: LoggerLevel = None,
        warnings_are_errors: bool = False,
        best_effort: bool = False,
        random_seed: int = None,
        start_symbol: str = "<start>",
        diversity_k: int = 5,
        diversity_weight: float = 1.0,
        max_repetition_rate: float = 0.5,
        max_repetitions: int = None,
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

        self.fixes_made = 0
        self.grammar = grammar
        self.constraints = constraints
        self.population_size = max(population_size, desired_solutions)
        self.expected_fitness = expected_fitness
        self.elitism_rate = elitism_rate
        self.destruction_rate = destruction_rate
        self.start_symbol = start_symbol
        self.tournament_size = max(2, int(self.population_size * tournament_size))
        self.max_generations = max_generations
        self.warnings_are_errors = warnings_are_errors
        self.best_effort = best_effort
        self.current_max_nodes = 50

        # Instantiate managers
        if self.grammar.fuzzing_mode == FuzzingMode.IO:
            self.population_manager = IoPopulationManager(
                grammar,
                start_symbol,
                self.population_size,
                self.current_max_nodes,
                warnings_are_errors,
            )
        else:
            self.population_manager = PopulationManager(
                grammar,
                start_symbol,
                self.population_size,
                self.current_max_nodes,
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
            self.current_max_nodes,
            max_repetitions,
            max_repetition_rate,
            max_nodes,
            max_nodes_rate,
        )

        self.profiling = profiling
        if self.profiling:
            self.profiler = Profiler()

        self.crossover_operator = crossover_method
        self.mutation_method = mutation_method

        # Initialize population
        if initial_population is not None:
            LOGGER.info("Saving the provided initial population...")
            unique_population = []
            unique_hashes = set()
            for individual in initial_population:
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
                    raise TypeError(
                        "Initial individuals must be DerivationTree or String"
                    )
                h = hash(tree)
                if h not in unique_hashes:
                    unique_hashes.add(h)
                    unique_population.append(tree)

            attempts = 0
            max_attempts = (self.population_size - len(unique_population)) * 10
            while (
                len(unique_population) < self.population_size
                and attempts < max_attempts
            ):
                candidate = self.fix_individual(
                    self.grammar.fuzz(
                        self.start_symbol, max_nodes=self.current_max_nodes
                    )
                )
                h = hash(candidate)
                if h not in unique_hashes:
                    unique_hashes.add(h)
                    unique_population.append(candidate)
                attempts += 1
            if len(unique_population) < self.population_size:
                LOGGER.warning(
                    f"Could not generate full unique initial population. Final size is {len(unique_population)}."
                )
            self.population = unique_population
        else:
            LOGGER.info(
                f"Generating initial population (size: {self.population_size})..."
            )
            st_time = time.time()

            if self.profiling:
                self.profiler.start_timer("initial_population")
            self.population = (
                self.population_manager.generate_random_initial_population(
                    self.fix_individual
                )
            )
            if self.profiling:
                self.profiler.stop_timer("initial_population")
                self.profiler.increment("initial_population", len(self.population))

            LOGGER.info(
                f"Initial population generated in {time.time() - st_time:.2f} seconds"
            )

        # Evaluate initial population
        if self.profiling:
            self.profiler.start_timer("evaluate_population")
        self.evaluation = self.evaluator.evaluate_population(self.population)
        if self.profiling:
            self.profiler.stop_timer("evaluate_population")
            self.profiler.increment("evaluate_population", len(self.population))
        self.fitness = (
            sum(fitness for _, fitness, _ in self.evaluation) / self.population_size
        )

        self.fixes_made = 0
        self.checks_made = self.evaluator.checks_made
        self.crossovers_made = 0
        self.mutations_made = 0
        self.time_taken = None
        self.solution = self.evaluator.solution
        self.solution_set = self.evaluator.solution_set
        self.desired_solutions = desired_solutions

    def fix_individual(
        self, individual: DerivationTree
    ) -> tuple[float, DerivationTree]:
        _, failing_trees = self.evaluator.evaluate_individual(individual)
        replacements = dict()
        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue
            for operator, value, side in failing_tree.suggestions:
                from fandango.constraints.fitness import Comparison, ComparisonSide

                # LOGGER.debug(f"Parsing {value} into {failing_tree.tree.symbol.symbol!s}")
                if operator == Comparison.EQUAL and isinstance(
                    value, (str, bytes, DerivationTree)
                ):
                    if side == ComparisonSide.RIGHT:
                        continue
                    if (
                        isinstance(value, DerivationTree)
                        and failing_tree.tree.symbol == value.symbol
                    ):
                        suggested_tree = value.__deepcopy__(None, True, False, False)
                        suggested_tree.set_all_read_only(False)
                    else:
                        suggested_tree = self.grammar.parse(
                            value, start=failing_tree.tree.symbol.symbol
                        )
                    if suggested_tree is None:
                        continue
                    replacements[failing_tree.tree] = suggested_tree
                    self.fixes_made += 1
        if len(replacements) > 0:
            individual = individual.replace_multiple(self.grammar, replacements)
        return individual

    def log_message_transfer(
        self,
        sender: str,
        receiver: str | None,
        msg: DerivationTree,
        self_is_sender: bool,
    ):
        if receiver is None:
            if self_is_sender:
                receiver = "Unknown"
            else:
                receiver = "Fandango"
        if self_is_sender:
            sender = "*" + sender
        else:
            receiver = "*" + receiver

        if msg.contains_bytes():
            msg = msg.to_bytes()
        else:
            msg = msg.to_string()

        LOGGER.info(f"({sender} -> {receiver}): {msg}")

    def _evolve_io(self) -> List[DerivationTree]:
        global_env, local_env = self.grammar.get_python_env()
        io_instance: FandangoIO = global_env["FandangoIO"].instance()
        history_tree: DerivationTree = random.choice(self.population)

        self.desired_solutions = 1
        while True:
            self.population.clear()
            self.evaluator.reset()
            self.solution.clear()
            self.solution_set.clear()
            forecaster = PacketForecaster(self.grammar)
            forecast = forecaster.predict(history_tree)

            if len(forecast.getMsgParties()) == 0:
                if len(history_tree.find_protocol_msgs()) == 0:
                    raise RuntimeError("Couldn't forecast next packet!")
                return [history_tree]

            msg_parties = []
            for party in forecast.getMsgParties():
                if io_instance.parties[party].is_fandango():
                    msg_parties.append(party)
            if len(msg_parties) != 0 and not io_instance.received_msg():
                fuzzable_packets = []
                for party in msg_parties:
                    fuzzable_packets.extend(forecast[party].nt_to_packet.values())
                self.population_manager.fuzzable_packets = fuzzable_packets

                new_population = (
                    self.population_manager.generate_random_initial_population(
                        self.fix_individual
                    )
                )

                self.population = new_population
                self.evaluation = self.evaluator.evaluate_population(self.population)
                self.fitness = (
                    sum(fitness for _, fitness, _ in self.evaluation)
                    / self.population_size
                )

                evolve_result = self._evolve_single()
                if len(evolve_result) == 0:
                    nonterminals_str = " | ".join(
                        map(lambda x: str(x.node.symbol), fuzzable_packets)
                    )
                    raise RuntimeError(
                        f"Couldn't find solution for any packet: {nonterminals_str}"
                    )
                next_tree = evolve_result[0]
                if io_instance.received_msg():
                    # Abort if we received a message during fuzzing
                    continue
                new_packet = next_tree.find_protocol_msgs()[-1]
                if (
                    new_packet.recipient is None
                    or not io_instance.parties[new_packet.recipient].is_fandango()
                ):
                    io_instance.set_transmit(
                        new_packet.sender, new_packet.recipient, new_packet.msg
                    )
                    self.log_message_transfer(
                        new_packet.sender, new_packet.recipient, new_packet.msg, True
                    )
                    exec("FandangoIO.instance().run_com_loop()", global_env, local_env)
                history_tree = next_tree
            else:
                while not io_instance.received_msg():
                    time.sleep(0.025)
                forecast, packet_tree = self._parse_next_remote_packet(
                    forecast, io_instance
                )
                self.log_message_transfer(
                    packet_tree.sender,
                    packet_tree.recipient,
                    packet_tree,
                    False,
                )

                hookin_option = next(iter(forecast.paths))
                history_tree = hookin_option.tree
                history_tree.append(hookin_option.path[1:], packet_tree)
                fitness, eval_report = self.evaluator.evaluate_individual(history_tree)
                if fitness < 0.99:
                    raise RuntimeError("Remote response doesn't match constraints!")
                self.solution.clear()
            history_tree.set_all_read_only(True)

    def evolve(self) -> List[DerivationTree]:
        if self.grammar.fuzzing_mode == FuzzingMode.COMPLETE:
            return self._evolve_single()
        elif self.grammar.fuzzing_mode == FuzzingMode.IO:
            return self._evolve_io()
        else:
            raise RuntimeError(f"Invalid mode: {self.grammar.fuzzing_mode}")

    def _evolve_single(self) -> List[DerivationTree]:
        LOGGER.info("---------- Starting evolution ----------")
        start_time = time.time()
        prev_best_fitness = 0.0

        for generation in range(1, self.max_generations + 1):
            if 0 < self.desired_solutions <= len(self.solution):
                self.fitness = 1.0
                temp_solution = self.solution[: self.desired_solutions]
                self.solution.clear()
                self.solution.extend(temp_solution)
                break
            if len(self.solution) >= self.population_size:
                self.fitness = 1.0
                temp_solution = self.solution[: self.population_size]
                self.solution.clear()
                self.solution.extend(temp_solution)
                break
            if self.fitness >= self.expected_fitness:
                self.fitness = 1.0
                temp_solution = self.population[: self.population_size]
                self.solution.clear()
                self.solution.extend(temp_solution)
                break

            LOGGER.info(
                f"Generation {generation} - Fitness: {self.fitness:.2f} - #solutions found: {len(self.solution)}"
            )

            # Selection & Crossover
            if self.profiling:
                self.profiler.start_timer("select_elites")
            new_population = self.evaluator.select_elites(
                self.evaluation, self.elitism_rate, self.population_size
            )
            if self.profiling:
                self.profiler.stop_timer("select_elites")
                self.profiler.increment("select_elites", len(new_population))

            unique_hashes = {hash(ind) for ind in new_population}

            while len(new_population) < self.population_size:
                if random.random() < self.adaptive_tuner.crossover_rate:
                    try:
                        if self.profiling:
                            self.profiler.start_timer("tournament_selection")
                        parent1, parent2 = self.evaluator.tournament_selection(
                            self.evaluation, self.tournament_size
                        )
                        if self.profiling:
                            self.profiler.stop_timer("tournament_selection")
                            self.profiler.increment("tournament_selection", 2)

                        if self.profiling:
                            self.profiler.start_timer("crossover")
                        child1, child2 = self.crossover_operator.crossover(
                            self.grammar, parent1, parent2
                        )
                        if self.profiling:
                            self.profiler.stop_timer("crossover")
                            self.profiler.increment("crossover", 2)

                        self.population_manager.add_unique_individual(
                            new_population, child1, unique_hashes
                        )
                        self.evaluator.evaluate_individual(child1)

                        if self.profiling:
                            self.profiler.start_timer("filling")
                            count = len(new_population)
                        if len(new_population) < self.population_size:
                            self.population_manager.add_unique_individual(
                                new_population, child2, unique_hashes
                            )
                            self.evaluator.evaluate_individual(child2)

                        if self.profiling:
                            self.profiler.stop_timer("filling")
                            self.profiler.increment(
                                "filling", len(new_population) - count
                            )
                        self.crossovers_made += 2
                    except Exception as e:
                        LOGGER.error(f"Error during crossover: {e}")
                        continue
                else:
                    break

            if len(new_population) > self.population_size:
                new_population = new_population[: self.population_size]

            # Mutation
            weights = [
                self.evaluator.fitness_cache[hash(ind)][0] for ind in new_population
            ]
            if not all(w == 0 for w in weights):
                mutation_pool = random.choices(
                    new_population, weights=weights, k=len(new_population)
                )
            else:
                mutation_pool = new_population
            mutated_population = []
            for individual in mutation_pool:
                if random.random() < self.adaptive_tuner.mutation_rate:
                    try:
                        if self.profiling:
                            self.profiler.start_timer("mutation")

                        mutated_individual = self.mutation_method.mutate(
                            individual,
                            self.grammar,
                            self.evaluator.evaluate_individual,
                            self.current_max_nodes,
                        )
                        if self.profiling:
                            self.profiler.stop_timer("mutation")
                            self.profiler.increment("mutation", 1)
                        mutated_population.append(mutated_individual)
                        self.mutations_made += 1
                    except Exception as e:
                        LOGGER.error(f"Error during mutation: {e}")
                        mutated_population.append(individual)
                else:
                    mutated_population.append(individual)
            new_population.extend(mutated_population)

            # Destruction
            if self.destruction_rate > 0:
                LOGGER.debug(
                    f"Destroying {self.destruction_rate * 100:.2f}% of the population"
                )
                random.shuffle(new_population)
                new_population = new_population[
                    : int(self.population_size * (1 - self.destruction_rate))
                ]
                unique_hashes = {hash(ind) for ind in new_population}

            # Ensure Uniqueness & Fill Population
            unique_temp = {}
            for ind in new_population:
                unique_temp[hash(ind)] = ind
            new_population = list(unique_temp.values())
            new_population = self.population_manager.refill_population(
                new_population, self.fix_individual
            )

            self.population = [self.fix_individual(ind) for ind in new_population]

            if any(isinstance(c, SoftValue) for c in self.constraints):
                # For soft constraints, the normalized fitness may change over time as we observe more inputs.
                # Hence, we periodically flush the fitness cache to re-evaluate the population.
                self.evaluator.fitness_cache = {}

            if self.profiling:
                self.profiler.start_timer("evaluate_population")
            self.evaluation = self.evaluator.evaluate_population(self.population)
            # Keep only the fittest individuals
            self.evaluation = sorted(self.evaluation, key=lambda x: x[1], reverse=True)[
                : self.population_size
            ]
            if self.profiling:
                self.profiler.stop_timer("evaluate_population")
                self.profiler.increment("evaluate_population", len(self.population))
            self.fitness = (
                sum(fitness for _, fitness, _ in self.evaluation) / self.population_size
            )

            current_best_fitness = max(fitness for _, fitness, _ in self.evaluation)
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

            self.population_manager.max_nodes = self.adaptive_tuner.current_max_nodes
            self.current_max_nodes = self.adaptive_tuner.current_max_nodes

            prev_best_fitness = current_best_fitness

            self.adaptive_tuner.log_generation_statistics(
                generation, self.evaluation, self.population, self.evaluator
            )
            visualize_evaluation(generation, self.max_generations, self.evaluation)

        clear_visualization()
        self.time_taken = time.time() - start_time
        LOGGER.info("---------- Evolution finished ----------")
        LOGGER.info(f"Perfect solutions found: ({len(self.solution)})")
        LOGGER.info(f"Fitness of final population: {self.fitness:.2f}")
        LOGGER.info(f"Time taken: {self.time_taken:.2f} seconds")
        LOGGER.debug("---------- FANDANGO statistics ----------")
        LOGGER.debug(f"Fixes made: {self.fixes_made}")
        LOGGER.debug(f"Fitness checks: {self.checks_made}")
        LOGGER.debug(f"Crossovers made: {self.crossovers_made}")
        LOGGER.debug(f"Mutations made: {self.mutations_made}")

        if self.profiling:
            self.profiler.log_results()

        if self.fitness < self.expected_fitness:
            LOGGER.error("Population did not converge to a perfect population")
            if self.warnings_are_errors:
                raise FandangoFailedError("Failed to find a perfect solution")
            if self.best_effort:
                return self.population

        if self.desired_solutions > 0 and len(self.solution) < self.desired_solutions:
            LOGGER.error(
                f"Only found {len(self.solution)} perfect solutions, instead of the required {self.desired_solutions}"
            )
            if self.warnings_are_errors:
                raise FandangoFailedError(
                    "Failed to find the required number of perfect solutions"
                )
            if self.best_effort:
                return self.population[: self.desired_solutions]

        return self.solution

    def msg_parties(self) -> List[FandangoParty]:
        global_env, local_env = self.grammar.get_python_env()
        io_instance: FandangoIO = global_env["FandangoIO"].instance()
        return list(io_instance.parties.values())

    def _parse_next_remote_packet(
        self, forecast: PacketForecaster.ForcastingResult, io_instance: FandangoIO
    ):
        if len(io_instance.get_received_msgs()) == 0:
            return None, None

        complete_msg = None
        used_fragments_idx = []
        next_fragment_idx = 0

        found_start = False
        selection_rounds = 0
        msg_sender = "None"
        while not found_start and selection_rounds < 20:
            for start_idx, (msg_sender, msg_recipient, _) in enumerate(
                io_instance.get_received_msgs()
            ):
                next_fragment_idx = start_idx
                if msg_sender in forecast.getMsgParties():
                    found_start = True
                    break

            if not found_start and len(io_instance.get_received_msgs()) != 0:
                raise FandangoValueError(
                    f"Unexpected party sent message. Expected: "
                    + " | ".join(forecast.getMsgParties())
                    + f". Received: {msg_sender}."
                    + f" Messages: {io_instance.get_received_msgs()}"
                )
            time.sleep(0.025)

        forecast_non_terminals = forecast[msg_sender]
        available_non_terminals = set(forecast_non_terminals.getNonTerminals())

        is_msg_complete = False

        elapsed_rounds = 0
        max_rounds = 0.025 * 2000
        failed_parameter_parsing = False
        parameter_parsing_exception = None

        while not is_msg_complete:
            for idx, (sender, recipient, msg_fragment) in enumerate(
                io_instance.get_received_msgs()[next_fragment_idx:]
            ):
                abs_msg_idx = next_fragment_idx + idx

                if msg_sender != sender:
                    continue
                if complete_msg is None:
                    complete_msg = msg_fragment
                else:
                    complete_msg += msg_fragment
                used_fragments_idx.append(abs_msg_idx)

                parsed_packet_tree = None
                forecast_packet = None
                for non_terminal in set(available_non_terminals):
                    forecast_packet = forecast_non_terminals[non_terminal]
                    path = random.choice(list(forecast_packet.paths))
                    hookin_tree = path.tree
                    path = list(
                        map(lambda x: x[0], filter(lambda x: not x[1], path.path))
                    )
                    hookin_point = hookin_tree.get_last_by_path(path)
                    parsed_packet_tree = self.grammar.parse(
                        complete_msg,
                        forecast_packet.node.symbol,
                        hookin_parent=hookin_point,
                    )

                    if parsed_packet_tree is not None:
                        parsed_packet_tree.sender = forecast_packet.node.sender
                        parsed_packet_tree.recipient = forecast_packet.node.recipient
                        try:
                            self.grammar.populate_sources(parsed_packet_tree)
                            break
                        except FandangoParseError as e:
                            parsed_packet_tree = None
                            failed_parameter_parsing = True
                            parameter_parsing_exception = e
                    incomplete_tree = self.grammar.parse(
                        complete_msg,
                        forecast_packet.node.symbol,
                        mode=Grammar.Parser.ParsingMode.INCOMPLETE,
                        hookin_parent=hookin_point,
                    )
                    if incomplete_tree is None:
                        available_non_terminals.remove(non_terminal)

                # Check if there are still NonTerminals that can be parsed with received prefix
                if len(available_non_terminals) == 0:
                    raise RuntimeError(
                        "Couldn't match remote message to any packet matching grammar! Expected nonterminal:",
                        "|".join(
                            map(
                                lambda x: str(x),
                                forecast_non_terminals.getNonTerminals(),
                            )
                        ),
                        "Got message:",
                        complete_msg,
                        "\nUnprocessed messages: ",
                        str(io_instance.get_received_msgs()),
                    )
                if parsed_packet_tree is not None:
                    nr_deleted = 0
                    used_fragments_idx.sort()
                    for del_idx in used_fragments_idx:
                        io_instance.clear_received_msg(del_idx - nr_deleted)
                        nr_deleted += 1
                    return forecast_packet, parsed_packet_tree

            if not is_msg_complete:
                elapsed_rounds += 1
                if elapsed_rounds >= max_rounds:
                    if failed_parameter_parsing:
                        applicable_nt = list(
                            map(lambda x: str(x.symbol), available_non_terminals)
                        )
                        if len(applicable_nt) == 0:
                            applicable_nt = "None"
                        else:
                            applicable_nt = ", ".join(applicable_nt)
                        raise FandangoFailedError(
                            f'Couldn\'t derive parameters for received packet or timed out while waiting for remaining packet. Applicable NT: {applicable_nt} Received part: "{complete_msg}". Exception: {str(parameter_parsing_exception)}'
                        )
                    else:
                        raise FandangoFailedError(
                            f"Incomplete packet received. Timed out while waiting for packet. Received part: {complete_msg}"
                        )
                time.sleep(0.025)
        return None

    def select_elites(self) -> List[DerivationTree]:
        return [
            x[0]
            for x in sorted(self.evaluation, key=lambda x: x[1], reverse=True)[
                : int(self.elitism_rate * self.population_size)
            ]
        ]
