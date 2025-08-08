import logging
import os
import sys
from typing import Any, IO

from fandango import Fandango
from fandango.cli.commands import COMMANDS, run
from fandango.cli.shell import shell_command
from fandango.cli.parser import get_parser
from fandango.logger import LOGGER


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
    Fandango.parser = args.parser

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
