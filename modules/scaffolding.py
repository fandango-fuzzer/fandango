import random
from fuzzingbook.GrammarFuzzer import EvenFasterGrammarFuzzer


class CustomGrammarFuzzer(EvenFasterGrammarFuzzer):
    def check_grammar(self) -> None:
        """Override the check_grammar method to bypass grammar checks."""
        return True


def adapt_grammar(grammar: dict, constraints: dict) -> dict:
    """
    Modify the grammar to replace constrained fields with placeholders.

    Args:
        grammar (dict): The grammar definition.
        constraints (dict): The constraints definition.

    Returns:
        dict: The adapted grammar with placeholders for constrained fields.
    """
    adapted_grammar = str(grammar)
    for constraint in constraints.keys():
        placeholder = f">{constraint[1:-1]}<"
        adapted_grammar = adapted_grammar.replace(constraint, placeholder)
    return eval(adapted_grammar)


def generate_scaffolding(grammar: dict, constraints: dict, num_inputs: int) -> list:
    """
    Generate a specified number of inputs using the provided grammar and constraints.

    Args:
        grammar (dict): The grammar definition.
        constraints (dict): The constraints definition.
        num_inputs (int): Number of inputs to generate.

    Returns:
        list: A list of generated inputs with placeholders for constrained fields.
    """
    adapted_grammar = adapt_grammar(grammar, constraints)
    fuzzer = CustomGrammarFuzzer(adapted_grammar)
    return [fuzzer.fuzz() for _ in range(num_inputs)]


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
        "<budget>": {"min": 1, "max": 20000},
        "<age>": {"min": 18, "max": 99},
    }

    # Generate inputs based on the JSON grammar and constraints
    num_inputs = 200
    generated_inputs = generate_scaffolding(
        JSON_GRAMMAR, CONSTRAINTS, num_inputs)

    # Output the generated inputs
    for input_data in generated_inputs:
        print(input_data)
