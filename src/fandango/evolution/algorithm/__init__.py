from .simple import SimpleGeneticAlgorithm
from .base import GeneticAlgorithm, LoggerLevel

DefaultAlgorithm = SimpleGeneticAlgorithm

__all__ = [
    "DefaultAlgorithm",
    "GeneticAlgorithm",
    "SimpleGeneticAlgorithm",
    "LoggerLevel",
]
