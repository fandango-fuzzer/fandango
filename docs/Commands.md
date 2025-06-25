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

(sec:commands)=
# Fandango Command Reference

## All Commands

Here is a list of all `fandango` commands:

```{code-cell}
:tags: ["remove-input"]
!fandango --help
```


## Fuzzing

To [produce outputs with `fandango`](sec:fuzzing), use `fandango fuzz`:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz --help
```

## Parsing

To [parse inputs with `fandango`](sec:parsing), use `fandango parse`:

```{code-cell}
:tags: ["remove-input"]
!fandango parse --help
```


## Converting

To [convert existing language specs with `fandango`](sec:converters), use `fandango convert`:

```{code-cell}
:tags: ["remove-input"]
!fandango convert --help
```


## Interacting

To [have Fandango interact with programs](sec:outputs) and [other parties](sec:protocols), use `fandango talk`:

```{code-cell}
:tags: ["remove-input"]
!fandango talk --help
```


## Shell

To [enter commands in `fandango`](sec:shell), use `fandango shell` or just `fandango`:

```{code-cell}
:tags: ["remove-input"]
!fandango shell --help
```


## Clearing

To [have Fandango clear its parser cache](sec:caching), use `fandango clear-cache`:

```{code-cell}
:tags: ["remove-input"]
!fandango clear-cache --help
```
