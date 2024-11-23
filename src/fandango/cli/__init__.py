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
    arguments = argparse.ArgumentParser(
        prog="fandango",
        description="The access point to the Fandango framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
                               Use `%(prog)s help` to get a list of commands.
                               Use `%(prog)s help COMMAND` to learn more about COMMAND.""")
    )

    arguments.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + importlib.metadata.version("fandango"),
        help="show version number",
    )

    arguments.add_argument(
        "-v", "--verbose",
        dest="verbose",
        action="store_true",
        help="enable verbose output",
    )

    # The subparsers
    commands = arguments.add_subparsers(
        title="commands",
        # description="Valid commands",
        help="the command to execute",
        dest="command",
        required=True,
    )

    # Commands

    # Fuzz
    fuzz_parser = commands.add_parser(
        FUZZ,
        help="produce outputs from .fan files"
    )
    fuzz_parser.add_argument(
        "-n", "--num-outputs",
        type=int,
        dest="num_outputs",
        default=1,
        help="the number of outputs to produce (default: 1)",
    )
    fuzz_parser.add_argument(
        "-o", "--output",
        type=int,
        dest="output",
        default=None,
        help="write output to OUTPUT (default: stdout)",
    )
    fuzz_parser.add_argument(
        "-c", "--constraint",
        type=int,
        dest="constraint",
        default=None,
        action="append",
        help="define an additional constraint CONSTRAINT",
    )
    fuzz_parser.add_argument(
        "-d", "--directory",
        type=int,
        dest="directory",
        default=None,
        help="create individual output files in DIRECTORY",
    )
    fuzz_parser.add_argument(
        "fan-file",
        type=argparse.FileType('r'),
        nargs="+",
        default=None,
        help="Fandango file (.fan, .py) to be processed",
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

    return arguments

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

def help(parser, args):
    for cmd in args.help_command:
        parser.parse_args([cmd] + ["--help"])
    else:
        parser.print_help()

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
    elif args.command == HELP:
        help(parser, args)

if __name__ == "__main__":
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)
    else:
        main()
