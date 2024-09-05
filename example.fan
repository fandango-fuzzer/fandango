<py>
def is_odd(x):
    return x % 2 != 0

assert is_odd(3)
</py>

<start> ::= <number> "pepe";
<number> ::= <int> | <int> <int> | <int> <number>;
is_odd(<number>.<number>);
<int> ::= ["0-9"];
forall <x> in <number>[0, 1]: <x>[1].<number>.<int>{0} == 0;


