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

(sec:binary)=
# Generating Binary Inputs

Creating _binary_ inputs with Fandango is a bit more challenging than creating human-readable inputs.
This is because they have a few special features, such as _checksums_ and _length encodings_.
Fortunately, we can address all of them with dedicated constraints.

## Checksums

:::{margin}
Strictly speaking, this only holds for context-free grammars Fandango uses.
_Context-sensitive_ and _universal_ grammars can perform arithmetic computations, but someone would have to implement them all.
:::

Our first challenge is _checksums_.
Binary input formats frequently use checksums to ensure integrity.
The problem is that checksums cannot be expressed in a grammar alone, as grammars lack the arithmetic functions required to compute and check checksums.
In Fandango, though, we can express the computation of a checksum in a dedicated function, which is then used in a dedicated constraint.

As an example for checksums, let's have a look at _credit card numbers_.
These are definitely very human-readable and not binary at all, but for an example, they will do fine.
A credit card number consists of a series of digits, where the last one is a _check digit_.
Here is a grammar that expresses the structure for 16-digit credit card numbers:

```{code-cell}
:tags: ["remove-input"]
# show grammar except '<byte>'
!grep '::=' credit_card.fan | grep -v '^<byte>'
```

All credit cards use [Luhn's algorithm](https://en.wikipedia.org/wiki/Luhn_algorithm) to compute the check digit.
Here is an implementation, adapted from the [Faker library](https://github.com/joke2k/faker/blob/master/faker/providers/credit_card/__init__.py#L99).
The function `credit_card_check_digit()` gets all numbers of a credit card (except the last digit) and returns the computed check digit.

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v ';' credit_card.fan
```

% ```{code-cell}
% from faker import Faker
% from faker.providers import credit_card
%
% fake = Faker()
% for _ in range(100):
%     num = fake.credit_card_number()
%     check_digit = credit_card_check_digit(num[:-1])
%     assert check_digit == num[-1], f"got check digit {check_digit} for {num}, expected {num[-1]}"
% ```

We can easily make use of `credit_card_check_digit()` in the constraint that ties `<check_digit>` and `<number>`:

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep ';$' credit_card.fan | grep -v '::='
```

All of this can go into a single `.fan` file: [`credit_card.fan`](credit_card.fan) joins the above grammar, the `credit_card_check_digit()` definition, and the above constraint into a single file.

:::{margin}
Do not use such numbers to test third-party systems.
:::

We can now use `credit-card.fan` to produce valid credit card numbers:

```shell
$ fandango fuzz -f credit_card.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f credit_card.fan -n 10
```

And we can also use it to _parse_ and _check_ numbers.

% TODO
:::{error}
Parsing functionality is not yet available on the command line.
:::

:::{margin}
You can also simply do an Internet search for a Python implementation of the respective algorithm.
Or ask your favorite AI assistant.
:::

Similarly, you can define any kind of checksum function and then use it in a constraint.
In Python, it is likely that someone has already implemented the specific checksum function, so you can also _import_ it:

* [The `hashlib` module](https://docs.python.org/3/library/hashlib.html) provides hash functions such as MD5 or SHA-256.
* [The `binascii` module](https://docs.python.org/3/library/binascii.html) offers CRC checks.
* [The `zlib` module](https://docs.python.org/3/library/zlib.html) provides CRC32 and ADLER32 checks used in zip files.

## Length Encodings

The second set of features one frequently encounters in binary formats is _length encodings_ - that is, a particular field holds a value that represents the length of one or more fields that follow.
Here is a simple grammar that expresses this characteristic: A `<field>` has a two-byte length, followed by the actual content (of length `<length>`).

% This is how I got the `<byte>` definition in `binary.fan` -- AZ

```{code-cell}
:tags: ["remove-input", "remove-output"]
import string
for i in range(0, 256):
    c = chr(i)
    if c in string.printable:
        print(repr(c), end=" | ")
    else:
        print(f"'\\x{i:02x}'", end=" | ")
```

```{code-cell}
:tags: ["remove-input"]
# show grammar except '<byte>'
!grep '::=' binary.fan | grep -v '^<byte>'
```

The relationship between `<length>` and `<content>` can again be expressed using a constraint.
We assume that `<length>` comes as a two-byte (16-bit) unsigned integer with _little-endian_ encoding - that is, the low byte comes first, and the high byte follows.
The value 258 (hexadecimal `0x0102`) would thus be represented as the two bytes `\x02` and `\x01`.

We can define a function `uint16()` that takes an integer and converts it to a two-byte string according to these rules:

:::{margin}
In Python, `//` is used for integer division.
:::

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v ';' binary.fan
```

Using `uint16()`, we can now define how the value of `<length>` is related to the length of `<content>`:

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep ';$' binary.fan | grep -v '::='
```

:::{tip}
Having a derived value (like `<length>`) isolated on the left-hand side of an equality equation makes it easy for Fandango to first compute the content and then compute and assign the derived value.
:::

Again, all of this goes into a single `.fan` file: [`binary.fan`](binary.fan) holds the grammar, the `uint16()` definition, and the constraint.
Let us produce a single output using `binary.fan` and view its (binary) contents, using `od -c`:

```shell
$ fandango fuzz -n 1 -f binary.fan | od -c
```

```{code-cell}
:tags: ["remove-input"]
! fandango fuzz -n 1 -f binary.fan | od -c
```

The hexadecimal dump shows that the first two bytes encode the length of the string of digits that follows.
The last character is a newline `\n` - this is produced by Fandango and not part of the grammar.
The format is correct - we have successfully produced a length encoding.

## Converting Values to Binary Formats

Instead of implementing `uint16()` manually, we can also use the Python [`struct` module](https://docs.python.org/3/library/struct.html), which offers several functions to convert data into binary formats.
Using `struct`, we can redefine `uint16()` as

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v ';' binary-pack.fan
```

and obtain the same result:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -n 1 -f binary-pack.fan | od -c
```

Note that return value of `struct.pack()` has the type `bytes` (byte string), which is different from the `str` Unicode strings that Fandango uses:

```{code-cell}
:tags: ["remove-input"]
from struct import pack
```

```{code-cell}
pack('<H', 20)
```

```{code-cell}
type(pack('<H', 20))
```

In Python, comparisons of different types always return `False`":

```{code-cell}
# Left hand is byte string, right hand is Unicode string
b'\x14\x00' == '\x14\x00'
```

Hence, a constraint that compares a Fandango symbol against a byte string _will always fail_.

```{warning}
When comparing symbols against values, always be sure to convert the values to Unicode `str` strings first.
```

```{tip}
Using the `'iso8859-1'` encoding (also known as `'latin-1'`) allows a 1:1 conversion of byte strings with values `'\x00'..'\xff'` into Unicode `str` strings without further interpretation.
```

```{tip}
Adding _type annotations_ to functions in `.fan` files allows for future static type checking and further optimizations.
```

Check out the [`struct` module](https://docs.python.org/3/library/struct.html) for additional encodings, including float types, long and short integers, and many more.


## Compression and Conversion

:::{error}
To be completed later.
:::

Some parts of a binary file may be _compressed_ to save space.
Here's a sketch on how to achieve this:

```python
<chunk> ::= <header> <compressed_content> <trailer>;
<compressed_content> ::= <byte>*;
<content> ::= <byte>*;

<compressed_content> == compress(<content>);    # for producing
<content> == uncompress(<compressed_content>);  # for parsing
```

or, using generators:

```python
<chunk> ::= <header> <compressed_content> <trailer>;
<compressed_content> ::= <byte>* | <foo> | <bar> := compress(<content>);
<content> ::= <byte>* = uncompress(<compressed_content>);
```


## Case Study: The GIF Format

:::{error}
To be added later.
:::

The [GIF format](https://www.fileformat.info/format/gif/egff.htm) is widely used to encode image sequences.
