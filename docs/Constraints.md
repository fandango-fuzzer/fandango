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

(sec:constraints)=
# Shaping Inputs with Constraints

## The Limits of Grammars

So far, all the operations we have performed on our data were _syntax-oriented_ - that is, we could shape the format and structure of our values, but not their _semantics_ - that is, their actual meaning.
Consider our [Person/Age dataset from the previous section](sec:fuzzing).
What would we do if we want the "age" in a specific range?
Or we want it to be odd?
Or we want the age to be distributed in a certain way?

:::margin
All of this refers to _context-free grammars_, which are the ones Fandango uses.
:::

Some of these can be obtained by altering the grammar - limiting the age to two digits at most, for instance, will keep the value below 100 - but others cannot.
Properties that cannot be expressed in a grammar are called _semantic properties_ - in contrast to _syntactical properties_, which is precisely what grammars are good for.


## Specifying Constraints

Fandango solves this problem through a pretty unique feature: It allows users to specify _constraints_ which inputs have to satisfy. These thus narrow down the set of possible inputs.

Constraints are _predicates over grammar symbols_.
Essentially, you write a Boolean expression, using grammar symbols (in `<...>`) to refer to individual elements of the input.

As an example, consider this Fandango constraint:

```
int(<age>) < 50
```

This constraint takes the `<age>` element from the input and converts it into an integer (all symbols are strings in the first place).
Inputs are produced only if the resulting value is less than 50.


We can add such constraints to any .fan file, say the [`persons.fan`](persons.fan) file from the previous section.
Constraints are preceded by a keyword `where`.
So the line we add reads

```
where int(<age>) < 50
```

and the full `persons.fan` file reads

```{code-cell}
:tags: ["remove-input"]
!cat persons.fan; echo 'where int(<age>) < 50'
```

If we do this and run Fandango, we obtain a new set of inputs:

```shell
$ fandango fuzz -f persons.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c 'int(<age>) < 50' --validate
assert _exit_code == 0
```

We see that all persons produced now indeed have an age of less than 50.
Even if an age begins with `0`, it still represents a number below 50.

The language Fandango uses to express constraints is Python, so you can make use of arbitrary Python expressions.
For instance, we can use Python Boolean operators (`and`, `or`, `not`) to request values in a range of 25-45:

:::margin
Interestingly, having symbols in `<...>` does not conflict with the rest of Python syntax.
Be sure, though, to leave spaces around `<` and `>` operators to avoid confusion.
:::

```
25 <= int(<age>) and int(<age>) <= 45
```

and we obtain these inputs:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c '25 <= int(<age>) and int(<age>) <= 45' --validate
assert _exit_code == 0
```

Start with [`persons.fan`](persons.fan) and add a constraint such that we generate people whose age is a multiple of 7, as in

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 -c 'int(<age>) % 7 == 0' --validate
assert _exit_code == 0
```
(Hint: The modulo operator in Python is `%`).

:::{admonition} Solution
:class: tip, dropdown
This is not too hard. Simply add
```
where int(<age>) % 7 == 0
```
as a constraint.
:::

(sec:DerivationTree)=
## Constraints and `DerivationTree` types

Whenever Fandango evaluates a constraint, such as

```
int(<age>) > 20
```

the type of `<age>` is actually not a string, but a `DerivationTree` object - [a tree representing the structure of the output.](sec:paths). You can use `DerivationTree` objects as other basic python data types by converting them using (`int(<age>)`, `str(<age>)`, `bytes(<age>)`).

* You can then invoke most _string, bytes and int methods_ on them (`<age>.startswith('0')`) (see [Details](sec:derivation-tree-direct-access-functions))
* You can _compare_ them against each other (`<age_1> == <age_2>`) as well as against other strings (`<age> != "19"`)

One thing you _cannot_ do, though, is _passing them directly as arguments to functions_ that do not expect a `DerivationTree` type. This applies to the vast majority of Python functions.

```{important}
If you want to pass a symbol as a function argument, convert it to the proper type (`int(<age>)`, `float(<age>)`, `str(<age>)`) first.
Otherwise, you will likely raise an internal error in that very function.
```

```{important}
On symbols, the `[...]` operator operates differently from strings - it returns a _subtree_ of the produced output: `<name>[0]` returns the `<first_name>` element, not the first character.
If you want to access a character (or a range of characters) of a symbol, convert it into a string first, as in `str(<name>)[0]`.
```

We will learn more about derivation trees, `DerivationTree` types, and their operators in {ref}`sec:paths`.


## Constraints on the Command Line

If you want to experiment with constraints, keeping on editing `.fan` files is a bit cumbersome.
As an alternative, Fandango also allows to specify constraints on the command line.
This is done with the `-c` (constraint) option, followed by the constraint expression (typically in quotes).

Starting with the original [`persons.fan`](persons.fan), we can thus apply age constraints as follows:

```shell
$ fandango fuzz -f persons.fan -n 10 -c '25 <= int(<age>) and int(<age>) <= 45'
```

Constraints can be given multiple times, so the above can also be obtained as

```shell
$ fandango fuzz -f persons.fan -n 10 -c '25 <= int(<age>)' -c 'int(<age>) <= 45'
```

```{important}
On the command line, always put constraints in single quotes (`'...'`), as the angle brackets might otherwise be interpreted as I/O redirection.
```

When do constraints belong in a `.fan` file, and when on the command line?
As a rule of thumb:

* If a constraint is _necessary_ for obtaining valid input files (i.e. if the inputs would not be accepted otherwise), it belongs into the `.fan` file.
* If a constraint is _optional_, for instance for shaping inputs towards a particular goal, then it can also go on the command line.


## How Fandango Solves Constraints

How does Fandango obtain these inputs?
In a nutshell, Fandango is an _evolutionary_ test generator:

1. It first uses the grammar to generate a _population_ of inputs.
2. It then checks which individual inputs are _closest_ in fulfilling the given constraints.
For instance, for a constraint `int(<X>) == 100`, an input where `<X>` has a value of 90 is closer to fulfillment than one with value of, say 20.
:::margin
Selecting the best inputs is also known as "survival of the fittest"
:::
3. The best inputs are selected, the others are discarded.
4. Fandango then generates new _offspring_ by _mutating_ the remaining inputs, recomputing parts according to grammar rules.
It can also exchange parts with those from other inputs; this is called _crossover_.
5. Fandango then repeats Steps 2-4 until all inputs satisfy the constraints.

All of this happens within Fandango, which runs through these steps with high speed.
The `-v` option (verbose) produces some info on how the algorithm progresses:

```shell
$ fandango -v fuzz -f persons.fan -n 10 -c 'int(<age>) % 7 == 0'
```

```{code-cell}
:tags: ["remove-input", "scroll-output"]
!fandango -v fuzz -f persons.fan -n 10 -c 'int(<age>) % 7 == 0' --progress-bar=off
assert _exit_code == 0
```

```{note}
The `-v` option comes right after `fandango` (and not after `fandango fuzz`), as `-v` affects all commands (and not just `fuzz`).
```

(sec:progress-bar)=
## The Fandango Progress Bar

While Fandango is solving constraints, you may see a _progress bar_ in the terminal.
The progress bar looks like this:

![progress-bar](progress-bar.png)

The progress bar is composed of three parts.
On the leftmost side, we have the _Fandango logo_ ("💃 Fandango"), followed by a _generation counter_ ("6/500") showing how often (6) the population has evolved (out of a maximum 500).

Most of the line, however, is filled by a _fitness visualization_ illustrating how the fitness is distributed across the inputs in the population.
Each fraction of the line corresponds to an equal fraction of individual inputs.
Hence, a 1/70 of the line (typically one character) stands for 1/70 of the population.

The _color_ of each fraction how _fit_ the inputs in the fraction are - on a scale from _bright green_ (perfect fitness, fulfilling the given constraints) to _dark red_ (very little fitness, far away from fulfilling the constraints).
Depending on its capabilities, your terminal may also show shades between these colors.
Inputs that do not satisfy the constraints at all (zero fitness) are shown in gray.

In the above example, we can see that Fandango already has produces a few inputs that satisfy the constraints; a few more are close and may get there through further evolution.

```{note}
By default, the progress bar only shows up if

* Fandango's standard error is a terminal;
* Fandango is not run within Jupyter notebook (Jupyter cannot interpret the terminal escape sequences); and
* Fandango logging is turned off (it also writes to standard error).

The option `--progress-bar=on` turns on the progress bar even if the above conditions are not met.
The option `--progress-bar=off` turns the progress bar off.
```


(sec:soft-constraints)=
## Soft Constraints and Optimization

So far, we have seen constraints that _have_ to be satisfied for Fandango to produce a string.
On top, Fandango also supports so-called "soft" constraints that Fandango _aims_ to satisfy as good as it can.
These "soft" constraints come in two forms:

* **maximizing** constraints: These constraints specify an _expression_ whose value should be as _high_ as possible
* **minimizing** constraints: These constraints specify an expression whose value should be as _low_ as possible.

Such soft constraints are specified

* on the command line, using `--maximizing EXPR` and `--minimizing EXPR`, respectively; or
* in the `.fan` file, introducing them with `minimizing` and `maximizing` (instead of `where`), respectively.

If, for instance, you want Fandango to maximize the `<age>` field, you write

```shell
$ fandango fuzz -f persons.fan --maximize 'int(<age>)'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 --maximize 'int(<age>)' --progress-bar=off
assert _exit_code == 0
```

Conversely, minimizing the `<age>` field yields

```shell
$ fandango fuzz -f persons.fan --maximize 'int(<age>)'
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 --minimize 'int(<age>)' --progress-bar=off
assert _exit_code == 0
```

Alternatively, you could also add to the `.fan` file:

```python
maximizing int(<age>)
```

or

```python
minimizing int(<age>)
```

respectively.

To express optional goals (i.e., real "soft" constraints), simply use a _Boolean_ expressions as the expressions for `--maximize` or `--minimize`.
Then, Fandango will aim to maximize (or minimize) its value.

```{note}
Remember that in Python `True` is equivalent to 1, and `False` is equivalent to 0; therefore, "maximizing" a Boolean value means that Fandango will aim to solve it.
```

Here is an example of a "soft" Boolean constraints, aiming to obtain names that start with "F":

```shell
$ fandango fuzz -f persons.fan --maximize '<name>.startswith("A")' -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan --maximize '<name>.startswith("A")' -n 10 --progress-bar=off
assert _exit_code == 0
```

As you see, "soft" constraints are truly optional :-)



## When Constraints Cannot be Solved

Normally, Fandango continues evolving the population until all inputs satisfy the constraints.
Some constraints, however, may be difficult or even impossible to solve.
After a maximum number of generations (which can be set using `-N`), Fandango stops and produces the inputs it has generated so far.
We can see this if we specify `False` as a constraint:

:::{margin}
The `-N` option limits the number of generations - the default is 500.
:::

```shell
$ fandango -v fuzz -f persons.fan -n 10 -c 'False' -N 50
```

```{code-cell}
:tags: ["remove-input", "scroll-output"]
!fandango -v fuzz -f persons.fan -n 10 -c 'False' -N 50 --validate --progress-bar=off
assert _exit_code == 0
```

As you see, Fandango produces a population of zero.
Of course, if the constraint is `False`, then there can be no success.

```{tip}
Fandango has a `--best-effort` option that allows you to still output the final population.
```
