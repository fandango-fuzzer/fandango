#!/usr/bin/env python3
# Fandango standard library

import string

iso8601lib = """# Standard library for Fandango
# This file is generated by the script docs/iso8601.py
# Do not edit this file directly.

# We define each element using all alternatives to avoid biasing the grammar.
"""

def make_def(symbol: str, chars: str, force_binary=False) -> str:
    expansions = []
    for c in chars:
        if c in string.printable and not force_binary:
            expansions.append(repr(c))
        else:
            # Declare these as binary to force latin-1 encoding
            expansions.append(f"b'\\x{ord(c):02x}'")
    return make_rule(symbol, expansions)

def make_rule(symbol: str, expansions: list[str]) -> str:
    return f"<{symbol}> ::= " + " | ".join(expansions) + ";\n"

def make_header(title: str) -> str:
    return f"\n# {title}\n"

def make_comment(comment: str) -> str:
    return f"# {comment}\n"

def make_constraint(constraint: str) -> str:
    return f"{constraint};\n"

def make_code(code: str) -> str:
    return f"{code}\n"


iso8601lib += make_header("ISO 8601 date and time")

iso8601lib += make_code("import datetime\n")

iso8601lib += make_rule("start", ["<iso8601datetime>"])

iso8601lib += make_rule("iso8601datetime",
                    ["<iso8601date> ('T' <iso8601time>)?"])

iso8601lib += make_rule("iso8601date",
                    ["<iso8601year> '-' <iso8601month> ('-' <iso8601day>)?",
                     "<iso8601year><iso8601month><iso8601day>"])
iso8601lib += make_rule("iso8601year", ["('+'|'-')? <digit>{4}"])
iso8601lib += make_rule("iso8601month",
                    [f"'{month:02d}'" for month in range(1, 13)])
iso8601lib += make_rule("iso8601day",
                    [f"'{day:02d}'" for day in range(1, 32)])

iso8601lib += make_rule("iso8601weekdate",
                    ["<iso8601year> '-'? 'W' <iso8601week> ('-' <iso8601weekday>)?"])
iso8601lib += make_rule("iso8601week",
                    [f"'{week:02d}'" for week in range(1, 54)])
iso8601lib += make_rule("iso8601weekday",
                    [f"'{weekday:1d}'" for weekday in range(1, 8)])
iso8601lib += make_rule("iso8601ordinaldate",
                    ["<iso8601year> ('-'? <iso8601ordinalday>)?"])
iso8601lib += make_rule("iso8601ordinalday",
                    [f"'{day:03d}'" for day in range(1, 367)])

iso8601lib += make_rule("iso8601time",
                    ["'T'? <iso8601hour> (':'? <iso8601minute> (':'? <iso8601second> (('.' | ',') <iso8601fraction>)? )? )? <iso8601timezone>?"])
iso8601lib += make_comment("24:00:00 is allowed to represent midnight at the end of a day")
iso8601lib += make_rule("iso8601hour",
                    [f"'{hour:02d}'" for hour in range(0, 25)])
iso8601lib += make_rule("iso8601minute",
                    [f"'{minute:02d}'" for minute in range(0, 60)])
iso8601lib += make_comment("xx:yy:60 is allowed to represent leap seconds")
iso8601lib += make_rule("iso8601second",
                    [f"'{second:02d}'" for second in range(0, 61)])
iso8601lib += make_rule("iso8601fraction", ["<digit>+"])

iso8601lib += make_rule("iso8601timezone", ["'Z'",
                                        "'+' <iso8601hour> (':'? <iso8601minute>)?",
                                        "'-' <iso8601hour> (':'? <iso8601minute>)?"])

iso8601lib += make_def("digit", string.digits)

iso8601lib += make_header("Constraints")
iso8601lib += make_comment("We're being lazy here and leave the checking of leap years and month lengths to the datetime module")

iso8601lib += make_code("""
def is_valid_iso8601datetime(iso8601datetime: str) -> bool:
    try:
        datetime.datetime.fromisoformat(iso8601datetime)
        return True
    except ValueError:
        return False
""")

iso8601lib += make_constraint("is_valid_iso8601datetime(str(<iso8601datetime>))")
# iso8601lib += make_constraint("<iso8601year>.startswith('20')")

if __name__ == "__main__":
    print(iso8601lib)   # Output the standard library