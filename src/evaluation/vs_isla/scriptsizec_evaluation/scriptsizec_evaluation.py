import os
import shutil
import subprocess
import tempfile
import time
from typing import Tuple

from tccbox import tcc_bin_path

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse_file


def declare_variables(c_code):
    import re
    import random

    # Regular expressions to find variable usage and check for declarations
    var_usage_pattern = r"\b([a-zA-Z])\b"  # Matches single-letter variables
    declaration_pattern = (
        r"\bint\s+([a-zA-Z])\b"  # Matches declared single-letter variables
    )

    # Find all single-letter variable uses in the code
    var_usage = set(re.findall(var_usage_pattern, c_code))

    # Find all declared single-letter variables
    declared_vars = set(re.findall(declaration_pattern, c_code))

    # Identify undeclared single-letter variables
    undeclared_vars = (
        var_usage - declared_vars - {"while", "if", "for", "return", "main"}
    )

    # Generate declarations for undeclared variables
    declarations = ""
    for var in undeclared_vars:
        value = random.randint(1, 100000)  # Random integer placeholder value
        declarations += f"    int {var} = {value};\n"

    # Insert the declarations at the start of the main function
    modified_code = re.sub(
        r"(\bint main\(\) {)", r"\1\n" + declarations, c_code, count=1
    )

    return modified_code


def is_valid_tinyc_code(c_code: str) -> bool:
    """
    This function takes a string containing Tiny C code and checks if it is syntactically valid.
    Returns True if valid, False otherwise.
    """
    # Create a temporary directory to store the C code and any generated files
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, "temp_code.c")

    # Write the C code to a file in the temporary directory
    with open(temp_file_path, "w") as temp_file:
        temp_file.write(c_code)

    try:
        # Use tcc to try and compile the file without generating an output (-c option)
        # This is equivalent to a syntax check
        result = subprocess.run(
            [tcc_bin_path(), "-c", temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=temp_dir,  # Set the working directory to the temp directory
        )

        # If return code is 0, the syntax is valid
        if result.returncode == 0:
            return True
        if "include file" in result.stderr.decode():
            return True
        else:
            return False
    finally:
        # Clean up the temporary directory and its contents
        shutil.rmtree(temp_dir)


def evaluate_scriptsizec(
    seconds=60,
) -> Tuple[str, int, int, float, Tuple[float, int, int], float, float]:
    grammar, constraints = parse_file("scriptsizec_evaluation/scriptsizec.fan")
    solutions = []

    time_in_an_hour = time.time() + seconds

    while time.time() < time_in_an_hour:
        fandango = Fandango(
            grammar, constraints, desired_solutions=100, logger_level=LoggerLevel.ERROR
        )
        fandango.evolve()
        solutions.extend(fandango.solution)

    coverage = grammar.compute_grammar_coverage(solutions, 4)

    valid = []
    for solution in solutions:
        parsed_solution = "int main() {\n"
        parsed_solution += "    " + str(solution).replace("\n", "    \t")
        parsed_solution += "\n" + "}"

        fixed_solution = declare_variables(parsed_solution)

        if is_valid_tinyc_code(str(fixed_solution)):
            valid.append(solution)

    set_mean_length = sum(len(str(x)) for x in valid) / len(valid)
    set_medium_length = sorted(len(str(x)) for x in valid)[len(valid) // 2]
    valid_percentage = len(valid) / len(solutions) * 100
    return (
        "SCRIPTSIZEC",
        len(solutions),
        len(valid),
        valid_percentage,
        coverage,
        set_mean_length,
        set_medium_length,
    )
