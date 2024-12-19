from faker import Faker
fake = Faker()
import random

<start> ::= <person_name> "," <age>;
<person_name> ::= <first_name> " " <last_name>;
<first_name> ::= <name> := fake.first_name();
<last_name> ::= <name> := fake.last_name();
<name> ::= <uppercase_letter><lowercase_letter>+;
<age> ::= <digit>+ := str(random.randint(25, 35));
<uppercase_letter> ::=
      "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K"
    | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V"
    | "W" | "X" | "Y" | "Z" ;
<lowercase_letter> ::=
      "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k"
    | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v"
    | "w" | "x" | "y" | "z" ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;