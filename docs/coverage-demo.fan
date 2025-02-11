<start> ::= <html>
<html> ::= <text> | <element>
<element> ::= <open_tag> <html> <close_tag> | <self_closing_tag>
where <open_tag>.<tag_name> == <close_tag>.<tag_name>

<open_tag> ::= r'\x3c' <tag_name> r'\x3e'
<close_tag> ::= r'\x3c/' <tag_name> r'\x3e'
<self_closing_tag> ::= r'\x3c' <tag_name> r'/\x3e'
<tag_name> ::= 'html' | 'head' | 'body' | 'title' | 'p' | 'h1' | 'h2' | 'h3'
<text> ::= r'[^\x3c\x3e]+' := 'Some beautiful text'


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

where coverage(remove_html_markup, str(<start>)) >= 10