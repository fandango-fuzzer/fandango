# fandango/evolution/algorithm.py
import enum
import logging
import random
import time
from typing import List, Union

from fandango import FandangoFailedError, FandangoParseError, FandangoValueError
from fandango.constraints.base import Constraint, SoftValue
from fandango.constraints.fitness import Comparison, ComparisonSide
from fandango.evolution.adaptation import AdaptiveTuner
from fandango.evolution.crossover import CrossoverOperator, SimpleSubtreeCrossover
from fandango.evolution.evaluation import Evaluator
from fandango.evolution.mutation import MutationOperator, SimpleMutation
from fandango.evolution.population import PopulationManager
from fandango.evolution.profiler import Profiler
from fandango.language.grammar import DerivationTree, Grammar
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

    def evolve(self) -> List[DerivationTree]:
        LOGGER.info("---------- Starting evolution ----------")
        start_time = time.time()
        prev_best_fitness = 0.0

        for generation in range(1, self.max_generations + 1):
            if 0 < self.desired_solutions <= len(self.solution):
                self.fitness = 1.0
                self.solution = self.solution[: self.desired_solutions]
                break
            if len(self.solution) >= self.population_size:
                self.fitness = 1.0
                self.solution = self.solution[: self.population_size]
                break
            if self.fitness >= self.expected_fitness:
                self.fitness = 1.0
                self.solution = self.population[: self.population_size]
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

    def fix_individual(self, individual: DerivationTree) -> DerivationTree:
        _, failing_trees = self.evaluator.evaluate_individual(individual)
        for failing_tree in failing_trees:
            if failing_tree.tree.read_only:
                continue
            for operator, value, side in failing_tree.suggestions:
                if (
                    operator == Comparison.EQUAL
                    and side == ComparisonSide.LEFT
                    and isinstance(value, (str, bytes, DerivationTree))
                ):
                    suggested_tree = self.grammar.parse(
                        value, start=failing_tree.tree.symbol.symbol
                    )
                    if suggested_tree is None:
                        continue
                    individual = individual.replace(
                        self.grammar, failing_tree.tree, suggested_tree
                    )
                    self.fixes_made += 1
        return individual

    def select_elites(self) -> List[DerivationTree]:
        return [
            x[0]
            for x in sorted(self.evaluation, key=lambda x: x[1], reverse=True)[
                : int(self.elitism_rate * self.population_size)
            ]
        ]
