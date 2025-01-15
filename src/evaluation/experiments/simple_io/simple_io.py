from fandango.evolution.algorithm import Fandango
from fandango.language.grammar import FuzzingMode
from fandango.language.parse import parse_file


def main():
    # Parse grammar and constraints
    grammar, constraints = parse_file("simple_io.fan")
    # Initialize FANDANGO with desired parameters
    fandango = Fandango(grammar=grammar, constraints=constraints, population_size=100)

    # Evolve solutions
    solutions = fandango.evolve()

    # Output solutions
    for solution in solutions:
        print(str(solution))


if __name__ == "__main__":
    main()
