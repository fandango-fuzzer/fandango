#!/usr/bin/env python3.11
import sys

import measure

from fandango.evolution.algorithm import (
    LoggerLevel,
    ProtocolAlgorithm,
    SimpleGeneticAlgorithm,
)
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.parse.parse import parse


def main():
    sys.setrecursionlimit(10**6)
    args = measure.parse_args()
    with open(args.grammar or "ftp_client.fan") as f:
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
    measure.run(fandango, args)


if __name__ == "__main__":
    main()
