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

When dealing with [complex input formats](sec:recursive), attaching [constraints](sec:constraints) can be complex, as elements can occur _multiple times_ in a generated input.
Fandango offers a few mechanisms to disambiguate these, and to specify specific _contexts_ in which to search for elements.

(sec:derivation-trees)=
## Derivation Trees

So far, we have always assumed that Fandango generates _strings_ from the grammar.
Behind the scenes, though, Fandango creates a far richer data structure - a so-called _derivation tree_ that _maintains the structure of the string_ and _allows accessing individual elements_.
Every time Fandango sees a grammar rule

```python
<symbol> ::= ...
```

it generates a derivation tree whose root is `<symbol>` and whose children are the elements of the right-hand side of the rule.

Let's have a look at our [`persons.fan`](persons.fan) spec:

```{code-cell}
:tags: ["remove-input"]
!cat persons.fan
```

The `<start>` rule says

```{code-cell}
:tags: ["remove-input"]
!grep '^<start>' persons.fan
```

Then, a resulting derivation tree for `<start>` looks like this:

```{code-cell}
:tags: ["remove-input"]
from Tree import Tree
```

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<start>',
  Tree('<person_name>'),
  Tree('","'),
  Tree('<age>')
)
tree.visualize()
```

As Fandango expands more and more symbols, it expands the derivation tree accordingly.
Since the grammar definition for `<person_name>` says

```{code-cell}
:tags: ["remove-input"]
!grep '^<person_name>' persons.fan
```

the above derivation tree would be extended to

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<start>',
  Tree('<person_name>',
    Tree('<first_name>'),
    Tree('" "'),
    Tree('<last_name>')
  ),
  Tree('","'),
  Tree('<age>')
)
tree.visualize()
```

And if we next extend `<age>` and then `<digit>` based on their definitions

```{code-cell}
:tags: ["remove-input"]
!egrep '^(<age>|<digit>)' persons.fan
```

% TODO: Is that so? -- AZ
:::{margin}
If one has a Kleene operator like `+`, `*`, or `?`, the elements operated on become children of the symbol being defined.
Hence, the `<digit>` elements become children of the `<age>` symbol.
:::

our tree gets to look like this:

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<start>',
  Tree('<person_name>',
    Tree('<first_name>'),
    Tree('" "'),
    Tree('<last_name>')
  ),
  Tree('","'),
  Tree('<age>',
    Tree('<digit>',
      Tree('"1"')
    ),
    Tree('<digit>',
      Tree('"8"')
    )
  )
)
tree.visualize()
```

Repeating the process, it thus obtains a tree like this:

% Could also compute and display derivation trees on the fly:
% ```
% import os
% os.chdir('../src')
% from fandango.language.tree import DerivationTree
% ```

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<start>',
  Tree('<person_name>',
    Tree('<first_name>',
      Tree('<name>',
        Tree('<ascii_uppercase_letter>',
          Tree('"E"')
        ),
        Tree('<ascii_lowercase_letter>',
          Tree('"x"')
        )
      )
    ),
    Tree('" "'),
    Tree('<last_name>',
      Tree('<name>',
        Tree('<ascii_uppercase_letter>',
          Tree('"P"')
        ),
        Tree('<ascii_lowercase_letter>',
          Tree('"l"')
        ),
        Tree('<ascii_lowercase_letter>',
          Tree('"t"')
        ),
        Tree('<ascii_lowercase_letter>',
          Tree('"z"')
        )
      )
    ),
  ),
  Tree('","'),
  Tree('<age>',
    Tree('<digit>',
      Tree('"1"'),
    ),
    Tree('<digit>',
      Tree('"8"'),
    ),
  )
)
tree.visualize()
```

Note how the tree records the entire history of how it was created - how it was _derived_, actually.

To obtain a string from the tree, we traverse its children left-to-right,
ignoring all _nonterminal_ symbols (in `<...>`) and considering only the _terminal_ symbols (in quotes).
This is what we get for the above tree:

```text
Ex Pltz,18
```

And this is the string Fandango produces.
However, viewing the Fandango results as derivation trees allows us to access _elements_ of the Fandango-produced strings and to express _constraints_ on them.


### Diagnosing Derivation Trees

To examine the derivation trees that Fandango produces, use the [`--format=grammar` output format](sec:formats).
This produces the output in a grammar-like format, where children are indented under their respective parents.
As an example, here is how to print a derivation tree from `persons.fan`:

```shell
$ fandango fuzz -f persons.fan -n 1 --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
!PYTHONHASHSEED=0 fandango fuzz -f persons.fan -n 1 --format=grammar --random-seed 4712 
assert _exit_code == 0
```

We see how the produced derivation tree consists of a `<start>` symbol, whose `<first_name>` and `<last_name>` children expand into `<name>` and letters; the `<age>` symbol expands into `<digit>` symbols.

The comments (after `#`) show the individual positions into the input, as well as the values of compound symbols.

What is the full string represented by the above derivation tree?

```{admonition} Solution
:class: tip, dropdown
It's `'Pl Seov,5150'`, as you can find on the right-hand side of the first line.
```

```{tip}
The `--format=grammar` option is great for debugging, especially [binary formats](sec:binary).
```



## Specifying Paths

One effect of Fandango producing derivation trees rather than "just" strings is that we can define special _operators_ that allow us to access _subtrees_ (or sub-elements) of the produced strings - and express constraints on them.
This is especially useful if we want constraints to apply only in specific _contexts_ - say, as part of some element `<a>`, but not as part of an element `<b>`.

### Accessing Children

:::{margin}
These selectors are similar to XPath, but better aligned with Python.
In XPath, the first child has the index 1, in Fandango, it has the index 0.
:::

The expression `<foo>[N]` accesses the `N`-th child of `<foo>`, starting with zero.

If `<foo>` is defined in the grammar as

```python
<foo> ::= <bar> ":" <baz>
```

then `<foo>[0]` returns the `<bar>` element, `<foo>[1]` returns `":"`, and `<foo>[2]` returns the `<baz>` element.

In our [`persons.fan` derivation tree for `Ex Pltz`](sec:derivation-trees), for instance, `<start>[0]` would return the `<person_name>` element (`"Ex Pltz"`), and `<start>[2]` would return the `<age>` element (`18`).

We can use this to access elements in specific contexts.
For instance, if we want to refer to a `<name>` element, but only if it is the child of a `<first_name>` element, we can refer to it as `<first_name>[0]` - the first child of a `<first_name>` element:

```{code-cell}
:tags: ["remove-input"]
!grep '^<first_name>' persons.fan
```

Here is a constraint that makes Fandango produce first names that end with `x`:

:::{margin}
Since a `<first_name>` is defined to be a `<name>`, we could also write `<first_name>.endswith("x")`
:::

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>[0].endswith("x")'
```

% FIXME: does not work (bug #501)
% ```{code-cell}
% :tags: ["remove-input"]
% !fandango fuzz -f persons.fan -n 10 -c '<first_name>[0].endswith("x")' --validate
% assert _exit_code == 0
% ```

% This works
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>.endswith("x")' --validate
assert _exit_code == 0
```


```{tip}
As in Python, you can use _negative_ indexes to refer to the last elements.
`<age>[-1]`, for instance, gives you the _last_ child of an `<age>` subtree.
```

```{important}
While symbols act as strings in many contexts, this is where they differ.
To access the first _character_ of a symbol `<foo>`, you need to explicitly convert it to a string first, as in `str(<foo>)[0]`.
```

### Slices

:::{margin}
The Fandango slices maintain the property that `<name>[n:m]` = `<name>[n]` + `<name>[n + 1]` + ... + `<name>[m - 1]`, which holds for all sequences in Python.
:::


Fandango also allows you to use Python _slice_ syntax to access _multiple children at once_.
`<name>[n:m]` returns a new (unnamed) root which has `<name>[n]`, `<name>[n + 1]`, ..., `<name>[m - 1]` as children.
This is useful, for instance, if you want to compare several children against a string:

```shell
$ fandango fuzz -f persons-faker.fan -n 10 -c '<name>[0:2] == "Ch"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -n 10 -c '<name>[0:2] == "Ch"' --validate
assert _exit_code == 0
```

Would one also be able to use `<start>[0:2] == "Ch"` to obtain inputs that all start with `"Ch"`?

:::{admonition} Solution
:class: tip, dropdown
No, this would not work.
Remember that in derivation trees, indexes refer to _children_, not characters.
So, according to the rule

```
<start> ::= <person_name> "," <age>
```

`<start>[0]` is a `<person_name>`, `<start>[1]` is a `","`, and `<start>[2]` is an `<age>`.
Hence, `<start>[0:2]` refers to `<start>` itself, which cannot be `"Ch"`.
:::

Indeed, to have the _string_ start with `"Ch"`, you (again) need to convert `<start>` into a string first, and then access its individual characters:

```shell
$ fandango fuzz -f persons-faker.fan -n 10 -c 'str(<start>)[0:2] == "Ch"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -n 10 -c 'str(<start>)[0:2] == "Ch"' --validate
assert _exit_code == 0
```

:::{margin}
The Fandango slices maintain the property that `<name>[i:]` + `<name>[:i]` = `<name>`
:::

Fandango supports the full Python slice semantics:

* An omitted first index defaults to zero, so `<foo>[:2]` returns the first two children.
* An omitted second index defaults to the size of the string being sliced, so `<foo>[2:]` returns all children starting with `<foo>[2]`.
* Both the first and the second index can be negative again.



### Selecting Children

Referring to children by _number_, as in `<foo>[0]`, can be a bit cumbersome.
This is why in Fandango, you can also refer to elements by _name_.

:::{margin}
In XPath, the corresponding operator is `/`.
:::

The expression `<foo>.<bar>` allows accessing elements `<bar>` when they are a _direct child_ of a symbol `<foo>`.
This requires that `<bar>` occurs in the grammar rule defining `<foo>`:

```python
<foo> ::= ...some expansion that has <bar>...
```

To refer to the `<name>` element as a direct child of a `<first_name>` element, you thus write `<first_name>.<name>`.
This allows you to express the earlier constraint in a possibly more readable form:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>.<name>.endswith("x")'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>.<name>.endswith("x")' --validate
assert _exit_code == 0
```

% TODO: Is that so? -- AZ
```{note}
You can only access _nonterminal_ children this way; `<person_name>." "` (the space in the `<person_name>`) gives an error.
```



### Selecting Descendants

Often, you want to refer to elements in a particular _context_ set by the enclosing element.
This is why in Fandango, you can also refer to _descendants_.

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

Let us take a look at some rules in our `persons.fan` example:

```python
<first_name> ::= <name>
<last_name> ::= <name>
<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>+
<ascii_uppercase_letter> ::= "A" | "B" | "C" | ... | "Z"
```

To refer to all `<ascii_uppercase_letter>` element as descendant of a `<first_name>` element, you thus write `<first_name>..<ascii_uppercase_letter>`.

Hence, to make all uppercase letters `X`, but only as part of a first name, you may write

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>..<ascii_uppercase_letter> == "X"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>..<ascii_uppercase_letter> == "X"' --validate
assert _exit_code == 0
```

### Chains

You can freely combine `[]`, `.`, and `..` into _chains_ that select subtrees.
What would the expression `<start>[0].<last_name>..<ascii_lowercase_letter>` refer to, for instance?

```{admonition} Solution
:class: tip, dropdown
This is easy:

* `<start>[0]` is the first element of start, hence a `<person_name>`.
* `.<last_name>` refers to the child of type `<last_name>`
* `..<ascii_lowercase_letter>` refers to all descendants of type `<ascii_lowercase_letter>`
```

Let's use this in a constraint:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<start>[0].<last_name>..<ascii_lowercase_letter> == "x"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<start>[0].<last_name>..<ascii_lowercase_letter> == "x"' --validate
assert _exit_code == 0
```

(sec:quantifiers)=
## Quantifiers

By default, whenever you use a symbol `<foo>` in a constraint, this constraint applies to _all_ occurrences of `<foo>` in the produced output string.
For your purposes, though, one such instance already may suffice.
This is why Fandango allows expressing _quantification_ in constraints.

### Star Expressions

% ```{admonition} Under Construction
% :class: attention
% The `*` syntax is not operational yet.
% ```

In Fandango, you can prefix an element with `*` to obtain a collection of _all_ these elements within an individual string.
Hence, `*<name>` is a collection of _all_ `<name>` elements within the generated string.
This syntax can be used in a variety of ways.
For instance, we can have a constraint check whether a particular element is in the collection:

:::{margin}
Not every constraint that can be _expressed_ also can be _solved_ by Fandango.
:::

```python
"Pablo" in *<name>
```

This constraint evaluates to True if any of the values in `*<name>` (= one of the two `<name>` elements) is equal to `"Pablo"`.
`*`-expressions are mostly useful in quantifiers, which we discuss below.

### Existential Quantification

To express that within a particular scope, at least one instance of a symbol must satisfy a constraint, use a `*`-expression in combination with `any()`:

```python
any(CONSTRAINT for ELEM in *SCOPE)
```

where

* `SCOPE` is a nonterminal (e.g. `<age>`);
* `ELEM` is a Python variable; and
* `CONSTRAINT` is a constraint over `ELEM`

Hence, the expression

```python
any(n.startswith("A") for n in *<name>)
```

ensures there is at least _one_ element `<name>` that starts with an "A":

Let us decompose this expression for a moment:

* The expression `for n in *<name>` lets Python iterate over `*<name>` (all `<name>` objects within a person)...
* ... and evaluate `n.startswith("A")` for each of them, resulting in a collection of Boolean values.
* The Python function `any(list)` returns `True` if at least one element in `list` is True.

So, what we get is existential quantification:

```shell
$ fandango fuzz -f persons.fan -n 10 -c 'any(n.startswith("A") for n in *<name>)'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c 'any(n.startswith("A") for n in *<name>)' --validate
assert _exit_code == 0
```


### Universal Quantification

Where there are existential quantifiers, there also are _universal_ quantifiers.
Here we use the Python `all()` function; `all(list)` evaluates to True only if _all_ elements in `list` are True.

We use a `*`-expression in combination with `all()`:

```python
all(CONSTRAINT for ELEM in *SCOPE)
```

Hence, the expression

```python
all(c == "a" for c in *<first_name>..<ascii_lowercase_letter>)
```

ensures that _all_ sub-elements `<ascii_lowercase_letter>` in `<first_name>` have the value "a".

Again, let us decompose this expression:

* The expression `for c in *<first_name>..<ascii_lowercase_letter>` lets Python iterate over all `<ascii_lowercase_letter>` objects within `<first_name>`...
* ... and evaluate `c == "a"` for each of them, resulting in a collection of Boolean values.
* The Python function `all(list)` returns `True` if all elements in `list` are True.

So, what we get is universal quantification:

```shell
$ fandango fuzz -f persons.fan -n 10 -c 'all(c == "a" for c in *<first_name>..<ascii_lowercase_letter>)'
```

% FIXME: Not star syntax yet - see bug #502
% ```{code-cell}
% :tags: ["remove-input"]
% !fandango fuzz -f persons.fan -n 10 -c 'all(c == "a" for c in *<first_name>..<ascii_lowercase_letter>)'
% assert _exit_code == 0
% ```

% This works
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>..<ascii_lowercase_letter> == "a"' --validate
assert _exit_code == 0
```

By default, all symbols are universally quantified within `<start>`, so a dedicated universal quantifier is only needed if you want to _limit the scope_ to some sub-element.
This is what we do here with `<first_name>..<ascii_lowercase_letter>`, limiting the scope to `<first_name>`.

Given the default universal quantification, you can actually achieve the same effect as above without `all()` and without a `*`. How?

:::{admonition} Solution
:class: tip, dropdown
You can access all `<ascii_lowercase_letter>` elements within `<first_name>` directly:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>..<ascii_lowercase_letter> == "a"'
```

:::
