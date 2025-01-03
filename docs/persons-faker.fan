from faker import Faker
fake = Faker()

include('docs/persons.fan')

<first_name> ::= <name> := fake.first_name();
<last_name> ::= <name> := fake.last_name();