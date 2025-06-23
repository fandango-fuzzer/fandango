include('expr.fan')

<start> ::= <interaction>
<interaction> ::= <In:input> <Out:output>
<input> ::= <expr> '\n'
<output> ::= <int> '\n'