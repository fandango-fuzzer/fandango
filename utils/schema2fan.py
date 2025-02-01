#!/usr/bin/env python

import argparse
import sys
import re

from lxml import etree

def fan(name):
    """Convert a name to a Fandango identifier."""
    r = re.compile(r"^[a-zA-Z0-9_]")
    return r.sub(name, "_")


# See https://lxml.de/validation.html#dtd-1 for information on DTD structure

class DTDConverter(object):
    """Convert a DTD schema to a Fandango grammar."""
    def __init__(self, dtd):
        self.dtd = dtd

    def convert(self, indent=0) -> str:
        s = ""
        for element in self.dtd.iterelements():
            s += self.convert_element(element)
        return s

    def convert_element(self, element, indent=0) -> str:
        s = f"\n\n# {element.name}\n"
        s += f"<{fan(element.name)}> ::= '<{element.name}' (' '+ <{fan(element.name)}_attributes>)* '>'"
        s += self.convert_content(element.content)
        s += f" '</{fan(element.name)}>'\n"
        s += self.convert_attributes(element)
        return s

    def convert_content(self, content):
        if content is None:
            return ""

        s = ""
        match content.type:
            case "pcdata":
                s += "<pcdata>"
            case "element":
                s += f"<{fan(content.name)}>"
            case "seq":
                s += (self.convert_content(content.left) + " "
                      + self.convert_content(content.right))
            case "or":
                s += (self.convert_content(content.left) + " | "
                      + self.convert_content(content.right))
            case _:
                raise ValueError(f"Unknown content type {content.type!r}")

        match content.occur:
            case "once":
                pass
            case "opt":
                s = f"({s})?"
            case "mult":
                s = f"({s})*"
            case "plus":
                s = f"({s})+"
            case _:
                raise ValueError(f"Unknown occurrence {content.occur!r}")

        return s

    def convert_attributes(self, element) -> str:
        s = f"<{fan(element.name)}_attributes> ::= "
        s += " | ".join(self.convert_attribute(attribute) for attribute in element.iterattributes())
        return s

    def convert_attribute(self, attribute) -> str:
        s = f"'{fan(attribute.name)}='"
        match attribute.type:
            case "enumeration":
                values = " (" + " | ".join(repr(value) for value in attribute.itervalues()) + ")"
                s += values
            case _:
                s += f" <{fan(attribute.type)}> "
        return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a [DTD] schema to a Fandango specification"
    )

    parser.add_argument(
        "files",
        type=argparse.FileType('r'),
        nargs="+",
        help="schema file"
    )

    args = parser.parse_args(sys.argv[1:])

    for file in args.files:
        converter = DTDConverter(etree.DTD(file))
        print(f"# Automatically generated from {file.name!r} by schema2fan. Do not edit.")
        print(converter.convert())
