lexer grammar FandangoLexer;

tokens {
    INDENT,
    DEDENT
}

options {
   superClass = FandangoLexerBase;
}

// constants
STRING: STRING_LITERAL | BYTES_LITERAL;

NUMBER: INTEGER | FLOAT_NUMBER | IMAG_NUMBER;

INTEGER: DECIMAL_INTEGER | OCT_INTEGER | HEX_INTEGER | BIN_INTEGER;

// These calls `python_start()`, `python_end()`, etc. work in Python and in C++
PYTHON_START: '<py>' { python_start(); };
PYTHON_END  : '</py>' { python_end(); };

// python keywords
AND        : 'and';
AS         : 'as';
ASSERT     : 'assert';
ASYNC      : 'async';
AWAIT      : 'await';
BREAK      : 'break';
CASE       : 'case' { python_start(); };
CLASS      : 'class' { python_start(); };
CONTINUE   : 'continue';
DEF        : 'def' { python_start(); };
DEL        : 'del';
ELIF       : 'elif' { python_start(); };
ELSE       : 'else' { python_start(); };
EXCEPT     : 'except' { python_start(); };
FALSE      : 'False';
FINALLY    : 'finally' { python_start(); };
FOR        : 'for' { python_start(); };
FROM       : 'from';
GLOBAL     : 'global';
IF         : 'if' { python_start(); };
IMPORT     : 'import';
IN         : 'in';
IS         : 'is';
LAMBDA     : 'lambda';
MATCH      : 'match' { python_start(); };
NONE       : 'None';
NONLOCAL   : 'nonlocal';
NOT        : 'not';
OR         : 'or';
PASS       : 'pass';
RAISE      : 'raise';
RETURN     : 'return';
TRUE       : 'True';
TRY        : 'try' { python_start(); };
TYPE       : 'type';
WHILE      : 'while' { python_start(); };
WHERE      : 'where';
WITH       : 'with' { python_start(); };
YIELD      : 'yield';
FORALL     : 'forall';
EXISTS     : 'exists';
MAXIMIZING : 'maximizing';
MINIMIZING : 'minimizing';

// identifiers
NAME: ID_START ID_CONTINUE*;

// literals
STRING_LITERAL: ( [rR] | [uU] | [fF] | ( [fF] [rR]) | ( [rR] [fF]))? ( SHORT_STRING | LONG_STRING);
BYTES_LITERAL: ( [bB] | ( [bB] [rR]) | ( [rR] [bB])) ( SHORT_BYTES | LONG_BYTES);
DECIMAL_INTEGER: NON_ZERO_DIGIT DIGIT* | '0'+;
OCT_INTEGER: '0' [oO] OCT_DIGIT+;
HEX_INTEGER: '0' [xX] HEX_DIGIT+;
BIN_INTEGER: '0' [bB] BIN_DIGIT+;
FLOAT_NUMBER: POINT_FLOAT | EXPONENT_FLOAT;
IMAG_NUMBER: ( FLOAT_NUMBER | INT_PART) [jJ];

// operators
GRAMMAR_ASSIGN     : '::=';
QUESTION           : '?';
BACKSLASH          : '\\';
DOT                : '.';
DOTDOT             : '..';
ELLIPSIS           : '...';
STAR               : '*';
OPEN_PAREN         : '(' { open_brace(); };
CLOSE_PAREN        : ')' { close_brace(); };
COMMA              : ',';
COLON              : ':';
SEMI_COLON         : ';';
POWER              : '**';
ASSIGN             : '=';
OPEN_BRACK         : '[' { open_brace(); };
CLOSE_BRACK        : ']' { close_brace(); };
OR_OP              : '|';
XOR                : '^';
AND_OP             : '&';
LEFT_SHIFT         : '<<';
RIGHT_SHIFT        : '>>';
ADD                : '+';
MINUS              : '-';
DIV                : '/';
MOD                : '%';
IDIV               : '//';
NOT_OP             : '~';
OPEN_BRACE         : '{' { open_brace(); };
CLOSE_BRACE        : '}' { close_brace(); };
LESS_THAN          : '<';
GREATER_THAN       : '>';
EQUALS             : '==';
GT_EQ              : '>=';
LT_EQ              : '<=';
NOT_EQ_1           : '<>';
NOT_EQ_2           : '!=';
AT                 : '@';
ARROW              : '->';
ADD_ASSIGN         : '+=';
SUB_ASSIGN         : '-=';
MULT_ASSIGN        : '*=';
AT_ASSIGN          : '@=';
DIV_ASSIGN         : '/=';
MOD_ASSIGN         : '%=';
AND_ASSIGN         : '&=';
OR_ASSIGN          : '|=';
XOR_ASSIGN         : '^=';
LEFT_SHIFT_ASSIGN  : '<<=';
RIGHT_SHIFT_ASSIGN : '>>=';
POWER_ASSIGN       : '**=';
IDIV_ASSIGN        : '//=';
EXPR_ASSIGN        : ':=';
EXCL               : '!';


NEWLINE: (('\r'? '\n' | '\r' | '\f') SPACES?) { on_newline(); };
SKIP_: ( SPACES | COMMENT | LINE_JOINING) -> channel(HIDDEN);

UNKNOWN_CHAR: .;

/*
 * fragments
 */
fragment SHORT_STRING:
    '\'' (STRING_ESCAPE_SEQ | ~[\\\r\n\f'])* '\''
    | '"' ( STRING_ESCAPE_SEQ | ~[\\\r\n\f"])* '"'
;
fragment LONG_STRING: '\'\'\'' LONG_STRING_ITEM*? '\'\'\'' | '"""' LONG_STRING_ITEM*? '"""';
fragment LONG_STRING_ITEM: LONG_STRING_CHAR | STRING_ESCAPE_SEQ;
fragment LONG_STRING_CHAR: ~'\\';
fragment STRING_ESCAPE_SEQ: '\\' . | '\\' NEWLINE;
fragment NON_ZERO_DIGIT: [1-9];
fragment DIGIT: [0-9];
fragment OCT_DIGIT: [0-7];
fragment HEX_DIGIT: [0-9a-fA-F];
fragment BIN_DIGIT: [01];
fragment POINT_FLOAT: INT_PART? FRACTION | INT_PART '.';
fragment EXPONENT_FLOAT: ( INT_PART | POINT_FLOAT) EXPONENT;
fragment INT_PART: DIGIT+;
fragment FRACTION: '.' DIGIT+;
fragment EXPONENT: [eE] [+-]? DIGIT+;
fragment SHORT_BYTES:
    '\'' (SHORT_BYTES_CHAR_NO_SINGLE_QUOTE | BYTES_ESCAPE_SEQ)* '\''
    | '"' ( SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE | BYTES_ESCAPE_SEQ)* '"'
;
fragment LONG_BYTES: '\'\'\'' LONG_BYTES_ITEM*? '\'\'\'' | '"""' LONG_BYTES_ITEM*? '"""';
fragment LONG_BYTES_ITEM: LONG_BYTES_CHAR | BYTES_ESCAPE_SEQ;
fragment SHORT_BYTES_CHAR_NO_SINGLE_QUOTE:
    [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0026]
    | [\u0028-\u005B]
    | [\u005D-\u007F]
;
fragment SHORT_BYTES_CHAR_NO_DOUBLE_QUOTE:
    [\u0000-\u0009]
    | [\u000B-\u000C]
    | [\u000E-\u0021]
    | [\u0023-\u005B]
    | [\u005D-\u007F]
;

fragment LONG_BYTES_CHAR: [\u0000-\u005B] | [\u005D-\u007F];
fragment BYTES_ESCAPE_SEQ: '\\' [\u0000-\u007F];

fragment SPACES: [ \t]+;
fragment COMMENT: '#' ~[\r\n\f]*;
fragment LINE_JOINING: '\\' SPACES? ( '\r'? '\n' | '\r' | '\f');

fragment UNICODE_OIDS: '\u1885' ..'\u1886' | '\u2118' | '\u212e' | '\u309b' ..'\u309c';
fragment UNICODE_OIDC: '\u00b7' | '\u0387' | '\u1369' ..'\u1371' | '\u19da';
fragment UNDERSCORE : '_';
fragment ID_START:
    UNDERSCORE
    | [\p{L}]
    | [\p{Nl}]
    //| [\p{Other_ID_Start}]
    | UNICODE_OIDS
;
fragment ID_CONTINUE:
    ID_START
    | [\p{Mn}]
    | [\p{Mc}]
    | [\p{Nd}]
    | [\p{Pc}]
    //| [\p{Other_ID_Continue}]
    | UNICODE_OIDC
;
