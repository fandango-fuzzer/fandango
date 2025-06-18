from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("grep.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)

    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        logger_level=LoggerLevel.INFO,
    )
    solutions = fandango.evolve()


if __name__ == "__main__":
    main()
