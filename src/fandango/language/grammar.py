import abc
import copy
import enum
import random
import typing
from copy import deepcopy
from typing import Dict, List, Optional, Tuple, Set, Any, Union, Iterator, overload

from fandango.language.symbol import NonTerminal, Terminal, Symbol
from fandango.language.tree import DerivationTree, RoledMessage
from fandango.logger import LOGGER

MAX_REPETITIONS = 5


class NodeType(enum.Enum):
    ALTERNATIVE = "alternative"
    CONCATENATION = "concatenation"
    REPETITION = "repetition"
    STAR = "star"
    PLUS = "plus"
    OPTION = "option"
    NON_TERMINAL = "non_terminal"
    TERMINAL = "terminal"
    CHAR_SET = "char_set"

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class FuzzingMode(enum.Enum):
    COMPLETE = 0
    IO = 1


class GrammarKeyError(KeyError):
    pass


class Node(abc.ABC):
    def __init__(
        self, node_type: NodeType, distance_to_completion: float = float("inf")
    ):
        self.node_type = node_type
        self.distance_to_completion = distance_to_completion

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        return []

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

    def tree_roles(self, grammar: "Grammar", include_recipients: bool = True):
        return self._tree_roles(grammar, set(), include_recipients)

    def _tree_roles(self, grammar: "Grammar", seen_nonterminals: set[NonTerminal], include_recipients: bool):
        roles = set()
        for child in self.children():
            roles = roles.union(child._tree_roles(grammar, seen_nonterminals, include_recipients))
        return roles

    def children(self):
        return []

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        """
        Returns an iterator of the descendents of this node.

        :param rules: The rules upon which to base non-terminal lookups.
        :return An iterator over the descendent nodes.
        """
        yield from ()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        super().__init__(NodeType.ALTERNATIVE)
        self.alternatives = alternatives

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        if self.distance_to_completion >= max_nodes:
            min_ = min(self.alternatives, key=lambda x: x.distance_to_completion)
            return random.choice(
                [
                    a
                    for a in self.alternatives
                    if a.distance_to_completion <= min_.distance_to_completion
                ]
            ).fuzz(grammar, 0, in_role)
        return random.choice(self.alternatives).fuzz(grammar, max_nodes - 1, in_role)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitAlternative(self)

    def children(self):
        return self.alternatives

    def __getitem__(self, item):
        return self.alternatives.__getitem__(item)

    def __len__(self):
        return len(self.alternatives)

    def __repr__(self):
        return "(" + " | ".join(map(repr, self.alternatives)) + ")"

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield from self.alternatives


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        super().__init__(NodeType.CONCATENATION)
        self.nodes = nodes

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        trees = []
        for idx, node in enumerate(self.nodes):
            if node.distance_to_completion >= max_nodes:
                tree = node.fuzz(grammar, 0, in_role)
            else:
                tree = node.fuzz(grammar, max_nodes - 1, in_role)
            trees.extend(tree)
            max_nodes -= sum(t.size() for t in tree)
        return trees

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitConcatenation(self)

    def children(self):
        return self.nodes

    def __getitem__(self, item):
        return self.nodes.__getitem__(item)

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return " ".join(map(repr, self.nodes))

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield from self.nodes


class Repetition(Node):
    # TODO: Shouldn't a children() method return [self.node]? -- AZ
    def __init__(self, node: Node, min_: int = 0, max_: int = MAX_REPETITIONS):
        super().__init__(NodeType.REPETITION)
        if min_ < 0:
            raise ValueError(
                f"Minimum repetitions {min_} must be greater than or equal to 0"
            )
        if max_ <= 0 or max_ < min_:
            raise ValueError(
                f"Maximum repetitions {max_} must be greater than 0 or greater than min {min_}"
            )
        self.node = node
        self.min = min_
        self.max = max_

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitRepetition(self)

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        repetitions = random.randint(self.min, self.max)
        trees = []
        for rep in range(repetitions):
            if self.node.distance_to_completion >= max_nodes:
                if rep > self.min:
                    break
                tree = self.node.fuzz(grammar, 0, in_role)
            else:
                tree = self.node.fuzz(grammar, max_nodes - 1, in_role)
            trees.extend(tree)
            max_nodes -= sum(t.size() for t in tree)
        return trees

    def __repr__(self):
        if self.min == self.max:
            return f"{self.node}{{{self.min}}}"
        return f"{self.node}{{{self.min},{self.max}}}"

    def children(self):
        return [self.node]

    def descendents(self, rules: Dict[NonTerminal, "Node"] | None) -> Iterator["Node"]:
        base = []
        if self.min == 0:
            base.append(TerminalNode(Terminal("")))
        if self.min <= 1 <= self.max:
            base.append(self.node)
        yield Alternative(
            base
            + [
                Concatenation([self.node] * r)
                for r in range(max(2, self.min), self.max + 1)
            ]
        )


class Star(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 0)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitStar(self)

    def __repr__(self):
        return f"{self.node}*"


class Plus(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitPlus(self)

    def __repr__(self):
        return f"{self.node}+"


class Option(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 0, 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitOption(self)

    def __repr__(self):
        return f"{self.node}?"

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield from (self.node, TerminalNode(Terminal("")))


class NonTerminalNode(Node):
    def __init__(self, symbol: NonTerminal, role: str = None, recipient: str = None):
        super().__init__(NodeType.NON_TERMINAL)
        self.symbol = symbol
        self.role = role
        self.recipient = recipient

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        if self.symbol not in grammar:
            raise ValueError(f"Symbol {self.symbol} not found in grammar")

        if self.symbol in grammar.generators:
            return [grammar.generate(self.symbol)]

        assign_role = None
        assign_recipient = None
        if in_role is None:
            assign_role = self.role
            assign_recipient = self.recipient
            in_role = self.role

        children = grammar[self.symbol].fuzz(grammar, max_nodes - 1, in_role)

        tree = DerivationTree(self.symbol, children, role=assign_role, recipient=assign_recipient, read_only=False)
        return [tree]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):

        if self.role is not None:
            if self.recipient is None:
                return f"<{self.role}:{self.symbol.__repr__()[1:-1]}>"
            else:
                return f"<{self.role}:{self.recipient}:{self.symbol.__repr__()[1:-1]}>"
        else:
            return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def _tree_roles(self, grammar: "Grammar", seen_nonterminals: set[NonTerminal], include_recipients: bool):
        roles = set()
        if self.role is not None:
            roles.add(self.role)
            if self.recipient is not None and include_recipients:
                roles.add(self.recipient)
        if self.symbol not in seen_nonterminals:
            seen_nonterminals.add(self.symbol)
            for role in grammar[self.symbol]._tree_roles(grammar, seen_nonterminals, include_recipients):
                roles.add(role)
        return roles

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        yield rules[self.symbol]


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        super().__init__(NodeType.TERMINAL, 0)
        self.symbol = symbol

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:

        return [DerivationTree(self.symbol)]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class CharSet(Node):
    def __init__(self, chars: str):
        super().__init__(NodeType.CHAR_SET, 0)
        self.chars = chars

    def fuzz(
        self, grammar: "Grammar", max_nodes: int = 100, in_role: str = None
    ) -> List[DerivationTree]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)

    def descendents(self, rules: Dict[NonTerminal, "Node"]) -> Iterator["Node"]:
        for char in self.chars:
            yield TerminalNode(Terminal(char))


class NodeVisitor(abc.ABC):
    def visit(self, node: Node):
        return node.accept(self)

    def default_result(self):
        pass

    def aggregate_results(self, aggregate, result):
        pass

    def visitChildren(self, node: Node) -> Any:
        # noinspection PyNoneFunctionAssignment
        result = self.default_result()
        for child in node.children():
            # noinspection PyNoneFunctionAssignment
            result = self.aggregate_results(result, self.visit(child))
        return result

    def visitAlternative(self, node: Alternative):
        return self.visitChildren(node)

    def visitConcatenation(self, node: Concatenation):
        return self.visitChildren(node)

    def visitRepetition(self, node: Repetition):
        return self.visit(node.node)

    def visitStar(self, node: Star):
        return self.visit(node.node)

    def visitPlus(self, node: Plus):
        return self.visit(node.node)

    def visitOption(self, node: Option):
        return self.visit(node.node)

    # noinspection PyUnusedLocal
    def visitNonTerminalNode(self, node: NonTerminalNode):
        return self.default_result()

    # noinspection PyUnusedLocal
    def visitTerminalNode(self, node: TerminalNode):
        return self.default_result()

    # noinspection PyUnusedLocal
    def visitCharSet(self, node: CharSet):
        return self.default_result()


class Disambiguator(NodeVisitor):
    def __init__(self):
        self.known_disambiguations = {}

    def visit(
        self, node: Node
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        if node in self.known_disambiguations:
            return self.known_disambiguations[node]
        result = super().visit(node)
        self.known_disambiguations[node] = result
        return result

    def visitAlternative(
        self, node: Alternative
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {}
        for child in node.children():
            endpoints: Dict[
                Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]
            ] = self.visit(child)
            for children in endpoints:
                # prepend the alternative to all paths
                if children not in child_endpoints:
                    child_endpoints[children] = []
                # join observed paths (these are impossible to disambiguate)
                child_endpoints[children].extend(
                    (node,) + path for path in endpoints[children]
                )

        return child_endpoints

    def visitConcatenation(
        self, node: Concatenation
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        child_endpoints = {(): []}
        for child in node.children():
            next_endpoints = {}
            endpoints: Dict[
                Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]
            ] = self.visit(child)
            for children in endpoints:
                for existing in child_endpoints:
                    concatenation = existing + children
                    if concatenation not in next_endpoints:
                        next_endpoints[concatenation] = []
                    next_endpoints[concatenation].extend(child_endpoints[existing])
                    next_endpoints[concatenation].extend(endpoints[children])
            child_endpoints = next_endpoints

        return {
            children: [(node,) + path for path in child_endpoints[children]]
            for children in child_endpoints
        }

    def visitRepetition(
        self, node: Repetition
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        # repetitions are alternatives over concatenations
        implicit_alternative = next(node.descendents(None))
        return self.visit(implicit_alternative)

    def visitStar(
        self, node: Star
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitPlus(
        self, node: Plus
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitOption(
        self, node: Option
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        implicit_alternative = Alternative(
            [Concatenation([]), Concatenation([node.node])]
        )
        return self.visit(implicit_alternative)

    def visitNonTerminalNode(
        self, node: NonTerminalNode
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitTerminalNode(
        self, node: TerminalNode
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitCharSet(
        self, node: CharSet
    ) -> Dict[Tuple[Union[NonTerminal, Terminal], ...], List[Tuple[Node, ...]]]:
        return {(Terminal(c),): [(node, TerminalNode(Terminal(c)))] for c in node.chars}


class NonTerminalFinder(NodeVisitor):

    def __init__(self, grammar: "Grammar"):
        self.grammar = grammar

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.extend(result)
        return aggregate

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol.is_implicit:
            return self.visit(self.grammar.rules[node.symbol]) + [node]
        return [node]


class PacketForecaster(NodeVisitor):

    class MountingPath:
        def __init__(self, tree: DerivationTree, path: Tuple[NonTerminal, ...]):
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

        def add_path(self, path: "PacketForecaster.MountingPath"):
            self.paths.add(path)

    class ForcastingNonTerminals:
        def __init__(self):
            self.nt_to_packet = dict[NonTerminal, PacketForecaster.ForcastingPacket]()

        def getNonTerminals(self) -> set[NonTerminal]:
            return set(self.nt_to_packet.keys())

        def __getitem__(self, item: NonTerminal):
            return self.nt_to_packet[item]

        def add_packet(self, packet: "PacketForecaster.ForcastingPacket"):
            if packet.node.symbol in self.nt_to_packet.keys():
                for path in packet.paths:
                    self.nt_to_packet[packet.node.symbol].add_path(path)
            else:
                self.nt_to_packet[packet.node.symbol] = packet

    class ForcastingResult:
        def __init__(self):
            # dict[roleName, dict[packetName, PacketForecaster.ForcastingPacket]]
            self.roles_to_packets = dict[str, PacketForecaster.ForcastingNonTerminals]()

        def getRoles(self) -> set[str]:
            return set(self.roles_to_packets.keys())

        def __getitem__(self, item: str):
            return self.roles_to_packets[item]

        def add_packet(self, role: str, packet: "PacketForecaster.ForcastingPacket"):
            if role not in self.roles_to_packets.keys():
                self.roles_to_packets[role] = PacketForecaster.ForcastingNonTerminals()
            self.roles_to_packets[role].add_packet(packet)

        def merge(self, other: "PacketForecaster.ForcastingResult"):
            c_new = copy.deepcopy(self)
            c_other = copy.deepcopy(other)
            for role, fnt in c_other.roles_to_packets.items():
                for fp in fnt.nt_to_packet.values():
                    c_new.add_packet(role, fp)
            return c_new

    def __init__(self, grammar: "Grammar", tree: DerivationTree | None = None):
        self.grammar = grammar
        self.tree = tree
        self.current_tree: list[list[DerivationTree] | None] = []
        self.current_path: list[NonTerminal] = []
        self.result = PacketForecaster.ForcastingResult()

    def add_option(self, node: NonTerminalNode):
        mounting_path = PacketForecaster.MountingPath(
            self.tree, tuple(self.current_path)
        )
        f_packet = PacketForecaster.ForcastingPacket(node)
        f_packet.add_path(mounting_path)
        self.result.add_packet(node.role, f_packet)

    def find(self):
        self.result = PacketForecaster.ForcastingResult()
        if self.tree is not None:
            self.current_path.append(self.tree.symbol)
            if len(self.tree.children) == 0:
                self.current_tree = [None]
            else:
                self.current_tree = [[self.tree.children[0]]]
        else:
            self.current_path.append(NonTerminal("<start>"))
            self.current_tree = [None]

        self.visit(self.grammar.rules[self.current_path[-1]])
        self.current_tree.pop()
        self.current_path.pop()
        return self.result

    def visitNonTerminalNode(self, node: NonTerminalNode):
        tree = self.current_tree[-1]
        if tree is not None:
            if tree[0].symbol != node.symbol:
                raise GrammarKeyError("Symbol mismatch")

        if node.role is not None:
            if tree is None:
                self.add_option(node)
                return False
            else:
                return True
        self.current_tree.append(None if tree is None else tree[0].children)
        self.current_path.append(node.symbol)
        try:
            result = self.visit(self.grammar.rules[node.symbol])
        finally:
            self.current_path.pop()
            self.current_tree.pop()
        return result

    def visitConcatenation(self, node: Concatenation):
        tree = self.current_tree[-1]
        child_idx = 0 if tree is None else (len(tree) - 1)
        continue_exploring = True
        if tree is not None:
            self.current_tree.append([tree[child_idx]])
            try:
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
        return continue_exploring

    def visitAlternative(self, node: Alternative):
        tree = self.current_tree[-1]
        continue_exploring = True

        if tree is not None:
            self.current_tree.append([tree[0]])
            found = False
            for alt in node.alternatives:
                try:
                    continue_exploring = self.visit(alt)
                    found = True
                    break
                except GrammarKeyError as e:
                    pass
            self.current_tree.pop()
            if not found:
                raise GrammarKeyError("Alternative mismatch")
            return continue_exploring
        else:
            self.current_tree.append(None)
            for alt in node.alternatives:
                continue_exploring |= not self.visit(alt)
            self.current_tree.pop()
            return continue_exploring

    def visitRepetition(self, node: Repetition):
        tree = self.current_tree[-1]
        continue_exploring = True
        tree_len = 0
        if tree is not None:
            tree_len = len(tree)
            self.current_tree.append([tree[-1]])
            continue_exploring = self.visit(node.node)
            self.current_tree.pop()

        if continue_exploring and tree_len < node.max:
            self.current_tree.append(None)
            continue_exploring = self.visit(node.node)
            self.current_tree.pop()
            if continue_exploring:
                return continue_exploring
        if tree_len >= node.min:
            return True
        return continue_exploring

    def visitStar(self, node: Star):
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)


class RoleAssigner:

    def __init__(
        self, implicite_role: str, grammar: "Grammar", processed_non_terminals: set[str]
    ):
        self.grammar = grammar
        self.seen_non_terminals = set()
        self.processed_non_terminals = set(processed_non_terminals)
        self.implicite_role = implicite_role

    def run(self, node: Node):
        non_terminals: list[NonTerminalNode] = NonTerminalFinder(self.grammar).visit(
            node
        )
        unprocessed_non_terminals = []
        for nt in non_terminals:
            if nt not in self.processed_non_terminals:
                unprocessed_non_terminals.append(nt)
        if node in unprocessed_non_terminals and not isinstance(node, NonTerminalNode):
            unprocessed_non_terminals.remove(node)
        child_roles = set()

        for c_node in unprocessed_non_terminals:
            child_roles = child_roles.union(c_node.tree_roles(self.grammar, False))

        if len(child_roles) == 0:
            return
        for c_node in unprocessed_non_terminals:
            if c_node.symbol.is_implicit:
                continue
            self.seen_non_terminals.add(c_node.symbol)
            if len(c_node.tree_roles(self.grammar, False)) != 0:
                continue
            c_node.role = self.implicite_role


class GrammarTruncator(NodeVisitor):
    def __init__(self, grammar: "Grammar", keep_roles: set[str]):
        self.grammar = grammar
        self.keep_roles = keep_roles

    def visitStar(self, node: Star):
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus):
        return self.visitRepetition(node)

    def visitOption(self, node: Option):
        return self.visitRepetition(node)

    def visitAlternative(self, node: Alternative):
        for child in list(node.children()):
            if self.visit(child):
                node.alternatives.remove(child)
        if len(node.alternatives) == 0:
            return True
        return False

    def visitRepetition(self, node: Repetition):
        for child in list(node.children()):
            if self.visit(child):
                return True
        return False

    def visitConcatenation(self, node: Concatenation):
        for child in list(node.children()):
            if self.visit(child):
                node.nodes.remove(child)
        if len(node.nodes) == 0:
            return True
        return False

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol.is_implicit:
            return self.visit(self.grammar[node.symbol])
        if node.role is None and node.recipient is None:
            return False
        truncatable = True
        if node.role is not None and node.role in self.keep_roles:
            truncatable = False
        if node.recipient is not None and node.recipient in self.keep_roles:
            truncatable = False
        return truncatable

    def visitTerminalNode(self, node: TerminalNode):
        return False


class RoleNestingDetector(NodeVisitor):
    def __init__(self, grammar: "Grammar"):
        self.grammar = grammar
        self.seen_nt = set()
        self.current_path = list()

    def fail_on_nested_packet(self, start_symbol: NonTerminal):
        self.current_nt = start_symbol
        self.visit(self.grammar[start_symbol])

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol.is_implicit:
            return self.visit(self.grammar[node.symbol])

        self.current_path.append(node.symbol)
        if node.symbol not in self.seen_nt:
            self.seen_nt.add(node.symbol)
        elif node.role is not None and node.symbol in self.current_path:
            str_path = [str(p) for p in self.current_path]
            raise RuntimeError(
                f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}! DerivationPath: " + " -> ".join(str_path))
        else:
            return

        if node.role is not None:
            tree_roles = self.grammar[node.symbol].tree_roles(self.grammar, False)
            if len(tree_roles) != 0:
                raise RuntimeError(f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}: " + ", ".join(tree_roles))
            return

        self.visit(self.grammar[node.symbol])
        self.current_path.pop()



class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: Tuple[Symbol, ...],
        dot: int = 0,
        children: Optional[List[DerivationTree]] = None,
        is_incomplete: bool = False,
    ):
        self.nonterminal = nonterminal
        self.position = position
        self.symbols = symbols
        self._dot = dot
        self.children = children or []
        self.is_incomplete = is_incomplete

    @property
    def dot(self):
        return self.symbols[self._dot] if self._dot < len(self.symbols) else None

    def finished(self):
        return self._dot >= len(self.symbols) and not self.is_incomplete

    def next_symbol_is_nonterminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot].is_non_terminal

    def next_symbol_is_terminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot].is_terminal

    def __hash__(self):
        return hash((self.nonterminal, self.position, self.symbols, self._dot))

    def __eq__(self, other):
        return (
            isinstance(other, ParseState)
            and self.nonterminal == other.nonterminal
            and self.position == other.position
            and self.symbols == other.symbols
            and self._dot == other._dot
        )

    def __repr__(self):
        return (
            f"({self.nonterminal} -> "
            + "".join(
                [
                    f"{'•' if i == self._dot else ''}{s.symbol}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("•" if self.finished() else "")
            + f", position {self.position}"
            + ")"
        )

    def next(self, position: Optional[int] = None):
        return ParseState(
            self.nonterminal,
            position or self.position,
            self.symbols,
            self._dot + 1,
            self.children[:],
        )


class Column:
    def __init__(self, states: Optional[List[ParseState]] = None):
        self.states = states or []
        self.unique = set(self.states)

    def __iter__(self):
        index = 0
        while index < len(self.states):
            yield self.states[index]
            index += 1

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item):
        return self.states[item]

    def __setitem__(self, key, value):
        self.states[key] = value

    def __delitem__(self, key):
        del self.states[key]

    def __contains__(self, item):
        return item in self.unique

    def add(self, state: ParseState):
        if state not in self.unique:
            self.states.append(state)
            self.unique.add(state)
            return True
        return False

    def update(self, states: Set[ParseState]):
        for state in states:
            self.add(state)

    def __repr__(self):
        return f"Column({self.states})"


class Grammar(NodeVisitor):
    class Parser(NodeVisitor):
        def __init__(
            self,
            rules: Dict[NonTerminal, Node],
        ):
            self.grammar_rules = rules
            self._rules = {}
            self._implicit_rules = {}
            self._process()
            self._cache: Dict[Tuple[str, NonTerminal], DerivationTree, bool] = {}
            self._incomplete = set()
            self._max_position = -1

        def _process(self):
            for nonterminal in self.grammar_rules:
                self._rules[nonterminal] = {
                    tuple(a) for a in self.visit(self.grammar_rules[nonterminal])
                }
            for nonterminal in self._implicit_rules:
                self._implicit_rules[nonterminal] = {
                    tuple(a) for a in self._implicit_rules[nonterminal]
                }

        def get_new_name(self):
            return NonTerminal(f"<*{len(self._implicit_rules)}*>")

        def set_implicit_rule(self, rule: List[List[Node]]) -> NonTerminalNode:
            nonterminal = self.get_new_name()
            self._implicit_rules[nonterminal] = rule
            return nonterminal

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.extend(result)
            return aggregate

        def visitConcatenation(self, node: Concatenation):
            result = [[]]
            for child in node.children():
                to_add = self.visit(child)
                new_result = []
                for r in result:
                    for a in to_add:
                        new_result.append(r + a)
                result = new_result
            return result

        def visitRepetition(self, node: Repetition):
            alternatives = self.visit(node.node)
            nt = self.set_implicit_rule(alternatives)
            prev = None
            for rep in range(node.min, node.max):
                alts = [[nt]]
                if prev is not None:
                    alts.append([nt, prev])
                prev = self.set_implicit_rule(alts)
            alts = [node.min * [nt]]
            if prev is not None:
                alts.append(node.min * [nt] + [prev])
            min_nt = self.set_implicit_rule(alts)
            return [[min_nt]]

        def visitStar(self, node: Star):
            alternatives = [[]]
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r + [nt])
            return [[nt]]

        def visitPlus(self, node: Plus):
            alternatives = []
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r)
                alternatives.append(r + [nt])
            return [[nt]]

        def visitOption(self, node: Option):
            return [[Terminal("")]] + self.visit(node.node)

        def visitNonTerminalNode(self, node: NonTerminalNode):
            return [[node.symbol]]

        def visitTerminalNode(self, node: TerminalNode):
            return [[node.symbol]]

        def predict(
            self, state: ParseState, table: List[Set[ParseState] | Column], k: int
        ):
            if state.dot in self._rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)
                        for rule in self._rules[state.dot]
                    }
                )
            elif state.dot in self._implicit_rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)
                        for rule in self._implicit_rules[state.dot]
                    }
                )

        def scan_bit(
            self,
            state: ParseState,
            word: str | bytes,
            table: List[Set[ParseState] | Column],
            k: int,
            w: int,
            bit_count: int,
        ) -> bool:
            """
            Scan a bit from the input `word`.
            `table` is the parse table (may be modified by this function).
            `table[k]` is the current column.
            `word[w]` is the current byte.
            `bit_count` is the current bit position (7-0).
            Return True if a bit was matched, False otherwise.
            """
            # LOGGER.debug(f"Trying {state} at {word[w:]!r}"
            #              + (f", bit {bit_count}" if bit_count >= 0 else ""))

            assert isinstance(state.dot.symbol, int)
            assert 0 <= bit_count <= 7

            # Get the highest bit. If `word` is bytes, word[w] is an integer.
            byte = ord(word[w]) if isinstance(word, str) else word[w]
            bit = (byte >> bit_count) & 1
            # LOGGER.debug(f"Bit {bit_count} has a value of {bit}")

            # LOGGER.debug(f"Found bit {bit_count}: {bit}")
            # LOGGER.debug(f"Compare against bit {state.dot!r}")
            if not state.dot.check(bit):
                # LOGGER.debug(f"Bit match failed")
                return False

            # Found a match
            # LOGGER.debug(f"Scanned bit {bit_count} ({bit}) {state} {word[w:]!r}")
            next_state = state.next()
            next_state.children.append(DerivationTree(state.dot))

            # Insert a new table entry with next state
            # This is necessary, as our initial table holds one entry
            # per input byte, yet needs to be expanded to hold the bits, too.
            table.insert(k + 1, Column())
            table[k + 1].add(next_state)

            # Save the maximum position reached, so we can report errors
            self._max_position = max(self._max_position, w)

            return True

        def scan_byte(
            self,
            state: ParseState,
            word: str | bytes,
            table: List[Set[ParseState] | Column],
            k: int,
            w: int,
        ) -> bool:
            """
            Scan a byte from the input `word`.
            `state` is the current parse state.
            `table` is the parse table.
            `table[k]` is the current column.
            `word[w]` is the current byte.
            Return True if a byte was matched, False otherwise.
            """

            # LOGGER.debug(f"Trying {state} at {word[w:]!r}"
            #              + (f", bit {bit_count}" if bit_count >= 0 else ""))

            assert not isinstance(state.dot.symbol, int)

            if not state.dot.check(word[w:]):
                # No match
                return False

            # Found a match
            # LOGGER.debug(f"Scanned byte {state} {word[w:]!r}")
            next_state = state.next()
            next_state.children.append(DerivationTree(state.dot))
            table[k + len(state.dot)].add(next_state)
            self._max_position = max(self._max_position, w)
            return True

        def complete(
            self,
            state: ParseState,
            table: List[Set[ParseState] | Column],
            k: int,
            use_implicit: bool = False,
        ):
            for s in list(table[state.position]):
                if s.dot == state.nonterminal:
                    s = s.next()
                    table[k].add(s)
                    if state.nonterminal in self._rules:
                        s.children.append(
                            DerivationTree(state.nonterminal, state.children)
                        )
                    else:
                        if use_implicit and state.nonterminal in self._implicit_rules:
                            s.children.append(
                                DerivationTree(
                                    NonTerminal(state.nonterminal.symbol), state.children
                                )
                            )
                        else:
                            s.children.extend(state.children)

        # Commented this out, as
        # (a) it is not adapted to bits yet, and (b) not used -- AZ
        #
        # def parse_table(self, word, start: str | NonTerminal = "<start>"):
        #     if isinstance(start, str):
        #         start = NonTerminal(start)
        #     table = [Column() for _ in range(len(word) + 1)]
        #     table[0].add(ParseState(NonTerminal("<*start*>"), 0, (start,)))
        #     self._max_position = -1
        #
        #     for k in range(len(word) + 1):
        #         for state in table[k]:
        #             if state.finished():
        #                 self.complete(state, table, k)
        #             else:
        #                 if state.next_symbol_is_nonterminal():
        #                     self.predict(state, table, k)
        #                 else:
        #                     # No bit parsing support yet
        #                     self.scan_byte(state, word, table, k, k)
        #     return table

        def _parse_forest(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
            *,
            allow_incomplete: bool = False,
        ):
            """
            Parse a forest of input trees from `word`.
            `start` is the start symbol (default: `<start>`).
            if `allow_incomplete` is True, the function will return trees even if the input ends prematurely.
            """

            if isinstance(start, str):
                start = NonTerminal(start)

            # Initialize the table
            table: list[set[ParseState] | Column] = [
                Column() for _ in range(len(word) + 1)
            ]
            implicit_start = NonTerminal("<*start*>")
            table[0].add(ParseState(implicit_start, 0, (start,)))

            # Save the maximum scan position, so we can report errors
            self._max_position = -1

            k = 0  # Index into the current table. Due to bits parsing, this may differ from the input position w.
            w = 0  # Index into the input word
            bit_count = -1  # If > 0, indicates the next bit to be scanned (7-0)

            while k < len(table) and w <= len(word):
                advance = 0
                for state in table[k]:
                    # LOGGER.debug(f"Processing {state} at {word[w:]!r}")
                    if w >= len(word):
                        # LOGGER.debug(f"End of input")
                        if allow_incomplete:
                            if state.nonterminal == implicit_start:
                                self._incomplete.update(state.children)
                            state.is_incomplete = True
                            self.complete(state, table, k)

                    if state.finished():
                        # LOGGER.debug(f"Finished {state}")
                        if state.nonterminal == implicit_start and w >= len(word):
                            for child in state.children:
                                yield child

                        self.complete(state, table, k)
                    elif not state.is_incomplete:
                        if state.next_symbol_is_nonterminal():
                            # LOGGER.debug(f"Predicting")
                            self.predict(state, table, k)
                        else:
                            # LOGGER.debug(f"Scanning")
                            if isinstance(state.dot.symbol, int):
                                # Scan a bit
                                if bit_count < 0:
                                    bit_count = 7
                                self.scan_bit(state, word, table, k, w, bit_count)
                                adv = 1
                            else:
                                # Scan a byte
                                if bit_count >= 0:
                                    # We are still expecting bits here:
                                    #
                                    # * we may have _peeked_ at a bit,
                                    # without actually parsing it; or
                                    # * we may have a grammar with bits
                                    # that do not come in multiples of 8.
                                    #
                                    # In either case, we need to skip back
                                    # to scanning bytes here.
                                    LOGGER.debug("Mixed parsing of bits and bytes")
                                    bit_count = -1
                                self.scan_byte(state, word, table, k, w)
                                adv = 8
                            advance = max(advance, adv)

                # LOGGER.debug(f"Advancing by {advance} bits")
                if advance == 1:
                    # Advance by one bit
                    bit_count -= 1
                if advance == 8 or bit_count < 0:
                    # Advance by one byte
                    w += 1

                # LOGGER.debug(f"w = {w}, bit_count = {bit_count}")

                k += 1

        def parse_forest(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
            *,
            allow_incomplete: bool = False,
        ):
            """
            Yield multiple parse alternatives, using a cache.
            """
            if isinstance(start, str):
                start = NonTerminal(start)

            cache_key = (word, start, allow_incomplete)
            if cache_key in self._cache:
                forest = self._cache[cache_key]
                for tree in forest:
                    yield deepcopy(tree)
                return

            self._incomplete = set()
            forest = []
            for tree in self._parse_forest(
                word, start, allow_incomplete=allow_incomplete
            ):
                forest.append(tree)
                yield tree

            if allow_incomplete:
                for tree in self._incomplete:
                    forest.append(tree)
                    yield tree

            # Cache entire forest
            self._cache[cache_key] = forest

        def parse_incomplete(self, word: str, start: str | NonTerminal = "<start>"):
            """
            Yield multiple parse alternatives,
            even for incomplete inputs
            """
            return self.parse_forest(word, start, allow_incomplete=True)

        def parse(self, word: str, start: str | NonTerminal = "<start>"):
            """
            Return the first parse alternative,
            or `None` if no parse is possible
            """
            tree_gen = self.parse_forest(word, start=start)
            return next(tree_gen, None)

        def max_position(self):
            """Return the maximum position reached during parsing."""
            return self._max_position

    def __init__(
        self,
        rules: Optional[Dict[NonTerminal, Node]] = None,
        fuzzing_mode: Optional[FuzzingMode] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.rules = rules or {}
        self.generators = {}
        self.fuzzing_mode = FuzzingMode.COMPLETE
        self._parser = Grammar.Parser(self.rules)
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._visited = set()

    def generate_string(self, symbol: str | NonTerminal = "<start>") -> str | Tuple:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return eval(
            self.generators[symbol], self._global_variables, self._local_variables
        )

    def generate(self, symbol: str | NonTerminal = "<start>") -> DerivationTree:
        string = self.generate_string(symbol)
        if not (isinstance(string, str) or isinstance(string, tuple)):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string or tuple"
            )

        if isinstance(string, tuple):
            return DerivationTree.from_sub_tree(string)
        else:
            tree = self.parse(string, symbol)
        if tree is None:
            raise ValueError(
                f"Failed to parse generated string: {string} for {symbol} with generator {self.generators[symbol]}"
            )
        return tree

    def assign_roles(
        self,
        tree: DerivationTree,
        roles: list[RoledMessage],
        parent_symbol=NonTerminal("<start>"),
    ):
        return self._assign_roles(tree, list(roles), parent_symbol)

    def _assign_roles(
        self, tree: DerivationTree, roles: list[RoledMessage], parent_symbol
    ):
        if len(roles) == 0:
            return True
        first = roles[0]
        current_str = str(tree)
        if not current_str.startswith(str(first.msg)):
            return False
        if current_str == str(first.msg):
            if parent_symbol in self.rules:
                nodes = []
                rule = self.rules[parent_symbol]
                nodes.append(rule)
                nodes.extend(rule.children())
                nodes = list(filter(lambda x: isinstance(x, NonTerminalNode), nodes))
                for node in nodes:
                    if tree.symbol == node.symbol and first.role == node.role:
                        tree.role = first.role
                        roles.remove(first)
                        return len(roles) == 0

        for child in tree.children:
            if self._assign_roles(child, roles, tree.symbol):
                return True
        return len(roles) == 0

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
        mode: FuzzingMode = None,
        in_role: str = None,
    ) -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        return NonTerminalNode(start).fuzz(self, max_nodes=max_nodes, in_role=in_role)[
            0
        ]

    def update(self, grammar: "Grammar" | Dict[NonTerminal, Node], prime=True):
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            local_variables = grammar._local_variables
            global_variables = grammar._global_variables
            rules = grammar.rules
            fuzzing_mode = grammar.fuzzing_mode
        else:
            rules = grammar
            generators = local_variables = global_variables = {}
            fuzzing_mode = FuzzingMode.COMPLETE

        self.rules.update(rules)
        self.fuzzing_mode = fuzzing_mode
        self.generators.update(generators)

        for symbol in rules.keys():
            # We're updating from a grammar with a rule, but no generator,
            # so we should remove the generator if it exists
            if symbol not in generators and symbol in self.generators:
                del self.generators[symbol]

        self._parser = Grammar.Parser(self.rules)
        self._local_variables.update(local_variables)
        self._global_variables.update(global_variables)
        if prime:
            self.prime()

    def parse(
        self,
        word: str,
        start: str | NonTerminal = "<start>",
    ):
        return self._parser.parse(word, start)

    def parse_forest(
        self,
        word: str,
        start: str | NonTerminal = "<start>",
        allow_incomplete: bool = False,
    ):
        return self._parser.parse_forest(word, start, allow_incomplete=allow_incomplete)

    def parse_incomplete(
        self,
        word: str,
        start: str | NonTerminal = "<start>",
    ):
        return self._parser.parse_incomplete(word, start)

    def max_position(self):
        """Return the maximum position reached during last parsing."""
        return self._parser.max_position()

    def __contains__(self, item: str | NonTerminal):
        if isinstance(item, str):
            item = NonTerminal(item)
        return item in self.rules

    def __getitem__(self, item: str | NonTerminal):
        if isinstance(item, str):
            item = NonTerminal(item)
        return self.rules[item]

    def __setitem__(self, key: str | NonTerminal, value: Node):
        if isinstance(key, str):
            key = NonTerminal(key)
        self.rules[key] = value

    def __delitem__(self, key: str | NonTerminal):
        if isinstance(key, str):
            key = NonTerminal(key)
        del self.rules[key]

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    def __repr__(self):
        return "\n".join(
            [
                f"{key} ::= {value}{' := ' + self.generators[key] if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

    def roles(self, include_recipients: bool = True):
        found_roles = set()
        for nt, rule in self.rules.items():
            if nt.is_implicit:
                continue
            found_roles = found_roles.union(rule.tree_roles(self, include_recipients))
        return found_roles

    def get_repr_for_rule(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol} ::= {self.rules[symbol]}"
            f"{' := ' + self.generators[symbol] if symbol in self.generators else ''}"
        )

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def dummy():
        return Grammar({})

    def set_generator(self, symbol: str | NonTerminal, param: str):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = param

    def has_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return symbol in self.generators

    def get_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return self.generators.get(symbol, None)

    def update_parser(self):
        self._parser = Grammar.Parser(self.rules)

    def compute_kpath_coverage(
        self, derivation_trees: List[DerivationTree], k: int
    ) -> float:
        """
        Computes the k-path coverage of the grammar given a set of derivation trees.
        Returns a score between 0 and 1 representing the fraction of k-paths covered.
        """
        # Generate all possible k-paths in the grammar
        all_k_paths = self._generate_all_k_paths(k)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            covered_k_paths.update(self._extract_k_paths_from_tree(tree, k))

        # Compute coverage score
        if not all_k_paths:
            return 1.0  # If there are no k-paths, coverage is 100%
        return len(covered_k_paths) / len(all_k_paths)

    def _generate_all_k_paths(self, k: int) -> Set[Tuple[Node, ...]]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :return: All paths of length up to *k* within this grammar.
        """

        initial = set()
        initial_work: [Node] = [NonTerminalNode(name) for name in self.rules.keys()]  # type: ignore
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self.rules))

        work: List[Set[Tuple[Node]]] = [set((x,) for x in initial)]

        for _ in range(1, k):
            next_work = set()
            for base in work[-1]:
                for descendent in base[-1].descendents(self.rules):
                    next_work.add(base + (descendent,))
            work.append(next_work)

        # return set.union(*work)
        return work[-1]

    @staticmethod
    def _extract_k_paths_from_tree(
        tree: DerivationTree, k: int
    ) -> Set[Tuple[Node, ...]]:
        """
        Extracts all k-length paths (k-paths) from a derivation tree.
        """
        paths = set()

        def traverse(node: DerivationTree, current_path: Tuple[str, ...]):
            new_path = current_path + (node.symbol.symbol,)
            if len(new_path) == k:
                paths.add(new_path)
                # Do not traverse further to keep path length at k
                return
            for child in node.children:
                traverse(child, new_path)

        traverse(tree, ())
        return paths

    def prime(self):
        nodes = sum([self.visit(self.rules[symbol]) for symbol in self.rules], [])
        while nodes:
            node = nodes.pop(0)
            if node.node_type == NodeType.TERMINAL:
                continue
            elif node.node_type == NodeType.NON_TERMINAL:
                if node.symbol not in self.rules:
                    raise ValueError(f"Symbol {node.symbol} not found in grammar")
                if self.rules[node.symbol].distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        self.rules[node.symbol].distance_to_completion + 1
                    )
            elif node.node_type == NodeType.ALTERNATIVE:
                node.distance_to_completion = (
                    min([n.distance_to_completion for n in node.alternatives]) + 1
                )
                if node.distance_to_completion == float("inf"):
                    nodes.append(node)
            elif node.node_type == NodeType.CONCATENATION:
                if any([n.distance_to_completion == float("inf") for n in node.nodes]):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        sum([n.distance_to_completion for n in node.nodes]) + 1
                    )
            elif node.node_type == NodeType.REPETITION:
                if node.node.distance_to_completion == float("inf"):
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        node.node.distance_to_completion * node.min + 1
                    )
            else:
                raise ValueError(f"Unknown node type {node.node_type}")

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.extend(result)
        return aggregate

    def visitAlternative(self, node: Alternative):
        return self.visitChildren(node) + [node]

    def visitConcatenation(self, node: Concatenation):
        return self.visitChildren(node) + [node]

    def visitRepetition(self, node: Repetition):
        return self.visit(node.node) + [node]

    def visitStar(self, node: Star):
        return self.visit(node.node) + [node]

    def visitPlus(self, node: Plus):
        return self.visit(node.node) + [node]

    def visitOption(self, node: Option):
        return self.visit(node.node) + [node]

    def visitNonTerminalNode(self, node: NonTerminalNode):
        return [node]

    def visitTerminalNode(self, node: TerminalNode):
        return []

    def visitCharSet(self, node: CharSet):
        return []

    def compute_k_paths(self, k: int) -> Set[Tuple[Node, ...]]:
        """
        Computes all possible k-paths in the grammar.

        :param k: The length of the paths.
        :return: A set of tuples, each tuple representing a k-path as a sequence of symbols.
        """
        return self._generate_all_k_paths(k)

    def traverse_derivation(
        self,
        tree: DerivationTree,
        disambiguator: Disambiguator = Disambiguator(),
        paths: Set[Tuple[Node, ...]] = None,
        cur_path: Tuple[Node, ...] = None,
    ) -> Set[Tuple[Node, ...]]:
        if paths is None:
            paths = set()
        if tree.symbol.is_terminal:
            if cur_path is None:
                cur_path = (TerminalNode(tree.symbol),)
            paths.add(cur_path)
        else:
            if cur_path is None:
                cur_path = (NonTerminalNode(tree.symbol),)
            assert tree.symbol == typing.cast(NonTerminalNode, cur_path[-1]).symbol
            disambiguation = disambiguator.visit(self.rules[tree.symbol])
            for tree, path in zip(
                tree.children, disambiguation[tuple(c.symbol for c in tree.children)]
            ):
                self.traverse_derivation(tree, disambiguator, paths, cur_path + path)
        return paths

    def compute_grammar_coverage(
        self, derivation_trees: List[DerivationTree], k: int
    ) -> Tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.compute_k_paths(k)

        disambiguator = Disambiguator()

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise ValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )

    def get_python_env(self):
        return self._global_variables, self._local_variables

    def contains_type(self, tp: type, *, start="<start>") -> bool:
        """
        Return true if the grammar can produce an element of type `tp` (say, `int` or `bytes`).
        * `start`: a start symbol other than `<start>`.
        """
        if isinstance(start, str):
            start = NonTerminal(start)

        # We start on the right hand side of the start symbol
        start_node = self.rules[start]
        seen = {start_node}

        def node_matches(node):
            if isinstance(node, TerminalNode) and isinstance(node.symbol.symbol, tp):
                return True
            if any(node_matches(child) for child in node.children()):
                return True
            if isinstance(node, NonTerminalNode) and node not in seen:
                seen.add(node)
                return node_matches(self.rules[node.symbol])

        return node_matches(start_node)

    def contains_bits(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a bit element (0 or 1).
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(int, start=start)

    def contains_bytes(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a bytes element.
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(bytes, start=start)

    def contains_strings(self, *, start="<start>") -> bool:
        """
        Return true iff the grammar can produce a (UTF-8) string element.
        * `start`: a start symbol other than `<start>`.
        """
        return self.contains_type(str, start=start)
