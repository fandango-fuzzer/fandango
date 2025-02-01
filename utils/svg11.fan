include('svg.fan')

<start> ::= <svg>
<cdata> ::= <digit>+ | <string>
<string> ::= '"' <char>* '"' | "'" <char>* "'"
<char> ::= <printable>
<id> ::= <ascii_letter> (<ascii_letter> | <digit> | '_')*
<nmtoken> ::= <id>
<pcdata> ::= <cdata>