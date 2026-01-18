#!/usr/bin/env python3

import sys
from typing import Any, Optional

from fandango.converters.FandangoConverter import FandangoConverter
from fandango.language.parse import parse_spec


class FandangoStateConverter(FandangoConverter):
    """Convert (normalize) Fandango grammar to state machine format."""

    def __init__(self, filename: str, parties: Optional[list[str]] = None):
        super().__init__(filename)
        self.parties = parties or []

    def to_state(self, **_kwargs: Any) -> str:
        """Convert the grammar spec to Fandango format"""
        contents = open(self.filename, "r").read()
        parsed_spec = parse_spec(
            contents, filename=self.filename, use_cache=False, parties=self.parties
        )
        header = f"""# Automatically generated from {self.filename!r}.
#
"""
        return header + str(parsed_spec.grammar.to_states())


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        converter = FandangoStateConverter(filename)
        print(converter.to_state(), end="")
