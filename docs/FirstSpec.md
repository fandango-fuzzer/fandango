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

(sec:first-spec)=
# A First Fandango Spec

To create test inputs, Fandango needs a _Fandango spec_ – a file that describes how the input should be structured.

A Fandango specification contains three types of elements:

* A _grammar_ describing the _syntax_ of the inputs to be generated;
* Optionally, _constraints_ that specify additional properties; and
* Optionally, _definitions_ of functions and constants within these constraints.

Only the first of these (the _grammar_) is actually required.

```{margin}
For writing extended Fandango Specs, check out our [Fandango language server and an IDE extension](sec:language-server).
```

Here is a very simple Fandango grammar that will get us started:

```{code-cell}
:tags: ["remove-input"]
!cat digits.fan
```

This grammar defines a _sequence of digits_:

* The first line in our grammar defines `<start>` – this is the input to be generated.
* What is `<start>`? This comes on the right-hand side of the "define" operator (`::=`).
* We see that `<start>` is defined as `<digit>+`, which means a non-empty sequence of `<digit>` symbols.
```{margin}
In Fandango grammars, you can append these operators to a symbol:

* `+` indicates _one or more_ repetitions;
* `*` indicates _zero or more_ repetitions; and
* `?` indicates that the symbol is _optional_.
```
* What is a `<digit>`? This is defined in the next line: one of ten alternative strings, separated by `|`, each representing a single digit.

To produce inputs from the grammar, Fandango

* starts with the start symbol (`<start>`)
* repeatedly replaces symbols (in `<...>`) by _one of their definitions_ (= one of the alternatives separated by `|`) on the right-hand side;
* until no symbols are left.

So,

* `<start>` first becomes `<digit><digit><digit>...` (any number of digits, but at least one);
* each `<digit>` becomes a digit from zero to nine;
* and in the end, we get a string such as `8347`, `66`, `2`, or others.

Let us try generating inputs with this right away by [_invoking Fandango_](sec:Invoking).