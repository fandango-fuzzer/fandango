from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse
from fandango.language.tree import DerivationTree


def count_g_params(tree: DerivationTree):
    count = 0
    if len(tree.generator_params) > 0:
        count += 1
    for child in tree.children:
        count += count_g_params(child)
    for child in tree.generator_params:
        count += count_g_params(child)
    return count

def run():
    # Load the fandango file
    file = open("nested_params.fan", "r")
    grammar, constraints = parse(file, use_stdlib=False, use_cache=False)

    fandango = Fandango(grammar, constraints, max_generations=100, desired_solutions=10)
    fandango.evolve()

    for solution in fandango.solution:
        print(count_g_params(solution))
        print(solution)


if __name__ == "__main__":
    run()