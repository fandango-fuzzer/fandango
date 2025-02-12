<start>  ::= <expr>
<expr>   ::= <term> ' + ' <expr> |<term> ' - ' <expr> | <term>
<term>   ::= <term> ' * ' <factor> | <term> ' / ' <factor> | <factor>
<factor> ::= '+' <factor> | '-' <factor>| '(' <expr> ')' | <int> | <int> '.' <digit>+
<int>    ::= r'[0-9]' | r'[1-9]' <digit>+
