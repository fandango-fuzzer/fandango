# Grammar for XML Bank Transaction

<start> ::= <xml_bank_transaction> ;
<xml_bank_transaction> ::= '<?xml version="1.0" encoding="windows-1251"?>\n' <statement> ;
<statement> ::= '<statement>\n' <info> <sender> <receiver> '</statement>' ;
<info> ::= '   <info>\n' <currency> <stmt_date> <amount>'   </info>' ;
<currency> ::= '      <currency>' 'EUR' '</currency>\n' | '      <currency>' 'USD' '</currency>\n' ;
<stmt_date> ::= '      <stmt_date>' 'dummy_date' '</stmt_date>\n' ;
<amount> ::= '      <amount>' <am> '</amount>\n' ;
<am> ::= <digit>* ;
<sender> ::= '\n   <sender>' <account_no> <bank_key> <start_balance> <end_balance> '   </sender>' ;
<receiver> ::= '\n   <receiver>' <account_no> <bank_key> <start_balance> <end_balance> '   </receiver>\n' ;
<account_no> ::= '\n      <account_no>' <account_number> '</account_no>\n' ;
<account_number> ::= <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit> ;
<bank_key> ::= '      <bank_key>' <bank_id> '</bank_key>\n' ;
<bank_id> ::= <digit><digit><digit><digit><digit> ;
<start_balance> ::= '      <start_balance>' <st_bal>* '</start_balance>\n' ;
<st_bal> ::= <digit>* ;
<end_balance> ::= '      <end_balance>' <end_bal> '</end_balance>\n' ;
<end_bal> ::= <digit>* ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

# Constraints

## Both <start_balance> and <end_balance> must be greater than 0.

int(<st_bal>) > 0;
int(<end_bal>) >= 0;

## The <account_number> must be different for both sender and receiver.

int(<account_number>[0]) != int(<account_number>[1]);

## The <end_balance> of sender must be equal to the <start_balance> - <amount>.

def compute_end_balance_sender(start_balance, amount):
    return start_balance - amount;

int(<end_bal>[0]) == compute_end_balance_sender(int(<st_bal>[0]), int(<amount>));

## The <end_balance> of receiver must be equal to the <start_balance> + <amount>.

def compute_end_balance_receiver(start_balance, amount):
    return start_balance + amount;

int(<end_bal>[1]) == compute_end_balance_receiver(int(<st_bal>[1]), int(<amount>));

## The <stmt_date> must be now.

import time;

def now():
    return time.strftime("%Y-%m-%d");

<stmt_date> == '      <stmt_date>' now() '</stmt_date>\n';


