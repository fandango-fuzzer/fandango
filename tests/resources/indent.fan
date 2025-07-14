# Various indentation tests
<a> ::= <b>
    <b> ::= <c>
<c> ::= "1"

<a> ::= (
    "a"
    | "a" <a>)

<a> ::= \
    "a" \
    | "a" <a>

where forall <a> in <b>:
    forall <c> in <d>:
        True

def foo():
    if 1:
        pass
    elif 2:
        pass

<start> ::= ('a' | 'b' | 'c')+
where str(<start>) != 'd'

<start> ::= ('a' | 'b' | 'c')+
    where str(<start>) != 'd'

    <start> ::= ('a' | 'b' | 'c')+ 'd'
    where str(<start>) != 'd'
    
