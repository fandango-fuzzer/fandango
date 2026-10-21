from collections.abc import Iterable
from typing import NamedTuple, Optional

from fandango.errors import FandangoConversionError
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

# How many of the nonterminals above a value locate it in the message
ANCHOR_LENGTH = 3
# The maximum length of a value made of literals that is also abstracted by its exact text
MAX_EXACT_LENGTH = 8


class ValueAbstraction(NamedTuple):
    # "classes", "length", "char" or "exact"
    kind: str
    value: tuple[str, ...] | int | str

    def describe(self) -> str:
        if self.kind == "classes":
            assert isinstance(self.value, tuple)
            return "+".join(self.value) or "empty"
        if self.kind == "length":
            assert isinstance(self.value, int)
            return f"length < {2**self.value}" if self.value else "length 0"
        if self.kind == "char":
            return f"with {self.value!r}"
        return f"= {self.value!r}"


class _ValueSummary(NamedTuple):
    length: int
    chars: frozenset[str]
    exact_text: Optional[str]

    @staticmethod
    def of_leaf(leaf: DerivationTree, literals: frozenset[str]) -> "_ValueSummary":
        if not leaf.symbol.is_terminal:
            return _ValueSummary(0, frozenset(), "")
        text = leaf.to_string()
        exact = text if len(text) <= MAX_EXACT_LENGTH and text in literals else None
        return _ValueSummary(len(text), frozenset(text), exact)

    @staticmethod
    def concatenate(parts: Iterable["_ValueSummary"]) -> "_ValueSummary":
        length = 0
        chars: set[str] = set()
        exact: Optional[str] = ""
        for part in parts:
            length += part.length
            chars |= part.chars
            exact = (
                None
                if exact is None or part.exact_text is None or length > MAX_EXACT_LENGTH
                else exact + part.exact_text
            )
        return _ValueSummary(length, frozenset(chars), exact)

    def abstractions(self) -> list[ValueAbstraction]:
        """Abstracts the value from coarse to fine."""
        abstractions = [
            ValueAbstraction(
                "classes",
                tuple(sorted({self._char_class(char) for char in self.chars})),
            ),
            ValueAbstraction("length", self.length.bit_length()),
        ]
        abstractions.extend(
            ValueAbstraction("char", char)
            for char in sorted(self.chars)
            if not char.isalnum() and ord(char) < 0x80
        )
        if self.exact_text is not None:
            abstractions.append(ValueAbstraction("exact", self.exact_text))
        return abstractions

    @staticmethod
    def _char_class(char: str) -> str:
        code = ord(char)
        if code >= 0x80:
            return "non-ascii"
        if char.islower():
            return "lower"
        if char.isupper():
            return "upper"
        if char.isdigit():
            return "digit"
        if char == " ":
            return "space"
        if char in "\r\n":
            return "newline"
        if code < 0x20 or code == 0x7F:
            return "control"
        return "punctuation"


def literals_of(rules: dict[NonTerminal, Node]) -> frozenset[str]:
    """Collects the texts of the grammar's literal terminals."""
    literals = set()
    pending = list(rules.values())
    while pending:
        node = pending.pop()
        if not isinstance(node, TerminalNode):
            pending.extend(node.children())
        elif not node.symbol.is_regex:
            try:
                literals.add(node.symbol.value().to_string())
            except FandangoConversionError:
                pass
    return frozenset(literals)


def value_features(
    message: DerivationTree, literals: frozenset[str]
) -> frozenset[tuple[tuple[str, ...], ValueAbstraction]]:
    """Abstracts each value in the message from coarse to fine, tied to where in the message it occurs."""
    features: set[tuple[tuple[str, ...], ValueAbstraction]] = set()
    summaries: dict[int, _ValueSummary] = {}
    stack: list[tuple[DerivationTree, tuple[str, ...], bool]] = [(message, (), False)]
    while stack:
        node, anchor, children_done = stack.pop()
        if not node.children:
            summaries[id(node)] = _ValueSummary.of_leaf(node, literals)
            continue
        if not children_done:
            name = _anchor_name(node)
            if name is not None:
                anchor = (*anchor, name)[-ANCHOR_LENGTH:]
            stack.append((node, anchor, True))
            stack.extend((child, anchor, False) for child in node.children)
            continue
        summary = _ValueSummary.concatenate(
            summaries.pop(id(child)) for child in node.children
        )
        summaries[id(node)] = summary
        if _anchor_name(node) is not None:
            features.update(
                (anchor, abstraction) for abstraction in summary.abstractions()
            )
    return frozenset(features)


def _anchor_name(node: DerivationTree) -> Optional[str]:
    """Returns the name of the node if it is a nonterminal of the grammar."""
    if not isinstance(node.symbol, NonTerminal):
        return None
    name = node.symbol.name()
    return None if name.startswith("<__") else name
