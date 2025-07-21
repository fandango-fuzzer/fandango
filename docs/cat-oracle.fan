<start> ::= <In:input> <Out:output>
<input> ::= <line>
<output> ::= <line>
<line> ::= r'[.*\n]+'
where str(<input>) == str(<output>)