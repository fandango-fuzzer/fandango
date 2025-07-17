
def reverse(input):
    return input[::-1]

def str_to_bit_converter(input):
    return input.encode()

def bit_to_str_converter(input):
    return input.decode()

<start> ::= <converted_outer>
<converted_outer> ::= <byte>+ := str_to_bit_converter(str(<converted_inner>))
<converted_inner> ::= <dummy_outer_2> := bit_to_str_converter(bytes(<converted_outer>))

<dummy_outer_2> ::= <number_tail>+ := bit_to_str_converter(bytes(<dummy_inner_2>))
<dummy_inner_2> ::= <dummy_outer> := str_to_bit_converter(str(<dummy_outer_2>))

<dummy_outer> ::= <byte>+ := str_to_bit_converter(str(<dummy_inner>))
<dummy_inner> ::= <nr_palindrome> := bit_to_str_converter(bytes(<dummy_outer>))

<nr_palindrome> ::= <number> <rev_number>

<rev_number> ::= <number_tail>{0, 2} <number_start> := reverse(str(<source_number>))
<source_number> ::= <number> := reverse(str(<rev_number>))



<number> ::= <number_start> <number_tail>{0, 2}
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tail> ::= <number_start> | '0'

<byte> ::= <bit>{8}
<bit> ::= 0 | 1


#where <source_number>.<number> == <nr_palindrome>.<number>
#where <nr_palindrome>.<number> == <source_number>.<number>
where str((<nr_palindrome>.<number>)[::-1]) == str(<rev_number>)
#where str(<rev_number>) == str((<nr_palindrome>.<number>)[::-1])