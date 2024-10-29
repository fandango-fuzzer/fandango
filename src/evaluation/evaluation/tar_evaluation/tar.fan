# Grammar
<start> ::= <entries><final_entry> ;
<entries> ::= <entry> ; # for testing purposes we just produce a single entry <entry><entries> ;
<entry> ::= <header><content> ;
<header> ::=
    <file_name><file_mode><uid><gid><file_size><mod_time><checksum><typeflag><linked_file_name>
    'ustar' <NUL> '00' <uname><gname><dev_maj_num><dev_min_num><file_name_prefix><header_padding>
;
<file_name> ::= <file_name_str><maybe_nuls>;
<file_name_str> ::= <file_name_first_char><file_name_chars> | <file_name_first_char> ;
<file_mode> ::= <octal_digits_for_mode><SPACE><NUL>;
<octal_digits_for_mode> ::=
    '004000' | '002000' | '001000' | '000400' | '000200' | '000100'
    | '000040' | '000020' | '000010' | '000004' | '000002' | '000001'
;
<uid> ::= <octal_digits_length_5><SPACE><NUL> ;
<octal_digits_length_5> ::= '0'<octal_digit><octal_digit><octal_digit><octal_digit><octal_digit> ;
<gid> ::= <octal_digits_length_5><SPACE><NUL> ;
<file_size> ::= <octal_digits><SPACE>;
<mod_time> ::= <octal_digits><SPACE>;
<checksum> ::= <octal_digits_for_checksum><NUL><SPACE> ;
<octal_digits_for_checksum> ::= <octal_digit>* ;
<typeflag> ::= '0' ; # | '2' ; # we only support regular files
<linked_file_name> ::= <file_name_str><maybe_nuls> | <nuls>;
<uname> ::= <uname_str><maybe_nuls> ;
<gname> ::= <uname_str><maybe_nuls> ;
<uname_str> ::= <uname_first_char><uname_chars><maybe_dollar> | <uname_first_char><maybe_dollar> ;
<uname_first_char> ::=
    'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'
    | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '_'
;
<uname_char> ::=
    'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'
    | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_' | '-'
;
<uname_chars> ::= <uname_char><uname_chars> | <uname_char> ;
<maybe_dollar> ::= '$' | '' ;
<dev_maj_num> ::= <octal_digits_for_devs><SPACE><NUL> ;
<dev_min_num> ::= <octal_digits_for_devs><SPACE><NUL> ;
<octal_digits_for_devs> ::= <octal_digit>*;
<file_name_prefix> ::= <nuls>;
<header_padding> ::= <nuls>;
<content> ::= <maybe_characters><maybe_nuls>;
<final_entry> ::= <nuls>;
<octal_digits> ::= <octal_digit><octal_digits> | <octal_digit> ;
<octal_digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' ;
<maybe_characters> ::= <characters> | '' ;
<characters> ::= <character><characters> | <character> ;
<character> ::=
    '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'
    | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'
    | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M'
    | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    | '!' | '"' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | ',' | '-'
    | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' | ']' | '^' | '_'
    | '`' | '{' | '|' | '}' | '~' | ' ' | '	'
;
<file_name_first_char> ::=
    'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'
    | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'
    | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M'
    | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'
    | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_'
;
<file_name_chars> ::= <file_name_char>* ;
<file_name_char> ::=
    '&' | '^' | 'I' | '}' | 'F' | 'J' | '|' | 'd' | '~' | '@' | '<' | ')'
    | 'S' | 'q' | 'k' | 'E' | 'r' | 'X' | 'H' | '`' | 'K' | ':' | 'Q' | '_'
    | '+' | '4' | ';' | '/' | 'P' | 'n' | "'" | 'g' | 'j' | 't' | 'p' | 'z'
    | 'c' | '!' | 'T' | 'o' | 'Y' | 'N' | 'e' | '>' | '0' | 'G' | '=' | '{'
    | '$' | '[' | 'a' | 's' | 'C' | 'A' | '2' | 'W' | '1' | 'V' | 'O' | '#'
    | 'u' | 'L' | 'R' | '6' | 'y' | 'l' | 'f' | 'h' | 'w' | '(' | ',' | '%'
    | '5' | '-' | '*' | 'Z' | '?' | '3' | 'b' | 'v' | 'U' | 'D' | '"' | '9'
    | 'M' | 'i' | 'm' | '8' | ']' | 'x' | '7' | '.' | 'B'
;
<maybe_nuls> ::= <nuls> | '' ;
<nuls> ::= <NUL><nuls> | <NUL> ;
<NUL> ::= '\x00' ;
<SPACE> ::= ' ' ;


# Constraints

## File Size Constraint "file_size_constr" (generator in grammar)

forall <entr> in <entry>:
    int(<entr>.<header>.<file_size>, 8) >= 10 and
    int(<entr>.<header>.<file_size>, 8) <= 100 and
    len(str(<entr>.<header>.<file_size>.<octal_digits>)) == 12
;

## File Name Length Constraint "file_name_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<file_name>)) == 100
;

## File Mode Length Constraint "file_mode_length_constraint"
## (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<file_mode>)) == 8
# ;

## UID Length Constraint "uid_length_constraint" (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<uid>)) == 8
# ;

## GID Length Constraint "gid_length_constraint" (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<gid>)) == 8
# ;

## Modification Time Length Constraint "mod_time_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<mod_time>.<octal_digits>)) == 12
;

## Checksum Constraint "checksum_constraint" (constraint for the fuzzer)

def produce_valid_checksum(header):
    header_bytes = list(str(header).encode("ascii"))
    checksum_value = str(oct(sum(header_bytes)))[2:].rjust(6, "0")
    return checksum_value

forall <entr> in <entry>:
    str(<entr>.<header>.<checksum>.<octal_digits_for_checksum>) == produce_valid_checksum(<entr>.<header>)
;

## Linked File Name Length Constraint "linked_file_name_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<linked_file_name>)) == 100
;

## User Name Length Constraint "uname_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<uname>)) == 32
;

## Group Name Length Constraint "gname_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<gname>)) == 32
;

## Device Major Number Length Constraint "dev_maj_num_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<dev_maj_num>.<octal_digits>)) == 8
;

## Device Minor Number Length Constraint "dev_min_num_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<dev_min_num>.<octal_digits>)) == 8
;

## Prefix Length Constraint "prefix_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<file_name_prefix>)) == 155
;

## Header Padding Length Constraint "header_padding_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<header>.<header_padding>)) == 12
;

## 15. Content Length Constraint "content_length_constraint" (generator in grammar)

def produce_valid_content():
    return "".ljust(512, "\x00")

forall <entr> in <entry>:
    len(str(<entr>.<content>.<maybe_characters>)) == 512
;

## 16. Content Size Constraint "content_size_constr" (constraint for the fuzzer)

forall <entr> in <entry>:
    str(<entr>.<content>.<maybe_characters>) == str(<entr>.<content>.<maybe_characters>).ljust(int(<entr>.<header>.<file_size>, 8), " ")
;

## 17. Final Entry Length Constraint "final_entry_length_constraint" (generator in grammar)

forall <entr> in <entry>:
    len(str(<entr>.<final_entry>)) == 1024
;

## 18. Link Constraint "link_constraint" (constraint for the fuzzer) # NOT IMPLEMENTED