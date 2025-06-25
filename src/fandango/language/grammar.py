import abc
import enum
import random
import re
import time
import typing
from collections import defaultdict
from copy import deepcopy
from typing import Any, Iterator, Optional, Union
from collections.abc import Generator

import exrex
from thefuzz import process as thefuzz_process

from fandango.errors import FandangoValueError, FandangoParseError
from fandango.language.symbol import NonTerminal, Symbol, Terminal
from fandango.language.tree import DerivationTree

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


class GeneratorParserValueError(ValueError):
    pass


class Node(abc.ABC):
    def __init__(
        self, node_type: NodeType, distance_to_completion: float = float("inf")
    ):
        self._node_type = node_type
        self.distance_to_completion = distance_to_completion

    @property
    def node_type(self):
        return self._node_type

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        return

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

    def msg_parties(self, *, include_recipients: bool = False) -> set[str]:
        parties: set[str] = set()
        for child in self.children():
            parties |= child.msg_parties(include_recipients=include_recipients)
        return parties

    def slice_parties(self, parties: list[str]) -> None:
        """Remove all nodes whose party is not in `parties`."""
        for child in self.children():
            child.slice_parties(parties)

    def in_parties(self, parties: list[str]) -> bool:
        return True

    def children(self):
        return []

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        """
        Returns an iterator of the descendents of this node.

        :param grammar: The rules upon which to base non-terminal lookups.
        :return An iterator over the descendent nodes.
        """
        yield from ()


class Alternative(Node):
    def __init__(self, alternatives: list[Node], id: str = ""):
        super().__init__(NodeType.ALTERNATIVE)
        self.id = id
        self.alternatives = alternatives

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        in_range_nodes = list(
            filter(lambda x: x.distance_to_completion < max_nodes, self.alternatives)
        )
        if len(in_range_nodes) == 0:
            min_ = min(self.alternatives, key=lambda x: x.distance_to_completion)
            random.choice(
                [
                    a
                    for a in self.alternatives
                    if a.distance_to_completion <= min_.distance_to_completion
                ]
            ).fuzz(parent, grammar, 0, in_message)
            return
        random.choice(in_range_nodes).fuzz(parent, grammar, max_nodes, in_message)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitAlternative(self)

    def children(self):
        return self.alternatives

    def slice_parties(self, parties: list[str]) -> None:
        self.alternatives = [
            node for node in self.alternatives if node.in_parties(parties)
        ]
        super().slice_parties(parties)

    def __getitem__(self, item):
        return self.alternatives.__getitem__(item)

    def __len__(self):
        return len(self.alternatives)

    def __repr__(self):
        return "(" + " | ".join(map(repr, self.alternatives)) + ")"

    def __str__(self):
        return "(" + " | ".join(map(str, self.alternatives)) + ")"

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from self.alternatives


class Concatenation(Node):
    def __init__(self, nodes: list[Node], id: str = ""):
        super().__init__(NodeType.CONCATENATION)
        self.id = id
        self.nodes = nodes

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        prev_parent_size = parent.size()
        for node in self.nodes:
            if node.distance_to_completion >= max_nodes:
                node.fuzz(parent, grammar, 0, in_message)
            else:
                reserved_distance = self.distance_to_completion
                for dist_node in self.nodes:
                    reserved_distance -= dist_node.distance_to_completion
                    if dist_node == node:
                        break
                node.fuzz(
                    parent, grammar, int(max_nodes - reserved_distance), in_message
                )
            max_nodes -= parent.size() - prev_parent_size
            prev_parent_size = parent.size()

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitConcatenation(self)

    def children(self):
        return self.nodes

    def slice_parties(self, parties: list[str]) -> None:
        self.nodes = [node for node in self.nodes if node.in_parties(parties)]
        super().slice_parties(parties)

    def __getitem__(self, item):
        return self.nodes.__getitem__(item)

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return " ".join(map(repr, self.nodes))

    def __str__(self):
        return " ".join(map(str, self.nodes))

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from self.nodes


class Repetition(Node):
    def __init__(
        self, node: Node, id: str = "", min_=("0", [], {}), max_=(f"{None}", [], {})
    ):
        super().__init__(NodeType.REPETITION)
        self.id = id
        # min_expr, min_nt, min_search = min_
        # max_expr, max_nt, max_search = max_

        # if min_ < 0:
        #    raise FandangoValueError(
        #        f"Minimum repetitions {min_} must be greater than or equal to 0"
        #    )
        # if max_ <= 0 or max_ < min_:
        #    raise FandangoValueError(
        #        f"Maximum repetitions {max_} must be greater than 0 or greater than min {min_}"
        #    )

        self.node = node
        self.expr_data_min = min_
        self.expr_data_max = max_
        self.static_min = None
        self.static_max = None

    def get_access_points(self):
        _, _, searches_min = self.expr_data_min
        _, _, searches_max = self.expr_data_max
        non_terminals = set[NonTerminal]()
        for search_list in [searches_min, searches_max]:
            for search in search_list.values():
                for nt in search.get_access_points():
                    non_terminals.add(nt)
        return non_terminals

    def _compute_rep_bound(
        self, grammar: "Grammar", tree: Optional[DerivationTree], expr_data
    ):
        expr, _, searches = expr_data
        if expr == "None":
            expr = f"{MAX_REPETITIONS}"
        local_cpy = grammar._local_variables.copy()

        if len(searches) == 0:
            return eval(expr, grammar._global_variables, local_cpy), True
        if tree is None:
            raise FandangoValueError("Need `tree` argument if symbols present")

        nodes = []
        if len(searches) != 1:
            raise FandangoValueError(
                "Computed repetition requires exactly one or zero searches"
            )

        search_name, search = next(iter(searches.items()))
        nodes.extend(
            [(search_name, container) for container in search.find(tree.get_root())]
        )
        if len(nodes) == 0:
            raise FandangoValueError(
                f"Couldn't find search target ({search}) in prefixed DerivationTree for computed repetition"
            )

        target_name, target_container = nodes[-1]
        target = target_container.evaluate()
        local_cpy[target_name] = target
        if isinstance(target, DerivationTree):
            target.set_all_read_only(True)
            first_uncommon_idx = 0
            for idx, (target_parent, tree_parent) in enumerate(
                zip(target.get_path(), tree.get_path())
            ):
                if target_parent.symbol == tree_parent.symbol:
                    first_uncommon_idx = idx + 1
                else:
                    break
            for parent in target.get_path()[first_uncommon_idx:]:
                parent.read_only = True
            for parent in tree.get_path()[first_uncommon_idx:]:
                parent.read_only = True

        return eval(expr, grammar._global_variables, local_cpy), False

    def min(self, grammar: "Grammar", tree: Optional[DerivationTree] = None):
        if self.static_min is None:
            current_min, is_static = self._compute_rep_bound(
                grammar, tree, self.expr_data_min
            )
            if is_static:
                self.static_min = current_min
            return current_min
        else:
            return self.static_min

    def max(self, grammar: "Grammar", tree: Optional[DerivationTree] = None):
        if self.static_max is None:
            current_max, is_static = self._compute_rep_bound(
                grammar, tree, self.expr_data_max
            )

            # if is_static:
            #    self.static_max = current_max
            return current_max
        else:
            return self.static_max

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitRepetition(self)

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        prev_parent_size = parent.size()

        current_min = self.min(grammar, parent)
        current_max = self.max(grammar, parent)

        goal_range = random.randint(current_min, current_max)
        reserved_max_nodes = self.distance_to_completion

        for rep in range(goal_range):
            if self.node.distance_to_completion >= max_nodes:
                if rep > current_min:
                    break
                self.node.fuzz(parent, grammar, 0, in_message)
            else:
                reserved_max_nodes -= self.node.distance_to_completion
                self.node.fuzz(
                    parent, grammar, int(max_nodes - reserved_max_nodes), in_message
                )
            max_nodes -= parent.size() - prev_parent_size
            prev_parent_size = parent.size()

    def __repr__(self):
        # We use "f()" as a placeholder for some function
        min_str = str(self.static_min) if self.static_min is not None else "f()"
        max_str = str(self.static_max) if self.static_max is not None else "f()"

        if min_str == max_str:
            return f"{self.node}{{{min_str}}}"
        return f"{self.node}{{{min_str},{max_str}}}"

    def __str__(self):
        # We use "f()" as a placeholder for some function
        min_str = str(self.static_min) if self.static_min is not None else "f()"
        max_str = str(self.static_max) if self.static_max is not None else "f()"

        if min_str == max_str:
            return f"{self.node!s}{{{min_str}}}"
        return f"{self.node!s}{{{min_str},{max_str}}}"

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        base: list[Node] = []
        # Todo: Context from DerivationTree is missing.
        #  Repetitions that depend on a value within the tree will cause a crash.
        if self.min(grammar) == 0:
            base.append(TerminalNode(Terminal("")))
        if self.min(grammar) <= 1 <= self.max(grammar):
            base.append(self.node)
        yield Alternative(
            base
            + [
                Concatenation([self.node] * r)
                for r in range(max(2, self.min(grammar)), self.max(grammar) + 1)
            ]
        )

    def children(self):
        return [self.node]

    def in_parties(self, parties: list[str]) -> bool:
        return self.node.in_parties(parties)


class Star(Repetition):
    def __init__(self, node: Node, id: str = "", max_repetitions: int = 5):
        super().__init__(node, id, ("0", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitStar(self)

    def __repr__(self):
        return f"{self.node}*"

    def __str__(self):
        return f"{self.node!s}*"


class Plus(Repetition):
    def __init__(self, node: Node, id: str = "", max_repetitions: int = 5):
        super().__init__(node, id, ("1", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitPlus(self)

    def __repr__(self):
        return f"{self.node}+"

    def __str__(self):
        return f"{self.node!s}+"


class Option(Repetition):
    def __init__(self, node: Node, id: str = ""):
        super().__init__(node, id, ("0", [], {}), ("1", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitOption(self)

    def __repr__(self):
        return f"{self.node}?"

    def __str__(self):
        return f"{self.node!s}?"

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from (self.node, TerminalNode(Terminal("")))


class NonTerminalNode(Node):
    def __init__(
        self,
        symbol: NonTerminal,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
    ):
        super().__init__(NodeType.NON_TERMINAL)
        self.symbol = symbol
        self.sender = sender
        self.recipient = recipient

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        if self.symbol not in grammar:
            raise FandangoValueError(f"Symbol {self.symbol} not found in grammar")
        dummy_current_tree = DerivationTree(self.symbol)
        parent.add_child(dummy_current_tree)

        if grammar.is_use_generator(dummy_current_tree):
            dependencies = grammar.generator_dependencies(self.symbol)
            for nt in dependencies:
                NonTerminalNode(nt).fuzz(dummy_current_tree, grammar, max_nodes - 1)
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

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):
        if self.sender is not None:
            if self.recipient is None:
                return f"<{self.sender}:{self.symbol.__repr__()[:-1]}>"
            else:
                return f"<{self.sender}:{self.recipient}:{self.symbol.__repr__()[:-1]}>"
        else:
            return self.symbol.__repr__()

    def __str__(self):
        if self.sender is not None:
            if self.recipient is None:
                return f"<{self.sender}:{self.symbol._repr()[1:-1]}>"
            else:
                return f"<{self.sender}:{self.recipient}:{self.symbol._repr()[1:-1]}>"
        else:
            return self.symbol._repr()

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

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield grammar.rules[self.symbol]

    def in_parties(self, parties: list[str]) -> bool:
        return not self.sender or self.sender in parties


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        super().__init__(NodeType.TERMINAL, 1)
        self.symbol = symbol

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        if self.symbol.is_regex:
            if isinstance(self.symbol.symbol, bytes):
                # Exrex can't do bytes, so we decode to str and back
                instance = exrex.getone(self.symbol.symbol.decode("iso-8859-1"))
                parent.add_child(
                    DerivationTree(Terminal(instance.encode("iso-8859-1")))
                )
                return

            instance = exrex.getone(self.symbol.symbol)
            parent.add_child(DerivationTree(Terminal(instance)))
            return
        parent.add_child(DerivationTree(self.symbol))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __str__(self):
        return self.symbol.__str__()

    def __eq__(self, other):
        return isinstance(other, TerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


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


class CharSet(Node):
    def __init__(self, chars: str):
        super().__init__(NodeType.CHAR_SET, 0)
        self.chars = chars

    def fuzz(
        self,
        parent: "DerivationTree",
        grammar: "Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ) -> list[DerivationTree]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        for char in self.chars:
            yield TerminalNode(Terminal(char))


class NodeVisitor(abc.ABC):
    def visit(self, node: Node):
        return node.accept(self)

    def default_result(self):
        pass

    def aggregate_results(self, aggregate, result):
        pass

    def visitChildren(self, node: Node):
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
    def __init__(self, grammar: "Grammar"):
        self.known_disambiguations: dict[
            Node, dict[tuple[Symbol, ...], list[tuple[Node, ...]]]
        ] = {}
        self.grammar = grammar

    def visit(self, node: Node) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        if node in self.known_disambiguations:
            return self.known_disambiguations[node]
        result = super().visit(node)
        self.known_disambiguations[node] = result
        return result

    def visitAlternative(
        self, node: Alternative
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        child_endpoints: dict[tuple[Symbol, ...], list[tuple[Node, ...]]] = {}
        for child in node.children():
            endpoints: dict[tuple[Symbol, ...], list[tuple[Node, ...]]] = self.visit(
                child
            )
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
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        child_endpoints: dict[tuple[Symbol, ...], list[tuple[Node, ...]]] = {(): []}
        for child in node.children():
            next_endpoints: dict[tuple[Symbol, ...], list[tuple[Node, ...]]] = {}
            endpoints: dict[tuple[Symbol, ...], list[tuple[Node, ...]]] = self.visit(
                child
            )
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
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        # repetitions are alternatives over concatenations
        implicit_alternative = next(node.descendents(self.grammar))
        return self.visit(implicit_alternative)

    def visitStar(self, node: Star) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitPlus(self, node: Plus) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return self.visitRepetition(node)

    def visitOption(
        self, node: Option
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        implicit_alternative = Alternative(
            [Concatenation([]), Concatenation([node.node])]
        )
        return self.visit(implicit_alternative)

    def visitNonTerminalNode(
        self, node: NonTerminalNode
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitTerminalNode(
        self, node: TerminalNode
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {(node.symbol,): [(node,)]}

    def visitCharSet(
        self, node: CharSet
    ) -> dict[tuple[Symbol, ...], list[tuple[Node, ...]]]:
        return {(Terminal(c),): [(node, TerminalNode(Terminal(c)))] for c in node.chars}


class SymbolFinder(NodeVisitor):
    def __init__(self):
        self.terminalNodes = []
        self.nonTerminalNodes = []

    def visitNonTerminalNode(self, node: NonTerminalNode):
        self.nonTerminalNodes.append(node)

    def visitTerminalNode(self, node: TerminalNode):
        self.terminalNodes.append(node)


class NodeReplacer(NodeVisitor):
    def __init__(self, old_node: Node, new_node: Node):
        self.old_node = old_node
        self.new_node = new_node

    def replace(self, node: Node):
        if node == self.old_node:
            return self.new_node
        return node

    def default_result(self):
        return []

    def aggregate_results(self, aggregate, result):
        aggregate.append(result)
        return aggregate

    def visitConcatenation(self, node: Concatenation):
        node = self.replace(node)
        node.nodes = self.visitChildren(node)
        return node

    def visitAlternative(self, node: Alternative):
        node = self.replace(node)
        node.alternatives = self.visitChildren(node)
        return node

    def visitRepetition(self, node: Repetition):
        node = self.replace(node)
        node.node = self.visit(node.node)
        return node

    def visitStar(self, node: Star):
        node = self.replace(node)
        node.node = self.visit(node.node)
        return node

    def visitPlus(self, node: Plus):
        node = self.replace(node)
        node.node = self.visit(node.node)
        return node

    def visitOption(self, node: Option):
        node = self.replace(node)
        node.node = self.visit(node.node)
        return node

    def visitNonTerminalNode(self, node: NonTerminalNode):
        node = self.replace(node)
        return node

    def visitTerminalNode(self, node: TerminalNode):
        node = self.replace(node)
        return node


class PacketTruncator(NodeVisitor):
    def __init__(self, grammar: "Grammar", keep_parties: set[str]):
        self.grammar = grammar
        self.keep_msg_parties = keep_parties

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
        if node.sender is None or node.recipient is None:
            return False
        truncatable = True
        if node.sender in self.keep_msg_parties:
            truncatable = False
        if node.recipient in self.keep_msg_parties:
            truncatable = False
        return truncatable

    def visitTerminalNode(self, node: TerminalNode):
        return False


class MessageNestingDetector(NodeVisitor):
    def __init__(self, grammar: "Grammar"):
        self.grammar = grammar
        self.seen_nt: set[NonTerminal] = set()
        self.current_path: list[NonTerminal] = []

    def fail_on_nested_packet(self, start_symbol: NonTerminal):
        self.current_path.append(start_symbol)
        self.visit(self.grammar[start_symbol])
        self.current_path.pop()

    def visitNonTerminalNode(self, node: NonTerminalNode):
        if node.symbol not in self.seen_nt:
            self.seen_nt.add(node.symbol)
        elif node.sender is not None and node.symbol in self.current_path:
            str_path = [str(p) for p in self.current_path]
            raise RuntimeError(
                f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}! DerivationPath: "
                + " -> ".join(str_path)
            )
        else:
            return

        if node.sender is not None:
            parties = self.grammar[node.symbol].msg_parties(include_recipients=False)
            if len(parties) != 0:
                raise RuntimeError(
                    f"Found illegal packet-definitions within packet-definition of non_terminal {node.symbol}: "
                    + ", ".join(parties)
                )
            return
        self.current_path.append(node.symbol)
        self.visit(self.grammar[node.symbol])
        self.current_path.pop()


class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: tuple[tuple[Symbol, frozenset[tuple[str, Any]]], ...],
        dot: int = 0,
        children: Optional[list[DerivationTree]] = None,
        is_incomplete: bool = False,
    ):
        self._nonterminal = nonterminal
        self._position = position
        self._symbols = symbols
        self._dot = dot
        self.children = children or []
        self.is_incomplete = is_incomplete
        self._hash: Optional[int] = None

    @property
    def nonterminal(self):
        return self._nonterminal

    def append_child(self, child: DerivationTree):
        self.children.append(child)
        self._hash = None

    def extend_children(self, children: list[DerivationTree]):
        self.children.extend(children)
        self._hash = None

    @property
    def position(self):
        return self._position

    @property
    def symbols(self):
        return self._symbols

    @property
    def dot(self):
        return self.symbols[self._dot][0] if self._dot < len(self.symbols) else None

    @property
    def dot_params(self) -> Optional[frozenset[tuple[str, Any]]]:
        return self.symbols[self._dot][1] if self._dot < len(self.symbols) else None

    def finished(self):
        return self._dot >= len(self.symbols) and not self.is_incomplete

    def next_symbol_is_nonterminal(self):
        return (
            self._dot < len(self.symbols) and self.symbols[self._dot][0].is_non_terminal
        )

    def next_symbol_is_terminal(self):
        return self._dot < len(self.symbols) and self.symbols[self._dot][0].is_terminal

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(
                (
                    self.nonterminal,
                    self.position,
                    self.symbols,
                    self._dot,
                    tuple(self.children),
                )
            )
        return self._hash

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
                    f"{'•' if i == self._dot else ''}{s[0]!s}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("•" if self.finished() else "")
            + f", column {self.position}"
            + ")"
        )

    def next(self, position: Optional[int] = None):
        return ParseState(
            self.nonterminal,
            position or self.position,
            self.symbols,
            self._dot + 1,
            self.children[:],
            self.is_incomplete,
        )


class Column:
    def __init__(self, states: Optional[list[ParseState]] = None):
        self.states = states or []
        self.dot_map = dict[NonTerminal, list[ParseState]]()
        self.unique = set(self.states)
        for state in self.states:
            self.dot_map[state.nonterminal].append(state)

    def __iter__(self):
        index = 0
        while index < len(self.states):
            yield self.states[index]
            index += 1

    def __len__(self):
        return len(self.states)

    def __getitem__(self, item):
        return self.states[item]

    def remove(self, state: ParseState):
        if state not in self.unique:
            return False
        self.unique.remove(state)
        self.states.remove(state)
        self.dot_map.get(state.dot, []).remove(state)

    def replace(self, old: ParseState, new: ParseState):
        self.unique.remove(old)
        self.unique.add(new)
        i_old = self.states.index(old)
        del self.states[i_old]
        self.states.insert(i_old, new)
        self.dot_map[old.dot].remove(old)
        dot_list = self.dot_map.get(new.dot, [])
        dot_list.append(new)
        self.dot_map[new.dot] = dot_list

    def __contains__(self, item):
        return item in self.unique

    def find_dot(self, nt: NonTerminal):
        return self.dot_map.get(nt, [])

    def add(self, state: ParseState):
        if state not in self.unique:
            self.states.append(state)
            self.unique.add(state)
            state_list = self.dot_map.get(state.dot, [])
            state_list.append(state)
            self.dot_map[state.dot] = state_list
            return True
        return False

    def update(self, states: set[ParseState]):
        for state in states:
            self.add(state)

    def __repr__(self):
        return f"Column({self.states})"


def closest_match(word, candidates):
    """
    `word` raises a syntax error;
    return alternate suggestion for `word` from `candidates`
    """
    return thefuzz_process.extractOne(word, candidates)[0]


class Grammar(NodeVisitor):
    """Represent a grammar."""

    class ParserDerivationTree(DerivationTree):
        def __init__(
            self,
            symbol: Symbol,
            children: Optional[list["DerivationTree"]] = None,
            *,
            parent: Optional["DerivationTree"] = None,
            sender: Optional[str] = None,
            recipient=None,
            read_only: bool = False,
        ):
            super().__init__(
                symbol,
                children,
                parent=parent,
                sources=[],
                sender=sender,
                recipient=recipient,
                read_only=read_only,
            )

        def set_children(self, children: list["DerivationTree"]):
            self._children = children
            self.invalidate_hash()

    class Parser(NodeVisitor):
        class ParsingMode(enum.Enum):
            COMPLETE = 0
            INCOMPLETE = 1

        def __init__(
            self,
            grammar: "Grammar",
        ):
            self.implicit_start = NonTerminal("<*start*>")
            self.grammar_rules: dict[NonTerminal, Node] = grammar.rules
            self.grammar = grammar
            self._rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
            self._implicit_rules: dict[
                NonTerminal, set[tuple[NonTerminal, frozenset]]
            ] = {}
            self._context_rules: dict[
                NonTerminal, tuple[Node, tuple[NonTerminal, frozenset]]
            ] = dict()
            self._tmp_rules: dict[NonTerminal, set[tuple[NonTerminal, frozenset]]] = {}
            self._cache: dict[
                tuple[
                    str | bytes,
                    NonTerminal,
                    Grammar.Parser.ParsingMode,
                    Optional[DerivationTree],
                ],
                list[DerivationTree],
            ] = {}
            self._incomplete: set[DerivationTree] = set()
            self._max_position = -1
            self.elapsed_time: float = 0
            self._process()

        def _process(self):
            self._rules.clear()
            self._implicit_rules.clear()
            self._context_rules.clear()
            for nonterminal in self.grammar_rules:
                self.set_rule(nonterminal, self.visit(self.grammar_rules[nonterminal]))

            for nonterminal in self._implicit_rules:
                self._implicit_rules[nonterminal] = {
                    tuple(a)  # type: ignore[misc]
                    for a in self._implicit_rules[nonterminal]
                }

        def set_implicit_rule(
            self, rule: list[list[tuple[NonTerminal, frozenset]]]
        ) -> tuple[NonTerminal, frozenset]:
            nonterminal = NonTerminal(f"<*{len(self._implicit_rules)}*>")
            self._implicit_rules[nonterminal] = rule  # type: ignore[assignment]
            return (nonterminal, frozenset())

        def set_rule(
            self,
            nonterminal: NonTerminal,
            rule: list[list[tuple[NonTerminal, frozenset]]],
        ):
            self._rules[nonterminal] = {tuple(a) for a in rule}  # type: ignore[misc]

        def set_context_rule(
            self, node: Node, non_terminal: tuple[NonTerminal, frozenset]
        ) -> NonTerminal:
            nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
            self._context_rules[nonterminal] = (node, non_terminal)
            return nonterminal

        def set_tmp_rule(
            self,
            rule: list[list[tuple[NonTerminal, frozenset]]],
            nonterminal: Optional[NonTerminal] = None,
        ):
            if nonterminal is None:
                nonterminal = NonTerminal(f"<*tmp_{len(self._tmp_rules)}*>")
            rule_id = nonterminal.symbol[2:-2]  # type: ignore[index]
            self._tmp_rules[nonterminal] = {tuple(a) for a in rule}  # type: ignore[misc]
            return (nonterminal, frozenset()), rule_id

        def _clear_tmp(self):
            self._tmp_rules.clear()

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.extend(result)
            return aggregate

        def visitAlternative(self, node: Alternative):
            result = self.visitChildren(node)
            intermediate_nt = NonTerminal(f"<__{NodeType.ALTERNATIVE}:{node.id}>")
            self.set_rule(intermediate_nt, result)
            return [[(intermediate_nt, frozenset())]]

        def visitConcatenation(self, node: Concatenation):
            result: list[list[tuple[NonTerminal, frozenset]]] = [[]]
            for child in node.children():
                to_add = self.visit(child)
                new_result = []
                for r in result:
                    for a in to_add:
                        new_result.append(r + a)
                result = new_result
            intermediate_nt = NonTerminal(f"<__{NodeType.CONCATENATION}:{node.id}>")
            self.set_rule(intermediate_nt, result)
            return [[(intermediate_nt, frozenset())]]

        def visitRepetition(
            self,
            node: Repetition,
            nt: Optional[tuple[NonTerminal, frozenset]] = None,
            tree: Optional[DerivationTree] = None,
        ):
            is_context = len(node.get_access_points()) != 0
            if nt is None:
                alternatives = self.visit(node.node)
                nt = self.set_implicit_rule(alternatives)

                if is_context:
                    i_nt = self.set_context_rule(node, nt)
                    repetition_nt = NonTerminal(f"<__{NodeType.REPETITION}:{node.id}>")
                    self.set_rule(repetition_nt, [[(i_nt, frozenset())]])
                    return [[(repetition_nt, frozenset())]]

            prev = None
            node_min = node.min(self.grammar, tree)
            node_max = node.max(self.grammar, tree)
            for rep in range(node_min, node_max):
                alts = [[nt]]
                if prev is not None:
                    alts.append([nt, prev])
                if is_context:
                    prev, rule_id = self.set_tmp_rule(alts)
                else:
                    prev = self.set_implicit_rule(alts)
            alts = [node_min * [nt]]
            if prev is not None:
                alts.append(node_min * [nt] + [prev])
            if is_context:
                tmp_nt, rule_id = self.set_tmp_rule(alts)
                return [[tmp_nt]]
            min_nt = self.set_implicit_rule(alts)
            intermediate_nt = NonTerminal(f"<__{NodeType.REPETITION}:{node.id}>")
            self.set_rule(intermediate_nt, [[min_nt]])
            return [[(intermediate_nt, frozenset())]]

        def visitStar(self, node: Star):
            alternatives: list[list[tuple[NonTerminal, frozenset]]] = [[]]
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r + [nt])
            result = [[nt]]
            intermediate_nt = NonTerminal(f"<__{NodeType.STAR}:{node.id}>")
            self.set_rule(intermediate_nt, result)
            return [[(intermediate_nt, frozenset())]]

        def visitPlus(self, node: Plus):
            alternatives: list[list[tuple[NonTerminal, frozenset]]] = []
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r)
                alternatives.append(r + [nt])
            result = [[nt]]
            intermediate_nt = NonTerminal(f"<__{NodeType.PLUS}:{node.id}>")
            self.set_rule(intermediate_nt, result)
            return [[(intermediate_nt, frozenset())]]

        def visitOption(self, node: Option):
            result: list[list[tuple[NonTerminal, frozenset]]] = [[]] + self.visit(
                node.node
            )
            intermediate_nt = NonTerminal(f"<__{NodeType.OPTION}:{node.id}>")
            self.set_rule(intermediate_nt, result)
            return [[(intermediate_nt, frozenset())]]

        def visitNonTerminalNode(self, node: NonTerminalNode):
            params = dict()
            if node.sender is not None:
                params["sender"] = node.sender
            if node.recipient is not None:
                params["recipient"] = node.recipient
            parameters = frozenset(params.items())
            return [[(node.symbol, parameters)]]

        def visitTerminalNode(self, node: TerminalNode):
            return [[(node.symbol, frozenset())]]

        def collapse(self, tree: Optional[DerivationTree]):
            if tree is None:
                return None
            if isinstance(tree.symbol, NonTerminal):
                if tree.symbol.symbol.startswith("<__"):  # type: ignore[union-attr, arg-type]
                    raise FandangoValueError(
                        "Can't collapse a tree with an implicit root node"
                    )
            return self._collapse(tree)[0]

        def _collapse(self, tree: DerivationTree):
            reduced = []
            for child in tree.children:
                rec_reduced = self._collapse(child)
                reduced.extend(rec_reduced)

            if isinstance(tree.symbol, NonTerminal):
                if tree.symbol.symbol.startswith("<__"):  # type: ignore[union-attr, arg-type]
                    return reduced

            return [
                DerivationTree(
                    tree.symbol,
                    children=reduced,
                    sources=tree.sources,
                    read_only=tree.read_only,
                    recipient=tree.recipient,
                    sender=tree.sender,
                )
            ]

        def predict(
            self,
            state: ParseState,
            table: list[Column],
            k: int,
            hookin_parent: Optional[DerivationTree] = None,
        ):
            if state.dot in self._rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                        for rule in self._rules[state.dot]
                    }
                )
            elif state.dot in self._implicit_rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                        for rule in self._implicit_rules[state.dot]
                    }
                )
            elif state.dot in self._tmp_rules:
                table[k].update(
                    {
                        ParseState(state.dot, k, rule, 0)  # type: ignore[arg-type]
                        for rule in self._tmp_rules[state.dot]
                    }
                )
            elif state.dot in self._context_rules:
                node, nt = self._context_rules[state.dot]
                self.predict_ctx_rule(state, table, k, node, nt, hookin_parent)

        def construct_incomplete_tree(
            self, state: ParseState, table: list[Column]
        ) -> DerivationTree:
            current_tree = Grammar.ParserDerivationTree(
                state.nonterminal, state.children
            )
            current_state = state
            found_next_state = True
            while found_next_state:
                found_next_state = False
                for table_state in table[current_state.position].states:
                    if table_state.dot == current_state.nonterminal:
                        current_state = table_state
                        found_next_state = True
                        break
                if str(current_tree.symbol).startswith("<*"):
                    current_tree = Grammar.ParserDerivationTree(
                        current_state.nonterminal,
                        [*current_state.children, *current_tree.children],
                        **dict(current_state.dot_params or {}),
                    )
                else:
                    current_tree = Grammar.ParserDerivationTree(
                        current_state.nonterminal,
                        [*current_state.children, current_tree],
                        **dict(current_state.dot_params or {}),
                    )

            return current_tree.children[0]

        def predict_ctx_rule(
            self,
            state: ParseState,
            table: list[Column],
            k: int,
            node: Node,
            nt_rule,
            hookin_parent: Optional[DerivationTree] = None,
        ):
            if not isinstance(node, Repetition):
                raise FandangoValueError(f"Node {node} needs to be a Repetition")

            tree = self.construct_incomplete_tree(state, table)
            tree = self.collapse(tree)
            if hookin_parent is not None:
                hookin_parent.set_children(hookin_parent.children + [tree])
            try:
                [[context_nt]] = self.visitRepetition(
                    node, nt_rule, tree if hookin_parent is None else hookin_parent
                )
            except (ValueError, FandangoValueError):
                return
            finally:
                if hookin_parent is not None:
                    hookin_parent.set_children(hookin_parent.children[:-1])
            new_symbols = []
            placed = False
            for symbol, dot_params in state.symbols:
                if symbol == state.dot and not placed:
                    new_symbols.append(context_nt)
                    placed = True
                else:
                    new_symbols.append((symbol, dot_params))
            new_state = ParseState(
                state.nonterminal,
                state.position,
                tuple(new_symbols),
                state._dot,
                state.children,
                state.is_incomplete,
            )
            if state in table[k]:
                table[k].replace(state, new_state)
            self.predict(new_state, table, k)

        def scan_bit(
            self,
            state: ParseState,
            word: str | bytes,
            table: list[Column],
            k: int,
            w: int,
            bit_count: int,
            nr_bits_scanned: int,
        ) -> bool:
            """
            Scan a bit from the input `word`.
            `table` is the parse table (may be modified by this function).
            `table[k]` is the current column.
            `word[w]` is the current byte.
            `bit_count` is the current bit position (7-0).
            Return True if a bit was matched, False otherwise.
            """
            assert isinstance(state.dot.symbol, int)
            assert 0 <= bit_count <= 7

            if w >= len(word):
                return False

            # Get the highest bit. If `word` is bytes, word[w] is an integer.
            byte = ord(word[w]) if isinstance(word, str) else word[w]
            bit = (byte >> bit_count) & 1

            # LOGGER.debug(f"Checking {state.dot} against {bit}")
            match, match_length = state.dot.check(bit)
            if not match or match_length == 0:
                # LOGGER.debug(f"No match")
                return False

            # Found a match
            # LOGGER.debug(f"Found bit {bit}")
            next_state = state.next()
            tree = Grammar.ParserDerivationTree(Terminal(bit))
            next_state.append_child(tree)
            # LOGGER.debug(f"Added tree {tree.to_string()!r} to state {next_state!r}")
            # Insert a new table entry with next state
            # This is necessary, as our initial table holds one entry
            # per input byte, yet needs to be expanded to hold the bits, too.

            # Add a new table row if the bit isn't already represented
            # by a row in the parsing table
            if len(table) <= len(word) + 1 + nr_bits_scanned:
                table.insert(k + 1, Column())
            table[k + 1].add(next_state)

            # Save the maximum position reached, so we can report errors
            self._max_position = max(self._max_position, w)

            return True

        def scan_bytes(
            self,
            state: ParseState,
            word: str | bytes,
            table: list[Column],
            k: int,
            w: int,
            mode: ParsingMode,
        ) -> bool:
            """
            Scan a byte from the input `word`.
            `state` is the current parse state.
            `table` is the parse table.
            `table[k]` is the current column.
            `word[w]` is the current byte.
            Return True if a byte was matched, False otherwise.
            """

            assert not isinstance(state.dot.symbol, int)
            assert not state.dot.is_regex

            # LOGGER.debug(f"Checking byte(s) {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

            match, match_length = state.dot.check(word[w:])
            if not match:
                if mode != Grammar.Parser.ParsingMode.INCOMPLETE or (
                    w + len(state.dot)
                ) < len(word):
                    return False
                match, match_length = state.dot.check(word[w:], incomplete=True)
                if not match or match_length == 0:
                    return False
                state.is_incomplete = True

            # Found a match
            # LOGGER.debug(f"Matched byte(s) {state.dot!r} at position {w:#06x} ({w}) (len = {match_length}) {word[w:w + match_length]!r}")
            next_state = state.next()
            tree = Grammar.ParserDerivationTree(Terminal(word[w : w + match_length]))
            next_state.append_child(tree)
            table[k + match_length].add(next_state)
            # LOGGER.debug(f"Next state: {next_state} at column {k + match_length}")
            self._max_position = max(self._max_position, w + match_length)

            return True

        def scan_regex(
            self,
            state: ParseState,
            word: str | bytes,
            table: list[Column],
            k: int,
            w: int,
            mode: ParsingMode,
        ) -> bool:
            """
            Scan a byte from the input `word`.
            `state` is the current parse state.
            `table` is the parse table.
            `table[k]` is the current column.
            `word[w]` is the current byte.
            Return (True, #bytes) if bytes were matched, (False, 0) otherwise.
            """

            assert not isinstance(state.dot.symbol, int)
            assert state.dot.is_regex

            # LOGGER.debug(f"Checking regex {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

            match, match_length = state.dot.check(word[w:])
            if not match:
                if mode != Grammar.Parser.ParsingMode.INCOMPLETE:
                    return False
                match, match_length = state.dot.check(word[w:], incomplete=True)
                if not match or (match_length + w) < len(word):
                    return False
                state.is_incomplete = True

            # Found a match
            # LOGGER.debug(f"Matched regex {state.dot!r} at position {w:#06x} ({w}) (len = {match_length}) {word[w:w+match_length]!r}")
            next_state = state.next()
            next_state.append_child(
                Grammar.ParserDerivationTree(Terminal(word[w : w + match_length]))
            )
            table[k + match_length].add(next_state)
            # LOGGER.debug(f"Next state: {next_state} at column {k + match_length}")
            self._max_position = max(self._max_position, w + match_length)
            return True

        def _rec_to_derivation_tree(self, tree: list["Grammar.ParserDerivationTree"]):
            ret = []
            for child in tree:
                children = self._rec_to_derivation_tree(child.children)  # type: ignore[arg-type]
                ret.append(
                    DerivationTree(
                        child.symbol,
                        children,
                        parent=child.parent,
                        sources=child.sources,
                        sender=child.sender,
                        recipient=child.recipient,
                        read_only=child.read_only,
                    )
                )
            return ret

        def to_derivation_tree(self, tree: "Grammar.ParserDerivationTree"):
            if tree is None:
                return None
            children = self._rec_to_derivation_tree(tree.children)  # type: ignore[arg-type]
            return DerivationTree(
                tree.symbol,
                children,
                parent=tree.parent,
                sources=tree.sources,
                sender=tree.sender,
                recipient=tree.recipient,
                read_only=tree.read_only,
            )

        def complete(
            self,
            state: ParseState,
            table: list[Column],
            k: int,
            use_implicit: bool = False,
        ):
            for s in table[state.position].find_dot(state.nonterminal):
                dot_params = s.dot_params
                s = s.next()
                if state.nonterminal in self._rules:
                    s.append_child(
                        Grammar.ParserDerivationTree(
                            state.nonterminal, state.children, **dict(dot_params)
                        )
                    )
                else:
                    if use_implicit and state.nonterminal in self._implicit_rules:
                        s.append_child(
                            Grammar.ParserDerivationTree(
                                NonTerminal(state.nonterminal.symbol),
                                state.children,
                                **dict(s.dot_params),
                            )
                        )
                    else:
                        s.extend_children(state.children)
                table[k].add(s)

        def place_repetition_shortcut(self, table: list[Column], k: int):
            col = table[k]
            states = col.states
            beginner_nts = ["<__plus:", "<__star:"]

            found_beginners = set()
            for state in states:
                if any(
                    map(lambda b: state.nonterminal.symbol.startswith(b), beginner_nts)
                ):
                    found_beginners.add(state.symbols[0][0])

            for beginner in found_beginners:
                current_col_state = None
                for state in states:
                    if state.nonterminal == beginner:
                        if state.finished():
                            continue
                        if len(state.symbols) == 2 and state.dot == beginner:
                            current_col_state = state
                            break
                if current_col_state is None:
                    continue
                new_state = current_col_state
                origin_states = table[current_col_state.position].find_dot(
                    current_col_state.dot
                )
                if len(origin_states) != 1:
                    continue
                origin_state = origin_states[0]
                while not any(
                    map(
                        lambda b: origin_state.nonterminal.symbol.startswith(b),
                        beginner_nts,
                    )
                ):
                    new_state = ParseState(
                        new_state.nonterminal,
                        origin_state.position,
                        new_state.symbols,
                        new_state._dot,
                        [*origin_state.children, *new_state.children],
                        new_state.is_incomplete,
                    )
                    origin_states = table[new_state.position].find_dot(new_state.dot)
                    if len(origin_states) != 1:
                        new_state = None  # type: ignore[assignment]
                        break
                    origin_state = origin_states[0]

                if new_state is not None:
                    col.replace(current_col_state, new_state)

        def _parse_forest(
            self,
            word: str | bytes,
            start: str | NonTerminal = "<start>",
            *,
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            starter_bit=-1,
        ):
            """
            Parse a forest of input trees from `word`.
            `start` is the start symbol (default: `<start>`).
            if `allow_incomplete` is True, the function will return trees even if the input ends prematurely.
            """
            if isinstance(start, str):
                start = NonTerminal(start)
            self._clear_tmp()
            hookin_parent = deepcopy(hookin_parent)

            # LOGGER.debug(f"Parsing {word} into {start!s}")

            # Initialize the table
            table: list[Column] = [Column() for _ in range(len(word) + 1)]
            time_start = time.time()
            table[0].add(ParseState(self.implicit_start, 0, ((start, frozenset()),)))

            # Save the maximum scan position, so we can report errors
            self._max_position = -1

            # Index into the input word
            w = 0

            # Index into the current table.
            # Due to bits parsing, this may differ from the input position w.
            k = 0

            # If >= 0, indicates the next bit to be scanned (7-0)
            bit_count = starter_bit
            nr_bits_scanned = 0

            while k < len(table):
                # LOGGER.debug(f"Processing {len(table[k])} states at column {k}")

                # True iff we have processed all characters
                # (or some bits of the last character)
                at_end = w >= len(word)  # or (bit_count > 0 and w == len(word) - 1)
                for state in table[k]:
                    if state.finished():
                        # LOGGER.debug(f"Finished")
                        if state.nonterminal == self.implicit_start:
                            if at_end:
                                # LOGGER.debug(f"Found {len(state.children)} parse tree(s)")
                                for child in state.children:
                                    time_took = time.time() - time_start
                                    time_took = time_took * 1000
                                    self.elapsed_time += time_took
                                    # print(f"Parser took {time_took:4.2f}ms/{self.elapsed_time:4.2f}ms: {start} {word}")
                                    time_start = time.time()
                                    yield child

                        self.complete(state, table, k)
                    elif not state.is_incomplete:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k, hookin_parent)
                            # LOGGER.debug(f"Predicted {state} at position {w:#06x} ({w}) {word[w:]!r}")
                        else:
                            if isinstance(state.dot.symbol, int):
                                # Scan a bit
                                if bit_count < 0:
                                    bit_count = 7
                                match = self.scan_bit(
                                    state, word, table, k, w, bit_count, nr_bits_scanned
                                )
                                if match:
                                    # LOGGER.debug(f"Matched bit {state} at position {w:#06x} ({w}) {word[w:]!r}")
                                    pass
                            else:
                                # Scan a regex or a byte
                                if 0 <= bit_count <= 7:
                                    # LOGGER.warning(f"Position {w:#06x} ({w}): Parsing a byte while expecting bit {bit_count}. Check if bits come in multiples of eight")

                                    # We are still expecting bits here:
                                    #
                                    # * we may have _peeked_ at a bit,
                                    # without actually parsing it; or
                                    # * we may have a grammar with bits
                                    # that do not come in multiples of 8.
                                    #
                                    # In either case, we need to get back
                                    # to scanning bytes here.
                                    bit_count = -1

                                # LOGGER.debug(f"Checking byte(s) {state} at position {w:#06x} ({w}) {word[w:]!r}")
                                if state.dot.is_regex:
                                    match = self.scan_regex(
                                        state, word, table, k, w, mode
                                    )
                                else:
                                    match = self.scan_bytes(
                                        state, word, table, k, w, mode
                                    )
                    else:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k)

                if mode == Grammar.Parser.ParsingMode.INCOMPLETE and at_end:
                    for state in table[k]:
                        state.is_incomplete = True
                        if state.is_incomplete and state._dot == 0:
                            continue
                        if state.nonterminal == self.implicit_start:
                            for child in state.children:
                                if child not in self._incomplete:
                                    self._incomplete.add(child)
                                    yield child
                        self.complete(state, table, k)

                # LOGGER.debug(f"Scanned byte at position {w:#06x} ({w}); bit_count = {bit_count}")
                if bit_count >= 0:
                    # Advance by one bit
                    bit_count -= 1
                    nr_bits_scanned += 1
                if bit_count < 0:
                    # Advance to next byte
                    w += 1

                self.place_repetition_shortcut(table, k)

                k += 1

        def parse_forest(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ) -> Generator[tuple[DerivationTree, Any] | DerivationTree, None, None]:
            """
            Yield multiple parse alternatives, using a cache.
            """
            starter_bit = -1
            if isinstance(word, DerivationTree):
                if word.contains_bytes():
                    starter_bit = (word.count_terminals() - 1) % 8
                    word = word.to_bytes()
                else:
                    word = word.to_string()
            if isinstance(word, int):
                word = str(word)
            assert isinstance(word, str) or isinstance(word, bytes)

            if isinstance(start, str):
                start = NonTerminal(start)
            assert isinstance(start, NonTerminal)

            cache_key = (word, start, mode, hookin_parent)
            forest: list[DerivationTree]
            if cache_key in self._cache:
                forest = self._cache[cache_key]
                for tree in forest:
                    tree = deepcopy(tree)
                    if not include_controlflow:
                        tree = self.collapse(tree)
                        yield tree
                return

            self._incomplete = set()
            forest = []
            for tree in self._parse_forest(
                word,
                start,
                mode=mode,
                hookin_parent=hookin_parent,
                starter_bit=starter_bit,
            ):
                tree = self.to_derivation_tree(tree)
                forest.append(tree)
                if not include_controlflow:
                    tree = self.collapse(tree)
                yield tree
            # Cache entire forest
            self._cache[cache_key] = forest

        def parse_multiple(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ):
            """
            Yield multiple parse alternatives,
            even for incomplete inputs
            """
            return self.parse_forest(
                word,
                start,
                mode=mode,
                hookin_parent=hookin_parent,
                include_controlflow=include_controlflow,
            )

        def parse(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            hookin_parent: Optional[DerivationTree] = None,
            include_controlflow: bool = False,
        ):
            """
            Return the first parse alternative,
            or `None` if no parse is possible
            """
            tree_gen = self.parse_multiple(
                word,
                start=start,
                mode=mode,
                hookin_parent=hookin_parent,
                include_controlflow=include_controlflow,
            )
            return next(tree_gen, None)

        def max_position(self):
            """Return the maximum position reached during parsing."""
            return self._max_position

    def __init__(
        self,
        rules: Optional[dict[NonTerminal, Node]] = None,
        fuzzing_mode: Optional[FuzzingMode] = FuzzingMode.COMPLETE,
        local_variables: Optional[dict[str, Any]] = None,
        global_variables: Optional[dict[str, Any]] = None,
    ):
        self.rules = rules or {}
        self.generators: dict[NonTerminal, LiteralGenerator] = {}
        self.fuzzing_mode = fuzzing_mode
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._parser = Grammar.Parser(self)

    @staticmethod
    def _topological_sort(graph: dict[NonTerminal, set[NonTerminal]]):
        indegree: dict[Any, int] = defaultdict(int)
        queue = []

        for node in graph:
            for neighbour in graph[node]:
                indegree[neighbour] += 1
        for node in graph:
            if indegree[node] == 0:
                queue.append(node)

        topological_order = []
        while queue:
            node = queue.pop(0)
            topological_order.append(node)

            for neighbour in graph[node]:
                indegree[neighbour] -= 1

                if indegree[neighbour] == 0:
                    queue.append(neighbour)

        if len(topological_order) != len(graph):
            print("Cycle exists")
        return topological_order[::-1]

    def is_use_generator(self, tree: "DerivationTree"):
        symbol = tree.symbol
        if not isinstance(symbol, NonTerminal):
            return False
        if symbol not in self.generators:
            return False
        if tree is None:
            path = set()
        else:
            path = set(map(lambda x: x.symbol, tree.get_path()))
        generator_dependencies = self.generator_dependencies(symbol)
        intersection = path.intersection(set(generator_dependencies))
        return len(intersection) == 0

    def derive_sources(self, tree: "DerivationTree"):
        gen_symbol = tree.symbol
        if not isinstance(gen_symbol, NonTerminal):
            raise FandangoValueError(f"Tree {tree.symbol} is not a nonterminal")
        if tree.symbol not in self.generators:
            raise FandangoValueError(f"No generator found for tree {tree.symbol}")

        if not self.is_use_generator(tree):
            return []

        dependent_generators: dict[NonTerminal, set[NonTerminal]] = {gen_symbol: set()}
        for key, val in self.generators[gen_symbol].nonterminals.items():
            if val.symbol not in self.rules:
                closest = closest_match(str(val), self.rules.keys())
                raise FandangoValueError(
                    f"Symbol {val.symbol!s} not defined in grammar. Did you mean {closest!s}?"
                )

            if val.symbol not in self.generators:
                raise FandangoValueError(
                    f"{val.symbol}: Missing converter from {gen_symbol} ({val.symbol} ::= ... := f({gen_symbol}))"
                )

            dependent_generators[val.symbol] = self.generator_dependencies(val.symbol)
        dependent_gens = self._topological_sort(dependent_generators)
        dependent_gens.remove(gen_symbol)

        args = [tree]
        for symbol in dependent_gens:
            generated_param = self.generate(symbol, args)
            generated_param.sources = []
            generated_param._parent = tree
            for child in generated_param.children:
                self.populate_sources(child)
            args.append(generated_param)
        args.pop(0)
        return args

    def derive_generator_output(self, tree: "DerivationTree"):
        generated = self.generate(tree.nonterminal, tree.sources)
        return generated.children

    def populate_sources(self, tree: "DerivationTree"):
        self._rec_remove_sources(tree)
        self._populate_sources(tree)

    def _populate_sources(self, tree: "DerivationTree"):
        if self.is_use_generator(tree):
            tree.sources = self.derive_sources(tree)
            for child in tree.children:
                child.set_all_read_only(True)
            return
        for child in tree.children:
            self._populate_sources(child)

    def _rec_remove_sources(self, tree: "DerivationTree"):
        tree.sources = []
        for child in tree.children:
            self._rec_remove_sources(child)

    def generate_string(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
    ) -> tuple[list[DerivationTree], str]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            raise ValueError(f"{symbol}: no generator")

        sources_: dict[Symbol, DerivationTree]
        if sources is None:
            sources_ = dict()
        else:
            sources_ = {tree.symbol: tree for tree in sources}
        generator = self.generators[symbol]

        local_variables = self._local_variables.copy()
        for id, nonterminal in generator.nonterminals.items():
            if nonterminal.symbol not in sources_:
                raise FandangoValueError(
                    f"{nonterminal.symbol}: missing generator parameter"
                )
            local_variables[id] = sources_[nonterminal.symbol]

        return list(sources_.values()), eval(
            generator.call, self._global_variables, local_variables
        )

    def generator_dependencies(self, symbol: str | NonTerminal = "<start>"):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            return set()
        return set(
            map(lambda x: x.symbol, self.generators[symbol].nonterminals.values())
        )

    def generate(
        self,
        symbol: str | NonTerminal = "<start>",
        sources: Optional[list[DerivationTree]] = None,
    ) -> DerivationTree:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        sources, string = self.generate_string(symbol, sources)
        if not (
            isinstance(string, str)
            or isinstance(string, bytes)
            or isinstance(string, int)
            or isinstance(string, tuple)
        ):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string, bytes, int, or tuple (returned {string!r})"
            )

        if isinstance(string, tuple):
            string = str(DerivationTree.from_tree(string))
        tree = self.parse(string, symbol)
        if tree is None:
            raise FandangoParseError(
                f"Could not parse {string!r} (generated by {self.generators[symbol]}) into {symbol}"
            )
        tree.sources = [p.deepcopy(copy_parent=False) for p in sources]
        return tree

    def collapse(self, tree: Optional[DerivationTree]) -> DerivationTree:
        return self._parser.collapse(tree)

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
        in_message: bool = False,
        prefix_node: Optional[DerivationTree] = None,
    ) -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        if prefix_node is None:
            root = DerivationTree(start)
        else:
            root = prefix_node
        fuzzed_idx = len(root.children)
        NonTerminalNode(start).fuzz(root, self, max_nodes=max_nodes)
        root = root.children[fuzzed_idx]
        root._parent = None
        return root

    def update(self, grammar: Union["Grammar", dict[NonTerminal, Node]], prime=True):
        generators: dict[NonTerminal, LiteralGenerator]
        local_variables: dict[str, Any]
        global_variables: dict[str, Any]
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            local_variables = grammar._local_variables
            global_variables = grammar._global_variables
            rules = grammar.rules
            fuzzing_mode = grammar.fuzzing_mode
        else:
            rules = grammar
            generators = {}
            local_variables = {}
            global_variables = {}
            fuzzing_mode = FuzzingMode.COMPLETE

        self.rules.update(rules)
        self.fuzzing_mode = fuzzing_mode
        self.generators.update(generators)

        for symbol in rules.keys():
            # We're updating from a grammar with a rule, but no generator,
            # so we should remove the generator if it exists
            if symbol not in generators and symbol in self.generators:
                del self.generators[symbol]

        self._parser = Grammar.Parser(self)
        self._local_variables.update(local_variables)
        self._global_variables.update(global_variables)
        if prime:
            self.prime()

    def parse(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: Parser.ParsingMode = Parser.ParsingMode.COMPLETE,
        hookin_parent: Optional[DerivationTree] = None,
        include_controlflow: bool = False,
    ):
        return self._parser.parse(
            word,
            start,
            mode=mode,
            hookin_parent=hookin_parent,
            include_controlflow=include_controlflow,
        )

    def parse_forest(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: Parser.ParsingMode = Parser.ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ):
        return self._parser.parse_forest(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

    def parse_multiple(
        self,
        word: str | bytes | DerivationTree,
        start: str | NonTerminal = "<start>",
        mode: Parser.ParsingMode = Parser.ParsingMode.COMPLETE,
        include_controlflow: bool = False,
    ):
        return self._parser.parse_multiple(
            word, start, mode=mode, include_controlflow=include_controlflow
        )

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
                f"{key} ::= {str(value)}{' := ' + str(self.generators[key]) if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

    def msg_parties(self, *, include_recipients: bool = True) -> set:
        parties: set[str] = set()
        for rule in self.rules.values():
            parties |= rule.msg_parties(include_recipients=include_recipients)
        return parties

    def get_repr_for_rule(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return (
            f"{symbol} ::= {self.rules[symbol]}"
            f"{' := ' + str(self.generators[symbol]) if symbol in self.generators else ''}"
        )

    @staticmethod
    def dummy():
        return Grammar({})

    def set_generator(
        self, symbol: str | NonTerminal, param: str, searches_map: dict = {}
    ):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators[symbol] = LiteralGenerator(
            call=param, nonterminals=searches_map
        )

    def remove_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        self.generators.pop(symbol)

    def has_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return symbol in self.generators

    def get_generator(self, symbol: str | NonTerminal):
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        return self.generators.get(symbol, None)

    def update_parser(self):
        self._parser = Grammar.Parser(self)

    def compute_kpath_coverage(
        self, derivation_trees: list[DerivationTree], k: int
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

    def _generate_all_k_paths(self, k: int) -> set[tuple[Node, ...]]:
        """
        Computes the *k*-paths for this grammar, constructively. See: doi.org/10.1109/ASE.2019.00027

        :param k: The length of the paths.
        :return: All paths of length up to *k* within this grammar.
        """

        initial = set()
        initial_work: [Node] = [NonTerminalNode(name) for name in self.rules.keys()]  # type: ignore[misc, valid-type]
        while initial_work:
            node = initial_work.pop(0)
            if node in initial:
                continue
            initial.add(node)
            initial_work.extend(node.descendents(self))

        work: list[set[tuple[Node, ...]]] = [set((x,) for x in initial)]

        for _ in range(1, k):
            next_work = set()
            for base in work[-1]:
                for descendent in base[-1].descendents(self):
                    next_work.add(base + (descendent,))
            work.append(next_work)

        # return set.union(*work)
        return work[-1]

    @staticmethod
    def _extract_k_paths_from_tree(
        tree: DerivationTree, k: int
    ) -> set[tuple[str | bytes | int, ...]]:
        """
        Extracts all k-length paths (k-paths) from a derivation tree.
        """
        paths = set()

        def traverse(node: DerivationTree, current_path: tuple[str | bytes | int, ...]):
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
        nodes: list[Node] = sum(
            [self.visit(self.rules[symbol]) for symbol in self.rules], []
        )
        while nodes:
            node = nodes.pop(0)
            if node.node_type == NodeType.TERMINAL:
                continue
            elif node.node_type == NodeType.NON_TERMINAL:
                if node.symbol not in self.rules:  # type: ignore[attr-defined] # We're checking types manually
                    raise FandangoValueError(
                        f"Symbol {node.symbol} not found in grammar"  # type: ignore[attr-defined] # We're checking types manually
                    )
                if self.rules[node.symbol].distance_to_completion == float("inf"):  # type: ignore[attr-defined] # We're checking types manually
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        self.rules[node.symbol].distance_to_completion + 1  # type: ignore[attr-defined] # We're checking types manually
                    )
            elif node.node_type == NodeType.ALTERNATIVE:
                node.distance_to_completion = (
                    min([n.distance_to_completion for n in node.alternatives]) + 1  # type: ignore[attr-defined] # We're checking types manually
                )
                if node.distance_to_completion == float("inf"):
                    nodes.append(node)
            elif node.node_type == NodeType.CONCATENATION:
                if any([n.distance_to_completion == float("inf") for n in node.nodes]):  # type: ignore[attr-defined] # We're checking types manually
                    nodes.append(node)
                else:
                    node.distance_to_completion = (
                        sum([n.distance_to_completion for n in node.nodes]) + 1  # type: ignore[attr-defined] # We're checking types manually
                    )
            elif node.node_type == NodeType.REPETITION:
                if node.node.distance_to_completion == float("inf"):  # type: ignore[attr-defined] # We're checking types manually
                    nodes.append(node)
                else:
                    try:
                        min_rep = node.min(self, None)  # type: ignore[attr-defined] # We're checking types manually
                    except ValueError:
                        min_rep = 0
                    node.distance_to_completion = (
                        node.node.distance_to_completion * min_rep + 1  # type: ignore[attr-defined] # We're checking types manually
                    )
            else:
                raise FandangoValueError(f"Unknown node type {node.node_type}")

    def slice_parties(self, parties: list[str]) -> None:
        """
        Returns a new grammar that only contains the rules that are relevant to the given parties.
        """
        for expansion in self.rules.values():
            expansion.slice_parties(parties)
        self.fuzzing_mode = FuzzingMode.COMPLETE

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

    def compute_k_paths(self, k: int) -> set[tuple[Node, ...]]:
        """
        Computes all possible k-paths in the grammar.

        :param k: The length of the paths.
        :return: A set of tuples, each tuple representing a k-path as a sequence of symbols.
        """
        return self._generate_all_k_paths(k)

    def traverse_derivation(
        self,
        tree: DerivationTree,
        disambiguator: Optional[Disambiguator] = None,
        paths: Optional[set[tuple[Node, ...]]] = None,
        cur_path: Optional[tuple[Node, ...]] = None,
    ) -> set[tuple[Node, ...]]:
        if disambiguator is None:
            disambiguator = Disambiguator(self)
        if paths is None:
            paths = set()
        if tree.symbol.is_terminal:
            if cur_path is None:
                cur_path = (TerminalNode(tree.terminal),)
            paths.add(cur_path)
        else:
            if cur_path is None:
                cur_path = (NonTerminalNode(tree.nonterminal),)
            assert tree.symbol == typing.cast(NonTerminalNode, cur_path[-1]).symbol
            disambiguation = disambiguator.visit(self.rules[tree.nonterminal])
            for tree, path in zip(
                tree.children, disambiguation[tuple(c.symbol for c in tree.children)]
            ):
                self.traverse_derivation(tree, disambiguator, paths, cur_path + path)
        return paths

    def compute_grammar_coverage(
        self, derivation_trees: list[DerivationTree], k: int
    ) -> tuple[float, int, int]:
        """
        Compute the coverage of k-paths in the grammar based on the given derivation trees.

        :param derivation_trees: A list of derivation trees (solutions produced by FANDANGO).
        :param k: The length of the paths (k).
        :return: A float between 0 and 1 representing the coverage.
        """

        # Compute all possible k-paths in the grammar
        all_k_paths = self.compute_k_paths(k)

        disambiguator = Disambiguator(self)

        # Extract k-paths from the derivation trees
        covered_k_paths = set()
        for tree in derivation_trees:
            for path in self.traverse_derivation(tree, disambiguator):
                # for length in range(1, k + 1):
                for window in range(len(path) - k + 1):
                    covered_k_paths.add(path[window : window + k])

        # Compute coverage
        if not all_k_paths:
            raise FandangoValueError("No k-paths found in the grammar")

        return (
            len(covered_k_paths) / len(all_k_paths),
            len(covered_k_paths),
            len(all_k_paths),
        )

    def get_spec_env(self):
        return self._global_variables, self._local_variables

    def contains_type(self, tp: type, *, start="<start>") -> bool:
        """
        Return true if the grammar can produce an element of type `tp` (say, `int` or `bytes`).
        * `start`: a start symbol other than `<start>`.
        """
        if isinstance(start, str):
            start = NonTerminal(start)

        if start not in self.rules:
            raise FandangoValueError(f"Start symbol {start} not defined in grammar")

        # We start on the right hand side of the start symbol
        start_node = self.rules[start]
        seen = set()

        def node_matches(node):
            if node in seen:
                return False
            seen.add(node)

            if isinstance(node, TerminalNode) and isinstance(node.symbol.symbol, tp):
                return True
            if any(node_matches(child) for child in node.children()):
                return True
            if isinstance(node, NonTerminalNode):
                return node_matches(self.rules[node.symbol])
            return False

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

    def set_max_repetition(self, max_rep: int):
        global MAX_REPETITIONS
        MAX_REPETITIONS = max_rep

    def get_max_repetition(self):
        return MAX_REPETITIONS
