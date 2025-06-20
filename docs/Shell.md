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

(sec:shell)=
# The Fandango Shell

Sometimes, you may find cumbersome to invoke Fandango from the command line again and again. This is especially true when

* You want to explore the effects of different constraints.
* You want to explore the effects of different algorithm settings.

This is why Fandango offers a _shell_, in which

* you can enter commands directly at a Fandango prompt
* you can set and edit parameters _once_ for future commands
* settings are preserved during your session
* your command history is preserved across sessions.


## Invoking the Fandango Shell

Invoking the Fandango shell is easy.
Just invoke Fandango without a command:

```shell
$ fandango
```

and you will be greeted by the Fandango prompt

```
(fandango)
```



## Invoking Commands

At the `(fandango)` prompt, you can enter the same commands you already know from the command line, such as

```
(fandango) fuzz -f persons.fan -n 10
```

```{tip}
Use TAB to complete commands, options, and file names.
```

and you will get the same results:

```{code-cell}
:tags: ["remove-input"]
!fandango fuzz -f persons.fan -n 10
assert _exit_code == 0
```

There is an important advantage though: You can set (and edit) a _common environment_ for all commands.


## Setting a Common Environment

The `set` command (available only in the Fandango shell) allows you to specify resources and settings that are then applied to all later commands (notably, `fuzz`).

You can, for instance, specify a `.fan` file with

```
(fandango) set -f persons.fan -n 10
```

```{note}
A big advantage of the `set` command is that the `.fan` file is read only _once_,
and then available for all later commands.
```

After options for resources and settings are set, you can omit them from later `fuzz` commands:

```
(fandango) fuzz
```

```{note}
If you give `fuzz` additional options, these temporarily _override_ the settings given with `set` earlier.
As an exception, _constraints_ (`-c`) are _added_ to those already set.
```

The options for the `set` command are roughly the same as for the `fuzz` command and include

* `.fan` files (`set -f FILE`)
* constraints (`set -c CONSTRAINT`)
* algorithm settings (`set --mutation-rate=0.2`)

To get a full list of options, try `help set`.

```{note}
Some command-specific options like `-o` or `-d` (controlling the output of the `fuzz` command)
are not available for setting with `set`.
```


## Retrieving Settings

To retrieve the current settings, simply enter `set`.
This will list:

* the grammar and constraints of the current `.fan` file
* as well as any constraints or settings you have made

Here is an example:
```
(fandango) set -N 10
(fandango) set
<start> ::= <person_name> ',' <age>
<person_name> ::= <first_name> ' ' <last_name>
<first_name> ::= <name>
<last_name> ::= <name>
<name> ::= <ascii_uppercase_letter> <ascii_lowercase_letter>+
<age> ::= <digit>+
--max-generations=10
```

## Resetting Settings

To reset all settings to default values, use the `reset` command:

```
(fandango) reset
```

This will

* clear all constraints defined with `set`
* reset all algorithm settings to their default value.

The current `.fan` file stays unchanged.

```{note}
Loading a new `.fan` file also clears all `set` constraints.
```


## Quotes and Escapes

The Fandango shell uses the same quoting conventions as a POSIX system shell.
For instance, to set a constraint, place it in quotes:

```
(fandango) set -c 'int(<age>) < 30'
```

You can also escape individual characters with backslashes:

```
(fandango) set -c int(<age>)\ <\ 30
```


## Editing Commands

The Fandango shell uses the GNU readline library.
Therefore, you can

* Use cursor keys _left_ and _right_ to edit commands
* Use cursor keys _up_ and _down_ to scroll through history
* Use the _TAB_ key to expand command names, options, and arguments.

The command history is saved in `~/.fandango_history`.


## Invoking Commands from the Shell

In the Fandango shell, you can invoke _system commands_ by prefixing them with `!`:

```
(fandango) !ls
LICENSE.md		docs			requirements.txt
Makefile		language		src
README.md		pyproject.toml		tests
```

```{tip}
Use TAB to complete file names.
```

You can also invoke and evaluate _Python commands_ by prefixing them with `/`:

```python
(fandango) /import random
(fandango) /random.randint(10, 20)
11
```

If the command you enter has a value, the value is automatically printed.

```{note}
Invoking system and Python commands is only available when the input is a terminal.
```


## Changing the Current Directory

To change the current directory, Fandango provides a built-in `cd` command:

:::{margin}
The alternative `!cd` does not work, as this changes the directory of the invoked shell.
:::

```
(fandango) cd docs/
```

Without arguments, `cd` switches to the home directory.

```{important}
This is different from Windows, where `cd` reports the current directory.
```


## Getting Shell Commands from a File

Instead of entering commands by keyboard, one can also have Fandango read in commands from a file or another command.
This is done by redirecting the `fandango` standard input.
To have Fandango read and execute commands from, say, `commands.txt`, use

```
$ fandango < commands.txt
```

Fandango can also process the commands issued from another program:

```
$ echo 'fuzz -n 10 -f persons.fan' | fandango
```

```{code-cell}
:tags: ["remove-input"]
!echo 'fuzz -n 10 -f persons.fan' | fandango
```

```{tip}
The input file can contain blank lines as well as comments prefixed with `#`.
```

```{note}
System commands (`!`) and Python commands (`/`) are not available when reading from a file.
```


## Exiting the Fandango Shell

To exit the Fandango shell and return to the system command line, enter the command `exit`:

```
(fandango) exit
$
```

Entering an EOF (end-of-file) character, typically `Ctrl-D`, will also exit the shell.

```
(fandango) ^D
$
```

In the next section, we'll talk about [custom generators](sec:generators).
