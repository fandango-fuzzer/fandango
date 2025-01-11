from faker import Faker
fake = Faker()

include('persons.fan')

<first_name> ::= <name> := fake.first_name()
<last_name> ::= <name> := fake.last_name()