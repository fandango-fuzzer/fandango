from __future__ import annotations

from copy import deepcopy
from typing import Optional
from fandango.errors import FandangoValueError
from fandango.io.navigation.grammarreducer import GrammarReducer
from fandango.io.navigation.packetiterativeparser import PacketIterativeParser
from fandango.io.navigation.visitor.continuing_nodevisitor import ContinuingNodeVisitor
from fandango.language.grammar import ParsingMode
from fandango.language.grammar.grammar import Grammar
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree
from fandango.language.tree_value import TreeValueType


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
        mounting_path = MountingPath(self.collapsed_tree, tuple(self.current_path))
        f_packet = ForcastingPacket(node)
        f_packet.add_path(mounting_path)
        self.result.add_packet(node.sender, f_packet)

    def find(self, tree: Optional[DerivationTree] = None) -> ForecastingResult:
        """
        Finds all possible protocol messages that can be mounted to the given DerivationTree.
        :param tree: The DerivationTree to base the search on. The DerivationTree must contain controlflow nodes
        as provided by the DerivationTree parser with the parsing option 'include_controlflow=True'
        """
        if tree is None:
            tree = DerivationTree(NonTerminal("<start>"))
        self.result = ForecastingResult()
        self.collapsed_tree = self.grammar.collapse(tree)
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

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        raise FandangoValueError(
            "PacketForecaster reached TerminalNode! This is a bug."
        )


class MountingPath:
    def __init__(
        self,
        tree: Optional[DerivationTree],
        controlflow_path: tuple[tuple[NonTerminal, bool], ...],
    ):
        """
        Represents a path in the given DerivationTree where a protocol message can be mounted.
        """
        self.tree = tree
        self.controlflow_path = controlflow_path
        self.path = MountingPath._collapsed_path(controlflow_path)

    @staticmethod
    def _collapsed_path(path: tuple[tuple[NonTerminal, bool], ...]):
        new_path = []
        for nt, new_node in path:
            if nt.is_type(TreeValueType.STRING) and str(nt.value()).startswith("<__"):
                continue
            elif nt.is_type(TreeValueType.BYTES) and bytes(nt.value()).startswith(
                b"<__"
            ):
                continue
            new_path.append((nt, new_node))
        return tuple(new_path)

    def __hash__(self):
        return hash((hash(self.tree), hash(self.path)))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return repr(self.path)


class ForcastingPacket:
    def __init__(self, node: NonTerminalNode):
        self.node = node
        self.paths: set[MountingPath] = set()

    def add_path(self, path: MountingPath) -> None:
        self.paths.add(path)


class ForcastingNonTerminals:
    def __init__(self):
        self.nt_to_packet = dict[NonTerminal, ForcastingPacket]()

    def get_non_terminals(self) -> set[NonTerminal]:
        return set(self.nt_to_packet.keys())

    def __getitem__(self, item: NonTerminal):
        return self.nt_to_packet[item]

    def add_packet(self, packet: ForcastingPacket) -> None:
        """
        Adds a packet to the ForcastingNonTerminals.
        """
        if packet.node.symbol in self.nt_to_packet.keys():
            for path in packet.paths:
                self.nt_to_packet[packet.node.symbol].add_path(path)
        else:
            self.nt_to_packet[packet.node.symbol] = packet


class ForecastingResult:
    def __init__(self):
        self.parties_to_packets = dict[str, ForcastingNonTerminals]()

    def get_msg_parties(self) -> set[str]:
        return set(self.parties_to_packets.keys())

    def contains_any_party(self, parties: list[str]):
        """
        Checks if the ForecastingResult contains any of the specified parties.
        :param parties: List of party names to check.
        :return: True if any party is found, False otherwise.
        """
        return any(party in self.parties_to_packets for party in parties)

    def __getitem__(self, item: str):
        return self.parties_to_packets[item]

    def __contains__(self, item: str) -> bool:
        return item in self.parties_to_packets

    def add_packet(self, party: Optional[str], packet: ForcastingPacket) -> None:
        """
        Adds a packet to the ForecastingResult under the specified party.
        """
        if party is None:
            raise FandangoValueError("Party cannot be None")
        if party not in self.parties_to_packets.keys():
            self.parties_to_packets[party] = ForcastingNonTerminals()
        self.parties_to_packets[party].add_packet(packet)

    def union(self, other: ForecastingResult) -> ForecastingResult:
        """
        Combines two ForecastingResults by adding all packets from the other result.
        Returns a copy of the current ForecastingResult with the combined packets.
        :param other: The other ForecastingResult to combine with.
        """
        c_new = deepcopy(self)
        c_other = deepcopy(other)
        for party, fnt in c_other.parties_to_packets.items():
            for fp in fnt.nt_to_packet.values():
                c_new.add_packet(party, fp)
        return c_new


class PacketForecaster:

    def __init__(self, grammar: Grammar):
        reduced_rules = GrammarReducer(grammar.grammar_settings).process(grammar.rules)
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
            options = options.union(finder.find())
        else:
            self._parser.reference_tree = tree
            self._parser.new_parse(NonTerminal("<start>"), ParsingMode.INCOMPLETE)
            for suggested_tree in self._parser.consume(history_nts):
                for orig_r_msg, r_msg in zip(
                    tree.protocol_msgs(), suggested_tree.protocol_msgs()
                ):
                    assert isinstance(r_msg.msg.symbol, NonTerminal)
                    assert isinstance(orig_r_msg.msg.symbol, NonTerminal)
                    if (
                        r_msg.msg.symbol.name()[9:] == orig_r_msg.msg.symbol.name()[1:]
                        and r_msg.sender == orig_r_msg.sender
                        and r_msg.recipient == orig_r_msg.recipient
                    ):
                        cpy = orig_r_msg.msg.deepcopy(copy_parent=False)
                        assert isinstance(cpy.symbol, NonTerminal)
                        r_msg.msg.set_children(cpy.children)
                        r_msg.msg.sources = deepcopy(cpy.sources)
                        r_msg.msg.symbol = NonTerminal("<" + cpy.symbol.name()[1:])
                    else:
                        break
                else:
                    options = options.union(finder.find(suggested_tree))
        return options
