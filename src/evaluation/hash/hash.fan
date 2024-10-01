<start> ::= <data_record> ;
<data_record> ::= <string> <hash> ;
<string> ::= <string> <char> | <char> ;
<char> ::= "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" ;
<hash> ::= <hex_digit>* ;
<hex_digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" ;

import hashlib

def check_hash(s, th):
    h = hashlib.new('sha256')
    return hashlib.sha256(str(<s>).encode('utf-8')).hexdigest() == str(<th>)

check_hash(str(<string>), str(<hash>)) ;