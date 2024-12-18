import warnings

from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

warnings.filterwarnings("ignore")


def tree_to_binary(tree):
    """
    Convert a tree to a binary representation
    :param tree: The tree to convert
    :return: The binary representation of the tree

    Example:
    tree = '<x17>T</x17>'
    tree_to_binary(tree) -> '001111000111100000110001001101110011111001010100001111000010111101111000001100010011011100111110'
    """
    return "".join(format(byte, "08b") for byte in str(tree).encode("utf-8"))


def binary_to_string(binary):
    """
    Convert a binary representation to a string
    :param binary: The binary representation to convert
    :return: The string representation of the binary

    Example:
    binary = '001111000111100000110001001101110011111001010100001111000010111101111000001100010011011100111110'
    binary_to_string(binary) -> '<x17>T</x17>'
    """
    return "".join(chr(int(binary[i : i + 8], 2)) for i in range(0, len(binary), 8))


if __name__ == "__main__":
    xml_grammar, xml_constraints = parse_file(
        "xml.fan"
    )  # Load the XML grammar and constraints
    xml_files = Fandango(xml_grammar, xml_constraints).evolve()  # Generate XML files
    xml_binaries = [
        tree_to_binary(xml) for xml in xml_files
    ]  # Convert XML files to binary

    bytes_grammar, bytes_constraints = parse_file(
        "bytes.fan"
    )  # Load the bytes grammar and constraints
    xml_binary_trees = [
        bytes_grammar.parse(xml_binary) for xml_binary in xml_binaries
    ]  # Parse the binary repr into derivation trees

    solutions = Fandango(
        bytes_grammar,
        bytes_constraints,
        initial_population=xml_binary_trees,
    ).evolve()  # Generate bytes files

    for solution in solutions:
        print(
            binary_to_string(str(solution))
        )  # Convert the binary files to strings and print them
