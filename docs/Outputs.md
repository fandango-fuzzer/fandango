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

(sec:outputs)=
# Checking Outputs

Since Fandango makes use of specifications both to [_produce_](sec:fuzzing) and to [_parse_](sec:parsing) strings, it can actually _combine both_ to

1. first send an input to a program under test; and
2. then parse its output to check if it produced the correct result.

For this purpose, Fandango provides a means to combine both input and output in a _single specification_, used by the Fandango `talk` command.
Let us see how this works.

```{admonition} Under Construction
:class: attention
Checking outputs is currently in beta.
Check out [the list of open issues](https://github.com/fandango-fuzzer/fandango/issues).
```


## Interaction Testing

So far, we have only considered two settings.
In _fuzzing_, Fandango sends a synthesized input to the program under test:

% See https://mermaid.js.org/syntax/sequenceDiagram.html

```{mermaid}
sequenceDiagram
    Fandango->>Program under Test: Some input
```

During _parsing_, Fandango accepts and processes _outputs_ from the program under test:

```{mermaid}
sequenceDiagram
    Program under Test-->>Fandango: Some output
```

What we want, though, is an _interaction_ - a means to _first_ send an input to the program, and then parse its output to check it:

```{mermaid}
sequenceDiagram
    Fandango->>Program under Test: Some input
    Program under Test-->>Fandango: Some output
```

For this, we need to specify which parts of the interaction are supposed to be _sent_ or _received_ by which _party_ in the interaction.


## Simple Input/Output Testing

Fandango allows a simple means to combine inputs and outputs in a single `.fan` specification.
The key idea is to _identify individual nonterminals with the party that is supposed to produce it_.
In Fandango, this is done by prefixing the nonterminal with a party name (an identifier), followed by a colon (`:`).
Hence, a nonterminal `<fandango:string>` refers to a `<string>` element that would be produced by a party named `fandango` (whoever that might be).

Fandango conveniently defines two standard parties:

* `In` refers to the standard input of the program under test; and
* `Out` refers to the standard output of the program under test.

Hence, in a Fandango spec, `<In:id>` refers to an `<id>` element that is _received_ (or input) by the program, and `<Out:result>` is a `<result>` element that is _sent_ (or output) by the program.

```{important}
Remember that `In` and `Out` describe the interaction from the _perspective of the program under test_.
```

With this, we can already write a first specification.

```{margin}
`cat` is an abbreviation for "concatenate". `cat` can take multiple inputs, and concatenates them as one.
```
The UNIX `cat` command accepts some input, and outputs this very input unchanged.
In Fandango, this interaction can be described in a file [`cat.fan`](cat.fan) as follows:

```{code-cell}
:tags: ["remove-input"]
!cat cat.fan
```

In this specification,

* `<input>` and `<output>` define the inputs and outputs of `cat`, respectively, as a `<string>`; and
* `<string>` defines a regular expression standing for any sequence of characters, including newlines.

Let us use Fandango with this spec to test the `cat` program.


## The Fandango `talk` command

Fandango provides a `talk` command that allows testing interactions.
Like `fuzz` and `parse`, it takes as argument a `-f` option, followed by a `.fan` file; however, this one must contain party specifications.
The remainder of the command line is the program to be tested (possibly with arguments).

In our case, this is how the invocation of Fandango looks like:

```shell
$ fandango talk -f cat.fan cat
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f cat.fan -n 1 --population-size 1 cat
assert _exit_code == 0
```

This command does not issue any outputs (all of them are being sent to `cat`), but here is what is happening behind the scenes:

* The `cat` command sends back the input via its output;
* Fandango receives and parses the `cat` output.


We can also specify multiple interactions, as in

```shell
$ fandango talk -f cat.fan -n 10 cat
```

Now, each time, `cat` is started anew, as shown in this diagram:
```{mermaid}
sequenceDiagram
    Fandango->>cat: "eroih&^%^32"
    cat-->>Fandango: "eroih&^%^32"
    Fandango->>cat2: "0[9481]^^^\n\n"
    cat2-->>Fandango: "0[9481]^^^\n\n"
    Fandango->>cat3: "ewifehfba"
    cat3-->>Fandango: "ewifehfba"
```

```{note}
Once a communication party is set for a nonterminal, it need not be repeated for its constituents.
In the above example, we can define `<input>` as `<string>` without restating the `In:` prefix; from the first line, it is clear that `<input>` comes from `In`.
Also, this allows multiple parties to share the same elements (such as `<string>`).
```

## Oracles

So far, our `.fan` specification has not really checked whether `cat` operates correctly.
It does check the `cat` output against the `<string>` regular expression - but that is a "match-all" expression, meaning that anything is valid.

To check whether the `cat` output is correct, we must compare it against the input we sent and ensure that input and output are identical.
For this, [constraints](sec:constraints) are the ideal tool, as they allow us to reference arbitrary elements in the entire interaction.
In our case, this simple constraint would suffice:

```python
str(<input>) == str(<output>)
```

This constraint defines the full behavior of `cat`; it acts as an _oracle_ that determines whether the behavior of the program under test is correct or not.

Let us add this constraint using a `where` clause to `cat.fan`, resulting in [`cat-oracle.fan`](cat-oracle.fan):

```{code-cell}
:tags: ["remove-input"]
!cat cat-oracle.fan
```

Again, we can test, and normally, nothing should happen.

```shell
$ fandango talk -f cat-oracle.fan cat
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f cat-oracle.fan -n 1 --population-size 1  cat
assert _exit_code == 0
```

```{margin}
The [first C implementation of `cat`](https://gist.github.com/sinclairtarget/47143ba52b9d9e360d8db3762ee0cbf5#file-3-cat-v7-c) had 80 lines of code.
A [detailed history of `cat`](https://twobithistory.org/2018/11/12/cat.html) is available.
```

So far, we have mostly seen constraints as a _precondition_ - that is, a condition that makes inputs valid in the first place.
Our constraint here acts as a _postcondition_ – that is, a condition that checks the output, possibly based on earlier input features.


## More Complex Interactions

Let us now test a program whose interaction scheme is a bit more complex.
The UNIX `bc` command accepts a line with an arithmetic expression, and then produces the result.
It keeps on doing so until the input ends.
To compute `2 + 2`, we can enter

```shell
$ bc
>>> 2 + 2
4
>>> (Ctrl-D)
```

Here, `>>> ` is the prompt of the `bc` program; it goes to `stderr` and is only produced in interactive settings, so we can ignore it.
A typical interaction between Fandango and `bc` would thus look like this:

```{mermaid}
sequenceDiagram
    Fandango->>bc: 2 + 2\n
    bc-->>Fandango: 4\n
    Fandango->>bc: 3 * 7\n
    bc-->>Fandango: 21\n
```

Let us define a sequence of 10 interactions with `bc`.
Using our earlier [expression grammar](sec:recursive) [`expr.fan`](expr.fan), we can define such interactions in a `.fan` spec [`bc.fan`](bc.fan):

```{code-cell}
:tags: ["remove-input"]
!cat bc.fan
```

We see that the `<input>` now is an expression; and the expected `<output>` is an integer.
This is how we can test `bc`:

```shell
$ fandango talk -f bc.fan bc
```

% FIXME: Doesn't work yet - see bug #500
% ```{code-cell}
% :tags: ["remove-input"]
% !fandango talk -f bc.fan --population-size=1 bc
% assert _exit_code == 0
% ```

Our `.fan` spec checks that the `bc` indeed produces integers, but it does not check whether the result is correct, too.
How would one do this? (Hint: use the Python `eval()` function.)

:::{admonition} Solution
:class: tip, dropdown
Add a constraint that _evaluates_ the expression (in Python) and compares it against the `bc` result.
```python
where eval(str(<input>)) == int(<output>)
```
:::

If we actually do this, we will find that there are a few differences between the way that Python and `bc` interpret expressions:

```shell
$ fandango talk -f bc.fan -n 1 -c 'eval(str(<input>)) == int(<output>)' bc
```

```{code-cell}
:tags: ["remove-input"]
!fandango talk -f bc.fan -n 1 --population-size 1 -c 'eval(str(<input>)) == int(<output>)' bc
```

To ensure complete testing, we need to

* avoid `+` and `-` prefixes; these are not understood by `bc`;
* avoid leading zeros in numbers; these are not permitted in Python;
* allow small differences between floating point numbers, or restrict ourselves to integer operations.

Right now, we leave this as an exercise to the reader :-)



## Testing Strategies

If you find that checking results is complicated, welcome to the world of testing!
Specifically, you have just encountered the _oracle problem_ - the effort in specifying what a correct result should be.
While Fandango makes it easy to _produce_ inputs and to _decompose_ outputs, the burden of specification is still on you.

Here are some established techniques to ease the oracle problem:

Compare against a different implementation.
: By using Python `eval()`, above, we already make our lives much easier. However, we could also compare against, say, a different `bc` implementation. This is called _differential testing_.

Compare against a different version.
: After having made a change to a program, we can check it against an older version to make sure there are no unexpected changes in behavior. This is called _regression testing_.

Compare the result of equivalent inputs.
: Send two inputs to a program that should produce the same result and check for differences. In the case of `bc`, for instance, any term `<a> + <b>` should yield the same result as `<b> + <a>`. This is called _metamorphic testing_.

```{admonition} Under Construction
:class: attention
Future versions of this tutorial will further detail these strategies and how to integrate them into Fandango.
```


## Troubleshooting Interactions

Since interactions are always being sent to some party, and since the party outputs are being processed by Fandango, it may not always be easy to track which data is being sent, and where.

However, you can also make use of interaction specs in the regular `fuzz` and `parse` commands.
The special `--party=PARTY` option allows you to produce outputs or parse inputs for just one given party `PARTY` in the interaction.
The effect of `--party` is that it _excludes_ all other parties from the interaction, allowing to produce or parse strings for just one party.

As an example, consider again our [`bc.fan`](bc.fan) example:

```{code-cell}
:tags: ["remove-input"]
!cat bc.fan
```

This is the effect of `--party=In`.
See how the `Out:` part of the interaction has been excluded, also excluding `<output>` from production:

```{margin}
These are actually produced using [`fandango convert`](sec:fan2fan) with the `--party` option.
```

```{code-cell}
:tags: ["remove-input"]
!fandango convert --party=In bc.fan
```

This is the effect of `--party=Out`, excluding the `In` part, and consequently, `<input>`:

```{code-cell}
:tags: ["remove-input"]
!fandango convert --party=Out bc.fan
```

Typically, you provide such a `--party` option directly as part of some `fuzz` or `parse` command.
To see what typical inputs to `bc` look like, use:

```{margin}
The `--format=value` option makes the strings readable.
```

```shell
$ fandango fuzz -f bc.fan --party=In -n 10 --format=value
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f bc.fan --party=In -n 10 --format=value
```

Conversely, to see what typical outputs from `bc` would be expected, use:

```shell
$ fandango fuzz -f bc.fan --party=Out -n 10 --format=value
```

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f bc.fan --party=Out -n 10 --format=value
```
