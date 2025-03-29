Automatically generated from `Language.md`. Do not edit.
<start> ::= <fandango>
<fandango> ::= <statement>*
<statement> ::= <newline> | <production> | <constraint> | <comment> | <python>
<newline> ::= (('\r'? '\n' | '\r' | '\f') ' '?) := '\n'
<_> ::= r'[ \t]'* := ' '
<comment> ::= <_>{2} '#' <_> r'[^\r\n\f]'* <newline>
<production> ::= (
    <nonterminal> <_> '::=' <_> <alternatives>
    (<_> ':=' <_> <python_expression>)?
    <comment>? <_> (';' | <newline>))
<nonterminal> ::= '<' <name> '>'
<name> ::= <id_start> <id_continue>*
<id_start> ::= <uppercase_letter> | '_'
<id_continue> ::= (<uppercase_letter>
    | <lowercase_letter>
    | <digit>
    | '_')
<uppercase_letter> ::= r'[A-Z]'
<lowercase_letter> ::= r'[a-z]'
<digit> ::= r'[0-9]'
<alternatives> ::= <concatenation> (<_> '|' <_> <concatenation>)*
<concatenation> ::= <operator> (<_> <operator>)*
<operator> ::= <symbol> | <kleene> | <plus> | <option> | <repeat>
<symbol> ::= (
      <nonterminal>
    | <string_literal>
    | <bytes_literal>
    | <number>
    | <generator_call>
    | '(' <alternatives> ')'
    )
<kleene> ::= <symbol> '*'
<plus>  ::= <symbol> '+'
<option> ::= <symbol> '?'
<repeat> ::= (
     <symbol> '{' <python_expression> '}'
   | <symbol> '{' <python_expression>? ',' <python_expression>? '}')
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
<generator_call> ::= (<name>
    | <generator_call> '.' <name>
    | <generator_call> '[' <python_slices> ']'
    | <generator_call> <python_genexp>
    | <generator_call> '(' <python_arguments>? ')')
<constraint> ::= 'where ' <python_expression> <comment>? (';' | <newline>)
<python> ::= 'pass' <newline>
<python_slices> ::= '0:1'
<python_arguments> ::= '1'
<python_expression> ::= '1'
<python_genexp> ::= '[for' <name> 'in' <name> ':' <python_expression> ']'
