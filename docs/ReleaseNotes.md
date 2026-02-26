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

```{versionadded} 1.1 (February 2026)
* Much enhanced [protocol fuzzing](sec:protocols):
   * Protocol fuzzing is now out of beta.
   * `fandango talk` now keeps on producing diverse interactions, systematically covering states and messages until stopped or 100% coverage is reached.
   * Detailed documentation with [FTP](sec:ftp) and [DNS](sec:dns) case studies.
   * `fandango convert` can now produce [state diagrams from grammars](sec:extracting-state-diagrams).
* You can now [download the documentation as a PDF](_static/fandango.pdf) from the upper-right download icon.
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
