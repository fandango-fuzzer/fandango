<start> ::= <image> ;
<image> ::= <width> <height> <pixels> ;
<width> ::= <uint8> ;
<height> ::= <uint8> ;
<uint8> ::= <byte> ;
<pixels> ::= <rgb>* ;
<rgb> ::= <byte> ;
<byte> ::= <bit> <bit> <bit> <bit> <bit> <bit> <bit> <bit> ;
<bit> ::= '0' | '1' ;


from struct import unpack
def uint8(s):
    return unpack('>H', s)[0]

len(<pixels>) == uint8(<width>) * uint8(<height>) * 3 ;
