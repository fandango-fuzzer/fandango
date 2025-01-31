<start> ::= <rgb> <endmarker>
    <rgb> ::= <RGB>*
    <RGB> ::= <R> <G> <B>
        <R> ::= <byte>
        <G> ::= <bit>{8}
        <B> ::= <byte>
    <endmarker> ::= <bit>{8} ";"
