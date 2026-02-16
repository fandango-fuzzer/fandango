"""Fitness function abstractions for evolutionary algorithms."""

from fandango.evolution.fitness.base import (
    FitnessFunction,
    IndividualFitnessFunction,
    SuiteFitnessFunction,
)
from fandango.evolution.fitness.suite import (
    SymbolCoverageFitnessFunction,
    PathCoverageFitnessFunction,
)

__all__ = [
    "FitnessFunction",
    "IndividualFitnessFunction",
    "SuiteFitnessFunction",
    "SymbolCoverageFitnessFunction",
    "PathCoverageFitnessFunction",
]
