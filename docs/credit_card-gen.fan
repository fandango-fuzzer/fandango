<start>              ::= <credit_card_number>
<credit_card_number> ::= <number> <check_digit> := add_check_digit(str(<number>))
<number>             ::= <digit>{15} := strip_check_digit(str(<credit_card_number>))
<check_digit>        ::= <digit>

def add_check_digit(number: str) -> str:
    """Add a check digit to the credit card number `number`."""
    check_digit = credit_card_check_digit(number)
    return number + check_digit

def strip_check_digit(number: str) -> str:
    """Strip the check digit from the credit card number `number`."""
    return number[:-1]

def credit_card_check_digit(number: str) -> str:
    """Create a check digit for the credit card number `number`."""
    luhn_lookup = {
        "0": 0,
        "1": 2,
        "2": 4,
        "3": 6,
        "4": 8,
        "5": 1,
        "6": 3,
        "7": 5,
        "8": 7,
        "9": 9,
    }

    # Calculate sum
    length = len(number) + 1
    reverse = number[::-1]
    tot = 0
    pos = 0
    while pos < length - 1:
        tot += luhn_lookup[reverse[pos]]
        if pos != (length - 2):
            tot += int(reverse[pos + 1])
        pos += 2

    # Calculate check digit
    check_digit = (10 - (tot % 10)) % 10
    return str(check_digit)
