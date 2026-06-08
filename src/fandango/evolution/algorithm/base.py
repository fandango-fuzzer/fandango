import enum
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable, Generator
from typing import Optional

from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.evolution.crossover import CrossoverOperator, SimpleSubtreeCrossover
from fandango.evolution.mutation import MutationOperator, SimpleMutation
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.tree import DerivationTree


class LoggerLevel(enum.Enum):
    NOTSET = logging.NOTSET
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


DEFAULT_CROSSOVER_OPERATOR: CrossoverOperator = SimpleSubtreeCrossover()
DEFAULT_MUTATION_OPERATOR: MutationOperator = SimpleMutation()


class GeneticAlgorithm(ABC):
    @abstractmethod
    def __init__(
        self,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
        population_size: int = 100,
        initial_population: Optional[list[DerivationTree | str]] = None,
        expected_fitness: float = 1.0,
        elitism_rate: float = 0.1,
        crossover_method: CrossoverOperator = DEFAULT_CROSSOVER_OPERATOR,
        crossover_rate: float = 0.8,
        tournament_size: float = 0.1,
        mutation_method: MutationOperator = DEFAULT_MUTATION_OPERATOR,
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
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        stop_criterion: Optional[Callable[[DerivationTree], bool]] = None,
        stop_after_seconds: Optional[int] = None,
    ):
        pass

    @abstractmethod
    def generate(
        self,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
    ) -> Generator[DerivationTree, None, None]:
        pass
