<start>   ::= <expr>;
<expr>    ::= <term> " + " <expr> | <term> " - " <expr> | <term>;
<term>    ::= <term> " * " <factor> | <term> " / " <factor> | <factor>;
<factor>  ::= "+" <factor> | "-" <factor> | "(" <expr> ")" | <int> ;
<int>     ::= <digit>+;
<digit>   ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";