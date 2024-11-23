import argparse
import importlib.metadata
import logging
import os
import sys
import textwrap

from fandango.cli.interactive import Interactive
from fandango.constants import INTERACTIVE, FUZZ, HELP
from fandango.logger import LOGGER


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

    main_parser.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose output",
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
        dest="fan_file",
        default=None,
        action="append",
        help="Fandango file (.fan, .py) to be processed. Can be given multiple times.",
    )
    file_parser.add_argument(
        "-c", "--constraint",
        type=int,
        dest="constraint",
        default=None,
        action="append",
        help="define an additional constraint CONSTRAINT. Can be given multiple times.",
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
        type=int,
        dest="output",
        default=None,
        help="write output to OUTPUT (default: stdout)",
    )
    fuzz_parser.add_argument(
        "-d", "--directory",
        type=int,
        dest="directory",
        default=None,
        help="create individual output files in DIRECTORY",
    )

    test_group = fuzz_parser.add_argument_group("command invocation settings")

    input_option = test_group.add_mutually_exclusive_group()
    input_option.add_argument(
        "--to-stdin",
        action="store_true",
        help="Fandango input will be passed as standard input",
    )
    input_option.add_argument(
        "--to-arg",
        action="store_true",
        help="Fandango input file will be passed as last command-line argument",
    )

    command_group = test_group.add_argument_group()
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
        nargs="*",
        help="Command arguments",
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
        print(f"Error during initialization: {type(e)}")
        sys.exit(1)

    try:
        interactive_.run()
    except Exception as e:
        print(f"Error during execution: {type(e)}")
        sys.exit(1)

def help(args):
    parser = get_parser()
    for cmd in args.help_command:
        # Alas, this exits after the first command
        parser.parse_args([cmd] + ["--help"])
    else:
        parser.print_help()

def fuzz(args):
    print(args, sys.argv)

def test(args):
    print(args, sys.argv)

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

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    if args.command == INTERACTIVE:
        interactive(args)
    elif args.command == FUZZ:
        fuzz(args)
    elif args.command == TEST:
        test(args)
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
