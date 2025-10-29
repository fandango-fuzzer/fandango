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
        return self.mutation_rate, self.crossover_rate