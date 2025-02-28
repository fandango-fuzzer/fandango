from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse


def run():
    # Load the fandango file
    file = open("duplex_convert.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False, use_cache=False)

    fandango = Fandango(grammar, constraints, max_generations=100, desired_solutions=10)
    fandango.evolve()

    for solution in fandango.solution:
        print(solution)


if __name__ == "__main__":
    run()