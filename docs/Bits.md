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
!fandango fuzz --format=bits -f bits.fan -n 1 --start-symbol='<format_flag>' --validate
assert _exit_code == 0
```

```{tip}
The combination of `--format=bits` and `--start-symbol` is particularly useful to debug bit fields.
```

Internally, Fandango treats individual flags as integers, too.
Hence, we can also apply _constraints_ to the individual flags.
For instance, we can profit from the fact that Python treats `0` as False and `1` as True:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 10 -c '<italic> and <bold>'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 10 -c '<italic> and <bold>' --validate
assert _exit_code == 0
```

Fandango strictly follows a "left-to-right" order - that is, the order in which bits and bytes are specified in the grammar, the most significant bit is stored first.

Hence, we can also easily set the value of the entire `brightness` field using a constraint:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 -c '<brightness> == 0b1111'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 1 -c '<brightness> == 0b1111' --validate
assert _exit_code == 0
```

```{note}
Fandango always strictly follows a "left-to-right" order - that is, the order in which bits and bytes are specified in the grammar.
```

Of course, we can also give the number in decimal format:

```shell
$ fandango fuzz --format=bits -f bits.fan -n 1 -c '<brightness> == 15'
```

% TODO: This does not work with <format_flag> :-(
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --format=bits -f bits.fan -n 10 -c '<brightness> == 15' --validate --population-size=20
assert _exit_code == 0
```

Note how the last four bits (the `<brightness>` field) are always set to `1111` - the number 15.

```{important}
When implementing a format, be sure to follow its conventions regarding

* _bit ordering_ (most or least significant bit first)
* _byte ordering_ (most or least significant byte first)
```


## Parsing Bits

Fandango also supports [parsing](sec:parsing) inputs with bits.
This is what happens if we send a byte `\xf0` (the upper four bits set) to the parser:

```shell
$ printf "\xf0" | fandango parse -f bits.fan -o - --format=bits
```

```{code-cell}
:tags: ["remove-input"]
!printf "\xf0" | fandango parse -f bits.fan -o - --format=bits --validate
assert _exit_code == 0
```

We see that the input was properly parsed and decomposed into individual bits.

This is the resulting parse tree:

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree
tree = Tree('<start>', Tree('<format_flag>',
  Tree('<italic>', Tree('<bit>', Tree(1))),
  Tree('<bold>', Tree('<bit>', Tree(1))),
  Tree('<underlined>', Tree('<bit>', Tree(1))),
  Tree('<strikethrough>', Tree('<bit>', Tree(1))),
  Tree('<brightness>',
    Tree('<bit>', Tree(0)),
    Tree('<bit>', Tree(0)),
    Tree('<bit>', Tree(0)),
    Tree('<bit>', Tree(0))
  )
))
tree.visualize()
```

The `grammar` format shows us that the values are properly assigned:

```shell
$ printf '\xf0' | fandango parse -f bits.fan -o - --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
!printf '\xf0' | fandango parse -f bits.fan -o - --format=grammar --validate
assert _exit_code == 0
```

```{note}
To parse bits properly, they must come in multiples of eight.
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

