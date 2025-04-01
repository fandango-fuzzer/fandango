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

(sec:installing_tut)=
# Installing Fandango

To install Fandango, you first need to install [Python](https://www.python.org/).
Then, run the following command:

```
$ pip install fandango-fuzzer
```

```{note}
In this tutorial, a `$` at the beginning of a command stands for your input prompt.
Do not enter it yourself.
```

You can check if everything works well by running

```
$ fandango --help
```

Entering `fandango --help` should result in an output like this:

```{code-cell}
:tags: ["remove-input"]
!fandango --help
assert _exit_code == 0
```

If this did not work, try out an alternate option; see [](sec:installing).