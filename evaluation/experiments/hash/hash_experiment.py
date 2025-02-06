from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def evaluate_hash():
    file = open("evaluation/experiments/hash/hash.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False)

    print(grammar)
    print(constraints)

    fandango = Fandango(grammar, constraints)
    fandango.evolve()

    print(fandango.solution)


if __name__ == "__main__":
    evaluate_hash()
