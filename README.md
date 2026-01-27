# Generating Test Inputs and Interactions with Fandango

[![PyPI Release](https://img.shields.io/pypi/v/fandango-fuzzer)](https://pypi.org/project/fandango-fuzzer/) [![Last Release](https://img.shields.io/github/release-date/fandango-fuzzer/fandango)](https://github.com/fandango-fuzzer/fandango/releases)
[![Tests](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml) [![Code Quality Checks](https://github.com/fandango-fuzzer/fandango/actions/workflows/code-checks.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/code-checks.yml) [![CodeQL Analysis](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql) [![Docs Deployment](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-book.yml) [![Build & Publish](https://github.com/fandango-fuzzer/fandango/actions/workflows/build-and-publish.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/build-and-publish.yml) [![Coverage Status](https://coveralls.io/repos/github/fandango-fuzzer/fandango/badge.svg?branch=main)](https://coveralls.io/github/fandango-fuzzer/fandango?branch=main) [![PyPI Downloads](https://img.shields.io/pypi/dm/fandango-fuzzer)](https://pypi.org/project/fandango-fuzzer/) [![PyPI Downloads](https://static.pepy.tech/badge/fandango-fuzzer)](https://pepy.tech/projects/fandango-fuzzer) [![GitHub stars](https://img.shields.io/github/stars/fandango-fuzzer/fandango?style=social)](https://github.com/fandango-fuzzer/fandango/stargazers)

Welcome to Fandango!
Fandango is a _generator_ of inputs and interactions for software testing.
Given the specification of a program's input or interaction language, Fandango quickly generates myriads of valid sample inputs for testing.

The specification language combines a _grammar_ with _constraints_ written in Python, so it is extremely expressive and flexible.
Most notably, you can define your own _testing goals_ in Fandango.
If you need the inputs to have particular values or distributions, you can express all these right away in Fandango.

Fandango supports multiple modes of operation:

* By default, Fandango operates as a _black-box_ fuzzer - that is, it creates inputs from a `.fan` Fandango specification file.
* If you have _sample inputs_, Fandango can _mutate_ these to obtain more realistic inputs.
* Fandango can also produce _interactions_ for _protocol fuzzing_ - that is, it acts as a client or server producing and reacting to interactions according to specification.

Fandango comes as a portable Python program and can easily be run on a large variety of platforms.

Under the hood, Fandango uses sophisticated _evolutionary algorithms_ to produce inputs,
it starts with a population of random inputs, and evolves these through mutations and cross-over until they fulfill the given constraints.

Fandango is in active development! Features planned for 2026 include:

* coverage-guided testing
* code-directed testing
* high diversity inputs

and many more.

For the complete Fandango documentation, including tutorials, references, and advanced usage guides, visit the [Fandango documentation](https://fandango-fuzzer.github.io/)

---

## License

Fandango is licensed under the European Union Public Licence V. 1.2. See the [LICENSE](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md) file for details.
