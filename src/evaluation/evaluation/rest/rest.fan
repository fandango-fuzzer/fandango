<start> ::= <body_elements> ;
<body_elements> ::= <body_element> "\n" <body_elements> | <body_element> ;
<body_element> ::= <section_title> "\n" | <labeled_paragraph> | <paragraph> | <enumeration> ;
<section_title> ::= <title_text> "\n" <underline> ;
<title_text> ::= <title_first_char> | <title_first_char> <nobr_string> ;
<paragraph> ::= <first_paragraph_element> <paragraph_elements> "\n" ;
<label> ::= ".. _" <id> ":" ;
<labeled_paragraph> ::=  <label> "\n\n" <paragraph> ;
<paragraph_elements> ::= <paragraph_element> <paragraph_elements> | <paragraph_element> ;
<first_paragraph_element> ::= <paragraph_chars_nospace> | <internal_reference_nospace> ;
<paragraph_element> ::= <paragraph_chars> | <internal_reference> ;
<internal_reference> ::= <presep> <id> "_" <postsep> ;
<internal_reference_nospace> ::= <id> "_" <postsep> ;
<enumeration> ::= <enumeration_items> "\n" ;
<enumeration_items> ::= <enumeration_item> "\n" <enumeration_items> | <enumeration_item> ;
<enumeration_item> ::= <number> ". " <nobr_string> ;
<paragraph_chars> ::= <paragraph_char> <paragraph_chars> | <paragraph_char> ;
<paragraph_chars_nospace> ::= <paragraph_char_nospace> <paragraph_chars_nospace> | <paragraph_char_nospace> ;
<paragraph_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" | " " | "\t" | "\n" | "\r" | "\x0b" | "\x0c" ;
<paragraph_char_nospace> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" ;
<presep> ::= " " | "\t" | "," | ";" | "(" | ")" ;
<postsep> ::= " " | "\t" | "," | "." | ";" | "(" | ")" ;
<id> ::= "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" ;
<number> ::= <digit_nonzero> <digits> | <digit> ;
<digit_nonzero> ::= "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
<digits> ::= <digit> <digits> | <digit> ;
<digit> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
<nobr_string> ::= <nobr_char> | <nobr_char> <nobr_string> ;
<nobr_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" | " " | "\x0b" | "\x0c" ;
<title_first_char> ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "!" | "\"" | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "," | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "~" ;
<underline> ::= <eqs> | <dashes> ;
<eqs> ::= "=" | "=" <eqs> ;
<dashes> ::= "-" | "-" <dashes> ;


def is_ljust_crop(text, width, fillchar):
    width = int(width)
    return text == (text.ljust(width, fillchar))[:width]

def is_extend_crop(text, width):
    return len(text) == int(width)

def get_number(node):
    # Extracts the number from an <enumeration_item>
    for child in node.children:
        if isinstance(child.symbol, NonTerminal) and child.symbol.symbol == '<number>':
            return int(''.join(get_number(child) for child in node.children if isinstance(child.symbol, Terminal)))
        elif isinstance(child.symbol, Terminal) and child.symbol.symbol.isdigit():
            return int(child.symbol.symbol)
    return None

def is_consecutive(item1, item2):
    # Checks if item2 immediately follows item1 in the same enumeration
    if item1.parent != item2.parent:
        return False
    siblings = item1.parent.children
    idx1 = siblings.index(item1)
    idx2 = siblings.index(item2)
    return idx2 == idx1 + 1


def is_same_position(node1, node2):
    # Checks if two nodes are the same object (same position in the parse tree)
    return node1 is node2

def get_id(node):
    # Extracts the ID from a label node
    # Implement according to your parse tree structure
    if hasattr(node, 'children') and node.children:
        for child in node.children:
            if isinstance(child.symbol, NonTerminal) and child.symbol.symbol == '<id>':
                return get_id(child)
            elif isinstance(child.symbol, Terminal):
                return child.symbol.symbol.strip()
    return ''

# LENGTH_UNDERLINE
forall <section_title> in <start>:
    exists <titletxt> in <section_title>.<title_text>:
        exists <underline> in <section_title>.<underline>:
            (len(str(<titletxt>)) > 0) and
            (len(str(<titletxt>)) <= len(str(<underline>))) and
            is_ljust_crop(str(<titletxt>), len(str(<titletxt>)), " ") and
            is_extend_crop(str(<underline>), len(str(<underline>)))
;

# DEF_LINK_TARGETS
forall <internal_reference> ref in <start>:
    exists <labeled_paragraph> labeled_par_1 in <start>:
        get_id(ref.<id>) == get_id(labeled_par_1.<id>)
    ;
forall <internal_reference_nospace> fref in <start>:
    exists <labeled_paragraph> labeled_par_2 in <start>:
        get_id(fref.<id>) == get_id(labeled_par_2.<id>)
    ;

# NO_LINK_TARGET_REDEF
forall <label> label_1 in <start>:
    exists <id> id_1 in label_1:
        forall <label> label_2 in <start>:
            exists <id> id_2 in label_2:
                is_same_position(label_1, label_2) or
                get_id(id_1) != get_id(id_2)
    ;

# LIST_NUMBERING_CONSECUTIVE
forall <enumeration> in <start>:
    forall <enumeration_item> item_1 in <enumeration>:
        exists <number> number_1 in item_1:
            forall <enumeration_item> item_2 in <enumeration>:
                exists <number> number_2 in item_2:
                    (not is_consecutive(item_1, item_2)) or
                    (is_consecutive(item_1, item_2) and
                        (get_number(number_2) == get_number(number_1) + 1 and
                         get_number(number_1) > 0))
    ;

