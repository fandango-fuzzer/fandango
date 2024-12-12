import subprocess
import tempfile
import time
from typing import Tuple

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse_file


def is_syntactically_valid_tar(tree: str):
    with tempfile.NamedTemporaryFile(suffix=".tar") as outfile:
        outfile.write(tree.encode())
        outfile.flush()
        cmd = ["bsdtar", "-tf", outfile.name]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = process.communicate(timeout=10)
        exit_code = process.wait()

        if exit_code == 0:
            return True
        else:
            return False


def evaluate_tar(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("tar_evaluation/tar.fan")
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = Fandango(
            grammar,
            constraints,
            desired_solutions=100,
            logger_level=LoggerLevel.ERROR,
        )
        fandango.evolve()
        solutions.extend(fandango.solution)

    coverage = grammar.compute_grammar_coverage(solutions, 4)

    valid = []
    for solution in solutions:
        if is_syntactically_valid_tar(str(solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "TAR",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )
