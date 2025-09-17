import argparse
import os
import sys
import textwrap

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
    main_parser = _get_main_parser(in_command_line)

    commands = main_parser.add_subparsers(
        title="commands",
        help="The command to execute.",
        dest="command",
    )

    algorithm_parser = _get_algorithm_parser()
    settings_parser = _get_settings_parser(in_command_line)
    file_parser = _get_file_parser()
    parties_parser = _get_parties_parser()

    _populate_fuzz_parser(
        parser=commands.add_parser(
            "fuzz",
            help="Produce outputs from .fan files and test programs.",
            parents=[file_parser, algorithm_parser, settings_parser, parties_parser],
        )
    )

    _populate_parse_parser(
        parser=commands.add_parser(
            "parse",
            help="Parse input file(s) according to .fan spec.",
            parents=[file_parser, settings_parser, parties_parser],
        )
    )

    _populate_talk_parser(
        parser=commands.add_parser(
            "talk",
            help="Interact with programs, clients, and servers.",
            parents=[file_parser, algorithm_parser, settings_parser],
        )
    )

    _populate_convert_parser(
        parser=commands.add_parser(
            "convert",
            help="Convert given external spec to .fan format.",
            parents=[parties_parser],
        )
    )

    _populate_clear_cache_parser(
        parser=commands.add_parser(
            "clear-cache", help="Clear the Fandango parsing cache."
        )
    )

    if in_command_line:
        commands.add_parser("shell", help="Run an interactive shell (default).")
    else:
        _populate_shell_parser_not_in_command_line(
            parser=commands.add_parser("!", help="Execute shell command."),
        )

        commands.add_parser(
            "set",
            help="Set or print default arguments.",
            parents=[file_parser, algorithm_parser, settings_parser, parties_parser],
        )
        commands.add_parser("reset", help="Reset defaults.")

        _populate_cd_parser(parser=commands.add_parser("cd", help="Change directory."))

        commands.add_parser("exit", help="Exit Fandango.")

        _populate_python_parser(
            parser=commands.add_parser("/", help="Execute Python command.")
        )

    _populate_help_parser(
        parser=commands.add_parser("help", help="Show this help and exit.")
    )

    commands.add_parser("copyright", help="Show copyright.")

    commands.add_parser("version", help="Show version.")

    return main_parser


def _get_main_parser(in_command_line: bool) -> argparse.ArgumentParser:
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

    return main_parser


def _get_algorithm_parser() -> argparse.ArgumentParser:
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
        help="Random seed to use for the algorithm. You probably also want to specify 'PYTHONHASHSEED=<some-value>' to achieve full reproducability.",
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
    algorithm_group.add_argument(
        "--progress-bar",
        choices=["on", "off", "auto"],
        default="auto",
        help="Whether to show the progress bar. 'auto' (default) shows the progress bar only if stderr is a terminal.",
    )

    return algorithm_parser


def _get_settings_parser(in_command_line: bool = True) -> argparse.ArgumentParser:
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

    return settings_parser


def _get_file_parser() -> argparse.ArgumentParser:
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
    return file_parser


def _get_parties_parser() -> argparse.ArgumentParser:
    parties_parser = argparse.ArgumentParser(add_help=False)
    parties_group = parties_parser.add_argument_group("Party settings")
    parties_group.add_argument(
        "--party",
        action="append",
        dest="parties",
        metavar="PARTY",
        help="Only consider the PARTY part of the interaction in the .fan file.",
    )

    return parties_parser


def _populate_fuzz_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: stdout).",
    )

    command_group = parser.add_argument_group("command invocation settings")

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


def _populate_parse_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "input_files",
        metavar="files",
        type=str,
        nargs="*",
        help="Files to be parsed. Use '-' for stdin.",
    )
    parser.add_argument(
        "--prefix",
        action="store_true",
        default=False,
        help="Parse a prefix only.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: none). Use '-' for stdout.",
    )


def _populate_talk_parser(parser: argparse.ArgumentParser) -> None:
    host_pattern = (
        "PORT on HOST (default: 127.0.0.1;"
        + " use '[...]' for IPv6 addresses)"
        + " using PROTOCOL ('tcp' (default)/'udp')."
    )
    parser.add_argument(
        "--client",
        metavar="[NAME=][PROTOCOL:][HOST:]PORT",
        type=str,
        help="Act as a client NAME (default: 'Client') connecting to " + host_pattern,
    )
    parser.add_argument(
        "--server",
        metavar="[NAME=][PROTOCOL:][HOST:]PORT",
        type=str,
        help="Act as a server NAME (default: 'Server') running at " + host_pattern,
    )
    parser.add_argument(
        "test_command",
        metavar="command",
        type=str,
        nargs="?",
        help="Optional command to be interacted with.",
    )
    parser.add_argument(
        "test_args",
        metavar="args",
        type=str,
        nargs=argparse.REMAINDER,
        help="The arguments of the command.",
    )


def _populate_convert_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--from",
        dest="from_format",
        choices=["antlr", "g4", "dtd", "010", "bt", "fan", "auto"],
        default="auto",
        help="Format of the external spec file: 'antlr'/'g4' (ANTLR), 'dtd' (XML DTD), '010'/'bt' (010 Editor Binary Template), 'fan' (Fandango spec), or 'auto' (default: try to guess from file extension).",
    )
    parser.add_argument(
        "--endianness", choices=["little", "big"], help="Set endianness for .bt files."
    )
    parser.add_argument(
        "--bitfield-order",
        choices=["left-to-right", "right-to-left"],
        help="Set bitfield order for .bt files.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        dest="output",
        default=None,
        help="Write output to OUTPUT (default: stdout).",
    )
    parser.add_argument(
        "convert_files",
        type=str,
        metavar="FILENAME",
        default=None,
        nargs="+",
        help="External spec file to be converted. Use '-' for stdin.",
    )


def _populate_clear_cache_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        dest="dry_run",
        default=False,
        help="Just output the action to be performed; do not actually clear the cache.",
    )


def _populate_cd_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        default=None,
        help="The directory to change into.",
    )


def _populate_shell_parser_not_in_command_line(parser: argparse.ArgumentParser) -> None:
    # Shell escape
    # Not processed by argparse,
    # but we have it here so that it is listed in help
    parser.add_argument(
        dest="shell_command",
        metavar="command",
        nargs=argparse.REMAINDER,
        default=None,
        help="The shell command to execute.",
    )


def _populate_python_parser(parser: argparse.ArgumentParser) -> None:
    # Python escape
    # Not processed by argparse,
    # but we have it here so that it is listed in help
    parser.add_argument(
        dest="python_command",
        metavar="command",
        nargs=argparse.REMAINDER,
        default=None,
        help="The Python command to execute.",
    )


def _populate_help_parser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "help_command",
        type=str,
        metavar="command",
        nargs="*",
        default=None,
        help="Command to get help on.",
    )
