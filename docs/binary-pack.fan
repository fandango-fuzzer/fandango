<start>    ::= <field>
<field>    ::= <length> <content>
<length>   ::= <byte> <byte>
<content>  ::= <digit>+

from struct import pack

def uint16(n: int) -> str:
    return pack('<H', n).decode('iso8859-1')  # convert to string

where <length> == uint16(len(<content>))