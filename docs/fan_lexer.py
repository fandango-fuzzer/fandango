#!/usr/bin/env python
# Simple pygmentizer for .fan files
# Use as
#     $ pygmentize -x -l fan_lexer.py:FanLexer FILE...
# or just invoke it as
#     $ ./fan_lexer.py FILE...

from pygments.lexers.python import PythonLexer
from pygments.token import *

class FanLexer(PythonLexer):
    """Special lexer code for .fan files"""
    name = 'fan'
    aliases = [ 'fan' ]
    filenames = ['*.fan']
    mimetypes = ['text/x-fan']
    
    tokens = PythonLexer.tokens
    tokens['root'] = [
            (r'<[a-zA-Z_][a-zA-Z0-9_]*>', Name.Variable.Magic)
        ] + tokens['root']

if __name__ == '__main__':
    import os, sys
    os.system(f"pygmentize -x -l {sys.argv[0]}:FanLexer " +
              " ".join(sys.argv[1:]))
    
