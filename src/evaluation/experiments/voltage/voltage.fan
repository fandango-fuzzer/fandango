<start> ::= <voltage> ;
<voltage> ::= <integer> ;
<integer> ::= <positive_integer> | "-" <positive_integer> ;
<positive_integer> ::= "0" | <digit_nonzero> <digit>* ;
<digit> ::= "0" | <digit_nonzero> ;
<digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

