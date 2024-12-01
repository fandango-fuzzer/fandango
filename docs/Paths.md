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
# Accessing Input Elements

```{error}
This chapter is still under construction.
```

When dealing with [complex input formats](sec:recursive), attaching [constraints](sec:constraints) can be complex, as elements can occur _multiple times_ in a generated input.
Fandango offers a few mechanisms to disambiguate these, and to specify specific _contexts_ in which to search for elements.


## Derivation Trees

% Could also compute and display derivation trees on the fly:
% import os
% os.chdir('../src')
% from fandango.language.tree import DerivationTree


```{code-cell}
from graphviz import Digraph
from IPython.display import display_svg, display_png

class Tree:
    id_counter = 1
    dot = None

    def __init__(self, symbol, *children):
        self.symbol = symbol
        self._children = children

    def children(self):
        return self._children

    def visualize(self, title="Derivation Tree"):
        """Display as PNG. (PNG works with HTML and PDF books, SVG does not)"""
        # https://graphviz.org/doc/info/lang.html
        Tree.dot = Digraph(comment=title, format='png')
        Tree.dot.attr('node', shape='none', fontname='courier-bold', fontsize='18pt')
        Tree.dot.attr('graph', rankdir='TB', tooltip=title)
        Tree.dot.attr('edge', penwidth='2pt')
        Tree.id_counter = 1
        self._visualize()
        display_png(self.dot)

    def _visualize(self):
        name = f"node-{Tree.id_counter}"
        Tree.id_counter += 1
        label = self.symbol

        # https://graphviz.org/doc/info/colors.html
        if self.symbol.startswith('<'):
            color = 'firebrick'
        else:
            color = 'darkblue'

        label = label.replace('<', '\\<')
        label = label.replace('>', '\\>')
        Tree.dot.node(name, label, fontcolor=color)

        for child in self.children():
            child_name = child._visualize()
            Tree.dot.edge(name, child_name)

        return name
```

```{code-cell}
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
