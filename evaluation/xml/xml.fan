<start> ::= <xml_tree>
<xml_tree> ::= <xml_open_tag> <inner_xml_tree> <xml_close_tag>
<inner_xml_tree> ::= <xml_tree> | <text>
<xml_open_tag> ::= "<" <id> " " <xml_attributes> ">" | "<" <id> ">"
<xml_close_tag> ::= "</" <id> ">"
<xml_attributes> ::= <xml_attribute> | <xml_attribute> " " <xml_attributes>
<xml_attribute> ::= <id> '=\"' <text> '\"'
<id> ::= <id_start_char> <id_chars> | <id_start_char>
<id_start_char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"| "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"| "u" | "v" | "w" | "x" | "y" | "z"| "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"| "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"| "U" | "V" | "W" | "X" | "Y" | "Z" | "_"
<id_chars> ::= <id_char> <id_chars> | <id_char>
<id_char> ::= <id_start_char> | "-" | "." | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<text> ::= <text_char> <text> | <text_char> 
<text_char> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"| "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"| "u" | "v" | "w" | "x" | "y" | "z"| "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J"| "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T"| "U" | "V" | "W" | "X" | "Y" | "Z"| "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"| "&quot;"| "&#x27;"| "."| " "| "\t"| "/"| "?"| "-"| ","| "="| ":"| "+"

where forall <tree> in <xml_tree>:
    <tree>.<xml_open_tag>.<id> == <tree>.<xml_close_tag>.<id>

where forall <open_tag> in <xml_tree>.<xml_open_tag>:
    forall <xml_attribute_1> in <open_tag>..<xml_attribute>:
        forall <xml_attribute_2> in <open_tag>..<xml_attribute>:
            (not(<xml_attribute_1> != <xml_attribute_2>) or (str(<xml_attribute_1>.<id>) != str(<xml_attribute_2>.<id>)))

