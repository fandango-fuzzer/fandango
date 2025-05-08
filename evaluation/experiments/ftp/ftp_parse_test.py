import time

from fandango import Grammar
from fandango.evolution.algorithm import Fandango, LoggerLevel
from fandango.language.parse import parse
from fandango.language.symbol import NonTerminal

word = 'modify=20250508110845;perm=fle;type=cdir;unique=C2U1024198;UNIX.group=0;UNIX.groupname=www-data;UNIX.mode=0755;UNIX.owner=0;UNIX.ownername=the_user; .\r\n'

with open("ftp.fan") as f:
    grammar, constraints = parse(f, use_stdlib=False)

tree = grammar.parse(word, NonTerminal('<mlsd_data>'), mode=Grammar.Parser.ParsingMode.COMPLETE)

print(tree)