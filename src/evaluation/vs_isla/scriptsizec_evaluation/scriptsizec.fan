<start> ::= <statement> ;
<statement> ::= <block>
              | "if " <paren_expr> <statement> " else " <statement>
              | "if " <paren_expr> <statement>
              | "while " <paren_expr> <statement>
              | "do " <statement> " while " <paren_expr> ";"
              | <expr> ";"
              | ";" ;
<block> ::= "{" <statements> "}" ;
<statements> ::= <block_statement> <statements>
               | "" ;
<block_statement> ::= <statement>
                    | <declaration> ;
<declaration> ::= "int " <id> "=" <expr> ";"
                | "int " <id> ";" ;
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


forall <use_id> in <statement>*<expr>*<id>:
    exists <dec> in <declaration>:
        str(<dec>.<id>) == str(<id>) and is_before(<start>, <dec>, <use_id>)
;

# --------------------------------------------------------------------


# C2: Ensure that no variable is declared more than once in the same scope.

forall <decl1> in <declaration>:
    forall <decl2> in <declaration>:
        (str(<decl1>.<id>) == str(<decl2>.<id>) -> <decl1> == <decl2>)
;

# --------------------------------------------------------------------



def declare_variables(c_code):
    import re
    import random

    # Regular expressions to find variable usage and check for declarations
    var_usage_pattern = r'\b([a-zA-Z])\b'  # Matches single-letter variables
    declaration_pattern = r'\bint\s+([a-zA-Z])\b'  # Matches declared single-letter variables

    # Find all single-letter variable uses in the code
    var_usage = set(re.findall(var_usage_pattern, c_code))

    # Find all declared single-letter variables
    declared_vars = set(re.findall(declaration_pattern, c_code))

    # Identify undeclared single-letter variables
    undeclared_vars = var_usage - declared_vars - {'while', 'if', 'for', 'return', 'main'}

    # Generate declarations for undeclared variables
    declarations = ""
    for var in undeclared_vars:
        value = random.randint(1,100000)  # Random integer placeholder value
        declarations += f"    int {var} = {value};\n"

    # Insert the declarations at the start of the main function
    modified_code = re.sub(r'(\bint main\(\) {)', r'\1\n' + declarations, c_code, count=1)

    return modified_code

str(<start>) == declare_variables(str(<start>));