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

forall <xml_tree> in <start>:
    <xml_tree>.<xml_open_tag>.<id> == <xml_tree>.<xml_close_tag>.<id>
;

forall <xml_open_tag> in <xml_tree>:
    forall <xml_attribute_1> in <xml_open_tag>.<xml_attributes>:
        forall <xml_attribute_2> in <xml_open_tag>.<xml_attributes>:
            <xml_attribute_1>.<xml_attribute>.<id> != <xml_attribute_2>.<xml_attribute>.<id>
;

