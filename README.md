# FANDANGO: Evolving Language-Based Testing

[![Python Tests](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml)
[![GitHub Pages](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-book.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-book.yml)
[![CodeQL](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql)
[![PyPI](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-pypi.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-pypi.yml)
[![Docker Image](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-docker.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/deploy-docker.yml)
[![Socket Badge](https://socket.dev/api/badge/pypi/package/fandango-fuzzer/0.1.0?artifact_id=tar-gz)](https://socket.dev/pypi/package/fandango-fuzzer/overview/0.1.0/tar-gz)

FANDANGO is a language-based fuzzer that leverages formal input specifications (grammars) combined with constraints to generate diverse sets of valid inputs for programs under test. Unlike traditional symbolic constraint solvers, FANDANGO uses a search-based approach to systematically evolve a population of inputs through syntactically valid mutations until semantic input constraints are satisfied.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Documentation](#documentation)
- [Evaluation](#evaluation)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Modern language-based test generators often rely on symbolic constraint solvers to satisfy both syntactic and semantic input constraints. While precise, this approach can be slow and restricts the expressiveness of constraints due to the limitations of solver languages.

FANDANGO introduces a search-based alternative, using genetic algorithms to evolve inputs until they meet the specified constraints. This approach not only enhances efficiency—being one to three orders of magnitude faster in our experiments compared to leading tools like [ISLa](https://github.com/rindPHI/isla/tree/ESEC_FSE_22)—but also allows for the use of the full Python language and libraries in defining constraints.

With FANDANGO, testers gain unprecedented flexibility in shaping test inputs and can state arbitrary goals for test generation. For example:

> "Please produce 1,000 valid test inputs where the ⟨voltage⟩ field follows a Gaussian distribution but never exceeds 20 mV."

## Features

- **Grammar-Based Input Generation**: Define formal grammars to specify the syntactic structure of inputs.
- **Constraint Satisfaction**: Use arbitrary Python code to define semantic constraints over grammar elements.
- **Genetic Algorithms**: Employ a search-based approach to evolve inputs, improving efficiency over symbolic solvers.
- **Flexible Constraint Language**: Leverage the full power of Python and its libraries in constraints.
- **Performance**: Achieve faster input generation without sacrificing precision.

---

## Documentation

For the complete FANDANGO documentation, including tutorials, references, and advanced usage guides, visit the [FANDANGO docs](https://fandango-fuzzer.github.io/Intro.html).

Here, you'll find the following sections:

#### Fuzzing with Fandango
   - [Fuzzing with Fandango](https://fandango-fuzzer.github.io/Intro.html)
#### About Fandango
   - [About Fandango](https://fandango-fuzzer.github.io/About.html)
#### Fandango Tutorial
  - [Fandango Tutorial](https://fandango-fuzzer.github.io/Tutorial.html)
  - [Installing Fandango](https://fandango-fuzzer.github.io/Installing.html)
  - [A First Fandango Spec](https://fandango-fuzzer.github.io/FirstSpec.html)
  - [Invoking Fandango](https://fandango-fuzzer.github.io/Invoking.html)
  - [Fuzzing with Fandango](https://fandango-fuzzer.github.io/Fuzzing.html)
  - [Some Fuzzing Strategies](https://fandango-fuzzer.github.io/Strategies.html)
  - [Shaping Inputs with Constraints](https://fandango-fuzzer.github.io/Constraints.html)
  - [The Fandango Shell](https://fandango-fuzzer.github.io/Shell.html)
  - [Data Generators and Fakers](https://fandango-fuzzer.github.io/Generators.html)
  - [Complex Input Structures](https://fandango-fuzzer.github.io/Recursive.html)
  - [Accessing Input Elements](https://fandango-fuzzer.github.io/Paths.html)
  - [Case Study: ISO 8601 Date + Time](https://fandango-fuzzer.github.io/ISO8601.html)
  - [Generating Binary Inputs](https://fandango-fuzzer.github.io/Binary.html)
  - [Bits and Bit Fields](https://fandango-fuzzer.github.io/Bits.html)
  - [Case Study: The GIF Format](https://fandango-fuzzer.github.io/Gif.html)
  - [Statistical Distributions](https://fandango-fuzzer.github.io/Distributions.html)
  - [Coverage-Guided Fuzzing](https://fandango-fuzzer.github.io/Whitebox.html)
  - [Hatching Specs](https://fandango-fuzzer.github.io/Hatching.html)
#### Fandango Reference
  - [Fandango Reference](https://fandango-fuzzer.github.io/Reference.html)
  - [Installing Fandango](https://fandango-fuzzer.github.io/Installing.html)
  - [Fandango Standard Library](https://fandango-fuzzer.github.io/Stdlib.html)
  - [Fandango Spec Locations](https://fandango-fuzzer.github.io/Including.html)

---

## Evaluation

FANDANGO has been submitted to ISSTA 2025. FANDANGO has been evaluated against [ISLa](https://github.com/rindPHI/isla/tree/ESEC_FSE_22), a state-of-the-art language-based fuzzer. The results show that FANDANGO is faster and more scalable than ISLa, while maintaining the same level of precision.

To reproduce the evaluation results from ISLa, please refer to [their replication package](https://dl.acm.org/do/10.1145/3554336/full/), published in FSE 2022.
To reproduce the evaluation results from FANDANGO, please download a development copy of the repository from [the official GitHub Repository](https://github.com/fandango-fuzzer/fandango), execute: (from the root directory)

```bash
python -m evaluation.vs_isla.run_evaluation
```

This script will execute FANDANGO on 5 subjects (CSV, reST, ScriptSizeC, TAR and XML). Each subject will be run for an hour, followed up by a computation on each grammar coverage (This process can take a while). The results will be printed in the terminal. Our evaluation showcases FANDANGO's search-based approach as a viable alternative to symbolic solvers, offering the following advantages:

- **Speed**: Faster by one to three orders of magnitude compared to symbolic solvers.
- **Precision**: Maintains precision in satisfying constraints.
- **Scalability**: Efficiently handles large grammars and complex constraints.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -am 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

Please ensure all tests pass and adhere to the coding style guidelines.

---

## License

This project is licensed under the European Union Public Licence V. 1.2. See the [LICENSE](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md) file for details.