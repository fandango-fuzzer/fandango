def is_big(n):
    return n > 2

<start> ::= <count> <pairs> <nested> <items> <tagged> <plain> <choice> <grouped> <permuted> <terminals>
<count> ::= ('1' | '2' | '3')
<pairs> ::= ('a' <b>)* ('c' 'd')+ ('e' 'f')? ('g' 'h'){2} ('i' 'j'){1,2}
<b> ::= 'b'
<nested> ::= ('k'?)+ ('l'*){2} (('m' 'n')*)?
<items> ::= <item>{int(<count>)} <more>{1,int(<count>)} ('o' 'p'){int(<count>)}
<item> ::= 'x'
<more> ::= 'y'
<tagged> ::= r'[0-9]' := str(int(<source>) + 1)
<source> ::= ('4' | '5') := str(int(<tagged>) - 1)
<plain> ::= r'[0-9]' := str(7)
<choice> ::= 'q' ('r' | 's') ('t' | 'u' 'v')* 'w'{2} 'z'{1,}
<grouped> ::= 'A' ('B' 'C') 'D'
<permuted> ::= [['E' 'F']] [[<b> ('G' 'H') ('I'?)]] ([['J' 'K']]){2}
<terminals> ::= "it's" '"' '\n' '\\' r'[a-c]+' r'''['\"]'''

where forall <i> in <item>: str(<i>) == 'x'
where exists <m> in <more>: str(<m>) == 'y'
where forall <p> in <pairs>: forall <q> in <p>.<b>: str(<q>) == 'b'
where all(str(<i>) == 'x' for <i> in *<item>)
where (int(<count>) > 2) == is_big(int(<count>))
where (int(<count>) > 0 or False) == True
where (not int(<count>)) == False
where (int(<count>) if True else 0) > 0
where int(<count>) > 0 and int(<count>) < 4
where (int(<count>) > 3 or int(<count>) < 4) and int(<count>) != 0
where (int(<count>) > 0 and int(<count>) < 4) and int(<count>) != 0
where (int(<count>) > 3 or int(<count>) < 4) or int(<count>) != 0
where 0 < int(<count>) <= 3 and int(<count>) != 0
where len(*<item>) > 0
where int(<count>) > 0 and (int(<count>) < 4 or not is_big(int(<count>)))
where 0 < int(<count>) <= 3
where str(<start>.<count>) != '' and str(<start>..<b>) != 'c' and str(<pairs>[0]) != ''
minimizing int(<count>)
maximizing len(str(<pairs>))
