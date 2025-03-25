from typing import List, Tuple

from fandango.evolution.evaluation import Evaluator
from fandango.language.grammar import DerivationTree
from fandango.logger import LOGGER


class AdaptiveTuner:
    def __init__(self, initial_mutation_rate: float, initial_crossover_rate: float):
        self.mutation_rate = initial_mutation_rate
        self.crossover_rate = initial_crossover_rate

    def update_parameters(
        self,
        generation: int,
        prev_best_fitness: float,
        current_best_fitness: float,
        population: List[DerivationTree],
        evaluator: Evaluator,
    ) -> Tuple[float, float]:
        diversity_map = evaluator.compute_diversity_bonus(population)
        avg_diversity = (
            sum(diversity_map.values()) / len(diversity_map) if diversity_map else 0
        )

        fitness_improvement_threshold = (
            0.01  # minimal improvement to be considered significant
        )
        diversity_low_threshold = 0.1  # low diversity threshold

        # Adaptive Mutation
        if (
            current_best_fitness - prev_best_fitness
        ) < fitness_improvement_threshold or avg_diversity < diversity_low_threshold:
            new_mutation_rate = min(1.0, self.mutation_rate * 1.1)
            LOGGER.info(
                f"Generation {generation}: Increasing mutation rate from {self.mutation_rate:.2f} to {new_mutation_rate:.2f}"
            )
            self.mutation_rate = new_mutation_rate
        else:
            new_mutation_rate = max(0.01, self.mutation_rate * 0.95)
            LOGGER.info(
                f"Generation {generation}: Decreasing mutation rate from {self.mutation_rate:.2f} to {new_mutation_rate:.2f}"
            )
            self.mutation_rate = new_mutation_rate

        # Adaptive Crossover
        if avg_diversity < diversity_low_threshold:
            new_crossover_rate = min(1.0, self.crossover_rate * 1.05)
            LOGGER.info(
                f"Generation {generation}: Increasing crossover rate from {self.crossover_rate:.2f} to {new_crossover_rate:.2f}"
            )
            self.crossover_rate = new_crossover_rate
        else:
            new_crossover_rate = max(0.1, self.crossover_rate * 0.98)
            LOGGER.info(
                f"Generation {generation}: Decreasing crossover rate from {self.crossover_rate:.2f} to {new_crossover_rate:.2f}"
            )
            self.crossover_rate = new_crossover_rate

        return self.mutation_rate, self.crossover_rate

    def log_generation_statistics(
        self,
        generation: int,
        evaluation: List[Tuple[DerivationTree, float, List]],
        population: List[DerivationTree],
        evaluator: Evaluator,
    ):
        best_fitness = max(fitness for _, fitness, _ in evaluation)
        avg_fitness = sum(fitness for _, fitness, _ in evaluation) / len(evaluation)
        diversity_bonus = evaluator.compute_diversity_bonus(population)
        avg_diversity = (
            sum(diversity_bonus.values()) / len(diversity_bonus)
            if diversity_bonus
            else 0
        )
        LOGGER.info(
            f"Generation {generation} stats -- Best fitness: {best_fitness:.2f}, "
            f"Avg fitness: {avg_fitness:.2f}, Avg diversity: {avg_diversity:.2f}, "
            f"Population size: {len(population)}"
        )
