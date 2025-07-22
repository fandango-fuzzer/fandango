<start> ::= <statement>
<statement> ::= <block>| "if " <paren_expr> <statement> " else " <statement>| "if " <paren_expr> <statement>| "while " <paren_expr> <statement>| "do " <statement> " while " <paren_expr> ";"| <expr> ";"| ";"
<block> ::= "{" <statements> "}"
<statements> ::= <block_statement> <statements> | ""
<block_statement> ::= <statement>| <declaration>
<declaration> ::= "int " <id> "=" <expr> ";"| "int " <id> ";"
<paren_expr> ::= "(" <expr> ")"
<expr> ::= <id> "=" <expr>| <test>
<test> ::= <sum> "<" <sum>| <sum>
<sum> ::= <sum> "+" <term> | <sum> "-" <term> | <term>
<term> ::= <paren_expr>| <id>| <int>
<id> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"| "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"| "u" | "v" | "w" | "x" | "y" | "z"
<int> ::= <digit_nonzero> <digits>| <digit>
<digits> ::= <digit> <int><digit>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"


# C1: Ensures that any identifier used in an expression is declared before its use, and the declaration occurs in the same or a higher block level (i.e., considering variable scope).


where forall <use_id> in <statement>..<expr>..<id>:
    exists <dec> in <declaration>:
        str(<dec>.<id>) == str(<id>) and is_before(<start>, <dec>, <use_id>)

# --------------------------------------------------------------------


# C2: Ensure that no variable is declared more than once in the same scope.

where forall <decl1> in <declaration>:
    forall <decl2> in <declaration>:
        not(str(<decl1>.<id>) == str(<decl2>.<id>)) or <decl1> == <decl2>
