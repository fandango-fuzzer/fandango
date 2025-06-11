from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_voltage():
    file = open("evaluation/experiments/voltage/voltage.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    fandango = Fandango(grammar, constraints)
    fandango.evolve(max_generations=100, desired_solutions=10)

    print("VOLTAGE")

    for solution in fandango.solution:
        print(solution)


if __name__ == "__main__":
    evaluate_voltage()
