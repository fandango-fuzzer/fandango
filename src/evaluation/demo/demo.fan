# Imports

import time

# Grammar for XML Bank Transaction

<start> ::= <xml_bank_transaction> ;
<xml_bank_transaction> ::= '<?xml version="1.0" encoding="windows-1251"?>\n' <statement> ;
<statement> ::= '<statement>\n' <info> <sender> <receiver> '</statement>' ;
<info> ::= '   <info>\n' <currency> <stmt_date> <amount>'   </info>' ;
<currency> ::= '      <currency>' 'EUR' '</currency>\n' | '      <currency>' 'USD' '</currency>\n' ;
<stmt_date> ::= '      <stmt_date>' <timestamp> '</stmt_date>\n' ;
<timestamp> ::= <digit>* :: str(int(time.time())) ;
<amount> ::= '      <amount>' <am> '</amount>\n' ;
<am> ::= <digit>* ;
<sender> ::= '\n   <sender>' <account_no> <bank_key> <start_balance> <end_balance> '   </sender>' ;
<receiver> ::= '\n   <receiver>' <account_no> <bank_key> <start_balance> <end_balance> '   </receiver>\n' ;
<account_no> ::= '\n      <account_no>' <account_number> '</account_no>\n' ;
<account_number> ::= <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit> ;
<bank_key> ::= '      <bank_key>' <bank_id> '</bank_key>\n' ;
<bank_id> ::= <digit><digit><digit><digit><digit> ;
<start_balance> ::= '      <start_balance>' <st_bal> '</start_balance>\n' ;
<st_bal> ::= <digit>* ;
<end_balance> ::= '      <end_balance>' <end_bal> '</end_balance>\n' ;
<end_bal> ::= <digit>* ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;




