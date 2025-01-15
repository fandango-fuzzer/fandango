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

(sec:bits)=
# Bits and Bit Fields

Some binary inputs use individual _bits_ to specify contents.
For instance, you might have a `flag` byte that holds multiple (bit) flags:

```C
struct {
  unsigned int italic: 1;  // 1 bit
  unsigned int bold: 1;
  unsigned int underlined: 1;
  unsigned int strikethrough: 1;
  unsigned int brightness: 4;  // 4 bits
} format_flags;
```

How does one represent such _bit fields_ in a Fandango spec?


## Representing Bits

In Fandango, bits can be represented in Fandango using the special values `0` (for a zero bit) and `1` (for a non-zero bit).
Hence, you can define a `<bit>` value as

```python
<bit> ::= 0 | 1
```

With this, the above `format_flag` byte would be specified as

```{code-cell}
:tags: ["remove-input"]
!cat bits.fan
```

A `<format_flag>` symbol would thus always consist of these eight bits.
We can use the special option ``--format=bits`` to view the output as a bit stream:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 --start-symbol='<format_flag>'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 1 --start-symbol='<format_flag>'
assert _exit_code == 0
```

```{note}
The combination of `--format=bits` and `--start-symbol` is particularly useful to debug bit fields.
```

Internally, Fandango treats the individual flags as if they were strings - that is, `"\x00"` for zero bits and `"\x01"` for nonzero bits.
Hence, we can also apply _constraints_ to the individual flags:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 10 -c '<italic> == "\x01" and <bold> == "\x00"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 10 -c '<italic> == "\x01" and <bold> == "\x00"'
assert _exit_code == 0
```

This alternative, using `chr()` to generate a single byte out of the specified integer might be more readable:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 -c '<italic> == chr(1) and <bold> == chr(0)'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 1 -c '<italic> == chr(1) and <bold> == chr(0)'
assert _exit_code == 0
```

We can also easily set the value of the entire `format_flag` field using a constraint:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 -c '<format_flag> == chr(0b11110000)'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 1 -c '<format_flag> == chr(0b11110000)'
assert _exit_code == 0
```

Since Fandango strictly follows a "left-to-right" order - that is, the order in which bits and bytes are specified in the grammar, the most significant bit is stored first.
Thus, the order of bits in the `chr()` argument is identical to the order of bits in the produced output.

```{note}
Fandango always strictly follows a "left-to-right" order - that is, the order in which bits and bytes are specified in the grammar.
```

To convert a bit into a numerical value, applying the Python `ord()` function comes in handy.
Note that its argument (the symbol) must be converted into a string first:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 -c 'ord(str(<brightness>)) > 10'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 10 -c 'ord(str(<brightness>)) > 10'
assert _exit_code == 0
```

Note how the last four bits (the `<brightness>` field) always represent a number greater than ten.

```{warning}
When implementing a format, be sure to follow its conventions regarding

* _bit ordering_ (most or least significant bit first)
* _byte ordering_ (most or least significant byte first)
```

```{error}
Note that _parsing_ binary inputs (and hence mutating them) is not available yet.
```

## Bits and Padding

When generating binary inputs, you may need to adhere to specific _lengths_.
Such lengths are often enforced by _padding_ – that is, adding bits until the required length is achieved.
For instance, let us assume you have a field consisting of some bits.
However, the overall length of the field must be a multiple of eight to have it byte-aligned.
For such _padding_, define the field as

```
<field> ::= <bits> <padding>
<padding> ::= 0*
```

combined with a constraint

```
where len(<field>) % 8 == 0
```

Note that applied on derivation trees, `len()` always returns the number of child elements, not the string length; here, we use this to access the number of elements in `<field>`.

