from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
import random


def plot_histogram(data, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def genetic_algorithm_distribution(constraints, num_values, ngen, verbose=False):
    min_val = constraints.get('min', None)
    max_val = constraints.get('max', None)
    distribution = constraints.get('distr', 'uniform')
    parity = constraints.get('parity', None)
    sum_constraint = constraints.get('sum_constraint', None)
    min_diff = constraints.get('min_diff', None)
    max_diff = constraints.get('max_diff', None)
    sub_ranges = constraints.get('sub_ranges', None)
    fixed_values = constraints.get('fixed_values', None)  # New: Fixed values constraint

    def fitness_uniform(individual):
        return -np.sum(np.abs(np.histogram(individual, bins=30, range=(min_val, max_val))[0] - num_values/30)),

    def fitness_normal(individual):
        target_distribution = np.clip(norm.rvs((min_val + max_val) / 2, (max_val - min_val) / 6, size=num_values),
                                      min_val, max_val).astype(int)
        return -np.sum(np.abs(np.histogram(individual, bins=30, range=(min_val, max_val))[0] - np.histogram(target_distribution, bins=30, range=(min_val, max_val))[0])),

    def fitness_inverse(individual):
        return -np.sum(np.abs(np.histogram(sorted(individual, reverse=True), bins=30, range=(min_val, max_val))[0] - num_values/30)),

    # Define the fitness function
    if distribution == 'uniform':
        fitness_function = fitness_uniform
    elif distribution == 'normal':
        fitness_function = fitness_normal
    elif distribution == 'inverse':
        fitness_function = fitness_inverse
    else:
        raise ValueError("Unknown genetic distribution type")

    # Create the individual and population structures
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_int", random.randint, min_val, max_val)
    toolbox.register("individual", tools.initRepeat,
                     creator.Individual, toolbox.attr_int, n=num_values)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutUniformInt,
                     low=min_val, up=max_val, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", fitness_function)

    # Feasibility function
    def feasible(individual):
        # Parity constraint
        if parity == 'even':
            if not all(x % 2 == 0 for x in individual):
                return False
        elif parity == 'odd':
            if not all(x % 2 == 1 for x in individual):
                return False

        # Sum constraint
        if sum_constraint is not None:
            if sum(individual) != sum_constraint:
                return False

        # Sub-range constraint
        if sub_ranges is not None:
            for (range_min, range_max, percentage) in sub_ranges:
                count_in_range = sum(
                    1 for x in individual if range_min <= x <= range_max)
                if count_in_range < percentage * num_values:
                    return False

        # Minimum difference between consecutive values
        if min_diff is not None:
            if any(abs(individual[i] - individual[i+1]) < min_diff for i in range(len(individual) - 1)):
                return False

        # Maximum difference between min and max values
        if max_diff is not None:
            if max(individual) - min(individual) > max_diff:
                return False

        # Fixed values constraint
        if fixed_values is not None:
            for position, value in fixed_values.items():
                if individual[position] != value:
                    return False

        return True

    # Distance function
    def distance(individual):
        penalty = 0

        # Parity penalty
        if parity == 'even':
            penalty += sum(x % 2 != 0 for x in individual)
        elif parity == 'odd':
            penalty += sum(x % 2 != 1 for x in individual)

        # Sum constraint penalty
        if sum_constraint is not None:
            penalty += abs(sum(individual) - sum_constraint)

        # Sub-range penalty
        if sub_ranges is not None:
            for (range_min, range_max, percentage) in sub_ranges:
                count_in_range = sum(
                    1 for x in individual if range_min <= x <= range_max)
                penalty += max(0, percentage * num_values - count_in_range)

        # Minimum difference penalty
        if min_diff is not None:
            penalty += sum(max(0, min_diff - abs(
                individual[i] - individual[i+1])) for i in range(len(individual) - 1))

        # Maximum difference penalty
        if max_diff is not None:
            penalty += max(0, max(individual) - min(individual) - max_diff)

        # Fixed values penalty
        if fixed_values is not None:
            for position, value in fixed_values.items():
                if individual[position] != value:
                    penalty += abs(individual[position] - value)

        return penalty

    # Decorate the evaluation function with the DeltaPenalty
    toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, 10.0, distance))

    population = toolbox.population(n=100)

    # Run the genetic algorithm
    algorithms.eaSimple(population, toolbox, cxpb=0.5,
                        mutpb=0.2, ngen=ngen, verbose=verbose)

    # Return the best individual found
    top_individual = tools.selBest(population, k=1)[0]
    return list(top_individual)


def generate_values(constraints, num_values, ngen, verbose=False):
    distribution = constraints['distr']

    if distribution in ['uniform', 'normal', 'inverse']:
        values = genetic_algorithm_distribution(
            constraints, num_values, ngen, verbose)
    else:
        raise ValueError("Unknown distribution type")

    return values


def fill_test_suite(test_suite, constraints, ngen, verbose, plot=False):
    num_values = len(test_suite)

    generated_values = {}
    for attribute, attr_constraints in constraints.items():
        generated_values[attribute] = generate_values(
            attr_constraints, num_values, ngen, verbose)

    if plot:
        for attribute, values in generated_values.items():
            plot_histogram(values, f"Distribution of {attribute}",
                           attribute, "Frequency")

    filled_suite = []
    for i, test_case in enumerate(test_suite):
        filled_case = test_case
        for attribute, values in generated_values.items():
            placeholder = f">{attribute[1:-1]}<"
            filled_case = filled_case.replace(placeholder, str(values[i]))
        filled_suite.append(filled_case)

    return filled_suite


if __name__ == "__main__":
    # Example test suite with placeholders
    test_suite = [
        '{"Name": "Jill", "Gender": "F", "Age": >age<, "Budget": >budget<}',
        '{"Name": "Jack", "Gender": "M", "Age": >age<, "Budget": >budget<}',
        '{"Name": "John", "Gender": "F", "Age": >age<, "Budget": >budget<}',
    ]

    # Example constraints for age and budget
    CONSTRAINTS = {
        "<age>": {
            "min": 18,
            "max": 99,
            "distr": "perf-normal",
            # "sub_ranges": [(18, 40, 0.3), (50, 99, 0.7)],
            # "sum_constraint": 350,  # Total sum constraint
            # "min_diff": 5,  # Minimum difference between consecutive values
            # "max_diff": 50,  # Maximum difference between min and max
            # "fixed_values": {0: 25, 4: 75},  # Fixed values at positions
        },
        "<budget>": {
            "min": 1000,
            "max": 20000,
            "distr": "uniform",
            # "sub_ranges": [(1000, 5000, 0.2), (10000, 20000, 0.8)],
            # "sum_constraint": 80000,
            # "min_diff": 500,  # Minimum difference between consecutive values
            # "max_diff": 15000,  # Maximum difference between min and max
            # "fixed_values": {2: 15000, 5: 5000},  # Fixed values at positions
        }
    }

    filled_test_suite = fill_test_suite(
        test_suite, CONSTRAINTS, ngen=500, verbose=True, plot=True)

    # Print the filled test suite
    for case in filled_test_suite:
        print(case)

