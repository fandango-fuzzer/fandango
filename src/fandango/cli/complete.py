import glob
from io import StringIO
import os
import re
import sys

from fandango.cli.commands import COMMANDS
from fandango.cli.parser import get_parser
from fandango.logger import LOGGER


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
