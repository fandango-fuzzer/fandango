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

(sec:hatching)=
# Hatching Specs

Fandango provides an `include()` function that you can use to _include_ existing Fandango content.
This allows you to distribute specifications over multiple files, defining _base_ specs whose definitions can be further _refined_ in specs that use them.


## Including Specs with `include()`

Specifically, in a `.fan` file, a call to `include(FILE)`

1. Finds and loads `FILE` (typically [in the same location as the including file](sec:including))
2. Executes the _code_ in `FILE`
3. Parses and adds the _grammar_ in `FILE`
4. Parses and adds the _constraints_ in `FILE`.

The `include()` function allows for _incremental refinement_ of Fandango specifications - you can create some base `base.fan` spec, and then have more _specialized_ specifications that alter grammar rules, add more constraints, or refine the code.


## Incremental Refinement

Let us assume you have a _base_ spec for a particular format, say, `base.fan`.
Then, in a _refined_ spec (say, `refined.fan`) that _includes_ `base.fan`, you can

* override _grammar definitions_, by redefining rules;
* override _function and constant definitions_, by redefining them; and
* add additional _constraints_.

As an example, consider our `persons.fan` [definition of a name database](sec:fuzzing).
We can create a more specialized version [`persons50.fan`](persons50.fan) by including `persons.fan` and adding a [constraint](sec:constraints):

```{code-cell}
:tags: ["remove-input"]
!cat persons50.fan
```

Likewise, we can create a specialized version [`persons-faker.fan`](persons-faker.fan) that uses [fakers](sec:generators) by overriding the `<first_name>` and `<last_name>` definitions:

```{code-cell}
:tags: ["remove-input"]
!cat persons-faker.fan
```

The _include_ mechanism thus allows us to split responsibilities across multiple files:

* We can have one spec #1 with basic definitions of individual elements
* We can have a spec #2 that uses (includes) these basic definitions from spec #1 to define a _syntax_
* We can have a spec #3 that refines spec #2 to define a specific format for a particular program or device
* We can have a spec #4 that refines spec #3 towards a particular testing goal.

These mechanisms are akin to _inheritance_ and _specialization_ in object-oriented programming.

```{tip}
Generally, Fandango will warn about unused symbols, but not in an included `.fan` file.
```


## Crafting a Library

If you create multiple specifications, you may wonder where best to store them.
The [rules for where Fandango searches for included files](sec:including) are complex, but they boil down to two simple rules:

```{tip}
Store your included Fandango specs either
* in the directory where the _including_ specs are, or
* in `$HOME/.local/share/fandango` (or `$HOME/Library/Fandango` on a Mac).
```


## `include()` vs. `import`

Python provides its own import mechanism for referring to existing features.
In general, you should use

* `import` whenever you want to make use of Python functions; and
* `include()` only if you want to make use of Fandango features.

```{important}
Using `include` for _pure Python code_, as in `include('code.py')` is not recommended.
Most importantly, the current Fandango implementation will process "included" Python code only _after_ all code in the "including" spec has been run. In contrast, the effects of `import` are immediate.
```

