import argparse
import importlib.metadata
import logging
import os
import sys
import textwrap
import subprocess
import tempfile

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



def get_parser():

    # Main parser
    main_parser = argparse.ArgumentParser(
        prog="fandango",
        description="The access point to the Fandango framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
                               Use `%(prog)s help` to get a list of commands.
                               Use `%(prog)s help COMMAND` to learn more about COMMAND.""")
    )

    main_parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("fandango"),
        help="show version number",
    )

    verbosity_option = main_parser.add_mutually_exclusive_group()
    verbosity_option.add_argument(
        "--verbose", "-v",
        dest="verbose",
        action="count",
        help="increase verbosity. Can be given multiple times (-vv)",
    )
    verbosity_option.add_argument(
        "--quiet", "-q",
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
        required=True,
    )

    # Shared Settings
    settings_parser = argparse.ArgumentParser(add_help=False)
    settings_group = settings_parser.add_argument_group("algorithm settings")

    settings_group.add_argument('-N', '--max-generations', type=int,
                                 help="the maximum number of generations to run the algorithm", default=500)
    settings_group.add_argument('--population-size', type=int,
                                 help="the size of the population", default=100)
    settings_group.add_argument('--elitism-rate', type=float,
                                 help="the rate of individuals preserved in the next generation", default=0.1)
    settings_group.add_argument('--crossover-rate', type=float,
                                 help="the rate of individuals that will undergo crossover", default=0.8)
    settings_group.add_argument('--mutation-rate', type=float,
                                 help="the rate of individuals that will undergo mutation", default=0.1)
    settings_group.add_argument("-n", "--num-outputs", type=int,
                                 help="the number of outputs to produce (default: 100)", default=100)

    # Shared file options
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-f", "--fandango-file",
        type=argparse.FileType('r'),
        dest="fan_files",
        metavar="FAN_FILE",
        default=None,
        action="append",
        help="Fandango file (.fan, .py) to be processed. Can be given multiple times.",
    )
    file_parser.add_argument(
        "-c", "--constraint",
        type=int,
        dest="constraints",
        metavar="CONSTRAINTS",
        default=None,
        action="append",
        help="define an additional constraint CONSTRAINT. Can be given multiple times.",
    )
    file_parser.add_argument(
        "-s", "--separator",
        type=str,
        default='\n',
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
        "-o", "--output",
        type=argparse.FileType('w'),
        dest="output",
        default=None,
        help="write output to OUTPUT (default: stdout)",
    )
    fuzz_parser.add_argument(
        "-d", "--directory",
        type=str,
        dest="directory",
        default=None,
        help="create individual output files in DIRECTORY",
    )

    command_group = fuzz_parser.add_argument_group("command invocation settings")

    command_group.add_argument(
        "--input-method",
        choices=['stdin', 'filename'],
        default='filename',
        help="When invoking COMMAND, choose whether Fandango input will be passed as standard input (`stdin`) or as last argument on the command line (`filename`) (default)",
    )
    command_group.add_argument(
        "--filename-format",
        type=str,
        default='fandango-{:04d}.txt',
        help="Format of generated file names (default: 'fandango-{:04d}.txt')",
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


    # Interactive
    interactive_parser = commands.add_parser(
        INTERACTIVE,
        help="open the interactive command line interface"
    )
    interactive_parser.add_argument(
        "-f", "--fan",
        type=str,
        dest="fan",
        default=None,
        help="the fan file to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-g", "--grammar",
        type=str,
        dest="grammar",
        default=None,
        help="the grammar to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-c", "--constraints",
        type=str,
        dest="constraints",
        default=None,
        help="the constraints to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-p", "--python",
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

def interactive(args):
    try:
        interactive_ = Interactive(
            args.fan, args.grammar, args.constraints, args.python
        )
    except Exception as e:
        # This should catch all kinds of parsing errors
        LOGGER.critical(f"Error during initialization: {type(e)}")
        sys.exit(1)

    interactive_.run()

def help(args):
    parser = get_parser()
    for cmd in args.help_command:
        # Alas, this exits after the first command
        parser.parse_args([cmd] + ["--help"])
    else:
        parser.print_help()

def merged_fan_contents(args) -> str:
    """Merge all given files and constraints into one; return content"""
    fan_contents = ""
    if args.fan_files:
        for file in args.fan_files:
            fan_contents += file.read() + '\n'
    if args.constraints:
        for constraint in args.constraints:
            fan_contents += '\n' + constraint + ';\n'
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
    constraint_processor = ConstraintProcessor(grammar,
        local_variables=local_vars, global_variables=global_vars,
        lazy=lazy,
    )
    constraints = constraint_processor.get_constraints(splitter.constraints)

    LOGGER.debug("Parsing complete")
    return grammar, constraints

def parse_fan_contents(args):
    """Parse .fan content as given in args"""
    LOGGER.debug("Reading .fan files")
    fan_contents = merged_fan_contents(args)
    grammar, constraints = extract_grammar_and_constraints(fan_contents)
    return grammar, constraints

def fuzz(args):
    LOGGER.info("---------- Parsing FANDANGO content ----------")
    grammar, constraints = parse_fan_contents(args)

    LOGGER.debug("Starting Fandango")
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=max(args.population_size, args.num_outputs),
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        max_generations=args.max_generations,
        elitism_rate=args.elitism_rate,
    )

    LOGGER.debug("Evolving population")
    population = fandango.evolve()

    LOGGER.debug("Reducing population")
    population = population[:args.num_outputs]

    output_on_stdout = True

    if args.directory:
        LOGGER.debug(f"Storing population in {args.directory} directory")
        try:
            os.mkdir(args.directory)
        except FileExistsError as e:
            pass

        counter = 1
        for individual in population:
            basename = "fandango-{:04d}.txt".format(counter)  # format should be configurable
            filename = os.path.join(args.directory, basename)
            with open(filename, 'w') as fd:
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
            if args.input_method == 'filename':
                with tempfile.NamedTemporaryFile(mode='w') as fd:
                    fd.write(str(individual))
                    fd.flush()
                    cmd = base_cmd + [fd.name]
                    LOGGER.debug(f"Running {cmd}")
                    subprocess.run(cmd, text=True)
            elif args.input_method == 'stdin':
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




def main(*args: str, stdout=sys.stdout, stderr=sys.stderr):
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    parser = get_parser()
    args = parser.parse_args(args or sys.argv[1:])

    LOGGER.setLevel(logging.WARNING)  # Default
    if args.quiet:
        LOGGER.setLevel(logging.ERROR)  # Suppress warnings
    elif args.verbose and args.verbose == 1:
            LOGGER.setLevel(logging.INFO)  # Give more info
    elif args.verbose and args.verbose > 1:
            LOGGER.setLevel(logging.DEBUG)  # Even more info

    if args.command == INTERACTIVE:
        interactive(args)
    elif args.command == FUZZ:
        fuzz(args)
    elif args.command == HELP:
        help(args)
    else:
        # This should not be reachable, but just in case
        parser.print_usage()

if __name__ == "__main__":
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)
    else:
        main()
