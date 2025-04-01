from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def evaluate_faker():
    grammar, constraints = parse_file("faker/faker.fan")

    fandango = FANDANGO(grammar, constraints, verbose=True)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_faker()
