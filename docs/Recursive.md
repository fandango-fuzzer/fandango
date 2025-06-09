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

(sec:recursive)=
# Complex Input Structures

The _context-free grammars_ that Fandango uses can specify very complex input formats.
In particular, they allow specifying _recursive_ inputs - that is, element types that can contain other elements of the same type again.
In this chapter, we explore some typical patterns as they occur within grammars.




## Recursive Inputs

A textbook example of a recursive input formats is an _arithmetic expression_.
Consider an operation such as addition (`+`).
Its operands can be _numbers_ (`3 + 5`), but can also be _other expressions_, as in `2 + (3 - 8)`.
In a grammar for arithmetic expressions, this relationship is expressed as a rule

:::{margin}
Why don't we write `<expr> ::= <expr> " + " <expr>;` here?
If we did that, a string such as `1 + 2 + 3` would become _ambiguous_: 
it will either be interpreted
(1) as `(1 + 2) + 3` – that is, the left `<expr>` becomes `1 + 2`, and the right `<expr>` becomes `3`; or
(2) as `1 + (2 + 3)` - that is, the left `<expr>` becomes `1`, and the right `<expr>` becomes `2 + 3`.
Such ambiguities may not be important in _producing_ inputs.
But when _parsing_ inputs, any ambiguities lead to interpretation and performance problems.
:::

```
<expr> ::= <term> " + " <expr>
```

which indicates that the right-hand side of the addition `+` operator can be _another expression_.
This is an example of a _recursive_ grammar rule - a rule where an expansion refers back to the defined symbol.

Let us add a definition for `<term>`, too, defining it as a number:

```
<term> ::= <number>
<number>  ::= <digit>+
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

What is it that `<expr>` can now expand into?
Have a look at the above rule first, and then check out the solution.

:::{admonition} Solution
:class: tip, dropdown
Actually, the above rules mean that `<expr>` would expand into an infinitely long string `<term> + <term> + <term> + ...`
:::

What we have here is a case of _infinite recursion_ – the string would keep on expanding forever.


% TODO
```{important}
At this time, Fandango does not detect infinite recursions; it keeps running until manually stopped.
```

In order to avoid infinite recursion, we need to provide a _non-recursive alternative_, as in:

```
<expr> ::= <term> " + " <expr> | <term>
```

With this rule, we can now store the above definitions in a `.fan` file [additions.fan](additions.fan) and get Fandango running:

```
$ fandango fuzz -f additions.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f additions.fan -n 10 --validate
assert _exit_code == 0
```

We see that the above rules yield nice (recursive) chains of additions.

```{important}
For each recursion in the grammar, there must be a non-recursive alternative.
```


## More Repetitions

In our definition of `<number>`, above, we used the `+` operator to state that an element should be repeated:

```
<number> ::= <digit>+
```

Instead of using the `+` operator, though, we can also use a recursive rule.
How would one do that?

:::{margin}
We could also write
```
<number> ::= <number> <digit> | <digit>
```
However, if the recursive element is the _last_ in a rule, this allows for more efficient parsing.
We prefer such _tail recursion_ whenever we can.
:::

:::{admonition} Solution
:class: tip, dropdown
Here's an equivalent `<number>` definition that comes without `+`:
```
<number> ::= <digit> <number> | <digit>
```
:::

Indeed, we can define a `<number>` as a `<digit>` that is followed by another "number".

```{tip}
Using shorthands such as `*`, `+`, and `?` can make Fandango parsers more efficient.
```


## Arithmetic Expressions

Let us put all of the above together into a grammar for arithmetic expressions.
[expr.fan](expr.fan) defines additional operators (`-`, `*`, `/`), unary `+` and `-`, as well as subexpressions in parentheses.
It also ensures the conventional [order of operations](https://en.wikipedia.org/wiki/Order_of_operations), giving  multiplication and division a higher rank than addition and subtraction.
Hence, `2 * 3 + 4` gets interpreted as `(2 * 3) + 4` (10), not `2 * (3 + 4)` (14).

```{code-cell}
:tags: ["remove-input"]
!cat expr.fan
```

These are the expressions we get from this grammar:

```
$ fandango fuzz -f expr.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f expr.fan -n 10 --validate
assert _exit_code == 0
```

We see that the resulting expressions can become quite complex.
If we had an arithmetic evaluation to test – say, from a programming language - these would all make a good start.

:::{margin}
Early Python versions interpreted zero-leading numbers as _octal_ numbers,
so `011` would evaluate to 9 (not 11).
This was prone to errors, so in today's Python, octal numbers need a `0o` prefix (as in `0o11`), and `0` prefixes yield an error.
:::

There are two ways we can still improve the grammar, though.

1. First, many programming languages assign a special meaning to _numbers starting with zero_, so we'd like to get rid of these.
2. Second, we only have _integers_ so far. How would one go to extend the grammar with _floating-point numbers_?

Try this out for yourself by extending the above grammar.

:::{admonition} Solution
:class: tip, dropdown
To get rid of numbers starting with `0`, we can introduce a `<lead_digit>`:
```
<int> ::= <digit> | <lead_digit> <digits>
<lead_digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```
Note that the option of having a single `0` as an `<int>` is still there, as a `<digit>` can expand into any digit.

To include floating-point numbers, we can add a `<float>` element:
```
<float> ::= <int> "." <digits>
```
Feel free to further extend this - say, with an optional exponent, or by making the `<int>` optional (`.001`).
:::

The resulting grammar [`expr-float.fan`](expr-float.fan) produces all-valid numbers:

```shell
$ fandango fuzz -f expr-float.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f expr-float.fan -n 10 --validate
assert _exit_code == 0
```

With extra constraints, we can now have Fandango produce only expressions that satisfy further properties – say, evaluate to a value above 1000 in Python:

```shell
$ fandango fuzz -f expr-float.fan -n 10 -c 'eval(str(<start>)) > 1000'
```

```{code-cell}
:tags: ["remove-input", "remove-stderr"]
!fandango fuzz -f expr-float.fan -n 10 -c 'eval(str(<start>)) > 1000' --validate 2> /dev/null
assert _exit_code == 0
```

Note that some of these expressions raise divisions by zero errors:

```
ZeroDivisionError: float division by zero
```

In the next section, we'll talk about [accessing input elements](sec:paths) in complex inputs, so we can impose further constraints on them.

