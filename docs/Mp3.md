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

(sec:mp3)=
# Case Study: MP3

The [MP3 format](https://en.wikipedia.org/wiki/MP3) is widely used to encode audio.

The PNG spec [mp3.fan](mp3.fan) can be directly used in Fandango:

```shell
$ fandango fuzz -f mp3.fan -n 1 --population-size=1 -o silence.mp3
```

produces a second of silence in [silence.mp3](silence.mp3).

The file [mp3.fan](mp3.fan) is reproduced verbatim below.

```{versionadded} 1.1
`png.fan` requires Fandango 1.1 or later.
```

```{code-cell}
:tags: ["remove-input"]
!cat mp3.fan
```

```{note}
Note that in `mp3.fan`, almost all fields have fixed values, so it creates only silent MP3 fields.
Feel free to extend it to increase diversity.
```
