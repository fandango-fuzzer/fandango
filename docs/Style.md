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

(sec:style)=
# Fandango Style Guide

Let us assume you want to go beyond toying with Fandango, and write Fandango specifications that are

* reusable;
* extensible;
* efficient; and
* useful for others.

This style guide describes some principles we have found useful for this task. Enjoy!

```{note}
This style guide is work in progress, and likely to be extended over time.
```


## Managing `.fan` Files

### How to Name `.fan` Files

A `.fan` file name should start with the format name (typically the file extension), optionally followed by `-` and additional details, such as

```
ical.fan
gif89a-v1.fan
svg-general.fan
```

### How to State Metadata

At the beginning of a `.fan` file, state

* the name of the format
* the format version, if any
* associated file extensions
* your name and contact info :-)
* the resources you used to create the format (the official spec); if possible, with URLs
* further details on capabilities (and non-capabilities)

Here is an example. The capability lines state what your spec actually does,
which is not necessarily everything the format allows:

```
# GIF89a format
# Version: 1

# Extensions: .gif

# Authors:
# * John Smith <smith@example.com>

# Sources:
# * W3 GIF spec, https://www.w3.org/Graphics/GIF/spec-gif89a.txt
# * Sweetscape GIF binary template, https://www.sweetscape.com/010editor/repository/templates/file_info.php?file=GIF.bt

# Details:
# * The spec can parse any valid GIF file.
# * Only 1x1 pixel GIFs can be produced at this time.
```

```{note}
Future Fandango versions will establish a standard for providing such metadata.
```

(sec:specialized_variant)=
### Managing Format Variants

For significant variants of a format, have them build on each other.
For instance, to disable an extension `<extension>` in an original specification, create a `specialized-format.fan` that says:

```python
# Specialized format

include ("full-format.fan")
<extension> ::= ''
```

In a similar vein, you can also create simple variants first that have some placeholder (conveniently defined with some "empty" value) which is then defined in a _generalized_ variant.

```python
# Generalized format

include ("simple-format.fan")
<extension> ::= ...  # Details go here
```

For details on file inclusion, extension, and generalization, see {ref}`sec:hatching`.


## Naming and Format Conventions

### How to Format Grammars

Present rules in a top-down style, e.g. starting with `<start>` (describing the overall structure) and then going down into details of the individual constituents.
First list the format's major sections or element types, then write rules for each; keep on refining.

You _can_ use indentation to express hierarchies, such as

```
<foo> ::= <bar> <qux> <quux>
  <bar> ::= ...
  <qux> ::= ...
  <quux> ::= ...
```

However, applying this style across the entire grammar can quickly lead to high indentation levels.
If you break down your grammar into individual sections, have each section again begin on column 1.

### Use Correct Fandango Syntax

Here are the most important Fandango syntax rules:

```
     <NT> ::= ALT_1 | ALT_2    productions / alternatives
     "..."  r'...'  b'...'     string literal / regex / bytes object
     *  +  ?  {N,M}            repetition
     := PYTHON_EXPR            generator (default value)
     where PYTHON_EXPR         constraint (cast symbols: str(), int(), len())
```

* Every rule ends in a newline. Avoid ending rules in `;`. Do not concatenate rules with `;` on the same line.
* Split long rules by placing them into parentheses `(...)` or use a trailing `\`.
A bare line break silently truncates the rule.
* Never put a literal newline inside a short string (`'...'`); use `\n` or a `'''triple-quoted'''` string instead.
* Comments (`#`) extend until the end of the line, so finish the rule before commenting.
* Use `lowercase_identifiers` for nonterminals.
* Use `CapWords` for protocol parties (notably because they are Python classes).
* Do not prefix identifiers with `_`, as these are defined for internal Fandango use.
* Stick to ASCII letters and numbers for all identifiers.

For details on syntax, see {ref}`sec:language`.


### Avoid Naming Conflicts

Grammars have a _global_ naming scope, so do not define the same element multiple times.
If an element like `<checksum>` or `<length>` appears in multiple
contexts `C`, give it a separate prefix for each context: `<C_checksum>` and `<C_length>`.


### Cover the Entire Specification

Do not just produce a toy subset, but go for maximum coverage of the respective language or protocol.
Share only specifications that define the vast majority of format features.

```{tip}
Document missing parts with `TODO`, `FIXME` and alike, both in the appropriate parts of the spec as well as under "Details" at the beginning of the file.
```


### Follow Python Style Conventions

Unless otherwise stated, stick to Python conventions for writing your specifications.
This includes

* code layout (4 spaces indentation; max line length 88 characters, matching our Ruff configuration);
* usage of blank lines (to separate larger grammar blocks);
* source file encoding (should be UTF-8);
* whitespace in expressions and statements; and
* naming conventions for Python elements.

See the [Style Guide for Python Code](https://peps.python.org/pep-0008/) for details.

## Repetitions and Length Encodings

### Use Repetitions Wherever Possible

Prefer `+` and `*` to denote repetitions, and `?` to denote optional elements.
Avoid modeling repetition by means of the grammar.
See {ref}`sec:repeat` for details.

### Use Regular Expressions for Simple Elements

For elements that are all equivalent from a testing perspective (and hence do not require exploration of alternatives), prefer regular expressions (using `r"expr"`) over grammar forms.
See {ref}`sec:regexes` for details.


### Use Explicit Length Encodings

If you know the length of a field is `N` bytes, use `<byte>{N}` instead of `<byte>*` or an associated constraint.

You can also use `<byte>{EXPR}`, where `EXPR` is computed from other elements (say, a preceding length value).
See {ref}`sec:length_encodings` for details.



## Using Constraints

### Use Constraints to Enforce Semantics

Wherever possible, use `where` constraints to enforces semantic properties. These include

* ranges;
* enumerations;
* relationships between symbols (e.g. a length symbol matching the size of a related payload);
* nestings; and
* checksums.

Break down constraints into individual `where` clauses as much as possible.
This makes it easier for Fandango to solve them one by one.

For details on constraints, see {ref}`sec:constraints` and {ref}`sec:generators`.
See also {ref}`sec:checksums` on how to specify checksums.


### Use Constructive Helper Functions

Use constructive helper functions (rather than checking helper functions)
whenever possible.
In Fandango, a constraint of the form

```python
<NT> == compute(...)
```

can be very efficiently "solved" - by evaluating `compute(...)` and ensuring that `<NT>` is associated with the resulting value.

This is in contrast to a "checking" predicate

```python
ok(<NT>, ...)
```

where Fandango must make use of slower algorithms to find proper values for `<NT>` until `ok(...)` is finally satisfied.


### Prefer Inline Expressions over Function Definitions

Prefer a `where` clause or an inline Python expression directly in the grammar over introducing named Python functions.

Function definitions are justified _only_ when the computation is genuinely too complex to write as one `where` expression or one `:=` expression inline (e.g. a real multi-step checksum algorithm) — never merely because a value is "random," reused in several places, or convenient to name.


### Prefer Constraints over Generators

Do _not_ use a `:=` generator and helper function as a workaround to avoid writing a `where` constraint.
If two symbols must agree (e.g. a length symbol and the actual length of some payload), express that agreement as a `where` equality between the two, not by generating both from one Python-side random computation that merely happens to keep them in sync.

For details on generators (and when to use them), see {ref}`sec:generators`.


### Use Generators only where Appropriate

Generators (`:=`) are for producing a value with no other constraint attached (a free choice).
Constraints (`where`) are for relationships between two or more parts of the grammar.
Do not blur the two to dodge writing the (more verbose but more correct) constraint form.

For details on generators (and when to use them), see {ref}`sec:generators`.


## Quality Assurance

### Verify your Specification with Fandango

Your spec should actually be verified to work, not just be plausible-looking.
With your spec in `SPEC.fan` producing files with an extension `EXTENSION`, run

```shell
$ fandango fuzz -f SPEC.fan -n 10 -d out -x .EXTENSION --warnings-are-errors
```

For GIF files in `gif.fan`, this would be:
```shell
$ fandango fuzz -f gif.fan -n 10 -d out -x .gif --warnings-are-errors
```

Ensure that

* the Fandango exit code is 0;
* Fandango does not produce warnings or error messages; and
* `out/` has exactly 10 files.

If not, fix and re-run.

For details on how to invoke Fandango, see {ref}`sec:invoking` and {ref}`sec:commands`.


### Verify your Outputs with a Processing Program

Feed your generated inputs into a program that should process them.
If inputs are rejected, you should adapt the spec accordingly.

```{note}
It is common that specs describe features that are not supported by the program under test (and thus rejected).
In that case, produce a _specialized_ specification for the program to test with;
see {ref}`sec:specialized_variant` for details.
```
