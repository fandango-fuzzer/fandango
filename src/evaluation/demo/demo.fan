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

## <start_balance> and <end_balance> must be positive integers (logic constraint)

int(<st_bal>) > 0;
int(<end_bal>) >= 0;

## <account_number> must be different. (there are 2 account numbers, receiver and sender)

int(<account_number>[0]) != int(<account_number>[1]);

## first <end_bal> must be equal to the first <st_bal> - <amount>. User who is sending the money (we invoke a user defined function)

#def remove_balance(start_balance, end_balance, amount):
#    return start_balance - amount;

#int(<end_bal>[0]) == remove_balance(int(<st_bal>[0]), int(<end_bal>[0]), int(<am>));

## second <end_balance> must be equal to the first <start_balance> + <amount>. User who is receiving the money (we invoke a user defined function)

#def check_valid_balance_receiver(start_balance, end_balance, amount):
#    return start_balance + amount == end_balance ;

#check_valid_balance_receiver(int(<start_balance>[1]), int(<end_balance>[1]), int(<amount>));

## invoke date_time to fill the <date> (This invokes a external lib)

# import time ;

#def fill_date(): ;
#    return time.strftime("%Y-%m-%d");

# str(<stmt_date>) == fill_date();
