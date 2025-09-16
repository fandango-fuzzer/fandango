import math
from typing import Optional

from fandango.constraints.fitness import FailingTree
from fandango.evolution.evaluation import Evaluator
from fandango.language import DerivationTree
from fandango.logger import LOGGER


class AdaptiveTuner:
    def __init__(
        self,
        initial_mutation_rate: float,
        initial_crossover_rate: float,
        initial_max_repetition: int,
        initial_max_nodes: int,
        max_repetition: Optional[int],
        max_repetition_rate: float,
        max_nodes: int,
        max_nodes_rate: float,
        max_safe_repetition: int = 1000,  # default safe max repetition cap
        max_safe_nodes: int = 5000,  # default safe max nodes cap
    ):
        self.mutation_rate = initial_mutation_rate
        self.crossover_rate = initial_crossover_rate
        self.max_repetitions = max_repetition
        self.current_max_repetition = initial_max_repetition
        self.max_repetition_rate = max_repetition_rate
        self.max_nodes = max_nodes
        self.current_max_nodes = initial_max_nodes
        self.max_nodes_rate = max_nodes_rate
        self.max_safe_repetition = max_safe_repetition
        self.max_safe_nodes = max_safe_nodes

    def update_parameters(
        self,
        generation: int,
        prev_best_fitness: float,
        current_best_fitness: float,
        population: list[DerivationTree],
        evaluator: Evaluator,
        current_max_repetition: int,
    ) -> tuple[float, float]:

        diversities = evaluator.compute_diversity_bonus(population)
        avg_diversity = sum(diversities) / len(diversities) if diversities else 0

        if prev_best_fitness > 0:
            fitness_improvement = (
                current_best_fitness - prev_best_fitness
            ) / prev_best_fitness
        else:
            fitness_improvement = current_best_fitness

        fitness_improvement_threshold = 0.005
        diversity_low_threshold = 0.1

        # Mutation rate adjustment
        if (
            fitness_improvement < fitness_improvement_threshold
            or avg_diversity < diversity_low_threshold
        ):
            new_mutation_rate = min(1.0, self.mutation_rate * 1.1)
            LOGGER.info(
                f"Generation {generation}: Increasing mutation rate from {self.mutation_rate:.3f} to {new_mutation_rate:.3f}"
            )
            self.mutation_rate = new_mutation_rate
        else:
            new_mutation_rate = max(0.01, self.mutation_rate * 0.95)
            LOGGER.info(
                f"Generation {generation}: Decreasing mutation rate from {self.mutation_rate:.3f} to {new_mutation_rate:.3f}"
            )
            self.mutation_rate = new_mutation_rate

        # Crossover rate adjustment
        if avg_diversity < diversity_low_threshold:
            new_crossover_rate = max(0.1, self.crossover_rate * 0.95)
            LOGGER.info(
                f"Generation {generation}: Decreasing crossover rate from {self.crossover_rate:.3f} to {new_crossover_rate:.3f}"
            )
            self.crossover_rate = new_crossover_rate
        else:
            new_crossover_rate = min(0.9, self.crossover_rate * 1.02)
            LOGGER.info(
                f"Generation {generation}: Increasing crossover rate from {self.crossover_rate:.3f} to {new_crossover_rate:.3f}"
            )
            self.crossover_rate = new_crossover_rate

        # Max repetition growth
        if (
            fitness_improvement < fitness_improvement_threshold
            or avg_diversity < diversity_low_threshold
        ):
            increment = math.ceil(
                self.max_repetition_rate * self.current_max_repetition
            )
            increment = max(1, increment)
            new_max_repetition = self.current_max_repetition + increment

            if self.max_repetitions is not None:
                new_max_repetition = min(new_max_repetition, self.max_repetitions)

            new_max_repetition = min(new_max_repetition, self.max_safe_repetition)

            if new_max_repetition > self.current_max_repetition:
                LOGGER.info(
                    f"Generation {generation}: Increasing MAX_REPETITION from {self.current_max_repetition} to {new_max_repetition}"
                )
                self.current_max_repetition = new_max_repetition

        # Max nodes growth
        if (
            fitness_improvement < fitness_improvement_threshold
            or avg_diversity < diversity_low_threshold
        ):
            increment = math.ceil(self.max_nodes_rate * self.current_max_nodes)
            increment = max(1, increment)
            new_max_nodes = self.current_max_nodes + increment

            new_max_nodes = min(new_max_nodes, self.max_nodes)
            new_max_nodes = min(new_max_nodes, self.max_safe_nodes)

            if new_max_nodes > self.current_max_nodes:
                LOGGER.info(
                    f"Generation {generation}: Increasing fuzzing budget from {self.current_max_nodes} to {new_max_nodes}"
                )
                self.current_max_nodes = new_max_nodes

        return self.mutation_rate, self.crossover_rate

    def log_generation_statistics(
        self,
        generation: int,
        evaluation: list[tuple[DerivationTree, float, list[FailingTree]]],
        population: list[DerivationTree],
        evaluator: Evaluator,
    ):
        fitnesses = [fitness for _ind, fitness, _failing_trees in evaluation]
        best_fitness = max(fitnesses)
        avg_fitness = sum(fitnesses) / len(fitnesses)
        diversities = evaluator.compute_diversity_bonus(population)
        avg_diversity = sum(diversities) / len(diversities) if diversities else 0
        LOGGER.info(
            f"Generation {generation} stats -- Best fitness: {best_fitness:.2f}, "
            f"Avg fitness: {avg_fitness:.2f}, Avg diversity: {avg_diversity:.2f}, "
            f"Population size: {len(population)}"
        )
