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

(sec:tutorial)=
# Fandango Tutorial

Welcome to Fandango! In this tutorial, you will learn how to

* write *Fandango specs*
* use the `fandango` *command-line tool*
* *test programs* with Fandango.


(sec:conventions)=
## Conventions in this Documentation

### Shell Commands

Fandango is mostly operated via the _command line_.
A command `fandango help` is shown as follows:

```shell
$ fandango help
```

This assumes an input prompt `$ ` already present at the command line.
Do not enter it.

```{tip}
Hovering the mouse pointer over the command offers an option to copy the command to the clipboard.
```


### Code

File contents (mostly Fandango `.fan`) files are shown like this:

```python
<start> ::= <fandango>
```

You can typically _download_ the complete examples, as in [digits.fan](digits.fan).

_Executable code_ examples (mostly in Python) are shown like this:

```{code-cell}
from fandango import Fandango
```


### Callouts

This documentation uses the following conventions for _callouts_:

:::{margin}
There are also _margin notes_, which show interesting, but not vital information.
:::

```{tip}
Show helpful information or another way to do something.
```

```{note}
Bring additional information to the readers' attention.
```

```{caution}
Tell the reader to proceed carefully.
```

```{warning}
A step that might cause irreversible damage, such as permanent data loss.
```

:::{margin}
So far, there are no "Danger" callouts in this documentation.
:::

```{danger}
A hazard that may lead to death or serious injury.
```

```{error}
An indication that some parts of the documentation are under construction.
```

### Quizzes

This documentation also uses _quizzes_ – that is, questions for the reader.
The solutions are initially hidden, but can be unhidden by clicking on them.

```{admonition} Solution
:class: tip, dropdown
You found the solution!
```


% ## Table of Contents
%
% ```{tableofcontents}
% ```


% ## Acknowledgments
%
% ```{include} Footer.md
