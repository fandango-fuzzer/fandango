import os
import time

from evaluation.experiments.utils import write_coverage_log
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    for _ in range(10):
        with open("radius_spec.fan") as f:
            grammar, constraints = parse(
                f,
                use_stdlib=False,
            )
        assert grammar is not None

        time_start = time.time()
        fandango = Fandango(
            grammar=grammar,
            constraints=constraints,
            logger_level=LoggerLevel.INFO,
            coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS
        )
        try:
            for solution in fandango.generate(mode=FuzzingMode.IO):
                if solution.contains_bytes():
                    print(bytes(solution))
                else:
                    print(str(solution))
        finally:
            pass

if __name__ == "__main__":
    main()
