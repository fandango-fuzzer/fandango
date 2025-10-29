import math
from typing import Optional

from fandango.constraints.failing_tree import FailingTree
from fandango.evolution.evaluation import Evaluator
from fandango.language import DerivationTree
from fandango.logger import LOGGER


class AdaptiveTuner:
    def __init__(
        self,
        initial_mutation_rate: float,
        initial_crossover_rate: float,
        initial_max_repetition: int,
    ):
        self.mutation_rate = initial_mutation_rate
        self.crossover_rate = initial_crossover_rate
        self.current_max_repetition = initial_max_repetition

    def update_parameters(
        self,
        generation: int,
        prev_best_fitness: float,
        current_best_fitness: float,
        population: list[DerivationTree],
        evaluator: Evaluator,
        current_max_repetition: int,
    ) -> tuple[float, float]:
        return self.mutation_rate, self.crossover_rate
