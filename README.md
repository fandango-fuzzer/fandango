# FANDANGO: Evolving Language-Based Testing

## Introduction

FANDANGO is a **Fuzzing framework** that leverages **grammar-based genetic algorithms** to generate inputs that satisfy complex constraints. It allows users to define grammars and constraints in a unified `.fan` file format and evolves inputs to meet the specified conditions. This framework is particularly useful for testing and validating software that expects inputs adhering to specific syntactical and semantical rules.

## Features

- **Grammar-Based Input Generation**: Define complex input structures using grammars.
- **Constraint Specification**: Incorporate constraints directly into the grammar files.
- **Genetic Algorithm Optimization**: Utilize genetic algorithms to evolve inputs that satisfy the constraints.
- **Customizable Parameters**: Adjust population size, mutation rates, crossover rates, and more via command-line arguments.
- **Command-Line Interface**: Easily run and configure the framework using CLI options.
- **Extensible Framework**: Easily add new constraints and grammars.

---

## Table of Contents

- [Installation](#installation)
- [Writing FANDANGO Files](#writing-fandango-files)
  - [Grammar Definition](#grammar-definition)
  - [Constraint Specification](#constraint-specification)
  - [Examples](#examples)
    - [Number Example](#number-example)
    - [CSV Example](#csv-example)
- [Running the Framework](#running-the-framework)
  - [Framework Code](#framework-code)
  - [Command-Line Arguments](#command-line-arguments)
- [Running the Evaluation](#running-the-evaluation)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

### Prerequisites

- **Python 3.11**

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/joszamama/fandango
   cd fandango
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages**

   ```bash
   pip install -r requirements.txt
   ```

---

## Writing FANDANGO Files

A FANDANGO (`.fan`) file combines both **grammar definitions** and **constraints**.

### Grammar Definition

Grammars are defined using Backus-Naur Form (BNF)-like syntax:

- **Non-Terminals**: Enclosed in `<` and `>`, e.g., `<number>`.
- **Terminals**: Enclosed in double quotes, e.g., `"0"`.
- **Rules**: Defined using `::=`, with alternatives separated by `|`.

Example:

```bnf
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
```

### Constraint Specification

Constraints are specified using Python code within the `.fan` file. They can be:

- **Boolean Functions**: Functions that return `True` or `False`.
- **Assertions**: Using the `assert` statement.
- **Quantifiers**: Using `forall` or `exists` to specify constraints over parts of the grammar.

Syntax:

- **Define a Function**:

  ```python
  def is_odd(x):
      return x % 2 != 0
  ```

- **Use an Assertion**:

  ```python
  assert is_odd(3)
  ```

- **Apply Constraint to a Non-Terminal**:

  ```python
  is_odd(<number>);
  ```

- **Use Quantifiers**:

  ```python
  forall <r1> in <csv_record>:
      |<r1>.<csv_string_list>.<raw_field>| == 3;
  ```

### Examples

#### Number Example

**File**: `number.fan`

```bnf
<start> ::= <number>;
<number> ::= <non_zero><digit>* | "0";
<non_zero> ::=
              "1"
            | "2"
            | "3"
            | "4"
            | "5"
            | "6"
            | "7"
            | "8"
            | "9"
            ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";
```

**Constraints**:

```python
def is_odd(x):
    return x % 2 != 0

assert is_odd(3)

is_odd(<number>);
```

**Explanation**:

- **Grammar**: Defines numbers, including digits and non-zero digits.
- **Constraint**: The `is_odd` function checks if a number is odd. The constraint `is_odd(<number>);` ensures that generated numbers are odd.

#### CSV Example

**File**: `csv.fan`

```bnf
<start> ::= <csv_file> ;
<csv_file> ::= <csv_header> <csv_records> ;
<csv_header> ::= <csv_record> ;
<csv_records> ::= <csv_record> <csv_records> | "" ;
<csv_record> ::= <csv_string_list> "\n" ;
<csv_string_list> ::= <raw_field> | <raw_field> ";" <csv_string_list> ;
<raw_field> ::= <simple_field> | <quoted_field> ;
<simple_field> ::= <spaces> <simple_characters> <spaces> ;
<simple_characters> ::= <simple_character> <simple_characters> | <simple_character> ;
<simple_character> ::= /* All printable ASCII characters except special ones */;
<quoted_field> ::= '"' <escaped_field> '"' ;
<escaped_field> ::= <escaped_characters> ;
<escaped_characters> ::= <escaped_character> <escaped_characters> | "" ;
<escaped_character> ::= /* All printable ASCII characters, including spaces and control characters */;
<spaces> ::= "" | " " <spaces> ;
```

**Constraint**:

```python
forall <r1> in <csv_record>:
    forall <r2> in <csv_record>:
        |<r1>.<csv_string_list>.<raw_field>| == |<r2>.<csv_string_list>.<raw_field>|
;
```

**Explanation**:

- **Grammar**: Defines the structure of a CSV file.
- **Constraint**: Ensures that all CSV records have the same number of fields.

---

## Running the Framework

To run the FANDANGO framework with your `.fan` files and utilize the command-line interface, use the `framework.py` script.

### Framework Code

**File**: `framework.py`

```python
# framework.py

import argparse
from fandango.evolution.algorithm import FANDANGO
from fandango.language.parse import parse_file

def main():
    parser = argparse.ArgumentParser(description='FANDANGO Grammar-Based Genetic Algorithm Framework')
    parser.add_argument('fan_file_path', type=str, help='Path to the .fan file containing the grammar and constraints')
    parser.add_argument('-p', '--population_size', type=int, default=100, help='Population size (default: 100)')
    parser.add_argument('-m', '--mutation_rate', type=float, default=0.1, help='Mutation rate (default: 0.1)')
    parser.add_argument('-c', '--crossover_rate', type=float, default=0.9, help='Crossover rate (default: 0.9)')
    parser.add_argument('-g', '--max_generations', type=int, default=100, help='Maximum number of generations (default: 100)')
    parser.add_argument('-e', '--elitism_rate', type=float, default=0.2, help='Elitism rate (default: 0.2)')
    parser.add_argument('-k', type=int, default=10, help='Number of paths in initial population generation (default: 10)')
    parser.add_argument('-d', '--max_depth', type=int, default=20, help='Maximum depth of derivation trees (default: 20)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Parse the grammar and constraints from the .fan file
    grammar, constraints = parse_file(args.fan_file_path)

    # Initialize FANDANGO
    fandango = FANDANGO(
        grammar=grammar,
        constraints=constraints,
        population_size=args.population_size,
        mutation_rate=args.mutation_rate,
        crossover_rate=args.crossover_rate,
        max_generations=args.max_generations,
        elitism_rate=args.elitism_rate,
        k=args.k,
        max_depth=args.max_depth,
        verbose=args.verbose
    )

    # Run the evolution process
    fandango.evolve()

    # Output the best solution found
    if fandango.best_individual:
        print("\nBest individual found:")
        print(fandango.best_individual)
    else:
        print("\nNo individual satisfying all constraints was found.")

if __name__ == "__main__":
    main()
```

### Command-Line Arguments

You can customize the behavior of the framework using various command-line arguments.

#### Usage

```bash
python framework.py path/to/yourfile.fan [options]
```

#### Example Command

```bash
python framework.py number.fan -p 200 -m 0.05 -c 0.8 -g 50 -e 0.1 -k 5 -d 15 -v
```

#### Displaying Help

To see all available options and their descriptions, run:

```bash
python framework.py -h
```

- **`fan_file_path`**: The path to your `.fan` file containing the grammar and constraints.

- **`-p`, `--population_size`**: Sets the number of individuals in the population. Increasing this can improve diversity but may increase computation time.

- **`-m`, `--mutation_rate`**: Sets the probability of mutation occurring during evolution. Higher rates introduce more variability.

- **`-c`, `--crossover_rate`**: Sets the probability of crossover (recombination) occurring. Controls how often offspring are produced from parents.

- **`-g`, `--max_generations`**: Sets the maximum number of generations for the evolution process.

- **`-e`, `--elitism_rate`**: Sets the proportion of top-performing individuals carried over to the next generation.

- **`-k`**: Determines the number of paths used in the initial population generation.

- **`-d`, `--max_depth`**: Sets the maximum depth of derivation trees to prevent excessively large structures.

- **`-v`, `--verbose`**: Enables verbose output to monitor the evolution process.

---

## Running the Evaluation

To reproduce the results from our paper or to run the evaluation suite:

1. **Navigate to the Evaluation Directory**

   ```bash
   cd src/evaluation
   ```

2. **Run the Evaluation Script**

   ```bash
   python run_evaluation.py
   ```

   - This script will process all `.fan` files in the `src/evaluation` directory.
   - It will generate inputs and evaluate them against the specified constraints.
   - Results will be output to the console.

---

## Contributing

We welcome contributions to the FANDANGO project! To contribute:

1. **Fork the Repository**

2. **Create a Feature Branch**

3. **Commit Your Changes**

4. **Submit a Pull Request**

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

---

## License

This project is licensed under the **MIT License**.

---

## Contact

For questions or suggestions, please open an issue on the [GitHub repository](https://github.com/yourusername/fandango).

---

© 2024 FANDANGO Contributors
```