import os
import sys
import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    # Parse grammar and constraints
    with open("ftp_client.fan") as f:
        grammar, constraints = parse(f, use_stdlib=True)
    assert grammar is not None
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.DEBUG,
        coverage_goal=CoverageGoal.STATE_INPUTS,
    )
    fandango.coverage_log_interval = 10
    solutions = []
    start_time = time.time()
    try:
        for solution in fandango.generate(mode=FuzzingMode.IO):
            solutions.append(solution)
    finally:
        print("Done in %.2f seconds." % (time.time() - start_time))

if __name__ == "__main__":
    main()
