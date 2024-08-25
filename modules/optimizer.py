import random
import numpy as np
from scipy.stats import norm, uniform
import matplotlib.pyplot as plt


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


def generate_values(constraints, num_values):
    """
    Generate a list of values based on constraints including min, max, and distribution.

    Args:
        constraints (dict): The constraints for the attribute.
        num_values (int): The number of values to generate.

    Returns:
        list: A list of generated values that satisfy the constraints.
    """
    min_val = constraints['min']
    max_val = constraints['max']
    distribution = constraints['distr']

    if distribution == 'uniform':
        values = np.random.uniform(min_val, max_val, num_values).astype(int)
    elif distribution == 'normal':
        mean = (min_val + max_val) / 2
        # Approximation to keep most values within bounds
        std_dev = (max_val - min_val) / 6
        values = np.clip(norm.rvs(mean, std_dev, size=num_values),
                         min_val, max_val).astype(int)
    elif distribution == 'inverse':
        values = max_val - \
            np.random.uniform(0, 1, num_values) * (max_val - min_val)
        values = np.sort(values).astype(int)  # Inverse relationship
    else:
        raise ValueError("Unknown distribution type")

    return values.tolist()


def fill_test_suite(test_suite, constraints, plot=False):
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
            attr_constraints, num_values)

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
        "<age>": {"min": 18, "max": 99, "distr": "normal"},
        "<budget>": {"min": 1000, "max": 20000, "distr": "uniform"}
    }

    filled_test_suite = fill_test_suite(test_suite, CONSTRAINTS, plot=True)

    # Print the filled test suite
    for case in filled_test_suite:
        print(case)
