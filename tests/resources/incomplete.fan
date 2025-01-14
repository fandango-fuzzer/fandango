<start> ::= <ab>;
<ab> ::=
      "a" (<ab> | "b")
    | <ab> "b"
    | "c"
    ;