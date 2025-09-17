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

(sec:conversion)=
# Data Converters

When defining a complex input format, some parts may be the result of applying an _operation_ on another, more structured part.
Most importantly, content may be _encoded_, _compressed_, or _converted_.

Fandango uses a special form of [generators](sec:generators) to handle these, called _converters_.
These are generator expressions with _symbols_, mostly functions that take symbols as arguments.
Let's have a look at how these work.


## Encoding Data During Fuzzing

In Fandango, a [generator](sec:generators) expression can contain _symbols_ (enclosed in `<...>`) as elements.
Such generators are called _converters_.
When fuzzing, converters have the effect of Fandango using the grammar to

* instantiate each symbol from the grammar,
* evaluate the resulting expression, and
* return the resulting value.

Here is a simple example to get you started.
The [Python `base64` module](https://docs.python.org/3/library/base64.html) provides methods to encode arbitrary binary data into printable ASCII characters:

```{code-cell}
import base64

encoded = base64.b64encode(b'Fandango\x01')
encoded
```

Of course, these can be decoded again:

```{code-cell}
base64.b64decode(encoded)
```

Let us make use of these functions.
Assume we have a `<data>` field that contains a number of bytes:

```{code-cell}
:tags: ["remove-input"]
!grep '^<data>' encode.fan
```

To encode such a `<data>` field into an `<item>`, we can write

```{code-cell}
:tags: ["remove-input"]
!grep '^<item>' encode.fan
```


This rule brings multiple things together:

* First, we convert `<data>` into a suitable type (in our case, `bytes`).
* Then, we invoke `base64.b64encode()` on it as a generator to obtain a string of bytes.
* We parse the string into an `<item>`, whose definition is `rb'.*'` (any sequence of bytes except newline).

In a third step, we embed the `<item>` into a (binary) string:

```{code-cell}
:tags: ["remove-input"]
!grep '^<start>' encode.fan
```

The full resulting [`encode.fan`](encode.fan) spec looks like this:

```{code-cell}
:tags: ["remove-input"]
!cat encode.fan
```

With this, we can encode and embed binary data:

```shell
$ fandango fuzz -f encode.fan -n 1
```

```{code-cell}
:tags: ["remove-input"]
!PYTHONHASHSEED=0 fandango fuzz -f encode.fan -n 1 --random-seed 7
assert _exit_code == 0
```

In the same vein, one can use functions for compressing data or any other kind of conversion.


## Sources, Encoders, and Constraints

When Fandango produces an input using a generator, it _saves_ the generated arguments as a _source_ in the produced derivation tree.
Sources become visible as soon as the input is shown as a grammar:

```shell
$ fandango fuzz -f encode.fan -n 1 --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
!PYTHONHASHSEED=0 fandango fuzz -f encode.fan -n 1 --format=grammar --random-seed 7
assert _exit_code == 0
```

In the definition of `<item>`, we see a generic converter `f(<data>)` as well as the definition of `<data>` that went into the generator.
(The actual generator code, `base64.b64encode(bytes(<data>))`, is not saved in the derivation tree.)

We can visualize the resulting tree, using a double arrow between `<item>` and its source `<data>`, indicating that their values depend on each other:

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree

tree = Tree('<start>',
  Tree(b'Data: '),
  Tree('<item>',
    Tree(b'RmFuZGFuZ29Nyhg='),
    sources=[
      Tree('<data>',
        Tree(b'Fandango'),
        Tree('<byte>', Tree('<_byte>', Tree(b'M'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'\xca'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'\x18')))
      ),
    ]
  )
)
tree.visualize()
```

Since sources like `<data>` are preserved, we can use them in [constraints](sec:constraints).
For instance, we can produce a string with specific values for `<data>`:

```shell
$ fandango fuzz -f encode.fan -n 1 -c '<data> == b"Fandango author"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f encode.fan -n 1 -c '<data> == b"Fandango author"' --population-size 1
assert _exit_code == 0
```

Is this string a correct encoding of a correct string?
We will see in the next section.


## Decoding Parsed Data

So far, we can only _encode_ data during fuzzing.
But what if we also want to _decode_ data, say during [parsing](sec:parsing)?
Our `encode.fan` will help us _parse_ the data, but not decode it:

```shell
$ echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode.fan
```

```{code-cell}
:tags: ["remove-input"]
!echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode.fan
assert _exit_code == 1
```

The fact that parsing fails is not a big surprise, as we only have specified an _encoder_, but not a _decoder_.
As the error message suggests, we need to add a generator for `<data>` - a decoder that converts `<item>` elements into `<data>`.

We can achieve this by providing a generator for `<data>` that builds on `<item>`:

```{code-cell}
:tags: ["remove-input"]
!grep '^<data>' encode-decode.fan
```

Here, `base64.b64decode(bytes(<item>))` takes an `<item>` (which is previously parsed) and decodes it.
The decoded result is parsed and placed in `<data>`.

The resulting [`encode-decode.fan`](encode-decode.fan) file now looks like this:

```{code-cell}
:tags: ["remove-input"]
!cat encode-decode.fan
```

```{margin}
Fandango allows generators in both directions so one `.fan` file can be used for fuzzing and parsing.
```

If this looks like a mutual recursive definition, that is because it is.
During fuzzing and parsing, Fandango tracks the _dependencies_ between generators and uses them to decide which generators to use first:

* When fuzzing, Fandango operates _top-down_, starting with the topmost generator encountered; their arguments are _produced_.
  In our case, this is the `<item>` generator, generating a value for `<data>`.
* When parsing, Fandango operates _bottom-up_, starting with the lowest generators encountered; their arguments are _parsed_.
  In our case, this is the `<data>` generator, parsing a value for `<item>`.

In both case, when Fandango encounters a recursion, _it stops evaluating the generator_:

* When parsing an `<item>`, Fandango does not invoke the generator for `<data>` because `<data>` is being processed already.
* Likewise, when producing `<data>`, Fandango does not invoke the generator for `<item>` because `<item>` is being processed already.

Let us see if all of this works and if this input is indeed properly parsed and decoded.

```shell
$ echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode-decode.fan -o - --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
!echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode-decode.fan -o - --format=grammar
assert _exit_code == 0
```

We see that the `<data>` element contains the `"Fandango author"` string we provided as a constraint during generation.
This is what the parsed derivation tree looks like:

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree

tree = Tree('<start>',
  Tree(b'Data: '),
  Tree('<item>',
    Tree(b'RmFuZGFuZ28gYXV0aG9y'),
    sources=[
      Tree('<data>',
        Tree(b'Fandango'),
        Tree('<byte>', Tree('<_byte>', Tree(b' '))),
        Tree('<byte>', Tree('<_byte>', Tree(b'a'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'u'))),
        Tree('<byte>', Tree('<_byte>', Tree(b't'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'h'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'o'))),
        Tree('<byte>', Tree('<_byte>', Tree(b'r')))
      ),
    ]
  )
)
tree.visualize()
```

With a constraint, we can check that the decoded string is correct:

```shell
$ echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode-decode.fan -c '<data> == b"Fandango author"'
```

```{code-cell}
:tags: ["remove-input"]
!echo -n 'Data: RmFuZGFuZ28gYXV0aG9y' | fandango parse -f encode-decode.fan -c '<data> == b"Fandango author"'
assert _exit_code == 0
```

We get no error - so the parse was successful, and that all constraints hold.


## Applications

The above scheme can be used for all kinds of encodings and compressions - and thus allow _translations between abstraction layers_.
Typical applications include:

* _Compressed_ data (e.g. pixels in a GIF or PNG file)
* _Encoded_ data (e.g. binary input as ASCII chars in MIME encodings)
* _Converted_ data (e.g. ASCII to UTF-8 to UTF-16 and back)

Even though parts of the input are encoded (or compressed), you can still use _constraints_ to shape them.
And if the encoding or compression can be inverted, you can also use it to _parse_ inputs again.


## Converters vs. Constraints

Since converters (and generally, generators) can do anything, they can be used for any purpose, including producing solutions that normally would come from [constraints](sec:constraints).

As an example, consider the credit card grammar from the [chapter on binary inputs](sec:binary):

```{code-cell}
:tags: ["remove-input"]
# show grammar except '<byte>'
!grep '::=' credit_card.fan; grep 'where' credit_card.fan
```

Instead of having a constraint (`where`) that expresses the relationship between `<number>` and `<check_digit>`, we can easily enhance the grammar with converters between `<number>` and `<credit_card_number>`:

```python
<credit_card_number> ::= <number> <check_digit> := add_check_digit(str(<number>))
<number>             ::= <digit>{15} := strip_check_digit(str(<credit_card_number>))
```

with

```python
def add_check_digit(number: str) -> str:
    """Add a check digit to the credit card number `number`."""
    check_digit = credit_card_check_digit(number)
    return number + check_digit
```

and

```
def strip_check_digit(number: str) -> str:
    """Strip the check digit from the credit card number `number`."""
    return number[:-1]
```

The resulting `.fan` spec [`credit_card-gen.fan`](credit_card-gen.fan)
has the same effect as the original [`credit_card.fan`](credit_card.fan) from the [chapter on binary inputs](sec:binary):

```shell
$ fandango fuzz -f credit_card-gen.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f credit_card-gen.fan -n 10
```


Now, these two functions `add_check_digit()` and `strip_check_digit()` are definitely longer than our original constraint

```python
where <check_digit> == credit_card_check_digit(str(<number>))
```

However, they are not necessarily more complex.
And they are more efficient, as they provide a solution right away.
So when should one use constraints, and when converters?

```{tip}
In general:

* If you have a simple, _operational_ way to solve a problem, consider a _converter_.
* If you want a simple, _declarative_ way to specify your needs, use a _constraint_.
```