from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


def count_g_params(tree: DerivationTree):
    count = 0
    if len(tree.sources) > 0:
        count += 1
    for child in tree.children:
        count += count_g_params(child)
    for child in tree.sources:
        count += count_g_params(child)
    return count


def run():
    # Load the fandango file
    # file = open("nested_params.fan", "r")
    with open("nested_params_complexer.fan", "r") as file:
        grammar, constraints = parse(file, use_stdlib=False, use_cache=False)
        assert grammar is not None
    # file = open("generator_params.fan", "r")

    fandango = Fandango(
        grammar,
        constraints,
        logger_level=LoggerLevel.DEBUG,
    )
    solutions = fandango.evolve(max_generations=100, desired_solutions=10)

    for solution in solutions:
        print(count_g_params(solution))
        print(solution.to_bytes().decode())


if __name__ == "__main__":
    run()
