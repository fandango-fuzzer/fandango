### **Project Overview**

FANDANGO implements a **grammar-based fuzzer enhanced with a genetic algorithm**. FANDANGO generates inputs that not only adhere to a formal grammar but also satisfy specific constraints or goals. The genetic algorithm evolves a population of inputs (represented as derivation trees) to maximize a fitness function derived from these constraints.
The primary aim of the project is to **generate inputs that satisfy complex constraints** by leveraging the structure provided by a formal grammar and the optimization capabilities of a genetic algorithm. This approach is particularly useful for testing and fuzzing applications where generating valid and interesting inputs can uncover edge cases and potential bugs.
### **Repository Structure**

The project is organized into several modules within the `fandango` package:

1. **Constraints Module (`fandango/constraints/base.py`):**
   - **Purpose:** Defines the constraint system and how fitness is calculated based on these constraints.
   - **Key Classes:**
     - `Constraint`: Abstract base class for all constraints.
     - `ExpressionConstraint`, `ComparisonConstraint`, `ConjunctionConstraint`, `DisjunctionConstraint`, `ImplicationConstraint`, `ExistsConstraint`, `ForallConstraint`: Different types of constraints that can be applied to derivation trees.
     - `Fitness`: Holds information about the fitness score and whether the constraints are satisfied.

2. **Evolution Module (`fandango/evolution/optimizer.py`):**
   - **Purpose:** Implements the genetic algorithm that evolves derivation trees to satisfy the constraints.
   - **Key Classes:**
     - `GeneticAlgorithmOptimizer`: Manages the population, selection, crossover, and mutation processes.

3. **Language Module (`fandango/language/`):**
   - **Purpose:** Handles parsing and processing of grammars and constraints, as well as searching within derivation trees.
   - **Submodules:**
     - `convert.py`: Converts grammar and constraints from their textual representation into internal structures using ANTLR-generated parsers.
       - **Classes:** `FandangoSplitter`, `GrammarProcessor`, `ConstraintProcessor`, `SearchProcessor`.
     - `grammar.py`: Defines the grammar structures and derivation tree nodes.
       - **Classes:** `Grammar`, `Node` (and its subclasses like `Alternative`, `Concatenation`, `Repetition`, `NonTerminal`, `Terminal`), `DerivationTree`.
     - `search.py`: Provides classes to search and manipulate derivation trees based on non-terminal symbols.
       - **Classes:** `NonTerminalSearch`, `RuleSearch`, `AttributeSearch`, `LengthSearch`.

4. **Framework (`fandango/framework.py`):**
   - **Purpose:** Demonstrates how to use the modules together to perform grammar-based fuzzing with constraints.
   - **Functionality:**
     - Defines a simple grammar for numbers.
     - Sets up constraints (e.g., number must be odd, less than 10,000, and end with '1').
     - Initializes the `GeneticAlgorithmOptimizer` with the grammar and constraints.
     - Runs the optimizer to evolve inputs that satisfy the constraints.

### **Detailed Breakdown**

#### **Constraints Module**

- **Constraint System:**
  - Constraints are rules that the generated inputs must satisfy.
  - Each constraint can evaluate a derivation tree and produce a `Fitness` object indicating how well the tree satisfies the constraint.

- **Fitness Evaluation:**
  - Fitness is calculated as the ratio of constraints solved to total constraints.
  - The `Fitness` class holds this ratio along with information about which parts of the tree failed to meet the constraints.

- **Types of Constraints:**
  - **ExpressionConstraint:** Evaluates a Python expression in the context of the derivation tree.
  - **ComparisonConstraint:** Compares values extracted from the tree using specified operators (e.g., EQUAL, NOT_EQUAL).
  - **Logical Constraints:** Combine other constraints using logical operators (AND, OR, NOT), implications, and quantifiers (exists, forall).

#### **Evolution Module**

- **Genetic Algorithm:**
  - **Population Initialization:** Starts with a population of randomly generated derivation trees based on the grammar.
  - **Fitness Evaluation:** Each individual (derivation tree) is evaluated using the constraints.
  - **Selection:** Parents are selected based on fitness-proportional selection (roulette wheel).
  - **Crossover:** Combines parts of two parents to create offspring. Supports both random and constraint-driven crossover methods.
  - **Mutation:** Randomly alters parts of an individual. Supports both random and constraint-driven mutation methods.
  - **Elitism:** A fraction of the best-performing individuals are carried over to the next generation unchanged.

- **Constraint-Driven Operations:**
  - **Crossover and Mutation:** Focus on parts of the derivation trees that failed to satisfy constraints to improve efficiency.

#### **Language Module**

- **Grammar Processing:**
  - **Grammar Representation:** Uses classes to represent grammar rules and constructs (e.g., alternatives, concatenations, repetitions).
  - **Derivation Trees:** Trees that represent the expansion of grammar rules to generate concrete inputs.

- **Parsing and Conversion:**
  - **ANTLR Parsers:** Used to parse grammar definitions and constraints from text.
  - **Converters:** Transform parsed representations into internal structures usable by the optimizer.

- **Search Functionality:**
  - **NonTerminalSearch:** Abstract base class for searching derivation trees.
  - **RuleSearch:** Finds nodes in the derivation tree that correspond to a specific non-terminal symbol.
  - **AttributeSearch:** Navigates through attributes or relationships in the tree.
  - **LengthSearch:** Determines the length of specific parts of the tree, useful for constraints involving length.

#### **Framework (Example Usage)**

- **Grammar Definition:**
  ```plaintext
  <start> ::= <number> ;
  <number> ::= <non_zero> <digit>* | "0" ;
  <non_zero> ::= "1" | "2" | "3"| "4" | "5" | "6" | "7" | "8" | "9" ;
  <digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
  ```

- **Constraints:**
  - **Odd Number Constraint:** The number must be odd (`int(number) % 2 != 0`).
  - **Less Than 10,000 Constraint:** The number must be less than 10,000 (`int(number) < 10000`).
  - **Ends With '1' Constraint:** The number must end with '1' (`int(number) % 10 == 1`).

- **Optimizer Configuration:**
  - Uses the constraint-driven methods for crossover and mutation to focus on parts of the input that fail constraints.
  - Evolves the population to find numbers satisfying all the constraints.

- **Execution:**
  - The optimizer runs for a specified number of generations or until a satisfactory solution is found.
  - Prints out the time taken and the final solution.
