from modules.extractor import extract_grammar_and_constraints
from modules.optimizer import fill_test_suite
from modules.scaffolding import generate_scaffolding

if __name__ == '__main__':
    # Define the JSON grammar
    JSON_GRAMMAR = {
        "<start>": ["{<json>}"],
        "<json>": ["<nameAttr>, <genderAttr>, <ageAttr>, <budgetAttr>"],
        "<nameAttr>": ['"Name": "<name>"'],
        "<genderAttr>": ['"Gender": "<gender>"'],
        "<ageAttr>": ['"Age": <age>'],
        "<budgetAttr>": ['"Budget": <budget>'],
        "<name>": ["John", "Jane", "Jim", "Jill", "Jack"],
        "<gender>": ["M", "F"],
        "<age>": ["<digit>", "<digit><age>"],
        "<budget>": ["<digit>", "<digit><budget>"],
        "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    }

    # Define the constraints for certain fields
    CONSTRAINTS = {
        "<age>": {
            "min": 18,
            "max": 99,
            "distr": "normal",
            "sum_constraint": 350,  # Total sum constraint
            "min_diff": 5,  # Minimum difference between consecutive values
            "max_diff": 50,  # Maximum difference between min and max
        },
        "<budget>": {
            "min": 1000,
            "max": 20000,
            "distr": "uniform",
            "sum_constraint": 80000,  # Total sum constraint
            "min_diff": 500,  # Minimum difference between consecutive values
            "max_diff": 15000,  # Maximum difference between min and max
        }
    }

    # Generate scaffolding
    scaffolding = generate_scaffolding(JSON_GRAMMAR, CONSTRAINTS, 200)

    # Optimize the scaffolding
    optimized_scaffolding = fill_test_suite(
        scaffolding, CONSTRAINTS, ngen=100, verbose=False, plot=True)
    print(optimized_scaffolding)
