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

(sec:strategies)=
# Some Fuzzing Strategies

The idea of fuzzing is to have inputs that are _out of the ordinary_, so we can detect errors in input parsers and beyond.
But let us again have a look at the inputs we generated so far:

```shell
$ fandango fuzz -f persons.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 --validate
assert _exit_code == 0
```

Despite clearly looking non-natural to humans, the strings we generated so far are unlikely to trigger errors in a program, because programs typically treat all letters equally.
So let us bring a bit more _weirdness_ into our inputs.

```{danger}
Don't feed such fuzz inputs into other people's systems; this can have unpredictable consequences.
```

```{warning}
In most countries, even _trying_ to feed such inputs into other people's systems will get you into jail.
```



## Looooooong Inputs

One way to increase the probability of detecting bugs is to test with _long_ inputs.
While processing data, many programs have limited storage for individual data fields, and thus need to cope with inputs that exceed this storage space.
If programmers do not care for such long inputs, serious errors may follow.
So-called _buffer overflows_ have long been among the most dangerous vulnerabilities, as they can be exploited to gain unauthorized access to systems.


We can easily create long inputs by specifying the _number of repetitions_ in our grammar:

* Appending `{N}` to a symbol, where `N` is a number, makes Fandango repeat this symbol `N` times.
* Appending `{N,M}` to a symbol makes Fandango repeat this symbol between `N` and `M` times.
* Appending `{N,}` to a symbol makes Fandango repeat this symbol at least `N` times.

```{margin}
The `+`, `*`, and `?` suffixes are actually equivalent to `{1,}`, `{0,}`, and `{0,1}`, respectively.
```

If, for instance, we want the above names to be 100 characters long, we can set up a new rule for `<name>`

```
<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>{99}
```

and the lowercase letters will be repeated 99 times.

This is the effect of this rule:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons100.fan -n 10 --validate
assert _exit_code == 0
```

We see that the names are now much longer.
For real-world fuzzing, we may try even longer fields (say, 1,000) to test the limits of our system.

```{tip}
Programmers often make "off-by-one" errors, so if an input is specified to have at most `N` characters, you should test this exact boundary - say, by giving `N` and `N`+1 characters.
```

```{danger}
Don't try this with other people's systems; the consequences are unpredictable.
```


## Unusual Inputs

Having "weird" inputs also applies to numerical values.
Think about our "age" field, for instance.
What happens if we have a person with a negative age?

:::{margin}
Note that the grammar already can produce ages way above 100.
:::

Try it yourself and modify [`persons.fan`](persons.fan) such that it can also produce negative numbers, as in

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons-neg.fan -n 10 --validate
assert _exit_code == 0
```

Did you succeed? Compare your answer against the solution below.

:::{admonition} Solution
:class: tip, dropdown
You can, for instance, change the `<age>` rule such that it introduces an alternative for negative numbers:
```
<age> ::= <digit>+ | "-" <digit>+
```
Another way to do it is to use the `?` modifier, which indicates an optional symbol:
```
<age> ::= "-"? <digit>+
```
:::

Other kinds of unusual inputs would be character sets that are out of the ordinary - for instance, Chinese or Hebrew characters - or plain Latin characters if your system expects Chinese names.
A simple Emoji, for instance, could be enough to cause the system to fail.

:::{margin}
In Python, try `float('nan') * float('inf')` and other variations.
:::

For numbers, besides being out of range, there are a few constants that are interesting.
Some common number parsers and converters accept values such as `Inf` (infinity) or `NaN` (not a number) as floating-point values. These actually _are_ valid and have special rules – anything multiplied with `Inf` also becomes infinitely large (`Inf` times zero is zero, though); and any operation involving a `NaN` becomes `NaN`.

:::{margin}
Fortunately, number converters typically treat `NaN` as invalid.
:::

Imagine what happens if we manage to place a `NaN` value in a database?
Any computation involving this value would also become a `NaN`, so in our example, the average age of persons would become `NaN`.
The `NaN` could even go viral across Excel sheets, companies, shareholder reports, and eventually the stock market.
Luckily, programs are prepared against that - or are they?

```{danger}
Don't try this with other people's systems; the consequences are unpredictable.
```


## String Injections

Another kind of attack is to insert special _strings_ into the input – strings that would be interpreted by the program not as data, but as _commands_.
A typical example for this is a _SQL injection_.
Many programs use the SQL, the _structured query language_, as a means to interact with databases.
A command such as

```sql
INSERT INTO CUSTOMERS VALUES ('John Smith', 34);
```

would be used to save the values `John Smith` (name) and `34` (age) in the `CUSTOMERS` table.

A SQL injection uses specially formed strings and values to subvert these commands.
If our "age" value, for instance, is not `34`, but, say

```
34); CREATE TABLE PWNED (Phone CHAR(20)); --
```

then creating the above `INSERT` command with this special "age" could result in the following command:

:::{margin}
Two dashes (`--`) start a comment in SQL.
:::
```sql
INSERT INTO CUSTOMERS VALUES ('John Smith', 34); CREATE TABLE PWNED (Phone CHAR(20)); --);
```

and suddenly, we have "injected" a new command that will alter the database by adding a `PWNED` table.

How would one do this with a grammar?
Well, for the above, it suffices to have one more alternative to the `<age>` rule.

:::{admonition} Solution
:class: tip, dropdown
Here's how one could change the `<age>` rule:
```
<age> ::= <digit>+ | "-" <digit>+ 
        | <digit>+ "); CREATE TABLE PWNED (Phone CHAR(20)); --"
```
:::

Try adding such alternatives to _all_ data fields processed by a system; feed the Fandango-generated inputs to it; and if you then find a `PWNED` table on your system, you know that you have a vulnerability.

```{danger}
Don't try this with other people's systems; the consequences are unpredictable.
```
