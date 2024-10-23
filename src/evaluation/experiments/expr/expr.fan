<start> ::= <expr> ;
<expr> ::=  <term> '+100' | <term> '-100' ;
<term> ::= <digit>* ;
<digit> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

int(eval(str(<start>))) < 50 ;
int(eval(str(<start>))) > 0 ;
