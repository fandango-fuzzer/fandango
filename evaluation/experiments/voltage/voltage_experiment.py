from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def evaluate_voltage():
    grammar, constraints = parse_file("voltage/voltage.fan")

    fandango = FANDANGO(grammar, constraints, verbose=False, desired_solutions=100)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_voltage()
