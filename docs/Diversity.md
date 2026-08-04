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

```{versionadded} 1.x
In a future version, during input generation, Fandango will also achieve grammar coverage by construction.
```


(sec:code-coverage)=
## Code Coverage

As of version 1.2, Fandango provides _experimental_ support for guidance by code coverage.
It works against a program under test that has been compiled with [`fcc`](https://github.com/fandango-fuzzer/fcc), the Fandango coverage compiler.
`fcc` records the control flow graph of the program at compile time; at run time, Fandango tracks which basic blocks each input reaches, and favors inputs that get closer to code it has not seen yet.

```shell
$ fandango --enable-experimental-module execution fuzz -f spec.fan --fcc ./program
```

```{warning}
This is an experimental feature, living in `fandango.experimental.execution`.
It may change without notice, so do not rely on it in production.
Fandango warns you about this the first time the module is loaded; `--enable-experimental-module execution` is how you acknowledge the warning and silence it.
```

```{versionadded} 1.2
Experimental code coverage guidance is available in Fandango 1.2 and later.
```



## Constraint Coverage

Future versions of Fandango will aim to achieve diversity by fulfilling different alternatives in constraints.
Once this is complete, details will be added here.

```{versionadded} 1.x
This feature is planned for a future Fandango version.
```
