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

Given the specification of a program's input language, Fandango quickly generates myriads of valid sample inputs for testing.

The specification language combines a _grammar_ with _constraints_ written in Python, so it is extremely expressive and flexible.
Most notably, you can define your own _testing goals_ in Fandango.
If you need the inputs to have particular values or distributions, you can express all these right away in Fandango.

Fandango supports multiple modes of operation:

* By default, Fandango operates as a _black-box_ fuzzer - that is, it creates inputs from a `.fan` Fandango specification file.
* If you have _sample inputs_, Fandango can _mutate_ these to obtain more realistic inputs.
% * Fandango can also operate as a _white-box_ fuzzer - that is, it runs a program under test to maximize coverage. In this case, only a minimal specification may be needed.

Fandango comes as a portable Python program and can easily be run on a large variety of platforms.

Under the hood, Fandango uses sophisticated _evolutionary algorithms_ to produce inputs,
it starts with a population of random inputs, and evolves these through mutations and cross-over until they fulfill the given constraints.

Fandango is in active development! Features planned for 2025 include:

* protocol testing
* coverage-guided testing
* code-directed testing
* high diversity inputs

and many more.



## Refer to Us

To refer to Fandango, use its official URL:

  https://fandango-fuzzer.github.io


## Cite Us

If you want to cite Fandango in your academic work, use our ISSTA 2025 paper {cite:ps}`zamudio2025fandango`:

```
@inproceedings{zamudio2025fandango,
  author = {José Antonio Zamudio Amaya and Marius Smytzek and Andreas Zeller},
  booktitle = {Proc. International Symposium on Software Testing and Analysis (ISSTA)},
  title = {{FANDANGO}: {E}volving Language-Based Testing},
  year = {2025},
  url = {https://publications.cispa.de/articles/standard/FANDANGO_Evolving_Language-Based_Testing/28769252?file=53591066}
}
```


## Read More

To learn more about how Fandango works, start with our ISSTA 2025 paper {cite:ps}`zamudio2025fandango`.

```{bibliography}
```


## Acknowledgments

```{include} Footer.md
