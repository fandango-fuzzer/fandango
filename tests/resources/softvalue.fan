<start> ::= <sub>
<sub>   ::= <a> "-" <b>
<number> ::= <leadingdigit> | <leadingdigit> <digits>
<leadingdigit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digits> ::= <digit> <digits> | <digit>
<a>     ::= <number>
<b>     ::= <number>

# Hard constraints
where str(<a>) == str(<b>)
where int(str(<a>)) < 1000000 # Unbounded growth would lead to float OverflowError in Fandango 

# Soft value
maximizing int(<a>)
