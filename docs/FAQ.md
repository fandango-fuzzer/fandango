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

(sec:faq)=
# Fandango FAQ

This document holds frequently asked questions about Fandango.

Why not use Python (or any program) to generate outputs in the first place?
: Regular programs either _parse_ or _produce_ inputs.
Fandango specifications (including constraints) allow for both in a single, concise representation.
Furthermore, you do not have to deal with implementing an appropriate algorithm to achieve goals such as constraints or input diversity; Fandango does all of this for you.

What's the difference to coverage-guided fuzzing?
: A specification-based fuzzer such as Fandango is a _blackbox_ fuzzer.
It does not require feedback (such as coverage) from the program to be tested, nor does it require sample inputs.
On the other hand, the constraints used by Fandango do not preclude coverage guidance. Stay tuned for future extensions.

When will Fandango be ready?
: We expect a public beta early April 2025, and a 1.0 release end of June 2025.