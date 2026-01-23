#!/usr/bin/env python3

import sys
from typing import Any, Optional

from fandango.converters.FandangoConverter import FandangoConverter
from fandango.language.parse.parse_spec import parse_content


class FandangoStateConverter(FandangoConverter):
    """Convert (normalize) Fandango grammar to state machine format."""

    def __init__(self, filename: str, parties: Optional[list[str]] = None):
        super().__init__(filename)
        self.parties = parties or []

    def to_state(self, format: str = "state", **_kwargs: Any) -> str:
        """Convert the grammar spec to state diagram"""
        contents = open(self.filename, "r").read()
        parsed_spec = parse_content(
            contents, filename=self.filename, use_cache=False, parties=self.parties
        )
        match format:
            case "dot":
                comment = "//"
            case "mermaid":
                comment = "%%"
            case _:
                comment = "#"
        header = f"""{comment} Automatically generated from {self.filename!r}.
{comment} Format: STATE_1 --> STATE_2: [ACTIONS]; `[*]` is a start/end state
{comment}
"""
        return header + str(parsed_spec.grammar.to_states(format=format))


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        converter = FandangoStateConverter(filename)
        print(converter.to_state(format="state"), end="")
