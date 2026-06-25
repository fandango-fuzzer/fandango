import sys

from fandango.evolution.algorithm import (
    LoggerLevel,
    ProtocolAlgorithm,
    SimpleGeneticAlgorithm,
)
from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    # Parse grammar and constraints
    with open("ftp_client.fan") as f:
        grammar, constraints = parse(f, use_stdlib=True)
    assert grammar is not None
    packet_algorithm = SimpleGeneticAlgorithm(
        grammar=grammar,
        constraints=constraints,
        logger_level=LoggerLevel.DEBUG,
    )
    fandango = ProtocolAlgorithm(
        packet_algorithm=packet_algorithm,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )

    list(fandango.generate(mode=FuzzingMode.IO))  # force evaluation of generator


if __name__ == "__main__":
    main()
