from collections.abc import Hashable, Iterable
from typing import NamedTuple, Optional

from fandango.errors import FandangoConversionError
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

# The last nonterminals above a value that tell where in the message it is
ANCHOR_SYMBOLS = 3
# Values made of literals up to this length count exactly as well
EXACT_LENGTH = 8


class _ValueSummary(NamedTuple):
    length: int
    chars: frozenset[str]
    exact: Optional[str]

    @staticmethod
    def merge(children: Iterable[_ValueSummary]) -> _ValueSummary:
        length = 0
        chars: set[str] = set()
        exact: Optional[str] = ""
        for child in children:
            length += child.length
            chars |= child.chars
            exact = (
                None
                if exact is None or child.exact is None or length > EXACT_LENGTH
                else exact + child.exact
            )
        return _ValueSummary(length, frozenset(chars), exact)

    def levels(self) -> list[Hashable]:
        """The value of a subtree from coarse to fine."""
        levels: list[Hashable] = [
            ("classes", tuple(sorted({self._char_class(char) for char in self.chars}))),
            ("length", self.length.bit_length()),
        ]
        levels.extend(
            ("char", char)
            for char in sorted(self.chars)
            if not char.isalnum() and ord(char) < 0x80
        )
        if self.exact is not None:
            levels.append(("exact", self.exact))
        return levels

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
    """The texts of the grammar's terminals that are not regular expressions; bits are left out."""
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
) -> frozenset[tuple[tuple[str, ...], Hashable]]:
    """
    Coarse to fine abstractions of the values in the message, each tied to where in the message the value occurs.
    The exact text of a value counts only if it is made of literals.
    """
    features: set[tuple[tuple[str, ...], Hashable]] = set()
    summaries: dict[int, _ValueSummary] = {}
    stack: list[tuple[DerivationTree, tuple[str, ...], bool]] = [(message, (), False)]
    while stack:
        node, anchor, children_done = stack.pop()
        if not node.children:
            summaries[id(node)] = _leaf_summary(node, literals)
            continue
        if not children_done:
            name = _anchor_name(node)
            if name is not None:
                anchor = (*anchor, name)[-ANCHOR_SYMBOLS:]
            stack.append((node, anchor, True))
            stack.extend((child, anchor, False) for child in node.children)
            continue
        summary = _ValueSummary.merge(
            summaries.pop(id(child)) for child in node.children
        )
        summaries[id(node)] = summary
        if _anchor_name(node) is not None:
            features.update((anchor, level) for level in summary.levels())
    return frozenset(features)


def describe_level(level: Hashable) -> str:
    assert isinstance(level, tuple)
    kind, value = level
    if kind == "classes":
        return "+".join(value) or "empty"
    if kind == "length":
        return f"length < {2**value}" if value else "length 0"
    if kind == "char":
        return f"with {value!r}"
    return f"= {value!r}"


def _anchor_name(node: DerivationTree) -> Optional[str]:
    """The name of a nonterminal of the grammar, None for terminals and control flow."""
    if not isinstance(node.symbol, NonTerminal):
        return None
    name = node.symbol.name()
    return None if name.startswith("<__") else name


def _leaf_summary(leaf: DerivationTree, literals: frozenset[str]) -> _ValueSummary:
    if not leaf.symbol.is_terminal:
        return _ValueSummary(0, frozenset(), "")
    text = leaf.to_string()
    exact = text if len(text) <= EXACT_LENGTH and text in literals else None
    return _ValueSummary(len(text), frozenset(text), exact)
