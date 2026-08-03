from .base import GeneticAlgorithm, LoggerLevel
from .simple import SimpleGeneticAlgorithm

DefaultAlgorithm = SimpleGeneticAlgorithm

__all__ = [
    "DefaultAlgorithm",
    "GeneticAlgorithm",
    "SimpleGeneticAlgorithm",
    "LoggerLevel",
]
