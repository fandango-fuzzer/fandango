# This cannot be in the main __init__.py or beartype.py
# because it has to be declared after beartype is initialized
# and those two files are imported before that happens
def dummy_function_to_check_if_beartype_is_active(input: int) -> int:
    return input
