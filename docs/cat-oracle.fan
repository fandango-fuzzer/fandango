<start> ::= <In:input> <Out:output>
<input> ::= <lines>
<output> ::= <lines>
<lines> ::= <line>+
<line> ::= r'.*\n'
where str(<input>) == str(<output>)