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



## Refer to Fandango

To refer to Fandango, use its official URL:

  https://fandango-fuzzer.github.io


## Cite Fandango

```{code-cell}
:tags: ["remove-input"]
import re

def find_reference(key, bibfile='fandango.bib'):
    bib = open(bibfile, 'r').read()
    match = re.match(r'@[a-zA-Z0-9]*\{' + key + r',(.|\n)*\n\}', bib)
    assert match is not None
    return match.group(0)

def print_reference(key, bibfile='fandango.bib'):
    print(find_reference(key, bibfile))
```

If you want to cite Fandango in your academic work, use the ISSTA 2025 paper by {cite:ts}`zamudio2025fandango`.
Note that José Antonio has two proper last names, Zamudio Amaya, so the proper way to cite the paper is like this:

```{code-cell}
:tags: ["remove-input"]
print_reference('zamudio2025fandango')
```


## Read More

To learn more about how Fandango works, start with the ISSTA 2025 paper by {cite:ts}`zamudio2025fandango`.

The core idea of Fandango, namely combining grammars and constraints, was introduced as _language-based software testing_ by {cite:ts}`steinhoefel2024language` and first implemented in the _ISLa_ framework {cite}`steinhoefel2022isla`. Both of these laid the foundation for Fandango.

The work on Fandango is funded by the ERC S3 project ["Semantics of Software Systems"](https://cispa.de/s3); the S3 grant proposal (available via the above link) lists several ideas that have been realized in Fandango (and a few more).

The work on Fandango is also related to _mining grammars_ from programs and inputs. Important works in the field include
{cite:ts}`bettscheider2024mining`,
{cite:ts}`gopinath2020mining`,
{cite:ts}`schroeder2022mining`, and
{cite:ts}`kulkarni2022arvada`.

```{bibliography}
```


## Acknowledgments

```{include} Footer.md
