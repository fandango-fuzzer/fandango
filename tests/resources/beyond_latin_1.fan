# Characters beyond Latin-1, where the parser predicts without lookahead
<start> ::= <char>+
<char> ::= '€' | r'[Ā-￿]' | 'b'
