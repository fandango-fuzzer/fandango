from fandango.evolution.algorithm import Fandango
from fandango.language.grammar import *
from fandango.language.symbol import *
from fandango.language.parse import parse


def main():
    # Parse grammar and constraints
    with open("simple_io.fan") as f:
        grammar, constraints = parse(f, use_stdlib=False)
    # Initialize FANDANGO with desired parameters

    fandango = Fandango(grammar=grammar, constraints=constraints, population_size=100)

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))


if __name__ == "__main__":
    main()
