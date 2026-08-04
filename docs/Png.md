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

(sec:png)=
# Case Study: PNG

The [PNG format](https://en.wikipedia.org/wiki/PNG) is widely used to encode images.

The PNG spec [png.fan](png.fan) can be directly used in Fandango:

```shell
$ fandango fuzz -f png.fan -n 1 --population-size=1 -o 32x32.png
```

produces a nice [32x32 pixel PNG file](32x32.png):

```{image} 32x32.png
:alt: Generated PNG file
:class: bg-primary mb-1
:width: 200px
:align: center
```

The PNG file [png.fan](png.fan) is reproduced verbatim below.

```{versionadded} 1.1
`png.fan` requires Fandango 1.1 or later.
```

```{code-cell}
:tags: ["remove-input"]
!cat png.fan
```

```{note}
Note that `png.fan` supports only a limited set of PNG fields, so it cannot be used to [parse](sec:parsing) arbitrary PNG files.
```
