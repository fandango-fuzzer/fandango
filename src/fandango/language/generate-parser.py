#!/usr/bin/env python3
# Generate a Python parser for the C++ parser

from speedy_antlr_tool import generate

generate(
    py_parser_path="parser/FandangoParser.py",
    cpp_output_dir="cpp_parser",
    entry_rule_names=["fandango"],
)
