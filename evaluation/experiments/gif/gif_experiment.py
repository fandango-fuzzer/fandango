import gif

from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse


def is_syntactically_valid_gif(file_path):
    file = open(file_path, "rb")
    reader = gif.Reader()
    reader.feed(file.read())
    errors = False
    if reader.has_screen_descriptor():
        if reader.has_unknown_block():
            errors = True
        if not reader.is_complete():
            errors = True
        if not errors:
            return True
    else:
        return False


def evaluate_gif():
    with open("evaluation/experiments/gif/gif.fan", "r") as fd:
        grammar, constraints = parse(fd)
    fandango = Fandango(
        grammar,
        constraints,
        logger_level=LoggerLevel.DEBUG,
        population_size=100,
        profiling=True,
    )
    fandango.evolve(max_generations=100, desired_solutions=100)
    i = 0
    for sol in fandango.solution:
        with open(f"evaluation/experiments/gif/files/fuzzed_{i}.gif", "wb") as fd:
            # Ensure sol is valid byte data, convert to bytes if needed
            gif_bytes = bytes(
                str(sol), "latin1"
            )  # Use 'latin1' to preserve byte values
            # First, convert the string into bytes, then decode the escape sequences,
            # then re-encode in a one-to-one manner (e.g. latin1) to preserve byte values.
            binary_data = gif_bytes.decode("unicode_escape").encode("latin1")

            fd.write(binary_data)  # Write the raw byte sequence to the file

        # Check the validity of the written file
        if is_syntactically_valid_gif(
            f"evaluation/experiments/gif/files/fuzzed_{i}.gif"
        ):
            i += 1


if __name__ == "__main__":
    evaluate_gif()
