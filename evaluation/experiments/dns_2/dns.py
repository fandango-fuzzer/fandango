import time

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("dns.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)

    time_start = time.time()
    fandango = Fandango(grammar=grammar, constraints=constraints, population_size=10)

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
