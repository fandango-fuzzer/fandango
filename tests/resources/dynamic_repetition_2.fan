from struct import unpack
import random

<start> ::= <len_a> <a>{int(<len_a>)} <len_b> <b>{int(<len_b>)}
<len_a> ::= <len>
<len_b> ::= <len>
<len> ::= <number> := str(random.randrange(3, 5))
<a> ::= 'a'
<b> ::= 'b'

<number> ::= <number_start> <number_tailing>*
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tailing> ::= '0' | <number_start>

where int(<len_a>) == (int(<len_b>) + 6)
# where int(<len_b>) < 6