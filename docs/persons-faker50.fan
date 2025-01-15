from faker import Faker
fake = Faker()

<start> ::= <person_name> "," <age>
<person_name> ::= <first_name> " " <last_name>
<first_name> ::= <name> | <natural_name>
<natural_name> ::= <name> := fake.first_name()
<last_name> ::= <name> := fake.last_name()
<name> ::= <ascii_uppercase_letter><ascii_lowercase_letter>+
<age> ::= <digit>+
