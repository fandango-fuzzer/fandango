<start> ::= '0' | <leading_digit> <digit>+
<leading_digit> ::= r'[1-9]'

where int(str(<start>)) % 2 == 0
