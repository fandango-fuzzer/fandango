from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def evaluate_pixels():
    grammar, constraints = parse_file("pixels.fan")

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, verbose=False)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_pixels()
