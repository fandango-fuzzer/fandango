import time

from fandango import Grammar
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from fandango.language.symbol.symbol import NonTerminal

word = "USER the_user"

with open("dune.fan") as f:
    grammar, constraints = parse(f, use_stdlib=False)

word = "[{'id': '65', 'quote': 'The thing the ecologically illiterate don't realise about an ecosystem is that it's a system. A system! A system maintains a certain fluid stability that can be destroyed by a misstep in just one niche. A system has order, flowing from point to point. If something dams that flow, order collapses. The untrained might miss that collapse until it was too late. That's why the highest function of ecology is the understanding of consequences.'}]"

tree = grammar.parse(
    word, NonTerminal("<response>"), mode=Grammar.Parser.ParsingMode.INCOMPLETE
)

print(tree.to_tree())
