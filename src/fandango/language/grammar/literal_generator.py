import re

from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.search import resolve_searches


class LiteralGenerator:
    def __init__(self, call: str, nonterminals: dict[str, NonTerminalNode]) -> None:
        self.call = call
        self.nonterminals = nonterminals

    def __repr__(self) -> str:
        return f"LiteralGenerator({self.call!r}, {self.nonterminals!r})"

    def __str__(self) -> str:
        # Generators are created with internal variables;
        # we replace them with "..." to avoid cluttering the output.
        s = re.sub(r"___[0-9a-zA-Z_]+___", r"...", str(self.call))
        return s

    def format_as_spec(self) -> str:
        """
        Format as a string that can be used in a spec file.
        """
        return resolve_searches(self.call, self.nonterminals)

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, LiteralGenerator)
            and self.call == other.call
            and self.nonterminals == other.nonterminals
        )

    def __hash__(self) -> int:
        return hash(self.call) ^ hash(self.nonterminals)
