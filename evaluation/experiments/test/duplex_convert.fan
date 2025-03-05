def convert(input):
    return input[::-1]

def un_convert(input):
    return input[::-1]

<start> ::= <number> <rev_number>
<rev_number> ::= <number_tail>{0, 2} <number_start> :: convert(<source_number>)
<source_number> ::= <number> :: un_convert(<rev_number>)

<number> ::= <number_start> <number_tail>{0, 2}
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= '0' | <number_start>
<byte> ::= <bit>{8}
<bit> ::= 1 | 0

#where <source_number>.<number> == <start>.<number>
#where <start>.<number> == <source_number>.<number>
#where str((<start>.<number>)[::-1]) == str(<rev_number>)
#where str(<rev_number>) == str((<start>.<number>)[::-1])
