from typing import List, Tuple, Set, Dict

from fandango.constraints.base import Constraint
from fandango.language.grammar import DerivationTree


def evaluate_fitness(
    individual: DerivationTree,
    constraints: List[Constraint],
    fitness_cache: Dict[int, Tuple[float, Set[DerivationTree]]],
) -> Tuple[float, Set[DerivationTree]]:
    """
    Evaluates the fitness of an individual derivation tree, using a cache to avoid redundant computations.

    :param individual: The derivation tree to evaluate.
    :param constraints: A list of constraints to check against.
    :param fitness_cache: A cache dictionary to store fitness evaluations.
    :return: A tuple containing the fitness score and a set of failing nodes.
    """
    # Use the hash representation as the cache key
    individual_hash = hash(individual)
    if individual_hash in fitness_cache:
        return fitness_cache[individual_hash]

    total_fitness = 0.0
    total_constraints = len(constraints)
    failing_nodes = set()

    for constraint in constraints:
        fitness_result = constraint.fitness(individual)
        if fitness_result.success:
            total_fitness += 1.0  # Full point for satisfying this constraint
        else:
            # Optionally, partial credit based on fitness_result.fitness()
            total_fitness += fitness_result.fitness()
            failing_nodes.update(fitness_result.failing_trees)

    # Normalize the fitness score to be between 0 and 1
    fitness_score = total_fitness / total_constraints if total_constraints > 0 else 0.0

    # Cache the result
    fitness_cache[individual_hash] = (fitness_score, failing_nodes)

    return fitness_score, failing_nodes


def evaluate_population(
    population: List[DerivationTree], constraints: List[Constraint]
) -> [List[Tuple[DerivationTree, float, Set[DerivationTree]]], Set[DerivationTree]]:
    """
    Evaluates the fitness of each individual in the population, using caching.

    :param population: The list of derivation trees.
    :param constraints: The list of constraints.
    :return: A list of tuples containing the individual, its fitness score, and failing nodes.
    """
    evaluated_population = []
    evaluated_failing_nodes = set()
    fitness_cache = {}

    for individual in population:
        fitness_score, failing_nodes = evaluate_fitness(
            individual, constraints, fitness_cache
        )
        evaluated_population.append((individual, fitness_score, failing_nodes))
        evaluated_failing_nodes.update(failing_nodes)

    return evaluated_population, evaluated_failing_nodes


if __name__ == "__main__":
    import time
    from fandango.language.parse import parse_file
    from fandango.evolution.initialization import generate_initial_population

    # Parse grammar from src/evaluation/csv/csv.fan
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    # Generate an initial population of 500 derivation trees
    population = generate_initial_population(grammar, 500)

    start_time = time.time()

    # Evaluate the fitness of each individual in the population
    evaluated_population, _ = evaluate_population(population, constraints)

    print(f"Elapsed time: {time.time() - start_time:.2f} seconds")

    # print the fitness score of each individual
    for individual, fitness_score, failing_nodes in evaluated_population:
        print(f"Fitness: {fitness_score}")
        print(f"Failing nodes: {failing_nodes}")
        print(individual)
        print()
