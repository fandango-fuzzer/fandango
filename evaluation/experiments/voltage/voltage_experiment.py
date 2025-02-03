from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file


def evaluate_voltage():
    grammar, constraints = parse_file("voltage.fan")

    print(grammar)
    print(constraints)

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_voltage()
