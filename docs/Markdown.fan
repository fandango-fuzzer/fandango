from faker import Faker
import random
fake = Faker()

LABELS = []

def make_header():
    header_text = "My Wonderful Section"
    label = header_text.lower().replace(" ", "-")
    LABELS.append(label)
    return header_text

def ref_header():
    if not LABELS:
        return ""
    label = random.choice(LABELS)
    return f"[section](" + label + ")"

<start> ::= (<text> " ")+

<text> ::= "Some text" | <emphasis> | <header> | <link> | <ref> | <table>
<basic_text> ::= r"[a-zA-Z0-9 ]+" := "Some basic text"
<emphasis> ::= "*" <text> "*" | "_" <text> "_"
<header> ::= r"\n#{1,3} " <header_text> "\n\n"
<header_text> ::= <basic_text> := make_header()
<link> ::= "[" <basic_text> "](" <url> ")" := "[example](http://example.com)"
<ref> ::= "[" <basic_text> "](" <label> ")" | "" := ref_header()
<label> ::= r"[a-zA-Z0-9-]+" := "label"
<url> ::= <printable>+ := str(fake.uri())

<table> ::= "\n" <row> <hline> <row>{3}
<row> ::= <cell>{3} "|\n"
<hline> ::= <line_cell>{3} "|\n"
<cell> ::= "|" <basic_text>
<line_cell> ::= "| -- "
