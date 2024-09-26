from typing import List, Tuple, Set

from fandango.constraints.base import Constraint
from fandango.language.grammar import DerivationTree


def evaluate_fitness(individual: DerivationTree, constraints: List[Constraint]) -> Tuple[float, Set[DerivationTree]]:
    """
    Evaluates the fitness of an individual derivation tree.

    :param individual: The derivation tree to evaluate.
    :param constraints: A list of constraints to check against.
    :return: A tuple containing the fitness score and a set of failing nodes.
    """
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

    return fitness_score, failing_nodes

if __name__ == "__main__":
    from fandango.language.parse import parse_file
    from fandango.evolution.initialization import generate_initial_population

    # Parse grammar from src/evaluation/csv/csv.fan
    grammar, constraints, _ = parse_file("../../evaluation/int/int.fan")

    # Generate an initial population of 10 derivation trees
    population = generate_initial_population(grammar, 500)

    # Evaluate the fitness of each individual in the population
    for individual in population:
        fitness, failing_nodes = evaluate_fitness(individual, constraints)
        print(f"Input: {individual}, Fitness: {fitness}, Failing nodes: {failing_nodes}")
