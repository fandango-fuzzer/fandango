from .simple import SimpleGeneticAlgorithm
from .protocol import ProtocolAlgorithm
from .base import GeneticAlgorithm, LoggerLevel

DefaultAlgorithm = SimpleGeneticAlgorithm

__all__ = [
    "DefaultAlgorithm",
    "GeneticAlgorithm",
    "SimpleGeneticAlgorithm",
    "ProtocolAlgorithm",
    "LoggerLevel",
]
