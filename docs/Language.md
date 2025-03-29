---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

(sec:language)=
# Fandango Syntax and Semantics

```{code-cell}
import os

cmd = """
SOURCE="Language.md"
TARGET="fandango.fan"
(
    echo 'Automatically generated from `'"$SOURCE"'`. Do not edit.'
    sed -n '/^```python$/,/^```$/p' "$SOURCE" | grep -v '```'
) > "$TARGET"
"""
print(cmd)
os.system(cmd)
```

## General Structure

```python
<start> ::= <fandango>
<fandango> ::= <statement>*
<statement> ::= <newline> | <production> | <constraint> | <comment> | <python>
```


## Whitespace

```python
<newline> ::= (('\r'? '\n' | '\r' | '\f') ' '?) := '\n'
<_> ::= r'[ \t]'* := ' '
```

## Comments

```python
<comment> ::= <_>{2} '#' <_> r'[^\r\n\f]'* <newline>
```



## Grammars

```python
<production> ::= (
    <nonterminal> <_> '::=' <_> <alternatives>
    (<_> ':=' <_> <python_expression>)?
    <comment>? <_> (';' | <newline>))
```


## Nonterminals

```python
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
```

## Alternatives

```python
<alternatives> ::= <concatenation> (<_> '|' <_> <concatenation>)*
```

## Concatenations

```python
<concatenation> ::= <operator> (<_> <operator>)*
```

## Symbols and Operators

```python
<operator> ::= <symbol> | <kleene> | <plus> | <option> | <repeat>
```

```python
<symbol> ::= (
      <nonterminal>
    | <string_literal>
    | <bytes_literal>
    | <number>
    | <generator_call>
    | '(' <alternatives> ')'
    )
```

```python
<kleene> ::= <symbol> '*'
<plus>  ::= <symbol> '+'
<option> ::= <symbol> '?'
<repeat> ::= (
     <symbol> '{' <python_expression> '}'
   | <symbol> '{' <python_expression>? ',' <python_expression>? '}')
```


## Strings

```python
<string_literal> ::= (
      r'[rR]'
    | r'[uU]'
    | r'[fF]'
    | r'[fF][rR]'
    | r'[rR][fF]')? ( <short_string> | <long_string>)
```

```python
<short_string> ::= (
      "'" (<string_escape_seq> | r"[^\\\r\n\f']")* "'"
    | '"' (<string_escape_seq> | r'[^\\\r\n\f"]')* '"')
```

```python
<string_escape_seq> ::= '\\' r'.' | '\\' <newline>
```

```python
<long_string> ::= (
      "'''" <long_string_item>* "'''"
    | '"""' <long_string_item>* '"""')
<long_string_item> ::= <long_string_char> | <string_escape_seq>

<long_string_char> ::= r'[^\\]'
```



## Bytes

```python
<bytes_literal> ::= (
      r'[bB]'
    | r'[bB][rR]'
    | r'[rR][bB]') (<short_bytes> | <long_bytes>)
```

```python
<short_bytes> ::= (
      "'" (<short_bytes_char_no_single_quote> | <bytes_escape_seq>)* "'"
    | '"' ( <short_bytes_char_no_double_quote> | <bytes_escape_seq> )* '"')
```

```python
<bytes_escape_seq> ::= '\\' r'[\u0000-\u007F]'
```

```python
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
```

```python
<long_bytes> ::= (
      "'''" <long_bytes_item>* "'''"
    | '"""' <long_bytes_item>* '"""')
<long_bytes_item> ::= <long_bytes_char> | <bytes_escape_seq>

<long_bytes_char> ::= r'[\u0000-\u005B]' | r'[\u005D-\u007F]'
```


## Numbers

```python
<number> ::= <integer> | <float_number> | <imag_number>
```

```python
<integer> ::= <decimal_integer> | <oct_integer> | <hex_integer> | <bin_integer>
```

```python
<decimal_integer> ::= <non_zero_digit> <digit>* | '0'+
<non_zero_digit> ::= r'[1-9]'
<digit> ::= r'[0-9]'
```

```python
<oct_integer> ::= '0' r'[oO]' <oct_digit>+
<oct_digit> ::= r'[0-7]'

<hex_integer> ::= '0' r'[xX]' <hex_digit>+
<hex_digit> ::= r'[0-9a-fA-F]'

<bin_integer> ::= '0' r'[bB]' <bin_digit>+
<bin_digit> ::= r'[01]'
```

```python
<float_number> ::= <point_float> | <exponent_float>
<point_float> ::= <int_part>? <fraction> | <int_part> '.'
<exponent_float> ::= ( <int_part> | <point_float> ) <exponent>
<int_part> ::= <digit>+
<fraction> ::= '.' <digit>+
<exponent> ::= r'[eE]' r'[+-]'? <digit>+

<imag_number> ::= (<float_number> | <int_part>) r'[jJ]'
```


## Inline Generators

```python
<generator_call> ::= (<name>
    | <generator_call> '.' <name>
    | <generator_call> '[' <python_slices> ']'
    | <generator_call> <python_genexp>
    | <generator_call> '(' <python_arguments>? ')')
```

## Constraints

```python
<constraint> ::= 'where ' <python_expression> <comment>? (';' | <newline>)
```


## Python Code

```python
<python> ::= 'pass' <newline>
<python_slices> ::= '0:1'
<python_arguments> ::= '1'
<python_expression> ::= '1'
<python_genexp> ::= '[for' <name> 'in' <name> ':' <python_expression> ']'
```
