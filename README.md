# FANDANGO: Evolving Language-Based Testing

FANDANGO is a language-based fuzzer that leverages formal input specifications (grammars) combined with constraints to generate diverse sets of valid inputs for programs under test. Unlike traditional symbolic constraint solvers, FANDANGO uses a search-based approach to systematically evolve a population of inputs through syntactically valid mutations until semantic input constraints are satisfied.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Defining Grammars](#defining-grammars)
  - [Defining Constraints](#defining-constraints)
  - [Running FANDANGO](#running-fandango)
- [Examples](#examples)
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

## Installation

FANDANGO requires [Python 3.11](https://www.python.org/downloads/release/python-3118/). After installing Python, it is recommended to use FANDANGO from a _python virtual environment_, so there is no version issues between libraries. After creating a new environment, change your directory to the root of the repository, and install the requirements:

```bash
pip install -r requirements.txt &&
pip install -e .
```

In order to see if your installation is correct, run the FANDANGO tests with:
```bash
pytest
```

---

If all tests pass, you are ready to use FANDANGO!

## Quick Start

Here's a minimal example to get started with FANDANGO:

1. **Define a Grammar**: Create a file `grammar.fan` containing your grammar rules.

   ```ebnf
   <start> ::= <number> ;
   <number> ::= <digit><number> | <digit> ;
   <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
   ```

2. **Define Constraints**: Specify constraints using Python code.

   ```python
   <start> ::= <number> ;
   <number> ::= <digit><number> | <digit> ;
   <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
   
   int(<number>) % 2 == 0;
   ```

3. **Run FANDANGO**:

   ```python
   from fandango.evolution.algorithm import Fandango
   from fandango.language.parse import parse_file

   # Parse grammar and constraints
   grammar, constraints = parse_file('grammar.fan')

   # Initialize FANDANGO
   fandango = Fandango(grammar, constraints, verbose=True)

   # Evolve solutions
   solutions = fandango.evolve()

   # Print solutions
   for solution in solutions:
       print(str(solution))
   ```

---

## Usage

### Defining Grammars

FANDANGO uses grammars defined in Extended Backus-Naur Form (EBNF). Here's an example of a grammar file `pixels.fan`:

```ebnf
<start> ::= <img> ;
<img> ::= <width> <height> <pixels> ;
<width> ::= <uint16> ;
<height> ::= <uint16> ;
<pixels> ::= <rgb>* ;
<uint16> ::= <byte> <byte> ;
<rgb> ::= <byte> <byte> <byte> ;
<byte> ::= <bit> <bit> <bit> <bit> <bit> <bit> <bit> <bit> ;
<bit> ::= "0" | "1" ;
```

### Defining Constraints

Constraints are Python expressions that evaluate over non-terminal rules. They reference grammar elements enclosed in angle brackets.

Example constraints:

```python
int(<pixels>) == int(<width>) * int(<height>) * 3;
```

Constraints can use any Python code and libraries, allowing for complex conditions.

### Running FANDANGO

Use the `FANDANGO` class to run the genetic algorithm:

```python
from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

# Parse grammar and constraints
grammar, constraints = parse_file('pixels.fan')

# Initialize FANDANGO with desired parameters
fandango = Fandango(
    grammar=grammar,
    constraints=constraints,
    population_size=100,
    max_generations=500,
    verbose=True
)

# Evolve solutions
solutions = fandango.evolve()

# Output solutions
for solution in solutions:
    print(str(solution))
```

---

## Examples

### Example 1: Hash Constraint

Suppose you want to generate inputs where a string and its SHA-256 hash are included:

**Grammar**:

```ebnf
<start> ::= <data_record> ;
<data_record> ::= <string> ' = ' <hash> ;
<string> ::= <char>* ;
<char> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
<hash> ::= <hex_digit>* ;
<hex_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" ;
```

**Constraint**:

```python
import hashlib
str(<hash>) == hashlib.sha256(str(<string>).encode('utf-8')).hexdigest();
```

**Running FANDANGO**:

```python
from fandango.evolution.algorithm import Fandango
from fandango.language.parse import parse_file

grammar, constraints = parse_file('hash_example.fan')

fandango = Fandango(grammar, constraints, verbose=True)
solutions = fandango.evolve()

for solution in solutions:
    print(str(solution))
```

### Example 2: CSV File Generation

Generate CSV files with specific constraints:

**Grammar**:

```ebnf
<start> ::= <csv_file> ;
<csv_file> ::= <csv_header> <csv_records> ;
<csv_header> ::= <csv_record> ;
<csv_records> ::= <csv_record> <csv_records> | "" ;
<csv_record> ::= <csv_string_list> "\n" ;
<csv_string_list> ::= <raw_field> | <raw_field> ";" <csv_string_list> ;
<raw_field> ::= <simple_field> | <quoted_field> ;
<simple_field> ::= <spaces> <simple_characters> <spaces> ;
<simple_characters> ::= <simple_character> <simple_characters> | <simple_character> ;
<simple_character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" ;
<quoted_field> ::= '"' <escaped_field> '"' ;
<escaped_field> ::= <escaped_characters> ;
<escaped_characters> ::= <escaped_character> <escaped_characters> | "" ;
<escaped_character> ::= "!" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "-" | "." | "/" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "[" | "\\" | "]" | "^" | "_" | "`" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "{" | "|" | "}" | "~" | " " | "\t" | "\r" |"\n" ;
<spaces> ::= "" | " " <spaces> ;
```

**Constraint**:

```python
forall <records> in <csv_records>:
    len(str(<records>.<csv_record>)) > 100
;
```

#### Need more examples? Check the [evaluation directory](https://github.com/fandango-fuzzer/fandango/tree/main/src/evaluation/evaluation) for more use cases! You will find grammars and constraints for well-known file formats such as XML, CSV, C. In addition, you will find more examples in the [experiments directory](https://github.com/fandango-fuzzer/fandango/tree/main/src/evaluation/experiments), where we have tried to produce statistical distributions, hashes and dynamic library invocation!

---

## Evaluation

FANDANGO has been submitted to ISSTA 2025, and it is currently under review. As stated in the submitted paper, FANDANGO has been evaluated against [ISLa](https://github.com/rindPHI/isla/tree/ESEC_FSE_22), a state-of-the-art language-based fuzzer. The results show that FANDANGO is faster and more scalable than ISLa, while maintaining the same level of precision.

To reproduce the evaluation results from ISLa, please refer to [their replication package](https://dl.acm.org/do/10.1145/3554336/full/), published in FSE 2022.
To reproduce the evaluation results from FANDANGO, execute: (from the root directory)

```bash
cd src/evaluation/evaluation &&
python run_evaluation.py
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

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md) file for details.