from typing import Tuple

from evaluation.evaluation.csv_evaluation.csv_evaluation import evaluate_csv
from evaluation.evaluation.rest_evaluation.rest_evaluation import evaluate_rest
from evaluation.evaluation.scriptsizec_evaluation.scriptsizec_evaluation import evaluate_scriptsizec
from evaluation.evaluation.xml_evaluation.xml_evaluation import evaluate_xml


# Return the evaluation results as a tuple of values (subject, total, valid, percentage, diversity, mean_length, median)
def better_print_results(results: Tuple[str, int, int, float, float, float, float]):
    print("================================")
    print(f"{results[0]} Evaluation Results")
    print("================================")
    print(f"Total inputs: {results[1]}")
    print(f"Valid {results[0]} solutions: {results[2]} ({results[3]:.2f}%)")
    print(f"Grammar coverage (0 to 1): {results[4]:.2f}")
    print(f"Mean length: {results[5]:.2f}")
    print(f"Median length: {results[6]:.2f}")
    print("")
    print("")


def run_evaluation():
    # better_print_results(evaluate_csv())
    # better_print_results(evaluate_rest())
    # better_print_results(evaluate_scriptsizec())
    better_print_results(evaluate_xml())


if __name__ == "__main__":
    run_evaluation()
