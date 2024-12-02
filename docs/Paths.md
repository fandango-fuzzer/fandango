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

(sec:paths)=
# Handling Input Elements

```{error}
This chapter is still under construction.
```

When dealing with [complex input formats](sec:recursive), attaching [constraints](sec:constraints) can be complex, as elements can occur _multiple times_ in a generated input.
Fandango offers a few mechanisms to disambiguate these, and to specify specific _contexts_ in which to search for elements.


## Derivation Trees

To start, let us dive a bit into the structure of _Fandango symbols_ – that is, the input elements enclosed in `<...>`.
While you can use these as strings in many context - say, in comparisons such as `<name> == "José"` or method calls such as `<name>.startswith('S')` – these are actually not strings, but _trees_ that represent the structure of the input.
As an example, consider the grammar in the [`persons.fan`](persons.fan) `.fan` file:

```{code-cell}
:tags: ["remove-input"]
!cat persons.fan
```

If one has a constraint `<name>.startswith('S')`, what is actually in a `<name>` symbol?

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree
```

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<name>',
  Tree('<uppercase_letter>', Tree('A')),
  Tree('<lowercase_letter>', Tree('a')))
tree.visualize()
```




% Could also compute and display derivation trees on the fly:
% import os
% os.chdir('../src')
% from fandango.language.tree import DerivationTree


```{code-cell}
:tags: ["remove-input"]
tree = Tree('<foo>', Tree('"bar"'), Tree('<baz>', Tree('"qux"')))
tree.visualize()
```

```{error}
(Introduce derivation trees)
```


## Specifying Paths

### Accessing Children

:::{margin}
These selectors are similar to XPath, but better aligned with Python.
In XPath, the first child has the index 1, in Fandango, it has the index 0.
:::

The expression `<foo>[N]` accesses the `N`-th child of `<foo>`, starting with zero.

If `<foo>` is defined in the grammar as
```
<foo> ::= <bar> ":" <baz>
```
then `<foo>[0]` returns the `<bar>` element, `<foo>[1]` returns `":"`, and `<foo>[2]` returns the `<baz>` element.

:::{warning}
While symbols act as strings in many contexts (and raise errors when they do not fit), this is where they differ.
To access the first _character_ of a symbol, you need to explicitly convert it to a string first, as in `str(<foo>)[0]`.
:::


### Selecting Children

:::{margin}
In XPath, the corresponding operator is `/`.
:::


The expression `<foo>.<bar>` allows accessing elements `<bar>` when they are a _direct child_ of a symbol `<foo>`.
This requires that `<bar>` occurs in the grammar rule defining `<foo>`:

```
<foo> ::= ...some expansion that has <bar>...
```

### Selecting Descendants

:::{margin}
In XPath, the corresponding operator is `//`.
:::

The expression `<foo>..<bar>` allows accessing elements `<bar>` when they are a _descendant_ of a symbol `<foo>`.
`<bar>` is a descendant of `<foo>` if

:::{margin}
`<foo>..<bar>` includes `<foo>.<bar>`.
:::

* `<bar>` is a child of `<foo>`; or
* one of `<foo>`'s children has `<bar>` as a descendant.

If that sounds like a recursive definition, that is because it is.
A simpler way to think about `<foo>..<bar>` may be "All `<bar>`s that occur within `<foo>`".


### Chains

One can _chain_ such paths


## Quantifiers


## Implications


The next section talks about [whitebox fuzzing](sec:whitebox).
