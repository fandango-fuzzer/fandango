<start> ::= <statement> ;
<statement> ::= <block>
              | "if" <paren_expr> <statement> "else" <statement>
              | "if" <paren_expr> <statement>
              | "while" <paren_expr> <statement>
              | "do" <statement> "while" <paren_expr> ";"
              | <expr> ";"
              | ";" ;
<block> ::= "{" <statements> "}" ;
<statements> ::= <block_statement> <statements>
               | "" ;
<block_statement> ::= <statement>
                    | <declaration> ;
<declaration> ::= "int" <id> "=" <expr> ";"
                | "int" <id> ";" ;
<paren_expr> ::= "(" <expr> ")" ;
<expr> ::= <id> "=" <expr>
         | <test> ;
<test> ::= <sum> "<" <sum>
         | <sum> ;
<sum> ::= <sum> "+" <term>
        | <sum> "-" <term>
        | <term> ;
<term> ::= <paren_expr>
         | <id>
         | <int> ;
<id> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
       | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
       | "u" | "v" | "w" | "x" | "y" | "z" ;
<int> ::= <digit_nonzero> <digits>
        | <digit> ;
<digits> ::= <digit> <int>
           | <digit> ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
<digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;


# C1: Ensures that any identifier used in an expression is declared before its use, and the declaration occurs in the same or a higher block level (i.e., considering variable scope).

def declaration_is_before_expression(tree, declaration, expression):
    code = str(tree)
    decl = str(declaration)
    expr = str(expression)

    index1 = code.find(decl)
    index2 = code.find(expr)

    if index1 == -1 or index2 == -1 or index1 > index2:
        return False  # Declaration is not before the expression

    # Function to calculate the block level of a given position
    def get_block_level(code, position):
        level = 0
        for i in range(position):
            if code[i] == '{':
                level += 1
            elif code[i] == '}':
                level -= 1
        return level

    # Check block levels at the two positions
    declaration_level = get_block_level(code, index1)
    expression_level = get_block_level(code, index2)

    # Return True if declaration is at the same or higher level than the expression
    return declaration_level <= expression_level


forall <expr> in <statement>:
    forall <id> in <expr>:
        exists <declaration> in <block_statement>:
            str(<declaration>.<id>) == str(<id>) and declaration_is_before_expression(<start>, <declaration>, <expr>)
;

# --------------------------------------------------------------------


# C2: Ensure that no variable is declared more than once in the same scope.

def check_positions(decl1, decl2, id1, id2):
    if str(decl1) != str(decl2):
        str(id1) != str(id2)

forall <decl1> in <declaration>:
    forall <decl2> in <declaration>:
        check_positions(<decl1>, <decl2>, <decl1>.<id>, <decl2>.<id>)
;
