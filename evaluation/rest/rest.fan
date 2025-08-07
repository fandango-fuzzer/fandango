<start> ::= <body_elements>
<body_elements> ::= <body_element> "\n" <body_elements> | <body_element>
<body_element> ::= <section_title> "\n" | <labeled_paragraph> | <paragraph> | <enumeration>
<section_title> ::= <title_text> "\n" <underline>
<title_text> ::= <title_first_char> | <title_first_char> <nobr_string>
<paragraph> ::= <first_paragraph_element> <paragraph_elements> "\n"
<label> ::= ".. _" <id> ":"
<labeled_paragraph> ::=  <label> "\n\n" <paragraph>
<paragraph_elements> ::= <paragraph_element> <paragraph_elements> | <paragraph_element>
<first_paragraph_element> ::= <paragraph_chars_nospace> | <internal_reference_nospace>
<paragraph_element> ::= <paragraph_chars> | <internal_reference>
<internal_reference> ::= <presep> <id> '\\_' <postsep>
<internal_reference_nospace> ::= <id> '\\_' <postsep>
<enumeration> ::= <enumeration_items> "\n"
<enumeration_items> ::= <enumeration_item> "\n" <enumeration_items> | <enumeration_item>
<enumeration_item> ::= "#. " <nobr_string>
<paragraph_chars> ::= <paragraph_char> <paragraph_chars> | <paragraph_char>
<paragraph_chars_nospace> ::= <paragraph_char_nospace> <paragraph_chars_nospace> | <paragraph_char_nospace>
<paragraph_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" | " " | "\t" | "\n" | "\r" | "\x0b" | "\x0c"
<paragraph_char_nospace> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~"
<presep> ::= " " | "\t" | "," | ";" | "(" | ")"
<postsep> ::= " " | "\t" | "," | "." | ";" | "(" | ")"
<id> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
<nobr_string> ::= <nobr_char> | <nobr_char> <nobr_string>
<nobr_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" | " " | "\x0b" | "\x0c"
<title_first_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "," | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~"
<underline> ::= <eqs> | <dashes>
<eqs> ::= "=" | "=" <eqs>
<dashes> ::= "-" | "-" <dashes>


# 1. refers to LENGTH_UNDERLINE constraint
where forall <body> in <body_elements>:
    len(str(<body>.<body_element>.<section_title>.<title_text>)) <= len(str(<body>.<body_element>.<section_title>.<underline>))

# 2. refers to DEF_LINK_TARGETS (1) constraint
where forall <internal> in <paragraph_element>:
    exists <labeled_p> in <body_element>:
        str(<labeled_p>.<labeled_paragraph>.<label>.<id>) == str(<internal>.<internal_reference>.<id>)

# 3. refers to DEF_LINK_TARGETS (2) constraint
where forall <inter> in <internal_reference_nospace>:
    exists <labeled_p> in <body_element>:
        str(<labeled_p>.<labeled_paragraph>.<label>.<id>) == str(<inter>.<id>)

# 4. refers to NO_LINK_TARGET_REDEF  constraint
where forall <l1> in <label>:
    exists <l2> in <label>:
        str(<l1>.<id>) == str(<l2>.<id>) and <l1> != <l2>