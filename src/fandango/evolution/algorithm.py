# fandango/evolution/algorithm.py
import enum
import logging
import random
import time
from typing import List, Union

from copy import deepcopy
from fandango.constraints.base import Constraint
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.evolution.crossover import CrossoverOperator, SimpleSubtreeCrossover
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator, SimpleMutation
from fandango.evolution.population import PopulationManager
from fandango.language.io import FandangoIO
from fandango.language.grammar import (
    DerivationTree,
    Grammar,
    FuzzingMode,
    PacketForecaster,
)
from fandango.language.symbol import NonTerminal
from fandango.language.tree import RoledMessage
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
    ):
        if tournament_size > 1:
            raise ValueError(
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
        self.population_size = population_size
        self.expected_fitness = expected_fitness
        self.elitism_rate = elitism_rate
        self.destruction_rate = destruction_rate
        self.start_symbol = start_symbol
        self.tournament_size = max(2, int(population_size * tournament_size))
        self.max_generations = max_generations
        self.warnings_are_errors = warnings_are_errors
        self.best_effort = best_effort

        # Instantiate managers
        self.population_manager = PopulationManager(
            grammar, start_symbol, population_size, warnings_are_errors
        )
        self.evaluator = Evaluator(
            grammar,
            constraints,
            expected_fitness,
            diversity_k,
            diversity_weight,
            warnings_are_errors,
        )
        self.adaptive_tuner = AdaptiveTuner(mutation_rate, crossover_rate)
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
                        raise ValueError(
                            f"Failed to parse initial individual: {individual}"
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
            max_attempts = (population_size - len(unique_population)) * 10
            while len(unique_population) < population_size and attempts < max_attempts:
                candidate = self.fix_individual(self.grammar.fuzz(self.start_symbol))
                h = hash(candidate)
                if h not in unique_hashes:
                    unique_hashes.add(h)
                    unique_population.append(candidate)
                attempts += 1
            if len(unique_population) < population_size:
                LOGGER.warning(
                    f"Could not generate full unique initial population. Final size is {len(unique_population)}."
                )
            self.population = unique_population
        else:
            LOGGER.info(f"Generating initial population (size: {population_size})...")
            st_time = time.time()
            self.population = (
                self.population_manager.generate_random_initial_population(
                    self.fix_individual
                )
            )
            LOGGER.info(
                f"Initial population generated in {time.time() - st_time:.2f} seconds"
            )

        # Evaluate initial population
        self.evaluation = self.evaluator.evaluate_population(self.population)
        self.fitness = (
            sum(fitness for _, fitness, _ in self.evaluation) / population_size
        )

        self.fixes_made = 0
        self.checks_made = self.evaluator.checks_made
        self.crossovers_made = 0
        self.mutations_made = 0
        self.time_taken = None
        self.solution = self.evaluator.solution
        self.solution_set = self.evaluator.solution_set
        self.desired_solutions = desired_solutions

    def fix_individual(self, individual: DerivationTree) -> DerivationTree:
        _, failing_trees = self.evaluator.evaluate_individual(individual)
        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue
            for operator, value, side in failing_tree.suggestions:
                from fandango.constraints.fitness import Comparison, ComparisonSide

                # LOGGER.debug(f"Parsing {value} into {failing_tree.tree.symbol.symbol!s}")
                if operator == Comparison.EQUAL and isinstance(
                    value, (str, bytes, DerivationTree)
                ):
                    if (
                        self.grammar.fuzzing_mode == FuzzingMode.IO
                        and side == ComparisonSide.LEFT
                    ):
                        continue
                    if (
                        self.grammar.fuzzing_mode != FuzzingMode.IO
                        and side == ComparisonSide.RIGHT
                    ):
                        continue
                    suggested_tree = self.grammar.parse(
                        value, start=failing_tree.tree.symbol.symbol
                    )
                    if suggested_tree is None:
                        continue
                    individual = individual.replace(failing_tree.tree, suggested_tree)
                    self.fixes_made += 1
        return individual

    def _evolve_io(self) -> List[DerivationTree]:
        global_env, local_env = self.grammar.get_python_env()
        io_instance: FandangoIO = global_env["FandangoIO"].instance()
        history_tree: DerivationTree = random.choice(self.population)

        self.desired_solutions = 1
        while True:
            self.population.clear()
            if history_tree.contains_bits():
               history_str = b''
            else:
               history_str = ""
            past_r_msgs = history_tree.find_role_msgs()
            for r_msg in past_r_msgs:
               if isinstance(history_str, bytes):
                   history_str += r_msg.msg.to_bytes()
               else:
                   history_str += r_msg.msg.to_string()

            forecasting_trees  = set[DerivationTree]()
            self.grammar.parse(history_str, self.start_symbol, include_controlflow=True)


            role_options = None
            for pop in set(self.population):
                forecaster = PacketForecaster(self.grammar, pop)
                if role_options is None:
                    role_options = forecaster.find()
                else:
                    packet_options_new = forecaster.find()
                    role_options = role_options.merge(packet_options_new)

            if len(role_options.getRoles()) == 0:
                if len(self.solution) == 0:
                    raise RuntimeError("Couldn't forecast next packet!")
                return self.solution[0]

            selected_role = random.choice(list(role_options.getRoles()))
            self.evaluator.reset()
            self.solution.clear()
            self.solution_set.clear()
            if (
                io_instance.roles[selected_role].is_fandango()
                and not io_instance.received_msg()
            ):
                non_terminal_options = role_options[selected_role]
                symbol = random.choice(list(non_terminal_options.getNonTerminals()))
                self.population_manager.io_next_packet = non_terminal_options[symbol]
                new_population = (
                    self.population_manager.generate_random_initial_population(
                        self.fix_individual
                    )
                )
                packet_node = self.population_manager.io_next_packet.node

                self.population = new_population
                self.evaluation = self.evaluator.evaluate_population(self.population)
                self.fitness = (
                    sum(fitness for _, fitness, _ in self.evaluation)
                    / self.population_size
                )

                evolve_result = self._evolve_single()
                if len(evolve_result) == 0:
                    raise RuntimeError(
                        f"Couldn't find solution with packet: {packet_node.symbol}"
                    )
                next_tree = evolve_result[0]
                self.evaluation = self.evaluator.evaluate_population(self.population)
                if io_instance.received_msg():
                    # Abort if we received a message during fuzzing
                    continue
                send_msg = next_tree.find_role_msgs()[-1].msg
                if send_msg.contains_bytes():
                    send_msg = send_msg.to_bytes()
                else:
                    send_msg = send_msg.to_string()
                if (
                    packet_node.recipient is None
                    or not io_instance.roles[packet_node.recipient].is_fandango()
                ):
                    io_instance.set_transmit(
                        packet_node.role, packet_node.recipient, send_msg
                    )
                    exec("FandangoIO.instance().run_com_loop()", global_env, local_env)
            else:
                while not io_instance.received_msg():
                    time.sleep(0.25)
                forecast, packet_tree = self._parse_next_remote_packet(
                    role_options, io_instance
                )

                prefix_data = next(iter(forecast.paths))
                next_tree = prefix_data.tree
                hookin_path = prefix_data.path
                next_tree.append(hookin_path[1:], packet_tree)
                next_tree.set_all_read_only(True)
                fitness, eval_report = self.evaluator.evaluate_individual(next_tree)
                if fitness < 0.99:
                    raise RuntimeError("Remote response doesn't match constraints!")
                self.solution.clear()

            # if next_tree.contains_bits():
            #    history = b''
            # else:
            #    history = ""
            # past_r_msgs = next_tree.find_role_msgs()
            # for r_msg in past_r_msgs:
            #    if isinstance(history, bytes):
            #        history += r_msg.msg.to_bytes()
            #    else:
            #        history += r_msg.msg.to_string()

            # new_population = []
            # for tree_option in self.grammar.parse_incomplete(
            #    history, self.start_symbol
            # ):
            #    tree_option.set_all_read_only(True)
            #    if self.grammar.assign_roles(tree_option, past_r_msgs):
            #        new_population.append(tree_option)
            #    if len(new_population) >= self.population_size:
            #        break
            # if len(new_population) == 0:
            #    raise RuntimeError(
            #        "Failed to append remote response to generated history matching grammar!"
            #    )
            new_population = [next_tree]
            self.population = list(new_population)
            self.solution.clear()
            self.solution.extend(new_population)
            while len(self.population) < self.population_size:
                self.population.append(random.choice(new_population))

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
            new_population = self.evaluator.select_elites(
                self.evaluation, self.elitism_rate, self.population_size
            )
            unique_hashes = {hash(ind) for ind in new_population}

            while len(new_population) < self.population_size:
                if random.random() < self.adaptive_tuner.crossover_rate:
                    try:
                        parent1, parent2 = self.evaluator.tournament_selection(
                            self.evaluation, self.tournament_size
                        )
                        child1, child2 = self.crossover_operator.crossover(
                            parent1, parent2
                        )
                        self.population_manager.add_unique_individual(
                            new_population, child1, unique_hashes
                        )
                        if len(new_population) < self.population_size:
                            self.population_manager.add_unique_individual(
                                new_population, child2, unique_hashes
                            )
                        self.crossovers_made += 1
                    except Exception as e:
                        LOGGER.error(f"Error during crossover: {e}")
                        continue
                else:
                    break

            if len(new_population) > self.population_size:
                new_population = new_population[: self.population_size]

            # Mutation
            mutated_population = []
            for individual in new_population:
                if random.random() < self.adaptive_tuner.mutation_rate:
                    try:
                        mutated_individual = self.mutation_method.mutate(
                            individual, self.grammar, self.evaluator.evaluate_individual
                        )
                        mutated_population.append(mutated_individual)
                        self.mutations_made += 1
                    except Exception as e:
                        LOGGER.error(f"Error during mutation: {e}")
                        mutated_population.append(individual)
                else:
                    mutated_population.append(individual)
            new_population = mutated_population

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

            fixed_population = [self.fix_individual(ind) for ind in new_population]
            self.population = fixed_population[: self.population_size]
            self.evaluation = self.evaluator.evaluate_population_parallel(
                self.population, num_workers=4
            )
            self.fitness = (
                sum(fitness for _, fitness, _ in self.evaluation) / self.population_size
            )

            current_best_fitness = max(fitness for _, fitness, _ in self.evaluation)
            self.adaptive_tuner.update_parameters(
                generation,
                prev_best_fitness,
                current_best_fitness,
                self.population,
                self.evaluator,
            )
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

        if self.fitness < self.expected_fitness:
            LOGGER.error("Population did not converge to a perfect population")
            if self.warnings_are_errors:
                raise RuntimeError("Failed to find a perfect solution")
            if self.best_effort:
                return self.population

        if self.desired_solutions > 0 and len(self.solution) < self.desired_solutions:
            LOGGER.error(
                f"Only found {len(self.solution)} perfect solutions, instead of the required {self.desired_solutions}"
            )
            if self.warnings_are_errors:
                raise RuntimeError(
                    "Failed to find the required number of perfect solutions"
                )
            if self.best_effort:
                return self.population[: self.desired_solutions]

        return self.solution

    def _parse_next_remote_packet(
        self, forecast: PacketForecaster.ForcastingResult, io_instance: FandangoIO
    ):
        if len(io_instance.get_received_msgs()) == 0:
            return None, None

        remote_msgs = io_instance.get_received_msgs()

        complete_msg = None
        used_fragments_idx = []

        msg_role, _ = remote_msgs[0]

        if msg_role not in forecast.getRoles():
            raise RuntimeError(
                f"Unexpected sender sent message. Expected:",
                "|".join(forecast.getRoles()),
                f" Received: {msg_role}",
            )
        forecasted_nonterminals = forecast[msg_role]
        nts_with_role = set(forecasted_nonterminals.getNonTerminals())

        is_msg_complete = False
        next_fragment_idx = 0

        while not is_msg_complete:
            for idx, (role, msg_fragment) in enumerate(remote_msgs, next_fragment_idx):
                next_fragment_idx = idx + 1

                if msg_role != role:
                    continue
                if complete_msg is None:
                    complete_msg = msg_fragment
                else:
                    complete_msg += msg_fragment
                used_fragments_idx.append(idx)

                parsed_packet_tree = None
                packet_option = None
                for non_terminal in set(nts_with_role):
                    packet_option = forecasted_nonterminals[non_terminal]
                    parsed_packet_tree = self.grammar.parse(
                        complete_msg, packet_option.node.symbol
                    )
                    parsed_packet_tree.role = packet_option.node.role
                    parsed_packet_tree.recipient = packet_option.node.recipient
                    if parsed_packet_tree is None:
                        try:
                            next(
                                self.grammar.parse_multiple(
                                    complete_msg, packet_option.node.symbol
                                )
                            )
                        except StopIteration:
                            nts_with_role.remove(non_terminal)
                    else:
                        break

                # Check if there are still NonTerminals that can be parsed with received prefix
                if len(nts_with_role) == 0:
                    raise RuntimeError(
                        f"Couldn't match remote message to any packet matching grammar: {complete_msg}"
                    )
                if parsed_packet_tree is not None:
                    for idx in used_fragments_idx:
                        del remote_msgs[idx]
                    return packet_option, parsed_packet_tree

            if not is_msg_complete:
                time.sleep(0.25)

    def select_elites(self) -> List[DerivationTree]:
        return [
            x[0]
            for x in sorted(self.evaluation, key=lambda x: x[1], reverse=True)[
                : int(self.elitism_rate * self.population_size)
            ]
        ]
