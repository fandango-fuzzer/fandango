#!/usr/bin/env python
# Simple pygmentizer for .fan files
# Use as
#     $ pygmentize -x -l fan_lexer.py:FanLexer FILE...
# or just invoke it as
#     $ ./fan_lexer.py FILE...

from pygments.lexers.python import PythonLexer
from pygments.token import *
from pygments.lexer import words


class FanLexer(PythonLexer):
    """Special lexer code for .fan files"""

    name = "fan"
    aliases = ["fan"]
    filenames = ["*.fan"]
    mimetypes = ["text/x-fan"]

    tokens = PythonLexer.tokens
    # We use Name.Tag for symbols, as in HTML/XML markup
    tokens["root"] = [(r"<[a-zA-Z_][a-zA-Z0-9_]*>", Name.Tag)] + tokens["root"]
    tokens["keywords"] = [("where", Keyword)] + tokens["keywords"]


if __name__ == "__main__":
    import os, sys

    os.system(f"pygmentize -x -l {sys.argv[0]}:FanLexer " + " ".join(sys.argv[1:]))
