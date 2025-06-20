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

(sec:gif)=
# Case Study: The GIF Format

```{admonition} Under Construction
:class: attention
To be added later.
```

The [GIF format](https://www.fileformat.info/format/gif/egff.htm) is widely used to encode image sequences.

We start with a very short GIF to keep things simple ([source](http://probablyprogramming.com/2009/03/15/the-tiniest-gif-ever)): [tinytrans.gif](tinytrans.gif).

We can parse this file using Fandango:

```{code-cell}
!fandango parse -f gif89a.fan tinytrans.gif -o - --format=grammar --validate
assert _exit_code == 0
```