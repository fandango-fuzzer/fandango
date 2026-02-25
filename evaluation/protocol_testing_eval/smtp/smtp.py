import os
import time

from evaluation.protocol_testing_eval.utils import write_coverage_log
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("smtp_client.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )
    assert grammar is not None

    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.INFO,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )

    for solution in fandango.generate(mode=FuzzingMode.IO):
        pass


if __name__ == "__main__":
    main()
