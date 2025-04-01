# FANDANGO: Evolving Language-Based Testing

FANDANGO is a language-based fuzzer that leverages formal input specifications (grammars) combined with constraints to generate diverse sets of valid inputs for programs under test. Unlike traditional symbolic constraint solvers, FANDANGO uses a search-based approach to systematically evolve a population of inputs through syntactically valid mutations until semantic input constraints are satisfied.

## Replication package

- [Installation](#installation)
- [Running the evaluation](#evaluation)
- [License](#license)

## Installation

FANDANGO requires [Python 3.11](https://www.python.org/downloads/release/python-3118/). After installing Python, it is recommended to use FANDANGO from a _python virtual environment_, so there is no version issues between libraries. After creating a new environment, change your directory to the root of the repository, and install the requirements:

```bash
make install
```

In order to see if your installation is correct, run the FANDANGO tests with:
```bash
make test
```

---

If all tests pass, you are ready to use FANDANGO!

## Running the evaluation

FANDANGO has been accepted to ISSTA 2025. As stated in the paper, FANDANGO has been evaluated against [ISLa](https://github.com/rindPHI/isla/tree/ESEC_FSE_22), a state-of-the-art language-based fuzzer. The results show that FANDANGO is faster and more scalable than ISLa, while maintaining the same level of precision.

To reproduce the evaluation results from ISLa, please refer to [their replication package](https://dl.acm.org/do/10.1145/3554336/full/), published in FSE 2022.
To reproduce the evaluation results from FANDANGO, execute: (from the root directory)

```bash
make evaluation
```

This script will execute FANDANGO on 5 subjects (CSV, reST, ScriptSizeC, TAR and XML). Each subject will be run for an hour, followed up by a computation on each grammar coverage (This process can take a while). The results will be printed in the terminal. Our evaluation showcases FANDANGO's search-based approach as a viable alternative to symbolic solvers, offering the following advantages:

- **Speed**: Faster by one to three orders of magnitude compared to symbolic solvers.
- **Precision**: Maintains precision in satisfying constraints.
- **Scalability**: Efficiently handles large grammars and complex constraints.

---

## License

This project is licensed under the European Union Public Licence V. 1.2. See the [LICENSE](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md) file for details.