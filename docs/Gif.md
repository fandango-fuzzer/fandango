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
# Case Study: GIF x ChatGPT

The [GIF format](https://www.fileformat.info/format/gif/egff.htm) is widely used to encode image sequences.

As with the [GIF format](sec:png), we asked ChatGPT for help.
Our prompt was the same as the [PNG prompt](prompt.txt), except that we replaced "PNG" with "GIF".

The resulting GIF file [gif.fan](gif.fan) is reproduced verbatim below.
It can be directly used in Fandango:

```shell
$ fandango fuzz -f gif.fan -n 1 --population-size=1 -o 32x32.gif 
```

produces a [32x32 pixel GIF file](32x32.gif):

```{image} 32x32.gif
:alt: Generated GIF file
:class: bg-primary mb-1
:width: 200px
:align: center
```

Here is the generated `gif.fan` specification file.
As far as we can tell, structure and documentation are accurate.

```{code-cell}
:tags: ["remove-input"]
!cat gif.fan 
```

```{note}
Note that `gif.fan` does not support only all GIF features, so it cannot be used to [parse](sec:parsing) arbitrary GIF files.
Feel free to use ChatGPT to add any extensions you'd like, or add them manually.
```

```{tip}
Be aware that every invocation of ChatGPT produces somewhat different code,
so you may need to provide further instructions to obtain your favorite `.fan` file.
```
