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

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, verbose=False)
    fandango.evolve()

    parser = []

    for solution in fandango.solution:
        tree = grammar.parse(str(solution))
        if tree:
            parser.append(tree)

    print(f"Number of valid solutions: {len(parser)}")


if __name__ == "__main__":
    evaluate_csv()
