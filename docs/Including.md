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

(sec:file_locations)=
# Fandango File Locations

(sec:including)=
## Where Does Fandango Look for Included Specs?

In a Fandango spec, [the `include()` function](sec:hatching) searches for Fandango files in a number of locations.
The actual rules for where Fandango searches are complex, versatile, and adhere to common standards.
Specifically, when including a `.fan` file using `include()`, Fandango searches for `.fan` files in the following locations, in this order:

1. In any directory `DIR` explicitly specified by `-I DIR` or `--include-dir DIR`.
2. In any directory specified by the `$FANDANGO_PATH` environment variable, if set. This variable is a colon-separated list of directories, e.g. `$HOME/my_cool_fan_specs:/Volumes/Fandango:/opt/local/fandango-1.27` which are searched from left to right.
3. In the directory of the _including file_. This is the most common usage. If the including file has no file name (say, because it is a stream), the current directory is used.
4. In the directory `$HOME/.local/share/fandango`. You can control this location by setting the 
`$XDG_DATA_HOME` environment variable; see the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/). On a Mac, the location `$HOME/Library/Fandango` is searched first.
5. In one of the system directories `/usr/local/share/fandango` or `/usr/share/fandango`. You can control these locations by setting the
`$XDG_DATA_DIRS` environment variable; see the [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/latest/). On a Mac, the location `/Library/Fandango` is searched first.
6. If the file to be included cannot be found in any of these locations, a `FileNotFoundError` is raised.

And then, there are two extra rules:

* If the included file has an _absolute_ path (say, `/usr/local/specs/spec.fan`), only this absolute path will be used.
* If the included file has a _relative_ path (say, `../spec.fan`), then this relative path will be applied to the locations above. This is mostly useful when you have a path relative to the including file.

```{tip}
We recommend to store included Fandango specs either
* in the directory where the _including_ specs are, or
* in `$HOME/.local/share/fandango` (or `$HOME/Library/Fandango` on a Mac).
```


Finally, keep in mind that `include()` is a Python function, so in principle, your spec can compute the file name and location in any way you like.
The simplest solution, however, is to use one of the "standard" locations as listed above.


(sec:caching)=
## Where Does Fandango Store Parsed Files?

Fandango maintains a _cache_ for parsed `.fan` files in order to retrieve them faster.

Use `fandango clear-cache -n` to retrieve its location:

```shell
$ fandango clear-cache -n
```

```{code-cell}
:tags: ["remove-input"]
!fandango clear-cache -n
assert _exit_code == 0
```

If you want to reclaim space, or if there is some incompatibility between parsed and cached files, use `fandango clear-cache` to clear the cache:

```shell
$ fandango clear-cache
```

```{code-cell}
:tags: ["remove-input"]
!fandango clear-cache -n 2>&1 | sed 's/Would clear/Clearing/'
assert _exit_code == 0
```


(sec:fandango_location)=
## Where is Fandango installed?

This depends on your Python installation.
You can query the location using

```shell
$ pip show fandango-fuzzer | grep Location
```

```{code-cell}
:tags: ["remove-input"]
!pip show fandango-fuzzer | grep Location
assert _exit_code == 0
```
