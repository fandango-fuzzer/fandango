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

(sec:fuzzing)=
# Fuzzing with Fandango

## Creating a Name Database

Let us now come up with an input that is slightly more complex.
We want to create a set of inputs with _names of persons_ and their respective _age_.
These two values would be _comma-separated_, such that typical inputs would look like this:

```
Alice Doe,27
John Smith,45
...
```

This makes the overall format of our input look like this:

```
<start> ::= <person_name> "," <age>
```

with `<age>` again being a sequence of digits, and a `<person>`'s name being defined as

```
<person_name> ::= <first_name> " " <last_name>
```

where both first and last name would be a sequence of letters - first, an uppercase letter, and then a sequence of lowercase letters.
The full definition looks like this:

:::{margin}
In Fandango specs, symbol names are formed like identifiers in Python - that is, they consist of letters, underscores, and digits.
:::

:::{margin}
Use [regular expressions](sec:regexes) to specifying character ranges.
:::

```{code-cell}
:tags: ["remove-input"]
!cat persons.fan
```

The symbols `<ascii_uppercase_letter>`, `<ascii_lowercase_letter>`, and `<digits>` are predefined in the [](sec:stdlib); they are defined exactly as would be expected.

Create or download a file [`persons.fan`](persons.fan) and run Fandango on it:

```shell
$ fandango fuzz -f persons.fan -n 10
```

Your output will look like this:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10 --validate
assert _exit_code == 0
```

Such random names are a typical result of _fuzzing_ – that is, testing with randomly generated values.
How do we get these into a program under test?


## Feeding Inputs Into Programs

So far, we have had Fandango simply _output_ the strings it generates.
This is nice for understanding and debugging, but not necessarily useful for processing these inputs further.
Fandango provides a number of means to help you process its output.

## Feed Inputs into a Single file

Fandango has a `-o` option that directs its output into a single file.
To store the generated strings in a file named `persons.txt`, use `-o persons.txt`:

```shell
$ fandango fuzz -f persons.fan -n 10 -o persons.txt
```

By default, the generated strings are separated by newlines.
With the `-s` option, you can define an alternate separator.
To have the outputs generated separated by `:`, for instance, use

```shell
$ fandango fuzz -f persons.fan -n 10 -o persons.txt -s ':'
```

## Feed Inputs into Individual Files

With the `-d` option, Fandango can store its strings into individual files in the directory given after `-d`.
They can then be picked up for post-processing.
To store all outputs in a directory named `persons`, for instance, use `-d persons`:

```shell
$ fandango fuzz -f persons.fan -n 10 -d persons
```

Fandango will create the directory and store the inputs as `Fandango-0001.txt`, `Fandango-0002.txt`, etc.

```{note}
If the directory is already present, Fandango will use that directory.
```

```{caution}
Fandango will overwrite files `Fandango-0001.txt`, `Fandango-0002.txt`, etc., but leave other files in the directory unchanged.
```

If you want a different file extension (for instance, because `.txt` is not suitable), Fandango provides a `--filename-extension` option to set a different one.


(sec:invoke-targets)=
## Invoking Programs Directly

You can have Fandango invoke _programs directly_, and have Fandango feed them the generated inputs.
The programs are specified as arguments on the command line.

There are three ways to pass the input into programs, on the command line, via standard input, and in-process to a shared object with a libFuzzer style harness.

Refer to [this example](https://github.com/fandango-fuzzer/fandango/tree/main/evaluation/experiments/libfuzzer-harness) for further details on how a harness can be compiled to interface with each mode.

### Passing Inputs on the Command Line

When Fandango invokes programs, you can pass input as a file name as last argument on the program's command line.
This is the default, and can also be obtained with the `--input-method=filename` option.

For instance, to test the `wc` program with its own `-c` option and the inputs Fandango generates, use

```shell
$ fandango fuzz -f persons.fan -n 10 wc -c
```

The `wc` program is then invoked as `wc -c FILE_1`, `wc -c FILE_2`, etc., where each `FILE` contains an individual input from Fandango.


### Passing Inputs via Standard Input

As an alternative, Fandango can pass inputs via standard input.
For this, use the `--input-method=stdin` option.

For instance, to test the `cat` program with its own `-n` option and the inputs Fandango generates, use

```shell
$ fandango fuzz -f persons.fan -n 10 --input-method=stdin cat -n
```

The `cat` program is then invoked repeatedly, each time passing a new Fandango-generated input as its standard input.

(sec:libfuzzer)=
### Calling a libFuzzer style harness directly

Fandango further supports calling a libFuzzer style harness directly. If you are able to compile your binary to a shared object (`.so` on Linux or `.dylib` on macOS), Fandango can load the binary and directly call the function. This requires some extra work initially but removes the need to start a new process for each input evaluation, thus improving performance significantly. Fandango will exit on the first crashing input. `--input-method=libfuzzer` is only supported in combination with `--file-mode=binary`, since libFuzzer style harnesses expect binary data.

Fandango is invoked as follows:

```
$ fandango fuzz -f persons.fan -n 10 --input-method=libfuzzer --file-mode=binary ./harness.{so,dylib}
```

```{note}
The libFuzzer interface is untested on Windows so far due to a lack of hardware. If you would like to test it, try un-skipping `test_output_with_libfuzzer_harness` in `test_cli.py`. You may need to adjust how the C file is compiled.
```

## Executable `.fan` files


On a Unix system, you can turn a `.fan` file into an _executable file_ by placing a line

```
#!/usr/bin/env -S fandango fuzz -f
```

at the top.

If you set its "executable" flag with `chmod +x FILE`, you can then directly execute the `.fan` file as a command as if it were prefixed by `fandango fuzz -f`.

As an example, let us create a file [`fuzz-persons.fan`](fuzz-persons.fan):

```shell
$ (echo '#!/usr/bin/env -S fandango fuzz -f'; cat persons.fan) > fuzz-persons.fan
$ chmod +x fuzz-persons.fan
```

```{code-cell}
:tags: ["remove-input"]
! (echo '#!/usr/bin/env -S fandango fuzz -f'; cat persons.fan) > fuzz-persons.fan
! chmod +x fuzz-persons.fan
```

You can now invoke the file, even with extra arguments:

```shell
$ ./fuzz-persons.fan -n 1
```

```{code-cell}
:tags: ["remove-input"]
! ./fuzz-persons.fan -n 1
```

:::{tip}
The `env` command varies greatly across Unix flavors and versions.
If the above does not work on your system, try skipping the `-S` option, such that the first line reads:
```
#!/usr/bin/env fandango fuzz -f
```
:::

## Running Fuzzing Campaigns

So far, we have only produced a limited number of outputs. This can be done in two ways: By limiting the number of generations for the evaluation or by capping the number of solutions:

```bash
$ fandango fuzz -f persons.fan -n 10 # to limit the number of solutions
$ fandango fuzz -f persons.fan -N 10 # to limit the number of generations
```

To run fuzzing continuously, consider specifying `--infinite` to keep Fandango producing inputs indefinitely. You likely want to combine this with one of the configurations where Fandango [executes your target directly](sec:invoke-targets) like so:

```bash
$ fandango fuzz -f persons.fan --infinite --input-method=libfuzzer --file-mode=binary ./harness.{so,dylib}
```
