# Fandango Cheat Sheet

## Fuzzing Demo

```
import random; ''.join([chr(random.randint(32, 179)) for i in range(100)])
```

## Miller Demo (`01-miller.fan`)

```
<start> ::= <byte>{20}
```

```shell
$ fandango fuzz -f 01-miller.fan -n 1 | ...
```


## Expression Demo (`02-expressions.fan`)

```
<start>  ::= <expr>
<expr>   ::= <term> ' + ' <expr> |<term> ' - ' <expr> | <term>
<term>   ::= <term> ' * ' <factor> | <term> ' / ' <factor> | <factor>
<factor> ::= '+' <factor> | '-' <factor>| '(' <expr> ')' | <int> | <int> '.' <digit>+
<int>    ::= r'[0-9]' | r'[1-9]' <digit>+
```

```shell
$ fandango fuzz -f 02-expressions.fan -c 'len(str(<start>)) == 10 and eval(str(<start>)) > 10'
```


## Balance Demo (`03-transactions.fan`)

```
### Imports

import time
from faker import Faker
fake = Faker()
def compute_end_balance_sender(start_balance, amount):
        return start_balance - amount


### Grammar for XML Bank Transaction

<start> ::= <xml_bank_transaction>
<xml_bank_transaction> ::= '<?xml version="1.0" encoding="windows-1251"?>\n' <hash> <statement>
<statement> ::= '<statement>\n' <info> <sender> <receiver> '</statement>'
<info> ::= '   <info>\n' <currency> <stmt_date> <amount>'   </info>'
<currency> ::= '      <currency>' 'EUR' '</currency>\n' | '      <currency>' 'USD' '</currency>\n'
<stmt_date> ::= '      <stmt_date>' <timestamp> '</stmt_date>\n'
<timestamp> ::= <digit>+ := str(int(time.time()))
<amount> ::= '      <amount>' <am> '</amount>\n'
<am> ::= <digit>+
<sender> ::= '\n   <sender>' <name> <account_no> <bank_key> <start_balance> <end_balance> '   </sender>'
<receiver> ::= '\n   <receiver>' <name> <account_no> <bank_key> <start_balance> <end_balance> '   </receiver>\n'
<name> ::= '\n      <name>' <name_str> '</name>'
<name_str> ::= r'[A-Z. ]+' # {4000} # := str(fake.name().upper())
<account_no> ::= '\n      <account_no>' <account_number> '</account_no>\n'
<account_number> ::= <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit><digit><digit><digit> <digit><digit>
<bank_key> ::= '      <bank_key>' <bank_id> '</bank_key>\n'
<bank_id> ::= <digit><digit><digit><digit><digit>
<start_balance> ::= '      <start_balance>' <st_bal> '</start_balance>\n'
<st_bal> ::= <digit>+
<end_balance> ::= '      <end_balance>' <end_bal> '</end_balance>\n'
<end_bal> ::= <digit>+
<hash> ::= '<hash>' <hash_val> '</hash>\n'
<hash_val> ::= <hex>*
<hex> ::= <digit> | 'a' | 'b' | 'c' | 'd' | 'e' | 'f'


### Constraints

#### The <amount> must be greater than 0.

where int(<am>) > 0

#### The sender <start_balance> must be greater than the <amount>.

#### The sender <start_balance> must be greater than the <amount>.

where int(<sender>.<end_balance>.<end_bal>) > int(<am>)

```

### Example
```shell
$ fandango fuzz -f 03-transactions.fan
```

```
<name_str> ::= "'; DROP TABLE CREDITORS; --"
```


## HTML Demo (`04-coverage.fan`)

```
<start> ::= <html>
<html> ::= <text> | <element>
<element> ::= <open_tag> <html> <close_tag> | <self_closing_tag>
where <open_tag>.<tag_name> == <close_tag>.<tag_name>

<open_tag> ::= r'\x3c' <tag_name> <attributes> r'\x3e'
<attributes> ::= <attribute>*
<attribute> ::= ' ' <attribute_name> '=' '"' <attribute_value> '"'
<attribute_name> ::= 'id' | 'class' | 'style'
<attribute_value> ::= r'[A-Za-z][aeiou][a-z]+'
<close_tag> ::= r'\x3c/' <tag_name> r'\x3e'
<self_closing_tag> ::= r'\x3c' <tag_name> r'/\x3e'
<tag_name> ::= 'html' | 'head' | 'body' | 'title' | 'p' | 'h1' | 'h2' | 'h3'
<text> ::= (r'[A-Za-z][aeiou][a-z]+ ')+ # := 'Some beautiful text'
```

```
import sys

def coverage(fun, *args, **kwargs):
    covered_lines = set()

    def traceit(frame, event, arg):
        if event == 'line':
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            covered_lines.add((filename, lineno))
        return traceit

    sys.settrace(traceit)
    ret = fun(*args, **kwargs)
    sys.settrace(None)

    return len(covered_lines)

def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out

where coverage(remove_html_markup, str(<start>)) >= 10  # 11, 12
```

```shell
$ fandango fuzz -f 04-coverage.fan
```