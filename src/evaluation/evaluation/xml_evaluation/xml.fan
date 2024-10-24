<start> ::= <xml_tree> ;
<xml_tree> ::= <xml_open_tag> <inner_xml_tree> <xml_close_tag> | <xml_openclose_tag> ;
<inner_xml_tree> ::= <xml_tree> <inner_xml_tree> | <xml_tree> | <text> ;
<xml_open_tag> ::= "<" <id> <xml_attribute> ">" | "<" <id> ">" ;
<xml_openclose_tag> ::= "<" <id> <xml_attribute> "/>" | "<" <id> "/>" ;
<xml_close_tag> ::= "</" <id> ">" ;
<xml_attribute> ::= <xml_attribute> <xml_attribute> | <id> '=\"' <text> '\"' ;
<id> ::= <id_start_char> <id_chars> | <id_start_char> ;
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
