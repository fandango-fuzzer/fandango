import os
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("dns.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=10,
        # elitism_rate=1.0,
        max_nodes=600 * 8,
        logger_level=LoggerLevel.INFO,
        coverage_goal=CoverageGoal.STATE_INPUTS
    )
    fandango.coverage_log_interval = 10
    fandango.enable_guidance(True)

    for solution in fandango.generate(mode=FuzzingMode.IO):
        pass


if __name__ == "__main__":
    main()
