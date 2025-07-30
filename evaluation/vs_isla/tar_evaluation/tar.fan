<start> ::= <entries> <final_entry> 
<entries> ::= <entry> | <entry> <entries> 
<entry> ::= <header> <content> 
<header> ::= <file_name><file_mode><uid><gid><file_size><mod_time><checksum><typeflag><linked_file_name>'ustar' <NUL>'00'<uname><gname><dev_maj_num><dev_min_num><file_name_prefix><header_padding>
<file_name> ::= <file_name_first_char> <file_name_chars> <NULs> := generate_file_name() 
<file_name_chars> ::= <file_name_char> <file_name_chars> | "" 
<NULs> ::= <NUL> <NULs> | "" 
<file_mode> ::= <octal_digit>{6} <SPACE> <NUL>
<uid> ::= <octal_digit>{6} <SPACE> <NUL> 
<gid> ::= <octal_digit>{6} <SPACE> <NUL>
<file_size> ::= '00000000' ('1' | '0') <octal_digit>{2} <SPACE>
<mod_time> ::= <octal_digit>{11} <SPACE>
<checksum> ::= <octal_digit>{6} <NUL> <SPACE> 
<typeflag> ::= '0' 
<linked_file_name> ::= <file_name_first_char> <file_name_char_or_nul>{99} | <NUL>{100} := generate_linked_file_name()
<file_name_char_or_nul> ::= <file_name_char> | <NUL> 
<uname> ::= <uname_first_char> <name_char_dollar_nul>{31} := generate_uname("<uname>") 
<gname> ::= <uname_first_char> <name_char_dollar_nul>{31} := generate_uname("<gname>") 
<name_char_dollar_nul> ::= <uname_char> | '$' | <NUL> 
<uname_first_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'| 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z' | '_'
<uname_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'| 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'| '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_' | '-'
<dev_maj_num> ::= <octal_digit>{6} <SPACE> <NUL> 
<dev_min_num> ::= <octal_digit>{6} <SPACE> <NUL> 
<file_name_prefix> ::= <NUL>{155}
<header_padding> ::= <NUL>{12}
<content> ::= <char_or_nul>{512} := generate_content() 
<char_or_nul> ::= <character> | <NUL> 
<final_entry> ::= <NUL>{1024}
<octal_digit> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' 
<character> ::= '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9'| 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'| 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'| 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M'| 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'| '!' | '"' | '#' | '$' | '%' | '&' | "'" | '(' | ')' | '*' | '+' | ',' | '-'| '.' | '/' | ':' | ';' | '<' | '=' | '>' | '?' | '@' | '[' | ']' | '^' | '_'| '`' | '{' | '|' | '}' | '~' | ' ' | '\t' | '\n' | '\r' | '\x0b' | '\x0c'
<file_name_first_char> ::= 'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm'| 'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'| 'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M'| 'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z'| '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '_'
<file_name_char> ::= '&' | '^' | 'I' | '}' | 'F' | 'J' | '|' | 'd' | '~' | '@' | '<' | ')'| 'S' | 'q' | 'k' | 'E' | 'r' | 'X' | 'H' | '`' | 'K' | ':' | 'Q' | '_'| '+' | '4' | ';' | '/' | 'P' | 'n' | "'" | 'g' | 'j' | 't' | 'p' | 'z'| 'c' | '!' | 'T' | 'o' | 'Y' | 'N' | 'e' | '>' | '0' | 'G' | '=' | '{'| '$' | '[' | 'a' | 's' | 'C' | 'A' | '2' | 'W' | '1' | 'V' | 'O' | '#'| 'u' | 'L' | 'R' | '6' | 'y' | 'l' | 'f' | 'h' | 'w' | '(' | ',' | '%'| '5' | '-' | '*' | 'Z' | '?' | '3' | 'b' | 'v' | 'U' | 'D' | '"' | '9'| 'M' | 'i' | 'm' | '8' | ']' | 'x' | '7' | '.' | 'B'
<NUL> ::= '\x00' 
<SPACE> ::= ' ' 

## File Size Constraint "file_size_constr" (generator in grammar)

where forall <entr> in <entry>:
    int(str(<entr>.<header>.<file_size>), 8) >= 10 and int(str(<entr>.<header>.<file_size>), 8) <= 100

## File Name Length Constraint "file_name_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#    len(str(<entr>.<header>.<file_name>)) == 100
# 

def generate_file_name():
    first = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'
    ]
    char = [
        '&', '^', 'I', '}', 'F', 'J', '|', 'd', '~', '@', '<', ')',
        'S', 'q', 'k', 'E', 'r', 'X', 'H', '`', 'K', ':', 'Q', '_',
        '+', '4', ';', '/', 'P', 'n', "'", 'g', 'j', 't', 'p', 'z',
        'c', '!', 'T', 'o', 'Y', 'N', 'e', '>', '0', 'G', '=', '{',
        '$', '[', 'a', 's', 'C', 'A', '2', 'W', '1', 'V', 'O', '#',
        'u', 'L', 'R', '6', 'y', 'l', 'f', 'h', 'w', '(', ',', '%',
        '5', '-', '*', 'Z', '?', '3', 'b', 'v', 'U', 'D', '"', '9',
        'M', 'i', 'm', '8', ']', 'x', '7', '.', 'B'
    ]
    # Previous versions of Fandango supported creating DerivationTrees directly in generators
    # This is deprecated now because it involves additional parsing/serializing
    # This old code serves as the original implementation, the above should be the equivalent string construction

    import random
    n = random.randint(0, 99)
    c = random.choice(first)
    for i in range(n):
        c += random.choice(char)
    for i in range(99 - n):
        c += "\0"
    return c
    # c = [("<file_name_first_char>", [(random.choice(first), [])])]
    # file_name_chars = ("<file_name_chars>", [("", [])])
    # for i in range(n):
    #     file_name_chars = ("<file_name_chars>", [("<file_name_char>", [(random.choice(char), [])]), file_name_chars])
    # c.append(file_name_chars)
    # nuls = ("<NULs>", [("", [])])
    # for i in range(99 - n):
    #     nuls = ("<NULs>", [("<NUL>", [("\0", [])]), nuls])
    # c.append(nuls)
    # return "<file_name>", c


## File Mode Length Constraint "file_mode_length_constraint"
## (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<file_mode>)) == 8
# 

## UID Length Constraint "uid_length_constraint" (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<uid>)) == 8
# 

## GID Length Constraint "gid_length_constraint" (modified in the grammar structure to produce only valid fields)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<gid>)) == 8
# 

## Modification Time Length Constraint "mod_time_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<mod_time>.<octal_digits>)) == 12
# 

## Checksum Constraint "checksum_constraint" (constraint for the fuzzer)

def produce_valid_checksum(header):
    def replace_checksum(tree):
        if tree.is_non_terminal:
            if tree.symbol.name() == "<checksum>":
                return " " * 8
            buf = ""
            for child in tree._children:
                buf += replace_checksum(child)
            return buf
            # return "".join([replace_checksum(child) for child in tree._children])
        if tree.is_terminal:
            return str(tree)
        raise ValueError("Invalid symbol type")

    header_bytes = list(replace_checksum(header).encode("ascii"))
    checksum_value = str(oct(sum(header_bytes)))[2:].rjust(6, "0")
    return checksum_value + "\0 "

where forall <entr> in <entry>:
    str(<entr>.<header>.<checksum>) == produce_valid_checksum(<entr>.<header>)

## Linked File Name Length Constraint "linked_file_name_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#    len(str(<entr>.<header>.<linked_file_name>)) == 100
# 

def generate_linked_file_name():
    import random
    if random.random() < 0.25 or True:
        return "\0" * 100
        # Previous versions of Fandango supported creating DerivationTrees directly in generators
        # This is deprecated now because it involves additional parsing/serializing
        # This old code serves as the original implementation, the above should be the equivalent string construction
        # c = []
        # for i in range(100):
        #     c.append(("<NUL>", [("\0", [])]))
        # return "<linked_file_name>", c
    first = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'
    ]
    char = [
        '&', '^', 'I', '}', 'F', 'J', '|', 'd', '~', '@', '<', ')',
        'S', 'q', 'k', 'E', 'r', 'X', 'H', '`', 'K', ':', 'Q', '_',
        '+', '4', ';', '/', 'P', 'n', "'", 'g', 'j', 't', 'p', 'z',
        'c', '!', 'T', 'o', 'Y', 'N', 'e', '>', '0', 'G', '=', '{',
        '$', '[', 'a', 's', 'C', 'A', '2', 'W', '1', 'V', 'O', '#',
        'u', 'L', 'R', '6', 'y', 'l', 'f', 'h', 'w', '(', ',', '%',
        '5', '-', '*', 'Z', '?', '3', 'b', 'v', 'U', 'D', '"', '9',
        'M', 'i', 'm', '8', ']', 'x', '7', '.', 'B'
    ]
    import random
    n = random.randint(0, 99)
    c = random.choice(first)
    for i in range(n):
        c += random.choice(char)
    for i in range(99 - n):
        c += "\0"
    return c
    # Previous versions of Fandango supported creating DerivationTrees directly in generators
    # This is deprecated now because it involves additional parsing/serializing
    # This old code serves as the original implementation, the above should be the equivalent string construction

    # c = [("<file_name_first_char>", [(random.choice(first), [])])]
    # for i in range(n):
    #     c.append(("<file_name_char_or_nul>", [("<file_name_char>", [(random.choice(char), [])])]))
    # for i in range(99 - n):
    #     c.append(("<file_name_char_or_nul>", [("<NUL>", [("\0", [])])]))
    # return "<linked_file_name>", c

## User Name Length Constraint "uname_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<uname>)) == 32
# 

def generate_uname(name):
    first = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_'
    ]
    char = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', '-'
    ]
    import random
    n = random.randint(0, 31)
    c = random.choice(first)
    for i in range(n):
        c += random.choice(char)
    for i in range(31 - n):
        c += "\0"
    return c
    # Previous versions of Fandango supported creating DerivationTrees directly in generators
    # This is deprecated now because it involves additional parsing/serializing
    # This old code serves as the original implementation, the above should be the equivalent string construction
    # c = [("<uname_first_char>", [(random.choice(first), [])])]
    # for i in range(n):
    #     c.append(("<name_char_dollar_nul>", [("<uname_char>", [(random.choice(char), [])])]))
    # if n < 31 and random.random() < 0.5:
    #     c.append(("<name_char_dollar_nul>", [("$", [])]))
    #     n += 1
    # for i in range(31 - n):
    #     c.append(("<name_char_dollar_nul>", [("<NUL>", [("\0", [])])]))
    # return name, c

## Group Name Length Constraint "gname_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<gname>)) == 32
# 

## Device Major Number Length Constraint "dev_maj_num_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<dev_maj_num>.<octal_digits>)) == 8
# 

## Device Minor Number Length Constraint "dev_min_num_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<dev_min_num>.<octal_digits>)) == 8
# 

## Prefix Length Constraint "prefix_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<file_name_prefix>)) == 155
# 

## Header Padding Length Constraint "header_padding_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<header>.<header_padding>)) == 12
# 

## 15. Content Length Constraint "content_length_constraint" (generator in grammar)

# forall <entr> in <entry>:
#     len(str(<entr>.<content>.<maybe_characters>)) == 512
# 

def generate_content():
    import random
    chars = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-',
        '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_',
        '`', '{', '|', '}', '~', ' '
    ]
    n = random.randint(0, 512)
    c = ""
    for i in range(n):
        c += random.choice(chars)
    for i in range(512 - n):
        c += "\0"
    return c

    # Previous versions of Fandango supported creating DerivationTrees directly in generators
    # This is deprecated now because it involves additional parsing/serializing
    # This old code serves as the original implementation, the above should be the equivalent string construction
    # c = []
    # for i in range(n):
    #     c.append(("<char_or_nul>", [("<character>", [(random.choice(chars), [])])]))
    # for i in range(512 - n):
    #     c.append(("<char_or_nul>", [("<NUL>", [("\0", [])])]))
    # return "<content>", c

## 16. Content Size Constraint "content_size_constr" (constraint for the fuzzer)

where forall <entr> in <entry>:
    str(<entr>.<content>.<content_chars>) == str(<entr>.<content>.<content_chars>).ljust(int(str(<entr>.<header>.<file_size>), 8), " ")

## 17. Final Entry Length Constraint "final_entry_length_constraint" (generator in grammar)

# forall <entr> in <final_entry>:
#     len(str(<entr>)) == 1024
# 

## 18. Link Constraint "link_constraint" (constraint for the fuzzer) # NOT IMPLEMENTED