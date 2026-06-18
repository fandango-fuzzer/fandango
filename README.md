# Welcome to Fandango!

[![PyPI Release](https://img.shields.io/pypi/v/fandango-fuzzer)](https://pypi.org/project/fandango-fuzzer/) [![Last Release](https://img.shields.io/github/release-date/fandango-fuzzer/fandango)](https://github.com/fandango-fuzzer/fandango/releases)
[![Tests](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/python-tests.yml) [![Code Quality Checks](https://github.com/fandango-fuzzer/fandango/actions/workflows/code-checks.yml/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/code-checks.yml) [![CodeQL Analysis](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/fandango-fuzzer/fandango/actions/workflows/github-code-scanning/codeql) [![PyPI Downloads](https://img.shields.io/pypi/dm/fandango-fuzzer)](https://pypi.org/project/fandango-fuzzer/) [![PyPI Downloads](https://static.pepy.tech/badge/fandango-fuzzer)](https://pepy.tech/projects/fandango-fuzzer) [![GitHub stars](https://img.shields.io/github/stars/fandango-fuzzer/fandango)](https://github.com/fandango-fuzzer/fandango/stargazers)

> **Fandango** is a powerful generator of inputs and interactions designed for software testing. Given the specification of a program's input or interaction language, Fandango quickly generates a myriad of valid inputs to test your systems.

### ✨ Expressive & Flexible Specifications
Fandango's specification language combines a **grammar** with **constraints written in Python**, making it incredibly expressive. 
* **Custom Testing Goals:** Define exactly what you need. If you require your inputs to have particular values or follow specific distributions, you can express these testing goals directly in Fandango right out of the box.

### 🚀 Versatile Modes of Operation
Fandango adapts to your workflow by supporting multiple operating modes:
* **Black-Box Fuzzing (Default):** Generate inputs directly from a `.fan` Fandango specification file.
* **Input Mutation:** Feed Fandango your sample inputs, and it will mutate them to obtain more complex and realistic test cases.
* **Protocol Fuzzing:** Generate dynamic interactions. Fandango can act as a client or server, producing and reacting to interactions according to your protocol specifications.

### 🧠 Under the Hood
Fandango comes as a portable Python program, meaning it runs easily on a large variety of platforms. To produce its inputs, it leverages sophisticated **evolutionary algorithms**. It starts with a population of random inputs and systematically evolves them through mutations and cross-overs until they perfectly fulfill your given constraints.

### 🗺️ Road to 2026
Fandango is in active development! We are constantly expanding its capabilities. Features planned for 2026 include:
* Coverage-guided testing
* Code-directed testing
* High-diversity input generation
* ...and much more!

📚 **Ready to dive deeper?** For complete documentation, including tutorials, references, and advanced usage guides, visit the [Fandango Documentation](https://fandango-fuzzer.github.io/).

## License

Fandango is licensed under the European Union Public Licence V. 1.2. See the [LICENSE](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md) file for details.
