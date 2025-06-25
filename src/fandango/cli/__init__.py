import argparse
import atexit
import ctypes
import difflib
import glob
import logging
import os
import os.path
import re
from typing import IO, Any
from collections.abc import Callable

from fandango.constraints.base import Constraint, SoftValue
from fandango.converters.FandangoConverter import FandangoConverter
from fandango.language.tree import DerivationTree

if "readline" not in globals():
    try:
        # Linux and Mac. This should do the trick.
        import gnureadline as readline  # type: ignore [import-not-found] # types not always available
    except Exception:
        pass

if "readline" not in globals():
    try:
        # Windows. This should do the trick.
        import pyreadline3 as readline  # type: ignore [import-not-found] # types not always available
    except Exception:
        pass

if "readline" not in globals():
    try:
        # Another Windows alternative
        import pyreadline as readline  # type: ignore [import-not-found] # types not always available
    except Exception:
        pass

if "readline" not in globals():
    try:
        # A Hail Mary Pass
        import readline
    except Exception:
        pass

import shlex
import subprocess
import sys
import tempfile
import zipfile
import shutil
import textwrap

from io import StringIO
from io import UnsupportedOperation
from pathlib import Path

from ansi_styles import ansiStyles as styles

from fandango import Fandango
from fandango.language.grammar import Grammar, FuzzingMode
from fandango.language.parse import parse, clear_cache, cache_dir
from fandango.logger import LOGGER, print_exception

from fandango.converters.antlr.ANTLRFandangoConverter import ANTLRFandangoConverter
from fandango.converters.bt.BTFandangoConverter import (
    BTFandangoConverter,
    Endianness,
    BitfieldOrder,
)
from fandango.converters.dtd.DTDFandangoConverter import DTDFandangoConverter
from fandango.converters.fan.FandangoFandangoConverter import FandangoFandangoConverter

from fandango.errors import FandangoParseError, FandangoError
import fandango


def terminal_link(url: str, text: str | None = None) -> str:
    """Output URL as a link"""
    if text is None:
        text = url
    # https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda
    return f"\x1b]8;;{url}\x1b\\{text}\x1b]8;;\x1b\\"


def homepage_as_link() -> str:
    """Return the Fandango homepage, formatted for terminals"""
    homepage = fandango.homepage()
    if os.getenv("JUPYTER_BOOK") is not None:
        return homepage  # Don't link in Jupyter Book

    if homepage.startswith("http") and sys.stdout.isatty():
        return terminal_link(homepage)
    else:
        return homepage


def get_parser(in_command_line: bool = True) -> argparse.ArgumentParser:
    # Main parser
    if in_command_line:
        prog = "fandango"
        epilog = textwrap.dedent(
            """\
            Use `%(prog)s help` to get a list of commands.
            Use `%(prog)s help COMMAND` to learn more about COMMAND."""
        )
    else:
        prog = ""
        epilog = textwrap.dedent(
            """\
            Use `help` to get a list of commands.
            Use `help COMMAND` to learn more about COMMAND.
            Use TAB to complete commands."""
        )
    epilog += f"\nSee {homepage_as_link()} for more information."

    main_parser = argparse.ArgumentParser(
        prog=prog,
        description="The access point to the Fandango framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=in_command_line,
        epilog=textwrap.dedent(epilog),
    )

    if in_command_line:
        main_parser.add_argument(
            "--version",
            action="version",
            version=f"Fandango {fandango.version()}",
            help="Show version number.",
        )

        verbosity_option = main_parser.add_mutually_exclusive_group()
        verbosity_option.add_argument(
            "--verbose",
            "-v",
            dest="verbose",
            action="count",
            help="Increase verbosity. Can be given multiple times (-vv).",
        )
        verbosity_option.add_argument(
            "--quiet",
            "-q",
            dest="quiet",
            action="count",
            help="Decrease verbosity. Can be given multiple times (-qq).",
        )

        main_parser.add_argument(
            "--parser",
            choices=["python", "cpp", "legacy", "auto"],
            default="auto",
            help="Parser implementation to use (default: 'auto': use C++ parser code if available, otherwise Python).",
        )

    # The subparsers
    commands = main_parser.add_subparsers(
        title="commands",
        # description="Valid commands",
        help="The command to execute.",
        dest="command",
        # required=True,
    )

    # Algorithm Settings
    algorithm_parser = argparse.ArgumentParser(add_help=False)
    algorithm_group = algorithm_parser.add_argument_group("Generation settings")

    algorithm_group.add_argument(
        "-N",
        "--max-generations",
        type=int,
        help="Maximum number of generations to run the algorithm (ignored if --infinite is set).",
        default=fandango.api.DEFAULT_MAX_GENERATIONS,
    )
    algorithm_group.add_argument(
        "--infinite",
        action="store_true",
        help="Run the algorithm indefinitely.",
        default=False,
    )
    algorithm_group.add_argument(
        "--population-size", type=int, help="Size of the population.", default=None
    )
    algorithm_group.add_argument(
        "--elitism-rate",
        type=float,
        help="Rate of individuals preserved in the next generation.",
        default=None,
    )
    algorithm_group.add_argument(
        "--crossover-rate",
        type=float,
        help="Rate of individuals that will undergo crossover.",
        default=None,
    )
    algorithm_group.add_argument(
        "--mutation-rate",
        type=float,
        help="Rate of individuals that will undergo mutation.",
        default=None,
    )
    algorithm_group.add_argument(
        "--random-seed",
        type=int,
        help="Random seed to use for the algorithm.",
        default=None,
    )
    algorithm_group.add_argument(
        "--destruction-rate",
        type=float,
        help="Rate of individuals that will be randomly destroyed in every generation.",
        default=None,
    )
    algorithm_group.add_argument(
        "--max-repetition-rate",
        type=float,
        help="Rate at which the number of maximal repetitions should be increased.",
        default=None,
    )
    algorithm_group.add_argument(
        "--max-repetitions",
        type=int,
        help="Maximal value the number of repetitions can be increased to.",
        default=None,
    )
    algorithm_group.add_argument(
        "--max-node-rate",
        type=float,
        help="Rate at which the maximal number of nodes in a tree is increased.",
        default=None,
    )
    algorithm_group.add_argument(
        "--max-nodes",
        type=int,
        help="Maximal value, the number of nodes in a tree can be increased to.",
        default=None,
    )
    algorithm_group.add_argument(
        "-n",
        "--desired-solutions",
        "--num-outputs",
        type=int,
        help="Number of outputs to produce.",
        default=None,
    )
    algorithm_group.add_argument(
        "--best-effort",
        dest="best_effort",
        action="store_true",
        help="Produce a 'best effort' population (may not satisfy all constraints).",
        default=None,
    )
    algorithm_group.add_argument(
        "-i",
        "--initial-population",
        type=str,
        help="Directory or ZIP archive with initial population.",
        default=None,
    )

    # Shared Settings
    settings_parser = argparse.ArgumentParser(add_help=False)
    settings_group = settings_parser.add_argument_group("General settings")

    settings_group.add_argument(
        "--warnings-are-errors",
        dest="warnings_are_errors",
        action="store_true",
        help="Treat warnings as errors.",
        default=None,
    )

    if not in_command_line:
        # Use `set -vv` or `set -q` to change logging levels
        verbosity_option = settings_group.add_mutually_exclusive_group()
        verbosity_option.add_argument(
            "--verbose",
            "-v",
            dest="verbose",
            action="count",
            help="Increase verbosity. Can be given multiple times (-vv).",
        )
        verbosity_option.add_argument(
            "--quiet",
            "-q",
            dest="quiet",
            action="store_true",
            help="Decrease verbosity. Can be given multiple times (-qq).",
        )

    # Shared file options
    file_parser = argparse.ArgumentParser(add_help=False)
    file_group = file_parser.add_argument_group("Fandango file settings")

    file_group.add_argument(
        "-f",
        "--fandango-file",
        type=argparse.FileType("r"),
        dest="fan_files",
        metavar="FAN_FILE",
        default=None,
        # required=True,
        action="append",
        help="Fandango file (.fan, .py) to be processed. Can be given multiple times. Use '-' for stdin.",
    )
    file_group.add_argument(
        "-c",
        "--constraint",
        type=str,
        dest="constraints",
        metavar="CONSTRAINT",
        default=None,
        action="append",
        help="Define an additional constraint CONSTRAINT. Can be given multiple times.",
    )
    file_group.add_argument(
        "-S",
        "--start-symbol",
        type=str,
        help="The grammar start symbol (default: '<start>').",
        default=None,
    )
    file_group.add_argument(
        "--max",
        "--maximize",
        type=str,
        dest="maxconstraints",
        metavar="MAXCONSTRAINT",
        default=None,
        action="append",
        help="Define an additional constraint MAXCONSTRAINT to be maximized. Can be given multiple times.",
    )
    file_group.add_argument(
        "--min",
        "--minimize",
        type=str,
        dest="minconstraints",
        metavar="MINCONSTRAINTS",
        default=None,
        action="append",
        help="Define an additional constraint MINCONSTRAINT to be minimized. Can be given multiple times.",
    )
    file_group.add_argument(
        "-I",
        "--include-dir",
        type=str,
        dest="includes",
        metavar="DIR",
        default=None,
        action="append",
        help="Specify a directory DIR to search for included Fandango files.",
    )
    file_group.add_argument(
        "--file-mode",
        choices=["text", "binary", "auto"],
        default="auto",
        help="Mode in which to open and write files (default is 'auto': 'binary' if grammar has bits or bytes, 'text' otherwise).",
    )
    file_group.add_argument(
        "--no-cache",
        default=True,
        dest="use_cache",
        action="store_false",
        help="Do not cache parsed Fandango files.",
    )
    file_group.add_argument(
        "--no-stdlib",
        default=True,
        dest="use_stdlib",
        action="store_false",
        help="Do not include the standard Fandango library.",
    )

    output_parser = argparse.ArgumentParser(add_help=False)
    output_group = file_parser.add_argument_group("Output settings")

    output_group.add_argument(
        "-s",
        "--separator",
        type=str,
        default="\n",
        help="Output SEPARATOR between individual inputs. (default: newline).",
    )
    output_group.add_argument(
        "-d",
        "--directory",
        type=str,
        dest="directory",
        default=None,
        help="Create individual output files in DIRECTORY.",
    )
    output_group.add_argument(
        "-x",
        "--filename-extension",
        type=str,
        default=".txt",
        help="Extension of generated file names (default: '.txt').",
    )
    output_group.add_argument(
        "--format",
        choices=["string", "bits", "tree", "grammar", "value", "repr", "none"],
        default="string",
        help="Produce output(s) as string (default), as a bit string, as a derivation tree, as a grammar, as a Python value, in internal representation, or none.",
    )
    output_group.add_argument(
        "--validate",
        default=False,
        action="store_true",
        help="Run internal consistency checks for debugging.",
    )

    parties_parser = argparse.ArgumentParser(add_help=False)
    parties_group = parties_parser.add_argument_group("Party settings")
    parties_group.add_argument(
        "--party",
        action="append",
        dest="parties",
        metavar="PARTY",
        help="Only consider the PARTY part of the interaction in the .fan file.",
    )

    # Commands

    # Fuzz
    fuzz_parser = commands.add_parser(
        "fuzz",
        help="Produce outputs from .fan files and test programs.",
        parents=[
            file_parser,
            output_parser,
            algorithm_parser,
            settings_parser,
            parties_parser,
        ],
    )
    fuzz_parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: stdout).",
    )

    command_group = fuzz_parser.add_argument_group("command invocation settings")

    command_group.add_argument(
        "--input-method",
        choices=["stdin", "filename", "libfuzzer"],
        default="filename",
        help="When invoking COMMAND, choose whether Fandango input will be passed as standard input (`stdin`), as last argument on the command line (`filename`) (default), or to a libFuzzer style harness compiled to a shared .so/.dylib object (`libfuzzer`).",
    )
    command_group.add_argument(
        "test_command",
        metavar="command",
        type=str,
        nargs="?",
        help="Command to be invoked with a Fandango input.",
    )
    command_group.add_argument(
        "test_args",
        metavar="args",
        type=str,
        nargs=argparse.REMAINDER,
        help="The arguments of the command.",
    )

    # Parse
    parse_parser = commands.add_parser(
        "parse",
        help="Parse input file(s) according to .fan spec.",
        parents=[file_parser, output_parser, settings_parser, parties_parser],
    )
    parse_parser.add_argument(
        "input_files",
        metavar="files",
        type=str,
        nargs="*",
        help="Files to be parsed. Use '-' for stdin.",
    )
    parse_parser.add_argument(
        "--prefix",
        action="store_true",
        default=False,
        help="Parse a prefix only.",
    )
    parse_parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: none). Use '-' for stdout.",
    )

    # Talk
    talk_parser = commands.add_parser(
        "talk",
        help="Interact with programs, clients, and servers.",
        parents=[file_parser, algorithm_parser, settings_parser],
    )
    host_pattern = (
        "PORT on HOST (default: 127.0.0.1;"
        + " use '[...]' for IPv6 addresses)"
        + " using PROTOCOL ('tcp' (default)/'udp')."
    )
    talk_parser.add_argument(
        "--client",
        metavar="[NAME=][PROTOCOL:][HOST:]PORT",
        type=str,
        help="Act as a client NAME (default: 'Client') connecting to " + host_pattern,
    )
    talk_parser.add_argument(
        "--server",
        metavar="[NAME=][PROTOCOL:][HOST:]PORT",
        type=str,
        help="Act as a server NAME (default: 'Server') running at " + host_pattern,
    )
    talk_parser.add_argument(
        "test_command",
        metavar="command",
        type=str,
        nargs="?",
        help="Optional command to be interacted with.",
    )
    talk_parser.add_argument(
        "test_args",
        metavar="args",
        type=str,
        nargs=argparse.REMAINDER,
        help="The arguments of the command.",
    )

    # Convert
    convert_parser = commands.add_parser(
        "convert",
        help="Convert given external spec to .fan format.",
        parents=[parties_parser],
    )
    convert_parser.add_argument(
        "--from",
        dest="from_format",
        choices=["antlr", "g4", "dtd", "010", "bt", "fan", "auto"],
        default="auto",
        help="Format of the external spec file: 'antlr'/'g4' (ANTLR), 'dtd' (XML DTD), '010'/'bt' (010 Editor Binary Template), 'fan' (Fandango spec), or 'auto' (default: try to guess from file extension).",
    )
    convert_parser.add_argument(
        "--endianness", choices=["little", "big"], help="Set endianness for .bt files."
    )
    convert_parser.add_argument(
        "--bitfield-order",
        choices=["left-to-right", "right-to-left"],
        help="Set bitfield order for .bt files.",
    )
    convert_parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: stdout).",
    )
    convert_parser.add_argument(
        "convert_files",
        type=str,
        metavar="FILENAME",
        default=None,
        nargs="+",
        help="External spec file to be converted. Use '-' for stdin.",
    )

    clear_cache_parser = commands.add_parser(
        "clear-cache",
        help="Clear the Fandango parsing cache.",
    )
    clear_cache_parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="Just output the action to be performed; do not actually clear the cache.",
    )

    if not in_command_line:
        # Set
        _set_parser = commands.add_parser(
            "set",
            help="Set or print default arguments.",
            parents=[
                file_parser,
                output_parser,
                algorithm_parser,
                settings_parser,
                parties_parser,
            ],
        )

    if not in_command_line:
        # Reset
        _reset_parser = commands.add_parser(
            "reset",
            help="Reset defaults.",
        )

    if not in_command_line:
        # cd
        cd_parser = commands.add_parser(
            "cd",
            help="Change directory.",
        )
        cd_parser.add_argument(
            "directory",
            type=str,
            nargs="?",
            default=None,
            help="The directory to change into.",
        )

    if not in_command_line:
        # Exit
        _exit_parser = commands.add_parser(
            "exit",
            help="Exit Fandango.",
        )

    if in_command_line:
        # Shell
        shell_parser = commands.add_parser(
            "shell",
            help="Run an interactive shell (default).",
        )

    if not in_command_line:
        # Shell escape
        # Not processed by argparse,
        # but we have it here so that it is listed in help
        shell_parser = commands.add_parser(
            "!",
            help="Execute shell command.",
        )
        shell_parser.add_argument(
            dest="shell_command",
            metavar="command",
            nargs=argparse.REMAINDER,
            default=None,
            help="The shell command to execute.",
        )

        # Python escape
        # Not processed by argparse,
        # but we have it here so that it is listed in help
        python_parser = commands.add_parser(
            "/",
            help="Execute Python command.",
        )
        python_parser.add_argument(
            dest="python_command",
            metavar="command",
            nargs=argparse.REMAINDER,
            default=None,
            help="The Python command to execute.",
        )

    # Help
    help_parser = commands.add_parser(
        "help",
        help="Show this help and exit.",
    )
    help_parser.add_argument(
        "help_command",
        type=str,
        metavar="command",
        nargs="*",
        default=None,
        help="Command to get help on.",
    )

    # Copyright
    _copyright_parser = commands.add_parser(
        "copyright",
        help="Show copyright.",
    )

    # Version
    _version_parser = commands.add_parser(
        "version",
        help="Show version.",
    )

    return main_parser


def help_command(args: argparse.Namespace, in_command_line: bool = True) -> None:
    parser = get_parser(in_command_line)

    help_issued = False
    for cmd in args.help_command:
        try:
            parser.parse_args([cmd] + ["--help"])
            help_issued = True
        except SystemExit:
            help_issued = True
            pass
        except argparse.ArgumentError:
            print("Unknown command:", cmd, file=sys.stderr)

    if not help_issued:
        parser.print_help()


def exit_command(args: argparse.Namespace) -> None:
    pass


def parse_files_from_args(
    args: argparse.Namespace,
    given_grammars: list[Grammar] = [],
    check: bool = True,
) -> tuple[Grammar | None, list[Constraint | SoftValue]]:
    """Parse .fan files as given in args"""
    return parse(
        args.fan_files,
        [],
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

    if hasattr(args, "initial_population") and args.initial_population is not None:
        settings["initial_population"] = extract_initial_population(
            args.initial_population
        )
    return settings


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


# Default Fandango file content (grammar, constraints); set with `set`
DEFAULT_FAN_CONTENT: tuple[Grammar | None, list[Constraint | SoftValue]] = (None, [])

# Additional Fandango constraints; set with `set`
DEFAULT_CONSTRAINTS: list[Constraint | SoftValue] = []

# Default Fandango algorithm settings; set with `set`
DEFAULT_SETTINGS: dict[str, Any] = {}


def set_command(args: argparse.Namespace) -> None:
    """Set global settings"""
    global DEFAULT_FAN_CONTENT
    global DEFAULT_CONSTRAINTS
    global DEFAULT_SETTINGS

    if args.fan_files:
        LOGGER.info("Parsing Fandango content")
        grammar, constraints = parse_contents_from_args(args)
        DEFAULT_FAN_CONTENT = (grammar, constraints)
        DEFAULT_CONSTRAINTS = []  # Don't leave these over
    elif args.constraints or args.maxconstraints or args.minconstraints:
        default_grammar = DEFAULT_FAN_CONTENT[0]
        if not default_grammar:
            raise FandangoError("Open a `.fan` file first ('set -f FILE.fan')")

        LOGGER.info("Parsing Fandango constraints")
        _, constraints = parse_constraints_from_args(
            args, given_grammars=[default_grammar]
        )
        DEFAULT_CONSTRAINTS = constraints

    settings = make_fandango_settings(args)
    for setting in settings:
        DEFAULT_SETTINGS[setting] = settings[setting]

    no_args = not args.fan_files and not args.constraints and not settings

    if no_args:
        # Report current settings
        LOGGER.info("Did not receive an arg for set, printing settings")
        grammar, constraints = DEFAULT_FAN_CONTENT
        if grammar:
            for symbol in grammar.rules:
                print(grammar.get_repr_for_rule(symbol))
        if constraints:
            for constraint in constraints:
                print("where " + str(constraint))

    if no_args or (DEFAULT_CONSTRAINTS and sys.stdin.isatty()):
        for constraint in DEFAULT_CONSTRAINTS:
            print("where " + str(constraint) + "  # set by user")
    if no_args or (DEFAULT_SETTINGS and sys.stdin.isatty()):
        for setting in DEFAULT_SETTINGS:
            print(
                "--" + setting.replace("_", "-") + "=" + str(DEFAULT_SETTINGS[setting])
            )


def reset_command(args: argparse.Namespace) -> None:
    """Reset global settings"""
    global DEFAULT_SETTINGS
    DEFAULT_SETTINGS = {}

    global DEFAULT_CONSTRAINTS
    DEFAULT_CONSTRAINTS = []


def cd_command(args: argparse.Namespace) -> None:
    """Change current directory"""
    if args.directory:
        os.chdir(args.directory)
    else:
        os.chdir(Path.home())

    if sys.stdin.isatty():
        print(os.getcwd())


def output(
    tree: DerivationTree, args: argparse.Namespace, file_mode: str
) -> str | bytes:
    assert file_mode == "binary" or file_mode == "text"

    if args.format == "string":
        if file_mode == "binary":
            LOGGER.debug("Output as bytes")
            return tree.to_bytes()
        elif file_mode == "text":
            LOGGER.debug("Output as text")
            return tree.to_string()

    def convert(s: str) -> str | bytes:
        if file_mode == "binary":
            return s.encode("utf-8")
        else:
            return s

    LOGGER.debug(f"Output as {args.format}")

    if args.format == "tree":
        return convert(tree.to_tree())
    if args.format == "repr":
        return convert(tree.to_repr())
    if args.format == "bits":
        return convert(tree.to_bits())
    if args.format == "grammar":
        return convert(tree.to_grammar())
    if args.format == "value":
        return convert(tree.to_value())
    if args.format == "none":
        return convert("")

    raise NotImplementedError("Unsupported output format")


def open_file(filename: str, file_mode: str, *, mode: str = "r") -> IO[Any]:
    assert file_mode == "binary" or file_mode == "text"

    if file_mode == "binary":
        mode += "b"

    LOGGER.debug(f"Opening {filename!r}; mode={mode!r}")

    if filename == "-":
        if "b" in mode:
            return sys.stdin.buffer if "r" in mode else sys.stdout.buffer
        else:
            return sys.stdin if "r" in mode else sys.stdout

    return open(filename, mode)


def output_population(
    population: list[DerivationTree],
    args: argparse.Namespace,
    file_mode: str,
    *,
    output_on_stdout: bool = True,
) -> None:
    if args.format == "none":
        return

    for i, solution in enumerate(population):
        output_solution(solution, args, i, file_mode, output_on_stdout=output_on_stdout)


def output_solution_to_directory(
    solution: DerivationTree,
    args: argparse.Namespace,
    solution_index: int,
    file_mode: str,
) -> None:
    LOGGER.debug(f"Storing solution in directory {args.directory!r}")
    os.makedirs(args.directory, exist_ok=True)

    basename = f"fandango-{solution_index:04d}{args.filename_extension}"
    filename = os.path.join(args.directory, basename)
    with open_file(filename, file_mode, mode="w") as fd:
        fd.write(output(solution, args, file_mode))


def output_solution_to_file(
    solution: DerivationTree,
    args: argparse.Namespace,
    file_mode: str,
) -> None:
    LOGGER.debug(f"Storing solution in file {args.output!r}")
    with open_file(args.output, file_mode, mode="a") as fd:
        try:
            position = fd.tell()
        except (UnsupportedOperation, OSError):
            # If we're writing to stdout, tell() may not be supported
            position = 0

        if position > 0:
            fd.write(
                args.separator.encode("utf-8")
                if file_mode == "binary"
                else args.separator
            )
        fd.write(output(solution, args, file_mode))


def output_solution_with_test_command(
    solution: DerivationTree, args: argparse.Namespace, file_mode: str
) -> None:
    LOGGER.info(f"Running {args.test_command}")
    base_cmd = [args.test_command] + args.test_args

    if args.input_method == "filename":
        prefix = "fandango-"
        suffix = args.filename_extension
        mode = "wb" if file_mode == "binary" else "w"

        # The return type is private, so we need to use Any
        def named_temp_file(*, mode: str, prefix: str, suffix: str) -> Any:
            try:
                # Windows needs delete_on_close=False, so the subprocess can access the file by name
                return tempfile.NamedTemporaryFile(  # type: ignore [call-overload] # the mode type is not available from the library
                    mode=mode,
                    prefix=prefix,
                    suffix=suffix,
                    delete_on_close=False,
                )
            except Exception:
                # Python 3.11 and earlier have no 'delete_on_close'
                return tempfile.NamedTemporaryFile(
                    mode=mode, prefix=prefix, suffix=suffix
                )

        with named_temp_file(mode=mode, prefix=prefix, suffix=suffix) as fd:
            fd.write(output(solution, args, file_mode))
            fd.flush()
            cmd = base_cmd + [fd.name]
            LOGGER.debug(f"Running {cmd}")
            subprocess.run(cmd, text=True)
    elif args.input_method == "stdin":
        cmd = base_cmd
        LOGGER.debug(f"Running {cmd} with individual as stdin")
        subprocess.run(
            cmd,
            input=output(solution, args, file_mode),
            text=(None if file_mode == "binary" else True),
        )
    elif args.input_method == "libfuzzer":
        if args.file_mode != "binary" or file_mode != "binary":
            raise NotImplementedError("LibFuzzer harnesses only support binary input")
        harness = ctypes.CDLL(args.test_command).LLVMFuzzerTestOneInput

        bytes = output(solution, args, file_mode)
        harness(bytes, len(bytes))
    else:
        raise NotImplementedError("Unsupported input method")


def output_solution_to_stdout(
    solution: DerivationTree,
    args: argparse.Namespace,
    file_mode: str,
) -> None:
    LOGGER.debug("Printing solution on stdout")
    out = output(solution, args, file_mode)
    if not isinstance(out, str):
        out = out.decode("iso8859-1")
    print(out, end="")
    print(args.separator, end="")


def output_solution(
    solution: DerivationTree,
    args: argparse.Namespace,
    solution_index: int,
    file_mode: str,
    *,
    output_on_stdout: bool = True,
) -> None:
    assert file_mode == "binary" or file_mode == "text"

    if args.format == "none":
        return
    if "output" not in args:
        return

    if args.directory:
        output_solution_to_directory(solution, args, solution_index, file_mode)
        output_on_stdout = False

    if args.output:
        output_solution_to_file(solution, args, file_mode)
        output_on_stdout = False

    if "test_command" in args and args.test_command:
        output_solution_with_test_command(solution, args, file_mode)
        output_on_stdout = False

    # Default
    if output_on_stdout:
        output_solution_to_stdout(solution, args, file_mode)


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
    if "start_symbol" in settings:
        start_symbol = settings["start_symbol"]
    else:
        start_symbol = "<start>"

    allow_incomplete = hasattr(args, "prefix") and args.prefix
    parsing_mode = Grammar.Parser.ParsingMode.COMPLETE
    if allow_incomplete:
        parsing_mode = Grammar.Parser.ParsingMode.INCOMPLETE
    tree_gen = grammar.parse_forest(individual, start=start_symbol, mode=parsing_mode)

    alternative_counter = 1
    passing_tree = None
    last_tree = None
    while tree := next(tree_gen, None):
        LOGGER.debug(f"Checking parse alternative #{alternative_counter}")
        last_tree = tree
        grammar.populate_sources(last_tree)

        passed = True
        for constraint in constraints:
            fitness = constraint.fitness(tree).fitness()
            LOGGER.debug(f"Fitness: {fitness}")
            if fitness == 0:
                passed = False
                break

        if passed:
            passing_tree = tree
            break

        # Try next parsing alternative
        alternative_counter += 1

    if passing_tree:
        # Found an alternative that satisfies all constraints

        # Validate tree
        if args.validate:
            validate(individual, passing_tree, filename=fd.name)

        return passing_tree

    # Tried all alternatives
    if last_tree is None:
        error_pos = grammar.max_position() + 1
        raise FandangoParseError(
            report_syntax_error(fd.name, error_pos, individual, binary=("b" in fd.mode))
        )

    # Report error for the last tree
    for constraint in constraints:
        fitness = constraint.fitness(last_tree).fitness()
        if fitness == 0:
            raise FandangoError(f"{fd.name!r}: constraint {constraint} not satisfied")

    raise FandangoError("This should not happen")


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
        if tree.contains_bits() or tree.contains_bytes():
            return "binary"
        else:
            return "text"

    raise FandangoError("Cannot determine file mode")


def fuzz_command(args: argparse.Namespace) -> None:
    """Invoke the fuzzer"""

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    LOGGER.debug("Starting Fandango")
    fandango = Fandango._with_parsed(
        grammar,
        constraints,
        start_symbol=args.start_symbol,
        logging_level=LOGGER.getEffectiveLevel(),
    )
    LOGGER.debug("Evolving population")

    def solutions_callback(sol, i):
        return output_solution(sol, args, i, file_mode)

    max_generations = args.max_generations
    desired_solutions = args.desired_solutions
    infinite = args.infinite

    population = fandango.fuzz(
        solution_callback=solutions_callback,
        max_generations=max_generations,
        desired_solutions=desired_solutions,
        infinite=infinite,
        mode=FuzzingMode.COMPLETE,
        **settings,
    )

    if args.validate:
        LOGGER.debug("Validating population")

        # Ensure that every generated file can be parsed
        # and returns the same string as the original
        try:
            temp_dir = tempfile.TemporaryDirectory(delete=False)  # type: ignore [call-overload] # delete is only available on some OSs
        except TypeError:
            # Python 3.11 does not know the `delete` argument
            temp_dir = tempfile.TemporaryDirectory()
        args.directory = temp_dir.name
        args.format = "string"
        output_population(population, args, file_mode=file_mode, output_on_stdout=False)
        generated_files = glob.glob(args.directory + "/*")
        generated_files.sort()
        assert len(generated_files) == len(population)

        errors = 0
        for i in range(len(generated_files)):
            generated_file = generated_files[i]
            individual = population[i]

            try:
                with open_file(generated_file, file_mode, mode="r") as fd:
                    tree = parse_file(fd, args, grammar, constraints, settings)
                    validate(individual, tree, filename=fd.name)

            except Exception as e:
                print_exception(e)
                errors += 1

        if errors:
            raise FandangoError(f"{errors} error(s) during validation")

        # If everything went well, clean up;
        # otherwise preserve file for debugging
        shutil.rmtree(temp_dir.name)


def parse_command(args: argparse.Namespace) -> None:
    """Parse given files"""
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    if not args.input_files:
        args.input_files = ["-"]

    population = []
    errors = 0

    for input_file in args.input_files:
        with open_file(input_file, file_mode, mode="r") as fd:
            try:
                tree = parse_file(fd, args, grammar, constraints, settings)
                population.append(tree)
            except Exception as e:
                print_exception(e)
                errors += 1
                tree = None

    if population and args.output:
        output_population(population, args, file_mode=file_mode, output_on_stdout=False)

    if errors:
        raise FandangoParseError(f"{errors} error(s) during parsing")


def talk_command(args: argparse.Namespace) -> None:
    """Interact with a program, client, or server"""
    # if not args.test_command and not args.client and not args.server:
    #     raise FandangoError(
    #         "Use '--client' or '--server' to create a client or server, "
    #         "or specify a command to interact with."
    #     )
    args.parties = []

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

    if grammar.fuzzing_mode != FuzzingMode.IO:
        LOGGER.warning("Fandango spec does not specify interaction parties")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    LOGGER.debug("Starting Fandango")

    fandango = Fandango._with_parsed(
        grammar=grammar,
        constraints=constraints,
        start_symbol=args.start_symbol,
        logging_level=LOGGER.getEffectiveLevel(),
    )
    LOGGER.debug("Evolving population")

    def solutions_callback(sol, i):
        return output_solution(sol, args, i, file_mode)

    max_generations = args.max_generations
    desired_solutions = args.desired_solutions
    infinite = args.infinite

    fandango.fuzz(
        solution_callback=solutions_callback,
        max_generations=max_generations,
        desired_solutions=desired_solutions,
        infinite=infinite,
        mode=FuzzingMode.IO,
        **settings,
    )


def convert_command(args: argparse.Namespace) -> None:
    """Convert a given language spec into Fandango .fan format"""

    output = args.output
    if output is None:
        output = sys.stdout

    for input_file in args.convert_files:
        from_format = args.from_format
        input_file_lower = input_file.lower()
        if from_format == "auto":
            if input_file_lower.endswith(".g4") or input_file_lower.endswith(".antlr"):
                from_format = "antlr"
            elif input_file_lower.endswith(".dtd"):
                from_format = "dtd"
            elif input_file_lower.endswith(".bt") or input_file_lower.endswith(".010"):
                from_format = "bt"
            elif input_file_lower.endswith(".fan"):
                from_format = "fan"
            else:
                raise FandangoError(
                    f"{input_file!r}: unknown file extension; use --from=FORMAT to specify the format"
                )

        temp_file = None
        if input_file == "-":
            # Read from stdin
            with open_file(input_file, "text", mode="r") as fd:
                contents = fd.read()
            temp_file = tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp"
            )
            temp_file.write(contents)
            temp_file.flush()
            input_file = temp_file.name

        converter: FandangoConverter
        match from_format:
            case "antlr" | "g4":
                converter = ANTLRFandangoConverter(input_file)
                spec = converter.to_fan()
            case "dtd":
                converter = DTDFandangoConverter(input_file)
                spec = converter.to_fan()
            case "bt" | "010":
                if args.endianness == "little":
                    endianness = Endianness.LittleEndian
                else:
                    endianness = Endianness.BigEndian
                if args.bitfield_order == "left-to-right":
                    bitfield_order = BitfieldOrder.LeftToRight
                else:
                    bitfield_order = BitfieldOrder.RightToLeft

                converter = BTFandangoConverter(input_file)
                spec = converter.to_fan(
                    endianness=endianness, bitfield_order=bitfield_order
                )
            case "fan":
                converter = FandangoFandangoConverter(input_file, parties=args.parties)
                spec = converter.to_fan()

        print(spec, file=output, end="")
        if temp_file:
            # Remove temporary file
            temp_file.close()
            os.unlink(temp_file.name)

    if output != sys.stdout:
        output.close()


def clear_command(args: argparse.Namespace) -> None:
    CACHE_DIR = cache_dir()
    if args.dry_run:
        print(f"Would clear {CACHE_DIR}", file=sys.stderr)
    elif os.path.exists(CACHE_DIR):
        print(f"Clearing {CACHE_DIR}...", file=sys.stderr, end="")
        clear_cache()
        print("done", file=sys.stderr)


def nop_command(args: argparse.Namespace) -> None:
    # Dummy command such that we can list ! and / as commands. Never executed.
    pass


def copyright_command(args: argparse.Namespace) -> None:
    print("Copyright (c) 2024-2025 CISPA Helmholtz Center for Information Security.")
    print("All rights reserved.")


def version_command(args: argparse.Namespace) -> None:
    if sys.stdout.isatty():
        version_line = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango{styles.color.close} {fandango.version()}"
    else:
        version_line = f"Fandango {fandango.version()}"
    print(version_line)


COMMANDS: dict[str, Callable[[argparse.Namespace], None]] = {
    "set": set_command,
    "reset": reset_command,
    "fuzz": fuzz_command,
    "parse": parse_command,
    "talk": talk_command,
    "convert": convert_command,
    "clear-cache": clear_command,
    "cd": cd_command,
    "help": help_command,
    "copyright": copyright_command,
    "version": version_command,
    "exit": exit_command,
    "!": nop_command,
    "/": nop_command,
}


def get_help(cmd: str) -> str:
    """Return the help text for CMD"""
    parser = get_parser(in_command_line=False)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    try:
        parser.parse_args([cmd] + ["--help"])
    except SystemExit:
        pass

    sys.stdout = old_stdout
    return mystdout.getvalue()


def get_options(cmd: str) -> list[str]:
    """Return all --options for CMD"""
    if cmd == "help":
        return list(COMMANDS.keys())

    help = get_help(cmd)
    options = []
    for option in re.findall(r"--?[a-zA-Z0-9_-]*", help):
        if option not in options:
            options.append(option)
    return options


def get_filenames(prefix: str = "", fan_only: bool = True) -> list[str]:
    """Return all files that match PREFIX"""
    filenames = []
    all_filenames = glob.glob(prefix + "*")
    for filename in all_filenames:
        if os.path.isdir(filename):
            filenames.append(filename + os.sep)
        elif (
            not fan_only
            or filename.lower().endswith(".fan")
            or filename.lower().endswith(".py")
        ):
            filenames.append(filename)

    return filenames


def complete(text: str) -> list[str]:
    """Return possible completions for TEXT"""
    LOGGER.debug("Completing " + repr(text))

    if not text:
        # No text entered, all commands possible
        completions = [s for s in COMMANDS.keys()]
        LOGGER.debug("Completions: " + repr(completions))
        return completions

    completions = []
    for s in COMMANDS.keys():
        if s.startswith(text):
            completions.append(s + " ")
    if completions:
        # Beginning of command entered
        LOGGER.debug("Completions: " + repr(completions))
        return completions

    # Complete command
    words = text.split()
    cmd = words[0]
    shell = cmd.startswith("!") or cmd.startswith("/")

    if not shell and cmd not in COMMANDS.keys():
        # Unknown command
        return []

    if len(words) == 1 or text.endswith(" "):
        last_arg = ""
    else:
        last_arg = words[-1]

    # print(f"last_arg = {last_arg}")
    completions = []

    if not shell:
        cmd_options = get_options(cmd)
        for option in cmd_options:
            if not last_arg or option.startswith(last_arg):
                completions.append(option + " ")

    if shell or len(words) >= 2:
        # Argument for an option
        filenames = get_filenames(prefix=last_arg, fan_only=not shell)
        for filename in filenames:
            if filename.endswith(os.sep):
                completions.append(filename)
            else:
                completions.append(filename + " ")

    LOGGER.debug("Completions: " + repr(completions))
    return completions


# print(complete(""))
# print(complete("set "))
# print(complete("set -"))
# print(complete("set -f "))
# print(complete("set -f do"))


def exec_single(
    code: str, _globals: dict[str, Any] = {}, _locals: dict[str, Any] = {}
) -> None:
    """Execute CODE in 'single' mode, printing out results if any"""
    block = compile(code, "<input>", mode="single")
    exec(block, _globals, _locals)


MATCHES = []


def shell_command(args: argparse.Namespace) -> None:
    """Interactive mode"""

    PROMPT = "(fandango)"

    def _read_history() -> None:
        if "readline" not in globals():
            return

        histfile = os.path.join(os.path.expanduser("~"), ".fandango_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        except Exception as e:
            LOGGER.warning(f"Could not read {histfile}: {e}")

        atexit.register(readline.write_history_file, histfile)

    def _complete(text: str, state: int) -> str | None:
        if "readline" not in globals():
            return None

        global MATCHES
        if state == 0:  # first trigger
            buffer = readline.get_line_buffer()[: readline.get_endidx()]
            MATCHES = complete(buffer)
        try:
            return MATCHES[state]
        except IndexError:
            return None

    if sys.stdin.isatty():
        if "readline" in globals():
            _read_history()
            readline.set_completer_delims(" \t\n;")
            readline.set_completer(_complete)
            readline.parse_and_bind("tab: complete")

        version_command(argparse.Namespace())
        print("Type a command, 'help', 'copyright', 'version', or 'exit'.")

    while True:
        if sys.stdin.isatty():
            try:
                command_line = input(PROMPT + " ").lstrip()
            except KeyboardInterrupt:
                print("\nEnter a command, 'help', or 'exit'")
                continue
            except EOFError:
                break
        else:
            try:
                command_line = input().lstrip()
            except EOFError:
                break

        if command_line.startswith("!"):
            # Shell escape
            LOGGER.debug(command_line)
            if sys.stdin.isatty():
                os.system(command_line[1:])
            else:
                raise FandangoError(
                    "Shell escape (`!`) is only available in interactive mode"
                )
            continue

        if command_line.startswith("/"):
            # Python escape
            LOGGER.debug(command_line)
            if sys.stdin.isatty():
                try:
                    exec_single(command_line[1:].lstrip(), globals())
                except Exception as e:
                    print_exception(e)
            else:
                raise FandangoError(
                    "Python escape (`/`) is only available in interactive mode"
                )
            continue

        command: Any = None
        try:
            command = shlex.split(command_line, comments=True)
        except Exception as e:
            print_exception(e)
            continue

        if not command:
            continue

        if command[0].startswith("exit"):
            break

        parser = get_parser(in_command_line=False)
        try:
            args = parser.parse_args(command)
        except argparse.ArgumentError:
            parser.print_usage()
            continue
        except SystemExit:
            continue

        if args.command not in COMMANDS:
            parser.print_usage()
            continue

        LOGGER.debug(args.command + "(" + str(args) + ")")
        try:
            if args.command == "help":
                help_command(args, in_command_line=False)
            else:
                command = COMMANDS[args.command]
                run(command, args)
        except SystemExit:
            pass
        except KeyboardInterrupt:
            pass


def run(command: Callable[[argparse.Namespace], None], args: argparse.Namespace) -> int:
    try:
        command(args)
    except Exception as e:
        print_exception(e)
        return 1

    return 0


def main(
    *argv: str, stdout: IO[Any] | None = sys.stdout, stderr: IO[Any] | None = sys.stderr
) -> int:
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    parser = get_parser(in_command_line=True)
    args = parser.parse_args(argv or sys.argv[1:])

    LOGGER.setLevel(os.getenv("FANDANGO_LOG_LEVEL", "WARNING"))  # Default

    if args.quiet and args.quiet == 1:
        LOGGER.setLevel(logging.WARNING)  # (Back to default)
    elif args.quiet and args.quiet > 1:
        LOGGER.setLevel(logging.ERROR)  # Even quieter
    elif args.verbose and args.verbose == 1:
        LOGGER.setLevel(logging.INFO)  # Give more info
    elif args.verbose and args.verbose > 1:
        LOGGER.setLevel(logging.DEBUG)  # Even more info

    # Set parsing method for .fan files
    fandango.Fandango.parser = args.parser

    if args.command in COMMANDS:
        # LOGGER.info(args.command)
        command = COMMANDS[args.command]
        last_status = run(command, args)
    elif args.command is None or args.command == "shell":
        last_status = run(shell_command, args)
    else:
        parser.print_usage()
        last_status = 2

    return last_status


if __name__ == "__main__":
    sys.exit(main())
