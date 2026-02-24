import os
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("dune.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )
    fandango.coverage_log_interval = 10
    fandango.enable_guidance(False)

    for solution in fandango.generate(mode=FuzzingMode.IO):
        pass


if __name__ == "__main__":
    main()
