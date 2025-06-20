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

(sec:invoking)=
# Invoking Fandango

## Running Fandango on our Example Spec

To run Fandango on [our "digits" example](sec:first-spec),
create or download a file [digits.fan](digits.fan) with the "digits" grammar in the current folder.

:::{margin}
Fandango specs have a `.fan` extension.
:::

Then, you can run Fandango on it to create inputs.
The command we need is called `fandango fuzz`, and it takes two important parameters:

* `-f` followed by the `.fan` file – for us, that is `digits.fan`;
* `-n` followed by the number of inputs we want to have – say, 10.

This is how we invoke Fandango:

```shell
$ fandango fuzz -f digits.fan -n 10
```

And this is what we get:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f digits.fan -n 10 --validate
assert _exit_code == 0
```

Success! We have created 10 random sequences of digits.

```{warning}
Be aware that `.fan` files can contain Python code that is _executed when being loaded_. This code can execute arbitrary commands.
```

```{caution}
Only load `.fan` files you trust.
```

## More Commands and Options

Besides `fandango fuzz`, Fandango supports more commands, and besides `-f` and `-n`, Fandango supports way more options.
To find out which commands Fandango supports, try

```shell
$ fandango --help
```

```{important}
Fandango commands not detailed in this documentation are _experimental_ – do not rely on them.
```

To find out which option a particular command supports, invoke the command with `--help`.
For instance, these are all the options supported by `fandango fuzz`:

```shell
$ fandango fuzz --help
```

```{code-cell}
:tags: ["remove-input", "scroll-output"]
!fandango fuzz --help
assert _exit_code == 0
```

Some of these options are very useful, such as `-o` and `-d`, which redirect the inputs generated towards individual files.
You can also specify a _command_ to be executed with the inputs Fandango generated.

We will go through these commands and options in due time.
For now, let us get back to our specifications and actually [_fuzz with Fandango_](sec:fuzzing).