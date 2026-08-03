# Contributing to Fandango

Thanks for wanting to help. Fandango is a community project, and your
experience using it is as valuable a contribution as code.

**The full guide lives in the Fandango book:
<https://fandango-fuzzer.github.io/Contributing.html>** (source:
[`docs/Contributing.md`](docs/Contributing.md)). This file is the short version.

## Before you start

By participating you agree to follow our
[Code of Conduct](CODE_OF_CONDUCT.md).

Found a **security vulnerability**? Do not open a public issue. Report it
privately through GitHub's [security advisory form](https://github.com/fandango-fuzzer/fandango/security/advisories/new), or from the
repository's Security tab. See [`SECURITY.md`](SECURITY.md).

## Reporting a bug

Open an [issue](https://github.com/fandango-fuzzer/fandango/issues/new/choose)
and include:

- the smallest `.fan` spec that still shows the problem, and the exact command
  you ran,
- what you expected, and what happened instead, with the full error output,
- the output of `fandango --version`, plus your Python version and OS.

## New to Fandango's specification language?

Start with the [hands-on tutorial](https://fandango-fuzzer.github.io/HandsOn.html).
It builds one small protocol from random bytes up to a stateful conversation, so
by the end you have written the grammars, constraints, and feedback that most
issues are about. It takes an afternoon and saves a round of review later.

## Picking up an issue

**If an issue is already assigned, please leave it** and pick another one.
Someone is working on it.

**If it is unassigned, comment on it before you start** and wait to be assigned.
It lets us tell you if the issue is thornier than it looks, or already being
handled elsewhere, which is much cheaper to hear before you write the code.

If you later cannot finish it, say so and unassign yourself. That is fine.

## Using AI assistance

We are not against AI tools, we use them too, and we do not ask you to declare
them. But **you own the code you submit**: you should be able to explain why it
is written that way, why it is correct, and what you rejected. If a reviewer
asks about a decision and the honest answer is "the model wrote it", the pull
request is not ready.

The problem is not AI, it is moving your work onto the maintainers. A patch
generated from an issue and pushed unread costs us more time than the issue
would have. Those pull requests get inspected closely, and if the work has been
handed to us rather than done, we close them.

Read every line, run it, and be ready to defend it in review. Do that and we do
not care how you got there.

## Setting up

Fandango needs **Python 3.11 or later**. With
[uv](https://docs.astral.sh/uv/) (recommended, this is what our CI uses):

```shell
git clone https://github.com/YOUR-USERNAME/fandango.git
cd fandango
make system-dev-tools          # ANTLR and a C++ compiler
uv sync --all-extras --locked  # exactly the dependency set CI resolves
```

If the C++ parser fails to build, skip it and use the pure-Python fallback:

```shell
FANDANGO_SKIP_CPP_PARSER=1 uv sync --all-extras --locked
```

Prefer plain `pip`? See
[the full guide](https://fandango-fuzzer.github.io/Contributing.html).

## Before you open a pull request

```shell
pre-commit install   # once; then it runs on every commit
make tests           # note the plural: `make test` does nothing
```

CI checks formatting and types across the **whole repository**, not just `src`,
so a stray file elsewhere can fail the build. `pre-commit` catches almost all
of it locally.

If you change dependencies in `pyproject.toml`, regenerate both lockfiles with
`make lock`, or CI will fail.

## What makes a pull request easy to merge

- It does one thing.
- It explains **why**, not just what; the diff already shows the what.
- It has a test for any behaviour it changes.
- It updates the docs if it changes something a user can see.
- It is green in CI.

When a review asks for changes, push more commits rather than force-pushing a
rewritten branch, so the review comments stay anchored. Pull requests are merged
with a merge commit, so your branch's commits stay in the project history.

## Licensing

Fandango is released under the [European Union Public Licence v1.2](LICENSE.md).
By contributing you agree your contribution is licensed under those same terms,
and confirm you have the right to submit it.
