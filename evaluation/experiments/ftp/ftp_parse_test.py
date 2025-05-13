import time

from fandango import Grammar
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal

word = 'USER the_user'

with open("ftp.fan") as f:
    grammar, constraints = parse(f, use_stdlib=False)

tree = grammar.parse(word, NonTerminal('<request_login_user_fail>'), mode=Grammar.Parser.ParsingMode.COMPLETE)

print(tree.to_tree())