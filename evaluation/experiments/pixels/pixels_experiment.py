from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_pixels():
    file = open("evaluation/experiments/pixels/pixels.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    print(grammar)
    for constraint in constraints:
        print(constraint)

    fandango = Fandango(grammar, constraints, max_generations=100)
    fandango.evolve()

    for solution in fandango.solution:
        print(solution)


if __name__ == "__main__":
    evaluate_pixels()
