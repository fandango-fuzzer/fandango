<start> ::= <digits>
<digits> ::= <digit> <digits> | <digit>
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

# Hard constraint
where len(str(<start>)) == 5

# Soft constraint
# This cannot be satisfied 100%.
# The best possible solution is something like 88988 or 12345.
where max forall <d1> in <digit>:
    exists <d2> in <digit>:
        int(str(<d1>)) == int(str(<d2>)) + 1
;