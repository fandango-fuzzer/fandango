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

```{error}
This chapter is still in construction.
```

## The `include()` Function

Fandango provides an `include()` function that you can use to _include_ existing Fandango content.
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


## Crafting a Library

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

:::{warning}
Using `include` for Python code, as in `include('code.py')` is not recommended.
Most importantly, the current Fandango implementation will process "included" Python code only _after_ all code in the "including" spec has been run. In contrast, the effects of `import` are immediate.
:::

