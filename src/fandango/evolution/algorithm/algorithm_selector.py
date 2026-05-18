from fandango.language import Grammar
from fandango.language.grammar import FuzzingMode


class AlgorithmSelector:

    def __init__(self, grammar: Grammar):
        self._grammar = grammar

    def select(self):
        match self._grammar.fuzzing_mode:
            case FuzzingMode.COMPLETE:
                from fandango.evolution.algorithm.simple import SimpleGeneticAlgorithm
                return SimpleGeneticAlgorithm
            case FuzzingMode.IO:
                from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
                return ProtocolAlgorithm
            case _:
                raise RuntimeError(f"Fuzzing Mode {self._grammar.fuzzing_mode} is not implemented")
