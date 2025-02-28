def convert(input):
    return input.to_bytes(4)

def un_convert(input):
    return int.from_bytes(input)

<start> ::= <converted> <number>
<converted> ::= <byte>+ :: convert(int(<source>))
<source> ::= <number> :: un_convert(<converted>.to_bytes())

<number> ::= <number_start> <number_tail>{0, 2}
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>
<byte> ::= <bit>{8}
<bit> ::= 1 | 0

where int(<start>.<number>) == int(<source>.<number>)