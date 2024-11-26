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
# Using (Fake) Data Generators

```{error}
This chapter is still in construction.
```


Often, you don't want to generate _totally_ random data; it suffices that _some_ aspects of it are random.
This naturally raises the question: Where can one get non-random, _natural_ data from, and how can one integrate this into Fandango?


## Augmenting Grammars with Data

The straightforward solution would be to simply extend our grammar with more natural data.
In order to obtain more natural first and last names in our [ongoing names/age example](sec:fuzzing), for instance, we could simply extend the [`persons.fan`](persons.fan) rule

```
<first_name> ::= <name>;
```

to

:::{margin}
These are the given names on [Pablo Picasso](https://en.wikipedia.org/wiki/Pablo_Picasso)'s birth certificate.
:::

```
<first_name> ::= <name> | "Alice" | "Bob" | "Eve" | "Pablo Diego José Francisco de Paula Juan Nepomuceno Cipriano de la Santísima Trinidad";
```

and extend the rule

```
<last_name> ::= <name>;
```

to, say,

```
<last_name> ::= <name> | "Doe" | "Smith" | "Ruiz Picasso";
```

then we can have Fandango create names such as

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-nat.fan -n 10
```

Note that we still get a few "random" names; this comes as specified by our rules.
By default, Fandango picks each alternative with equal likelihood, so there is a 20% chance for the first name and a 25% chance for the last name to be completely random.

:::{note}
Future Fandango versions will have means to control these likelihoods.
:::


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

```
<first_name> ::= <name> = fake.first_name();
```

The _generator_ `= EXPR` assigns the value produced by the expression `EXPR` (in our case, `fake.first_name()`) to the symbol on the left-hand side of the rule (in our case, `<first_name>`).

We can do the same for the last name:

```
<last_name> ::= <name> = fake.last_name();
```

(Show the full file)

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-faker.fan -n 10
```

(Why does one still have to specify the syntax? Give an example, say `<name>.startswith('S')`.)

:::{note}
The rule applies to _all_ productions, not just one alternative.
:::

:::{note}
Any functions you use still need to be imported.
:::

(Continue with more fakers)


## Creating Distributions

(TODO)

In the next section, we'll talk about [recursive inputs](sec:recursive).