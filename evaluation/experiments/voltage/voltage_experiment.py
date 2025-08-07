from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_voltage():
    with open("evaluation/experiments/voltage/voltage.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False)
        assert grammar is not None

    fandango = Fandango(grammar, constraints)
    solutions = fandango.evolve(max_generations=100, desired_solutions=10)

    print("VOLTAGE")

    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    evaluate_voltage()
