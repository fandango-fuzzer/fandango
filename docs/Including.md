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

(sec:including)=
# Including Specs

## The `include()` Function

Fandango provides an `include()` function that you can use to _include_ existing Fandango content.
Specifically, a call to `include(FILE)`

1. Finds and loads `FILE` (typically in the same location as the including file; see below)
2. Executes the _code_ in `FILE`
3. Parses and adds the _grammar_ in `FILE`
4. Parses and adds the _constraints_ in `FILE`.

This allows for _incremental refinement_ of Fandango specifications - you can create some base `base.fan` spec, and then have more _specialized_ specifications that

* override _grammar definitions_, by redefining rules;
* override _function and constant definitions_, by redefining them; and
* add additional _constraints_.


## `include()` vs. `import`

Python provides its own import mechanism for referring to existing features.
In general, you should use

* `import` whenever you want to make use of Python functions; and
* `include()` whenever you want to make use of Fandango features.

:::{warning}
Using `include` for Python code, as in `include('code.py')` is not recommended.
Most importantly, the "included" Python code may only be processed after code in the "including" file, which is different from Python.
:::


## Where Fandango Files are Found

The `include()` function searches for Fandango files in a number of locations.

```{tip}
Store your included Fandango specs either
* in the directory where the _including_ specs are, or
* in `$HOME/.local/share/fandango` (or `$HOME/Library/Fandango` on a Mac).
```

The actual rules for where Fandango searches for included files are complex, versatile, and adhering to common standards.
When including a `.fan` file using `include()`, Fandango searches for `.fan` files in the following locations, in this order:

1. In any directory `DIR` explicitly specified by `-I DIR` or `--include-dir DIR`.
2. In any directory specified by the `FANDANGO_PATH` environment variable, if set. This variable is a `:`-separated list of directories, e.g. `$HOME/my_cool_fan_specs:/Volumes/Fandango`
3. In the directory of the _including file_. (This is the most common usage.) If the including file has no file name (say, because it is a stream), the current directory is used.
4. In the directory `$HOME/.local/share/fandango`. You can control this location by setting the 
`XDG_DATA_HOME` environment variable; see the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/). On a Mac, the location `$HOME/Library/Fandango` is searched first.
5. In one of the system directories `/usr/local/share/fandango` or `/usr/share/fandango`. You can control these locations by setting the
`XDG_DATA_DIRS` environment variable; see the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/). On a Mac, the location `/Library/Fandango` is searched first.
6. If the file cannot be found in any of these locations, a `FileNotFoundError` is raised.

And then, there are two extra rules:
* If the included file has an _absolute_ path (say, `/usr/local/specs/spec.fan`), only this absolute path will be used.
* If the included file has a _relative_ path (say, `../spec.fan`), then this relative path will be applied to the locations above. This is mostly useful when you have a path relative to the including file.

Keep in mind that `include()` is a Python function; you can thus compute the file name in any way you'd like.
The simplest solution, however, is to use one of the "standard" locations as listed above.