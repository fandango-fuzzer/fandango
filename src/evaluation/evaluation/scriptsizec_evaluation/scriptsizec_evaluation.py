import os
import subprocess
import tempfile
import time
from typing import Tuple

from tccbox import tcc_bin_path

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_valid_tinyc_code(c_code: str) -> bool:
    """
    This function takes a string containing Tiny C code and checks if it is syntactically valid.
    Returns True if valid, False otherwise.
    """
    # Create a temporary file to store the C code
    with tempfile.NamedTemporaryFile(suffix=".c", delete=False) as temp_file:
        temp_file.write(c_code.encode())
        temp_file.flush()  # Ensure the content is written to the file
        temp_file_path = temp_file.name

    try:
        # Use tcc to try and compile the file without generating an output (-c option)
        # This is equivalent to a syntax check
        result = subprocess.run(
            [tcc_bin_path(), '-c', temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # If return code is 0, the syntax is valid
        if result.returncode == 0:
            return True
        if "include file" in result.stderr.decode():
            return True
        else:
            print(f"Syntax error:\n{result.stderr.decode()}")
            return False
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        # if any file extension is .o, remove it
        if os.path.exists(temp_file_path[:-2]):
            os.remove(temp_file_path[:-2])


def evaluate_scriptsizec(seconds=1) -> Tuple[str, int, int, float, float, float, float]:
    grammar, constraints = parse_file("scriptsizec_evaluation/scriptsizec.fan")
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = FANDANGO(grammar, constraints, verbose=True, desired_solutions=10)
        fandango.evolve()
        solutions.extend(fandango.solution)


    valid = []
    for solution in solutions:
        parsed_solution = "int main() {\n"
        parsed_solution += "\n" + str(solution).replace("\n", "    \t")
        parsed_solution += "\n" + "}"

        if is_valid_tinyc_code(str(parsed_solution)):
            valid.append(solution)

    coverage = grammar.compute_kpath_coverage(valid, 3)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return "SCRIPTSIZEC", len(solutions), len(valid), valid_percentage, coverage, set_mean_length, set_medium_length