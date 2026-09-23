import sys

from fandango import Fandango
from fandango.language.parse.parse import parse


sys.setrecursionlimit(10_000_000)
with open("concat_grammar.fan") as f:
    SPEC = f.read()
grammar, constraints = parse(SPEC, use_stdlib=True, use_cache=True)

fandango = Fandango._with_parsed(grammar, constraints)

for s in fandango.generate_solutions():
    print(s)
