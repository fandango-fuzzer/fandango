# Automatically generated from '../src/fandango/converters/antlr/Calculator.g4'.
#
# Calculator
<expression> ::= <NUMBER> | '(' <expression> ')' | <expression> <TIMES> <expression> | <expression> <DIV> <expression> | <expression> <PLUS> <expression> | <expression> <MINUS> <expression>
<PLUS> ::= '+'
<MINUS> ::= '-'
<TIMES> ::= '*'
<DIV> ::= '/'
<NUMBER> ::= r'[0-9]'+
<WS> ::= r'[ \r\n\t]'+  # NOTE: was '-> skip'
