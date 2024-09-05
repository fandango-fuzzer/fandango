import unittest


class TestLanguage(unittest.TestCase):
    EXAMPLE = """

def f(x):
    return x + 1    

start : ab;
ab : "ab" | "a" ab "b";
count(ab) == 4

import os
fandango.import('zip.fan')

def twice(x, ef):
    return x == 2 * ef
    
fitness(<start>) > 0.9

mutate()

selection()
    
<start> ::= <fmt1> | <fmt2>

if <fmt1>:
    <x> > 0

def will_halt(x):
    if x == 0:
        return True
    else:
        return will_halt(x - 1)

<start> ::= <ab>
<ab> ::= "ab" | "a" <ab> "b" | \
    "cd"
count(<ab>) == 4

<ef> ::= "ef" | "e" <ef> "f" 
os.system('ls ' + <ef>) == 0
twice(2, <ab>)


<py>
x = f(1)
</py>
"""

    def test_splitting(self):
        pass
