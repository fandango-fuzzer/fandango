#!/usr/bin/env python
# Simple coverage measurement for Python

import sys


def coverage(fun, *args, **kwargs):
    covered_lines = set()

    def traceit(frame, event, arg):
        if event == "line":
            filename = frame.f_code.co_filename
            lineno = frame.f_lineno
            covered_lines.add((filename, lineno))
        return traceit

    sys.settrace(traceit)
    ret = fun(*args, **kwargs)
    sys.settrace(None)

    return ret, covered_lines


if __name__ == "__main__":

    def remove_html_markup(s):
        tag = False
        quote = False
        out = ""

        for c in s:
            if c == "<" and not quote:
                tag = True
            elif c == ">" and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

        return out

    ret, covered_lines = coverage(remove_html_markup, "foo")
    print("Return value:", ret)
    print("Covered lines:", len(covered_lines))
