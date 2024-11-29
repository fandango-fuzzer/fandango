from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

if __name__ == "__main__":
    grammar, constraints = parse_file("playground.fan")

    fandango = Fandango(grammar, constraints)
    solutions = fandango.evolve()

    for solution in solutions:
        print(str(solution))
