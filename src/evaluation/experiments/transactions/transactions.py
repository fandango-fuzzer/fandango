from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

import hashlib


def main():
    # Load the fandango file
    grammar, constraints = parse_file("transactions.fan")

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    main()
