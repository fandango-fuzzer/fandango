(sec:contributing)=
# Contributing to Fandango

Welcome! Fandango is a community project that aims to work for a wide range of
developers. If you are trying out Fandango, your experience and what you can
contribute are important to the project's success.

This page covers everything from reporting a bug to getting a pull request
merged. If you only want to *use* Fandango, see [Installing](sec:installing)
instead.

(sec:code-of-conduct)=
## Code of Conduct

Everyone participating in Fandango, and in particular in our issue tracker,
pull requests, and chat, is expected to treat other people with respect and to
follow the [Python Community Code of
Conduct](https://www.python.org/psf/codeofconduct/).

If you experience or witness unacceptable behaviour, report it to
[fandango-fuzzer@protonmail.com](mailto:fandango-fuzzer@protonmail.com). Reports
are handled confidentially. See
[`CODE_OF_CONDUCT.md`](https://github.com/fandango-fuzzer/fandango/blob/main/CODE_OF_CONDUCT.md)
in the repository root.

(sec:ways-to-contribute)=
## Ways to Contribute

You do not have to write code to help.

* **Report a bug.** See [reporting bugs](sec:reporting-bugs) below.
* **Request a feature**, or tell us where Fandango was confusing to use.
* **Improve the documentation.** This book is part of the repository, and doc
  fixes are among the most useful contributions we get.
* **Fix an issue.** Browse the [issue
  tracker](https://github.com/fandango-fuzzer/fandango/issues) and pick
  something up.

For security vulnerabilities, do **not** open a public issue. Report them
privately through GitHub's [security advisory form](https://github.com/fandango-fuzzer/fandango/security/advisories/new), reachable from the
repository's Security tab, so the report, the fix, and the advisory stay in one
private thread. See
[`SECURITY.md`](https://github.com/fandango-fuzzer/fandango/blob/main/SECURITY.md).

(sec:reporting-bugs)=
## Reporting Bugs

A good report is one someone else can reproduce. Please include:

* **What you did**: the `.fan` spec (reduced to the smallest one that still
  shows the problem) and the exact command you ran.
* **What you expected** to happen, and **what happened instead**, including the
  full error message and traceback.
* **Your environment**: the output of `fandango --version`, your Python version,
  and your operating system.

A spec that is a hundred lines long makes a bug much harder to act on than one
that is five. Time spent reducing the input is usually time saved overall.

(sec:first-time-contributors)=
## First Time Contributors

If you are not yet fluent in Fandango's specification language, the fastest way
in is the [hands-on tutorial](sec:handson). It builds one small protocol from
random bytes up to a stateful conversation, and by the end you will have written
the grammars, constraints, and feedback that most issues are about. It takes an
afternoon and it is the same material we would otherwise explain in review.

If you are looking for something to work on, browse the [issue
tracker](https://github.com/fandango-fuzzer/fandango/issues).

**Check whether the issue is assigned before you start.** If it already has an
assignee, someone is working on it, so please pick a different one. Duplicated
effort is wasted effort, and it is discouraging for whoever got there first.

**If it is unassigned, say so in the issue before you begin**, and wait to be
assigned. A short comment is enough. This is not bureaucracy: it lets us tell
you if the issue is more involved than it looks, if it is already being
addressed elsewhere, or if we have a view on the approach. All of that is much
cheaper to hear before you write the code than after.

Once the issue is yours, fix it, [add a test](sec:running-tests), and open a
pull request.

To get help with a specific issue, comment on the issue itself, and say what you
have already tried and where you have looked. If you find you cannot finish
something you claimed, just say so in the issue and unassign yourself. That is
completely fine and much better than an issue going quiet.

If your change is going to be a significant amount of work, open an issue first
describing what you intend to do. That way a conversation can happen early,
before you have written code that someone disagrees with.

(sec:getting-started-with-development)=
## Setting Up a Development Environment

Fandango requires **Python 3.11 or later**. Our CI tests against Python 3.11,
3.12, 3.13, and 3.14 on Linux, macOS, and Windows.

### Step 1: Fork and clone

You do not need push access to the Fandango repository, and you should not wait
for it. All your work happens on your own fork, and reaches us as a [pull
request across forks](sec:contributing-code).

Fork the [Fandango repository](https://github.com/fandango-fuzzer/fandango) on
GitHub, then clone your fork:

```shell
$ git clone https://github.com/YOUR-USERNAME/fandango.git
$ cd fandango
```

### Step 2: Install the system tools

Fandango's parser is generated with ANTLR and compiled with a C++ compiler.
Install both:

```shell
$ make system-dev-tools
```

```{note}
This installs system packages (via Homebrew, apt, or Chocolatey depending on
your platform), so it may ask for your password.
```

(sec:uv-install)=
### Step 3: Install Fandango with `uv`

We recommend [uv](https://docs.astral.sh/uv/). It creates the virtual
environment and installs the exact dependency set our CI uses, taken from
`uv.lock`:

```shell
$ uv sync --all-extras --locked
```

That is the whole setup. Run Fandango with `uv run fandango`, or activate the
environment it created:

```shell
$ source .venv/bin/activate
```

On Windows, use `.venv\Scripts\activate`.

```{tip}
Because `--locked` pins every dependency to the versions our CI resolved, this
is also the fastest way to rule out a dependency problem when something behaves
differently for you than for us.
```

(sec:pip-install)=
### Step 3, alternative: Install with `pip`

If you would rather not use `uv`, create a virtual environment and install
Fandango into it as an editable package:

```shell
$ python3 -m venv .venv
$ source .venv/bin/activate
$ python -m pip install -e ".[full]"
```

On Windows, create and activate the environment with:

```shell
$ python -m venv .venv
$ .venv\Scripts\activate
```

The `full` extra pulls in everything you need to develop: it is shorthand for
`book`, `development`, and `test`. To install a subset instead, name the ones
you want, for example `pip install -e ".[test]"`.

| Extra | Gives you |
|---|---|
| `test` | the unit test suite and its fixtures |
| `development` | Ruff, mypy, and the other code-quality tools |
| `book` | everything needed to build this documentation |
| `full` | all three of the above |

Reset your shell's command lookup afterwards, so `fandango` resolves to your
copy (not needed on Windows):

```shell
$ hash -r
```

### If the build fails

The C++ parser is the usual culprit, because it needs ANTLR and a working C++
toolchain. You can skip it entirely:

```shell
$ FANDANGO_SKIP_CPP_PARSER=1 uv sync --all-extras --locked
```

Fandango then falls back to the pure-Python parser. Everything still works and
parsing is slower, which is fine for most development.

```{note}
`make system-dev-tools` is what installs the toolchain the C++ parser needs. If
you skipped it in Step 2, that is the first thing to try.
```

That's it. You have installed your personal copy of Fandango, you can invoke it
as `fandango`, and you can change its code as you like.

(sec:running-tests)=
## Running Tests

Running the full suite takes a while and is usually not necessary while
preparing a pull request. Once you open one, the full suite runs on GitHub and
you can fix anything it catches.

To run it yourself:

```shell
$ make tests
```

or equivalently:

```shell
$ pytest
```

The suite runs in parallel by default via
[pytest-xdist](https://pytest-xdist.readthedocs.io/en/stable/). To run a single
test file while working on it:

```shell
$ pytest tests/test_some_file.py -x
```

```{warning}
`make test` (singular) is not the test target and does nothing. Use `make
tests`.
```

(sec:pre-commit)=
## Pre-commit

Fandango ships a `pre-commit` configuration that catches most of what CI checks,
before you push:

```shell
$ pip install pre-commit
$ pre-commit install
```

The hooks run Ruff formatting, Ruff linting, mypy (including `--strict` on
`src`), and the lockfile checks described below.

```{warning}
The [tests](sec:running-tests) are not part of pre-commit, because they take
too long. Run them yourself.
```

(sec:ci-checks)=
## What CI Checks

Every pull request runs the following. Knowing this list saves a round trip,
since these are the things that most often turn a pull request red:

| Check | Command | Scope |
|---|---|---|
| Formatting | `ruff format --check .` | the **whole repository**, not just `src` |
| Linting | `ruff check src tests evaluation scripts` | those four directories |
| Types | `mypy .` and `mypy --strict src` | the whole repository, then `src` strictly |
| Tests | `pytest` | Python 3.11 to 3.14, on Linux, macOS, and Windows |
| Docs | `make web` | the whole book must build |
| Lockfiles | `uv lock --check` and a `pylock.toml` diff | see below |

The formatting and type checks cover the entire repository, so a stray file
outside `src` can fail the build. Running `pre-commit` locally catches almost
all of it.

(sec:lockfiles)=
### Lockfiles

We keep both lockfiles current, for reproducible environments and for
compatibility with the wider Python ecosystem:

* `uv.lock` is generated by `uv` and is the source of truth for the dependency
  set. Update it with `uv lock`.
* `pylock.toml` is derived from `uv.lock` so that other tools can consume it.
  Update it with `uv export --output-file=pylock.toml --all-extras --locked`.

After changing dependencies in `pyproject.toml`, regenerate both:

```shell
$ make lock
```

Both pre-commit and CI check that these are in sync, so forgetting this step
fails the build.

(sec:ai-assistance)=
## Using AI Assistance

We are not against AI tools. Plenty of good contributions are written with a
model in the loop, and we use them ourselves.

Two things we ask.

**Tell us when you used one.** If a change was substantially written with AI
assistance, say so in the pull request. We cannot verify it and it will not
count against you. It tells a reviewer what kind of read the change needs, which
makes triage faster for everyone.

**Write the description yourself.** Generated pull request and issue
descriptions tend to be long and say little, which moves work onto the reader.
Writing it in your own words is also the quickest way to find out whether you
understand the change.

And one thing we require: **you own the code you submit**. You should be able to
say why the change is written the way it is, why it is correct, what
alternatives you rejected, and what happens at the edges. If a reviewer asks
about a decision and the honest answer would be "the model wrote it that way",
the pull request is not ready to open.

The problem we care about is not AI. It is **moving your work onto the
maintainers**. A patch produced by pasting an issue into a model and pushing the
result, without reading it, running it, or understanding it, costs us more time
than the issue would have. Reviewing that means reconstructing an intent that
was never formed in the first place, which is harder than writing the fix from
scratch. That is not a contribution, it is a transfer of effort.

Keep the diff minimal while you are at it. Models like to reformat, rename, and
"improve" code the change never needed to touch, and every unrelated hunk is
more for a reviewer to read and rule out.

So before you open a pull request, whatever tools you used to get there:

- Have you read every line you are about to submit, and do you understand what
  each one does and why it is there?
- Have you run it, and does your test actually fail without the change?
- Is the diff limited to what the change requires?

(sec:contributing-code)=
## Contributing Code

We use the usual GitHub pull request flow, from a fork:

1. **Fork** the [Fandango
   repository](https://github.com/fandango-fuzzer/fandango) on GitHub. This
   gives you your own copy, at `https://github.com/YOUR-USERNAME/fandango`.
2. **Clone your fork** and set it up as described in [Setting up a development
   environment](sec:getting-started-with-development).
3. **Commit your change on a branch** in your fork, and push that branch:

   ```shell
   $ git switch -c my-change
   $ git commit -am "Say what changed and why"
   $ git push -u origin my-change
   ```

4. **Open a pull request across forks**: from your branch on your fork, to
   `main` on `fandango-fuzzer/fandango`. GitHub offers this on your fork's page
   right after you push, and you can also open it from the [main
   repository](https://github.com/fandango-fuzzer/fandango/compare) by picking
   your fork and branch as the source.

Branches on the main repository itself are for the core developers, so this is
the route for everyone else, and it needs nothing from us to get started.

If any of this is unfamiliar, see [GitHub's
documentation](https://docs.github.com/en/pull-requests).

Anyone interested in Fandango may review your code, and one of the core
developers merges it when they think it is ready.

**What makes a pull request easy to merge:**

* It does **one thing**. A focused change is far easier to review than a large
  one, and reviewability is usually what decides how fast something lands.
* It says **what** it changes and **why**. The why matters more; the diff
  already shows the what.
* It comes with **tests** for any behaviour it changes. A regression test that
  fails before your fix and passes after is the most convincing thing you can
  include.
* It **updates the documentation** when it changes something a user can see.
* It is **green in CI**.

If a review asks for changes, push additional commits to the same branch rather
than force-pushing a rewritten history. That keeps the review comments anchored
to the code they refer to.

Pull requests are merged with a merge commit, so the commits on your branch stay
in the project history. They do not need to be perfect, but a reader six months
from now benefits from commit messages that say what changed and why.

(sec:contribution-licensing)=
### Licensing of Contributions

Fandango is released under the [European Union Public Licence v1.2](https://github.com/fandango-fuzzer/fandango/blob/main/LICENSE.md).
By contributing, you agree that your contribution is licensed under those same
terms, and you confirm that you have the right to submit it.

### Changing the Parser

If your contribution changes the ANTLR `.g4` files, you have to regenerate and
recompile the parser. This needs a C++ compiler such as `clang`.

Regenerate the parser code:

```shell
$ make parser
```

Then reinstall Fandango, which recompiles it: see [installing with
uv](sec:uv-install) or [with pip](sec:pip-install).

```{note}
If compiling the C++ parser fails, Fandango falls back to the slower Python
parser, so this is not a hard blocker for testing your change.
```

### Contributing to the Documentation

This book lives in `docs/` in the repository. Preview your changes before
opening a pull request:

```shell
$ make html
```

The result lands in `docs/_build/html`. Because CI builds the book on every
pull request, a broken directive or a dead cross-reference fails the build, so
it is worth checking locally.

```{tip}
The book executes many of its own code examples while building. If your change
touches an executed example, build the book to confirm the output is still what
the page claims.
```

## Attributions

This guide was originally forked from the [mypy contribution
guide](https://github.com/python/mypy/blob/master/CONTRIBUTING.md), which is
licensed under the terms of the MIT license.
