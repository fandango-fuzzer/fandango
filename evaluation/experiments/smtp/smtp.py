import os
import time

from fandango.language.grammar import FuzzingMode
from utils import write_coverage_log
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("smtp.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )

    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
    )

    for solution in fandango.generate(mode=FuzzingMode.IO):
            print(str(solution))



if __name__ == "__main__":
    main()
