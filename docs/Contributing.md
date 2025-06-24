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

(sec:contributing)=
# Contributing to Fandango

Welcome!
Fandango is a community project that aims to work for a wide
range of developers.
If you're trying out Fandango, your experience and what you can contribute are
important to the project's success.

(sec:code-of-conduct)=
## Code of Conduct

Everyone participating in Fandango, and in particular in our
issue tracker, pull requests, and chat, is expected to treat
other people with respect and more generally to follow the guidelines
articulated in the [Python Community Code of Conduct](https://www.python.org/psf/codeofconduct/).

(sec:getting-started-with-development)=
## Getting Started with Development

### Step 1: Fork the Fandango repository

Within GitHub, navigate to the [Fandango GitHub repository](https://github.com/fandango-fuzzer/fandango) and fork the repository.


### Step 2: Clone the Fandango repository and enter into it

```shell
$ git clone https://github.com/fandango-fuzzer/fandango.git
```

```shell
$ cd fandango
```

### Step 3: Create, then activate a virtual environment

```shell
$ python3 -m venv venv
```

```shell
$ source venv/bin/activate
```

For Windows, use
```shell
$ python -m venv venv
```

```shell
$ . venv/Scripts/activate
```

For more details, see https://docs.python.org/3/library/venv.html#creating-virtual-environments


### Step 4: Install development tools

Install `antlr` and other system-level tools:

```shell
$ make system-dev-tools
```

(sec:pip-install)=
### Step 5: Install Fandango

Install your local copy of Fandango:

```shell
$ python -m pip install -e .
```

To install additional dependencies for unit tests, code checks, running the evaluation, and building the Fandango book, install Fandango like this (or with the subsection of dependencies you need):

```shell
$ python -m pip install -e ".[test,development,evaluation,book]"
```

If you don't need the (much faster) C++ parser, build Fandango without:

```shell
$ FANDANGO_SKIP_CPP_PARSER=1 python -m pip install -e .
```

Reset the shell PATH cache (not necessary on Windows):

```shell
$ hash -r
```

That's it! You just have installed your personal copy of Fandango.
You can invoke it as `fandango` and can alter its code as you like.

(sec:running-tests)=
## Running Tests

Running the full test suite can take a while, and usually is not necessary when
preparing a pull request.
Once you file a pull request, the full test suite will run on GitHub.
You'll then be able to see any test failures, and make any necessary changes to
your pull request.

However, if you wish to do so, you can run the full test suite
like this:

```shell
$ make tests
```

or simply

```shell
$ pytest
```

To run tests in parallel, you can use [pytest-xdist](https://pytest-xdist.readthedocs.io/en/stable/) (installed with the `test` depenendencies):

```shell
$ pytest -n auto
```

### Pre-commit

Fandango provides a config file for `pre-commit`. To install it, run the following:

```shell
$ pip install pre-commit
$ pre-commit install
```

This will run code formatting and type checking before every commit.

```{warning}
The [tests](sec:running-tests)= aren't run as part of pre-commit, because they take significant time to complete. Run them manually.
```

(sec:first-time-contributors)=
## First Time Contributors

If you're looking for things to help with, browse our [issue tracker](https://github.com/fandango-fuzzer/fandango/issues)!

You do not need to ask for permission to work on any of these issues.
Just fix the issue yourself, [try to add a unit test](sec:running-tests) and open a pull request.

To get help fixing a specific issue, it's often best to comment on the issue itself.
You're much more likely to get help if you provide details about what you've tried and where you've looked (maintainers tend to help those who help themselves).


(sec:contributing-code)=
## Contributing Code

Even more excellent than a good bug report is a fix for a bug, or the implementation of a much-needed new feature.
We'd love to have your contributions.

We use the usual GitHub pull-request flow, which may be familiar to you if you've contributed to other projects on GitHub.
For the mechanics, see [GitHub's own documentation](https://help.github.com/articles/using-pull-requests/).

Anyone interested in Fandango may review your code.
One of the Fandango core developers will merge your pull request when they think it's ready.

If your change will be a significant amount of work to write, we highly recommend starting by opening an issue laying out
what you want to do.
That lets a conversation happen early in case other contributors disagree with what you'd like to do or have ideas that will help you do it.

The best pull requests are focused, clearly describe what they're for and why they're correct, and contain tests for whatever changes they make to the code's behavior.
As a bonus these are easiest for someone to review, which helps your pull request get merged quickly!
Standard advice about good pull requests for open-source projects applies.


### Changing Parser Files

If your contribution involves changing the ANTLR `.g4` parser files,
you need to _regenerate_ and _recompile_ the parser code.
For this, you need a C++ compiler such as `clang`.

#### Step 1: Generate the parser code

To (re)generate the parser code, use

```shell
$ make parser
```

#### Step 2: Compile the parser code

The `pip` command takes care of (re)compiling the parser code.
Simply [reinstall Fandango](sec:pip-install).

```{note}
If compiling the C++ code for parsing fails,
Fandango uses (slower) Python code instead.
```


### Contributing to Documentation

If you want to contribute to this very tutorial and reference, be sure to preview your changes.
Use

```shell
$ make html
```

to create a HTML version of the documentation in `docs/_build/html`.


## Attributions

This guide was forked from the [mypy contribution guide](https://github.com/python/mypy/blob/master/CONTRIBUTING.md), which is licensed under the terms of the MIT license.
