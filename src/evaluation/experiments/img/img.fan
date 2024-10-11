<start> ::= <image> ;
<image> ::= <width> <height> <pixels> ;
<width> ::= <uint16> ;
<height> ::= <uint16> ;
<uint16> ::= <byte> <byte> ;
<pixels> ::= <rgb>* ;
<rgb> ::= <byte> <byte> <byte> ;
<byte> ::= b"\x00" | b"\x01" | b"\x02" |


from struct import unpack
def uint16(s):
    return unpack('>H', s)[0]

len(<pixels>) == uint16(<width>) * uint16(<height>) * 3 ;
