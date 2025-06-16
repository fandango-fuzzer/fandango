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

(sec:python-api)=
# Python API Reference

Fandango provides a simple API for Python programs to

* [_load_ a `.fan` specification with `Fandango()`](sec:fandango-class);
* [_produce outputs_ from the spec with `fuzz()`](sec:fuzz-api); and
* [_parse inputs_ using the spec with `parse()`](sec:parse-api).

```{note}
This API will be extended over time.
```

## Installing the API

When you [install Fandango](sec:installing), the Python Fandango API is installed as well.


```{code-cell}
:tags: ["remove-input", "remove-output"]
# Monkey hack to prevent "_UnixSelectorEventLoop" exceptions
# See https://stackoverflow.com/questions/75760275/unixselectoreventloop-has-no-attribute-closed-nor-other-instance-attributes

import asyncio

_original_del = asyncio.base_events.BaseEventLoop.__del__

def _patched_del(self):
    try:
        _original_del(self)
    except:
        pass

asyncio.base_events.BaseEventLoop.__del__ = _patched_del
```

```{code-cell}
:tags: ["remove-input", "remove-output"]
# Redirect logging to stdout to avoid warnings about stderr output
import logging
import sys

logging.basicConfig(
    level=logging.WARNING,
    stream=sys.stdout,
    format="%(name)s:%(levelname)s: %(message)s",
)
```


(sec:fandango-class)=
## The `Fandango` class

The Fandango API comes as a class, named `Fandango`.
To use it, write

```{code-cell}
from fandango import Fandango
```

The `Fandango` constructor allows reading in a `.fan` specification, either from an (open) file, a string, or a list of strings or files.

```python
class Fandango(fan_files: str | IO | List[str | IO],
    constraints: List[str] = None, *,
    start_symbol: Optional[str] = None,
    use_cache: bool = True,
    use_stdlib: bool = True,
    logging_level: Optional[int] = None)
```

Create a `Fandango` object.

* `fan_files` is the Fandango specification to load.
This is either
  - a _string_ holding a `.fan` specification; or
  - an (open) `.fan` _file_; or
  - a _list_ of strings or files.
* `constraints`, if given, is a list of additional constraints (as strings).
* `start_symbol` is the start symbol to use (default: `<start>`).
* `use_cache` can be set to `False` to avoid loading the input from cache.
* `use_stdlib` can be set to `False` to avoid loading the [standard library](sec:stdlib).
* `includes`: A list of directories to search for include files before the [Fandango spec locations](sec:including).
* `logging_level` controls the logging output. It can be set to any of the values in the [Python logging module](https://docs.python.org/3/library/logging.html), such as `logging.DEBUG` or `logging.INFO`. Default is `logging.WARNING`.

```{warning}
Be aware that `.fan` files can contain Python code that is _executed when loaded_. This code can execute arbitrary commands.
```

```{warning}
Code in the `.fan` spec cannot access identifiers from the API-calling code or vice versa. However, as both are executed in the same Python interpreter, there is a risk that loaded `.fan` code may bypass these restrictions and gain access to the API-calling code.
```

```{caution}
Only load `.fan` files you trust.
```


`Fandango()` can raise a number of exceptions, including

* `FandangoSyntaxError` if the `.fan` input has syntax errors. The exception attributes `line`, `column`, and `msg` hold the line, column, and error message.
* `FandangoValueError` if the `.fan` input has consistency errors.

The exception class `FandangoError` is the superclass of these exceptions.



(sec:fuzz-api)=
## The `fuzz()` method

On a `Fandango` object, use the `fuzz()` method to produce outputs from the loaded specification.

```python
fuzz(extra_constraints: Optional[List[str]] = None, **settings)
    -> List[DerivationTree])
```

Create outputs from the specification, as a list of [derivation trees](sec:derivation-tree).

```{margin}
In the future, the set of available `settings` may change dependent on the chosen algorithm.
```

* `extra_constraints`: if given, use this list of strings as additional constraints
* `settings`: pass extra values to control the fuzzer algorithm. These include
  - `population_size: int`: set the population size (default: 100).
  - `desired_solutions: int`: set the number of desired solutions.
  - `initial_population: List[Union[DerivationTree, str]]`: set the initial population.
  - `max_generations: int`: set the maximum number of generations (default: 500).
  - `warnings_are_errors: bool` can be set to True to raise an exception on warnings.
  - `best_effort: bool` can be set to True to return the population even if it does not satisfy the constraints.

The `fuzz()` method returns a list of [`DerivationTree` objects](sec:derivation-tree). These are typically converted into Python data types (typically using `str()` or `bytes()`) to be used in standard Python functions.

`fuzz()` can raise a number of exceptions, including

* `FandangoFailedError` if the algorithm failed _and_ `warnings_are_errors` is set.
* `FandangoValueError` if algorithm settings are invalid.
* `FandangoParseError` if a generator value could not be parsed.

The exception class `FandangoError` is the superclass of these exceptions.


(sec:parse-api)=
## The `parse()` method

On a `Fandango` object, use the `parse()` method to parse an input using the loaded specification.

```python
parse(word: str | bytes | DerivationTree, *, prefix: bool = False, **settings)
    -> Generator[DerivationTree, None, None]
```

Parse a word; return a generator for [derivation trees](sec:derivation-tree).

* `word`: the word to be parsed. This can be a string, a byte string, or a derivation tree.
* `prefix`: if True, allow incomplete inputs that form a prefix of the inputs accepted by the grammar.
* `settings`: additional settings for the parser.
  - There are no additional user-facing settings for the parser at this point.

The return value is a _generator_ of derivation trees - if the `.fan` grammar is ambiguous, a single word may be parsed into different trees.
To iterate over all trees parsed, use a construct such as

```python
for tree in fan.parse(word):
    ...  # do something with the tree
```

`parse()` can raise exceptions, notably

* `FandangoParseError` if parsing fails. The attribute `position` of the exception indicates the position in `word` at which the syntax error was detected.[^position]

[^position]: Note that due to parser lookahead, the position may be slightly off the position of the actual error.

```{note}
At this point, the `parse()` method does not check whether constraints are satisfied.
```

(sec:api-example)=
## API Usage Examples

### Fuzzing from a `.fan` Spec

Let us read and produce inputs from [`persons-faker.fan`](persons-faker.fan) discussed in [the section on generators and fakers](sec:generators):

```{code-cell}
from fandango import Fandango

# Read in a .fan spec from a file
with open('persons-faker.fan') as persons:
    fan = Fandango(persons)

for tree in fan.fuzz(desired_solutions=10):
    print(str(tree))
```

### Fuzzing from a `.fan` String

We can also read a `.fan` spec from a string. This also demonstrates the usage of the `logging_level` parameter.

```{code-cell}
from fandango import Fandango
import logging

# Read in a .fan spec from a string
spec = """
    <start> ::= ('a' | 'b' | 'c')+
    where str(<start>) != 'd'
"""

fan = Fandango(spec, logging_level=logging.INFO)
for tree in fan.fuzz(desired_solutions=10):
    print(str(tree))
```


### Parsing an Input

This example illustrates usage of the `parse()` method.

```{code-cell}
from fandango import Fandango

spec = """
    <start> ::= ('a' | 'b' | 'c')+
    where str(<start>) != 'd'
"""

fan = Fandango(spec)
word = 'abc'

for tree in fan.parse(word):
    print(f"tree = {repr(str(tree))}")
    print(tree.to_grammar())
```

Use the [`DerivationTree` functions](sec:derivation-tree) to convert and traverse the resulting trees.


### Parsing an Incomplete Input

This example illustrates how to parse a prefix (`'ab'`) for a grammar that expects a final `d` letter.

```{code-cell}
from fandango import Fandango

spec = """
    <start> ::= ('a' | 'b' | 'c')+ 'd'
    where str(<start>) != 'd'
"""

fan = Fandango(spec)
word = 'ab'

for tree in fan.parse(word, prefix=True):
    print(f"tree = {repr(str(tree))}")
    print(tree.to_grammar())
```

Without `prefix=True`, parsing would fail:

```{code-cell}
:tags: ["raises-exception"]
from fandango import Fandango

spec = """
    <start> ::= ('a' | 'b' | 'c')+ 'd'
    where str(<start>) != 'd'
"""

fan = Fandango(spec)
word = 'ab'

fan.parse(word)
```



### Handling Parsing Errors

This example illustrates handling of `parse()` errors.

```{code-cell}
from fandango import Fandango, FandangoParseError

spec = """
    <start> ::= ('a' | 'b' | 'c')+
    where str(<start>) != 'd'
"""

fan = Fandango(spec)
invalid_word = 'abcdef'

try:
    fan.parse(invalid_word)
except FandangoParseError as exc:
    error_position = exc.position
    print("Syntax error at", repr(invalid_word[error_position]))
```
