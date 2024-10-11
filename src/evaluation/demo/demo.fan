# Grammar for XML Bank Transaction

<start> ::= <xml_bank_transaction> ;
<xml_bank_transaction> ::= '<?xml version="1.0" encoding="windows-1251"?>\n' <statement> ;
<statement> ::= '<statement>\n' <info> <sender> <receiver> '</statement>' ;
<info> ::= '    <info>\n' <currency> <stmt_date> <amount>'    </info>' ;
<currency> ::= '        <currency>' 'EUR' '</currency>\n' | '       <currency>' 'USD' '</currency>\n' ;
<stmt_date> ::= '       <stmt_date>' 'dummy_date' '</stmt_date>\n' ;
<amount> ::= '        <amount>' <digit>* '</amount>\n' ;
<sender> ::= '  <sender>\n' <account_no> <bank_key> <start_balance> <end_balance> '</sender>' ;
<receiver> ::= '<receiver>' <account_no> <bank_key> <start_balance> <end_balance> '</receiver>' ;
<account_no> ::= '      <account_no>' <account_number> '</account_no>\n' ;
<account_number> ::= <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit> ;
<bank_key> ::= '        <bank_key>' <bank_id> '</bank_key>\n' ;
<bank_id> ::= <digit><digit><digit><digit><digit> ;
<start_balance> ::= '       <start_balance>' <digit>* '</start_balance>\n' ;
<end_balance> ::= '     <end_balance>' 'dummy_amount' '</end_balance>\n' ;
<digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' ;

# Constraints

## <start_balance> and <end_balance> must be positive integers (logic constraint)

## <account_number> must be different. (there are 2 account numbers, receiver and sender)

## first <end_balance> must be equal to the first <start_balance> - <amount>. User who is sending the money (we invoke a user defined function)

## second <end_balance> must be equal to the first <start_balance> + <amount>. User who is receiving the money (we invoke a user defined function)

## invoke date_time to fill the <date> (This invokes a external lib)
