# FDP stage 0: pure random bytes. The baseline you show first.
# No structure at all: almost every input dies at the magic check in frame(),
# so this reaches only the outermost lines of the target. It is the "why
# grammars" motivation, live.
<start> ::= <byte>*
