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

(sec:regexes)=
# Regular Expressions

Although the Fandango grammars cover a wide range of input language features, there are situations where they may be a bit cumbersome to work with.
Consider specifying _every digit except for zeros_: this requires you to enumerate all the other digits `1`, `2`, and so on.
This is why Fandango also supports _regular expressions_, which allow you to use a concise syntax for character ranges, repeated characters and more.
Specifying all digits from `1` to `9`, for instance, becomes the short regular expression `r'[1-9]'`.


## About Regular Expressions

Regular expressions form a language on their own and come with several useful features.
To get an introduction to the regular expressions Fandango uses, read the Python [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) and check out the Python [Regular Expression Syntax](https://docs.python.org/3/library/re.html#regular-expression-syntax) for a complete reference.

In Fandango, regular expressions are used for two purposes:

* When _producing_ inputs, a regular expression is instantiated into a random string that matches the expression.
* When _parsing_ inputs, a regular expression is used to _parse_ and _match_ inputs.


## Writing Regular Expressions

:::{margin}
For Python aficionados: this is actually a Python "raw string"
:::

In Fandango, a regular expression comes as a string, prefixed with a `r` character.
To express that a digit can have the values `0` to `9`, instead of

```
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

you can write

```
<digit> ::= r'[0-9]'
```

which is much more concise.

Likewise, to match a sequence of characters that ends in `;`, you can write

```
<some_sequence> ::= r'[^;]+;'
```

Besides the `r` prefix indicating a regular expression, it also makes the string a _raw_ string.
This means that backslashes are treated as _literal characters_.
The regular expression `\d`, for instance, matches a Unicode digit, which includes `[0-9]`, and also [many other digit characters](https://en.wikipedia.org/wiki/Numerals_in_Unicode).
To include `\d` in a regular expression, write it _as is_; do not escape the backslash with another backslash (as you would do in a regular string):

:::{margin}
The expression `r'\\d'` would actually match a backslash, followed by a `d` character.
:::

```
<any_digit> ::= r'\d'
```

```{important}
Be aware of the specific syntax of `r`-strings as it comes to backslashes.
```

One consequence of backslashes being interpreted literally is that you cannot escape quote characters in a regular expression.
This causes a problem if you need two kinds of quotes (`"` and `'`) in the same regular expression – say, a rule that checks for forbidden characters.

However, encodings of the form `\xNN` are also interpreted by regular expressions.
Hence, if you need quotes, you can use

* `\x22` instead of `"`
* `\x27` instead of `'`

Here is an example:

```
<forbidden_characters> ::= r'[\x22\x27;]'
```


## Fine Points about Regular Expressions

For parsing inputs, Fandango uses the Python [`re`](https://docs.python.org/3/library/re.html) module for matching strings against regular expressions;
for producing inputs, Fandango uses the Python [`exrex`](https://github.com/asciimoo/exrex) module for generating strings that match regular expressions.
All the `re` and `exrex` capabilities and limitations thus extend to Fandango.

% No longer true -- AZ
% :::{tip}
% For regex shortcuts, the `exrex` producer only produces characters in the range `\0x00` to `\0xff`:
%
% * for digits (`\d`), the characters `[0-9]`
% * for whitespace (`\s`), the characters `[ \t\n\r\f\v]`
% * for words (`\w`), the characters `[a-zA-Z0-9_]`
% * for non-words (`\W`), the character range `[^a-zA-Z0-9_]`
%
% To produce Unicode characters, make them part of an explicit range (e.g. `[äöüÄÖÜß]`).
% :::


### Repetition Limits

Most notably, `exrex` imposes a _repetition limit_ of 20 on generated strings that in principle can have arbitrary length; a `+` or `*` operator will not expand to more than 20 repetitions.
Thus, a grammar [`infinity.fan`](infinity.fan)

```{code-cell}
:tags: ["remove-input"]
!cat infinity.fan
```

that in principle, could produce arbitrary long sequences `abcabcabcabc...` will be limited to 20 repetitions at most:

```shell
$ fandango fuzz -f infinity.fan -n 10
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f infinity.fan -n 10 --validate
assert _exit_code == 0
```

To precisely control the number of repetitions, use the regular expression `{m,n}` construct, limiting the number of repetitions from `m` to `n`.
Let us limit the number of repetitions to the range 1..5:

```{code-cell}
:tags: ["remove-input"]
!cat finity.fan
```

This is what we get:

```shell
$ fandango fuzz -f finity.fan -n 5
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f finity.fan -n 5 --validate
assert _exit_code == 0
```

:::{tip}
Remember that _grammars_ also have operators `+`, `*`, `?`, and `{N,M}` which apply to the preceding grammar element, and work like their _regular expression_ counterparts.
Using these, we could also write the above as
```
<start> ::= "abc"+
```
and
```
<start> ::= "abc"{1,5}
```
respectively.
:::

### Regular Expressions over Bytes

Regular expressions can also be formed over bytes.
See [Bytes and Regular Expressions](sec:byte-regexes) for details.


## Regular Expressions vs. Grammars

:::{margin}
In theory, context-free grammars are a strict _superset_ of regular expressions - any language that can be expressed in a regular expression can also be expressed in an equivalent grammar.
Practical implementations of regular expressions break this hierarchy by introducing some features such as _backreferences_ (check out what `(?P=name)` does), which cannot be expressed in grammars.
:::

In many cases, a grammar can be replaced by a regular expression and vice versa.
This raises the question: When should one use a regular expression, and when a grammar?
Here are some points to help you decide.

* Regular expressions are often more _concise_ (but arguably harder to read) than grammars.
* If you want to _reference_ individual elements of a string (say, as part of a constraint now or in the future), use a _grammar_.
* Since their underlying model is simpler, regular expressions are _faster_ to generate, and _much faster_ to [parse](Parsing.md) than grammars.
* If your underlying language separates lexical and syntactical processing, use
    - _regular expressions_ for specifying _lexical_ parts such as tokens and fragments;
    - a _grammar_ for the _syntax_; and
    - [constraints](Constraints.md) for any semantic properties.
* Prefer grammars and constraints over overly complex regular expressions.


```{important}
Do not use regular expressions for inputs that are [recursive](Recursive.md).
Languages like HTML, XML, even e-mail addresses or URLs, are much easier to capture as grammars.
```


## Regular Expressions as Equivalence Classes

The choice of grammars vs. regular expressions also affects the Fandango generation algorithm.
Generally speaking, Fandango attempts to cover all alternatives of a grammar.
If, say, `<digits>` is specified as

```
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
```

then Fandango will attempt to produce every digit at least once, and also try to cover digit _combinations_ up to a certain depth.
This is useful if you want to specifically test digit processing, or if each of the digits causes a different behavior that needs to be covered.

If, however, you specify `<digits>` as

```
<digit> ::= r'[0-9]'
```

then Fandango will treat this as a _single_ alternative (with all expansions considered semantically equivalent), which once expanded into (some) digit will be considered as covered.

```{tip}
* If you do want or need to _differentiate_ between individual elements of a set (because they would be treated differently), consider _grammar alternatives_.
* If you do _not_ want or need to differentiate between individual elements of a set (because they would all be treated the same), consider a _regular expression_.
```

