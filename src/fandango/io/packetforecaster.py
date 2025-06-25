from copy import deepcopy
from typing import Optional

from fandango.errors import FandangoValueError
from fandango.language.grammar import (
    Grammar,
    NodeVisitor,
    NonTerminalNode,
    TerminalNode,
    ParseState,
    Column,
    Node,
    Concatenation,
    Alternative,
    Repetition,
    Option,
    Plus,
    Star,
    CharSet,
    GrammarKeyError,
    NodeType,
)
from fandango.language.symbol import Terminal, NonTerminal
from fandango.language.tree import DerivationTree


class PathFinder(NodeVisitor):
    """
    For a given grammar and DerivationTree, this class
    finds possible upcoming message types, the nonterminals that generate them and the paths where the messages
    can be added to the DerivationTree.
    """

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.tree: Optional[DerivationTree] = None
        self.collapsed_tree: Optional[DerivationTree] = None
        self.current_tree: list[list[DerivationTree] | None] = []
        self.current_path: list[tuple[NonTerminal, bool]] = []
        self.result = PacketForecaster.ForecastingResult()

    def add_option(self, node: NonTerminalNode) -> None:
        mounting_path = PacketForecaster.MountingPath(
            self.collapsed_tree, tuple(self._collapsed_path(self.current_path))
        )
        f_packet = PacketForecaster.ForcastingPacket(node)
        f_packet.add_path(mounting_path)
        self.result.add_packet(node.sender, f_packet)

    @staticmethod
    def _collapsed_path(path: list[tuple[NonTerminal, bool]]):
        new_path = []
        for nt, new_node in path:
            if isinstance(nt.symbol, str) and nt.symbol.startswith("<__"):
                continue
            elif isinstance(nt.symbol, bytes) and nt.symbol.startswith(b"<__"):
                continue
            new_path.append((nt, new_node))
        return tuple(new_path)

    def find(
        self, tree: Optional[DerivationTree] = None
    ) -> "PacketForecaster.ForecastingResult":
        """
        Finds all possible protocol messages that can be mounted to the given DerivationTree.
        :param tree: The DerivationTree to base the search on. The DerivationTree must contain controlflow nodes
        as provided by the DerivationTree parser with the parsing option 'include_controlflow=True'
        """
        if tree is None:
            self.tree = DerivationTree(NonTerminal("<start>"))
        else:
            self.tree = tree
        self.collapsed_tree = self.grammar.collapse(self.tree)
        self.current_path = []
        self.current_tree = []

        self.result = PacketForecaster.ForecastingResult()
        self.current_path.append((self.tree.nonterminal, False))
        if len(self.tree.children) == 0:
            self.current_tree = [None]
        else:
            self.current_tree = [[self.tree.children[0]]]

        self.visit(self.grammar.rules[self.current_path[-1][0]])
        self.current_tree.pop()
        self.current_path.pop()
        return self.result

    def on_enter_controlflow(self, expected_nt: str):
        tree = self.current_tree[-1]
        cf_nt = (NonTerminal(expected_nt), True)
        if tree is not None:
            if len(tree) != 1:
                raise GrammarKeyError(
                    "Expected len(tree) == 1 for controlflow entries!"
                )
            if str(tree[0].symbol) != expected_nt:
                raise GrammarKeyError("Symbol mismatch!")
            cf_nt = (NonTerminal(str(tree[0].symbol)), False)
        self.current_tree.append(None if tree is None else tree[0].children)
        self.current_path.append(cf_nt)

    def on_leave_controlflow(self):
        self.current_tree.pop()
        self.current_path.pop()

    def visitNonTerminalNode(self, node: NonTerminalNode):
        tree = self.current_tree[-1]
        if tree is not None:
            if tree[0].symbol != node.symbol:
                raise GrammarKeyError("Symbol mismatch")

        if node.sender is not None:
            if tree is None:
                self.add_option(node)
                return False
            else:
                return True
        self.current_tree.append(None if tree is None else tree[0].children)
        self.current_path.append((node.symbol, tree is None))
        try:
            result = self.visit(self.grammar.rules[node.symbol])
        finally:
            self.current_path.pop()
            self.current_tree.pop()
        return result

    def visitTerminalNode(self, node: TerminalNode):
        raise FandangoValueError(
            "PacketForecaster reached TerminalNode! This is a bug."
        )

    def visitConcatenation(self, node: Concatenation):
        self.on_enter_controlflow(f"<__{NodeType.CONCATENATION}:{node.id}>")
        tree = self.current_tree[-1]
        child_idx = 0 if tree is None else (len(tree) - 1)
        continue_exploring = True
        if tree is not None:
            self.current_tree.append([tree[child_idx]])
            try:
                if len(node.nodes) <= child_idx:
                    raise GrammarKeyError(
                        "Tree contains more children, then concatination node"
                    )
                continue_exploring = self.visit(node.nodes[child_idx])
                child_idx += 1
            finally:
                self.current_tree.pop()
        while continue_exploring and child_idx < len(node.children()):
            next_child = node.children()[child_idx]
            self.current_tree.append(None)
            continue_exploring = self.visit(next_child)
            self.current_tree.pop()
            child_idx += 1
        self.on_leave_controlflow()
        return continue_exploring

    def visitAlternative(self, node: Alternative):
        self.on_enter_controlflow(f"<__{NodeType.ALTERNATIVE}:{node.id}>")
        tree = self.current_tree[-1]

        if tree is not None:
            continue_exploring = True
            self.current_tree.append([tree[0]])
            fallback_tree = list(self.current_tree)
            fallback_path = list(self.current_path)
            found = False
            for alt in node.alternatives:
                try:
                    continue_exploring = self.visit(alt)
                    found = True
                    break
                except GrammarKeyError as e:
                    self.current_tree = fallback_tree
                    self.current_path = fallback_path
            self.current_tree.pop()
            self.on_leave_controlflow()
            if not found:
                raise GrammarKeyError("Alternative mismatch")
            return continue_exploring
        else:
            continue_exploring = False
            self.current_tree.append(None)
            for alt in node.alternatives:
                continue_exploring |= self.visit(alt)
            self.current_tree.pop()
            self.on_leave_controlflow()
            return continue_exploring

    def visitRepetition(self, node: Repetition):
        self.on_enter_controlflow(f"<__{NodeType.REPETITION}:{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitRepetitionType(self, node: Repetition):
        tree = self.current_tree[-1]
        continue_exploring = True
        tree_len = 0
        if tree is not None:
            tree_len = len(tree)
            self.current_tree.append([tree[-1]])
            continue_exploring = self.visit(node.node)
            self.current_tree.pop()

        rep_max = node.max(self.grammar, self.grammar.collapse(self.tree))
        if continue_exploring and tree_len < rep_max:
            self.current_tree.append(None)
            continue_exploring = self.visit(node.node)
            self.current_tree.pop()
            if continue_exploring:
                return continue_exploring
        if tree_len >= node.min(self.grammar, self.grammar.collapse(self.tree)):
            return True
        return continue_exploring

    def visitStar(self, node: Star):
        self.on_enter_controlflow(f"<__{NodeType.STAR}:{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitPlus(self, node: Plus):
        self.on_enter_controlflow(f"<__{NodeType.PLUS}:{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitOption(self, node: Option):
        self.on_enter_controlflow(f"<__{NodeType.OPTION}:{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret


class PacketForecaster:
    class MountingPath:
        def __init__(
            self,
            tree: Optional[DerivationTree],
            path: tuple[tuple[NonTerminal, bool], ...],
        ):
            """
            Represents a path in the given DerivationTree where a protocol message can be mounted.
            """
            self.tree = tree
            self.path = path

        def __hash__(self):
            return hash((hash(self.tree), hash(self.path)))

        def __eq__(self, other):
            return hash(self) == hash(other)

        def __repr__(self):
            return repr(self.path)

    class ForcastingPacket:
        def __init__(self, node: NonTerminalNode):
            self.node = node
            self.paths: set[PacketForecaster.MountingPath] = set()

        def add_path(self, path: "PacketForecaster.MountingPath") -> None:
            self.paths.add(path)

    class ForcastingNonTerminals:
        def __init__(self):
            self.nt_to_packet = dict[NonTerminal, PacketForecaster.ForcastingPacket]()

        def get_non_terminals(self) -> set[NonTerminal]:
            return set(self.nt_to_packet.keys())

        def __getitem__(self, item: NonTerminal):
            return self.nt_to_packet[item]

        def add_packet(self, packet: "PacketForecaster.ForcastingPacket") -> None:
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
            self.parties_to_packets = dict[
                str, PacketForecaster.ForcastingNonTerminals
            ]()

        def get_msg_parties(self) -> set[str]:
            return set(self.parties_to_packets.keys())

        def __getitem__(self, item: str):
            return self.parties_to_packets[item]

        def add_packet(
            self, party: Optional[str], packet: "PacketForecaster.ForcastingPacket"
        ) -> None:
            """
            Adds a packet to the ForecastingResult under the specified party.
            """
            if party is None:
                raise FandangoValueError("Party cannot be None")
            if party not in self.parties_to_packets.keys():
                self.parties_to_packets[party] = (
                    PacketForecaster.ForcastingNonTerminals()
                )
            self.parties_to_packets[party].add_packet(packet)

        def union(
            self, other: "PacketForecaster.ForecastingResult"
        ) -> "PacketForecaster.ForecastingResult":
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

    class GrammarReducer(NodeVisitor):
        """
        Converts a grammar into a reduced form, where all protocol message defining NonTerminalNodes are replaced with
        a TerminalNode that describes the protocol message type.
        Message defining NonTerminals are replaced with a Terminal, in the form of <_packet_<message_type>>.
        This allows the PacketForecaster to predict upcoming
        protocol messages without parsing each protocol message again.
        """

        def __init__(self):
            self._reduced = dict()
            self.seen_keys = set()
            self.processed_keys = set()

        def process(self, grammar: Grammar) -> dict[NonTerminal, Node]:
            """
            Applies the grammar reduction to the provided grammar.
            """
            self._reduced = dict()
            self.seen_keys = set()
            self.seen_keys.add(NonTerminal("<start>"))
            self.processed_keys = set()
            diff_keys = self.seen_keys - self.processed_keys
            while len(diff_keys) != 0:
                key = diff_keys.pop()
                self._reduced[key] = self.visit(grammar.rules[key])
                self.processed_keys.add(key)
                diff_keys = self.seen_keys - self.processed_keys
            return self._reduced

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.append(result)
            return aggregate

        def visitConcatenation(self, node: Concatenation):
            return Concatenation(self.visitChildren(node), node.id)

        def visitTerminalNode(self, node: TerminalNode):
            return TerminalNode(node.symbol)

        def visitAlternative(self, node: Alternative):
            return Alternative(self.visitChildren(node), node.id)

        def visitRepetition(self, node: Repetition):
            return Repetition(
                self.visit(node.node), node.id, node.expr_data_min, node.expr_data_max
            )

        def visitOption(self, node: Option):
            return Option(self.visit(node.node), node.id)

        def visitPlus(self, node: Plus):
            return Plus(self.visit(node.node), node.id, node.expr_data_max)

        def visitStar(self, node: Star):
            return Star(self.visit(node.node), node.id, node.expr_data_max)

        def visitCharSet(self, node: CharSet):
            return CharSet(node.chars)

        def visitNonTerminalNode(self, node: NonTerminalNode):
            if node.sender is None and node.recipient is None:
                self.seen_keys.add(node.symbol)
                return node

            if isinstance(node.symbol.symbol, str):
                symbol = NonTerminal("<_packet_" + node.symbol.symbol[1:])
            else:
                raise FandangoValueError("NonTerminal symbol must be a string!")
            repl_node = NonTerminalNode(symbol, node.sender, node.recipient)
            self._reduced[symbol] = TerminalNode(Terminal(node.symbol.symbol))
            self.seen_keys.add(symbol)
            self.processed_keys.add(symbol)
            return repl_node

    class Parser(Grammar.Parser):
        def __init__(self, grammar: Grammar):
            super().__init__(grammar)
            self.reference_tree: Optional[DerivationTree] = None
            self.detailed_tree: Optional[DerivationTree] = None

        def construct_incomplete_tree(
            self, state: ParseState, table: list[Column]
        ) -> DerivationTree:
            i_tree = super().construct_incomplete_tree(state, table)
            i_cpy = deepcopy(i_tree)
            if self.reference_tree is None:
                raise FandangoValueError(
                    "Reference tree must be set before constructing the incomplete tree!"
                )
            for i_msg, r_msg in zip(
                i_cpy.protocol_msgs(), self.reference_tree.protocol_msgs()
            ):
                i_msg.msg.set_children(r_msg.msg.children)
                i_msg.msg.sources = r_msg.msg.sources
                symbol = r_msg.msg.symbol.symbol
                if isinstance(symbol, str):
                    i_msg.msg.symbol = NonTerminal("<" + symbol[1:])
                else:
                    raise FandangoValueError("NonTerminal symbol must be a string!")
            return i_cpy

    def __init__(self, grammar: Grammar):
        g_globals, g_locals = grammar.get_spec_env()
        reduced = PacketForecaster.GrammarReducer().process(grammar)
        self.grammar = grammar
        self.reduced_grammar = Grammar(
            reduced, grammar.fuzzing_mode, g_locals, g_globals
        )
        self._parser = PacketForecaster.Parser(self.reduced_grammar)

    def predict(self, tree: DerivationTree) -> "ForecastingResult":
        """
        Predicts the next possible message types based on the provided tree and the grammar,
        that the PacketForecaster was initialized with.
        :param tree: The DerivationTree to base the prediction on.
        """
        history_nts = ""
        for r_msg in tree.protocol_msgs():
            history_nts += str(r_msg.msg.symbol)
        self._parser.detailed_tree = tree

        finder = PathFinder(self.grammar)
        options = PacketForecaster.ForecastingResult()
        if history_nts == "":
            options = options.union(finder.find())
        else:
            self._parser.reference_tree = tree
            for suggested_tree in self._parser.parse_multiple(
                history_nts,
                NonTerminal("<start>"),
                Grammar.Parser.ParsingMode.INCOMPLETE,
                include_controlflow=True,
            ):
                for orig_r_msg, r_msg in zip(
                    tree.protocol_msgs(), suggested_tree.protocol_msgs()
                ):
                    if (
                        str(r_msg.msg.symbol)[9:] == str(orig_r_msg.msg.symbol)[1:]
                        and r_msg.sender == orig_r_msg.sender
                        and r_msg.recipient == orig_r_msg.recipient
                    ):
                        cpy = orig_r_msg.msg.deepcopy(copy_parent=False)
                        r_msg.msg.set_children(cpy.children)
                        r_msg.msg.sources = deepcopy(cpy.sources)
                        r_msg.msg.symbol = NonTerminal("<" + str(cpy.symbol)[1:])
                    else:
                        break
                else:
                    options = options.union(finder.find(suggested_tree))
        return options
