import random
from typing import Tuple

from evaluation.vs_isla.csv_evaluation.csv_evaluation import evaluate_csv
from evaluation.vs_isla.rest_evaluation.rest_evaluation import evaluate_rest
from evaluation.vs_isla.scriptsizec_evaluation.scriptsizec_evaluation import (
    evaluate_scriptsizec,
)
from evaluation.vs_isla.tar_evaluation.tar_evaluation import evaluate_tar
from evaluation.vs_isla.xml_evaluation.xml_evaluation import evaluate_xml


# Return the evaluation results as a tuple of values (subject, total, valid, percentage, diversity, mean_length, median)
def better_print_results(
    results: Tuple[str, int, int, float, Tuple[float, int, int], float, float]
):
    print("================================")
    print(f"{results[0]} Evaluation Results")
    print("================================")
    print(f"Total inputs: {results[1]}")
    print(f"Valid {results[0]} solutions: {results[2]} ({results[3]:.2f}%)")
    print(
        f"Grammar coverage (0 to 1): {results[4][0]:.2f} ({results[4][1]} / {results[4][2]})"
    )
    print(f"Mean length: {results[5]:.2f}")
    print(f"Median length: {results[6]:.2f}")
    print("")
    print("")


def run_evaluation(seconds: int = 3600, random_seed: int = 1):
    # Set the random seed
    random.seed(random_seed)

    better_print_results(evaluate_csv(seconds))
    better_print_results(evaluate_rest(seconds))
    better_print_results(evaluate_scriptsizec(seconds))
    better_print_results(evaluate_tar(seconds))
    better_print_results(evaluate_xml(seconds))


if __name__ == "__main__":
    run_evaluation()
