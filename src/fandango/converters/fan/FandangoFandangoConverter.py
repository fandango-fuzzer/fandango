#!/usr/bin/env python3

import sys

from fandango.converters.FandangoConverter import FandangoConverter
from fandango.language.parse import parse_spec


class FandangoFandangoConverter(FandangoConverter):
    """Convert (normalize) Fandango grammar to Fandango format"""

    def __init__(self, filename: str, parties: list[str] | None = None):
        super().__init__(filename)
        self.parties = parties or []

    def to_fan(self, **kw_args) -> str:
        """Convert the grammar spec to Fandango format"""
        contents = open(self.filename, "r").read()
        parsed_spec = parse_spec(
            contents, filename=self.filename, use_cache=False, parties=self.parties
        )
        header = f"""# Automatically generated from {self.filename!r}.
#
"""
        return header + str(parsed_spec)


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        converter = FandangoFandangoConverter(filename)
        print(converter.to_fan(), end="")
