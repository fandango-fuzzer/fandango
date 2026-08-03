# WARM-UP - random ("dumb") fuzzing. Nothing to fill in here.
#
# This is the baseline: no structure at all, just random bytes. Run it, then
# measure it, and see how little of the target it reaches. Everything the rest
# of the tutorial adds is about closing that gap.
#
#   fandango fuzz -f exercises/00_random.fan -n 5
#   python fdp_harness.py --spec exercises/00_random.fan --n 1000
#   python fdp_validate.py --step random --spec exercises/00_random.fan
#
# Docs:  first steps with Fandango -> https://fandango-fuzzer.github.io/FirstSpec.html

<start> ::= <byte>*
