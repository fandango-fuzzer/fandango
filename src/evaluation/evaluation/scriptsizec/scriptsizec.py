import os
import subprocess
import tempfile

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


def evaluate_scriptsizec():
    grammar, constraints = parse_file("scriptsizec.fan")

    fandango = FANDANGO(grammar, constraints, verbose=True)

    print(fandango.solution)

    parser = []

    for solution in fandango.solution:
        tree = grammar.parse(str(solution))
        if tree:
            parser.append(tree)

    print(f"Number of valid solutions: {len(parser)}")

    # not_valid = []
    # for solution in fandango.solution:
    #     if not is_valid_tinyc_code(str(solution)):
    #         not_valid.append(solution)
    # print(f"Number of invalid solutions: {len(not_valid)}")


if __name__ == "__main__":
    evaluate_scriptsizec()
