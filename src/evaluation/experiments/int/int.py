from typing import Set

from fandango.evolution.algorithm import FANDANGO
from fandango.language.tree import DerivationTree
from fandango.language.parse import parse_file


def evaluate_int(
    population_size: int = 10, max_generations: int = 3000
) -> Set[DerivationTree]:
    grammar, constraints = parse_file("int.fan")

    print(grammar)
    print(constraints)

    fandango = FANDANGO(
        grammar,
        constraints,
        population_size=population_size,
        max_generations=max_generations,
    )
    fandango.evolve()

    print(fandango.solution)

    return fandango.solution


if __name__ == "__main__":
    evaluate_int()
