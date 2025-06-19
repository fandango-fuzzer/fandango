<start> ::= <number>
<number> ::= <non_zero><digit>* | "0"
<non_zero> ::= (
              "1"
            | "2"
            | "3"
            | "4"
            | "5"
            | "6"
            | "7"
            | "8"
            | "9")
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

def f(x):
    return int(x)

where f(<number>) % 2 == 0