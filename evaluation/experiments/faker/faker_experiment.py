from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_faker():
    file = open("evaluation/experiments/faker/faker.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_faker()
