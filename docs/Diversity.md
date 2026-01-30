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

(sec:diversity)=
# Covering Specs and Code

During input generation, Fandango attempts to _cover_ as many behaviors as possible.
There are three ways to do so:

* **Grammar coverage** - that is, covering _alternatives in the grammar_;
* **Code coverage** - that is, covering _alternatives in the program under test_; and
* **Constraint coverage** - that is, covering _alternatives in constraints_.

Fandango is set to satisfy all these goals in unison.


## Grammar Coverage

During _input generation_, Fandango favors individual inputs that have a high _grammar coverage_ - that is, they cover as many alternatives as possible.
It does so after construction, as part of evaluating the fitness of individual inputs.

During [_protocol testing_](sec:protocols), Fandango already produces such interactions _by construction_ – that is, with every new iteration, it tries to cover parts of the grammar (= states, messages, and transitions) that have not been seen yet.

Grammar coverage is determined and achieved using the $k$-path metric by {cite:ts}`havrikov2019ase`.

```{versionadded} 1.2
For version 1.2, during input generation, Fandango will also achieve grammar coverage by construction.
```


## Code Coverage

As of version 1.2, Fandango will provide experimental support for guidance by code coverage.
Details will be added here.

```{versionadded} 1.2
This feature is planned for Fandango 1.2.
```



## Constraint Coverage

Future versions of Fandango will aim to achieve diversity by fulfilling different alternatives in constraints.
Once this is complete, details will be added here.

```{versionadded} 1.x
This feature is planned for a future Fandango version.
```
