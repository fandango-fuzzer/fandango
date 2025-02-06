from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_pixels():
    file = open("evaluation/experiments/pixels/pixels.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_pixels()
