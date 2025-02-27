from struct import unpack

def byte_to_int(byte_val):
    return int(unpack('>H', bytes(byte_val))[0])

<start> ::= <len> <inner>{byte_to_int(bytes(<len>))} <byte>+
<len> ::= <byte>{2}
<inner> ::= <len> <byte>{byte_to_int(bytes(<len>))}
<byte> ::= <bit>{8}
<bit> ::= 1 | 0