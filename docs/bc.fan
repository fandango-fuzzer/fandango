include('expr.fan')

<start> ::= <interaction>{10}
<interaction> ::= <In:input> <Out:output>
<input> ::= <expr> '\n'
<output> ::= <int> '\n'