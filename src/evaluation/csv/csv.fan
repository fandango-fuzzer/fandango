<start> ::= <csv-file> ;
<csv-file> ::= <csv-header> <csv-records> ;
<csv-header> ::= <csv-record> ;
<csv-records> ::= <csv-record> <csv-records> | "" ;
<csv-record> ::= <csv-string-list> "\n" ;
<csv-string-list> ::= <raw-field> | <raw-field> ";" <csv-string-list> ;
<raw-field> ::= <simple-field> | <quoted-field> ;
<simple-field> ::= <spaces> <simple-characters> <spaces> ;
<simple-characters> ::= <simple-character> <simple-characters> | <simple-character> ;
<simple-character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" ;
<quoted-field> ::= '"' <escaped-field> '"' ;
<escaped-field> ::= <escaped-characters> ;
<escaped-characters> ::= <escaped-character> <escaped-characters> | "" ;
<escaped-character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" | " " | "\t" | "\r" |"\n" ;
<spaces> ::= "" | " " <spaces> ;

forall <r1> in <csv_record>: forall <r2> in <csv_record>: |<r1>.<raw_field>| == |<r2>.<raw_field>| ;