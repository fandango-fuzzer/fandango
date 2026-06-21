import sys

from fandango.evolution.algorithm import (
    LoggerLevel,
    ProtocolAlgorithm,
    SimpleGeneticAlgorithm,
)
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse

GRAMMAR = sys.argv[1] if len(sys.argv) > 1 else "smtp_client.fan"


def main():
    with open(GRAMMAR) as f:
        grammar, constraints = parse(f, use_stdlib=False)
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

    list(fandango.generate(mode=FuzzingMode.IO))


if __name__ == "__main__":
    main()
