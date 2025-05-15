import abc
import enum
import random
import typing
from collections import defaultdict

import exrex

from copy import deepcopy
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple, Union, Generator

from fandango.language.symbol import NonTerminal, Symbol, Terminal
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER

from fandango import FandangoValueError

from thefuzz import process as thefuzz_process


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


class Node(abc.ABC):
    def __init__(
        self, node_type: NodeType, distance_to_completion: float = float("inf")
    ):
        self.node_type = node_type
        self.distance_to_completion = distance_to_completion

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
        return

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

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
    def __init__(self, alternatives: list[Node]):
        super().__init__(NodeType.ALTERNATIVE)
        self.alternatives = alternatives

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
        if self.distance_to_completion >= max_nodes:
            min_ = min(self.alternatives, key=lambda x: x.distance_to_completion)
            random.choice(
                [
                    a
                    for a in self.alternatives
                    if a.distance_to_completion <= min_.distance_to_completion
                ]
            ).fuzz(parent, grammar, 0)
            return
        random.choice(self.alternatives).fuzz(parent, grammar, max_nodes - 1)

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

    def __str__(self):
        return "(" + " | ".join(map(str, self.alternatives)) + ")"

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from self.alternatives


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        super().__init__(NodeType.CONCATENATION)
        self.nodes = nodes

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
        prev_parent_size = parent.size()
        for node in self.nodes:
            if node.distance_to_completion >= max_nodes:
                node.fuzz(parent, grammar, 0)
            else:
                node.fuzz(parent, grammar, max_nodes - 1)
            max_nodes -= parent.size() - prev_parent_size
            prev_parent_size = parent.size()

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

    def __str__(self):
        return " ".join(map(str, self.nodes))

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from self.nodes


class Repetition(Node):
    def __init__(self, node: Node, min_=("0", [], {}), max_=(f"{None}", [], {})):
        super().__init__(NodeType.REPETITION)
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

    def _compute_rep_bound(self, grammar: "Grammar", tree: "DerivationTree", expr_data):
        expr, _, searches = expr_data
        if expr == "None":
            expr = f"{MAX_REPETITIONS}"
        local_cpy = grammar._local_variables.copy()

        if len(searches) == 0:
            return eval(expr, grammar._global_variables, local_cpy), True
        if tree is None:
            raise FandangoValueError("Need `tree` argument if symbols present")

        nodes = []
        for name, search in searches.items():
            nodes.extend(
                [(name, container) for container in search.find(tree.get_root())]
            )
        for _, container in nodes:
            container.evaluate().set_all_read_only(True)
        local_cpy.update({name: container.evaluate() for name, container in nodes})
        for name, _ in nodes:
            if not isinstance(local_cpy[name], DerivationTree):
                continue
            local_cpy[name].set_all_read_only(True)
        return eval(expr, grammar._global_variables, local_cpy), False

    def min(self, grammar: "Grammar", tree: "DerivationTree" = None):
        if self.static_min is None:
            current_min, is_static = self._compute_rep_bound(
                grammar, tree, self.expr_data_min
            )
            if is_static:
                self.static_min = current_min
            return current_min
        else:
            return self.static_min

    def max(self, grammar: "Grammar", tree: "DerivationTree" = None):
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

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
        prev_parent_size = parent.size()

        current_min = self.min(grammar, parent.get_root())
        current_max = self.max(grammar, parent.get_root())

        for rep in range(random.randint(current_min, current_max)):
            if self.node.distance_to_completion >= max_nodes:
                if rep > current_min:
                    break
                self.node.fuzz(parent, grammar, 0)
            else:
                self.node.fuzz(parent, grammar, max_nodes - 1)
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
        base = []
        # Todo: Context from DerivationTree is missing. Repetitions that depend on a value within the tree will cause a crash.
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


class Star(Repetition):
    def __init__(self, node: Node, max_repetitions: int = 5):
        super().__init__(node, ("0", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitStar(self)

    def __repr__(self):
        return f"{self.node}*"

    def __str__(self):
        return f"{self.node!s}*"


class Plus(Repetition):
    def __init__(self, node: Node, max_repetitions: int = 5):
        super().__init__(node, ("1", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitPlus(self)

    def __repr__(self):
        return f"{self.node}+"

    def __str__(self):
        return f"{self.node!s}+"


class Option(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, ("0", [], {}), ("1", [], {}))

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitOption(self)

    def __repr__(self):
        return f"{self.node}?"

    def __str__(self):
        return f"{self.node!s}?"

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield from (self.node, TerminalNode(Terminal("")))


class NonTerminalNode(Node):
    def __init__(self, symbol: NonTerminal):
        super().__init__(NodeType.NON_TERMINAL)
        self.symbol = symbol

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
        if self.symbol not in grammar:
            raise FandangoValueError(f"Symbol {self.symbol} not found in grammar")
        dummy_current_tree = DerivationTree(self.symbol)
        parent.add_child(dummy_current_tree)

        if grammar.is_use_generator(dummy_current_tree):
            dependencies = grammar.generator_dependencies(self.symbol)
            for nt in dependencies:
                NonTerminalNode(nt).fuzz(dummy_current_tree, grammar, max_nodes - 1)
            generated = grammar.generate(self.symbol, dummy_current_tree.children)
            # Prevent children from being overwritten without executing generator
            generated.set_all_read_only(True)
            generated.read_only = False
            parent.set_children(parent.children[:-1])
            parent.add_child(generated)
            return
        parent.set_children(parent.children[:-1])

        current_tree = DerivationTree(self.symbol)
        parent.add_child(current_tree)
        grammar[self.symbol].fuzz(current_tree, grammar, max_nodes - 1)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __str__(self):
        return self.symbol._repr()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)

    def descendents(self, grammar: "Grammar") -> Iterator["Node"]:
        yield grammar.rules[self.symbol]


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        super().__init__(NodeType.TERMINAL, 0)
        self.symbol = symbol

    def fuzz(self, parent: "DerivationTree", grammar: "Grammar", max_nodes: int = 100):
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
        return str(self.call)

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

    def fuzz(self, grammar: "Grammar", max_nodes: int = 100) -> List[DerivationTree]:
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
    def __init__(self, grammar: "Grammar"):
        self.known_disambiguations = {}
        self.grammar = grammar

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
        implicit_alternative = next(node.descendents(self.grammar))
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


class ParseState:
    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: Tuple[tuple[Symbol, frozenset[tuple[str, any]]], ...],
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
        return self.symbols[self._dot][0] if self._dot < len(self.symbols) else None

    @property
    def dot_params(self) -> frozenset[tuple[str, any]]:
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
    def __init__(self, states: Optional[List[ParseState]] = None):
        self.states = states or []
        self.dot_map = dict[NonTerminal, list[ParseState]]()
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

    def update(self, states: Set[ParseState]):
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
            children: Optional[List["DerivationTree"]] = None,
            *,
            parent: Optional["DerivationTree"] = None,
            read_only: bool = False,
        ):
            super().__init__(
                symbol, children, parent=parent, sources=[], read_only=read_only
            )

        def set_children(self, children: List["DerivationTree"]):
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
            self.grammar_rules: Dict[NonTerminal, Node] = grammar.rules
            self.grammar = grammar
            self._rules = {}
            self._implicit_rules = {}
            self._context_rules: dict[
                NonTerminal, tuple[Node, tuple[NonTerminal, frozenset]]
            ] = dict()
            self.alternative_count = 0
            self.concatenation_count = 0
            self.repetition_count = 0
            self.star_count = 0
            self.plus_count = 0
            self.option_count = 0
            self._process()
            self._cache: Dict[Tuple[str, NonTerminal], DerivationTree, bool] = {}
            self._incomplete = set()
            self._max_position = -1

        def _process(self):
            self._rules.clear()
            self._implicit_rules.clear()
            self._context_rules.clear()
            self.alternative_count = 0
            self.concatenation_count = 0
            self.repetition_count = 0
            self.star_count = 0
            self.plus_count = 0
            self.option_count = 0
            for nonterminal in self.grammar_rules:
                self.set_rule(nonterminal, self.visit(self.grammar_rules[nonterminal]))

            for nonterminal in self._implicit_rules:
                self._implicit_rules[nonterminal] = {
                    tuple(a) for a in self._implicit_rules[nonterminal]
                }

        def set_implicit_rule(
            self, rule: List[List[NonTerminal]]
        ) -> tuple[NonTerminal, frozenset]:
            nonterminal = NonTerminal(f"<*{len(self._implicit_rules)}*>")
            self._implicit_rules[nonterminal] = rule
            return (nonterminal, frozenset())

        def set_rule(
            self,
            nonterminal: NonTerminal,
            rule: List[List[tuple[NonTerminal, frozenset]]],
        ):
            self._rules[nonterminal] = {tuple(a) for a in rule}

        def set_context_rule(
            self, node: Node, non_terminal: tuple[NonTerminal, frozenset]
        ) -> NonTerminal:
            nonterminal = NonTerminal(f"<*ctx_{len(self._context_rules)}*>")
            self._context_rules[nonterminal] = (node, non_terminal)
            return nonterminal

        def default_result(self):
            return []

        def aggregate_results(self, aggregate, result):
            aggregate.extend(result)
            return aggregate

        def visitAlternative(self, node: Alternative):
            result = self.visitChildren(node)
            intermediate_nt = NonTerminal(
                f"<__{NodeType.ALTERNATIVE}:{self.alternative_count}>"
            )
            self.set_rule(intermediate_nt, result)
            self.alternative_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitConcatenation(self, node: Concatenation):
            result = [[]]
            for child in node.children():
                to_add = self.visit(child)
                new_result = []
                for r in result:
                    for a in to_add:
                        new_result.append(r + a)
                result = new_result
            intermediate_nt = NonTerminal(
                f"<__{NodeType.CONCATENATION}:{self.concatenation_count}>"
            )
            self.set_rule(intermediate_nt, result)
            self.concatenation_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitRepetition(
            self,
            node: Repetition,
            nt: tuple[NonTerminal, frozenset] = None,
            tree: DerivationTree = None,
        ):
            if nt is None:
                alternatives = self.visit(node.node)
                nt = self.set_implicit_rule(alternatives)

                if len(node.get_access_points()) != 0:
                    i_nt = self.set_context_rule(node, nt)
                    return [[(i_nt, frozenset())]]

            prev = None
            node_min = node.min(self.grammar, tree)
            node_max = node.max(self.grammar, tree)
            for rep in range(node_min, node_max):
                alts = [[nt]]
                if prev is not None:
                    alts.append([nt, prev])
                prev = self.set_implicit_rule(alts)
            alts = [node_min * [nt]]
            if prev is not None:
                alts.append(node_min * [nt] + [prev])
            min_nt = self.set_implicit_rule(alts)
            intermediate_nt = NonTerminal(
                f"<__{NodeType.REPETITION}:{self.repetition_count}>"
            )
            self.set_rule(intermediate_nt, [[min_nt]])
            self.repetition_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitStar(self, node: Star):
            alternatives = [[]]
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r + [nt])
            result = [[nt]]
            intermediate_nt = NonTerminal(f"<__{NodeType.STAR}:{self.star_count}>")
            self.set_rule(intermediate_nt, result)
            self.star_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitPlus(self, node: Plus):
            alternatives = []
            nt = self.set_implicit_rule(alternatives)
            for r in self.visit(node.node):
                alternatives.append(r)
                alternatives.append(r + [nt])
            result = [[nt]]
            intermediate_nt = NonTerminal(f"<__{NodeType.PLUS}:{self.plus_count}>")
            self.set_rule(intermediate_nt, result)
            self.plus_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitOption(self, node: Option):
            result = [[(Terminal(""), frozenset())]] + self.visit(node.node)
            intermediate_nt = NonTerminal(f"<__{NodeType.OPTION}:{self.option_count}>")
            self.set_rule(intermediate_nt, result)
            self.option_count += 1
            return [[(intermediate_nt, frozenset())]]

        def visitNonTerminalNode(self, node: NonTerminalNode):
            params = dict()
            params = frozenset(params.items())
            return [[(node.symbol, params)]]

        def visitTerminalNode(self, node: TerminalNode):
            return [[(node.symbol, frozenset())]]

        def collapse(self, tree: DerivationTree):
            if isinstance(tree.symbol, NonTerminal):
                if tree.symbol.symbol.startswith("<__"):
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
                if tree.symbol.symbol.startswith("<__"):
                    return reduced

            return [
                DerivationTree(
                    tree.symbol,
                    children=reduced,
                    sources=tree.sources,
                    read_only=tree.read_only,
                )
            ]

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
            elif state.dot in self._context_rules:
                node, nt = self._context_rules[state.dot]
                self.predict_ctx_rule(state, table, k, node, nt)

        def construct_incomplete_tree(
            self, state: ParseState, table: List[Set[ParseState] | Column]
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
                        **dict(current_state.dot_params),
                    )
                else:
                    current_tree = Grammar.ParserDerivationTree(
                        current_state.nonterminal,
                        [*current_state.children, current_tree],
                        **dict(current_state.dot_params),
                    )

            return current_tree.children[0]

        def predict_ctx_rule(
            self,
            state: ParseState,
            table: List[Set[ParseState] | Column],
            k: int,
            node: Node,
            nt_rule,
        ):
            if not isinstance(node, Repetition):
                raise FandangoValueError(f"Node {node} needs to be a Repetition")

            tree = self.construct_incomplete_tree(state, table)
            tree = self.collapse(tree)
            try:
                [[context_nt]] = self.visitRepetition(node, nt_rule, tree)
            except (ValueError, FandangoValueError):
                return

            new_symbols = []
            for symbol, dot_params in state.symbols:
                if symbol == state.dot:
                    new_symbols.append(context_nt)
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
            state.symbols = tuple(new_symbols)
            for nonterminal in self._implicit_rules:
                self._implicit_rules[nonterminal] = {
                    tuple(a) for a in self._implicit_rules[nonterminal]
                }
            self.predict(state, table, k)

        def scan_bit(
            self,
            state: ParseState,
            word: str | bytes,
            table: List[Set[ParseState] | Column],
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
            if not match:
                # LOGGER.debug(f"No match")
                return False

            # Found a match
            # LOGGER.debug(f"Found bit {bit}")
            next_state = state.next()
            tree = Grammar.ParserDerivationTree(Terminal(bit))
            next_state.children.append(tree)
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

            assert not isinstance(state.dot.symbol, int)
            assert not state.dot.is_regex

            # LOGGER.debug(f"Checking byte(s) {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

            match, match_length = state.dot.check(word[w:])
            if not match:
                return False

            # Found a match
            # LOGGER.debug(f"Matched byte(s) {state.dot!r} at position {w:#06x} ({w}) (len = {match_length}) {word[w:w + match_length]!r}")
            next_state = state.next()
            next_state.children.append(
                Grammar.ParserDerivationTree(Terminal(word[w : w + match_length]))
            )
            table[k + match_length].add(next_state)
            # LOGGER.debug(f"Next state: {next_state} at column {k + match_length}")
            self._max_position = max(self._max_position, w + match_length)

            return True

        def scan_regex(
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
            Return (True, #bytes) if bytes were matched, (False, 0) otherwise.
            """

            assert not isinstance(state.dot.symbol, int)
            assert state.dot.is_regex

            # LOGGER.debug(f"Checking regex {state.dot!r} at position {w:#06x} ({w}) {word[w:]!r}")

            match, match_length = state.dot.check(word[w:])
            if not match:
                return False

            # Found a match
            # LOGGER.debug(f"Matched regex {state.dot!r} at position {w:#06x} ({w}) (len = {match_length}) {word[w:w+match_length]!r}")
            next_state = state.next()
            next_state.children.append(
                Grammar.ParserDerivationTree(Terminal(word[w : w + match_length]))
            )
            table[k + match_length].add(next_state)
            # LOGGER.debug(f"Next state: {next_state} at column {k + match_length}")
            self._max_position = max(self._max_position, w + match_length)
            return True

        def _rec_to_derivation_tree(self, tree: list["Grammar.ParserDerivationTree"]):
            ret = []
            for child in tree:
                children = self._rec_to_derivation_tree(child.children)
                ret.append(
                    DerivationTree(
                        child.symbol,
                        children,
                        parent=child.parent,
                        sources=child.sources,
                        read_only=child.read_only,
                    )
                )
            return ret

        def to_derivation_tree(self, tree: "Grammar.ParserDerivationTree"):
            children = self._rec_to_derivation_tree(tree.children)
            return DerivationTree(
                tree.symbol,
                children,
                parent=tree.parent,
                sources=tree.sources,
                read_only=tree.read_only,
            )

        def complete(
            self,
            state: ParseState,
            table: List[Set[ParseState] | Column],
            k: int,
            use_implicit: bool = False,
        ):
            for s in table[state.position].find_dot(state.nonterminal):
                dot_params = s.dot_params
                s = s.next()
                table[k].add(s)
                if state.nonterminal in self._rules:
                    s.children.append(
                        Grammar.ParserDerivationTree(
                            state.nonterminal, state.children, **dict(dot_params)
                        )
                    )
                else:
                    if use_implicit and state.nonterminal in self._implicit_rules:
                        s.children.append(
                            Grammar.ParserDerivationTree(
                                NonTerminal(state.nonterminal.symbol),
                                state.children,
                                **dict(s.dot_params),
                            )
                        )
                    else:
                        s.children.extend(state.children)

        def place_repetition_shortcut(self, table: List[Column], k: int):
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
                        continue
                    origin_state = origin_states[0]

                if new_state is not None:
                    col.replace(current_col_state, new_state)

        def _parse_forest(
            self,
            word: str,
            start: str | NonTerminal = "<start>",
            *,
            mode: ParsingMode = ParsingMode.COMPLETE,
        ):
            """
            Parse a forest of input trees from `word`.
            `start` is the start symbol (default: `<start>`).
            if `allow_incomplete` is True, the function will return trees even if the input ends prematurely.
            """
            if isinstance(start, str):
                start = NonTerminal(start)

            # LOGGER.debug(f"Parsing {word} into {start!s}")

            # Initialize the table
            table: list[set[ParseState] | Column] = [
                Column() for _ in range(len(word) + 1)
            ]
            implicit_start = NonTerminal("<*start*>")
            self._process()
            table[0].add(ParseState(implicit_start, 0, ((start, frozenset()),)))

            # Save the maximum scan position, so we can report errors
            self._max_position = -1

            # Index into the input word
            w = 0

            # Index into the current table.
            # Due to bits parsing, this may differ from the input position w.
            k = 0

            # If >= 0, indicates the next bit to be scanned (7-0)
            bit_count = -1
            nr_bits_scanned = 0

            while k < len(table):
                # LOGGER.debug(f"Processing {len(table[k])} states at column {k}")
                for state in table[k]:
                    # True iff we have processed all characters
                    # (or some bits of the last character)
                    at_end = w >= len(word)  # or (bit_count > 0 and w == len(word) - 1)

                    if at_end:
                        if mode == Grammar.Parser.ParsingMode.INCOMPLETE:
                            if state.nonterminal == implicit_start:
                                self._incomplete.update(state.children)
                            state.is_incomplete = True
                            self.complete(state, table, k)

                    if state.finished():
                        # LOGGER.debug(f"Finished")
                        if state.nonterminal == implicit_start:
                            if at_end:
                                # LOGGER.debug(f"Found {len(state.children)} parse tree(s)")
                                for child in state.children:
                                    yield child

                        self.complete(state, table, k)
                    elif not state.is_incomplete:
                        if state.next_symbol_is_nonterminal():
                            self.predict(state, table, k)
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
                                    match = self.scan_regex(state, word, table, k, w)
                                else:
                                    match = self.scan_bytes(state, word, table, k, w)

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
            include_controlflow: bool = False,
            allow_incomplete: bool = False,
        ) -> Generator[DerivationTree, None, None]:
            """
            Yield multiple parse alternatives, using a cache.
            """
            if isinstance(word, DerivationTree):
                word = word.value()  # type: ignore
            if isinstance(word, int):
                word = str(word)
            assert isinstance(word, str) or isinstance(word, bytes)

            if isinstance(start, str):
                start = NonTerminal(start)
            assert isinstance(start, NonTerminal)

            cache_key = (word, start, mode)
            if cache_key in self._cache:
                forest = self._cache[cache_key]
                for tree in forest:
                    tree = deepcopy(tree)
                    if include_controlflow:
                        yield tree
                    else:
                        yield self.collapse(tree)
                return

            self._incomplete = set()
            forest = []
            for tree in self._parse_forest(word, start, mode=mode):
                tree = self.to_derivation_tree(tree)
                forest.append(tree)
                if include_controlflow:
                    yield tree
                else:
                    yield self.collapse(tree)

            if mode == Grammar.Parser.ParsingMode.INCOMPLETE:
                for tree in self._incomplete:
                    forest.append(tree)
                    if include_controlflow:
                        yield tree
                    else:
                        yield self.collapse(tree)

            # Cache entire forest
            self._cache[cache_key] = forest

        def parse_multiple(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            include_controlflow: bool = False,
        ):
            """
            Yield multiple parse alternatives,
            even for incomplete inputs
            """
            return self.parse_forest(
                word, start, mode=mode, include_controlflow=include_controlflow
            )

        def parse(
            self,
            word: str | bytes | DerivationTree,
            start: str | NonTerminal = "<start>",
            mode: ParsingMode = ParsingMode.COMPLETE,
            include_controlflow: bool = False,
        ):
            """
            Return the first parse alternative,
            or `None` if no parse is possible
            """
            tree_gen = self.parse_forest(
                word, start=start, mode=mode, include_controlflow=include_controlflow
            )
            return next(tree_gen, None)

        def max_position(self):
            """Return the maximum position reached during parsing."""
            return self._max_position

    def __init__(
        self,
        rules: Optional[Dict[NonTerminal, Node]] = None,
        local_variables: Optional[Dict[str, Any]] = None,
        global_variables: Optional[Dict[str, Any]] = None,
    ):
        self.rules = rules or {}
        self.generators: Dict[NonTerminal, LiteralGenerator] = {}
        self._parser = Grammar.Parser(self)
        self._local_variables = local_variables or {}
        self._global_variables = global_variables or {}
        self._visited = set()

    @staticmethod
    def _topological_sort(graph: dict[str, set[str]]):
        indegree = defaultdict(int)
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
            path = tree.get_path()
        generator_dependencies = self.generator_dependencies(symbol)
        intersection = set(path).intersection(set(generator_dependencies))
        return len(intersection) == 0

    def derive_sources(self, tree: "DerivationTree"):
        gen_symbol = tree.symbol
        if not isinstance(gen_symbol, NonTerminal):
            raise FandangoValueError(f"Tree {tree.symbol} is not a nonterminal")
        if tree.symbol not in self.generators:
            raise FandangoValueError(f"No generator found for tree {tree.symbol}")

        if not self.is_use_generator(tree):
            return []

        dependent_generators = {gen_symbol: set()}
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
        dependent_generators = self._topological_sort(dependent_generators)
        dependent_generators.remove(gen_symbol)

        args = [tree]
        for symbol in dependent_generators:
            generated_param = self.generate(symbol, args)
            generated_param.sources = []
            generated_param._parent = tree
            for child in generated_param.children:
                self.populate_sources(child)
            args.append(generated_param)
        args.pop(0)
        return args

    def derive_generator_output(self, tree: "DerivationTree"):
        generated = self.generate(tree.symbol, tree.sources)
        return generated.children

    def populate_sources(self, tree: "DerivationTree"):
        self._rec_remove_sources(tree)
        self._populate_sources(tree)

    def _populate_sources(self, tree: "DerivationTree"):
        if tree.symbol in self.generators:
            tree.sources = self.derive_sources(tree)
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
        sources: list[DerivationTree] = None,
    ) -> tuple[list[DerivationTree], str]:
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        if self.generators[symbol] is None:
            raise ValueError(f"{symbol}: no generator")

        if sources is None:
            sources = dict()
        else:
            sources = {tree.symbol: tree for tree in sources}
        generator = self.generators[symbol]

        local_variables = self._local_variables.copy()
        for id, nonterminal in generator.nonterminals.items():
            if nonterminal.symbol not in sources:
                raise FandangoValueError(
                    f"{nonterminal.symbol}: missing generator parameter"
                )
            local_variables[id] = sources[nonterminal.symbol]

        return list(sources.values()), eval(
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
        sources, string = self.generate_string(symbol, sources)
        if not (
            isinstance(string, str)
            or isinstance(string, bytes)
            or isinstance(string, int)
            or isinstance(string, tuple)
        ):
            raise TypeError(
                f"Generator {self.generators[symbol]} must return string, bytes, int, or tuple"
            )

        if isinstance(string, tuple):
            tree = DerivationTree.from_tree(string)
        else:
            tree = self.parse(string, symbol)
        if tree is None:
            raise FandangoValueError(
                f"Could not parse {string!r} (generated by {self.generators[symbol]}) into {symbol}"
            )
        tree.sources = deepcopy(sources)
        return tree

    def fuzz(
        self,
        start: str | NonTerminal = "<start>",
        max_nodes: int = 50,
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

    def update(self, grammar: "Grammar" | Dict[NonTerminal, Node], prime=True):
        if isinstance(grammar, Grammar):
            generators = grammar.generators
            local_variables = grammar._local_variables
            global_variables = grammar._global_variables
            rules = grammar.rules
        else:
            rules = grammar
            generators = local_variables = global_variables = {}

        self.rules.update(rules)
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
        include_controlflow: bool = False,
    ):
        return self._parser.parse(
            word, start, mode=mode, include_controlflow=include_controlflow
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
                f"{key} ::= {str(value)}{' := ' + self.generators[key] if key in self.generators else ''}"
                for key, value in self.rules.items()
            ]
        )

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
            initial_work.extend(node.descendents(self))

        work: List[Set[Tuple[Node]]] = [set((x,) for x in initial)]

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
                    raise FandangoValueError(
                        f"Symbol {node.symbol} not found in grammar"
                    )
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
                    try:
                        min_rep = node.min(self, None)
                    except ValueError:
                        min_rep = 0
                    node.distance_to_completion = (
                        node.node.distance_to_completion * min_rep + 1
                    )
            else:
                raise FandangoValueError(f"Unknown node type {node.node_type}")

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
        disambiguator: Disambiguator = None,
        paths: Set[Tuple[Node, ...]] = None,
        cur_path: Tuple[Node, ...] = None,
    ) -> Set[Tuple[Node, ...]]:
        if disambiguator is None:
            disambiguator = Disambiguator(self)
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

    def contains_type(self, tp: type, *, start="<start>") -> bool:
        """
        Return true if the grammar can produce an element of type `tp` (say, `int` or `bytes`).
        * `start`: a start symbol other than `<start>`.
        """
        if isinstance(start, str):
            start = NonTerminal(start)

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
