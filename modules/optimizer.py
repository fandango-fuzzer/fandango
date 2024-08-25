import random
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms


def plot_histogram(data, title, xlabel, ylabel):
    """
    Plots a histogram of the data.

    Args:
        data (list): The data to plot.
        title (str): The title of the histogram.
        xlabel (str): The label for the x-axis.
        ylabel (str): The label for the y-axis.
    """
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()


def generate_perfect_distribution(constraints, num_values):
    min_val = constraints['min']
    max_val = constraints['max']
    distribution = constraints['distr']

    if distribution == 'perf-uniform':
        values = np.linspace(min_val, max_val, num_values).astype(int)
    elif distribution == 'perf-normal':
        mean = (min_val + max_val) / 2
        std_dev = (max_val - min_val) / 6
        values = np.clip(norm.rvs(mean, std_dev, size=num_values),
                         min_val, max_val).astype(int)
        values.sort()  # Sort to simulate a perfect normal distribution
    elif distribution == 'perf-inverse':
        values = np.linspace(max_val, min_val, num_values).astype(int)
    else:
        raise ValueError("Unknown perfect distribution type")

    return values.tolist()

def genetic_algorithm_distribution(constraints, num_values, ngen, verbose=False):
    min_val = constraints['min']
    max_val = constraints['max']
    distribution = constraints['distr']
    parity = constraints.get('parity', None)  # Get the parity constraint

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
        if parity == 'even':
            return all(x % 2 == 0 for x in individual)
        elif parity == 'odd':
            return all(x % 2 == 1 for x in individual)
        return True  # If no parity constraint, it's always feasible

    # Distance function
    def distance(individual):
        if parity == 'even':
            return sum(x % 2 != 0 for x in individual)
        elif parity == 'odd':
            return sum(x % 2 != 1 for x in individual)
        return 0  # If no parity constraint, no distance

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
    """
    Generate a list of values based on constraints including min, max, and distribution.

    Args:
        constraints (dict): The constraints for the attribute.
        num_values (int): The number of values to generate.

    Returns:
        list: A list of generated values that satisfy the constraints.
    """
    distribution = constraints['distr']

    if distribution in ['perf-uniform', 'perf-normal', 'perf-inverse']:
        values = generate_perfect_distribution(constraints, num_values)
    elif distribution in ['uniform', 'normal', 'inverse']:
        values = genetic_algorithm_distribution(
            constraints, num_values, ngen, verbose)
    else:
        raise ValueError("Unknown distribution type")

    return values


def fill_test_suite(test_suite, constraints, ngen, verbose, plot=False):
    """
    Fill the test suite with values generated based on the constraints.

    Args:
        test_suite (list): List of test cases with placeholders.
        constraints (dict): The constraints for each attribute.

    Returns:
        list: The test suite with placeholders replaced by generated values.
    """
    # Determine how many values we need to generate for each attribute
    num_values = len(test_suite)

    # Generate values for each attribute based on constraints
    generated_values = {}
    for attribute, attr_constraints in constraints.items():
        generated_values[attribute] = generate_values(
            attr_constraints, num_values, ngen, verbose)

    if plot:
        for attribute, values in generated_values.items():
            plot_histogram(values, f"Distribution of {attribute}",
                           attribute, "Frequency")

    # Fill the test suite with the generated values
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
        # Add more test cases as needed
    ]

    # Example constraints for age and budget
    CONSTRAINTS = {
        "<age>": {"min": 18, "max": 99, "distr": "perf-normal"},
        "<budget>": {"min": 1000, "max": 20000, "distr": "uniform"}
    }

    filled_test_suite = fill_test_suite(
        test_suite, CONSTRAINTS, ngen=500, verbose=True, plot=True)

    # Print the filled test suite
    for case in filled_test_suite:
        print(case)
