from io import StringIO

from docutils.core import publish_doctree
from docutils.utils import SystemMessage

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_syntactically_valid_rest(rst_string):
    # StringIO to capture output messages (warnings, errors, etc.)
    error_stream = StringIO()

    try:
        # Parse the reST string into a document tree, capturing system messages
        doctree = publish_doctree(rst_string, settings_overrides={'warning_stream': error_stream})

        # Check if any errors or warnings were captured in the error stream
        errors_warnings = error_stream.getvalue().strip()

        if errors_warnings:
            return False

        return True

    except SystemMessage as e:
        # If an exception is raised, it's definitely not valid
        return False


def evaluate_rest():
    grammar, constraints = parse_file("rest.fan")

    solutions = []
    time_taken = 0
    while len(solutions) < 50000:
        fandango = FANDANGO(grammar, constraints, verbose=False, desired_solutions=1000)
        fandango.evolve()
        time_taken += fandango.time_taken

        valid = []
        for solution in fandango.solution:
            if is_syntactically_valid_rest(str(solution)):
                valid.append(solution)

        solutions.extend(valid)

    print(f"Valid CSV solutions: {len(solutions)}")
    print(f"Time taken: {time_taken}")


if __name__ == "__main__":
    evaluate_rest()
