parser grammar FandangoParser;

options {
    tokenVocab = FandangoLexer;
}

// start
fandango: program EOF;

program: NEWLINE* (statement NEWLINE*)*;

statement
    : production
    | constraint
    | python
    ;

// grammar part

production
    : nonterminal '::=' alternative (':=' expression)? (';' | NEWLINE | EOF)
    | nonterminal '::=' alternative ('=' expression)? (';' | NEWLINE | EOF)   // deprecated
    | nonterminal '::=' alternative (':' ':' expression)? (';' | NEWLINE | EOF)  // deprecated
    ;

alternative: concatenation ('|' concatenation)*;

concatenation: operator (operator)*;

operator
    : symbol
    | kleene
    | plus
    | option
    | repeat
    ;

kleene: symbol STAR;
plus  : symbol ADD;
option: symbol QUESTION;
repeat
    : symbol OPEN_BRACE (expression) CLOSE_BRACE
    | symbol OPEN_BRACE (expression)? COMMA (expression)? CLOSE_BRACE
    ;

symbol
    : NEWLINE*
        ( nonterminal_right
        | STRING
        | NUMBER  // for 0 and 1 bits
        | generator_call
        | char_set // deprecated
        | OPEN_PAREN alternative CLOSE_PAREN
        )
      NEWLINE*
    ;

nonterminal_right
    : '<' ((NAME ':')? NAME ':')? NAME '>'
    ;

nonterminal
    : '<' NAME '>'
    ;



generator_call
    : NAME
    | generator_call '.' NAME
    | generator_call '[' slices ']'
    | generator_call genexp
    | generator_call '(' arguments? ')'
    ;

char_set
    : OPEN_BRACK XOR? STRING CLOSE_BRACK
    ;

// constraint part
constraint
    : WHERE implies (';' | NEWLINE | EOF)
    | MINIMIZING expr (';' | NEWLINE | EOF)
    | MAXIMIZING expr (';' | NEWLINE | EOF)
    | implies ';' // deprecated
    ;

implies:
    NEWLINE*
    (
        quantifier ARROW implies // deprecated
        | quantifier
    )
    NEWLINE*
    ;

quantifier:
    NEWLINE*
    (
        FORALL nonterminal IN selector COLON quantifier
        | EXISTS nonterminal IN selector COLON quantifier
        | formula_disjunction
    )
    NEWLINE*
    ;

formula_disjunction:
    NEWLINE*
    (
        formula_conjunction (OR formula_conjunction)*
    )
    NEWLINE*
    ;

formula_conjunction:
    NEWLINE*
    (
        formula_atom (AND formula_atom)*
    )
    NEWLINE*
    ;

formula_atom
    :
    NEWLINE*
    (
        formula_comparison
        | OPEN_PAREN implies CLOSE_PAREN
        | expr
    )
    NEWLINE*
    ;

formula_comparison:
    expr (LESS_THAN | GREATER_THAN | EQUALS | GT_EQ | LT_EQ | NOT_EQ_1 | NOT_EQ_2) expr
    ;

expr:
    selector_length
    | inversion
    | inversion 'if' inversion 'else' inversion
    ;

selector_length
    : '|' selector '|'
    | selector
    ;

selector:
    selection
    | selector '.' selection
    | selector '..' selection
    ;

selection
    : base_selection
    | base_selection '[' rs_slices ']'
    | base_selection '{' rs_pairs '}'
    ;

base_selection
    : nonterminal
    | '(' selector ')'
    ;

rs_pairs
    : rs_pair (',' rs_pair)* ','?
    ;

rs_pair
    : '*' nonterminal (':' rs_slice)?
    ;

rs_slices
    : rs_slice (',' rs_slice)* ','?
    ;

rs_slice
    : NUMBER
    | NUMBER? ':' NUMBER?
    | NUMBER? ':' NUMBER? ':' NUMBER?
    ;

// python part

python
    : compound_stmt
    | simple_stmt
    // PYTHON_START (python_tag | NEWLINE)* PYTHON_END
    ;

python_tag:
    (NEWLINE* (stmt) NEWLINE*)
    ;

// STARTING RULES
// ==============

python_file
    : statements? EOF?
    ;

interactive
    : statement_newline
    ;

eval
    : expressions NEWLINE* EOF?
    ;

func_type
    : '(' type_expressions? ')' '->' expression NEWLINE* EOF?
    ;

// GENERAL STATEMENTS
// ==================

statements
    : (stmt | NEWLINE)+
    ;

stmt
    : compound_stmt
    | simple_stmts
    ;

statement_newline
    : compound_stmt NEWLINE
    | simple_stmts
    | NEWLINE
    ;

simple_stmts
    :  simple_stmt (';' simple_stmt)* ';'? (NEWLINE+ | NEWLINE* EOF)
    ;

simple_stmt
    : assignment
    | type_alias
    | star_expressions
    | return_stmt
    | import_stmt
    | raise_stmt
    | 'pass'
    | del_stmt
    | yield_stmt
    | assert_stmt
    | 'break'
    | 'continue'
    | global_stmt
    | nonlocal_stmt
    ;

compound_stmt
    : function_def
    | if_stmt
    | class_def
    | with_stmt
    | for_stmt
    | try_stmt
    | while_stmt
    | match_stmt
    ;

// SIMPLE STATEMENTS
// =================

assignment
    : NAME ':' expression ('=' annotated_rhs)?
    | ('(' single_target ')'
         | single_subscript_attribute_target) ':' expression ('=' annotated_rhs)?
    | (star_targets '=' )+ (yield_expr | star_expressions)
    | single_target augassign (yield_expr | star_expressions)
    ;

annotated_rhs
    : yield_expr
    | star_expressions
    ;

augassign
    : '+='
    | '-='
    | '*='
    | '@='
    | '/='
    | '%='
    | '&='
    | '|='
    | '^='
    | '<<='
    | '>>='
    | '**='
    | '//='
    ;

return_stmt
    : 'return' star_expressions?
    ;

raise_stmt
    : 'raise' expression ('from' expression)?
    | 'raise'
    ;

global_stmt
    : 'global' NAME (',' NAME)*
    ;

nonlocal_stmt
    : 'nonlocal' NAME (',' NAME)*
    ;

del_stmt
    : 'del' del_targets
    ;

yield_stmt
    : yield_expr
    ;

assert_stmt
    : 'assert' expression (',' expression)?
    ;

import_stmt
    : import_name
    | import_from
    ;

// Import statements
// -----------------

import_name
    : 'import' dotted_as_names
    ;

import_from
    : 'from' ('.' | '...')* dotted_name 'import' import_from_targets
    | 'from' ('.' | '...')+ 'import' import_from_targets
    ;

import_from_targets
    : '(' import_from_as_names ','? ')'
    | import_from_as_names
    | '*'
    ;

import_from_as_names
    : import_from_as_name (',' import_from_as_name)*
    ;

import_from_as_name
    : NAME ('as' NAME)?
    ;

dotted_as_names
    : dotted_as_name (',' dotted_as_name)*
    ;

dotted_as_name
    : dotted_name ('as' NAME)?
    ;

dotted_name
    : dotted_name '.' NAME
    | NAME
    ;

// COMPOUND STATEMENTS
// ===================

// Common elements
// ---------------

block
    : NEWLINE INDENT statements DEDENT
    | simple_stmts
    ;

decorators
    : ('@' named_expression NEWLINE)+
    ;

// Class definitions
// -----------------

class_def
    : decorators? class_def_raw
    ;

class_def_raw
    : 'class' NAME type_params? ('(' arguments? ')')? ':' block
    ;

// Function definitions
// --------------------

function_def
    : decorators? function_def_raw
    ;

function_def_raw
    : 'async'? 'def' NAME type_params? '(' params? ')' ('->' expression)? ':' func_type_comment? block
    ;

// Function parameters
// -------------------

params
    : parameters
    ;

parameters
    : slash_no_default param_no_default* param_with_default* star_etc?
    | slash_with_default param_with_default* star_etc?
    | param_no_default+ param_with_default* star_etc?
    | param_with_default+ star_etc?
    | star_etc
    ;

// Some duplication here because we can't write (',' | &')'),
// which is because we don't support empty alternatives (yet).

slash_no_default
    : param_no_default+ '/' ','?
    ;

slash_with_default
    : param_no_default* param_with_default+ '/' ','?
    ;

star_etc
    : '*' param_no_default param_maybe_default* kwds?
    | '*' param_no_default_star_annotation param_maybe_default* kwds?
    | '*' ',' param_maybe_default+ kwds?
    | kwds
    ;

kwds
    : '**' param_no_default
    ;

// One parameter.  This *includes* a following comma and type comment.
//
// There are three styles:
// - No default
// - With default
// - Maybe with default
//
// There are two alternative forms of each, to deal with type comments:
// - Ends in a comma followed by an optional type comment
// - No comma, optional type comment, must be followed by close paren
// The latter form is for a final parameter without trailing comma.
//

param_no_default
    : param ','
    | param
    ;

param_no_default_star_annotation
    : param_star_annotation ','
    | param_star_annotation
    ;

param_with_default
    : param default ','
    | param default
    ;

param_maybe_default
    : param default? ','
    | param default?
    ;

param
    : NAME annotation?
    ;

param_star_annotation
    : NAME star_annotation
    ;

annotation
    : ':' expression
    ;

star_annotation
    : ':' star_expression
    ;

default
    : '=' expression
    ;

// If statement
// ------------

if_stmt
    : 'if' named_expression ':' block elif_stmt
    | 'if' named_expression ':' block else_block?
    ;

elif_stmt
    : 'elif' named_expression ':' block elif_stmt
    | 'elif' named_expression ':' block else_block?
    ;

else_block
    : 'else' ':' block
    ;

// While statement
// ---------------

while_stmt
    : 'while' named_expression ':' block else_block?
    ;

// For statement
// -------------

for_stmt
    : 'for' star_targets 'in' star_expressions ':'  block else_block?
    | 'async' 'for' star_targets 'in' star_expressions ':'  block else_block?
    ;

// With statement
// --------------

with_stmt
    : 'with' '(' with_item (',' with_item)* ','? ')' ':' block
    | 'with' with_item (',' with_item)* ':'  block
    | 'async' 'with' '(' with_item (',' with_item)* ','? ')' ':' block
    | 'async' 'with' with_item (',' with_item)* ':'  block
    ;

with_item
    : expression 'as' star_target
    | expression
    ;

// Try statement
// -------------

try_stmt
    : 'try' ':' block finally_block
    | 'try' ':' block except_block+ else_block? finally_block?
    | 'try' ':' block except_star_block+ else_block? finally_block?
    ;


// Except statement
// ----------------

except_block
    : 'except' expression ('as' NAME)? ':' block
    | 'except' ':' block
    ;

except_star_block
    : 'except' '*' expression ('as' NAME)? ':' block
    ;

finally_block
    : 'finally' ':' block
    ;

// Match statement
// ---------------

match_stmt
    : 'match' subject_expr ':' NEWLINE INDENT case_block+ DEDENT
    ;

subject_expr
    : star_named_expression ',' star_named_expressions?
    | named_expression
    ;

case_block
    : 'case' patterns guard? ':' block
    ;

guard
    : 'if' named_expression
    ;

patterns
    : open_sequence_pattern
    | pattern
    ;

pattern
    : as_pattern
    | or_pattern
    ;

as_pattern
    : or_pattern 'as' pattern_capture_target
    ;

or_pattern
    : closed_pattern ('|' closed_pattern)*
    ;

closed_pattern
    : literal_pattern
    | capture_pattern
    | wildcard_pattern
    | value_pattern
    | group_pattern
    | sequence_pattern
    | mapping_pattern
    | class_pattern
    ;

// Literal patterns are used for equality and identity constraints
literal_pattern
    : signed_number
    | complex_number
    | strings
    | 'None'
    | 'True'
    | 'False'
    ;

// Literal expressions are used to restrict permitted mapping pattern keys
literal_expr
    : signed_number
    | complex_number
    | strings
    | 'None'
    | 'True'
    | 'False'
    ;

complex_number
    : signed_real_number '+' imaginary_number
    | signed_real_number '-' imaginary_number
    ;

signed_number
    : NUMBER
    | '-' NUMBER
    ;

signed_real_number
    : real_number
    | '-' real_number
    ;

real_number
    : NUMBER
    ;

imaginary_number
    : NUMBER
    ;

capture_pattern
    : pattern_capture_target
    ;

pattern_capture_target
    : NAME
    ;

wildcard_pattern
    : UNDERSCORE
    ;

value_pattern
    : attr
    ;

attr
    : name_or_attr '.' NAME
    ;

name_or_attr
    : name_or_attr '.' NAME
    | NAME
    ;

group_pattern
    : '(' pattern ')'
    ;

sequence_pattern
    : '[' maybe_sequence_pattern? ']'
    | '(' open_sequence_pattern? ')'
    ;

open_sequence_pattern
    : maybe_star_pattern ',' maybe_sequence_pattern?
    ;

maybe_sequence_pattern
    : maybe_star_pattern (',' maybe_star_pattern)* ','?
    ;

maybe_star_pattern
    : star_pattern
    | pattern
    ;

star_pattern
    : '*' pattern_capture_target
    | '*' wildcard_pattern
    ;

mapping_pattern
    : '{' '}'
    | '{' double_star_pattern ','? '}'
    | '{' items_pattern ',' double_star_pattern ','? '}'
    | '{' items_pattern ','? '}'
    ;

items_pattern
    : key_value_pattern (',' key_value_pattern)*
    ;

key_value_pattern
    : (literal_expr | attr) ':' pattern
    ;

double_star_pattern
    : '**' pattern_capture_target
    ;

class_pattern
    : name_or_attr '(' ')'
    | name_or_attr '(' positional_patterns ','? ')'
    | name_or_attr '(' keyword_patterns ','? ')'
    | name_or_attr '(' positional_patterns ',' keyword_patterns ','? ')'
    ;

positional_patterns
    : pattern (',' pattern)*
    ;

keyword_patterns
    : keyword_pattern (',' keyword_pattern)*
    ;

keyword_pattern
    : NAME '=' pattern
    ;

// Type statement
// ---------------

type_alias
    : 'type' NAME type_params? '=' expression
    ;

// Type parameter declaration
// --------------------------

type_params
    : '[' type_param_seq  ']'
    ;

type_param_seq
    : type_param (',' type_param)* ','?
    ;

type_param
    : NAME type_param_bound?
    | '*' NAME
    | '**' NAME
    ;

type_param_bound
    : ':' expression
    ;

// EXPRESSIONS
// -----------

expressions
    : expression (',' expression )* ','?
    ;

expression
    : disjunction 'if' disjunction 'else' expression
    | disjunction
    | lambdef
    ;

yield_expr
    : 'yield' 'from' expression
    | 'yield' star_expressions?
    ;

star_expressions
    : star_expression (',' star_expression )* ','?
    ;

star_expression
    : '*' bitwise_or
    | expression
    ;

star_named_expressions
    : star_named_expression (',' star_named_expression )* ','?
    ;

star_named_expression
    : '*' bitwise_or
    | named_expression
    ;

assignment_expression
    : NAME ':=' expression
    ;

named_expression
    : assignment_expression
    | expression
    ;

disjunction
    : conjunction ('or' conjunction )*
    ;

conjunction
    : inversion ('and' inversion )*
    ;

inversion
    : 'not' inversion
    | comparison
    ;

// Comparison operators
// --------------------

comparison
    : bitwise_or compare_op_bitwise_or_pair*
    ;

compare_op_bitwise_or_pair
    : eq_bitwise_or
    | noteq_bitwise_or
    | lte_bitwise_or
    | lt_bitwise_or
    | gte_bitwise_or
    | gt_bitwise_or
    | notin_bitwise_or
    | in_bitwise_or
    | isnot_bitwise_or
    | is_bitwise_or
    ;

eq_bitwise_or
    : '==' bitwise_or
    ;

noteq_bitwise_or
    : '!=' bitwise_or
    ;

lte_bitwise_or
    : '<=' bitwise_or
    ;

lt_bitwise_or
    : '<' bitwise_or
    ;

gte_bitwise_or
    : '>=' bitwise_or
    ;

gt_bitwise_or
    : '>' bitwise_or
    ;

notin_bitwise_or
    : 'not' 'in' bitwise_or
    ;

in_bitwise_or
    : 'in' bitwise_or
    ;

isnot_bitwise_or
    : 'is' 'not' bitwise_or
    ;

is_bitwise_or
    : 'is' bitwise_or
    ;

// Bitwise operators
// -----------------

bitwise_or
    : bitwise_or '|' bitwise_xor
    | bitwise_xor
    ;

bitwise_xor
    : bitwise_xor '^' bitwise_and
    | bitwise_and
    ;

bitwise_and
    : bitwise_and '&' shift_expr
    | shift_expr
    ;

shift_expr
    : shift_expr '<<' sum
    | shift_expr '>>' sum
    | sum
    ;

// Arithmetic operators
// --------------------

sum
    : sum '+' term
    | sum '-' term
    | term
    ;

term
    : term '*' factor
    | term '/' factor
    | term '//' factor
    | term '%' factor
    | term '@' factor
    | factor
    ;

factor
    : '+' factor
    | '-' factor
    | '~' factor
    | power
    ;

power
    : await_primary '**' factor
    | await_primary
    ;

// Primary elements
// ----------------

// Primary elements are things like "obj.something.something", "obj[something]", "obj(something)", "obj" ...

await_primary
    : 'await' primary
    | primary
    ;

primary
    : primary '.' NAME
    | primary genexp
    | primary '(' arguments? ')'
    | primary '[' slices ']'
    | atom
    ;

slices
    : (slice | starred_expression) (',' (slice | starred_expression))* ','?
    ;

slice
    : expression? ':' expression? (':' expression?)?
    | named_expression
    ;

atom
    : selector_length
    | NAME
    | 'True'
    | 'False'
    | 'None'
    | strings
    | NUMBER
    | (tuple | group | genexp)
    | (list | listcomp)
    | (dict | set | dictcomp | setcomp)
    | '...'
    ;

group
    : '(' (yield_expr | named_expression) ')'
    ;

// Lambda functions
// ----------------

lambdef
    : 'lambda' lambda_params? ':' expression
    ;

lambda_params
    : lambda_parameters
    ;

// lambda_parameters etc. duplicates parameters but without annotations
// or type comments, and if there's no comma after a parameter, we expect
// a colon, not a close parenthesis.  (For more, see parameters above.)
//
lambda_parameters
    : lambda_slash_no_default lambda_param_no_default* lambda_param_with_default* lambda_star_etc?
    | lambda_slash_with_default lambda_param_with_default* lambda_star_etc?
    | lambda_param_no_default+ lambda_param_with_default* lambda_star_etc?
    | lambda_param_with_default+ lambda_star_etc?
    | lambda_star_etc
    ;

lambda_slash_no_default
    : lambda_param_no_default+ '/' ','?
    ;

lambda_slash_with_default
    : lambda_param_no_default* lambda_param_with_default+ '/' ','?
    ;

lambda_star_etc
    : '*' lambda_param_no_default lambda_param_maybe_default* lambda_kwds?
    | '*' ',' lambda_param_maybe_default+ lambda_kwds?
    | lambda_kwds
    ;

lambda_kwds
    : '**' lambda_param_no_default
    ;

lambda_param_no_default
    : lambda_param ','?
    ;

lambda_param_with_default
    : lambda_param default ','?
    ;

lambda_param_maybe_default
    : lambda_param default? ','?
    ;

lambda_param
    : NAME
    ;

// LITERALS
// ========

fstring_middle
    : fstring_replacement_field
    | FSTRING_MIDDLE
    ;

fstring_replacement_field
    : '{' (yield_expr | star_expressions) '='? fstring_conversion? fstring_full_format_spec? '}'
    ;

fstring_conversion:
    | '!' NAME
    ;

fstring_full_format_spec
    : ':' fstring_format_spec*
    ;

fstring_format_spec
    : FSTRING_MIDDLE
    | fstring_replacement_field
    ;

fstring
    : FSTRING_START fstring_middle* FSTRING_END
    ;

string
    : STRING
    ;

strings
    : (fstring | string)+
    ;

list
    : '[' star_named_expressions? ']'
    ;

tuple
    : '(' (star_named_expression ',' (star_named_expressions))? ')'
    ;

set
    : '{' star_named_expressions '}'
    ;

// Dicts
// -----

dict
    : '{' double_starred_kvpairs? '}'
    ;

double_starred_kvpairs
    : double_starred_kvpair (',' double_starred_kvpair)* ','?
    ;

double_starred_kvpair
    : '**' bitwise_or
    | kvpair
    ;

kvpair
    : expression ':' expression
    ;

// Comprehensions & Generators
// ---------------------------

for_if_clauses
    : for_if_clause+
    ;

for_if_clause
    : 'async'? 'for' star_targets 'in' disjunction ('if' disjunction)*
    ;

listcomp
    : '[' named_expression for_if_clauses ']'
    ;

setcomp
    : '{' named_expression for_if_clauses '}'
    ;

genexp
    : '(' (assignment_expression | expression) for_if_clauses ')'
    ;

dictcomp
    : '{' kvpair for_if_clauses '}'
    ;

// FUNCTION CALL ARGUMENTS
// =======================

arguments
    : args ','?
    ;

args
    : arg (',' arg)* (',' kwargs)?
    | kwargs
    ;

arg
    : starred_expression
    | assignment_expression
    | expression
    ;

kwargs
    : kwarg_or_starred (',' kwarg_or_starred)* ',' kwarg_or_double_starred (',' kwarg_or_double_starred)*
    | kwarg_or_starred (',' kwarg_or_starred)*
    | kwarg_or_double_starred (',' kwarg_or_double_starred)*
    ;

starred_expression
    : '*' expression
    ;

kwarg_or_starred
    : NAME '=' expression
    | starred_expression
    ;

kwarg_or_double_starred
    : NAME '=' expression
    | '**' expression
    ;

// ASSIGNMENT TARGETS
// ==================

// Generic targets
// ---------------

// NOTE: star_targets may contain *bitwise_or, targets may not.
star_targets
    : star_target (',' star_target )* ','?
    ;

star_targets_list_seq
    : star_target (',' star_target )* ','?
    ;

star_targets_tuple_seq
    : star_target (',' star_target )+ ','?
    | star_target ','
    ;

star_target
    : '*' star_target
    | target_with_star_atom
    ;

target_with_star_atom
    : t_primary '.' NAME
    | t_primary '[' slices ']'
    | star_atom
    ;

star_atom
    : NAME
    | '(' target_with_star_atom ')'
    | '(' star_targets_tuple_seq? ')'
    | '[' star_targets_list_seq? ']'
    ;

single_target
    : single_subscript_attribute_target
    | NAME
    | '(' single_target ')'
    ;

single_subscript_attribute_target
    : t_primary '.' NAME
    | t_primary '[' slices ']'
    ;

t_primary
    : t_primary '.' NAME
    | t_primary '[' slices ']'
    | t_primary genexp
    | t_primary '(' arguments? ')'
    | atom
    ;

// Targets for del statements
// --------------------------

del_targets
    : del_target (',' del_target)* ','?
    ;

del_target
    : t_primary '.' NAME
    | t_primary '[' slices ']'
    | del_t_atom
    ;

del_t_atom
    : NAME
    | '(' del_targets? ')'
    | '[' del_targets? ']'
    ;

// TYPING ELEMENTS
// ---------------

// type_expressions allow */** but ignore them
type_expressions
    : expression (',' expression)* ',' '*' expression ',' '**' expression
    | expression (',' expression)* ',' '*' expression
    | expression (',' expression)* ',' '**' expression
    | '*' expression ',' '**' expression
    | '*' expression
    | '**' expression
    | expression (',' expression)*
    ;

func_type_comment
    : NEWLINE
    ;

// ========================= END OF THE GRAMMAR ===========================