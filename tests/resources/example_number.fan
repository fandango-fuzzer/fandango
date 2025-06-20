<start> ::= <number>
<number> ::= <non_zero><digit>*
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

def is_odd(x):
    return x % 2 != 0

where is_odd(int(<number>))