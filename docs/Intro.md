---
sd_hide_title: true
---

# Fuzzing with Fandango

::::{grid}
:reverse:
:gutter: 3 4 4 4
:margin: 1 2 1 2

:::{grid-item}
:columns: 12 4 4 4

```{image} Icon-reverse.png
:width: 200px
:class: sd-m-auto
```

:::

:::{grid-item}
:columns: 12 8 8 8
:child-align: justify
:class: sd-fs-5

```{rubric} Fuzzing with Fandango
```

Fandango produces myriads of _high-quality random inputs_ to test programs, giving users unprecedented control over format and shape of the inputs.

```{button-ref} GettingStarted
:ref-type: doc
:color: primary
:class: sd-rounded-pill

Get Started
```

:::

::::

----------------

::::{grid} 1 2 2 3
:gutter: 1 1 1 2

:::{grid-item-card} {material-regular}`edit_note;2em` Specify
:link: sec:getting-started
:link-type: ref

Specify the format of your input data in a single file, combining _grammars_ (for input syntax) and _constraints_ (for arbitrary input features).
Constraints come as Python code, so there are no limits to what you can specify.

+++
[Learn more »](sec:getting-started)
:::

:::{grid-item-card} {material-regular}`published_with_changes;2em` Test
:link: sec:test
:link-type: ref

Produce valid inputs at high speeds, from hundreds to thousands of inputs per second, quickly covering the entire input space.
Test with extreme and uncommon values, uncovering bugs before your users do.


+++
[Learn more »](Test)
:::

:::{grid-item-card} {material-regular}`settings;2em` Customize
:link: sec:customize
:link-type: ref

Shape inputs using your _own testing targets_, constraints, and statistical distributions.
Make use of _existing samples_ to obtain realistic inputs.
Use _feedback_ from the program under test to guide test generation to uncovered code.

+++
[Learn more »](sec:customize)
:::

::::

----------------

Fandango is a project of the [CISPA Helmholtz Center for Information Security](https://www.cispa.de/) to facilitate highly efficient and highly customizable software testing.

This research was funded by the European Union ([ERC S3](https://www.cispa.de/s3), 101093186). Views and opinions expressed are however those of the authors only and do not necessarily reflect those of the European Union or the European Research Council. Neither the European Union nor the granting authority can be held responsible for them.




<!--
Given a specification of the program's input language, Fandango quickly generates myriads of valid sample inputs for testing.


The specification language combines a _grammar_ with _constraints_ written in Python, so it is extremely expressive and flexible.
Most notably, you can define your own _testing goals_ in Fandango.
If you need the inputs to have particular values or distributions, you can express all these right away in Fandango.

Fandango supports multiple modes of operation:

* By default, Fandango operates as a _black-box_ fuzzer - that is, it creates inputs from a `.fan` Fandango specification file.
* If you have _sample inputs_, Fandango can _mutate_ these to obtain more realistic inputs.
* Fandango can also operate as a _white-box_ fuzzer - that is, it runs a program under test to maximize coverage. In this case, only a minimal specification may be needed.

Fandango comes as a portable Python program and can easily be run on a large variety of platforms.

Under the hood, Fandango uses sophisticated _evolutionary algorithms_ to produce inputs,
It starts with a population of random inputs, and evolving these through mutations and cross-over until they fulfill the given constraints.
-->
