<start> ::= <xml_tree> ;
<xml_tree> ::= <xml_open_tag> <inner_xml_tree> <xml_close_tag>  ;
<inner_xml_tree> ::= <xml_tree> | <text> ;
<xml_open_tag> ::= "<" <id> " " <xml_attributes> ">" | "<" <id> ">" ;
<xml_close_tag> ::= "</" <id> ">" ;
<xml_attributes> ::= <xml_attribute> | <xml_attribute> " " <xml_attributes> ;
<xml_attribute> ::= <id> '=\"' <text> '\"' ;
# <id> ::= <id_with_prefix> | <id_no_prefix> ;
<id> ::= <id_start_char> <id_chars> | <id_start_char> ;
# <id_with_prefix> ::= <id_no_prefix> ':' <id_no_prefix> ;
<id_start_char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
                  | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
                  | "u" | "v" | "w" | "x" | "y" | "z"
                  | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
                  | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
                  | "U" | "V" | "W" | "X" | "Y" | "Z" | "_" ;

<id_chars> ::= <id_char> <id_chars> | <id_char> ;
<id_char> ::= <id_start_char> | "-" | "." | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

<text> ::= <text_char> <text> | <text_char> ;

<text_char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
              | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
              | "u" | "v" | "w" | "x" | "y" | "z"
              | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"
              | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"
              | "U" | "V" | "W" | "X" | "Y" | "Z"
              | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
              | "&quot;"
              | "&#x27;"
              | "."
              | " "
              | "\t"
              | "/"
              | "?"
              | "-"
              | ","
              | "="
              | ":"
              | "+" ;

forall <tree> in <xml_tree>:
    <tree>.<xml_open_tag>.<id> == <tree>.<xml_close_tag>.<id>
;

forall <open_tag> in <xml_tree>.<xml_open_tag>:
    forall <xml_attribute_1> in <open_tag>*<xml_attribute>:
        forall <xml_attribute_2> in <open_tag>*<xml_attribute>:
            (<xml_attribute_1> != <xml_attribute_2> -> str(<xml_attribute_1>.<id>) != str(<xml_attribute_2>.<id>))
;

def measure_coverage(input_string):
    import coverage
    import xml.etree.ElementTree as ET

    # Initialize the coverage object with source configuration
    cov = coverage.Coverage(source=["xml.etree.ElementTree", "fandango"])

    try:
        cov.start()
        root = ET.fromstring(input_string)
        cov.stop()
        cov.save()
    except ET.ParseError as e:
        return 0

    # Filter to only ElementTree.py in the specific directory
    try:
        cov_data = cov.get_data()
        for file in cov_data.measured_files():
            if "xml/etree/ElementTree.py" in file:
                # Use _get_file_reporter and _analyze directly on the file
                file_reporter = cov._get_file_reporter(file)
                analysis = cov._analyze(file_reporter)
                covered_statements = len(analysis.statements) - len(analysis.missing)
                total_statements = len(analysis.statements)
                coverage_percentage = (covered_statements / total_statements) * 100 if total_statements > 0 else 0

                return coverage_percentage

    except Exception as e:
        return 0


measure_coverage(str(<start>)) > 0.5;