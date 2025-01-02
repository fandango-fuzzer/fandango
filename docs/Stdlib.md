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

(sec:stdlib)=
# Fandango Standard Library

Fandango provides a set of predefined grammar symbols.
Each symbol is defined as

* `<_SYMBOL>` (with the actual "official" definition), and
* `<SYMBOL>` (defined as `<_SYMBOL>` by default; can be overridden in individual specifications)

If you'd like to narrow the definition of, say, punctuation characters, you can redefine `<punctuation>` to your liking:

```
<punctuation> ::= '!' | '?' | ',' | '.' | ';' | ':';
```

The original definition of `<_punctuation>`, however, must not be changed, as other definitions may depend on it.

```{warning}
Symbols starting with an underscore must _not_ be redefined.
```


```{code-cell}
:tags: ["remove-input"]
from fandango.language import stdlib
```

## Printable Characters

These symbols mimic the [string constants from the Python `string` module](https://docs.python.org/3/library/string.html).
Use `<digit>`, `<ascii_letter>`, `<whitespace>`, and more to your liking.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.printable)
```

## ASCII Characters

`<ascii_char>` expands into all 7-bit characters in the ASCII range 0x00-0x7F, printable and non-printable.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.ascii_char)
```


## ASCII Control Characters

`<ascii_control>` expands into any of the ASCII control characters 0x00-0x1F and 0x7F.
We also provide ASCII codes such as `<ESC>`, `<LF>`, or `<NUL>`.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.ascii_control)
```


## Bits

A `<bit>` represents a bit of 0 or 1.
Use `<bit>{N}` to specify a sequence of `N` bits.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.bits)
```

## Bytes

A `<byte>` is any byte 0x00-0xFF.
During parsing and production, it will always be interpreted as a single byte.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.bytes)
```


## Characters

A `<char>` is any Unicode character.

```{error}
`<char>` is currently not defined.
Use `<ascii_char>`, `<byte>`, or `<utf8_char>` instead.
```
% We need charset or regex specs for this: <char> ::= /./ | '\n'


## UTF-8 characters

A `<utf8_char>` is a UTF-8 encoding of a character, occupying one (`<utf8_char1>`) to four (`<utf8_char4`) bytes.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.utf8)
```

## Binary Numbers

For binary representations of numbers, use symbols such as `<int8>` (8 bits) or `<int32>` (32 bits).
Note that these symbols only specify the _length_; they do not cover signs, endianness, or byte ordering.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.numbers)
```

## Fandango Dancer

The `<fandango-dancer>` symbol is used to test UTF-8 compatibility.

```{code-cell}
:tags: ["remove-input"]
print(stdlib.dancer)
```
