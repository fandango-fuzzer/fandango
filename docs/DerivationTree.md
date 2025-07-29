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
# Derivation Tree Reference

```{code-cell}
:tags: ["remove-input", "remove-output"]
from myst_nb import glue
from fandango.language.tree import DerivationTree
from fandango.language.symbols import NonTerminal
t = DerivationTree(NonTerminal('a string'))
number_of_methods = len(dir(t)) + len(dir(str))
glue("number_of_methods", number_of_methods)
```

Fandango constraints make use of _symbols_ (anything enclosed in `<...>`) to express desired or required properties of generated inputs.
During evaluation, any `<SYMBOL>` returns a _derivation tree_ representing the composition of the produced or parsed string.

This derivation tree has a type of `DerivationTree`, as do all subtrees.
`DerivationTree` objects support *{glue:}`number_of_methods` functions, methods, and operators* directly; after converting `DerivationTree` objects into standard Python types such as `str`, the entire Python ecosystem is available.

(sec:derivation-tree-structure)=
## Derivation Tree Structure

Let's have a look at the structure of a derivation tree. Consider this derivation tree from the [ISO 8601 date and time grammar](ISO8601.md):

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

Concatenating all terminal symbols (using `str(<SYMBOL>)`) in a derivation tree yields the string represented. For the above tree, this would be `2025-10-27`.


## Evaluating Derivation Trees

To write constraints, you may want to serialize derivation trees into standard Python types such as `str`ings, `bytes`, or `int`s. To do so, simply call `str(<SYMBOL>)`, `bytes(<SYMBOL>)`, or `int(<SYMBOL>)` respectively.

Internally, the serialization is done in `str` objects as long as the sub-tree only contains string values, and in `bytes` otherwise. During concatenation, strings are converted to bytes in with `utf-8` encoding, for conversion from bytes to strings, `latin-1` is used to prevent breaking non-utf-8 strings. If you would like to convert them using utf-8, you can call `<SYMBOL>.to_string("utf-8")`.

Concatenation of non-bit types with bit types always triggers Fandango to convert the remaining trailing bits into `bytes` (with the first bit being the most significant). If the number of trailing bits isn't a multiple of 8, Fandango will throw an error.

`int(<SYMBOL>)` on a subtree consisting only of strings will attempt to parse the string as a number. If the tree consists of bits only, it will be converted to a number with the first bit being the most significant. Bytes are converted to strings and then treated accordingly.

Previous versions of Fandango automatically converted certain values — this no longer works to prevent accidental mistakes while writing constraints.

```{tip}
It is generally unwise to rely on the type of the internal representation of linearized `DerivationTree` values as these may change with future expansions of Fandango. Use functions directly implemented on them (`<SYMBOL>.startswith("Hello")`), or explicitly convert them to a base type in Python instead (`str(<SYMBOL>)`).
```

## General `DerivationTree` Functions

These functions are available for all `DerivationTree` objects, regardless of the type they evaluate into.

### Converters

Since any `<SYMBOL>` has the type `DerivationTree`, one must convert it first into a standard Python type before passing it as argument to a standard Python function.

`str(<SYMBOL>) -> str`
: Convert `<SYMBOL>` into a Unicode string. Byte strings in `<SYMBOL>` are converted using `latin-1` encoding.

`<SYMBOL>.to_string(encoding: str = "latin-1") -> str`
: More flexible alternative to `str(<SYMBOL>)`

`bytes(<SYMBOL>) -> bytes`
: Convert `<SYMBOL>` into a byte string. Unicode strings in `<SYMBOL>` are converted using `utf-8` encoding.

`<SYMBOL>.to_bytes(encoding: str = "utf-8") -> bytes`
: More flexible alternative to `bytes(<SYMBOL>)`

`int(<SYMBOL>) -> int`
: Convert `<SYMBOL>` into an integer, like the Python `int()` function.
`<SYMBOL>` must be exclusively bits, or a Unicode string or byte string representing an integer literal.

`<SYMBOL>.to_int(encoding: str = "utf-8") -> int`
: More flexible alternative to `int(<SYMBOL>)`

`<SYMBOL>.should_be_serialized_to_bytes() -> bool`
: Returns `True` if the sub-tree contains bits or bytes and thus is natively serialized to bytes

`<SYMBOL>.contains_bits() -> bool`
: Returns `True` if the sub-tree contains bits

`<SYMBOL>.contains_bytes() -> bool`
: Returns `True` if the sub-tree contains bytes

`<SYMBOL>.to_bits(encoding: str = "utf-8") -> int`
: Provides a bitwise representation of the input, in a string of `0`s  and `1`s

`<SYMBOL>.is_terminal() -> bool`
: True if `<SYMBOL>` is a terminal node.

`<SYMBOL>.is_nonterminal() -> bool`
: True if `<SYMBOL>` is a nonterminal node.


### Accessing Children

`len(<SYMBOL>) -> int`
: Return the number of children of `<SYMBOL>`.

```{important}
To access the length of the _string_ represented by `<SYMBOL>`, use `len(str(<SYMBOL>))`.
```

`<SYMBOL>[n] -> DerivationTree`
: Access the `n`th child of `<SYMBOL>`, as a `DerivationTree`. `<SYMBOL>[0]` is the first child; `<SYMBOL>[-1]` is the last child.

```{important}
To access the `n`th _character_ of `<SYMBOL>`, use `str(<SYMBOL>)[n]`.
```

`<SYMBOL>[start:stop] -> DerivationTree`
: Return a new `DerivationTree` which has the children `<SYMBOL>[start]` to `<SYMBOL>[stop-1]` as children. If `start` is omitted, children start from the beginning; if `stop` is omitted, children go up to the end, including the last one.

`<SYMBOL>.children() -> list[DerivationTree]`
: Return a list containing all children of `<SYMBOL>`.

`<SYMBOL>.children_values() -> list[TreeValue]`
: Return a list containing the values of all children of `<SYMBOL>`.

```{note}
`TreeValue` objects can be converted into standard Python objects with `str()`, `bytes()`, or `int().` Alternatively, use the same base functionality from `str`, `bytes`, and `int` on them directly that is [implemented on entire `DerivationTree`s](sec:derivation-tree-direct-access-functions).
```

`<SYMBOL_1> in <SYMBOL_2>`
: Return True if `<SYMBOL_1> == CHILD` for any of the children of `<SYMBOL_2>`.

`VALUE in <SYMBOL>`
: Return True if `VALUE == CHILD.value()` for any of the children of `<SYMBOL>`.

### Accessing Descendants

`<SYMBOL>.descendants() -> list[DerivationTree]`
: Return a list containing all descendants of `<SYMBOL>`; that is, all children and their transitive children.

`<SYMBOL>.descendant_values() -> list[TreeValue]`
: Return a list containing the values of all descendants of `<SYMBOL>`; that is, the values of all children and their transitive children.

```{note}
`TreeValue` objects can be converted into standard Python objects with `str()`, `bytes()`, or `int().` Alternatively, use the same base functionality from `str`, `bytes`, and `int` on them directly that is [implemented on entire `DerivationTree`s](sec:derivation-tree-direct-access-functions).
```

### Accessing Parents

`<SYMBOL>.parent() -> DerivationTree | None`
: Return the parent of the current node, or `None` for the root node.


### Accessing Sources

`<SYMBOL>.sources() -> list[DerivationTree]`
: Return a list containing all sources of `<SYMBOL>`. Sources are symbols used in generator expressions out of which the value of `<SYMBOL>` was created; see [the section on data conversions](sec:conversion) for details.


### Comparisons

`<SYMBOL_1> == <SYMBOL_2>`
: Returns True if both trees have the same structure and all nodes have the same values.

`<SYMBOL> == VALUE`
: Returns True if `<SYMBOL>.value() == VALUE` — requires the types to match

`<SYMBOL_1> != <SYMBOL_2>`
: Returns True if both trees have a different structure or any nodes have different values.

`<SYMBOL> != VALUE`
: Inverse of `<SYMBOL> == VALUE`.

To compare values with `<`, `>`, `<=`, `>=`, etc., explicitly convert them to the type you would like to use for comparison first.

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


(sec:derivation-tree-direct-access-functions)=
## Type-Specific Functions

The bulk of available functions comes from the Python standard library. The vast majority of methods implemented on `str`, `bytes`, and `int` are also implemented on `DerivationTree`s:

* If a method is only implemented on one of the three base types, the `DerivationTree` internally is first transformed into that type (using `str(<SYMBOL>)` etc.).
* If a method is implemented on multiple base types, but they always have different signatures (such as `.startswith`, which takes a `str` if called on a `str`, and `bytes` if called on `bytes`), the `DerivationTree` is transformed into the appropriate base type.
* If a method is implemented on multiple base types, and there is no way to distinguish based on the signatures, the method is envoked on the underlying type. This is not recommended as these methods rely on knowledge of the type of the internal representation (which may change in the future). Simply convert the tree to the desired base type first (`str(<SYMBOL>).upper()`).

