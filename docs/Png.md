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
# Case Study: A PNG spec from ChatGPT

The [PNG format](https://en.wikipedia.org/wiki/PNG) is widely used to encode images.
To obtain a Fandango specification that creates PNG images, we asked ChatGPT for help.

The file [png.fan](png.fan) was created by asking [ChatGPT](https://chatgpt.com) for assistance.
The [prompt](prompt.txt) instructed ChatGPT 

* to produce a Fandango PNG spec;
* to avoid specific mistakes about Fandango; and
* to prefer more efficient alternatives wherever possible:

```{code-cell}
:tags: ["remove-input"]
!cat prompt.txt
```

The resulting PNG file [png.fan](png.fan) is reproduced verbatim below.
It can be directly used in Fandango:

```shell
$ fandango fuzz -f png.fan -n 1 --population-size=1 -o 32x32.png
```

produces a nice [32x32 pixel PNG file](32x32.png):

```{image} 32x32.png
:alt: Generated PNG file
:class: bg-primary mb-1
:width: 100px
:align: center
```

If you need a `.fan` file for a specific format, feel free to start with the above prompt.

```{code-cell}
:tags: ["remove-input"]
!cat png.fan
```
