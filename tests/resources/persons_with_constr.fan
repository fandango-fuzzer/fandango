<start> ::= <person_name> "," <age>
<person_name> ::= <first_name> " " <last_name>
<first_name> ::= <name>
<last_name> ::= <name>
<name> ::= <xascii_uppercase_letter> <xascii_lowercase_letters>
<xascii_lowercase_letters> ::= <xascii_lowercase_letter> <xascii_lowercase_letters> | <xascii_lowercase_letter>
<age> ::= <xdigit> <age> | <xdigit>
<xdigit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<xascii_uppercase_letter> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
<xascii_lowercase_letter> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"

# soft constraint

minimizing min (len(str(<name>)), int(<age>)+100)