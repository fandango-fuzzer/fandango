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
# Conversion and Compression

When defining a complex input format, some parts may be the result of applying an _operation_ on another, more structured part.
Most importantly, content may be _encoded_, _compressed_, or _sanitized_.

Fandango uses a special form of [generators](sec:generators) to handle these, namely generators with _symbols_.
Let's have a look at how these work.


## Encoding Data During Fuzzing

In Fandango, a [generator](sec:generators) expression can contain _symbols_ (enclosed in `<...>`) as elements.
When fuzzing, this has the effect of Fandango using the grammar to

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

Let us assume we have a `<data>` field that contains a number of bytes:

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

The resulting [`encode.fan`](encode.fan) spec allows us to encode and embed binary data:

```{code-cell}
!fandango fuzz -f encode.fan -n 1
```

In the same vein, one can use functions for compressing data or any other kind of conversion.


## Decoding Parsed Data

```{code-cell}
!echo -n 'Data: RmFuZGFuZ2+O' | fandango parse -f encode-decode.fan -o - --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree

tree = Tree('<start>',
  Tree(b'Data: '),
  Tree('<item>',
    Tree(b'RmFuZGFuZ2+O'),
    sources=[
      Tree('<data>',
        Tree(b'Fandango'),
        Tree('<byte>', Tree('<_byte>', Tree(b'\x8e')))
      ),
    ]
  )
)
tree.visualize()
```
