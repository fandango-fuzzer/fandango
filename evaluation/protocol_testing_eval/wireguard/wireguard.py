from fandango.evolution.algorithm import (
    LoggerLevel,
    ProtocolAlgorithm,
    SimpleGeneticAlgorithm,
)
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.grammar import FuzzingMode
from fandango.language.parse.parse import parse


def main():
    # Parse grammar and constraints
    with open("wireguard.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )
    assert grammar is not None

    packet_algorithm = SimpleGeneticAlgorithm(
        grammar=grammar,
        constraints=constraints,
        population_size=10,
        logger_level=LoggerLevel.INFO,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )
    fandango = ProtocolAlgorithm(
        packet_algorithm=packet_algorithm,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )

    for _solution in fandango.generate(mode=FuzzingMode.IO, max_generations=3):
        pass


if __name__ == "__main__":
    main()
