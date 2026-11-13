# Constructs that `fandango convert` has printed with a different meaning or
# in a form that does not parse, next to related ones it printed correctly.
# tests/test_spec_printing.py checks this file like every other .fan file.

def is_big(n):
    return n > 2  # comments are not printed; that is fine


# A setting has to be printed as well.
setting <count> max_out_of_regex_tries = 9999

<start> ::= <count> <pairs> <nested> <items> <tagged> <plain> <choice> <grouped> <terminals>
<count> ::= "1" | "2" | "3"

# A parenthesised sequence under each repetition operator.
<pairs> ::= ("a" <b>)* ("c" "d")+ ("e" "f")? ("g" "h"){2} ("i" "j"){1,2}
<b> ::= "b"

# A repetition of a repetition.
<nested> ::= ("k"?)+ ("l"*){2} (("m" "n")*)?

# Repetition bounds computed from another element.
<items> ::= <item>{int(<count>)} <more>{1, int(<count>)} ("o" "p"){int(<count>)}
<item> ::= "x"
<more> ::= "y"

# Generators that use another element, and one that does not.
<tagged> ::= r"[0-9]" := str(int(<source>) + 1)
<source> ::= "4" | "5" := str(int(<tagged>) - 1)
<plain> ::= r"[0-9]" := str(7)

# Printed correctly so far: alternatives in groups, fixed and open counts.
<choice> ::= "q" ("r" | "s") ("t" | "u" "v")* "w"{2} "z"{1,}

# A parenthesised sequence within a sequence.
<grouped> ::= "A" ("B" "C") "D"

# Printed correctly so far: the kinds of terminals.
<terminals> ::= "it's" '"' "\n" "\\" r"[a-c]+" r"['\"]"

# Quantifiers.
where forall <i> in <item>:
    str(<i>) == "x"
where exists <m> in <more>:
    str(<m>) == "y"
where forall <p> in <pairs>:
    forall <q> in <p>.<b>:
        str(<q>) == "b"
where all(str(<i>) == "x" for <i> in *<item>)

# Parenthesised operands of a comparison.
where (int(<count>) > 2) == is_big(int(<count>))
where (int(<count>) > 0 or False) == True
where (not int(<count>)) == False
where (int(<count>) if True else 0) > 0

# A parenthesised part of a formula.
where (int(<count>) > 3 or int(<count>) < 4) and int(<count>) != 0

# The number of elements of a star selection.
where len(*<item>) > 0

# and, or, not, chained comparisons, selectors.
where int(<count>) > 0 and (int(<count>) < 4 or not is_big(int(<count>)))
where 0 < int(<count>) <= 3
where str(<start>.<count>) != "" and str(<start>..<b>) != "c" and str(<pairs>[0]) != ""

# Soft constraints.
minimizing int(<count>)
maximizing len(str(<pairs>))
