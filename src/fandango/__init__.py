#!/usr/bin/env python3

__all__ = ["FandangoError",
           "FandangoParseError",
           "FandangoSyntaxError",
           "FandangoValueError",
           "FandangoBase",
           "Fandango",
           "DerivationTree"]

class FandangoError(ValueError):
    """Generic Error"""
    pass

class FandangoParseError(FandangoError, SyntaxError):
    """Error during parsing inputs"""
    def __init__(self, position: int, *, message: str = None):
        if message is None:
            message = f"Parse error at position {position}"
        FandangoError.__init__(self, message)
        SyntaxError.__init__(self, message)
        self.position = position

class FandangoSyntaxError(FandangoError, SyntaxError):
    """Error during parsing a Fandango spec"""
    pass

class FandangoValueError(FandangoError, ValueError):
    """Error during evaluating a Fandango spec"""
    pass

class FandangoFailedError(FandangoError):
    """Error during the Fandango algorithm"""
    pass



from abc import ABC, abstractmethod
from typing import IO, List, Optional, Generator
import sys
import logging

from fandango.language.parse import parse
from fandango.evolution.algorithm import Fandango as FandangoStrategy
import fandango.language.tree
from fandango.language.grammar import Grammar
from fandango.logger import LOGGER
import itertools

DerivationTree = fandango.language.tree.DerivationTree


class FandangoBase(ABC):
    """Public Fandango API"""

    def __init__(
        self,
        fan_files: str | IO | List[IO],
        constraints: List[str] = None,
        *,
        logging_level: Optional[int] = None,
        use_cache: bool = True,
        use_stdlib: bool = True,
        lazy: bool = False,
        start_symbol: Optional[str] = None,
        includes: List[str] = None,
    ):
        """
        Initialize a Fandango object.
        :param fan_files: One (open) .fan file, one string, or a list of these
        :param constraints: List of constraints (as strings); default: []
        :param use_cache: If True (default), cache parsing results
        :param use_stdlib: If True (default), use the standard library
        :param lazy: If True, the constraints are evaluated lazily
        :param start_symbol: The grammar start symbol (default: "<start>")
        :param includes: A list of directories to search for include files
        """
        if start_symbol is None:
            start_symbol = "<start>"
        self._start_symbol = start_symbol

        if logging_level is None:
            logging_level = logging.WARNING
        LOGGER.setLevel(logging_level)

        grammar, constraints = parse(
            fan_files,
            constraints,
            use_cache=use_cache,
            use_stdlib=use_stdlib,
            lazy=lazy,
            start_symbol=start_symbol,
            includes=includes,
        )
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

    @property
    def logging_level(self):
        return LOGGER.getEffectiveLevel()

    @logging_level.setter
    def logging_level(self, value):
        LOGGER.setLevel(value)

    @abstractmethod
    def fuzz(
        self, extra_constraints: Optional[List[str]] = None, **settings
    ) -> List[DerivationTree]:
        """
        Create a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        pass

    @abstractmethod
    def parse(
        self, word: str | bytes | DerivationTree, *, prefix: bool = False, **settings
    ) -> Generator[DerivationTree, None, None]:
        """
        Parse a string according to spec.
        :param word: The string to parse
        :param prefix: If True, allow incomplete parsing
        :param settings: Additional settings for the parse function
        :return: A generator of derivation trees
        """
        pass


class Fandango(FandangoBase):
    """Evolutionary testing with Fandango."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fuzz(
        self, extra_constraints: Optional[List[str]] = None, **settings
    ) -> List[DerivationTree]:
        """
        Create a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        constraints = self.constraints[:]
        if extra_constraints:
            constraints += extra_constraints

        fandango = FandangoStrategy(
            self.grammar, constraints, start_symbol=self.start_symbol, **settings
        )
        population = fandango.evolve()
        return population

    def parse(
        self, word: str | bytes | DerivationTree, *, prefix: bool = False, **settings
    ) -> Generator[DerivationTree, None, None]:
        """
        Parse a string according to spec.
        :param word: The string to parse
        :param prefix: If True, allow incomplete parsing
        :param settings: Additional settings for the parse function
        :return: A generator of derivation trees
        """
        if prefix:
            mode = Grammar.Parser.ParsingMode.INCOMPLETE
        else:
            mode = Grammar.Parser.ParsingMode.COMPLETE

        tree_generator = self.grammar.parse_forest(
            word, mode=mode, start=self.start_symbol, **settings
        )
        try:
            peek = next(tree_generator)
            tree_generator = itertools.chain([peek], tree_generator)
            have_tree = True
        except StopIteration:
            have_tree = False

        if not have_tree:
            position = self.grammar.max_position() + 1
            raise FandangoParseError(position)

        return tree_generator


if __name__ == "__main__":
    # Example Usage

    # Set the logging level (for debugging)
    logging_level = None
    if "-vv" in sys.argv:
        logging_level = logging.DEBUG
    elif "-v" in sys.argv:
        logging_level = logging.INFO

    # Read in a .fan spec (from a string)
    # We could also pass an (open) file or a list of files
    spec = """
        <start> ::= 'a' | 'b' | 'c'
        where str(<start>) != 'd'
    """
    fan = Fandango(spec, logging_level=logging_level)

    # Instantiate the spec into a population of derivation trees
    population = fan.fuzz(population_size=3)
    print("Fuzzed:", ", ".join(str(individual) for individual in population))

    # Parse a single input into a derivation tree
    trees = fan.parse("a")
    print("Parsed:", ", ".join(str(individual) for individual in trees))
