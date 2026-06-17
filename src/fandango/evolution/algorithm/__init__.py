from .base import GeneticAlgorithm, LoggerLevel
from .simple import SimpleGeneticAlgorithm
from .protocol import ProtocolAlgorithm

DefaultAlgorithm = SimpleGeneticAlgorithm

__all__ = [
    "DefaultAlgorithm",
    "GeneticAlgorithm",
    "SimpleGeneticAlgorithm",
    "ProtocolAlgorithm",
    "LoggerLevel",
]
