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

```
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
% import os
% os.chdir('../src')
% from fandango.language.tree import DerivationTree

```{code-cell}
:tags: ["remove-input"]
tree = \
Tree('<start>',
  Tree('<person_name>',
    Tree('<first_name>',
      Tree('<name>',
        Tree('<uppercase_letter>',
          Tree('"E"')
        ),
        Tree('<lowercase_letter>',
          Tree('"x"')
        )
      )
    ),
    Tree('" "'),
    Tree('<last_name>',
      Tree('<name>',
        Tree('<uppercase_letter>',
          Tree('"P"')
        ),
        Tree('<lowercase_letter>',
          Tree('"l"')
        ),
        Tree('<lowercase_letter>',
          Tree('"t"')
        ),
        Tree('<lowercase_letter>',
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

```
Ex Pltz,18
```

And this is the string Fandango produces.
However, viewing the Fandango results as derivation trees allows us to access _elements_ of the Fandango-produced strings and to express _constraints_ on them.



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

```
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

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>[0].endswith("x")'
```

:::{note}
As in Python, you can use _negative_ indexes to refer to the last elements.
`<age>[-1]`, for instance, gives you the _last_ child of an `<age>` subtree.
:::

:::{warning}
While symbols act as strings in many contexts, this is where they differ.
To access the first _character_ of a symbol `<foo>`, you need to explicitly convert it to a string first, as in `str(<foo>)[0]`.
:::


### Selecting Children

Referring to children by _number_, as in `<foo>[0]` can be a bit cumbersome.
This is why in Fandango, you can also refer to elements by _name_.

:::{margin}
In XPath, the corresponding operator is `/`.
:::

The expression `<foo>.<bar>` allows accessing elements `<bar>` when they are a _direct child_ of a symbol `<foo>`.
This requires that `<bar>` occurs in the grammar rule defining `<foo>`:

```
<foo> ::= ...some expansion that has <bar>...
```

To refer to the `<name>` element as a direct child of a `<first_name>` element, you thus write `<name>.<first_name>`.
This allows you to express the earlier constraint in a possibly more readable form:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>.<name>.endswith("x")'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>.<name>.endswith("x")'
```

% TODO: Is that so? -- AZ
:::{note}
You can only access _nonterminal_ children this way; `<person_name>." "` (the space in the `<person_name>`) gives an error.
:::


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

Let us take a look at some of the rules in our `persons.fan` example:

```
<first_name> ::= <name>;
<last_name> ::= <name>;
<name> ::= <uppercase_letter><lowercase_letter>+;
<uppercase_letter> ::= "A" | "B" | "C" | ... | "Z";
```

To refer to all `<uppercase_letter>` element as descendant of a `<first_name>` element, you thus write `<first_name>..<uppercase_letter>`.

Hence, to make all uppercase letters `X`, but only as part of a first name, you may write

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>..<uppercase_letter> == "X"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>..<uppercase_letter> == "X"'
```


### Chains

You can freely combine `[]`, `.`, and `..` into _chains_ that select subtrees.
What would the expression `<start>[0].<last_name>..<lowercase_letter>` refer to, for instance?

:::{admonition} Solution
:class: tip, dropdown
This is easy:
* `<start>[0]` is the first element of start, hence a `<person_name>`.
* `.<last_name>` refers to the child of type `<last_name>`
* `..<lowercase_letter>` refers to all descendants of type `<lowercase_letter>`
:::

Let's use this in a constraint:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '<start>[0].<last_name>..<lowercase_letter> == "x"'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<start>[0].<last_name>..<lowercase_letter> == "x"'
```



## Quantifiers

By default, whenever you use a symbol `<foo>` in a constraint, this constraint applies to _all_ occurrences of `<foo>` in the produced output string.
For your purposes, though, one such instance already may suffice.
This is why Fandango allows to express _quantifiers_ in constraints.

### Existential Quantifiers

To express that within a particular scope, at least one instance of a symbol should satisfy a constraint, write

```
exists SYMBOL in SCOPE: CONSTRAINT
```

where `SYMBOL` and `SCOPE` are nonterminals (e.g. `<age>`) and `CONSTRAINT` is a constraint.

Hence, the expression

```
exists <name> in <start>: <name>.startswith("A")
```

ensures there is at least _one_ subelement `<name>` of `<start>` that starts with an "A":

```shell
$ fandango fuzz -f persons.fan -n 10 -c 'exists <name> in <start>: <name>.startswith("A")'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c 'exists <name> in <start>: <name>.startswith("A")'
```

### Universal Quantifiers

Where there are existential quantifiers, there also are _universal_ quantifiers.
The syntax is 

```
forall SYMBOL in SCOPE: CONSTRAINT
```

where `SYMBOL` and `SCOPE` are nonterminals (e.g. `<age>`) and `CONSTRAINT` is a constraint.

Hence, the expression

```
forall <lowercase_letter> in <first_name>: <lowercase_letter> == "a"
```

ensures that _all_ subelements `<lowercase_letter>` in `<first_name>` have the value "a":

```shell
$ fandango fuzz -f persons.fan -n 10 -c 'forall <lowercase_letter> in <first_name>: <lowercase_letter> == "a"'
```

% FIXME: This does not work yet (#119) - AZ
% ```{code-cell}
% :tags: ["remove-input"]
% !fandango fuzz -f persons.fan -n 10 -c 'forall <lowercase_letter> in <first_name>: <lowercase_letter> == "a"'
% ```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '<first_name>..<lowercase_letter> == "a"'
```

By default, all symbols are universally quantified within `<start>` (as in `forall SYMBOL in <start>: ...`), so a universal quantifier is only needed if you want to limit the scope to some sub-element.

You can actually achieve the same effect as above without `forall`. How?

:::{admonition} Solution
:class: tip, dropdown
You can use a `..` selector to access all `<lowercase_letter>` elements within `<first_name>`:
```
$ fandango fuzz -f persons.fan -n 10 -c '<first_name>..<lowercase_letter> == "a"'
```
:::


## Implications

Finally, Fandango supports _implications_ - that is, constraints that only need to hold if some other constraint is met.
The syntax is

```
ANTECEDENT -> CONSEQUENCE
```

where `ANTECEDENT` and `CONSEQUENCE` are constraints.
If `ANTECEDENT` is met, then `CONSEQUENCE` must also be met.

Hence, the expression

```
int(<age>) > 30 -> <first_name>.startswith("A")
```

ensures that if a person is aged more than 30, then their first name should start with an `"A"`.
Let's try this:

```shell
$ fandango fuzz -f persons.fan -n 10 -c 'int(<age>) > 30 -> <first_name>.startswith("A")'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c 'int(<age>) > 30 -> <first_name>.startswith("A")'
```

Note how Fandango "solves" the problem by mostly producing only persons whose age is _below_ the threshold.
But if we have the age come from a Gaussian distribution, as discussed in {ref}`sec:generators`, we get

```shell
$ fandango fuzz -f persons-faker-gauss.fan -n 10 -c 'int(<age>) > 30 -> <first_name>.startswith("A")'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker-gauss.fan -n 10 -c 'int(<age>) > 30 -> <first_name>.startswith("A")'
```

While the implication is indeed resolved, note that the Gaussian distribution no longer holds.
We will revisit this issue in {ref}`sec:distributions`, when we specify targets that must hold for the entire population.