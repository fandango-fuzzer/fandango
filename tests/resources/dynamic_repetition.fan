from struct import unpack
import random

<start> ::= <len> '(' <inner>{int(<len>)} ')'
<len> ::= <number> := str(random.randrange(1, 4))
<inner> ::= <len> <letter>{int(<len>)}
<letter> ::= r'[a-zA-Z]'

<number> ::= <number_start> <number_tailing>*
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tailing> ::= '0' | <number_start>
