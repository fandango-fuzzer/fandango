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
# Case Study: PNG x ChatGPT

The [PNG format](https://en.wikipedia.org/wiki/PNG) is widely used to encode images.
To obtain a Fandango specification that creates PNG images, we asked ChatGPT for help.

We created the file [png.fan](png.fan) by asking [ChatGPT](https://chatgpt.com) for assistance.
The [prompt](prompt.txt) instructs ChatGPT 

* to produce a Fandango PNG spec;
* to avoid specific mistakes about Fandango; and
* to prefer more efficient alternatives wherever possible.

```{margin}
The prompt is fairly generic. 
Instead of `PNG`, you may use other image formats (or even other arbitrary file formats) as you like.
```

```{tip}
Use the copy button in the upper right corner to copy the prompt, so you can paste it into your favorite editor, and then paste it into ChatGPT.
```

```{code-cell}
:tags: ["remove-input"]
!cat prompt.txt
```

The resulting PNG file [png.fan](png.fan) can be directly used in Fandango:

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

The resulting PNG file [png.fan](png.fan) is reproduced verbatim below.
As far as we can tell, structure and documentation are accurate.

```{code-cell}
:tags: ["remove-input"]
!cat png.fan
```

```{note}
Note that `png.fan` supports only a limited set of PNG fields, so it cannot be used to [parse](sec:parsing) arbitrary PNG files.
Feel free to use ChatGPT to add any extensions you'd like, or add them manually;
```

```{tip}
Be aware that every invocation of ChatGPT produces somewhat different code,
so you may need to provide further instructions to obtain your favorite `.fan` file.
```
