import argparse
import importlib.metadata
import logging
import os
import sys

from fandango.constants import INTERACTIVE
from fandango.logger import LOGGER


def get_parser():
    arguments = argparse.ArgumentParser(
        description="The access point to the fandango framework"
    )

    arguments.add_argument(
        "--version",
        action="version",
        version=importlib.metadata.version("tests4py"),
        help="Show version number",
    )

    arguments.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="enable verbose output",
    )

    # The subparsers
    commands = arguments.add_subparsers(
        help="The command of the fandango framework to execute",
        dest="command",
        required=True,
    )

    interactive_parser = commands.add_parser(
        INTERACTIVE, help="Open the interactive command line interface"
    )

    # Interactive
    interactive_parser.add_argument(
        "-f",
        "--fan",
        type=str,
        dest="fan",
        default=None,
        help="The fan file to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-g" "--grammar",
        type=str,
        dest="grammar",
        default=None,
        help="The grammar to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-c",
        "--constraints",
        type=str,
        dest="constraints",
        default=None,
        help="The constraints to use for the interactive mode",
    )
    interactive_parser.add_argument(
        "-p",
        "--python",
        type=str,
        dest="python",
        default=None,
        help="The python code to use in the interactive mode",
    )
    return arguments


def main(*args: str, stdout=sys.stdout, stderr=sys.stderr):
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)

    if stdout is not None:
        sys.stdout = stdout
    if stderr is not None:
        sys.stderr = stderr

    args = get_parser().parse_args(args or sys.argv[1:])

    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)

    if args.command == INTERACTIVE:
        interactive(args.fan, args.grammar, args.constraints, args.python)


if __name__ == "__main__":
    if "-O" in sys.argv:
        sys.argv.remove("-O")
        os.execl(sys.executable, sys.executable, "-O", *sys.argv)
    else:
        main()
