from abc import ABC, abstractmethod
from collections.abc import Callable, Generator
import itertools
import logging
import time
from typing import IO, Optional, cast
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.language.grammar import FuzzingMode, ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER
from fandango.evolution.algorithm import Fandango as FandangoStrategy
from fandango.errors import FandangoFailedError, FandangoParseError

DEFAULT_MAX_GENERATIONS = 500


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
        start_symbol: Optional[str] = None,
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
        self._start_symbol = start_symbol if start_symbol is not None else "<start>"
        LOGGER.setLevel(logging_level if logging_level is not None else logging.WARNING)
        grammar, self._constraints = parse(
            fan_files,
            constraints,
            use_cache=use_cache,
            use_stdlib=use_stdlib,
            lazy=lazy,
            start_symbol=start_symbol,
            includes=includes,
        )
        if grammar is None:
            raise FandangoParseError(
                position=0,
                message="Failed to parse grammar, Grammar is None",
            )
        self._grammar = grammar

    @property
    def grammar(self) -> Grammar:
        return self._grammar

    @grammar.setter
    def grammar(self, value: Grammar):
        self._grammar = value

    @property
    def constraints(self) -> list[Constraint | SoftValue]:
        return self._constraints

    @constraints.setter
    def constraints(self, value: list[Constraint | SoftValue]):
        self._constraints = value

    @property
    def start_symbol(self) -> str:
        return self._start_symbol

    @start_symbol.setter
    def start_symbol(self, value: str):
        self._start_symbol = value

    @property
    def logging_level(self) -> int:
        return LOGGER.getEffectiveLevel()

    @logging_level.setter
    def logging_level(self, value: int):
        LOGGER.setLevel(value)

    @abstractmethod
    def init_population(
        self,
        *,
        extra_constraints: Optional[list[str] | list[Constraint | SoftValue]] = None,
        **settings,
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
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
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
        desired_solutions: Optional[int] = None,
        max_generations: Optional[int] = None,
        infinite: bool = False,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
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
    ) -> Generator[DerivationTree, None, Optional[DerivationTree]]:
        """
        Parse a string according to spec.
        :param word: The string to parse
        :param prefix: If True, allow incomplete parsing
        :param settings: Additional settings for the parse function
        :return: A generator yielding derivation trees that match the grammar and constraints. The generator returns the last tree that did not match the constraints if any.
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

    def _parse_extra_constraints(
        self, extra_constraints: list[str], start_symbol: str
    ) -> list[Constraint | SoftValue]:
        _, extra_constraints_parsed = parse(
            [],
            extra_constraints,
            given_grammars=[self.grammar],
            start_symbol=start_symbol,
        )
        return extra_constraints_parsed

    def init_population(
        self,
        *,
        extra_constraints: Optional[list[str] | list[Constraint | SoftValue]] = None,
        skip_base_constraints: bool = False,
        **settings,
    ) -> None:
        """
        Initialize a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        LOGGER.info("---------- Initializing base population ----------")

        start_symbol = settings.pop("start_symbol", self._start_symbol)

        constraints = [] if skip_base_constraints else self.constraints[:]

        if extra_constraints:
            if all(isinstance(c, str) for c in extra_constraints):
                extra_constraints_parsed = self._parse_extra_constraints(
                    cast(list[str], extra_constraints), start_symbol
                )
                constraints += extra_constraints_parsed
            else:
                assert all(
                    isinstance(c, (Constraint, SoftValue)) for c in extra_constraints
                )
                constraints += cast(list[Constraint | SoftValue], extra_constraints)

        self.fandango = FandangoStrategy(
            self.grammar, constraints, start_symbol=start_symbol, **settings
        )
        LOGGER.info("---------- Done initializing base population ----------")

    def generate_solutions(
        self,
        max_generations: Optional[int] = None,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
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
            f"---------- Generating {'' if max_generations is None else f' for {max_generations} generations'}----------"
        )
        start_time = time.time()
        yield from self.fandango.generate(max_generations=max_generations, mode=mode)
        LOGGER.info(
            f"---------- Done generating {'' if max_generations is None else f' for {max_generations} generations'}----------"
        )
        LOGGER.info(f"Time taken: {(time.time() - start_time):.2f} seconds")

    def _sanitize_runtime_end_settings(
        self,
        mode: FuzzingMode,
        desired_solutions: Optional[int],
        max_generations: Optional[int],
        infinite: bool,
    ) -> tuple[Optional[int], Optional[int], bool]:
        """
        Sanitize the runtime end settings and emit warnings if necessary.
        :param mode: The fuzzing mode
        :param desired_solutions: The desired number of solutions
        :param max_generations: The maximum number of generations
        :param infinite: Whether to run infinitely
        :return: The sanitized max_generations, desired_solutions, and infinite values
        """
        if mode == FuzzingMode.IO:
            match desired_solutions:
                case None:
                    LOGGER.warning(
                        "Fandango IO will only return a single solution for now, manually set with -n 1 to hide this warning"
                    )
                case 1:
                    pass
                case _:
                    LOGGER.warning(
                        "Fandango IO only supports desired-solution values of 1 for now, overriding value"
                    )
            desired_solutions = 1

        if max_generations is None and desired_solutions is None and not infinite:
            LOGGER.info(
                f"Infinite is not set and neither max_generations nor desired_solutions are specified. Limiting to default max_generations of {DEFAULT_MAX_GENERATIONS}"
            )
            max_generations = DEFAULT_MAX_GENERATIONS
        else:
            LOGGER.debug(
                f"Limiting fuzzing to max_generations: {max_generations} and desired_solutions: {desired_solutions}"
            )

        if infinite:
            if max_generations is not None:
                LOGGER.warning("Infinite mode is activated, overriding max_generations")
            max_generations = None  # infinite overrides max_generations

        return max_generations, desired_solutions, infinite

    def _print_warnings_if_necessary_post_fuzz(
        self,
        desired_solutions: Optional[int],
        solutions: list[DerivationTree],
        settings: dict,
    ) -> list[DerivationTree]:
        """
        Print warnings if necessary after fuzzing.
        :param desired_solutions: The desired number of solutions
        :param solutions: The solutions found
        :param settings: The settings used for the fuzzing
        :return: A list of derivation trees from the population to append to the solutions before returning; used for best-effort solving of constraints
        """
        assert self.fandango is not None
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
                    padding = self.fandango.population[
                        : desired_solutions - len(solutions)
                    ]
                    return solutions + padding

            LOGGER.error(
                f"Only found {len(solutions)} perfect solutions, instead of the required {desired_solutions}"
            )
            if warnings_are_errors:
                raise FandangoFailedError(
                    "Failed to find the required number of perfect solutions"
                )
            elif best_effort:
                padding = self.fandango.population[: desired_solutions - len(solutions)]
                return solutions + padding
        return []

    def fuzz(
        self,
        *,
        extra_constraints: Optional[list[str]] = None,
        solution_callback: Callable[[DerivationTree, int], None] = lambda _a, _b: None,
        desired_solutions: Optional[int] = None,
        max_generations: Optional[int] = None,
        infinite: bool = False,
        mode: FuzzingMode = FuzzingMode.COMPLETE,
        **settings,
    ) -> list[DerivationTree]:
        """
        Create a Fandango population.
        :param extra_constraints: Additional constraints to apply
        :param solution_callback: What to do with each solution; receives the solution and a unique index
        :param settings: Additional settings for the evolution algorithm
        :return: A list of derivation trees
        """
        max_generations, desired_solutions, infinite = (
            self._sanitize_runtime_end_settings(
                mode,
                desired_solutions,
                max_generations,
                infinite,
            )
        )

        solution_i = 0
        solutions = []

        self.init_population(extra_constraints=extra_constraints, **settings)
        raw_generator = self.generate_solutions(max_generations, mode)

        # limit the generator to desired_solutions — no limit if desired_solutions is None
        generator = itertools.islice(raw_generator, desired_solutions)

        for s in generator:
            solution_callback(s, solution_i)
            solution_i += 1
            # prevent memory buildup in infinite mode
            if not infinite:
                solutions.append(s)

        padding = self._print_warnings_if_necessary_post_fuzz(
            desired_solutions, solutions, settings
        )

        solutions.extend(padding)

        return solutions

    def parse(
        self, word: str | bytes | DerivationTree, *, prefix: bool = False, **settings
    ) -> Generator[DerivationTree, None, Optional[DerivationTree]]:
        """
        Parse a string according to spec.
        :param word: The string to parse
        :param prefix: If True, allow incomplete parsing
        :param settings: Additional settings for the parse function
        :return: A generator yielding derivation trees that match the grammar and constraints. The generator returns the last tree that did not match the constraints if any.
        """
        if prefix:
            mode = ParsingMode.INCOMPLETE
        else:
            mode = ParsingMode.COMPLETE

        tree_generator = self.grammar.parse_forest(
            word, mode=mode, start=self._start_symbol, **settings
        )

        last_tree = None

        for tree in tree_generator:
            if all(constraint.check(tree) for constraint in self.constraints):
                yield tree
            else:
                last_tree = tree

        return last_tree
