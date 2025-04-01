# Imports

import time
from faker import Faker
fake = Faker()
def compute_end_balance_sender(start_balance, amount):
        return start_balance - amount


# Grammar for XML Bank Transaction

<start> ::= <xml_bank_transaction> ;
<xml_bank_transaction> ::= '<?xml version="1.0" encoding="windows-1251"?>\n' <hash> <statement> ;
<statement> ::= '<statement>\n' <info> <sender> <receiver> '</statement>' ;
<info> ::= '   <info>\n' <currency> <stmt_date> <amount>'   </info>' ;
<currency> ::= '      <currency>' 'EUR' '</currency>\n' | '      <currency>' 'USD' '</currency>\n' ;
<stmt_date> ::= '      <stmt_date>' <timestamp> '</stmt_date>\n' ;
<timestamp> ::= <digit>* :: str(int(time.time())) ;
<amount> ::= '      <amount>' <am> '</amount>\n' ;
<am> ::= <digit>* ;
<sender> ::= '\n   <sender>' <name> <account_no> <bank_key> <start_balance> <end_balance> '   </sender>' ;
<receiver> ::= '\n   <receiver>' <name> <account_no> <bank_key> <start_balance> <end_balance> '   </receiver>\n' ;
<name> ::= '\n      <name>' <name_str> '</name>' ;
<name_str> ::= <letter>* :: str(fake.name()).upper();
<account_no> ::= '\n      <account_no>' <account_number> '</account_no>\n' ;
<account_number> ::= <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit> ;
<bank_key> ::= '      <bank_key>' <bank_id> '</bank_key>\n' ;
<bank_id> ::= <digit><digit><digit><digit><digit> ;
<start_balance> ::= '      <start_balance>' <st_bal> '</start_balance>\n' ;
<st_bal> ::= <digit>* ;
<end_balance> ::= '      <end_balance>' <end_bal> '</end_balance>\n' ;
<end_bal> ::= <digit>* ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;
<letter> ::= ' ' | '.' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' ;
<hash> ::= '<hash>' <hash_val> '</hash>\n' ;
<hash_val> ::= <hex>* ;
<hex> ::= <digit> | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' ;


# Constraints

## The <amount> must be greater than 0.

int(<am>) > 0;

## The sender <start_balance> must be greater than the <amount>.

int(<sender>*<end_bal>) > int(<am>);

## The <end_balance> of sender must be equal to the <start_balance> - <amount>.

int(<sender>*<end_bal>) == compute_end_balance_sender(int(<sender>*<st_bal>), int(<am>));

## The <end_balance> of receiver must be equal to the <start_balance> + <amount>.

int(<receiver>*<end_bal>) == int(<receiver>*<st_bal>) + int(<am>);

