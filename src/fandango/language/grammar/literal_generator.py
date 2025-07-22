import re


class LiteralGenerator:
    def __init__(self, call: str, nonterminals: dict):
        self.call = call
        self.nonterminals = nonterminals

    def __repr__(self):
        return f"LiteralGenerator({self.call!r}, {self.nonterminals!r})"

    def __str__(self):
        # Generators are created with internal variables;
        # we replace them with "..." to avoid cluttering the output.
        s = re.sub(r"___[0-9a-zA-Z_]+___", r"...", str(self.call))
        return s

    def __eq__(self, other):
        return (
            isinstance(other, LiteralGenerator)
            and self.call == other.call
            and self.nonterminals == other.nonterminals
        )

    def __hash__(self):
        return hash(self.call) ^ hash(self.nonterminals)
