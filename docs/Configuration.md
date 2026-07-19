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

(sec:configuration)=
# Configuration Options

Fandango provides several configuration options to control input generation and parsing behavior.

## max_repetitions

**Type:** `int` (default: `5`)

Controls the maximum number of times a repetition operator (`*`, `+`, `{n,m}`) can be expanded when generating inputs. This prevents infinite loops and ensures generation terminates.

### Example

```python
# Set max_repetitions to limit repetition expansions
fandango = Fandango(max_repetitions=5)

# Or in your .fan file
@config(max_repetitions=5)
```

### Use Cases
* **Performance**: Lower values for faster generation
* **Testing**: Higher values to test deeper structures
* **Resource constraints**: Prevent excessively large inputs

## Setting Options in `.fan` Files

You can directly configure Fandango options within your `.fan` grammar files. This allows your specification to be self-contained, specifying the ideal execution environment without relying on external shell scripts or command-line flags.

To set an option, use the `# @option` directive at the beginning of the file or on its own line:

```fan
# @option max_repetitions = 10
# @option mutation_rate = 0.5
# @option desired_solutions = 100

<start> ::= <expr>
```

### Supported Options
You can configure any option that is supported by the `Fandango.fuzz()` or `Fandango.init_population()` methods (such as `max_repetitions`, `desired_solutions`, `mutation_rate`, `max_generations`, etc).

### Option Precedence
Fandango resolves options with the following priority:
1. **Explicit API arguments or Command-line arguments** (highest precedence)
2. **Options set in `.fan` files** via `# @option`
3. **Fandango defaults** (lowest precedence)
