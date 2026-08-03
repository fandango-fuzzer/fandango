<!--
Thanks for contributing to Fandango!

The full guide is at https://fandango-fuzzer.github.io/Contributing.html
Nothing below is mandatory, but a reviewer who can see what changed and why
will get to your pull request faster.
-->

## What does this change?

<!-- A short description. If it fixes an issue, write "Fixes #123" so GitHub
     closes it on merge. -->

## Why?

<!-- The reasoning matters more than the diff, which already shows the what.
     If there was a design choice with a real alternative, mention it. -->

## How was it tested?

<!-- New tests, existing tests, manual steps. If behaviour changed, a test that
     fails before this change and passes after is the most convincing thing you
     can point at. -->

## Checklist

- [ ] The change does one thing
- [ ] Tests cover any changed behaviour
- [ ] Documentation updated, if this changes something a user can see
- [ ] `pre-commit` passes (`pre-commit run --all-files`)
- [ ] `make tests` passes locally (note the plural)
- [ ] `make lock` was run, if `pyproject.toml` dependencies changed
- [ ] I have read every line of this change and can explain it in review

<!--
That last box is the one that matters most. Use whatever tools you like,
including AI, but the code is yours: you should be able to say why it is
written this way and why it is correct. See "Using AI assistance" in
CONTRIBUTING.md.
-->

<!--
Working from an issue? Please make sure it was assigned to you first. If it was
already assigned to someone else, we will most likely close this in favour of
their work, which is a waste of your time.
-->


<!--
CI checks formatting and types across the WHOLE repository, not just src/, so a
stray file elsewhere can turn the build red. Running pre-commit locally catches
almost all of it.
-->
