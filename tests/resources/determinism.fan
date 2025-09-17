# PYTHONHASHSEED=0 fandango fuzz -f tests/resources/determinism.fan -n 10 --random-seed 1

<start> ::= <sub>
<sub>   ::= <a> "-" <b>
<number> ::= <leadingdigit> | <leadingdigit> <digits>
<leadingdigit> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
<digits> ::= <digit> <digits> | <digit>
<a>     ::= <number>
<b>     ::= <number>

where str(<a>) == str(<b>)
where int(str(<a>)) < 1000000
where int(str(<b>)) >  500000