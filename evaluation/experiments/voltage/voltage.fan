<start> ::= <voltage>
<voltage> ::= <integer> := str(produce_gaussian_integer())
<integer> ::= <positive_integer> | "-" <positive_integer>
<positive_integer> ::= "0" | <digit_nonzero> <digit>*
<digit> ::= "0" | <digit_nonzero>
<digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"

def produce_gaussian_integer():
    import random
    mu = 100
    sigma = 50
    value = random.gauss(mu, sigma)
    return round(value)