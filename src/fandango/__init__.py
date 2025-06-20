#!/usr/bin/env python3

from abc import ABC, abstractmethod
import importlib.metadata
import itertools
import logging
import sys
import time
from typing import IO, Callable, Iterable, Optional, Generator

from fandango.constraints.base import Constraint, SoftValue
from fandango.evolution.algorithm import Fandango as FandangoStrategy
from fandango.language.parse import parse
from fandango.language.grammar import Grammar
import fandango.language.tree
from fandango.logger import LOGGER

__all__ = [
    "FandangoError",
    "FandangoParseError",
    "FandangoSyntaxError",
    "FandangoValueError",
    "FandangoBase",
    "DerivationTree",
    "version",
    "homepage",
]

DEFAULT_MAX_GENERATIONS = 500


class FandangoError(ValueError):
    """Generic Error"""

    pass


class FandangoParseError(FandangoError, SyntaxError):
    """Error during parsing inputs"""

    def __init__(self, message: str | None = None, position: int | None = None):
        if message is None:
            if position is not None:
                message = f"Parse error at position {position}"
            else:
                message = "Parse error"

        # Call the parent class constructors
        FandangoError.__init__(self, message)
        SyntaxError.__init__(self, message)
        self.position = position


class FandangoSyntaxError(FandangoError, SyntaxError):
    """Error during parsing a Fandango spec"""

    def __init__(self, message: str):
        FandangoError.__init__(self, message)
        SyntaxError.__init__(self, message)


class FandangoValueError(FandangoError, ValueError):
    """Error during evaluating a Fandango spec"""

    def __init__(self, message: str):
        FandangoError.__init__(self, message)
        ValueError.__init__(self, message)


class FandangoFailedError(FandangoError):
    """Error during the Fandango algorithm"""

    def __init__(self, message: str):
        super().__init__(self, message)


DISTRIBUTION_NAME = "fandango-fuzzer"


def version() -> str:
    """Return the Fandango version number"""
    return importlib.metadata.version(DISTRIBUTION_NAME)


def homepage() -> str:
    """Return the Fandango homepage"""
    metadata = importlib.metadata.metadata(DISTRIBUTION_NAME)
    return [
        e.split(",")[1].strip()
        for e in metadata.get_all("Project-URL", [])
        if e.startswith("homepage,")
    ].pop(0) or "the Fandango homepage"


DerivationTree = fandango.language.tree.DerivationTree


class FandangoBase(ABC):
    """Public Fandango API"""

    # The parser to be used
    parser = "auto"  # 'auto', 'cpp', 'python', or 'legacy'

    def __init__(
        self,
        fan_files: str | IO | list[str | IO],
        constraints: Optional[list[str]] = None,
        *,
        logging_level: Optional[int] = None,
        use_cache: bool = True,
        use_stdlib: bool = True,
        lazy: bool = False,
        start_symbol: str = "<start>",
        includes: Optional[list[str]] = None,
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
        self._start_symbol = start_symbol
        LOGGER.setLevel(logging_level if logging_level is not None else logging.WARNING)
        self._grammar, self._constraints = parse(
            fan_files,
            constraints,
            use_cache=use_cache,
            use_stdlib=use_stdlib,
            lazy=lazy,
            start_symbol=start_symbol,
            includes=includes,
        )

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
    def init_population(
        self, *, extra_constraints: Optional[list[str]] = None, **settings
    ) -> None:
        """
        Initialize a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        pass

    @abstractmethod
    def generate_solutions(
        self,
        max_generations=None,
    ) -> Generator[DerivationTree, None, None]:
        """
        Generate trees that conform to the language.

        Will initialize a population with default settings if none has been initialized before.
        Initialization can be done manually with `init_population` for more flexibility.

        :param max_generations: Maximum number of generations to evolve through
        :return: A generator for solutions to the language
        """
        pass

    @abstractmethod
    def fuzz(
        self,
        *,
        extra_constraints: Optional[list[str]] = None,
        solution_callback: Callable[[DerivationTree, int], None] = lambda _a, _b: None,
        **settings,
    ) -> list[DerivationTree]:
        """
        Create a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param solution_callback: What to do with each solution; receives the solution and a unique index
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
        self.fandango = None

    @classmethod
    def _with_parsed(
        cls,
        grammar: Grammar,
        constraints: list[Constraint | SoftValue],
        *,
        start_symbol: Optional[str] = None,
        logging_level: Optional[int] = None,
    ) -> "FandangoBase":
        LOGGER.setLevel(logging_level if logging_level is not None else logging.WARNING)
        obj = cls.__new__(cls)  # bypass __init__ to prevent the need for double parsing
        obj._grammar = grammar
        obj._constraints = constraints
        obj.fandango = None
        obj._start_symbol = start_symbol if start_symbol is not None else "<start>"
        return obj

    def init_population(
        self, *, extra_constraints: Optional[list[str]] = None, **settings
    ) -> None:
        """
        Initialize a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        LOGGER.info("---------- Initializing base population ----------")

        constraints = self.constraints[:]
        if extra_constraints:
            _, extra_constraints_parsed = parse(
                [],
                extra_constraints,
                given_grammars=[self.grammar],
                start_symbol=self._start_symbol,
            )
            constraints += extra_constraints_parsed

        self.fandango = FandangoStrategy(
            self.grammar, constraints, start_symbol=self._start_symbol, **settings
        )

    def generate_solutions(
        self,
        max_generations=None,
    ) -> Generator[DerivationTree, None, None]:
        """
        Generate trees that conform to the language.

        Will initialize a population with default settings if none has been initialized before.
        Initialization can be done manually with `init_population` for more flexibility.

        :param max_generations: Maximum number of generations to evolve through
        :return: A generator for solutions to the language
        """
        if self.fandango is None:
            self.init_population()
            assert self.fandango is not None

        LOGGER.info(
            f"---------- Generating {'' if max_generations is None else f' {max_generations} solutions'}----------"
        )
        start_time = time.time()
        yield from self.fandango.generate(max_generations=max_generations)
        LOGGER.info(f"Time taken: {(time.time() - start_time):.2f} seconds")

    def fuzz(
        self,
        *,
        extra_constraints: Optional[list[str]] = None,
        solution_callback: Callable[[DerivationTree, int], None] = lambda _a, _b: None,
        **settings,
    ) -> list[DerivationTree]:
        """
        Create a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param solution_callback: What to do with each solution; receives the solution and a unique index
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """

        max_generations = settings.pop("max_generations", None)
        desired_solutions = settings.pop("desired_solutions", None)
        infinite = settings.pop("infinite", False)

        # initialize if not initialized or settings changed
        if self.fandango is None or extra_constraints or settings:
            self.init_population(extra_constraints=extra_constraints, **settings)
        assert self.fandango is not None

        if max_generations is None and desired_solutions is None:
            max_generations = DEFAULT_MAX_GENERATIONS

        if infinite:
            max_generations = None  # infinite overrides max_generations

        generator: Iterable[DerivationTree] = self.generate_solutions(max_generations)
        if desired_solutions is not None:
            LOGGER.info(f"Generating {desired_solutions} solutions")
            generator = itertools.islice(generator, desired_solutions)

        solutions = []
        for i, s in enumerate(generator):
            solutions.append(s)
            solution_callback(s, i)

        if desired_solutions is not None and len(solutions) < desired_solutions:
            warnings_are_errors = settings.get("warnings_are_errors", False)
            best_effort = settings.get("best_effort", False)
            if (
                self.fandango.average_population_fitness
                < self.fandango.evaluator.expected_fitness
            ):
                LOGGER.error("Population did not converge to a perfect population")
                if warnings_are_errors:
                    raise FandangoFailedError("Failed to find a perfect solution")
                elif best_effort:
                    return self.fandango.population

            LOGGER.error(
                f"Only found {len(solutions)} perfect solutions, instead of the required {desired_solutions}"
            )
            if warnings_are_errors:
                raise FandangoFailedError(
                    "Failed to find the required number of perfect solutions"
                )
            elif best_effort:
                return self.fandango.population[:desired_solutions]

        return solutions

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
            word, mode=mode, start=self._start_symbol, **settings
        )
        try:
            peek = next(tree_generator)
            self.grammar.populate_sources(peek)
            tree_generator = itertools.chain([peek], tree_generator)
            have_tree = True
        except StopIteration:
            have_tree = False

        if not have_tree:
            position = self.grammar.max_position() + 1
            raise FandangoParseError(position=position)

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
        <my_start> ::= 'a' | 'b' | 'c'
        where str(<my_start>) != 'd'
    """
    fan = Fandango(spec, logging_level=logging_level, start_symbol="<my_start>")

    # Instantiate the spec into a population of derivation trees
    population = fan.fuzz(extra_constraints=["<my_start> != 'e'"], population_size=3)
    print("Fuzzed:", ", ".join(str(individual) for individual in population))

    # Parse a single input_ into a derivation tree
    trees = fan.parse("a")
    print("Parsed:", ", ".join(str(individual) for individual in trees))
