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

(sec:about)=
# About Fandango

This the docs.

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


## Acknowledgments

```{include} Footer.md
