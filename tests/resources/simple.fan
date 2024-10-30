<start> ::= <ab>;
<ab> ::= 
      "a" <ab> 
    | <ab> "b"
    | ""
    ;

'a' not in str(<ab>) and |<ab>| > 2;
