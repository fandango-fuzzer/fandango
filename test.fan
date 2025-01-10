<start> ::= <str>;
<digit> ::= '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '0';
<str> ::= <char>{int(<digit>)};
<char> ::= 'a' | 'b' | 'c';

# I want to check if I can use a nonterminal as a parameter of a generator
# Not sure about this. Nope.

def correct_length(a):
    print(a)
    return 'a'

# We have a new feature in fandango, which is using partial derivation trees

# We do something, like we expand some nonterminals. We stop the execution and do something to that input
# Then, we resume the fuzzing, and keep expanding the tree.

# This is not merged yet, its part of alexander's work,
# but it also may help you in the future.

# in any case, I will talk w marius about the <char>{<digit>} bc i think it is quite 
# interesting, not only for your work but for future work we plan to do. 