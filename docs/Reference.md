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

(sec:reference)=
# Fandango Reference

(sec:installing)=
## Installing Fandango

### Installing Fandango for Usage

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

## Installing Fandango for Development

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





Let us build a simple application.

```{code-cell}
:tags: ["remove-input"]
from myst_nb import glue
NAME_FAN = """
<start> ::= <name> ", " <age>;
<name> ::= "Alice" | "Bob";
<age> ::= <digit>+;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
"""
print(NAME_FAN)	
```






A Fandango specification comes in two parts:

* A _grammar_ describing the _syntax_ of the inputs to be generated
* Optionally, _constraints_ that specify additional properties.



----------------

```{include} Footer.md