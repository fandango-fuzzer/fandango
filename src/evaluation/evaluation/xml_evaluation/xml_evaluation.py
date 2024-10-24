import xml.etree.ElementTree as ET

from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file


def is_syntactically_valid_xml(xml_string):
    try:
        # Try to parse the XML string
        ET.fromstring(xml_string)
        return True
    except ET.ParseError as e:
        # If parsing fails, it's not a valid XML
        print(f"XML syntax error: {e}")
        return False

def evaluate_xml():
    grammar, constraints = parse_file("xml.fan")

    fandango = FANDANGO(grammar, constraints, verbose=True, desired_solutions=1000)
    fandango.evolve()

    not_valid = []
    for inp_ in fandango.solution:
        if not is_syntactically_valid_xml(str(inp_)):
            print(f"Invalid XML: {inp_}")
            not_valid.append(inp_)
            print("--------------------")

    #compute mean and median len of input in fandango.solution
    mean_len = sum([len(str(inp_)) for inp_ in fandango.solution]) / len(fandango.solution)
    print(f"Mean length of XMLs: {mean_len}")

    median_len = sorted([len(str(inp_)) for inp_ in fandango.solution])[len(fandango.solution) // 2]
    print(f"Median length of XMLs: {median_len}")

    print(f"Number of invalid XMLs: {len(not_valid)}")

if __name__ == "__main__":
    evaluate_xml()
