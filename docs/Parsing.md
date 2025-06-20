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

(sec:parsing)=
# Parsing Inputs

Fandango can also use its specifications to _parse_ given inputs and to _check_ if they conform to the specification - both

* _syntactically_ (according to the grammar); and
* _semantically_ (according to the constraints).

Fandango uses this ability extensively for [checking outputs](sec:outputs) and [protocol testing](sec:protocols).
In this section, we cover the basics of parsing.


## The `parse` command

To parse an existing input, Fandango provides a `parse` command.
Its arguments are any _files_ to be parsed; if no files are given, `parse` reads from standard input.
As with the `fuzz` command, providing a specification (with `-f FILE.fan`) is mandatory.

Let us use `parse` to check some dates against the [ISO 8601 format](sec:iso8601) we have written a Fandango spec for.
The command `echo -n` outputs the string given as argument (`-n` suppresses the newline it would normally produce); the pipe symbol `|` feeds this as input into Fandango:

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-01-27' | fandango parse -f iso8601.fan
assert _exit_code == 0
```

If we do this, nothing happens.
That is actually a good sign: it means that Fandango has successfully parsed the input.


If we pass an _invalid_ input, however, Fandango will report this.
This holds for _syntactically_ invalid inputs:

```shell
$ echo -n '01/27/2025' | fandango parse -f iso8601.fan
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '01/27/2025' | fandango parse -f iso8601.fan
assert _exit_code == 1
```

And also for _semantically_ invalid inputs:

```shell
$ echo -n '2025-02-29' | fandango parse -f iso8601.fan
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-02-29' | fandango parse -f iso8601.fan
assert _exit_code == 1
```

In both cases, the return code will be non-zero:

```shell
$ echo $?
1
```


## Validating Parse Results

By default, the `parse` command produces no output.
However, to inspect the parse results, you can output the parsed string again.
The `-o FILE` option writes the parsed string to `FILE`, with `-` being the standard output.

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan -o -
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan -o -
assert _exit_code == 0
```

We see that input and output are identical (as should always be with parsing and unparsing).

```{tip}
As it comes to producing and storing outputs, the `parse` command has the same options as the `fuzz` command.
```

Since parsing and unparsing should always be symmetrical to each other, Fandango provides a `--validate` option to run this check automatically:

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan --validate
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan --validate
assert _exit_code == 0
```

Again, if nothing happens, then the (internal) check was successful.

The `--validate` option can also be passed to the `fuzz` command; here, it ensures that the produced string can be parsed by the same grammar (again, as should be).

```{important}
If you find that `--validate` fails, please report this as a Fandango bug.
```

(sec:formats)=
## Alternate Output Formats

In order to debug grammars, Fandango provides a number of _alternate_ formats in which to output the parsed tree, controlled by the `--format` flag.

### String

The option `--format=string` outputs the parsed tree as a string. This is the default.

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan -o - --format=string
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan -o - --format=string
assert _exit_code == 0
```


### Tree

The option `--format=string` outputs the parsed tree as a Python `Tree()` expression. This is useful for evaluating and visualizing the tree.

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan -o - --format=tree
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan -o - --format=tree
assert _exit_code == 0
```

Here comes this tree, visualized:
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


### Grammar

The option `--format=grammar` outputs the parsed tree as a (highly specialized) grammar, in which
children are indented under their respective parents.
This is useful for debugging, but also for creating a grammar from a sample file and then generalizing it.

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan -o - --format=grammar
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan -o - --format=grammar
assert _exit_code == 0
```

### Bits

The option `--format=bits` outputs the parsed tree as a bit sequence.

```shell
$ echo -n '2025-01-27' | fandango parse -f iso8601.fan -o - --format=bits
```

```{code-cell}
:tags: ["remove-input"]
!echo -n '2025-10-27' | fandango parse -f iso8601.fan -o - --format=bits
assert _exit_code == 0
```

This is useful for debugging [binary formats](sec:binary) that contain [bits](sec:bits).