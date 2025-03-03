<start>    ::= <field>
<field>    ::= <length> <content>
<length>   ::= <byte> <byte> := b'\x00\x04'
<content>  ::= <byte>{from_uint16(<length>.value())}

def from_uint16(n: bytes) -> int:
    return n[0] << 8 | n[1]