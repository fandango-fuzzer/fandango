<start> ::= <leading_digit> <digit>+
<leading_digit> ::= r'[1-9]'

where int(str(<start>)) < 10000
maximizing int(str(<start>))