<start>    ::= <field>
<field>    ::= <length> <content>
<length>   ::= <byte> <byte>
where <length> == uint16(len(<content>))
<content>  ::= <byte>+

def uint16(n: int) -> bytes:
    return n.to_bytes(2, 'big')
