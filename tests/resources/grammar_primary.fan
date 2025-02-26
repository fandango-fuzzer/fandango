from zlib import compress, decompress

def get_name():
    return "JOHN SMITH"
    
def compress_name(name: str):    
    return compress(name.encode("utf-8")).hex()
    
def decompress_name(compressed: str):
    return decompress(bytes.fromhex(compressed)).decode()


<start> ::= <name>
<name> ::= <decompressed_name> | <generated_name>
<generated_name> ::= <alpha>* := get_name()
<decompressed_name> ::= <alpha>* := decompress_name(<compressed_name>)
<alpha> ::= ' ' | '.' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
<compressed_name> ::= <alphanum>* := compress_name(<name>)