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

```{note}
In this tutorial, a `$` at the beginning of a command stands for your input prompt.
Do not enter it yourself.
```

```{tip}
Hovering the mouse pointer over the command offers an option to copy the command to the clipboard.
```


### Code

File contents (mostly Fandango `.fan` files) are shown like this:

```python
<start> ::= <fandango>
```

We often only show excerpts; the complete examples can be downloaded, as in [digits.fan](digits.fan).

_Executable code_ examples (mostly in Python) are shown like this:

```{code-cell}
from fandango import Fandango
```

Enter these at a Python prompt, or include them in your Python programs.

```{tip}
Hovering the mouse pointer over the code offers an option to copy the code to the clipboard.
```



### Callouts

This documentation uses the following conventions for _callouts_:

:::{margin}
There are also _margin notes_, which show interesting background information.
:::

```{tip}
Show helpful information or another way to do something.
```

```{note}
Bring additional information to the readers' attention.
```

```{important}
Bring important information to the readers' attention.
```

```{admonition} Under Construction
:class: attention
Indicate that some parts of the documentation or the implementation are under construction.
```

```{caution}
Tell the reader to proceed carefully.
```

```{warning}
Warn about possible irreversible damage, such as permanent data loss.
```

:::{margin}
Pretty much all of these occur in the chapter on [Fuzzing Strategies](sec:strategies).
:::

```{danger}
Warn about hazards that may lead to death or serious injury.
```

### Quizzes

This documentation also uses _quizzes_ – that is, questions for the reader.
The solutions are initially hidden, but can be unhidden by clicking on them.

For instance, what does a _Warning_ callout indicate?

```{admonition} Solution
:class: tip, dropdown
It indicates a step that might cause irreversible damage, such as permanent data loss.
```

### Changes

These hints highlight changes across versions:

```{versionadded} 1.0
Explanation of the new feature.
```

```{versionchanged} 1.0
Explanation of the change.
```

```{deprecated} 1.0
Explanation of the deprecation.
```



% ## Table of Contents
%
% ```{tableofcontents}
% ```


% ## Acknowledgments
%
% ```{include} Footer.md
