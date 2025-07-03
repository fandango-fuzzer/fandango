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

Where does the name Fandango come from?
: Fandango is an [Iberian dance](https://en.wikipedia.org/wiki/Fandango). We chose the name because of the lively nature of the dance. Also, in the [Hacker file](http://www.catb.org/jargon/) (also known as The New Hacker's Dictionary), the term [Fandango on Core](http://www.catb.org/jargon/html/F/fandango-on-core.html) is listed as a term for corrupted main (core) memory, so it is also related to bugs.
% Finally, the song [Bohemian Rhapsody](https://en.wikipedia.org/wiki/Bohemian_Rhapsody) famously references Fandango.

Where would one get Fandango grammars and constraints from?
: Besides writing them manually, one can use [converters](sec:converters) to generate them from other formal specifications such as ANTLR. Recent research has shown various methods to extract grammars from existing programs ({cite}`bettscheider2024mining`,
{cite}`gopinath2020mining`,
{cite}`schroeder2022mining`,
{cite}`kulkarni2022arvada`)
In a few years, we expect that LLMs will be able to help with writing input specifications just like they help in synthesizing code - and then, Fandango will be there to leverage your specs.

Why not use Python (or any program) to generate outputs in the first place?
: Regular programs either _parse_ or _produce_ inputs.
Fandango specifications (including constraints) allow for both in a single, concise representation.
Since Fandango can use its specs to parse _and_ produce inputs, it can easily mutate existing inputs without any implementation effort.
Finally, you do not have to deal with implementing an appropriate algorithm to achieve goals such as constraints or input diversity; Fandango does all of this for you.

What other alternatives are there to specify input languages?
: Apart from program code (see above), not many. We believe that Fandango is the only approach to allow a full specification of inputs that can be used for both _parsing_ and _producing_; indeed, it can specify inputs from the bit layer up to the application layer, including how these layers translate into each other.

What's the difference to coverage-guided fuzzing?
: A specification-based fuzzer such as Fandango is a _blackbox_ fuzzer.
It does not require feedback (such as coverage) from the program to be tested, nor does it require sample inputs.
On the other hand, the constraints used by Fandango do not preclude coverage guidance. Stay tuned for future extensions.

How well does Fandango scale?
: _Programs_ are the most complex inputs known to mankind; and Fandango very likely will not be able to achieve both 100% precision and 100% diversity, (Nor does any other method on this planet, by the way.) But any file format whose complexity is lower (or if you can live with much lower precision or diversity) should work with Fandango. Please share your experiences!

Who made the Fandango teaser video?
: The [Fandango teaser video](https://www.youtube.com/watch?v=JXMk-XhuKPY) was produced by the Public Relations team at CISPA, based on a script by Andreas Zeller and starring José Antonio Zamudio Amaya. Andreas also did the narration in Attenborough style; no AI or other post-processing was involved.
