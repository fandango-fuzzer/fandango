import argparse
from collections.abc import Callable
import glob
import os
from pathlib import Path
import shutil
from ansi_styles import ansiStyles as styles
import sys
import tempfile
from typing import Any

import fandango
from fandango.api import Fandango
from fandango.cli.output import open_file, output_population, output_solution
from fandango.cli.parser import get_parser
from fandango.cli.utils import (
    get_file_mode,
    make_fandango_settings,
    parse_constraints_from_args,
    parse_contents_from_args,
    parse_file,
    validate,
)
from fandango.constraints.constraint import Constraint
from fandango.constraints.soft import SoftValue
from fandango.converters.FandangoConverter import FandangoConverter
from fandango.converters.antlr.ANTLRFandangoConverter import ANTLRFandangoConverter
from fandango.converters.bt.BTFandangoConverter import (
    BitfieldOrder,
    BTFandangoConverter,
    Endianness,
)
from fandango.converters.dtd.DTDFandangoConverter import DTDFandangoConverter
from fandango.converters.fan.FandangoFandangoConverter import FandangoFandangoConverter
from fandango.errors import FandangoError, FandangoParseError
from fandango.language.grammar import FuzzingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.parse import cache_dir, clear_cache
from fandango.logger import LOGGER, print_exception


def help_command(args: argparse.Namespace, in_command_line: bool = True) -> None:
    parser = get_parser(in_command_line)

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


def exit_command(args: argparse.Namespace) -> None:
    pass


# Default Fandango file content (grammar, constraints); set with `set`
DEFAULT_FAN_CONTENT: tuple[Grammar | None, list[Constraint | SoftValue]] = (None, [])

# Additional Fandango constraints; set with `set`
DEFAULT_CONSTRAINTS: list[Constraint | SoftValue] = []

# Default Fandango algorithm settings; set with `set`
DEFAULT_SETTINGS: dict[str, Any] = {}


def set_command(args: argparse.Namespace) -> None:
    """Set global settings"""
    global DEFAULT_FAN_CONTENT
    global DEFAULT_CONSTRAINTS
    global DEFAULT_SETTINGS

    if args.fan_files:
        LOGGER.info("Parsing Fandango content")
        grammar, constraints = parse_contents_from_args(args)
        DEFAULT_FAN_CONTENT = (grammar, constraints)
        DEFAULT_CONSTRAINTS = []  # Don't leave these over
    elif args.constraints or args.maxconstraints or args.minconstraints:
        default_grammar = DEFAULT_FAN_CONTENT[0]
        if not default_grammar:
            raise FandangoError("Open a `.fan` file first ('set -f FILE.fan')")

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
        LOGGER.info("Did not receive an arg for set, printing settings")
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


def reset_command(args: argparse.Namespace) -> None:
    """Reset global settings"""
    global DEFAULT_SETTINGS
    DEFAULT_SETTINGS = {}

    global DEFAULT_CONSTRAINTS
    DEFAULT_CONSTRAINTS = []


def cd_command(args: argparse.Namespace) -> None:
    """Change current directory"""
    if args.directory:
        os.chdir(args.directory)
    else:
        os.chdir(Path.home())

    if sys.stdin.isatty():
        print(os.getcwd())


def fuzz_command(args: argparse.Namespace) -> None:
    """Invoke the fuzzer"""

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    LOGGER.debug("Starting Fandango")
    fandango = Fandango._with_parsed(
        grammar,
        constraints,
        start_symbol=args.start_symbol,
        logging_level=LOGGER.getEffectiveLevel(),
    )
    LOGGER.debug("Evolving population")

    def solutions_callback(sol, i):
        return output_solution(sol, args, i, file_mode)

    max_generations = args.max_generations
    desired_solutions = args.desired_solutions
    infinite = args.infinite

    population = fandango.fuzz(
        solution_callback=solutions_callback,
        max_generations=max_generations,
        desired_solutions=desired_solutions,
        infinite=infinite,
        mode=FuzzingMode.COMPLETE,
        **settings,
    )

    if args.validate:
        LOGGER.debug("Validating population")

        # Ensure that every generated file can be parsed
        # and returns the same string as the original
        try:
            temp_dir = tempfile.TemporaryDirectory(delete=False)  # type: ignore [call-overload] # delete is only available on some OSs
        except TypeError:
            # Python 3.11 does not know the `delete` argument
            temp_dir = tempfile.TemporaryDirectory()
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
                    validate(individual, tree, filename=fd.name)

            except Exception as e:
                print_exception(e)
                errors += 1

        if errors:
            raise FandangoError(f"{errors} error(s) during validation")

        # If everything went well, clean up;
        # otherwise preserve file for debugging
        shutil.rmtree(temp_dir.name)


def parse_command(args: argparse.Namespace) -> None:
    """Parse given files"""
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

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
        raise FandangoParseError(f"{errors} error(s) during parsing")


def talk_command(args: argparse.Namespace) -> None:
    """Interact with a program, client, or server"""
    # if not args.test_command and not args.client and not args.server:
    #     raise FandangoError(
    #         "Use '--client' or '--server' to create a client or server, "
    #         "or specify a command to interact with."
    #     )
    args.parties = []

    LOGGER.info("---------- Parsing FANDANGO content ----------")
    if args.fan_files:
        # Override given default content (if any)
        grammar, constraints = parse_contents_from_args(args)
    else:
        grammar = DEFAULT_FAN_CONTENT[0]
        constraints = DEFAULT_FAN_CONTENT[1]

    if grammar is None:
        raise FandangoError("Use '-f FILE.fan' to open a Fandango spec")

    if grammar.fuzzing_mode != FuzzingMode.IO:
        LOGGER.warning("Fandango spec does not specify interaction parties")

    # Avoid messing with default constraints
    constraints = constraints.copy()

    if DEFAULT_CONSTRAINTS:
        constraints += DEFAULT_CONSTRAINTS

    settings = make_fandango_settings(args, DEFAULT_SETTINGS)
    LOGGER.debug(f"Settings: {settings}")

    file_mode = get_file_mode(args, settings, grammar=grammar)
    LOGGER.info(f"File mode: {file_mode}")

    LOGGER.debug("Starting Fandango")

    fandango = Fandango._with_parsed(
        grammar=grammar,
        constraints=constraints,
        start_symbol=args.start_symbol,
        logging_level=LOGGER.getEffectiveLevel(),
    )
    LOGGER.debug("Evolving population")

    def solutions_callback(sol, i):
        return output_solution(sol, args, i, file_mode)

    max_generations = args.max_generations
    desired_solutions = args.desired_solutions
    infinite = args.infinite

    fandango.fuzz(
        solution_callback=solutions_callback,
        max_generations=max_generations,
        desired_solutions=desired_solutions,
        infinite=infinite,
        mode=FuzzingMode.IO,
        **settings,
    )


def convert_command(args: argparse.Namespace) -> None:
    """Convert a given language spec into Fandango .fan format"""

    output = args.output
    if output is None:
        output = sys.stdout

    for input_file in args.convert_files:
        from_format = args.from_format
        input_file_lower = input_file.lower()
        if from_format == "auto":
            if input_file_lower.endswith(".g4") or input_file_lower.endswith(".antlr"):
                from_format = "antlr"
            elif input_file_lower.endswith(".dtd"):
                from_format = "dtd"
            elif input_file_lower.endswith(".bt") or input_file_lower.endswith(".010"):
                from_format = "bt"
            elif input_file_lower.endswith(".fan"):
                from_format = "fan"
            else:
                raise FandangoError(
                    f"{input_file!r}: unknown file extension; use --from=FORMAT to specify the format"
                )

        temp_file = None
        if input_file == "-":
            # Read from stdin
            with open_file(input_file, "text", mode="r") as fd:
                contents = fd.read()
            temp_file = tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".tmp"
            )
            temp_file.write(contents)
            temp_file.flush()
            input_file = temp_file.name

        converter: FandangoConverter
        match from_format:
            case "antlr" | "g4":
                converter = ANTLRFandangoConverter(input_file)
                spec = converter.to_fan()
            case "dtd":
                converter = DTDFandangoConverter(input_file)
                spec = converter.to_fan()
            case "bt" | "010":
                if args.endianness == "little":
                    endianness = Endianness.LittleEndian
                else:
                    endianness = Endianness.BigEndian
                if args.bitfield_order == "left-to-right":
                    bitfield_order = BitfieldOrder.LeftToRight
                else:
                    bitfield_order = BitfieldOrder.RightToLeft

                converter = BTFandangoConverter(input_file)
                spec = converter.to_fan(
                    endianness=endianness, bitfield_order=bitfield_order
                )
            case "fan":
                converter = FandangoFandangoConverter(input_file, parties=args.parties)
                spec = converter.to_fan()

        print(spec, file=output, end="")
        if temp_file:
            # Remove temporary file
            temp_file.close()
            os.unlink(temp_file.name)

    if output != sys.stdout:
        output.close()


def clear_command(args: argparse.Namespace) -> None:
    CACHE_DIR = cache_dir()
    if args.dry_run:
        print(f"Would clear {CACHE_DIR}", file=sys.stderr)
    elif os.path.exists(CACHE_DIR):
        print(f"Clearing {CACHE_DIR}...", file=sys.stderr, end="")
        clear_cache()
        print("done", file=sys.stderr)


def nop_command(args: argparse.Namespace) -> None:
    # Dummy command such that we can list ! and / as commands. Never executed.
    pass


def copyright_command(args: argparse.Namespace) -> None:
    print("Copyright (c) 2024-2025 CISPA Helmholtz Center for Information Security.")
    print("All rights reserved.")


def version_command(args: argparse.Namespace) -> None:
    if sys.stdout.isatty():
        version_line = f"💃 {styles.color.ansi256(styles.rgbToAnsi256(128, 0, 0))}Fandango{styles.color.close} {fandango.version()}"
    else:
        version_line = f"Fandango {fandango.version()}"
    print(version_line)


COMMANDS: dict[str, Callable[[argparse.Namespace], None]] = {
    "set": set_command,
    "reset": reset_command,
    "fuzz": fuzz_command,
    "parse": parse_command,
    "talk": talk_command,
    "convert": convert_command,
    "clear-cache": clear_command,
    "cd": cd_command,
    "help": help_command,
    "copyright": copyright_command,
    "version": version_command,
    "exit": exit_command,
    "!": nop_command,
    "/": nop_command,
}


def run(command: Callable[[argparse.Namespace], None], args: argparse.Namespace) -> int:
    try:
        command(args)
    except Exception as e:
        print_exception(e)
        return 1

    return 0
