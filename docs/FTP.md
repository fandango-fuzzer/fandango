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

(sec:ftp)=
# Case Study: FTP

This FTP specification allows testing FTP clients and servers.
It demonstrates how additional channels (`ClientData` and `ServerData`) are created on demand, based on the ports returned by the FTP server.

```{admonition} Under Construction
:class: attention
Extended documentation for this case study is under construction.
```

```{code-cell}
:tags: ["remove-input"]
!cat ../evaluation/experiments/ftp/ftp.fan
assert _exit_code == 0
```