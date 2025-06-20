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
!grep -v '::=' credit_card.fan | grep -v '^where'
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

We can easily make use of `credit_card_check_digit()` in a constraint that ties `<check_digit>` and `<number>`:

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep '^where' credit_card.fan
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
!fandango fuzz -f credit_card.fan -n 10 --validate
assert _exit_code == 0
```

We can also use the grammar to _parse_ and _check_ numbers.
This credit card number should be valid:

```shell
$ echo -n 4931633575526870 | fandango parse -f credit_card.fan
$ echo $?  # print exit code
0
```

```{code-cell}
:tags: ["remove-input"]
!echo -n 4931633575526870 | fandango parse -f credit_card.fan
assert _exit_code == 0
```

Adding 1 to this number should make it _invalid_:

```shell
$ echo -n 4931633575526871 | fandango parse -f credit_card.fan
```

```{code-cell}
:tags: ["remove-input"]
!echo -n 4931633575526871 | fandango parse -f credit_card.fan
assert _exit_code == 1
```

```shell
$ echo $?  # print exit code
1
```



:::{margin}
You can also simply do an Internet search for a Python implementation of the respective algorithm.
Or ask your favorite AI assistant.
:::

Similarly, you can define any kind of checksum function and then use it in a constraint.
In Python, it is likely that someone has already implemented the specific checksum function, so you can also _import_ it:

* [The `hashlib` module](https://docs.python.org/3/library/hashlib.html) provides hash functions such as MD5 or SHA-256.
* [The `binascii` module](https://docs.python.org/3/library/binascii.html) offers CRC checks.
* [The `zlib` module](https://docs.python.org/3/library/zlib.html) provides CRC32 and ADLER32 checks used in zip files.


## Characters and Bytes

The second set of features one frequently encounters in binary formats is, well, _bytes_.
So far, we have seen Fandango operates on strings of Unicode _characters_, which use UTF-8 encoding.
This clashes with a byte interpretation as soon as the produced string contains a UTF-8 prefix byte, such as `\xc2` or `\xe0`, which mark the beginning of a two- and three-byte UTF-8 sequence, respectively.

To ensure bytes will be interpreted as bytes (and as bytes only), place a `b` (binary) prefix in front of them.
This ensures that a byte `b'\xc2'` will always be interpreted as a single byte, whereas `💃` will be interpreted as a single character (despite occupying multiple bytes).

```{tip}
Fandango provides a `<byte>` symbol by default, which expands into all bytes `b'\x00'..b'\xff'`.
```

### Text Files and Binary Files

By default, Fandango will read and write files in `text` mode, meaning that characters will be read in using UTF-8 encoding.
However, if a grammar can produce bytes (or [bits](sec:bits)), the associated files will be read and written in `binary` mode, reading and writing _bytes_ instead of (encoded) characters.
If your grammar contains bytes _and_ strings, then the strings will be written in UTF-8 encoding into the binary file.

You can enforce a specific behavior using the Fandango `--file-mode` flag for the `fuzz` and `parse` commands:

* `fuzz --file-mode=text` opens all files in `text` mode. Strings and bytes will be written in UTF-8 encoding.
* `fuzz --file-mode=binary` opens all files in `binary` mode. Strings will be written in UTF-8 encoding; bytes will be written as is.

The default is `fuzz --file=mode=auto` (default), which will use `binary` or `text` mode as described above.

```{tip}
Avoid mixing non-ASCII strings with bits and bytes in a single grammar.
```

(sec:byte-regexes)=
### Bytes and Regular Expressions

Fandango also supports [regular expressions](Regexes.md) over bytes.
To obtain a regular expression over a byte string, use both `r` and `b` prefixes.
This is especially useful for character classes.

Here is an example: [`binfinity.fan`](binfinity.fan) produces strings of five bytes _outside_ the range `\x80-\xff`:

```{code-cell}
:tags: ["remove-input"]
!cat binfinity.fan
```

This is what we get:

```shell
$ fandango fuzz -f binfinity.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f binfinity.fan -n 10 --validate
assert _exit_code == 0
```


## Length Encodings

The third set of features one frequently encounters in binary formats is _length encodings_ - that is, a particular field holds a value that represents the length of one or more fields that follow.
Here is a simple grammar that expresses this characteristic: A `<field>` has a two-byte length, followed by the actual (byte) content (of length `<length>`).

```{code-cell}
:tags: ["remove-input"]
!grep '::=' binary.fan
```

### Encoding Lengths with Constraints

The relationship between `<length>` and `<content>` can again be expressed using a constraint.
Let us assume that `<length>` comes as a two-byte (16-bit) unsigned integer with _little-endian_ encoding - that is, the low byte comes first, and the high byte follows.
The value 258 (hexadecimal `0x0102`) would thus be represented as the two bytes `\x02` and `\x01`.

We can define a function `uint16()` that takes an integer and converts it to a two-byte string according to these rules.
The Python method `N.to_bytes(LENGTH, ENDIANNESS)` converts the integer `N` into a bytes string of length `LENGTH`. `ENDIANNESS` is either `'big'` (default) or `'little'`.

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v '::=' binary.fan | grep -v '^where'
```

Using `uint16()`, we can now define how the value of `<length>` is related to the length of `<content>`:

```{code-cell}
:tags: ["remove-input"]
# show constraints
!grep '^where' binary.fan
```

```{tip}
Having a derived value (like `<length>`) isolated on the left-hand side of an equality equation makes it easy for Fandango to first compute the content and then compute and assign the derived value.
```

Again, all of this goes into a single `.fan` file: [`binary.fan`](binary.fan) holds the grammar, the `uint16()` definition, and the constraint.
Let us produce a single output using `binary.fan` and view its (binary) contents, using `od -c`:

```shell
$ fandango fuzz -n 1 -f binary.fan -o - | hexdump -C
```

```{code-cell}
:tags: ["remove-input"]
! fandango fuzz -n 1 -f binary.fan -o - | hexdump -C
```

The hexadecimal dump shows that the first two bytes encode the length of the string of digits that follows.
The format is correct - we have successfully produced a length encoding.


### Encoding Lengths with Repetitions

Another way to implement length constraints is by using _repetitions_.
In Fandango, repetitions `{}` can also contain _expressions_, and like constraints, these can also refer to nonterminals that have already been parsed or produced.
Hence, we can specify a rule

```python
<content> ::= <byte>{f(<length>)}
```

where `f()` is a function that computes the number of `<byte>` repetitions based on `<length>`.

Let us define a variant [`binary-rep.fan`](binary-rep.fan) that makes use of this.
Here, we specify that `<content>` consists of `N` bytes, where `N` is given as follows:

:::{margin}
We use a generator expression `:= VALUE` to prevent generated values from getting too large.
:::

```{code-cell}
:tags: ["remove-input"]
!grep '::=' binary-rep.fan
```

The method `<length>.value()` returns the bytes string value of the `<length>` element.
The function `from_uint16()` is defined as follows:

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v '::=' binary-rep.fan | grep -v '^where'
```

With this, we can easily produce length-encoded inputs:


```shell
$ fandango fuzz -n 1 -f binary-rep.fan -o - | hexdump -C
```

```{code-cell}
:tags: ["remove-input"]
! fandango fuzz -n 1 -f binary-rep.fan -o - | hexdump -C
```

```{tip}
When [parsing](sec:parsing) inputs, computed repetitions are much more efficient than constraints.
```



## Converting Values to Binary Formats

Instead of implementing `uint16()` manually, we can also use the Python [`struct` module](https://docs.python.org/3/library/struct.html), which offers several functions to convert data into binary formats.
Using `struct`, we can redefine `uint16()` as

```{code-cell}
:tags: ["remove-input"]
# show code
!grep -v '::=' binary-pack.fan | grep -v '^where'
```

and obtain the same result:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -n 1 -f binary-pack.fan -o - --validate | od -c
assert _exit_code == 0
```

Note that the return value of `struct.pack()` has the type `bytes` (byte string), which is different from the `str` Unicode strings that Fandango uses:

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

In Python, comparisons of different types always return `False`:

```{code-cell}
# Left hand is byte string, right hand is Unicode string
b'\x14\x00' == '\x14\x00'
```

Hence, a constraint that compares a Fandango symbol against a byte string _will always fail_.

```{important}
When comparing symbols against values, always be sure to convert the values to the appropriate type first.
```

```{tip}
Using the `'iso8859-1'` encoding (also known as `'latin-1'`) allows a 1:1 conversion of byte strings with values `'\x00'..'\xff'` into Unicode `str` strings without further interpretation.
```

```{tip}
Adding _type annotations_ to functions in `.fan` files allows for future static type checking and further optimizations.
```

Check out the [`struct` module](https://docs.python.org/3/library/struct.html) for additional encodings, including float types, long and short integers, and many more.
