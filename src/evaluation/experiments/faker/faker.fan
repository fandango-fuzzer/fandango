<start> ::= <transaction> ;
<transaction> ::= <sender> <receiver> <amount> <currency> ;
<sender> ::= <bank_account> ;
<receiver> ::= <bank_account> ;
<bank_account> ::= <country_code><check_digits><bank_identifier><account_number> ;
<country_code> ::= <alpha><alpha> ;
<check_digits> ::= <digit><digit> ;
<bank_identifier> ::= <alpha><alpha><alpha><alpha> ;
<account_number> ::= <digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit><digit> ;
<amount> ::= <digit>* ;
<currency> ::= "EUR" | "USD" | "GBP" | "JPY" | "CHF" | "CAD" ;
<alpha> ::= 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

from faker import Faker
fake = Faker()

def generate_iban():
    return fake.iban()

str(<sender>) == generate_iban()
str(<receiver>) == generate_iban()