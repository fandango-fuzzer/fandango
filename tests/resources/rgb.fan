<start> ::= <rgb> <endmarker>
    <rgb> ::= <RGB>*
    <RGB> ::= <R> <G> <B>
        <R> ::= <digit>
        <G> ::= <bit>{8}
        <B> ::= <digit>
    <endmarker> ::= <bit>{8} ";"
