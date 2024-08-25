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
    # Example constraints for age and budget with additional constraints
    CONSTRAINTS = {
        "<age>": {
            "min": 18,
            "max": 99,
            "distr": "normal",
        },
        "<budget>": {
            "min": 1000,
            "max": 20000,
            "distr": "uniform",
        }
    }

    # Generate scaffolding
    scaffolding = generate_scaffolding(JSON_GRAMMAR, CONSTRAINTS, 100)

    # Optimize the scaffolding
    optimized_scaffolding = fill_test_suite(scaffolding, CONSTRAINTS, plot=True)
    print(optimized_scaffolding)
