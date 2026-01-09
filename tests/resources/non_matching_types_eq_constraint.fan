<start> ::= <length> ";" <content>
<length> ::= <starting_digit> <digit>*
<starting_digit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<content> ::= <word> ("-" <word>)*
<word> ::= "a"

# this compares an int to a field which cannot be converted to an int
where int(str(<length>)) == str(<content>).count("-") + 1