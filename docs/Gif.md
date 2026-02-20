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
# Case Study: A GIF Spec

The [GIF format](https://www.fileformat.info/format/gif/egff.htm) is widely used to encode image sequences.


## A GIF Spec from ChatGPT

As with the [PNG format](sec:png), we asked ChatGPT for help.
Our prompt was the same as the [PNG prompt](prompt.txt), except that we also asked to "make the resulting file as simple as possible".

The resulting GIF file [gif.fan](gif.fan) is reproduced verbatim below.
It can be directly used in Fandango:

```shell
$ fandango fuzz -f gif.fan -n 1 --population-size=1 -o 1x1.gif
```

produces a [1x1 pixel GIF file](1x1.gif) (which is probably invisible):

```{image} 1x1.gif
:alt: Generated GIF file
:class: bg-primary mb-1
:width: 100px
:align: center
```

Here is the generated `gif.fan` constructor.
Note that due to the structure of the file, it can only be used for producing, but not parsing or mutating.
For this, one would have to change it as follows:

* Many of the `<byte>*` fields could actually be turned into fixed-length values (e.g., `<byte>4`)
* Many of the generator functions `<elem> ::= <byte>* := f()` could be turned into constraints `where <elem> == f()`.
* Length encodings and checksums should be expressed as constraints, expressing lengths and checksums of the payloads
* There are many more fields and alternatives in GIF

```{code-cell}
:tags: ["remove-input"]
!cat gif.fan
```
