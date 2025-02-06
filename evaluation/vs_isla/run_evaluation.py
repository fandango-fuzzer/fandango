import random
import sys
from typing import Tuple

import logging
from fandango.logger import LOGGER

from evaluation.vs_isla.csv_evaluation.csv_evaluation import evaluate_csv
from evaluation.vs_isla.rest_evaluation.rest_evaluation import evaluate_rest
from evaluation.vs_isla.scriptsizec_evaluation.scriptsizec_evaluation import (
    evaluate_scriptsizec,
)
from evaluation.vs_isla.tar_evaluation.tar_evaluation import evaluate_tar
from evaluation.vs_isla.xml_evaluation.xml_evaluation import evaluate_xml

LOGGER.setLevel(logging.WARNING)  # Default

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


def run_evaluation(time: int = 3600):
    seconds = 3600
    random_seed = 1

    if time is not None:
        seconds = int(time)
        print(f"Running evaluation with a time limit of {seconds} seconds.")
    else:
        print("Running evaluation with default settings (1 hour).")

    # Set the random seed
    random.seed(random_seed)

    try:
        better_print_results(evaluate_csv(seconds))
        better_print_results(evaluate_rest(seconds))
        better_print_results(evaluate_scriptsizec(seconds))
        better_print_results(evaluate_tar(seconds))
        better_print_results(evaluate_xml(seconds))
    except Exception as e:
        raise e


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_evaluation(arg)
