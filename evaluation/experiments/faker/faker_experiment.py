from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_faker():
    with open("evaluation/experiments/faker/faker.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False)
        assert grammar is not None

    fandango = Fandango(grammar, constraints)
    solutions = fandango.evolve()

    print("FAKER")

    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    evaluate_faker()
