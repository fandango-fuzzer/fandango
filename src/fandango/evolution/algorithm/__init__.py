from .base import GeneticAlgorithm, LoggerLevel
from .protocol import ProtocolAlgorithm
from .simple import SimpleGeneticAlgorithm

DefaultAlgorithm = SimpleGeneticAlgorithm

__all__ = [
    "DefaultAlgorithm",
    "GeneticAlgorithm",
    "SimpleGeneticAlgorithm",
    "ProtocolAlgorithm",
    "LoggerLevel",
]
