from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_valid_tar(tar_string):
    pass


def evaluate_tar():
    grammar, constraints = parse_file("tar.fan")

    fandango = FANDANGO(grammar, constraints, verbose=True)
    fandango.evolve()

    for sol in fandango.solution:
        print(sol)


if __name__ == "__main__":
    evaluate_tar()
