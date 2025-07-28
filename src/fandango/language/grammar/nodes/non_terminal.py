from typing import TYPE_CHECKING, Optional
from collections.abc import Iterator, Sequence
from fandango.errors import FandangoValueError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.node import Node, NodeType
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree

if TYPE_CHECKING:
    import fandango


class NonTerminalNode(Node):
    def __init__(
        self,
        symbol: NonTerminal,
        grammar_settings: Sequence["HasSettings"],
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
    ):
        self.symbol = symbol
        self.sender = sender
        self.recipient = recipient
        super().__init__(NodeType.NON_TERMINAL, grammar_settings)

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        if self.symbol not in grammar:
            raise FandangoValueError(f"Symbol {self.symbol} not found in grammar")

        # Gmutator mutation (4)
        if self.settings.get("non_terminal_use_other_rule"):
            other_nodes = [
                rhs
                for nt, rhs in grammar.rules.items()
                if nt.name() != self.symbol.name()
            ]
            print("other_nodes", [n.format_as_spec() for n in other_nodes])
            alt = Alternative(other_nodes, self._grammar_settings)
            return alt.fuzz(parent, grammar, max_nodes, in_message)

        dummy_current_tree = DerivationTree(self.symbol)
        parent.add_child(dummy_current_tree)

        if grammar.is_use_generator(dummy_current_tree):
            dependencies = grammar.generator_dependencies(self.symbol)
            for nt in dependencies:
                NonTerminalNode(nt, self._grammar_settings).fuzz(
                    dummy_current_tree, grammar, max_nodes - 1
                )
            parameters = dummy_current_tree.children
            for p in parameters:
                p._parent = None
            generated = grammar.generate(self.symbol, parameters)
            # Prevent children from being overwritten without executing generator
            for child in generated.children:
                child.set_all_read_only(True)

            generated.sender = self.sender
            generated.recipient = self.recipient
            parent.set_children(parent.children[:-1])
            parent.add_child(generated)
            return
        parent.set_children(parent.children[:-1])

        assign_sender = None
        assign_recipient = None
        if not in_message and self.sender is not None:
            assign_sender = self.sender
            assign_recipient = self.recipient
            in_message = True

        current_tree = DerivationTree(
            self.symbol,
            [],
            sender=assign_sender,
            recipient=assign_recipient,
            read_only=False,
        )
        parent.add_child(current_tree)
        grammar[self.symbol].fuzz(current_tree, grammar, max_nodes - 1, in_message)

    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor",
    ):
        return visitor.visitNonTerminalNode(self)

    def format_as_spec(self) -> str:
        if self.sender is not None:
            if self.recipient is None:
                return f"<{self.sender}:{(self.symbol.format_as_spec())[:-1]}>"
            else:
                return f"<{self.sender}:{self.recipient}:{(self.symbol.format_as_spec())[:-1]}>"
        else:
            return self.symbol.format_as_spec()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def msg_parties(self, *, include_recipients: bool = False) -> set[str]:
        parties: set[str] = super().msg_parties(include_recipients=include_recipients)
        if self.sender is not None:
            parties.add(self.sender)
            if self.recipient is not None and include_recipients:
                parties.add(self.recipient)
        return parties

    def descendents(
        self, grammar: "fandango.language.grammar.grammar.Grammar"
    ) -> Iterator["Node"]:
        yield grammar.rules[self.symbol]

    def in_parties(self, parties: list[str]) -> bool:
        return not self.sender or self.sender in parties
