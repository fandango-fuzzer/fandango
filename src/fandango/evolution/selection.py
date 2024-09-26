import random

def roulette_wheel_selection(evaluated_population, num_parents):
    total_fitness = sum(fitness for _, fitness, _ in evaluated_population)
    selection_probabilities = [fitness / total_fitness for _, fitness, _ in evaluated_population]
    parents = random.choices(
        population=[individual for individual, _, _ in evaluated_population],
        weights=selection_probabilities,
        k=num_parents
    )
    return parents

def tournament_selection(evaluated_population, tournament_size, num_parents):
    parents = []
    for _ in range(num_parents):
        tournament = random.sample(evaluated_population, tournament_size)
        best_individual = max(tournament, key=lambda x: x[1])  # x[1] is the fitness score
        parents.append(best_individual[0])  # x[0] is the individual
    return parents

def rank_selection(evaluated_population, num_parents):
    sorted_population = sorted(evaluated_population, key=lambda x: x[1])
    ranks = range(1, len(sorted_population) + 1)
    total_rank = sum(ranks)
    selection_probabilities = [rank / total_rank for rank in ranks]
    parents = random.choices(
        population=[individual for individual, _, _ in sorted_population],
        weights=selection_probabilities,
        k=num_parents
    )
    return parents

if __name__ == "__main__":
    from fandango.language.parse import parse_file
    from fandango.evolution.initialization import generate_initial_population
    from fandango.evolution.fitness import evaluate_population

    # Load a grammar from a file
    grammar, constraints, _ = parse_file("../../evaluation/csv/csv.fan")

    # Generate an initial population of 500 derivation trees
    population = generate_initial_population(grammar, 500)

    # Evaluate the fitness of the population
    evaluated_population = evaluate_population(population, constraints)

    # Perform selection using roulette wheel
    print("Performing roulette wheel selection:")
    parents = roulette_wheel_selection(evaluated_population, 10)
    for parent in parents:
        print(parent)

    # Perform selection using tournament selection
    print("\nPerforming tournament selection:")
    parents = tournament_selection(evaluated_population, 5, 10)
    for parent in parents:
        print(parent)

    # Perform selection using rank selection
    print("\nPerforming rank selection:")
    parents = rank_selection(evaluated_population, 10)
    for parent in parents:
        print(parent)



