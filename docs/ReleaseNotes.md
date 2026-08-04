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

(sec:release-notes)=
# Release Notes

This document lists major changes across releases.

```{versionadded} 1.2 (August 2026)
* Grammars gained a **permutation operator**: `[[ <a> <b> <c> ]]` produces and parses the enclosed symbols in any order. It works for protocol messages too, so a spec can state that two packets may arrive in either order.
* **Timers for protocol testing.** A spec can now start and cancel timers and react to them expiring, so interactions that hinge on timeouts can be tested.
* Two new ways to stop a fuzzing run once it has done its job:
   * `--stop-criterion` takes a Python lambda that is evaluated on every new solution, for instance `--stop-criterion 'lambda t: t.to_string().startswith("abc")'`.
   * `--stop-after-seconds` stops at the start of the first generation after the given number of seconds.
* Experimental support for [guidance by code coverage](sec:code-coverage). Against a program compiled with [`fcc`](https://github.com/fandango-fuzzer/fcc), `fandango fuzz --fcc` steers input generation towards code that has not been reached yet.
* Submodules under `fandango.experimental.*` are now marked as experimental: they can change without notice, and importing one emits a warning. `--enable-experimental-module MODULE` opts you in to a module and silences its warning.
* Internal caches are now bounded, so long runs no longer grow without limit. Set their size with the `FANDANGO_CACHE_SIZE` environment variable.
* `--format=1` prints the constant `1` for every output, which is useful for testing.
* New `DerivationTree.find_subtrees()`, which also accepts a symbol name as a plain string. It replaces `find_all_trees()`.
* Further improved [protocol fuzzing](sec:protocols): a dedicated protocol algorithm, $k$-path coverage tracking of the interactions produced so far, and a packet selector that plans which message to send next.
* We have added new [PNG](sec:png) and [MP3](sec:mp3) case studies.
* New [hands-on tutorial](sec:handson), which builds one protocol from random bytes up to a stateful conversation.
* New [style guide](sec:style) for writing specs that are reusable, extensible, and efficient.
* Lots of minor bug fixes.
* [development] Python 3.14 is now supported, and tested in CI alongside 3.11, 3.12, and 3.13.
* [development] Fandango now builds with `scikit-build-core` alone, and `setup.py` is gone. Set `FANDANGO_SKIP_CPP_PARSER=1` to skip the C++ parser, or `FANDANGO_REQUIRE_BINARY_BUILD=1` to insist on it.
* [development] We now ship a `pylock.toml` next to `uv.lock`, so tools other than `uv` can consume our dependency set.
* [development] Ruff replaces black for formatting and linting.
* [development] The project now has a [contribution guide](sec:contributing), a code of conduct, a support policy, a security policy, issue and pull request templates, and a `CITATION.cff`.
```

```{versionchanged} 1.2
* Fandango now requires **Python 3.11 or later**. Python 3.10 is no longer supported.
* `DerivationTree.find_all_trees()` is deprecated. Use `find_subtrees()` instead.
```

```{versionadded} 1.1 (February 2026)
* Much enhanced [protocol fuzzing](sec:protocols):
   * Protocol fuzzing is now out of beta.
   * `fandango talk` now keeps on producing diverse interactions, systematically covering states and messages until stopped or 100% coverage is reached.
   * Detailed documentation with [FTP](sec:ftp) and [DNS](sec:dns) case studies.
   * `fandango convert` can now produce [state diagrams from grammars](sec:extracting-state-diagrams).
* We have added a new [GIF](sec:gif) case study.
* You can now [download the **documentation** as a PDF](_static/fandango.pdf) from the upper-right download icon.
* Lots of minor bug fixes.
* [development] Major internal refactorings and code quality improvements.
* [development] Added support for the `uv` package manager, including appropriate lock files to ensure compatible and fixed dependency versions
```

```{versionadded} 1.0 (June 2025)
* New command `fandango talk` for [checking outputs](sec:outputs) and [testing protocols](sec:protocols) (beta).
* Much faster parser for `.fan` files, using C++ code.
* Support for [regular expressions](sec:regexes) for producing and parsing.
* Support for [soft constraints and optimization](sec:soft-constraints) (`maximizing` / `minimizing`).
* Using `*`/`**` expressions for Python-style [quantifiers](sec:quantifiers) is now operational.
* f-strings in Python code are now supported.
* Support for [`libfuzzer` harnesses](sec:libfuzzer).
* New command `fandango convert` for [converting ANTLR and other input specifications](sec:converters).
* New command `fandango clear-cache` for [clearing the parser cache](sec:including).
* Improved bit parser.
* Lots of minor and major improvements and bug fixes across the board.
```

```{versionchanged} 1.0
* We now apply Python [end-of-line rules to grammar parsing](sec:language). End continuation lines with `\` or use parentheses.
* Fuzzing by default is now "infinite", producing results until stopped. Specify `-n N` to obtain `N` outputs.
```

```{versionadded} 0.8 (April 2025)
* First public beta release.
* `fandango fuzz` and `fandango parse` commands.
```
