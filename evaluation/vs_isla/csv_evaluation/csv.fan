<start> ::= <csv_file> ;
<csv_file> ::= <csv_header> <csv_records> ;
<csv_header> ::= <csv_record> ;
<csv_records> ::= <csv_record> <csv_records> | "" ;
<csv_record> ::= <csv_string_list> "\n" ;
<csv_string_list> ::= <raw_field> | <raw_field> ";" <csv_string_list> ;
<raw_field> ::= <simple_field> | <quoted_field> ;
<simple_field> ::= <spaces> <simple_characters> <spaces> ;
<simple_characters> ::= <simple_character> <simple_characters> | <simple_character> ;
<simple_character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" ;
<quoted_field> ::= '"' <escaped_field> '"' ;
<escaped_field> ::= <escaped_characters> ;
<escaped_characters> ::= <escaped_character> <escaped_characters> | "" ;
<escaped_character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" | " " | "\t" | "\r" |"\n" ;
<spaces> ::= "" | " " <spaces> ;

where forall <r1> in <csv_record>:
    forall <r2> in <csv_record>:
        |<r1>.<csv_string_list>.<raw_field>| == |<r2>.<csv_string_list>.<raw_field>|