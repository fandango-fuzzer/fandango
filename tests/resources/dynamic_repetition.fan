from struct import unpack

<start> ::= <len> '(' <inner>{min(int(<len>), 4)} ')'
<len> ::= <number>
<inner> ::= <len> <letter>{min(int(<len>), 4)}
<letter> ::= r'[a-zA-Z]'

<number> ::= <number_start> <number_tailing>*
<number_start> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<number_tailing> ::= '0' | <number_start>

where 1 <= int(<len>) and int(<len>) <= 4