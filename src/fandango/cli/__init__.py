import argparse
import importlib.metadata
import logging
import os
import sys
import textwrap
import subprocess
import tempfile
import readline
import shlex
import atexit
from os import environ


from fandango.cli.interactive import Interactive
from fandango.constants import INTERACTIVE, FUZZ, HELP
from fandango.logger import LOGGER

import ast

from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream
from antlr4.error.ErrorStrategy import BailErrorStrategy

from fandango.constraints import predicates
from fandango.constraints.fitness import GeneticBase
from fandango.evolution.algorithm import Fandango
from fandango.language.convert import (
    FandangoSplitter,
    GrammarProcessor,
    PythonProcessor,
    ConstraintProcessor,
)
from fandango.language.grammar import Grammar
from fandango.language.parser.FandangoLexer import FandangoLexer
from fandango.language.parser.FandangoParser import FandangoParser
from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


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
            Use `help COMMAND` to learn more about COMMAND."""

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
            version="%(prog)s " + importlib.metadata.version("fandango"),
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
            action="store_true",
            help="suppress warnings",
        )

    # The subparsers
    commands = main_parser.add_subparsers(
        title="commands",
        # description="Valid commands",
        help="the command to execute",
        dest="command",
        # required=True,
    )

    # Shared Settings
    settings_parser = argparse.ArgumentParser(add_help=False)
    settings_group = settings_parser.add_argument_group("algorithm settings")

    settings_group.add_argument(
        "-N",
        "--max-generations",
        type=int,
        help="the maximum number of generations to run the algorithm",
        default=None,
    )
    settings_group.add_argument(
        "--population-size", type=int, help="the size of the population", default=None
    )
    settings_group.add_argument(
        "--elitism-rate",
        type=float,
        help="the rate of individuals preserved in the next generation",
        default=None,
    )
    settings_group.add_argument(
        "--crossover-rate",
        type=float,
        help="the rate of individuals that will undergo crossover",
        default=None,
    )
    settings_group.add_argument(
        "--mutation-rate",
        type=float,
        help="the rate of individuals that will undergo mutation",
        default=None,
    )
    settings_group.add_argument(
        "-n",
        "--num-outputs",
        type=int,
        help="the number of outputs to produce (default: 100)",
        default=None,
    )
    settings_group.add_argument(
        "-S",
        "--start-symbol",
        type=str,
        help="the grammar start symbol (default: `start`)",
        default=None,
    )
    settings_group.add_argument(
        "--warnings-are-errors",
        dest="warnings_are_errors",
        action="store_true",
        help="treat warnings as errors",
        default=None,
    )
    settings_group.add_argument(
        '--best-effort',
        dest="best_effort",
        action="store_true",
        help="produce a 'best effort' population (may not satisfy all constraints)",
        default=None,
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
        help="Fandango file (.fan, .py) to be processed. Can be given multiple times.",
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
        "-s",
        "--separator",
        type=str,
        default="\n",
        help="output SEPARATOR between individual inputs. (default: newline)",
    )

    # Commands

    # Fuzz
    fuzz_parser = commands.add_parser(
        FUZZ,
        help="produce outputs from .fan files and test programs",
        parents=[file_parser, settings_parser],
    )
    fuzz_parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        dest="output",
        default=None,
        help="write output to OUTPUT (default: stdout)",
    )
    fuzz_parser.add_argument(
        "-d",
        "--directory",
        type=str,
        dest="directory",
        default=None,
        help="create individual output files in DIRECTORY",
    )

    command_group = fuzz_parser.add_argument_group("command invocation settings")

    command_group.add_argument(
        "--input-method",
        choices=["stdin", "filename"],
        default="filename",
        help="When invoking COMMAND, choose whether Fandango input will be passed as standard input (`stdin`) or as last argument on the command line (`filename`) (default)",
    )
    command_group.add_argument(
        "-x", "--filename-extension",
        type=str,
        default=".txt",
        help="Extension of generated file names (default: '.txt')",
    )

    command_group.add_argument(
        "test_command",
        metavar="command",
        type=str,
        nargs="?",
        help="Command to be invoked with a Fandango input",
    )
    command_group.add_argument(
        "test_args",
        metavar="args",
        type=str,
        nargs=argparse.REMAINDER,
        help="The arguments of the command",
    )

    if not in_command_line:
        # Set
        set_parser = commands.add_parser(
            "set",
            help="set defaults",
            parents=[file_parser, settings_parser],
        )

    if not in_command_line:
        # Reset
        set_parser = commands.add_parser(
            "reset",
            help="reset defaults",
        )

    if in_command_line:
        # Shell
        shell_parser = commands.add_parser(
            "shell",
            help="run an interactive shell (default)",
        )

    if in_command_line:
        # Interactive
        interactive_parser = commands.add_parser(
            INTERACTIVE,
            help="open the interactive command line interface (deprecated)",
        )
        interactive_parser.add_argument(
            "-f",
            "--fan",
            type=str,
            dest="fan",
            default=None,
            help="the fan file to use for the interactive mode",
        )
        interactive_parser.add_argument(
            "-g",
            "--grammar",
            type=str,
            dest="grammar",
            default=None,
            help="the grammar to use for the interactive mode",
        )
        interactive_parser.add_argument(
            "-c",
            "--constraints",
            type=str,
            dest="constraints",
            default=None,
            help="the constraints to use for the interactive mode",
        )
        interactive_parser.add_argument(
            "-p",
            "--python",
            type=str,
            dest="python",
            default=None,
            help="the Python code to use in the interactive mode",
        )

    # Help
    help_parser = commands.add_parser(
        HELP,
        help="show this help and exit",
    )
    help_parser.add_argument(
        "help_command",
        type=str,
        nargs="*",
        default=None,
        help="command to get help on",
    )

    return main_parser


def interactive_command(args):
    LOGGER.warn("Deprecated. Use the 'shell' command instead.")
    try:
        interactive_ = Interactive(
            args.fan, args.grammar, args.constraints, args.python
        )
    except Exception as e:
        # This should catch all kinds of parsing errors
        LOGGER.critical(f"Error during initialization: {type(e)}")
        sys.exit(1)

    interactive_.run()


def help_command(args, **kwargs):
    parser = get_parser(**kwargs)
    parser.exit_on_error = False

    for cmd in args.help_command:
        parser.parse_args([cmd] + ["--help"])
    else:
        parser.print_help()


def merged_fan_contents(args) -> str:
    """Merge all given files and constraints into one; return content"""
    fan_contents = ""
    if args.fan_files:
        for file in args.fan_files:
            fan_contents += file.read() + "\n"
    if args.constraints:
        for constraint in args.constraints:
            fan_contents += "\n" + constraint + ";\n"
    return fan_contents


def extract_grammar_and_constraints(fan_contents: str, lazy: bool = False):
    """Extract grammar and constraints from the given content"""
    # TODO: This should go into a separate module (parser.py maybe?), not here -- AZ

    LOGGER.debug("Parsing .fan content")
    input_stream = InputStream(fan_contents)
    lexer = FandangoLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = FandangoParser(token_stream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.fandango()

    LOGGER.debug("Extracting code")
    splitter = FandangoSplitter()
    splitter.visit(tree)
    global_vars: dict = {}
    local_vars = predicates.__dict__
    python_processor = PythonProcessor()
    code_tree = python_processor.get_code(splitter.python_code)
    code_text = ast.unparse(code_tree)

    LOGGER.debug("Running code")
    exec(code_text, global_vars, local_vars)

    LOGGER.debug("Extracting grammar")
    grammar_processor = GrammarProcessor(
        local_variables=local_vars, global_variables=global_vars
    )
    grammar: Grammar = grammar_processor.get_grammar(splitter.productions)

    LOGGER.debug("Extracting constraints")
    constraint_processor = ConstraintProcessor(
        grammar,
        local_variables=local_vars,
        global_variables=global_vars,
        lazy=lazy,
    )
    constraints = constraint_processor.get_constraints(splitter.constraints)

    LOGGER.debug("Parsing complete")
    return grammar, constraints


def parse_fan_contents(args):
    """Parse .fan content as given in args"""
    LOGGER.debug("Reading .fan files")
    fan_contents = merged_fan_contents(args)
    if not fan_contents:
        return None, None

    grammar, constraints = extract_grammar_and_constraints(fan_contents)
    return grammar, constraints


def make_fandango_settings(args, initial_settings={}):
    """Create keyword settings for Fandango() constructor"""
    settings = initial_settings.copy()
    if args.population_size is not None:
        settings['population_size'] = args.population_size
    if args.num_outputs is not None:
        settings['desired_solutions'] = args.num_outputs
    if args.mutation_rate is not None:
        settings['mutation_rate'] = args.mutation_rate
    if args.crossover_rate is not None:
        settings['crossover_rate'] = args.crossover_rate
    if args.max_generations is not None:
        settings['max_generations'] = args.max_generations
    if args.elitism_rate is not None:
        settings['elitism_rate'] = args.elitism_rate
    if args.warnings_are_errors is not None:
        settings['warnings_are_errors'] = args.warnings_are_errors
    if args.best_effort is not None:
        settings['best_effort'] = args.best_effort
    if args.start_symbol is not None:
        if args.start_symbol.startswith("<"):
            start_symbol = args.start_symbol
        else:
            start_symbol = f"<{args.start_symbol}>"
        settings['start_symbol'] = start_symbol

    return settings

# Default Fandango file contents; set with `set`
DEFAULT_FAN = (None, None)

# Additional Fandango constraints; set with `set`
DEFAULT_CONSTRAINTS = []

# Default Fandango algorithm settings; set with `set`
DEFAULT_SETTINGS = {}

def set_command(args):
    """Set global settings"""
    LOGGER.info("---------- Parsing FANDANGO content ----------")

    if args.fan_files:
        global DEFAULT_FAN
        fan_contents = ""
        for file in args.fan_files:
            fan_contents += file.read() + "\n"
        grammar, constraints = extract_grammar_and_constraints(fan_contents)
        DEFAULT_FAN = (grammar, constraints)

    if args.constraints:
        global DEFAULT_CONSTRAINTS
        fan_contents = ""
        for constraint in args.constraints:
            fan_contents += "\n" + constraint + ";\n"
        _, constraints = extract_grammar_and_constraints(fan_contents)
        DEFAULT_CONSTRAINTS = constraints

    global DEFAULT_SETTINGS
    settings = make_fandango_settings(args)
    for setting in settings:
        DEFAULT_SETTINGS[setting] = settings[setting]

def reset_command(args):
    """Reset global settings"""
    global DEFAULT_SETTINGS
    DEFAULT_SETTINGS = {}

    global DEFAULT_CONSTRAINTS
    DEFAULT_CONSTRAINTS = []

def fuzz_command(args):
    """Invoke the fuzzer"""

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_fan_contents(args)
    else:
        grammar, constraints = DEFAULT_FAN

    if grammar is None:
        print("fuzz: Use -f to specify a .fan file", file=sys.stderr)
        return

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    if args.constraints:
        # Add given constraints
        fan_contents = ""
        for constraint in args.constraints:
            fan_contents += "\n" + constraint + ";\n"
        _, extra_constraints = extract_grammar_and_constraints(fan_contents)
        constraints += extra_constraints

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    LOGGER.debug("Starting Fandango")
    fandango = Fandango(grammar, constraints, **settings)

    LOGGER.debug("Evolving population")
    population = fandango.evolve()

    output_on_stdout = True

    if args.directory:
        LOGGER.debug(f"Storing population in {args.directory} directory")
        try:
            os.mkdir(args.directory)
        except FileExistsError as e:
            pass

        counter = 1
        for individual in population:
            basename = f"fandango-{counter:04d}{args.filename_extension}"
            filename = os.path.join(args.directory, basename)
            with open(filename, "w") as fd:
                fd.write(str(individual))
            counter += 1

        output_on_stdout = False

    if args.output:
        LOGGER.debug(f"Storing population in file")
        for individual in population:
            args.output.write(str(individual))
            args.output.write(args.separator)

        args.output.close()
        output_on_stdout = False

    if args.test_command:
        print(args, sys.argv)
        LOGGER.info(f"Running {args.test_command}")
        base_cmd = [args.test_command] + args.test_args
        for individual in population:
            if args.input_method == "filename":
                prefix = 'fandango-'
                suffix = args.filename_extension
                with tempfile.NamedTemporaryFile(mode="w",
                                                 prefix=prefix,
                                                 suffix=suffix) as fd:
                    fd.write(str(individual))
                    fd.flush()
                    cmd = base_cmd + [fd.name]
                    LOGGER.debug(f"Running {cmd}")
                    subprocess.run(cmd, text=True)
            elif args.input_method == "stdin":
                cmd = base_cmd
                LOGGER.debug(f"Running {cmd} with individual as stdin")
                subprocess.run(cmd, input=str(individual), text=True)
            else:
                raise ValueError("Unsupported input method")

        output_on_stdout = False

    if output_on_stdout:
        # Default
        LOGGER.debug(f"Printing population on stdout")
        for individual in population:
            print(individual, end=args.separator)

COMMANDS = {
    "set": set_command,
    "reset": reset_command,
    "fuzz": fuzz_command,
    "interactive": interactive_command,
    "help": help_command,
}

def shell_command(args):
    """(New) interactive mode"""
    def _read_history():
        histfile = os.path.join(os.path.expanduser("~"), ".fandango_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        atexit.register(readline.write_history_file, histfile)

    def _complete(text, state):
        # print("Completing", repr(text), repr(state), COMMANDS)
        if state == 0:  # first trigger
            if text:
                matches = [
                    s + " " for s in COMMANDS if s and s.startswith(text)
                ]
            else:
                matches = COMMANDS

        try:
            return matches[state]
        except IndexError:
            return None

    def _display_matches(self, substitution, matches, longest_match_length):
        line_buffer = readline.get_line_buffer()
        columns = environ.get("COLUMNS", 80)

        print()

        tpl = "{:<" + str(int(max(map(len, matches)) * 1.2)) + "}"

        buffer = ""
        for match in matches:
            match = tpl.format(match[len(substitution) :])
            if len(buffer + match) > columns:
                print(buffer)
                buffer = ""
            buffer += match

        if buffer:
            print(buffer)

        print("> ", end="")
        print(line_buffer, end="")
        sys.stdout.flush()

    _read_history()
    readline.set_completer_delims(" \t\n;")
    readline.set_completer(_complete)
    readline.parse_and_bind("tab: complete")  # Linux
    readline.parse_and_bind("bind '\t' rl_complete")  # Mac
    readline.set_completion_display_matches_hook(_display_matches)

    print("Fandango", importlib.metadata.version("fandango"))
    print("Enter a command, 'help', or 'exit'")

    while True:
        try:
            command_line = input("(fandango) ").lstrip()
        except KeyboardInterrupt:
            print("\nEnter a command, 'help', or 'exit'")
            continue
        except EOFError:
            break

        command = shlex.split(command_line, comments=True)
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

        try:
            if args.command == "help":
                help_command(args, in_command_line=False)
            else:
                command = COMMANDS[args.command]
                command(args)
        except SystemExit:
            pass


def main(*args: str, stdout=sys.stdout, stderr=sys.stderr):
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    parser = get_parser(in_command_line=True)
    args = parser.parse_args(args or sys.argv[1:])

    LOGGER.setLevel(logging.WARNING)  # Default
    if args.quiet:
        LOGGER.setLevel(logging.ERROR)  # Suppress warnings
    elif args.verbose and args.verbose == 1:
        LOGGER.setLevel(logging.INFO)  # Give more info
    elif args.verbose and args.verbose > 1:
        LOGGER.setLevel(logging.DEBUG)  # Even more info

    if args.command in COMMANDS:
        command = COMMANDS[args.command]
        command(args)
    elif args.command is None or args.command == 'shell':
        shell_command(args)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
