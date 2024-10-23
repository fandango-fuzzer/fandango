import csv
from io import StringIO

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


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
        print(f"CSV syntax error: {e}")
        return False


def evaluate_csv():
    grammar, constraints = parse_file("csv.fan")

    solutions = []
    time_taken = 0
    while len(solutions) < 50000:
        fandango = FANDANGO(grammar, constraints, verbose=False, desired_solutions=1000)
        fandango.evolve()
        time_taken += fandango.time_taken

        valid = []
        for solution in fandango.solution:
            if is_syntactically_valid_csv(str(solution)):
                valid.append(solution)

        solutions.extend(valid)

    print(f"Valid CSV solutions: {len(solutions)}")
    print(f"Time taken: {time_taken}")

if __name__ == "__main__":
    evaluate_csv()
