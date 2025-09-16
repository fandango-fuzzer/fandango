import argparse
import difflib
import logging
import os
from typing import IO, Any
import zipfile


from fandango.api import Fandango
from fandango.constraints.soft import SoftValue
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.errors import FandangoError, FandangoParseError
from fandango.evolution import GeneratorWithReturn
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER, set_visualization


def report_syntax_error(
    filename: str, position: int, individual: str | bytes, *, binary: bool = False
) -> str:
    """
    Return position and error message in `individual`
    in user-friendly format.
    """
    if position >= len(individual):
        return f"{filename!r}: missing input at end of file"

    mismatch = individual[position]
    if binary:
        assert isinstance(mismatch, int)
        return f"{filename!r}, position {position:#06x} ({position}): mismatched input {mismatch.to_bytes()!r}"

    line = 1
    column = 1
    for i in range(position):
        if individual[i] == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return f"{filename!r}, line {line}, column {column}: mismatched input {mismatch!r}"


def extract_initial_population(path: str) -> list[str]:
    try:
        initial_population = list()
        if path.strip().endswith(".zip"):
            with zipfile.ZipFile(path, "r") as zip:
                for file in zip.namelist():
                    data = zip.read(file).decode()
                    initial_population.append(data)
        else:
            for file in os.listdir(path):
                filename = os.path.join(path, file)
                with open(filename, "r") as fd:
                    individual = fd.read()
                initial_population.append(individual)
        return initial_population
    except FileNotFoundError as e:
        raise e


def _copy_setting(
    args: argparse.Namespace,
    settings: dict[str, Any],
    name: str,
    *,
    args_name: str | None = None,
) -> None:
    if args_name is None:
        args_name = name
    if hasattr(args, args_name) and getattr(args, args_name) is not None:
        settings[name] = getattr(args, args_name)
        LOGGER.debug(f"Settings: {name} is {settings[name]}")


def make_fandango_settings(
    args: argparse.Namespace, initial_settings: dict[str, Any] = {}
) -> dict[str, Any]:
    """Create keyword settings for Fandango() constructor"""
    LOGGER.debug(f"Pre-sanitized settings: {args}")
    settings = initial_settings.copy()
    _copy_setting(args, settings, "population_size")
    _copy_setting(args, settings, "mutation_rate")
    _copy_setting(args, settings, "crossover_rate")
    _copy_setting(args, settings, "elitism_rate")
    _copy_setting(args, settings, "destruction_rate")
    _copy_setting(args, settings, "warnings_are_errors")
    _copy_setting(args, settings, "best_effort")
    _copy_setting(args, settings, "random_seed")
    _copy_setting(args, settings, "max_repetition_rate")
    _copy_setting(args, settings, "max_repetitions")
    _copy_setting(args, settings, "max_nodes")
    _copy_setting(args, settings, "max_node_rate")

    if hasattr(args, "start_symbol") and args.start_symbol is not None:
        if args.start_symbol.startswith("<"):
            start_symbol = args.start_symbol
        else:
            start_symbol = f"<{args.start_symbol}>"
        settings["start_symbol"] = start_symbol

    if args.quiet and args.quiet == 1:
        LOGGER.setLevel(logging.WARNING)  # Default
    elif args.quiet and args.quiet > 1:
        LOGGER.setLevel(logging.ERROR)  # Even quieter
    elif args.verbose and args.verbose == 1:
        LOGGER.setLevel(logging.INFO)  # Give more info
    elif args.verbose and args.verbose > 1:
        LOGGER.setLevel(logging.DEBUG)  # Even more info

    if hasattr(args, "progress_bar") and args.progress_bar is not None:
        match args.progress_bar:
            case "on":
                set_visualization(True)
            case "off":
                set_visualization(False)
            case "auto":
                if args.infinite:
                    set_visualization(False)
                else:
                    set_visualization(None)

    if hasattr(args, "initial_population") and args.initial_population is not None:
        settings["initial_population"] = extract_initial_population(
            args.initial_population
        )
    return settings


def get_file_mode(
    args: argparse.Namespace,
    settings: dict[str, Any],
    *,
    grammar: Grammar | None = None,
    tree: DerivationTree | None = None,
) -> str:
    if (
        hasattr(args, "file_mode")
        and isinstance(args.file_mode, str)
        and args.file_mode != "auto"
    ):
        return args.file_mode

    if grammar is not None:
        start_symbol = settings.get("start_symbol", "<start>")
        if grammar.contains_bits(start=start_symbol) or grammar.contains_bytes(
            start=start_symbol
        ):
            return "binary"
        else:
            return "text"

    if tree is not None:
        if tree.should_be_serialized_to_bytes():
            return "binary"
        return "text"

    raise FandangoError("Cannot determine file mode")


def parse_contents_from_args(
    args: argparse.Namespace,
    given_grammars: list[Grammar] = [],
    check: bool = True,
) -> tuple[Grammar | None, list[Constraint | SoftValue]]:
    """Parse .fan content as given in args"""
    max_constraints = [f"maximizing {c}" for c in (args.maxconstraints or [])]
    min_constraints = [f"minimizing {c}" for c in (args.minconstraints or [])]
    constraints = (args.constraints or []) + max_constraints + min_constraints

    extra_defs = ""
    if "test_command" in args and args.test_command:
        arg_list = ", ".join(repr(arg) for arg in [args.test_command] + args.test_args)
        extra_defs += f"""
set_program_command([{arg_list}])
"""

    if "client" in args and args.client:
        # Act as client
        extra_defs += f"""
class Client(ConnectParty):
    def __init__(self):
        super().__init__(
            "{args.client}",
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(ConnectParty):
    def __init__(self):
        super().__init__(
            "{args.client}",
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
"""

    if "server" in args and args.server:
        # Act as server
        extra_defs += f"""
class Client(ConnectParty):
    def __init__(self):
        super().__init__(
            "{args.server}",
            ownership=Ownership.EXTERNAL_PARTY,
            endpoint_type=EndpointType.CONNECT,
        )
        self.start()

class Server(ConnectParty):
    def __init__(self):
        super().__init__(
            "{args.server}",
            ownership=Ownership.FANDANGO_PARTY,
            endpoint_type=EndpointType.OPEN,
        )
        self.start()
"""

    LOGGER.debug("Extra definitions:" + extra_defs)
    args.fan_files += [extra_defs]

    return parse(
        args.fan_files,
        constraints,
        given_grammars=given_grammars,
        includes=args.includes,
        use_cache=args.use_cache,
        use_stdlib=args.use_stdlib,
        start_symbol=args.start_symbol,
        parties=args.parties,
        check=check,
    )


def parse_constraints_from_args(
    args: argparse.Namespace,
    given_grammars: list[Grammar] = [],
    check: bool = True,
) -> tuple[Grammar | None, list[Constraint | SoftValue]]:
    """Parse .fan constraints as given in args"""
    max_constraints = [f"maximizing {c}" for c in (args.maxconstraints or [])]
    min_constraints = [f"minimizing {c}" for c in (args.minconstraints or [])]
    constraints = (args.constraints or []) + max_constraints + min_constraints
    return parse(
        [],
        constraints,
        given_grammars=given_grammars,
        includes=args.includes,
        use_cache=args.use_cache,
        use_stdlib=args.use_stdlib,
        start_symbol=args.start_symbol,
        parties=args.parties,
        check=check,
    )


def validate(
    original: str | bytes | DerivationTree,
    parsed: DerivationTree,
    *,
    filename: str = "<file>",
) -> None:
    if (
        (isinstance(original, DerivationTree) and original.value() != parsed.value())
        or (isinstance(original, bytes) and original != parsed.to_bytes())
        or (isinstance(original, str) and original != parsed.to_string())
    ):
        exc = FandangoError(f"{filename!r}: parsed tree does not match original")
        if getattr(Exception, "add_note", None):
            # Python 3.11+ has add_note() method
            if isinstance(original, DerivationTree) and isinstance(
                parsed, DerivationTree
            ):
                original_grammar = original.to_grammar()
                parsed_grammar = parsed.to_grammar()
                diff = difflib.context_diff(
                    original_grammar.split("\n"),
                    parsed_grammar.split("\n"),
                    fromfile="original",
                    tofile="parsed",
                )
                out = "\n".join(line for line in diff)
                exc.add_note(out)
        raise exc


def parse_file(
    fd: IO[Any],
    args: argparse.Namespace,
    grammar: Grammar,
    constraints: list[Constraint | SoftValue],
    settings: dict[str, Any],
) -> DerivationTree:
    """
    Parse a single file `fd` according to `args`, `grammar`, `constraints`, and `settings`, and return the parse tree.
    """
    LOGGER.info(f"Parsing {fd.name!r}")
    individual = fd.read()
    start_symbol = settings.get("start_symbol", "<start>")
    allow_incomplete = hasattr(args, "prefix") and args.prefix
    fan = Fandango._with_parsed(grammar, constraints, start_symbol=start_symbol)

    gen = GeneratorWithReturn(fan.parse(individual, prefix=allow_incomplete))
    for tree in gen:
        if args.validate:
            validate(individual, tree, filename=fd.name)
        return tree

    # so no tree matched everything (we would have returned above)
    last_tree = gen.return_value

    if last_tree is not None:
        # check if any tree matched the grammar and failed constraints
        grammar.populate_sources(last_tree)
        failed_constraints = [
            c.format_as_spec() for c in constraints if not c.check(last_tree)
        ]
        raise FandangoParseError(
            f"Did not match the following constraints: {', '.join(failed_constraints)}"
        )
    else:
        # no tree matched the grammar
        raise FandangoParseError(
            report_syntax_error(
                fd.name, len(individual), individual, binary=("b" in fd.mode)
            )
        )


def exec_single(
    code: str, _globals: dict[str, Any] = {}, _locals: dict[str, Any] = {}
) -> None:
    """Execute CODE in 'single' mode, printing out results if any"""
    block = compile(code, "<input>", mode="single")
    exec(block, _globals, _locals)
