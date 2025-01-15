from faker import Faker
fake = Faker()
import random

include('persons-faker.fan')

<age> ::= <digit>+ := str(random.randint(25, 35))
