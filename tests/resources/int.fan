<start> ::= <number>
<number> ::= <non_zero> <digits> | "0"
<non_zero> ::= "1" | "2" | "3"| "4" | "5" | "6" | "7" | "8" | "9"
<digits> ::= <digit> | <digit> <digits>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

where int(<number>) % 2 == 0
where int(<number>) > 10000
where int(<number>) < 100000