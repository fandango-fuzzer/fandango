<start>   ::= <expr>
<expr>    ::= <term> " + " <expr> | <term> " - " <expr> | <term>
<term>    ::= <term> " * " <factor> | <term> " / " <factor> | <factor>
<factor>  ::= "+" <factor> | "-" <factor> | "(" <expr> ")" | <int>
<int>     ::= <digit>+