#!/usr/bin/env python

import argparse
import re
import sys
from typing import Any

from lxml import etree  # type: ignore[attr-defined] # types not available

from fandango.converters.FandangoConverter import FandangoConverter


def fan(name):
    """Convert a name to a Fandango identifier."""
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


# See https://lxml.de/validation.html#dtd-1 for information on DTD structure


class DTDFandangoConverter(FandangoConverter):
    """Convert a DTD schema to a Fandango grammar."""

    def __init__(self, filename: str):
        super().__init__(filename)

        self.dtd = etree.DTD(filename)
        self.entities = {}

        for entity in self.dtd.iterentities():
            # print(f"name = {entity.name}, orig = {entity.orig}, content = {entity.content}")
            self.entities[entity.name] = entity.content

        self.attribute_types: dict[str, str] = {}

    def header(self):
        s = f"""# Automatically generated from {self.filename!r}.
#
<ws> ::= <whitespace>+ := ' '  # whitespace sequence
<q> ::= ('"' | "'")? := '"'    # optional quote
"""
        return s

    def to_fan(self) -> str:
        self.attribute_types = {}

        s = self.header()
        for element in self.dtd.iterelements():
            s += self.convert_element(element)

        types = list(self.attribute_types)
        types.sort()
        if types:
            s += f"\n\n# Attribute types, to be further refined"
        for tp in types:
            s += f"\n<{tp}> ::= {self.attribute_types[tp]}"

        return s

    def convert_element(self, element) -> str:
        attrs, values, required_attributes = self.convert_attributes(element)

        s = f"\n\n# {element.name} ({element.type})\n"
        s += f"<{fan(element.name)}> ::= '<{element.name}' (<ws> <{fan(element.name)}_attribute>)* ('/>' | '>' "
        s += self.convert_content(element.content)
        s += f" '</{fan(element.name)}>')\n"
        s += attrs

        if required_attributes:
            s += f"\nwhere ("
            s += "\n   and ".join(
                f"{fan(attribute.name) + '='!r} in <{fan(element.name)}>.descendant_values()"
                for attribute in required_attributes
            )
            s += ")  # required"
        if values:
            s += f"\n\n# {element.name} attribute types"
        for value in values:
            s += f"\n<{fan(element.name)}_{value}> ::= <{value}>"
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
                s += (
                    self.convert_content(content.left)
                    + " "
                    + self.convert_content(content.right)
                )
            case "or":
                s += (
                    self.convert_content(content.left)
                    + " | "
                    + self.convert_content(content.right)
                )
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

    def convert_attributes(self, element) -> tuple[str, list[str], list[Any]]:
        s = f"<{fan(element.name)}_attribute> ::= "

        attrs = []
        values = []
        required_attributes = []
        for attribute in element.iterattributes():
            attr, value, required = self.convert_attribute(attribute)
            attrs.append(attr)
            if value:
                values.append(value)
            if required:
                required_attributes.append(attribute)

        s += "\n    | ".join(attrs)
        return s, values, required_attributes

    def convert_attribute(self, attribute) -> tuple[str, str | None, bool]:
        value = None
        s = f"'{fan(attribute.name)}='"
        if attribute.default == "fixed":
            s += f" <q> {attribute.default_value!r} <q>"
            return s, None, False

        match attribute.type:
            case "enumeration":
                values = (
                    " <q> ("
                    + " | ".join(f"{value!r}" for value in attribute.itervalues())
                    + ") <q>"
                )
                s += values
            case _:
                value = fan(attribute.name + "_value")
                self.attribute_types[value] = f"<{attribute.type}>"
                s += f" <{fan(attribute.elemname)}_{value}> "

        required = attribute.default == "required"
        s += f"  # {attribute.default}"
        if attribute.default_value:
            s += f"; default {attribute.default_value!r}"

        return s, value, required


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a [DTD] schema to a Fandango specification"
    )

    parser.add_argument(dest="files", action="append", type=str, help="schema file")

    args = parser.parse_args(sys.argv[1:])

    for filename in args.files:
        converter = DTDFandangoConverter(filename)
        print(converter.to_fan())
