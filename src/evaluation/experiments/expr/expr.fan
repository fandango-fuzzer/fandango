# Grammar for Arithmetic Expressions

<start> ::= <expr> ;
<expr> ::= <term> '+' <expr> | <term> '-' <expr> | <term> ;
<term> ::= <factor> '*' <term> | <factor> '/' <term> | <factor> ;
<factor> ::= '+' <factor> | '-' <factor> |  '(' <expr> ')' | <number> | <number> '.' <number> ;
<number> ::= <digit>* ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

# Constraints