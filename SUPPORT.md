# Getting Help with Fandango

## Start with the documentation

The [Fandango book](https://fandango-fuzzer.github.io/) covers most questions:

- [Installing Fandango](https://fandango-fuzzer.github.io/Installing.html)
- [Your first specification](https://fandango-fuzzer.github.io/FirstSpec.html)
- [Grammars and constraints](https://fandango-fuzzer.github.io/Constraints.html)
- [Testing protocols](https://fandango-fuzzer.github.io/Protocols.html)
- [Frequently asked questions](https://fandango-fuzzer.github.io/FAQ.html)

If you are new, the [hands-on
tutorial](https://fandango-fuzzer.github.io/HandsOn.html) builds one running
example from random bytes up to a stateful protocol conversation.

## Asking a question

If the documentation does not answer it, open an
[issue](https://github.com/fandango-fuzzer/fandango/issues). There is no
separate forum, so questions are welcome on the tracker.

You will get a better answer faster if you include:

- the smallest `.fan` spec that shows what you are asking about,
- the exact command you ran and its full output,
- what you expected to happen instead,
- the output of `fandango --version`, plus your Python version and OS.

## Reporting a bug

Use the [bug report
template](https://github.com/fandango-fuzzer/fandango/issues/new/choose). See
[CONTRIBUTING.md](CONTRIBUTING.md) for what makes a report easy to act on.

## Reporting a security vulnerability

Please do **not** open a public issue. Report it privately through GitHub's
[security advisory form](https://github.com/fandango-fuzzer/fandango/security/advisories/new), or from the repository's Security tab. See
[SECURITY.md](SECURITY.md).

## Contributing a fix

See [CONTRIBUTING.md](CONTRIBUTING.md). Note that we ask you to comment on an
issue and be assigned before starting work on it.

## What we cannot help with

We cannot debug your program under test for you, or write your specification
from scratch. If your specification is not producing what you expect, reduce it
to the smallest case that still shows the problem and ask about that; that is
usually enough for us to see what is going on, and often enough for you to spot
it yourself.
