<start> ::= <img>
<img> ::= <width> <height> <pixels>
<width> ::= <uint16>
<height> ::= <uint16>
<pixels> ::= <rgb>*
<uint16> ::= <byte> <byte>
<rgb> ::= <byte> <byte> <byte>

def uint16(tree):
    b = tree.to_bytes()
    return b[1] * 256 + b[0]

where len(<pixels>) == uint16(<width>) * uint16(<height>) * 3
