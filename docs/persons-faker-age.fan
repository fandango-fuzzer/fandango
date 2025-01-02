from faker import Faker
fake = Faker()
import random

<start> ::= <person_name> "," <age>;
<person_name> ::= <first_name> " " <last_name>;
<first_name> ::= <name> := fake.first_name();
<last_name> ::= <name> := fake.last_name();
<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>+;
<age> ::= <digit>+ := str(random.randint(25, 35));
