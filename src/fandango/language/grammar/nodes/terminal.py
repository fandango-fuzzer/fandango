import random
import re
from types import NoneType
from typing import TYPE_CHECKING
from collections.abc import Sequence
import exrex
from fandango.errors import FandangoValueError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.symbols import Terminal
from fandango.language.tree import DerivationTree
import fandango.language.grammar.nodes as nodes
from fandango.language.tree_value import TreeValueType
from fandango.logger import LOGGER

if TYPE_CHECKING:
    import fandango


class TerminalNode(Node):
    def __init__(
        self,
        symbol: Terminal,
        grammar_settings: Sequence[HasSettings],
    ):
        self.symbol = symbol
        super().__init__(
            NodeType.TERMINAL, grammar_settings, distance_to_completion=1.0
        )

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        repetitions = 1
        # Gmutator mutation (1a)
        if random.random() < self.settings.get("terminal_should_repeat"):
            if random.random() < 0.5:
                repetitions = 0
                return  # nop, don't add a node
            else:
                repetitions = nodes.MAX_REPETITIONS
        for _ in range(repetitions):
            if not self.symbol.is_regex:
                parent.add_child(DerivationTree(self.symbol))
            else:

                def get_one(pattern: str) -> str:
                    # Gmutator mutation (3)
                    if random.random() < self.settings.get("invert_regex"):
                        attempts = 0
                        while attempts < self.settings.get("max_out_of_regex_tries"):
                            attempt = exrex.getone(".*")
                            if not re.match(pattern, attempt):
                                return attempt
                            attempts += 1
                        LOGGER.warning(
                            f"Failed to generate a non-matching regex: {pattern}, falling back to matching regex"
                        )

                    return exrex.getone(pattern)

                instance: str | bytes
                if self.symbol.is_type(TreeValueType.BYTES):
                    # Exrex can't do bytes, so we decode to str and back
                    pattern = self.symbol.value().to_string("latin-1")
                    instance = get_one(pattern).encode("latin-1")
                elif self.symbol.is_type(TreeValueType.STRING):
                    instance = get_one(str(self.symbol.value()))
                else:
                    raise FandangoValueError(
                        f"Unsupported type: {self.symbol.value().type_}"
                    )
                parent.add_child(DerivationTree(Terminal(instance)))

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitTerminalNode(self)

    def format_as_spec(self) -> str:
        return self.symbol.format_as_spec()

    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)
