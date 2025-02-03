from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file


def evaluate_pixels():
    grammar, constraints = parse_file("pixels.fan")

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_pixels()
