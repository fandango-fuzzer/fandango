from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file


def evaluate_faker():
    grammar, constraints = parse_file("faker.fan")

    fandango = Fandango(grammar, constraints, verbose=True, destruction_rate=0.6)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_faker()
