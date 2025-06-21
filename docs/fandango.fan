# Automatically generated from `Language.md`. Do not edit.


# Fandango Language Reference

# This chapter specifies the exact syntax (and semantics) of Fandango specifications (`.fan` files).

## General Structure

# We specify the Fandango syntax in form of a Fandango specification.

# A `.fan` Fandango specification file consists of

# * [_grammar productions_](sec:grammar) (`<production>`)
# * [_constraints_](sec:constraint) (`<constraint>`)
# * [_Python code_](sec:code) (`<python_statement>`).

<start> ::= <fandango>
<fandango> ::= <statement>*
<statement> ::= <production> | <constraint> | <python_statement> | <newline> | <comment>


## Whitespace

# Besides grammar productions, constraints, and code, a `.fan` file can contain _newlines_ (`<newline>`) and _whitespace_ (`<_>`).

# :::{margin}
# The _generators_ (`:= '\n'` and `:= ' '`) specify useful default values when fuzzing.
# :::

<newline> ::= ('\r'? '\n' | '\r' | '\f') := '\n'
<_> ::= r'[ \t]*' := ' '

## Physical and Logical Lines

# [As in Python](https://docs.python.org/3/reference/lexical_analysis.html#explicit-line-joining), one can join two physical lines into a logical by adding a backslash `\` at the end of the first line.
# For example:

# <element> := <a_very_long_line> \
#     <continued_on_the_next_line>

# [As in Python](https://docs.python.org/3/reference/lexical_analysis.html#implicit-line-joining), expressions in parentheses can be split over more than one physical line without using backslashes.
# For example:

# <element> := (<an_alternative> |
#               <another_alternative>)

# Grammar rules can be indented; this has no effect on semantics.


## Comments

# Comments are as in Python; they are introduced by a `#` character and continue until the end of the line.
# By convention, there are two spaces in front of the `#` and one space after.

<comment> ::= <_>{2} '#' <_> r'[^\r\n\f]'* <newline>

# For example:

# <element> := <another_element>    # a comment

# Extending beyond this grammar, the actual implementation allows a comment at any end of a line.



## Grammars

# A _grammar_ is a set of _productions_.
# Each production defines a [_nonterminal_](sec:nonterminal) followed by `::=` and a number of [_alternatives_](sec:alternatives).

# An optional [_generator_](sec:generator) can define a Python function to produce a value during fuzzing.

# Productions end with a _newline_ or a _`;` character_.

<production> ::= (
    <nonterminal> <_> '::=' <_> <alternatives> 
    <generator>? <comment>? (';' | <newline>))

## Nonterminals

# A _nonterminal_ is a Python identifier enclosed in angle brackets `<...>`.
# It starts with a letter (regular expression `\w`) or an underscore (`_`), followed by more letters, digits (regular expression `\d`), or underscores.

<nonterminal> ::= '<' <name> '>'
<name> ::= r'(\w|_)(\w|\d|_)*'

# Like Python, Fandango allows all Unicode letters and digits in identifiers.

# For portability, we recommend to use only ASCII letters `a`..`z`, `A`..`Z`, digits `0`..`9`, and underscores `_` in identifiers.



## Alternatives

# The _alternatives_ part of a production rule defines possible [expansions](sec:concatenation) (`<concatenation>`) for a nonterminal, separated by `|`.

<alternatives> ::= <concatenation> (<_> '|' <_> <concatenation>)*

## Concatenations

# A _concatenation_ is a sequence of individual [operators](sec:operator) (typically symbols such as strings).

<concatenation> ::= <operator> (<_> <operator>)*


## Symbols and Operators

# An operator is a _symbol_ (`<symbol>`), followed by an optional [repetition](sec:repeat) operator.

<operator> ::= <symbol> | <kleene> | <plus> | <option> | <repeat>

# A symbol can be a [_nonterminal_](sec:nonterminal), a [string](sec:strings) or [bytes](sec:bytes) _literal_, a [_number_](sec:number) (for bits), a [_generator call_](sec:generator), or
# (parenthesized) [alternatives](sec:alternatives).

<symbol> ::= (
      <nonterminal>
    | <string_literal>
    | <bytes_literal>
    | <number>
    | <generator_call>
    | '(' <alternatives> ')'
    )

## Repetitions

# Any symbol can be followed by a repetition specification.
# The syntax `{N,M}` stands for a number of repetitions from `N` to `M`.
# For example, `<a>{3,5}` will match from 3 to 5 `<a>` symbols.

# Both `N` and `M` can be omitted:

# * Omitting `N` creates a lower bound of zero.
# * Omitting `M` creates an infinite upper bound (i.e, any number of repetitions).
# * The comma may not be omitted, as this would create confusion with `{N}` (see below).

# In Fandango, the number of repetitions is limited.
# Use the `--max-repetitions M` flag to change the limit.

# Fandango supports a number of abbreviations for repetitions:

# * The form `{N}` stands for `{N, N}` (exactly `N` repetitions)
# * The form `*` stands for `{0,}` (zero or more repetitions)
# * The form `+` stands for `{1,}` (one or more repetitions)
# * The form `?` stands for `{0,1}` (an optional element)

<kleene> ::= <symbol> '*'
<plus>  ::= <symbol> '+'
<option> ::= <symbol> '?'
<repeat> ::= (
     <symbol> '{' <python_expression> '}'
   | <symbol> '{' <python_expression>? ',' <python_expression>? '}')


## String Literals

# Fandango supports the full [Python syntax for string literals](https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals):

# * Short strings are enclosed in single (`'...'`) or double (`"..."`) quotes
# * Long strings are enclosed in triple quotes (`'''...'''` and `"""..."""`)
# * One can use [escape sequences](https://docs.python.org/3/reference/lexical_analysis.html#escape-sequences) (`\n`) to express special characters

# Fandango interprets Python _raw strings_ (using an `r` prefix, as in `r'foo'`) as _regular expressions_.
# During parsing, these are matched against the input; during fuzzing, they are instantiated into a matching string.

<string_literal> ::= (
      r'[rR]'
    | r'[uU]'
    | r'[fF]'
    | r'[fF][rR]'
    | r'[rR][fF]')? ( <short_string> | <long_string>)

<short_string> ::= (
      "'" (<string_escape_seq> | r"[^\\\r\n\f']")* "'"
    | '"' (<string_escape_seq> | r'[^\\\r\n\f"]')* '"')

<string_escape_seq> ::= '\\' r'.' | '\\' <newline>

<long_string> ::= (
      "'''" <long_string_item>* "'''"
    | '"""' <long_string_item>* '"""')

<long_string_item> ::= <long_string_char> | <string_escape_seq>
<long_string_char> ::= r'[^\\]'


## Byte Literals

# Byte literals (a string prefixed with `b`) are interpreted as in Python; the [rules for strings](sec:strings) apply as well.

# * If a grammar can produce bytes (or [bits](sec:number)), the associated files will be read and written in `binary` mode, reading and writing _bytes_ instead of (encoded) characters.
# * If the grammar contains bytes _and_ strings, then strings will be written in UTF-8 encoding into the binary file.
# * See the [section on binary files](sec:binary) for more details.

<bytes_literal> ::= (
      r'[bB]'
    | r'[bB][rR]'
    | r'[rR][bB]') (<short_bytes> | <long_bytes>)

<short_bytes> ::= (
      "'" (<short_bytes_char_no_single_quote> | <bytes_escape_seq>)* "'"
    | '"' ( <short_bytes_char_no_double_quote> | <bytes_escape_seq> )* '"')

<bytes_escape_seq> ::= '\\' r'[\u0000-\u007F]'

<short_bytes_char_no_single_quote> ::= (
      r'[\u0000-\u0009]'
    | r'[\u000B-\u000C]'
    | r'[\u000E-\u0026]'
    | r'[\u0028-\u005B]'
    | r'[\u005D-\u007F]')

<short_bytes_char_no_double_quote> ::= (
      r'[\u0000-\u0009]'
    | r'[\u000B-\u000C]'
    | r'[\u000E-\u0021]'
    | r'[\u0023-\u005B]'
    | r'[\u005D-\u007F]')

<long_bytes> ::= (
      "'''" <long_bytes_item>* "'''"
    | '"""' <long_bytes_item>* '"""')

<long_bytes_item> ::= <long_bytes_char> | <bytes_escape_seq>
<long_bytes_char> ::= r'[\u0000-\u005B]' | r'[\u005D-\u007F]'

## Numbers

# Grammars can contain _numbers_, which are interpreted as [_bits_](sec:bits).
# While the Fandango grammar supports arbitrary numbers, only the number literals `0` and `1` are supported (possibly with repetitions).

<number> ::= <integer> | <float_number> | <imag_number>

<integer> ::= <decimal_integer> | <oct_integer> | <hex_integer> | <bin_integer>

<decimal_integer> ::= <non_zero_digit> <digit>* | '0'+
<non_zero_digit> ::= r'[1-9]'
<digit> ::= r'[0-9]'

<oct_integer> ::= '0' r'[oO]' <oct_digit>+
<oct_digit> ::= r'[0-7]'

<hex_integer> ::= '0' r'[xX]' <hex_digit>+
<hex_digit> ::= r'[0-9a-fA-F]'

<bin_integer> ::= '0' r'[bB]' <bin_digit>+
<bin_digit> ::= r'[01]'

<float_number> ::= <point_float> | <exponent_float>
<point_float> ::= <int_part>? <fraction> | <int_part> '.'
<exponent_float> ::= ( <int_part> | <point_float> ) <exponent>
<int_part> ::= <digit>+
<fraction> ::= '.' <digit>+
<exponent> ::= r'[eE]' r'[+-]'? <digit>+

<imag_number> ::= (<float_number> | <int_part>) r'[jJ]'


## Generators

# A _generator_ is an expression that is evaluated during fuzzing to produce a value, which is then _parsed_ into the given nonterminal.
# See [the section on generators](sec:generators) for details.
# It is added at the end of a production rule, separated by `:=`.

<generator> ::= <_> ':=' <_> <python_expression>

# Future Fandango versions will also support invoking a generator as if it were a symbol.

<generator_call> ::= (<name>
    | <generator_call> '.' <name>
    | <generator_call> '[' <python_slices> ']'
    | <generator_call> <python_genexp>
    | <generator_call> '(' <python_arguments>? ')')

## Constraints

# A _constraint_ is a Python expression that is to be satisfied during fuzzing and parsing.
# It is introduced by the keyword `where`.

# Constraints typically contain [_symbols_](sec:selector) (`<...>`); these are allowed wherever values are allowed.
# The constraint has to hold for all values of the given symbols.

# Symbols in constraints have a `DerivationTree` type; see the [Derivation Tree Reference](sec:derivation-tree) for details.

<constraint> ::= 'where' <_> <python_expression> <comment>? (';' | <newline>)

## Selectors

# Symbols in constraints can take the following special forms:

# * `<A>.<B>`: The constraint has to hold for all elements `<B>` that are a direct child of `<A>`
# * `<A>..<B>`: The constraint has to hold for all elements `<B>` that are a direct or indirect child of `<A>`

# For details, see [the section on derivation trees](sec:derivation-tree).

<selector> ::= (
      <selection>
    | <selector> '.' <selection>
    | <selector> '..' <selection>)

# The `[...]` operator allows accessing individual children of a derivation tree:

<selection> ::= <base_selection> | <base_selection> '[' <python_slices> ']'

# These operators can be combined and parenthesized:

<base_selection> ::= <nonterminal> | '(' <selector> ')'

## Python Code

# In a `.fan` file, anything that is neither a [grammar production rule](sec:grammar) nor a [constraint](sec:constraint) is interpreted as _Python code_, parsed as `<statement>` in the [official Python grammar](https://docs.python.org/3/reference/grammar.html).

# Also, in the above spec, any nonterminal in the form `<python_NAME>` (say, `<python_expression>`) refers to `<NAME>` (say, `<expression>`) in the [official Python grammar](https://docs.python.org/3/reference/grammar.html).

# For more details on Python syntax and semantics, consult the [Python language reference](https://docs.python.org/3/reference/index.html).


## The Full Spec


# You can access the above spec [`fandango.fan`](fandango.fan) for reference.

# `fandango.fan` is sufficient for parsing `.fan` input without Python expressions or code:

# $ echo '<start> ::= "a" | "b" | "c"' | fandango parse -f fandango.fan -o -


# To complete the grammar, `fandango.fan` provides placeholders for included Python elements:

<python_statement> ::= 'pass' <newline>
<python_slices> ::= '0:1'
<python_arguments> ::= '1'
<python_expression> ::= '1' | <selector>
<python_genexp> ::= '[for' <_> <name> <_> 'in' <_> <name> ':' <_> <python_expression> ']'

# Hence, it is also possible to produce Fandango specs (with set Python code) using `fandango.fan`.
# Hence, Fandango can be fuzzed with itself:

# $ fandango fuzz -f fandango.fan -n 1


# Note that such generated files satisfy the Fandango syntax, but not its _semantics_.
# For instance, one would have to add extra constraints such that all used nonterminals are defined.

