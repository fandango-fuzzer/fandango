from __future__ import annotations

from typing import Optional

from fandango.errors import FandangoValueError
from fandango.io.navigation.graph.forecasting_result import (
    ForecastingPacket,
    ForecastingResult,
    MountingPath,
)
from fandango.io.navigation.graph.packetiterativeparser import PacketIterativeParser
from fandango.io.navigation.graph.stategrammarconverter import StateGrammarConverter
from fandango.io.navigation.graph.visitor.continuing_nodevisitor import (
    ContinuingNodeVisitor,
)
from fandango.io.packet_evolution.packet_mounter import MessageHolders
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree


class PathFinder(ContinuingNodeVisitor):
    """
    For a given grammar and DerivationTree, this class
    finds possible upcoming message types, the nonterminals that generate them and the paths where the messages
    can be added to the DerivationTree.
    """

    def __init__(self, grammar: Grammar):
        super().__init__(grammar)
        self.collapsed_tree: Optional[DerivationTree] = None
        self.result = ForecastingResult()

    def add_option(self, node: NonTerminalNode) -> None:
        assert self.collapsed_tree is not None
        mounting_path = MountingPath(self.collapsed_tree, tuple(self.current_path))
        f_packet = ForecastingPacket(node)
        f_packet.add_path(mounting_path)
        self.result.add_packet(node.sender, f_packet)

    def forecast(
        self,
        tree: Optional[DerivationTree] = None,
        session_messages: Optional[MessageHolders] = None,
    ) -> ForecastingResult:
        """
        Finds all possible protocol messages that can be mounted to the given DerivationTree.
        :param tree: The DerivationTree to base the search on. The DerivationTree must contain controlflow nodes
        as provided by the DerivationTree parser with the parsing option 'include_controlflow=True'
        :param session_messages: The session's messages, hung into the collapsed tree in place of the message placeholders.
        """
        if tree is None:
            tree = DerivationTree(NonTerminal("<start>"))
        self.result = ForecastingResult()
        self.collapsed_tree = self.grammar.collapse(tree)
        if session_messages is not None and self.collapsed_tree is not None:
            session_messages.hang_messages_into(self.collapsed_tree)
        super().find(tree)
        return self.result

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        if node.sender is not None:
            if is_exploring:
                self.add_option(node)
                return False, False
            else:
                return True, False
        return True, True

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        raise FandangoValueError(
            "PacketForecaster reached TerminalNode! This is a bug."
        )


class PacketForecaster:
    def __init__(self, grammar: Grammar):
        reduced_rules = StateGrammarConverter(grammar.grammar_settings).process(
            grammar.rules
        )
        self.grammar = grammar
        self._parser = PacketIterativeParser(reduced_rules)

    def predict(self, tree: DerivationTree) -> ForecastingResult:
        """
        Predicts the next possible message types based on the provided tree and the grammar,
        that the PacketForecaster was initialized with.
        :param tree: The DerivationTree to base the prediction on.
        """
        history_nts = ""
        for r_msg in tree.protocol_msgs():
            assert isinstance(r_msg.msg.symbol, NonTerminal)
            history_nts += r_msg.msg.symbol.name()
        self._parser.detailed_tree = tree

        finder = PathFinder(self.grammar)
        options = ForecastingResult()
        if history_nts == "":
            options = options.union(finder.forecast())
        else:
            # Save messages from original session tree
            session_messages = MessageHolders(tree)
            self._parser.reference_tree = tree
            self._parser.parse_history(history_nts)
            for suggested_tree, is_complete in self._parser.tree_at(
                self._parser.consumed_length(), incomplete=True
            ):
                for orig_r_msg, r_msg in zip(
                    tree.protocol_msgs(), suggested_tree.protocol_msgs(), strict=False
                ):
                    assert isinstance(r_msg.msg.symbol, NonTerminal)
                    assert isinstance(orig_r_msg.msg.symbol, NonTerminal)
                    if (
                        r_msg.msg.symbol.name()[9:] != orig_r_msg.msg.symbol.name()[1:]
                        or r_msg.sender != orig_r_msg.sender
                        or r_msg.recipient != orig_r_msg.recipient
                    ):
                        break
                    r_msg.msg.symbol = orig_r_msg.msg.symbol
                else:
                    options = options.union(
                        finder.forecast(suggested_tree, session_messages)
                    )
                    if is_complete and finder.collapsed_tree is not None:
                        options.complete_trees.add(finder.collapsed_tree)

            # Restore messages from original session tree
            session_messages.hold_messages()
        return options
