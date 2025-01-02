<start>    ::= <field>;
<field>    ::= <length> <content>;
<length>   ::= <byte> <byte>;
<content>  ::= <digit>+;
<digit>    ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9";

def uint16(n: int) -> str:
    return chr(n % 256) + chr(n // 256)

<length> == uint16(len(<content>));