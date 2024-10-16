from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def evaluate_faker():
    grammar, constraints = parse_file("faker.fan")

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, verbose=True, desired_solutions=1)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_faker()
