include('expr.fan')

<start> ::= <interaction>{10}
<interaction> ::= <stdin:input> <stdout:output>
<input> ::= <expr> '\n'
<output> ::= <int> '\n'