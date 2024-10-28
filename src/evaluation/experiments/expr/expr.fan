# Grammar for Arithmetic Expressions

<start> ::= <expr> ;
<expr> ::=  <term> | <expr> '+' <term> | <expr> '-' <term> ;
<term> ::= <factor> | <term> '*' <factor> | <term> '/' <factor> ;
<factor> ::= <digit>* | '(' <expr> ')' ;
<digit> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;
