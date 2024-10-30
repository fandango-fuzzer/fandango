from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file

import hashlib


def main():
    # Load the fandango file
    grammar, constraints = parse_file("demo.fan")

    fandango = FANDANGO(grammar, constraints, desired_solutions=1)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    main()
