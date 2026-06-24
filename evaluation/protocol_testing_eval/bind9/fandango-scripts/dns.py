import measure
from fandango.evolution.algorithm import (
    LoggerLevel,
    ProtocolAlgorithm,
    SimpleGeneticAlgorithm,
)
from fandango.io.navigation.coverage_goal import CoverageGoal
from fandango.language.parse.parse import parse


def main():
    args = measure.parse_args()
    with open(args.grammar or "dns_client.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    assert grammar is not None
    packet_algorithm = SimpleGeneticAlgorithm(
        grammar=grammar,
        constraints=constraints,
        population_size=20,
        max_nodes=600 * 8,
        logger_level=LoggerLevel.INFO,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )
    fandango = ProtocolAlgorithm(
        packet_algorithm=packet_algorithm,
        coverage_goal=CoverageGoal.STATE_INPUTS_OUTPUTS,
    )
    measure.run(fandango, args)


if __name__ == "__main__":
    main()
