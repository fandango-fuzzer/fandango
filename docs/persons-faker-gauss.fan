from faker import Faker
fake = Faker()
import random

include('persons-faker.fan')

<age> ::= <digit>+ := str(int(random.gauss(35)))
