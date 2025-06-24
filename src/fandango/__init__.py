#!/usr/bin/env python3

import importlib.metadata
import logging
import sys

from fandango.api import Fandango
from fandango.errors import (
    FandangoError,
    FandangoParseError,
    FandangoSyntaxError,
    FandangoValueError,
)
import fandango.language.tree
import fandango.language.parse

__all__ = [
    "FandangoError",
    "FandangoParseError",
    "FandangoSyntaxError",
    "FandangoValueError",
    "FandangoBase",
    "DerivationTree",
    "version",
    "homepage",
]

if "pytest" in sys.modules:
    from beartype.claw import beartype_this_package  # type: ignore [import-not-found]
    from beartype import BeartypeConf  # type: ignore [import-not-found]

    beartype_this_package(conf=BeartypeConf(claw_skip_package_names=("fandango",)))


DISTRIBUTION_NAME = "fandango-fuzzer"


def version() -> str:
    """Return the Fandango version number"""
    return importlib.metadata.version(DISTRIBUTION_NAME)


def homepage() -> str:
    """Return the Fandango homepage"""
    metadata = importlib.metadata.metadata(DISTRIBUTION_NAME)
    return [
        e.split(",")[1].strip()
        for e in metadata.get_all("Project-URL", [])
        if e.startswith("homepage,")
    ].pop(0) or "the Fandango homepage"


DerivationTree = fandango.language.tree.DerivationTree
parse = fandango.language.parse.parse


if __name__ == "__main__":
    # Example Usage

    # Set the logging level (for debugging)
    logging_level = None
    if "-vv" in sys.argv:
        logging_level = logging.DEBUG
    elif "-v" in sys.argv:
        logging_level = logging.INFO

    # Read in a .fan spec (from a string)
    # We could also pass an (open) file or a list of files
    spec = """
        <my_start> ::= 'a' | 'b' | 'c'
        where str(<my_start>) != 'd'
    """
    fan = Fandango(spec, logging_level=logging_level, start_symbol="<my_start>")

    # Instantiate the spec into a population of derivation trees
    population = fan.fuzz(extra_constraints=["<my_start> != 'e'"], population_size=3)
    print("Fuzzed:", ", ".join(str(individual) for individual in population))

    # Parse a single input_ into a derivation tree
    trees = fan.parse("a")
    print("Parsed:", ", ".join(str(individual) for individual in trees))
