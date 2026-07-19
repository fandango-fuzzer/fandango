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
