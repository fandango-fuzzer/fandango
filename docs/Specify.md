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

(sec:specify)=
# Specifying Inputs

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