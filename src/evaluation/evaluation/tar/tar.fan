<start> ::= <entries> ;

<entries> ::= <entry>
            | <entry> <entries> ;

<entry> ::= <header> <content> ;

<header> ::= <file_name> <checksum> <typeflag> <linked_file_name> ;

<file_name> ::= <characters> <maybe_nuls> ;

<checksum> ::= <padded_octal_digits> <NUL> <SPACE> ;

<typeflag> ::= "0"  | "2"  ;

<linked_file_name> ::= <characters> <maybe_nuls> ;

<content> ::= "CONTENT" ;

<padded_octal_digits> ::= <maybe_zeroes> <octal_digit_nonzero> <maybe_octal_digits> ;

<maybe_octal_digits> ::= ""
                       | <octal_digits> ;

<octal_digits> ::= <octal_digit>
                 | <octal_digit> <octal_digits> ;

<octal_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" ;

<octal_digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" ;

<maybe_zeroes> ::= ""
                 | <zeroes> ;

<zeroes> ::= <ZERO>
           | <ZERO> <zeroes> ;

<characters> ::= <character>
               | <character> <characters> ;

<character> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
              | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
              | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D"
              | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N"
              | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X"
              | "Y" | "Z" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7"
              | "8" | "9" | "!" | "@" | "#" | "$" | "%" | "^" | "&" | "*"
              | "(" | ")" | "-" | "_" | "=" | "+" | "[" | "]" | "{" | "}"
              | "\\" | "|" | ";" | ":" | "'" | "\"" | "," | "<" | "." | ">"
              | "/" | "?" | "`" | "~" | " " ;

<maybe_nuls> ::= ""
               | <nuls> ;

<nuls> ::= <NUL>
         | <NUL> <nuls> ;

<NUL> ::= "\x00" ;

<SPACE> ::= " " ;

<ZERO> ::= "0" ;

