import argparse
import ast
import atexit
import glob
import importlib.metadata
import logging
import os
import os.path
import re
import readline
import shlex
import subprocess
import sys
import tempfile
import textwrap
import zipfile
import shutil

from io import StringIO
from io import UnsupportedOperation
from pathlib import Path
from ansi_styles import ansiStyles as styles
from enum import Enum

from ansi_styles import ansiStyles as styles
from antlr4.error.Errors import ParseCancellationException

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.logger import LOGGER, print_exception


def get_parser(in_command_line=True):
    # Main parser
    if in_command_line:
        prog = "fandango"
        epilog = """\
            Use `%(prog)s help` to get a list of commands.
            Use `%(prog)s help COMMAND` to learn more about COMMAND."""
    else:
        prog = ""
        epilog = """
            Use `help` to get a list of commands.
            Use `help COMMAND` to learn more about COMMAND.
            Use TAB to complete commands.
            """

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
            version="Fandango " + importlib.metadata.version("fandango-fuzzer"),
            help="show version number",
        )

        verbosity_option = main_parser.add_mutually_exclusive_group()
        verbosity_option.add_argument(
            "--verbose",
            "-v",
            dest="verbose",
            action="count",
            help="increase verbosity. Can be given multiple times (-vv)",
        )
        verbosity_option.add_argument(
            "--quiet",
            "-q",
            dest="quiet",
            action="count",
            help="decrease verbosity. Can be given multiple times (-qq)",
        )

    # The subparsers
    commands = main_parser.add_subparsers(
        title="commands",
        # description="Valid commands",
        help="the command to execute",
        dest="command",
        # required=True,
    )

    # Algorithm Settings
    algorithm_parser = argparse.ArgumentParser(add_help=False)
    algorithm_group = algorithm_parser.add_argument_group("algorithm settings")

    algorithm_group.add_argument(
        "-N",
        "--max-generations",
        type=int,
        help="the maximum number of generations to run the algorithm",
        default=None,
    )
    algorithm_group.add_argument(
        "--population-size", type=int, help="the size of the population", default=None
    )
    algorithm_group.add_argument(
        "--elitism-rate",
        type=float,
        help="the rate of individuals preserved in the next generation",
        default=None,
    )
    algorithm_group.add_argument(
        "--crossover-rate",
        type=float,
        help="the rate of individuals that will undergo crossover",
        default=None,
    )
    algorithm_group.add_argument(
        "--mutation-rate",
        type=float,
        help="the rate of individuals that will undergo mutation",
        default=None,
    )
    algorithm_group.add_argument(
        "--random-seed",
        type=int,
        help="the random seed to use for the algorithm",
        default=None,
    )
    algorithm_group.add_argument(
        "--destruction-rate",
        type=float,
        help="the rate of individuals that will be randomly destroyed in every generation",
        default=None,
    )
    algorithm_group.add_argument(
        "-n",
        "--num-outputs",
        "--desired-solutions",
        type=int,
        help="the number of outputs to produce (default: 100)",
        default=None,
    )
    algorithm_group.add_argument(
        "--best-effort",
        dest="best_effort",
        action="store_true",
        help="produce a 'best effort' population (may not satisfy all constraints)",
        default=None,
    )
    algorithm_group.add_argument(
        "-i",
        "--initial-population",
        type=str,
        help="directory or ZIP archive with initial population",
        default=None,
    )

    # Shared Settings
    settings_parser = argparse.ArgumentParser(add_help=False)
    settings_group = settings_parser.add_argument_group("general settings")

    settings_group.add_argument(
        "-S",
        "--start-symbol",
        type=str,
        help="the grammar start symbol (default: `<start>`)",
        default=None,
    )
    settings_group.add_argument(
        "--warnings-are-errors",
        dest="warnings_are_errors",
        action="store_true",
        help="treat warnings as errors",
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
            help="increase verbosity. Can be given multiple times (-vv)",
        )
        verbosity_option.add_argument(
            "--quiet",
            "-q",
            dest="quiet",
            action="store_true",
            help="decrease verbosity. Can be given multiple times (-qq)",
        )

    # Shared file options
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-f",
        "--fandango-file",
        type=argparse.FileType("r"),
        dest="fan_files",
        metavar="FAN_FILE",
        default=None,
        # required=True,
        action="append",
        help="Fandango file (.fan, .py) to be processed. Can be given multiple times. Use '-' for stdin",
    )
    file_parser.add_argument(
        "-c",
        "--constraint",
        type=str,
        dest="constraints",
        metavar="CONSTRAINT",
        default=None,
        action="append",
        help="define an additional constraint CONSTRAINT. Can be given multiple times.",
    )
    file_parser.add_argument(
        "--no-cache",
        default=True,
        dest="use_cache",
        action="store_false",
        help="do not cache parsed Fandango files.",
    )
    file_parser.add_argument(
        "--no-stdlib",
        default=True,
        dest="use_stdlib",
        action="store_false",
        help="do not use standard library when parsing Fandango files.",
    )
    file_parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default="\n",
        help="output SEPARATOR between individual inputs. (default: newline)",
    )
    file_parser.add_argument(
        "-I",
        "--include-dir",
        type=str,
        dest="includes",
        metavar="DIR",
        default=None,
        action="append",
        help="specify a directory DIR to search for included Fandango files",
    )
    file_parser.add_argument(
        "-d",
        "--directory",
        type=str,
        dest="directory",
        default=None,
        help="create individual output files in DIRECTORY",
    )
    file_parser.add_argument(
        "-x",
        "--filename-extension",
        type=str,
        default=".txt",
        help="extension of generated file names (default: '.txt')",
    )
    file_parser.add_argument(
        "--format",
        choices=["string", "bits", "tree", "grammar", "none"],
        default="string",
        help="produce output(s) as string (default), as a bit string, as a derivation tree, as a grammar, or none",
    )
    file_parser.add_argument(
        "--file-mode",
        choices=["text", "binary", "auto"],
        default="auto",
        help="mode in which to open and write files (default is 'auto': 'binary' if grammar has bits or bytes, 'text' otherwise)",
    )
    file_parser.add_argument(
        "--validate",
        default=False,
        action="store_true",
        help="run internal consistency checks for debugging",
    )

    # Commands

    # Fuzz
    fuzz_parser = commands.add_parser(
        "fuzz",
        help="produce outputs from .fan files and test programs",
        parents=[file_parser, settings_parser, algorithm_parser],
    )
    fuzz_parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="write output to OUTPUT (default: stdout)",
    )

    command_group = fuzz_parser.add_argument_group("command invocation settings")

    command_group.add_argument(
        "--input-method",
        choices=["stdin", "filename"],
        default="filename",
        help="when invoking COMMAND, choose whether Fandango input will be passed as standard input (`stdin`) or as last argument on the command line (`filename`) (default)",
    )
    command_group.add_argument(
        "test_command",
        metavar="command",
        type=str,
        nargs="?",
        help="command to be invoked with a Fandango input",
    )
    command_group.add_argument(
        "test_args",
        metavar="args",
        type=str,
        nargs=argparse.REMAINDER,
        help="the arguments of the command",
    )

    # Parse
    parse_parser = commands.add_parser(
        "parse",
        help="parse input file(s) according to .fan spec",
        parents=[file_parser, settings_parser],
    )
    parse_parser.add_argument(
        "input_files",
        metavar="files",
        type=str,
        nargs="*",
        help="files to be parsed. Use '-' for stdin",
    )
    parse_parser.add_argument(
        "--prefix",
        action="store_true",
        default=False,
        help="parse a prefix only",
    )
    parse_parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="write output to OUTPUT (default: none). Use '-' for stdout",
    )

    if not in_command_line:
        # Set
        set_parser = commands.add_parser(
            "set",
            help="set or print default arguments",
            parents=[file_parser, settings_parser, algorithm_parser],
        )

    if not in_command_line:
        # Reset
        reset_parser = commands.add_parser(
            "reset",
            help="reset defaults",
        )

    if not in_command_line:
        # cd
        cd_parser = commands.add_parser(
            "cd",
            help="change directory",
        )
        cd_parser.add_argument(
            "directory",
            type=str,
            nargs="?",
            default=None,
            help="the directory to change into",
        )

    if not in_command_line:
        # Exit
        exit_parser = commands.add_parser(
            "exit",
            help="exit Fandango",
        )

    if in_command_line:
        # Shell
        shell_parser = commands.add_parser(
            "shell",
            help="run an interactive shell (default)",
        )

    if not in_command_line:
        # Shell escape
        # Not processed by argparse,
        # but we have it here so that it is listed in help
        shell_parser = commands.add_parser(
            "!",
            help="execute shell command",
        )
        shell_parser.add_argument(
            dest="shell_command",
            metavar="command",
            nargs=argparse.REMAINDER,
            default=None,
            help="the shell command to execute",
        )

        # Python escape
        # Not processed by argparse,
        # but we have it here so that it is listed in help
        python_parser = commands.add_parser(
            "/",
            help="execute Python command",
        )
        python_parser.add_argument(
            dest="python_command",
            metavar="command",
            nargs=argparse.REMAINDER,
            default=None,
            help="the Python command to execute",
        )

    # Help
    help_parser = commands.add_parser(
        "help",
        help="show this help and exit",
    )
    help_parser.add_argument(
        "help_command",
        type=str,
        metavar="command",
        nargs="*",
        default=None,
        help="command to get help on",
    )

    # Copyright
    copyright_parser = commands.add_parser(
        "copyright",
        help="show copyright",
    )

    # Version
    version_parser = commands.add_parser(
        "version",
        help="show version",
    )

    return main_parser


def help_command(args, **kwargs):
    parser = get_parser(**kwargs)
    parser.exit_on_error = False

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


def exit_command(args):
    pass


def parse_files_from_args(args, given_grammars=[]):
    """Parse .fan files as given in args"""
    return parse(
        args.fan_files,
        [],
        given_grammars=given_grammars,
        includes=args.includes,
        use_cache=args.use_cache,
        use_stdlib=args.use_stdlib,
        start_symbol=args.start_symbol,
    )


def parse_constraints_from_args(args, given_grammars=[]):
    """Parse .fan constraints as given in args"""
    return parse(
        [],
        args.constraints,
        given_grammars=given_grammars,
        includes=args.includes,
        use_cache=args.use_cache,
        use_stdlib=args.use_stdlib,
        start_symbol=args.start_symbol,
    )


def parse_contents_from_args(args, given_grammars=[]):
    """Parse .fan content as given in args"""
    return parse(
        args.fan_files,
        args.constraints,
        given_grammars=given_grammars,
        includes=args.includes,
        use_cache=args.use_cache,
        use_stdlib=args.use_stdlib,
        start_symbol=args.start_symbol,
    )


def make_fandango_settings(args, initial_settings={}):
    """Create keyword settings for Fandango() constructor"""

    def copy(settings, name, *, args_name=None):
        if args_name is None:
            args_name = name
        if hasattr(args, args_name) and getattr(args, args_name) is not None:
            settings[name] = getattr(args, args_name)
            LOGGER.debug(f"Settings: {name} is {settings[name]}")

    settings = initial_settings.copy()
    copy(settings, "population_size")
    copy(settings, "desired_solutions", args_name="num_outputs")
    copy(settings, "mutation_rate")
    copy(settings, "crossover_rate")
    copy(settings, "max_generations")
    copy(settings, "elitism_rate")
    copy(settings, "destruction_rate")
    copy(settings, "warnings_are_errors")
    copy(settings, "best_effort")
    copy(settings, "random_seed")

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


def extract_initial_population(path):
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
DEFAULT_FAN_CONTENT = (None, None)

# Additional Fandango constraints; set with `set`
DEFAULT_CONSTRAINTS = []

# Default Fandango algorithm settings; set with `set`
DEFAULT_SETTINGS = {}


def set_command(args):
    """Set global settings"""
    global DEFAULT_FAN_CONTENT
    global DEFAULT_CONSTRAINTS
    global DEFAULT_SETTINGS

    if args.fan_files:
        DEFAULT_FAN_CONTENT = None, None
        DEFAULT_CONSTRAINTS = []
        LOGGER.info("Parsing Fandango content")
        grammar, constraints = parse_contents_from_args(args)
        DEFAULT_FAN_CONTENT = (grammar, constraints)
        DEFAULT_CONSTRAINTS = []  # Don't leave these over
    elif args.constraints:
        default_grammar = DEFAULT_FAN_CONTENT[0]
        if not default_grammar:
            raise ValueError("Open a `.fan` file first ('set -f FILE.fan')")

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


def reset_command(args):
    """Reset global settings"""
    global DEFAULT_SETTINGS
    DEFAULT_SETTINGS = {}

    global DEFAULT_CONSTRAINTS
    DEFAULT_CONSTRAINTS = []


def cd_command(args):
    """Change current directory"""
    if args.directory:
        os.chdir(args.directory)
    else:
        os.chdir(Path.home())

    if sys.stdin.isatty():
        print(os.getcwd())


def output(tree, args, file_mode: str) -> str | bytes:
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
    if args.format == "bits":
        return convert(tree.to_bits())
    if args.format == "grammar":
        return convert(tree.to_grammar())
    if args.format == "none":
        return convert("")

    raise NotImplementedError("Unsupported output format")


def open_file(filename, file_mode, *, mode="r"):
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


def output_population(population, args, file_mode=None, *, output_on_stdout=True):
    assert file_mode == "binary" or file_mode == "text"

    if args.format == "none":
        return

    if args.directory:
        LOGGER.debug(f"Storing population in directory {args.directory!r}")
        try:
            os.mkdir(args.directory)
        except FileExistsError:
            pass

        counter = 1
        for individual in population:
            basename = f"fandango-{counter:04d}{args.filename_extension}"
            filename = os.path.join(args.directory, basename)
            with open_file(filename, file_mode, mode="w") as fd:
                fd.write(output(individual, args, file_mode))
            counter += 1

        output_on_stdout = False

    if args.output:
        LOGGER.debug(f"Storing population in file {args.output!r}")

        with open_file(args.output, file_mode, mode="w") as fd:
            sep = False
            for individual in population:
                if sep:
                    fd.write(
                        args.separator.encode("utf-8")
                        if file_mode == "binary"
                        else args.separator
                    )
                fd.write(output(individual, args, file_mode))
                sep = True

        output_on_stdout = False

    if "test_command" in args and args.test_command:
        LOGGER.info(f"Running {args.test_command}")
        base_cmd = [args.test_command] + args.test_args
        for individual in population:
            if args.input_method == "filename":
                prefix = "fandango-"
                suffix = args.filename_extension
                mode = "wb" if file_mode == "binary" else "w"
                with tempfile.NamedTemporaryFile(
                    mode=mode, prefix=prefix, suffix=suffix
                ) as fd:
                    fd.write(output(individual, args, file_mode))
                    fd.flush()
                    cmd = base_cmd + [fd.name]
                    LOGGER.debug(f"Running {cmd}")
                    subprocess.run(cmd, text=True)
            elif args.input_method == "stdin":
                cmd = base_cmd
                LOGGER.debug(f"Running {cmd} with individual as stdin")
                subprocess.run(
                    cmd, input=output(individual, args, file_mode), text=True
                )
            else:
                raise ValueError("Unsupported input method")

        output_on_stdout = False

    if output_on_stdout:
        # Default
        LOGGER.debug("Printing population on stdout")
        sep = False
        for individual in population:
            if sep:
                print(args.separator, end="")
            print(output(individual, args, file_mode), end="")
            sep = True


def report_syntax_error(
    filename: str, position: int, individual: str | bytes, *, binary: bool = False
) -> str:
    """
    Return position and error message in `individual`
    in user-friendly format.
    """
    if position >= len(individual):
        return f"{filename!r}: missing input at end of file"

    mismatch = repr(individual[position])
    if binary:
        return f"{filename!r}, position {hex(position)} ({position}): mismatched input 0x{mismatch}"

    line = 1
    column = 1
    for i in range(position):
        if individual[i] == "\n":
            line += 1
            column = 1
        else:
            column += 1
    return f"{filename!r}, line {line}, column {column}: mismatched input {mismatch}"


def validate(individual, tree, *, filename="<file>"):
    if isinstance(individual, bytes) and tree.to_bytes() != individual:
        raise ValueError(f"{filename!r}: parsed tree does not match original")
    if isinstance(individual, str) and tree.to_string() != individual:
        raise ValueError(f"{filename!r}: parsed tree does not match original")


def parse_file(fd, args, grammar, constraints, settings):
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
    tree_gen = grammar.parse_forest(
        individual, start=start_symbol, allow_incomplete=allow_incomplete
    )

    alternative_counter = 1
    passing_tree = None
    last_tree = None
    while tree := next(tree_gen, None):
        LOGGER.debug(f"Checking parse alternative #{alternative_counter}")
        last_tree = tree

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
        raise SyntaxError(
            report_syntax_error(fd.name, error_pos, individual, binary=("b" in fd.mode))
        )

    # Report error for the last tree
    for constraint in constraints:
        fitness = constraint.fitness(last_tree).fitness()
        if fitness == 0:
            raise ValueError(f"{fd.name!r}: constraint {constraint} not satisfied")


def get_file_mode(args, settings, *, grammar=None, tree=None):
    if hasattr(args, "file_mode") and args.file_mode != "auto":
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

    raise ValueError("Cannot determine file mode")


def fuzz_command(args):
    """Invoke the fuzzer"""

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise ValueError("Use '-f FILE.fan' to open a Fandango spec")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    LOGGER.debug("Starting Fandango")
    fandango = Fandango(grammar, constraints, **settings)

    LOGGER.debug("Evolving population")
    population = fandango.evolve()

    output_population(population, args, file_mode=file_mode, output_on_stdout=True)

    if args.validate:
        LOGGER.debug("Validating population")

        # Ensure that every generated file can be parsed
        # and returns the same string as the original
        temp_dir = tempfile.TemporaryDirectory(delete=False)
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
                    validate(individual, tree, filename=fd.n)

            except Exception as e:
                print_exception(e)
                errors += 1

        if errors:
            raise ValueError(f"{errors} error(s) during validation")

        # If everything went well, clean up;
        # otherwise preserve file for debugging
        shutil.rmtree(temp_dir.name)


def parse_command(args):
    """Parse given files"""
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise ValueError("Use '-f FILE.fan' to open a Fandango spec")

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
        raise ValueError(f"{errors} error(s) during parsing")


def nop_command(args):
    # Dummy command such that we can list ! and / as commands. Never executed.
    pass


def copyright_command(args):
    print("Copyright (c) 2024-2025 CISPA Helmholtz Center for Information Security.")
    print("All rights reserved.")


def version_command(args):
    version = importlib.metadata.version("fandango-fuzzer")
    if sys.stdout.isatty():
        version_line = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango{styles.color.close} {version}"
    else:
        version_line = f"Fandango {version}"
    print(version_line)


COMMANDS = {
    "set": set_command,
    "reset": reset_command,
    "fuzz": fuzz_command,
    "parse": parse_command,
    "cd": cd_command,
    "help": help_command,
    "copyright": copyright_command,
    "version": version_command,
    "exit": exit_command,
    "!": nop_command,
    "/": nop_command,
}


def get_help(cmd):
    """Return the help text for CMD"""
    parser = get_parser(in_command_line=False)
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()

    parser.exit_on_error = False
    try:
        parser.parse_args([cmd] + ["--help"])
    except SystemExit:
        pass

    sys.stdout = old_stdout
    return mystdout.getvalue()


def get_options(cmd):
    """Return all --options for CMD"""
    if cmd == "help":
        return COMMANDS.keys()

    help = get_help(cmd)
    options = []
    for option in re.findall(r"--?[a-zA-Z0-9_-]*", help):
        if option not in options:
            options.append(option)
    return options


def get_filenames(prefix="", fan_only=True):
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


def complete(text):
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


def exec_single(code, _globals={}, _locals={}):
    """Execute CODE in 'single' mode, printing out results if any"""
    block = compile(code, "<input>", mode="single")
    exec(block, _globals, _locals)


MATCHES = []


def shell_command(args):
    """Interactive mode"""

    PROMPT = "(fandango)"

    def _read_history():
        histfile = os.path.join(os.path.expanduser("~"), ".fandango_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        except Exception as e:
            LOGGER.warning(f"Could not read {histfile}: {e}")

        atexit.register(readline.write_history_file, histfile)

    def _complete(text, state):
        global MATCHES
        if state == 0:  # first trigger
            buffer = readline.get_line_buffer()[: readline.get_endidx()]
            MATCHES = complete(buffer)
        try:
            return MATCHES[state]
        except IndexError:
            return None

    if sys.stdin.isatty():
        _read_history()
        readline.set_completer_delims(" \t\n;")
        readline.set_completer(_complete)
        readline.parse_and_bind("tab: complete")

        version_command([])
        print("Type a command, 'help', 'copyright', 'version', or 'exit'.")

    last_status = 0

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
                raise ValueError(
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
                raise ValueError(
                    "Python escape (`/`) is only available in interactive mode"
                )
            continue

        command = None
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
        parser.exit_on_error = False
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
                last_status = run(command, args)
        except SystemExit:
            pass

    return last_status


def run(command, args):
    try:
        command(args)

    except SyntaxError as e:
        print_exception(e)
        return 1

    except ValueError as e:
        print_exception(e)
        return 1

    except UnsupportedOperation as e:
        print_exception(e)
        return 1

    except Exception as e:
        print_exception(e)
        return 1

    return 0


def main(*argv: str, stdout=sys.stdout, stderr=sys.stderr):
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    parser = get_parser(in_command_line=True)
    args = parser.parse_args(argv or sys.argv[1:])

    LOGGER.setLevel(logging.WARNING)  # Default

    if args.quiet and args.quiet == 1:
        LOGGER.setLevel(logging.WARNING)  # (Back to default)
    elif args.quiet and args.quiet > 1:
        LOGGER.setLevel(logging.ERROR)  # Even quieter
    elif args.verbose and args.verbose == 1:
        LOGGER.setLevel(logging.INFO)  # Give more info
    elif args.verbose and args.verbose > 1:
        LOGGER.setLevel(logging.DEBUG)  # Even more info

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


def fandango(cmd: str, stdout=sys.stdout, stderr=sys.stderr):
    # Entry point for tutorial
    try:
        main(*shlex.split(cmd, comments=True), stdout=stdout, stderr=stderr)
    except SystemExit as e:
        pass  # Do not exit


if __name__ == "__main__":
    sys.exit(main())
