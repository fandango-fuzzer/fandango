from struct import unpack

<start> ::= <len> <inner>{unpack('>H', bytes(<len>))[0]} <byte>+
<len> ::= <byte>{2}
<inner> ::= <len> <byte>{unpack('>H', bytes(<len>))[0]}
<byte> ::= <bit>{8}
<bit> ::= 1 | 0