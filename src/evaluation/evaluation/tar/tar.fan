# Grammar
<start> ::= <entries><final_entry> ;
<entries> ::= <entry> | <entry><entries> ;
<entry> ::= <header><content> ;
<header> ::= <file_name><file_mode><uid><gid><file_size><mod_time><checksum><typeflag><linked_file_name> 'ustar' <NUL> '00' <uname><gname><dev_maj_num><dev_min_num><file_name_prefix><header_padding> ;
<file_name> ::= <file_name_str><maybe_nuls> ;
<file_name_str> ::= <file_name_first_char><file_name_chars> | <file_name_first_char> ;
<file_mode> ::= <octal_digits><SPACE><NUL> ;
<uid> ::= <octal_digits><SPACE><NUL> ;
<gid> ::= <octal_digits><SPACE><NUL> ;
<file_size> ::= <octal_digits><SPACE> ;
<mod_time> ::= <octal_digits><SPACE> ;
<checksum> ::= <octal_digits><NUL><SPACE> ;
<typeflag> ::= '0' | '2' ;
<linked_file_name> ::= <file_name_str><maybe_nuls> | <nuls> ;
<uname> ::= <uname_str><maybe_nuls> ;
<gname> ::= <uname_str><maybe_nuls> ;
<uname_str> ::= <uname_first_char><uname_chars><maybe_dollar> | <uname_first_char><maybe_dollar> ;
<uname_first_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '_' ;
<uname_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_' | '-' ;
<uname_chars> ::= <uname_char><uname_chars> | <uname_char> ;
<maybe_dollar> ::= '$' | '' ;
<dev_maj_num> ::= <octal_digits><SPACE><NUL> ;
<dev_min_num> ::= <octal_digits><SPACE><NUL> ;
<file_name_prefix> ::= <nuls> ;
<header_padding> ::= <nuls> ;
<content> ::= <maybe_characters><maybe_nuls> ;
<final_entry> ::= <nuls> ;
<octal_digits> ::= <octal_digit><octal_digits> | <octal_digit> ;
<octal_digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' ;
<maybe_characters> ::= <characters> | '' ;
<characters> ::= <character><characters> | <character> ;
<character> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '!' | '"' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | ',' | '-' | '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' | ']' | '^' | '_' | '`' | '{' | '|' | '}' | '~' | ' ' | '	' ;
<file_name_first_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' | 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' | 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' | '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_'  ;
<file_name_chars> ::= <file_name_char><file_name_chars> | <file_name_char> ;
<file_name_char> ::= '&' | '^' | 'I' | '}' | 'F' | 'J' | '|' | 'd' | '~' | '@' | '<' | ')' | 'S' | 'q' | 'k' | 'E' | 'r' | 'X' | 'H' | '`' | 'K' | ':' | 'Q' | '_' | '+' | '4' | ';' | '/' | 'P' | 'n' | "'" | 'g' | 'j' | 't' | 'p' | 'z' | 'c' | '!' | 'T' | 'o' | 'Y' | 'N' | 'e' | '>' | '0' | 'G' | '=' | '{' | '$' | '[' | 'a' | 's' | 'C' | 'A' | '2' | 'W' | '1' | 'V' | 'O' | '#' | 'u' | 'L' | 'R' | '6' | 'y' | 'l' | 'f' | 'h' | 'w' | '(' | ',' | '%' | '5' | '-' | '*' | 'Z' | '?' | '3' | 'b' | 'v' | 'U' | 'D' | '"' | '9' | 'M' | 'i' | 'm' | '8' | ']' | 'x' | '7' | '.' | 'B' ;
<maybe_nuls> ::= <nuls> | '' ;
<nuls> ::= <NUL><nuls> | <NUL> ;
<NUL> ::= '\x00' ;
<SPACE> ::= ' ' ;


# Constraints