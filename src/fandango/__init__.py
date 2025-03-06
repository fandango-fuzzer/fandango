#!/usr/bin/env python3

__all__ = ['Fandango', 'DerivationTree']

from abc import ABC
from typing import IO, List, Optional, Generator

from fandango.language.parse import parse
from fandango.evolution.algorithm import Fandango as FandangoStrategy
import fandango.language.tree
from fandango.logger import LOGGER
import logging

DerivationTree = fandango.language.tree.DerivationTree

class Fandango(ABC):
    """Public Fandango API (tentative)"""
    def __init__(self,
                 fan_files: str | IO | List[IO],
                 constraints: List[str] = None,
                 *,
                 use_cache: bool = True,
                 use_stdlib: bool = True,
                 lazy: bool = False,
                 start_symbol: Optional[str] = None):
        """Initialize a Fandango object."""
        if start_symbol is None:
            start_symbol = '<start>'
        self._start_symbol = start_symbol

        grammar, constraints = parse(fan_files, constraints,
                                      use_cache=use_cache, use_stdlib=use_stdlib,
                                      lazy=lazy,
                                      start_symbol=start_symbol)
        self._grammar = grammar
        self._constraints = constraints

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        self._grammar = value

    @property
    def constraints(self):
        return self._constraints

    @constraints.setter
    def constraints(self, value):
        self._constraints = value

    @property
    def start_symbol(self):
        return self._start_symbol

    @start_symbol.setter
    def start_symbol(self, value):
        self._start_symbol = value

    def fuzz(self,
             extra_constraints: Optional[List[str]] = None,
             **settings) -> List[DerivationTree]:
        """Create a Fandango population."""
        constraints = self.constraints[:]
        if extra_constraints:
            constraints += extra_constraints

        fandango = FandangoStrategy(self.grammar, constraints,
                                    start_symbol=self.start_symbol,
                                    **settings)
        population = fandango.evolve()
        return population

    def parse(self, individual: str, **settings) -> Generator[DerivationTree, None, None]:
        """Parse a string according to spec."""
        tree_generator = self.grammar.parse_forest(
            individual, start=self.start_symbol, **settings
        )
        return tree_generator

if __name__ == "__main__":
    # Example Usage
    spec = """
        <start> ::= 'a' | 'b' | 'c'
        where str(<start>) != 'd'
    """
    fandango = Fandango(spec)
    population = fandango.fuzz(population_size=10)
    print("Fuzzed:",
          ", ".join(str(individual) for individual in population))

    trees = fandango.parse('a')
    print("Parsed:",
          ", ".join(str(individual) for individual in trees))
