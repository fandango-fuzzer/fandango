import hashlib

<start> ::= <data_record>
<data_record> ::= <string> ' = ' <hash>
<string> ::= <char>+
<char> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
<hash> ::= <hex_digit>+
<hex_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f"

where str(<hash>) == hashlib.sha256(str(<string>).encode('utf-8')).hexdigest();