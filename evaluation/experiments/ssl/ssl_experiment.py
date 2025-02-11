import subprocess
import time
from typing import Tuple

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def is_syntactically_valid_ssl(ssl_string: str) -> bool:
    """
    Check whether the given byte sequence (DER-encoded SSL data)
    is syntactically valid according to 'openssl asn1parse -in SSL_INPUT -inform DER'.

    :param ssl_bytes: The SSL data in DER form as bytes.
    :return: True if asn1parse succeeds, False otherwise.
    """
    try:
        process = subprocess.Popen(
            ["openssl", "asn1parse", "-in", ssl_string.encode(), "-inform", "DER"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        # Return True only if the exit code is 0 (successful parse)
        return process.returncode == 0
    except Exception:
        print("Error while running openssl asn1parse")
        # If something goes wrong (e.g., openssl not found), consider it invalid
        return False


def evaluate_ssl(
    seconds=60,
) -> Tuple[str, int, int, float, float, float]:
    file = open("evaluation/experiments/ssl_evaluation/ssl.fan", "r")
    grammar, constraints = parse(file)
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = Fandango(
            grammar,
            constraints,
            population_size=10,
            desired_solutions=10,
            logger_level=LoggerLevel.ERROR,
        )
        fandango.evolve()
        solutions.extend(fandango.solution)

    valid = []
    for solution in solutions:
        if is_syntactically_valid_ssl(str(solution)):
            valid.append(solution)

    try:
        set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    except ZeroDivisionError:
        set_mean_length = 0
    try:
        set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    except IndexError:
        set_medium_length = 0
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "SSL",
        len(solutions),
        len(valid),
        valid_percentage,
        set_mean_length,
        set_medium_length,
    )


# Return the evaluation results as a tuple of values (subject, total, valid, percentage, diversity, mean_length, median)
def better_print_results(results: Tuple[str, int, int, float, float, float]):
    print("================================")
    print(f"{results[0]} Evaluation Results")
    print("================================")
    print(f"Total inputs: {results[1]}")
    print(f"Valid {results[0]} solutions: {results[2]} ({results[3]:.2f}%)")
    print(f"Mean length: {results[4]:.2f}")
    print(f"Median length: {results[5]:.2f}")
    print("")
    print("")


if __name__ == "__main__":
    better_print_results(evaluate_ssl(1))
