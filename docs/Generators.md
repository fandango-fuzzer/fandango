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

(sec:generators)=
# Data Generators and Fakers

Often, you don't want to generate _totally_ random data; it suffices that _some_ aspects of it are random.
This naturally raises the question: Where can one get non-random, _natural_ data from, and how can one integrate this into Fandango?


## Augmenting Grammars with Data

The straightforward solution would be to simply extend our grammar with more natural data.
In order to obtain more natural first and last names in our [ongoing names/age example](sec:fuzzing), for instance, we could simply extend the [`persons.fan`](persons.fan) rule

```
<first_name> ::= <name>
```

to

:::{margin}
These are the given names on [Pablo Picasso](https://en.wikipedia.org/wiki/Pablo_Picasso)'s birth certificate.
:::

```
<first_name> ::= <name> | "Alice" | "Bob" | "Eve" | "Pablo Diego José Francisco de Paula Juan Nepomuceno Cipriano de la Santísima Trinidad"
```

and extend the rule

```
<last_name> ::= <name>
```

to, say,

```
<last_name> ::= <name> | "Doe" | "Smith" | "Ruiz Picasso"
```

then we can have Fandango create names such as

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-nat.fan -n 10 --validate
assert _exit_code == 0
```

Note that we still get a few "random" names; this comes as specified by our rules.
By default, Fandango picks each alternative with equal likelihood, so there is a 20% chance for the first name and a 25% chance for the last name to be completely random.

```{note}
Future Fandango versions will have means to control these likelihoods.
```


## Using Fakers

Frequently, there already are data sources available that you'd like to reuse – and converting each of their elements into a grammar alternative is inconvenient.
That is why Fandango allows you to _specify a data source as part of the grammar_ - as a _Python function_ that supplies the respective value.
Let us illustrate this with an example.

The Python `faker` module is a great source of "natural" data, providing "fake" data for names, addresses, credit card numbers, and more.

Here's an example of how to use it:

```{code-cell}
from faker import Faker
fake = Faker()
for i in range(10):
  print(fake.first_name())
```

Have a look at the [`faker` documentation](https://faker.readthedocs.io/) to see all the fake data it can produce.
The methods `first_name()` and `last_name()` are what we need.
The idea is to extend the `<first_name>` and `<last_name>` rules such that they can draw on the `faker` functions.
To do so, in Fandango, you can simply extend the grammar as follows:


:::{margin}
A generator applies to _all_ alternatives, not just the last one.
:::

```
<first_name> ::= <name> := fake.first_name()
```

:::{margin}
`:=` is the assignment operator in several programming languages; in Python, it can be used to assign values within expressions.
:::

The _generator_ `:= EXPR` _assigns_ the value produced by the expression `EXPR` (in our case, `fake.first_name()`) to the symbol on the left-hand side of the rule (in our case, `<first_name>`).

```{important}
Whatever value the generator returns, it must be _parseable_ by at least one of the alternatives in the rule. Our example works because `<first_name>` matches the format of `fake.first_name()`.
```

:::{tip}
If your generator returns a string, a "match-all" rule such as
```
<generated_string> ::= <char>* := generator()
```
will fit all possible string values returned by `generator()`.
:::

We can do the same for the last name, too; and then this is the full Fandango spec [persons-faker.fan](persons-faker.fan):

```{code-cell}
:tags: ["remove-input"]
!cat persons-faker.fan
```

```{note}
The [Fandango `include()` function](sec:including) _includes_ the Fandango definitions of the given file.
This way, we need not repeat the definitions from `persons.fan` and only focus on the differences.
```

```{note}
Python code (from Python files) that you use in a generator (or in a constraint, for that matter) needs to be imported.
Use the Python `import` features to do that.
```

:::{important}
`include(FILE)` is for Fandango files, `import MODULE` is for Python modules.
:::

This is what the output of the above spec looks like:


```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -n 10 --validate
assert _exit_code == 0
```

You see that all first and last names now stem from the Faker library.

## Number Generators

In the above output, the "age" fields are still very random, though.
With generators, we can achieve much more natural distributions.

After importing the Python `random` module:

```python
import random
```

we can make use of [dozens of random number functions](https://docs.python.org/3/library/random.html) to use as generators.
For instance, `random.randint(A, B)` return a random integer $n$ such that $A \le n \le B$ holds.
To obtain a range of ages between 25 and 35, we can thus write:

```
<age> ::= <digit>+ := str(random.randint(25, 35));
```

```{important}
All Fandango generators must return strings or byte strings.

* Use `str(N)` to convert a number N into a string
* Use `bytes([N])` to convert numbers N into bytes.
```

The resulting [Fandango spec file](persons-faker-age.fan) produces the desired range of ages:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker-age.fan -n 10 --validate
assert _exit_code == 0
```

We can also create a Gaussian (normal) distribution this way:

```
<age> ::= <digit>+ := str(int(random.gauss(35)));
```

`random.gauss()` returns floating point numbers.
However, the final value must fit the given symbol rules (in our case, `<digit>+`), so we convert the age into an integer (`int()`).

These are the ages we get this way:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker-gauss.fan -n 10 --validate
assert _exit_code == 0
```

In {ref}`sec:distributions`, we will introduce more ways to obtain specific distributions.


## Generators and Random Productions

In testing, you want to have a good balance between _common_ and _uncommon_ inputs:

* Common inputs are important because they represent the typical usage, and you don't want your program to fail there;
* Uncommon inputs are important because they uncover bugs you may _not_ find during alpha or beta testing, and thus avoid latent bugs (and vulnerabilities!) slipping into production.

We can easily achieve such a mix by adding rules such as

```
<first_name> ::= <name> | <natural_name>
<natural_name> ::= <name> := fake.first_name()
```

With this, both random names (`<name>`) and natural names (`<natural_name>`) will have a chance of 50% to be produced:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker50.fan -n 10 --validate
assert _exit_code == 0
```

(sec:generators-and-constraints)=
## Combining Generators and Constraints

When using a generator, why does one still have to specify the format of the data, say `<name>`?
This is so for two reasons:

:::{margin}
To allow access to the elements of the generator output, Fandango _parses_ the output according to the symbol rules.
:::

% TODO: reference a chapter on parsing/mutating here
1. It allows the Fandango spec to be used for _parsing_ existing data, and consequently, _mutating_ it;
2. It allows additional [_constraints_](Constraints.md) to be applied on the generator result and its elements.

In our example, the latter can be used to further narrow down the set of names.
If we want all last names to start with an `S`, for instance, we can invoke Fandango as

:::{margin}
Grammar symbols `<...>` support all [Python string methods](https://docs.python.org/3/library/stdtypes.html#string-methods).
:::

```shell
$ fandango fuzz -f persons-faker.fan -c '<last_name>.startswith("S")' -n 10
```

and we get

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -c '<last_name>.startswith("S")' -n 10 --validate
assert _exit_code == 0
```




## When to use Generators, and when Constraints

One might assume that instead of a generator, one could also use a _constraint_ to achieve the same effect. So, couldn't one simply add a constraint that says

% TODO: Shouldn't this also assign the value directly?
```
<first_name> == fake.first_name()
```

:::{margin}
In case this should work, this is only through some internal Fandango optimization that directly assigns computed values to symbols.
:::

Unfortunately, this does not work.
% ```{code-cell}
% :tags: ["remove-input"]
% !fandango fuzz -f persons-faker.fan -c '<first_name> == fake.first_name()' -n 10 --validate
% assert _exit_code == 0
% ```
The reason is that the faker returns _a different value_ every time it is invoked, making it hard for Fandango to solve the constraint.
Remember that Fandango solves constraints by applying mutations to a population, getting closer to the target with each iteration.
If the target keeps on changing, the algorithm will lose guidance and will not progress towards the solution.

Likewise, in contrast to our example in {ref}`sec:generators-and-constraints`, one may think about using a _constraint_ to set a limit to a number, say:

```shell
$ fandango fuzz -f persons-faker.fan -c '<last_name>.startswith("S")' -c 'int(<age>) >= 25 and int(<age>) <= 35' -n 10
```

This would work:
```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -c '<last_name>.startswith("S")' -c 'int(<age>) >= 25 and int(<age>) <= 35' -n 10 --validate --progress-bar=off
assert _exit_code == 0
```

But while the values will fit the constraint, they will not be randomly distributed.
This is because Fandango treats and generates them as _strings_ (= sequences of digits), ignoring thur semantics as numerical values.
To obtain well-distributed numbers from the beginning, use a generator.

1. If a value to be produced is _random_, it should be added via a _generator_.
2. If a value to be produced is _constant_, it can go into a _generator_ or a _constraint_.
3. If a value to be produced must be _part of a valid input_, it should go into a _constraint_. (Constraints are checked during parsing _and_ production.)
:::
