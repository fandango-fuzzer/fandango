<start>   ::= <expr>
<expr>    ::= <term> " + " <expr> | <term> " - " <expr> | <term>
<term>    ::= <term> " * " <factor> | <term> " / " <factor> | <factor>
<factor>  ::= "+" <factor> | "-" <factor> | "(" <expr> ")" | <int>
<int>     ::= <digit>+

where eval(str(<expr>)) == 10