import time

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("smtp.fan") as f:
        grammar, constraints = parse(
            f,
            use_stdlib=False,
        )
        assert grammar is not None

    time_start = time.time()
    fandango = Fandango(
        grammar=grammar,
        constraints=constraints,
        population_size=100,
        logger_level=LoggerLevel.INFO,
    )

    # Evolve solutions

    solutions = fandango.evolve()
    print(time.time() - time_start)

    # Output solutions
    for solution in solutions:
        if solution.contains_bytes():
            print(bytes(solution))
        else:
            print(str(solution))


if __name__ == "__main__":
    main()
