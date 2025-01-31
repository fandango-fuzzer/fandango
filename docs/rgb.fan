<start> ::= <rgb> <endmarker>
    <rgb> ::= <RGB>*  # FIXME: must be {size}
    <RGB> ::= <R> <G> <B>
        <R> ::= <byte>
        <G> ::= <byte>
        <B> ::= <byte>
    <endmarker> ::= "1"
