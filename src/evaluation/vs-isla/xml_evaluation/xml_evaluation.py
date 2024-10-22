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

    print(grammar)
    print(constraints)

    fandango = FANDANGO(grammar, constraints, verbose=True)
    fandango.evolve()

    print(fandango.solution)

    # check = True
    # not_Valid = []
    # for inp_ in fandango.solution:
    #     if not is_syntactically_valid_xml(str(inp_)):
    #         check = False
    #         not_Valid.append(inp_)
    #         break


if __name__ == "__main__":
    evaluate_xml()
