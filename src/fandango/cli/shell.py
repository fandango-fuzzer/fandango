import argparse
import atexit
import os
import shlex
import sys
from typing import Any

from fandango.cli.commands import COMMANDS, help_command, run, version_command
from fandango.cli.complete import complete
from fandango.cli.parser import get_parser
from fandango.cli.utils import exec_single
from fandango.errors import FandangoError
from fandango.logger import LOGGER, print_exception

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
        return MATCHES[state] if state < len(MATCHES) else None

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
            # hack to get this working for now — posix mode doesn't work with windows paths, non-posix mode doesn't do proper escaping
            posix = "win" not in sys.platform
            command = shlex.split(command_line, comments=True, posix=posix)
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
        except (SystemExit, KeyboardInterrupt):
            pass
