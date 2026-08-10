# This grammar can't run. It contains a couple infinite, unbreakable loops for testing the primer here.
# - <inf_simple> - simple unbreakable loop
# - <inf_complex> - complex unbreakable loop
# - <escapable> - escapable loops

<start> ::= <inf_simple> | <inf_complex> | <escapable>


# simple non-escapable loop
<inf_simple> ::= "x" <inf_simple>


# complex non-escapable loops
<inf_complex> ::= <inf_a> | <inf_b> | <inf_c>
<inf_a> ::= "<" <inf_b> ">" | <inf_c> <space> | <inf_b>{1,3}
<inf_b> ::= <inf_c>{2,4} | <inf_a> <name>
<inf_c> ::= <inf_a> | <inf_b> <inf_a> | "?" <inf_b>
<space> ::= " "


# escapable loops
<escapable> ::= <expr>
<expr> ::= <term> | <expr> "+" <term> | "-" <expr>
<term> ::= <factor> | <term> "*" <factor>
<factor> ::= <numeral> | "(" <expr> ")"


# Non-loops
<numeral> ::= <dig>+
<dig> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<name> ::= "fandango" | "is" | "awesome"

