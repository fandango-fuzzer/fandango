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

(sec:derivation-tree)=
# Symbols and their Functions

Fandango constraints make use of _symbols_ (anything enclosed in `<...>`) to express desired or required properties of generated inputs.
This chapter defines symbols and the applicable functions.

## Derivation Trees

Any `<SYMBOL>` has a type of `DerivationTree`, with the functions and methods applicable as described in this chapter.

As the name suggests, a `DerivationTree` comes as a _tree_ representing the composition of the produced or parsed string.
As an example, consider this derivation tree from the [ISO 8601 date and time](ISO8601.md) grammar:

:::{margin}
Note that nonterminals can be empty strings, such as the second child of `<iso8601datetime>`.
:::

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree
tree = Tree('<start>', Tree('<iso8601datetime>',
  Tree('<iso8601date>', Tree('<iso8601calendardate>',
    Tree('<iso8601year>',
      Tree(''),
      Tree('<digit>', Tree('2')),
      Tree('<digit>', Tree('0')),
      Tree('<digit>', Tree('2')),
      Tree('<digit>', Tree('5'))
    ),
    Tree('-'),
    Tree('<iso8601month>', Tree('10')),
    Tree('-'),
    Tree('<iso8601day>', Tree('27'))
  )),
  Tree('')
))
tree.visualize()
```

The elements of the tree are designated as follows:

Node
: Any connected element of a tree.

Child
: An immediate descendant of a node. In the above tree, the `<start>` node has one child, `<iso8601datetime>`.

Descendant
: A child of a node, or a descendant of one of its children. `<iso8601month>` is a descendant of `<iso8601date>`. All nodes (except the root node) are descendants of the root node.

Parent
: The parent of a node $N$ is the node that has $N$ as a child. `<start>` is the parent of `<iso8601datetime>`.

Root
: The node without parent; typically `<start>`.

Terminal Symbol
: A node with at least one child.

Nonterminal Symbol
: A node without children.

Concatenating all terminal symbols in a derivation tree yields the string represented.
For the above tree, this would be `2025-10-27`.


(sec:derivation-tree-value)=
## Evaluating Symbols

Since standard Python functions do not accept derivation trees, one must first convert them into an acceptable type.
The `value()` method plays a central role in this.

`<SYMBOL>.value() -> str | int | bytes`
: The method `<SYMBOL>.value()` _evaluates_ `<SYMBOL>` and returns its value, which represents the concatenation of all descendants.
The _type_ of the return value is
    * A _Unicode string_ (`str`) if all descendants are Unicode strings.
    * An _integer_ (`int`) if all descendants are bits.
    * A _byte string_ (`bytes`) in all other cases, notably if
        - any of the descendants of `<SYMBOL>` is a byte string, or
        - the descendants of `<SYMBOL>` contain bits _and_ other elements.


### Unicode Strings

Any symbol that is composed only from Unicode strings will evaluate into a Python _Unicode string_ (`str`).
The descendants of `<SYMBOL>` are concatenated as strings.

Example - in
```python
<foo> ::= <bar> "bara"
<bar> ::= "bar"
```

`<foo>.value()` will be the Unicode string `"barbara"`.

This is the most common case.


### Integers

Any symbol that is composed only from bits will evaluate into a Python _integer_ (`int`).
The descendants are concatenated as bits; the most significant bit comes first.

Example - in
```python
<foo> ::= <bar> 0 1 1
<bar> ::= 0 1 0
```

`<foo>.value()` will be the integer `0b010011`, or 19.


### Byte Strings

Any symbol where any of the descendants is a byte string, or where the descendants are bits _and_ other elements, will evaluate into a Python _byte string_ (`bytes`).
The descendants are all concatenated as follows:

1. Any _bit sequence_ $B$ is converted into a _bytes string_ with the most significant bit coming first.
2. Any _Unicode string_ $S$ is converted into a _bytes string_ representing $S$ in UTF-8 encoding.
3. The resulting byte strings are all concatenated.

Example 1 - in
```python
<foo> ::= <bar> "foo"  # a Unicode string
<bar> ::= b"bar"       # a byte string
```

`<foo>.value()` will be the byte string `b"barfoo"`.

:::{warning}
If you mix Unicode strings and byte strings in a grammar, Fandango will issue a warning.
:::

Example 2 - in
```python
<foo> ::= <bar> b"foo"    # a byte string
<bar> ::= 1 1 1 1 1 1 1 1 # a bit string
```

`<foo>.value()` will be the byte string `b"foo\xff"`.

:::{warning}
If you mix Unicode strings and bits in a grammar, Fandango will issue a warning.
:::


## General Symbol Functions

These functions are available for all symbols, regardless of the type they evaluate into.

### Converters

:::{margin}
Invoking methods (`<SYMBOL>.METHOD()`), as well as operators (`<SYMBOL> + ...`), where `<SYMBOL>` is one of the operators, do not require conversion.
:::

Since any `<SYMBOL>` has the type `DerivationTree`, one must convert it first into a standard Python type before passing it as argument to a standard Python function.

`str(<SYMBOL>) -> str`
: Convert `<SYMBOL>` into a Unicode string. If `<SYMBOL>` is a byte string, its contents are converted using `latin-1` encoding.

`int(<SYMBOL>) -> int`
: Convert `<SYMBOL>` into an integer, like the Python `int()` function.
`<SYMBOL>` must be an `int`, or a Unicode string or byte string representing an integer literal.

`float(<SYMBOL>) -> float`
: Convert `<SYMBOL>` into a floating-point number, like the Python `float()` function.
`<SYMBOL>` must be an int, or a Unicode string or byte string representing a float literal.

`complex(<SYMBOL>) -> complex`
: Convert `<SYMBOL>` into a complex number, like the Python `complex()` function.
`<SYMBOL>` must be an int, or a Unicode string or byte string representing a float literal.

`bool(<SYMBOL>) -> bool`
: Convert `<SYMBOL>` into a truth value:
    * If `<SYMBOL>` evaluates into an integer (because it represents bits), the value will be `True` if the integer is non-zero.
    * If `<SYMBOL>` evaluates into a string (bytes or Unicode), the value will be `True` if the string is not empty.

    Note that Python applies `bool()` conversion by default if a truth value is needed; hence, expressions like `<flag_1> and <flag_2>`, where both flags are bits, are allowed.


### Accessing Children

`len(<SYMBOL>) -> int`
: Return the number of children of `<SYMBOL>`.

:::{note}
To access the length of the _string_ represented by `<SYMBOL>`, use `len(str(<SYMBOL>))`.
:::

`<SYMBOL>[n] -> DerivationTree`
: Access the `n`th child of `<SYMBOL>`, as a `DerivationTree`. `<SYMBOL>[0]` is the first child; `<SYMBOL>[-1]` is the last child.

:::{note}
To access the `n`th _character_ of `<SYMBOL>`, use `str(<SYMBOL>)[n]`.
:::

`<SYMBOL>[start:stop] -> DerivationTree`
: Return a new `DerivationTree` which has the children `<SYMBOL>[start]` to `<SYMBOL>[stop-1]` as children. If `start` is omitted, children start from the beginning; if `stop` is omitted, children go up to the end, including the last one.

`<SYMBOL>.descendants() -> list[DerivationTree]`
: Return a list containing all descendants of `<SYMBOL>`; that is, all children and their transitive children.

`<SYMBOL>.descendant_values() -> list[str | int | bytes]`
: Return a list containing the values of all descendants of `<SYMBOL>`; that is, the values of all children and their transitive children.

`<SYMBOL_1> in <SYMBOL_2>`
: Return True if `<SYMBOL_1> == CHILD` for any of the children of `<SYMBOL_2>`.

`VALUE in <SYMBOL>`
: Return True if `VALUE == CHILD.value()` for any of the children of `<SYMBOL>`.



### Comparisons

`<SYMBOL_1> == <SYMBOL_2>`
: Returns True if both trees have the same structure and all nodes have the same values.

`<SYMBOL> == VALUE`
: Returns True if `<SYMBOL>.value() == VALUE`

`<SYMBOL_1> != <SYMBOL_2>`
: Returns True if both trees have a different structure or any nodes have different values.

`<SYMBOL> == VALUE`
: Returns True if `<SYMBOL>.value() == VALUE`.

`<SYMBOL_1> <|>|<=|>= <SYMBOL_2>`
: Returns True if `<SYMBOL_1>.value() <|>|<=|>= <SYMBOL_2>.value()`.

`<SYMBOL> <|>|<=|>= VALUE`
: Returns True if `<SYMBOL>.value() <|>|<=|>= VALUE`.


### Debugging

See the [section on output formats](sec:formats) for details on these representations.

`<SYMBOL>.to_bits() -> str`
: Return a bit representation (`0` and `1` characters) of `<SYMBOL>`.

`<SYMBOL>.to_grammar() -> str`
: Return a grammar-like representation of `<SYMBOL>`.

`<SYMBOL>.to_tree() -> str`
: Return a tree representation of `<SYMBOL>`, using `Tree(...)` constructors.

`repr(<SYMBOL>) -> str`
: Return the internal representation of `<SYMBOL>`, as a `DerivationTree` constructor that can be evaluated as a Python expression.



## Type-Specific Functions

The bulk of available functions comes from the Python standard library.

### Unicode Strings

For symbols that [evaluate](sec:derivation-tree-value) into Unicode strings (`str`), all [Python String methods](https://docs.python.org/3/library/stdtypes.html#string-methods) are available, such as
`<SYMBOL>.startswith()`, `<SYMBOL>.endswith()`, `<SYMBOL>.strip()`, and more.
The method is invoked on the `<SYMBOL>.value()` string value.


### Integers

For symbols that [evaluate](sec:derivation-tree-value) into integers (`int`), all [Python numeric operators and functions](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex) are available, including `+`, `-`, or `abs()`, as well as bitwise operators such as `<<`, `&`, `~`, etc.
Symbols can be used on either side of an operator.

In addition, the [Python methods on integer types](https://docs.python.org/3/library/stdtypes.html#additional-methods-on-integer-types) can be used, such as `<SYMBOL>.to_bytes()` or `<SYMBOL>.bit_count()`.
Methods are invoked on the `<SYMBOL>.value()` integer value.


### Byte Strings

For symbols that [evaluate](sec:derivation-tree-value) into byte strings (`bytes`), all [Python bytes methods](https://docs.python.org/3/library/stdtypes.html#bytes-and-bytearray-operations) are available, including `<SYMBOL>.decode()`, `<SYMBOL>.startswith()`, `<SYMBOL>.endswith()`, etc.
The method is invoked on the `<SYMBOL>.value()` byte string value.

