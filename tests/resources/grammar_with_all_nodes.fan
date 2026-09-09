<start> ::= <record>+
<record> ::= <key> '=' <value> <flags> ';'
<key> ::= r'[a-z]+'
<value> ::= <number> | <quoted> | <empty>
<number> ::= <digit>{1,4}
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
<quoted> ::= '"' <char>* '"'
<char> ::= 'x' | 'y'
<empty> ::= ''
<flags> ::= <flag>?
<flag> ::= '!'
