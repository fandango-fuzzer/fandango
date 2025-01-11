<start>    ::= <field>
<field>    ::= <length> <content>
<length>   ::= <byte> <byte>
where <length> == uint16(len(<content>))
<content>  ::= <digit>+

def uint16(n: int) -> str:
    return chr(n % 256) + chr(n // 256)
