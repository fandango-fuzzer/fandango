import tarfile
from io import BytesIO

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_valid_tar(tar_string):
    try:
        # Convert string to bytes (assuming the input string is base64 or binary data)
        # If it's a text string, you'll need a proper encoding.
        tar_bytes = BytesIO(tar_string.encode('utf-8'))  # This step depends on the source of your string data

        # Open the tarfile object
        with tarfile.open(fileobj=tar_bytes, mode='r') as tar:
            # Try to read the contents to validate it's a proper tar file
            tar.getmembers()
        return True
    except (tarfile.TarError, Exception) as e:
        # If it's not a valid tar file, or there's another error
        print(f"Error: {e}")
        return False


def evaluate_tar():
    grammar, constraints = parse_file("tar.fan")

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, verbose=True)
    fandango.evolve()

    print(fandango.solution)

    not_Valid = []
    for inp_ in fandango.solution:
        if not is_valid_tar(str(inp_)):
            not_Valid.append(inp_)

    print(f"Invalid tar files: {not_Valid}, ({len(not_Valid)} in total)")



if __name__ == "__main__":
    evaluate_tar()
