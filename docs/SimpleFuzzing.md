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

(sec:simple-fuzzing)=
# Simple Fuzzing with Fandango

Let us now come up with an input that is slightly more complex.
We want to create a set of inputs with _names of persons_ and their respective _age_.
These two values would be _comma-separated_, such that typical inputs would look like this:

```
Alice Doe,27
John Smith,45
...
```

This makes the overall format of our input look like this:

```
<start> ::= <person_name> "," <age>;
```

with `<age>` again being a sequence of digits, and a `<person>`'s name being defined as

```
<person_name> ::= <first_name> " " <last_name>;
```

where both first and last name would be a sequence of letters - first, an uppercase letter, and then a sequence of lowercase letters.
The full definition looks like this:

```{margin}
In Fandango specs, symbol names are formed as identifiers in Python - that is, they consist of letters, underscores, and digits.
```

```{margin}
In Fandango specs, every grammar rule must end with a semicolon.
```

```{code-cell}
:tags: ["remove-input"]
!cat persons.fan
```

Create or download a file [`persons.fan`](persons.fan) and run Fandango on it:

```shell
$ fandango fuzz -f persons.fan -n 10
```

Your output will look like this:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10
```


To create test inputs, Fandango needs a _Fandango spec_ – a file that describes how the input should be structured.

A Fandango specification contains three types of elements:

* A _grammar_ describing the _syntax_ of the inputs to be generated;
* Optionally, _constraints_ that specify additional properties; and
* Optionally, _definitions_ of functions and constants within these constraints.

Only the first of these (the _grammar_) is actually required.
Here is a very simple Fandango grammar that will get us started:


This grammar defines a _sequence of digits_:

* The first line in our grammar defines `<start>` – this is the input to be generated.
* What is `<start>`? This comes on the right-hand side of the "define" operator (`::=`).
* We see that `<start>` is defined as `<digit>+`, which means a non-empty sequence of `<digit>` symbols.
```{margin}
In Fandango grammars, you can affix these characters to a symbol:

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

Let us try this right away by _invoking Fandango_.