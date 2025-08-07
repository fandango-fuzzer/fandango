from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_pixels():
    with open("evaluation/experiments/pixels/pixels.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False)
        assert grammar is not None

    fandango = Fandango(grammar, constraints)
    solutions = fandango.evolve(max_generations=100, desired_solutions=10)

    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    evaluate_pixels()
