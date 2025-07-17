from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.grammar import *
from fandango.language.symbol.symbol import *
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("simple_io.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    # Initialize FANDANGO with desired parameters

    # tree = grammar.parse("{}{\"nr_high\":10,\"nr_low\":5}", mode=ParsingMode.INCOMPLETE_ROLE)

    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        logger_level=LoggerLevel.INFO,
    )

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))


if __name__ == "__main__":
    main()
