"""Evolutionary algorithm implementations."""

DEFAULT_ALGORITHM = "genetic"

from fandango.evolution.algorithms.base import GenerationAlgorithm
from fandango.evolution.algorithms.mio import MIOAlgorithm
from fandango.evolution.algorithms.dynamosa import DynaMOSAAlgorithm
from fandango.evolution.algorithms.wholesuite import WholeSuiteAlgorithm
from fandango.evolution.algorithms.random import (
    RandomIndividualAlgorithm,
    RandomSuiteAlgorithm,
)

__all__ = [
    DEFAULT_ALGORITHM,
    "GenerationAlgorithm",
    "MIOAlgorithm",
    "DynaMOSAAlgorithm",
    "WholeSuiteAlgorithm",
    "RandomIndividualAlgorithm",
    "RandomSuiteAlgorithm",
]
