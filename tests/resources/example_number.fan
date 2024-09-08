<start> ::= <number>;
<number> ::= <non_zero><digit>* | "0";
<non_zero> ::=
              "1"
            | "2"
            | "3"
            | "4"
            | "5"
            | "6"
            | "7"
            | "8"
            | "9"
            ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";

<py>
def is_odd(x):
    return x % 2 != 0

assert is_odd(3)
</py>

is_odd(<number>);