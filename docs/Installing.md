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

(sec:installing)=
# Installing Fandango

## Installing the public version of Fandango

```{warning}
While Fandango is in beta, only development versions can be installed.
```

Fandango comes as a Python package. To install Fandango, run the following command:

```
$ pip install fandango
```

To test if everything worked well, try

```
$ fandango --help
```

which should give you a list of options:

```{code-cell}
:tags: ["remove-input"]
!fandango --help
```

## Installing development versions of Fandango

```{caution}
This will get you the very latest version of Fandango, which may be unstable. Use at your own risk.
```

```{note}
At this point, only registered developers have access to Fandango.
```

Clone the Fandango repository:

```
$ git clone https://github.com/fandango-fuzzer/fandango/
```

In the top-level `fandango/` folder, run
```
$ pip install -e .
```

You should then be able to invoke Fandango as described above.



