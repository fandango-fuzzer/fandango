import csv
import time
from io import StringIO
from typing import Tuple, List

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file
from fandango.language.tree import DerivationTree


def compute_diversity_score(solution: List[DerivationTree], ngram_range=(2, 2)):
    """
    Compute the diversity score of a list of strings based on pairwise Jaccard distance.

    Args:
    - str_list: List of strings to evaluate.
    - ngram_range: The n-gram range for tokenization (default is bigrams).

    Returns:
    - diversity_score: A number between 0 and 1 representing the overall diversity.
    """
    population = [str(x) for x in solution]

    # Step 1: Convert strings into n-gram sets using CountVectorizer
    vectorizer = CountVectorizer(analyzer='char', ngram_range=ngram_range, binary=True)
    ngram_matrix = vectorizer.fit_transform(population).toarray()

    # Step 2: Compute pairwise Jaccard distances
    num_strings = len(population)
    total_distance = 0
    num_pairs = 0

    # Iterate over all pairs of strings to compute average dissimilarity
    for i in range(num_strings):
        for j in range(i + 1, num_strings):
            # Compute Jaccard similarity
            sim = jaccard_score(ngram_matrix[i], ngram_matrix[j])
            # Convert to Jaccard distance
            distance = 1 - sim
            total_distance += distance
            num_pairs += 1

    # Step 3: Compute the average Jaccard distance (dissimilarity)
    if num_pairs == 0:
        return 0  # Only one string, no diversity

    avg_dissimilarity = total_distance / num_pairs

    # Return diversity score (between 0 and 1)
    return avg_dissimilarity


def is_syntactically_valid_csv(csv_string):
    try:
        # Create a file-like object from the string
        csv_file = StringIO(csv_string)

        # Create a CSV reader to parse the string
        reader = csv.reader(csv_file)

        # Iterate through the reader to trigger any parsing errors
        for row in reader:
            pass

        # If no errors, it's a valid CSV syntactically
        return True
    except csv.Error as e:
        # If there's a CSV parsing error, it's not valid
        return False


def evaluate_csv(seconds=60) -> Tuple[str, int, int, float, float, float, float]:
    grammar, constraints = parse_file("csv.fan")
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = FANDANGO(grammar, constraints, verbose=False)
        fandango.evolve()
        solutions.extend(fandango.solution)

    print(f"Total inputs: {len(solutions)}")

    valid = []
    for solution in solutions:
        if is_syntactically_valid_csv(str(solution)):
            valid.append(solution)

    print(f"Valid CSV solutions: {len(solutions)} ({len(solutions) / len(valid) * 100:.2f}%)")

    set_diversity = compute_diversity_score(valid)
    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    return "CSV", len(solutions), len(valid), len(solutions) / len(
        valid) * 100, set_diversity, set_mean_length, set_medium_length


if __name__ == "__main__":
    results = evaluate_csv()
