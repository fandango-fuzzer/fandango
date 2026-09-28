from collections.abc import Generator
from typing import Optional

from fandango.errors import FandangoValueError
from fandango.io.navigation.nested_steps import run_nested_steps
from fandango.language import Grammar, NonTerminal
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.tree import DerivationTree

VisitSteps = Generator[Node, bool, bool]


class GrammarKeyError(KeyError):
    pass


class ContinuingNodeVisitor(NodeVisitor[None, bool]):
    """
    For a given grammar and DerivationTree, this class
    finds possible upcoming message types, the nonterminals that generate them and the paths where the messages
    can be added to the DerivationTree.
    """

    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.tree: Optional[DerivationTree] = None
        self.current_tree: list[list[DerivationTree] | None] = []
        self.current_path: list[tuple[NonTerminal, bool]] = []
        self.current_path_collapsed: list[tuple[NonTerminal, bool]] = []

    def find(self, tree: Optional[DerivationTree] = None) -> None:
        self.tree = tree
        self.current_path = []
        self.current_tree = [None]
        if self.tree is not None:
            self.current_path.append((self.tree.nonterminal, False))
            self.current_path_collapsed.append((self.tree.nonterminal, False))
            if len(self.tree.children) != 0:
                self.current_tree = [[self.tree.children[0]]]
            self.visit(self.grammar.rules[self.current_path[-1][0]])
        else:
            self.current_path.append((NonTerminal("<start>"), True))
            self.current_path_collapsed.append((NonTerminal("<start>"), True))
            self.visit(NonTerminalNode(NonTerminal("<start>"), []))

        self.current_tree.pop()
        self.current_path.pop()
        self.current_path_collapsed.pop()

    def visit(self, node: Node) -> bool:
        return run_nested_steps(self._visit_steps(node), self._visit_steps)

    def _visit_steps(self, node: Node) -> VisitSteps:
        if isinstance(node, NonTerminalNode):
            return self._non_terminal_steps(node)
        if isinstance(node, Concatenation):
            return self._concatenation_steps(node)
        if isinstance(node, Alternative):
            return self._alternative_steps(node)
        if isinstance(node, Repetition):
            return self._repetition_steps(node)
        if isinstance(node, TerminalNode):
            return self._terminal_steps(node)
        if isinstance(node, CharSet):
            return self._char_set_steps(node)
        raise FandangoValueError(f"No visit steps for {type(node).__name__}")

    def on_enter_controlflow(self, expected_nt: str) -> None:
        tree = self.current_tree[-1]
        cf_nt = (NonTerminal(expected_nt), True)
        if tree is not None:
            if len(tree) != 1:
                raise GrammarKeyError(
                    "Expected len(tree) == 1 for controlflow entries!"
                )
            assert isinstance(tree[0].symbol, NonTerminal)
            nt_name = tree[0].symbol.name()
            if nt_name != expected_nt:
                raise GrammarKeyError("Symbol mismatch!")
            cf_nt = (NonTerminal(nt_name), False)
        self.current_tree.append(None if tree is None else tree[0].children)
        self.current_path.append(cf_nt)

    def on_leave_controlflow(self) -> None:
        self.current_tree.pop()
        self.current_path.pop()

    def _non_terminal_steps(self, node: NonTerminalNode) -> VisitSteps:
        tree = self.current_tree[-1]
        if tree is not None:
            if tree[0].symbol != node.symbol:
                raise GrammarKeyError("Symbol mismatch")

        self.current_tree.append(None if tree is None else tree[0].children)
        self.current_path.append((node.symbol, tree is None))
        self.current_path_collapsed.append((node.symbol, tree is None))

        try:
            continue_exploring, enter_non_terminal = self.onNonTerminalNodeVisit(
                node, tree is None
            )
            if not enter_non_terminal:
                return continue_exploring
            result = yield self.grammar.rules[node.symbol]
            return result
        finally:
            self.current_path.pop()
            self.current_path_collapsed.pop()
            self.current_tree.pop()

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        raise NotImplementedError()

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool) -> bool:
        raise NotImplementedError()

    def visitTerminalNode(self, node: TerminalNode) -> bool:
        tree = self.current_tree[-1]
        return self.onTerminalNodeVisit(node, tree is None)

    def _terminal_steps(self, node: TerminalNode) -> VisitSteps:
        yield from ()
        return self.visitTerminalNode(node)

    def _char_set_steps(self, node: CharSet) -> VisitSteps:
        yield from ()
        return self.visitCharSet(node)

    def _concatenation_steps(self, node: Concatenation) -> VisitSteps:
        self.on_enter_controlflow(f"<__{node.id}>")
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
                continue_exploring = yield node.nodes[child_idx]
                child_idx += 1
            finally:
                self.current_tree.pop()
        while continue_exploring and child_idx < len(node.children()):
            next_child = node.children()[child_idx]
            self.current_tree.append(None)
            continue_exploring = yield next_child
            self.current_tree.pop()
            child_idx += 1
        self.on_leave_controlflow()
        return continue_exploring

    def _alternative_steps(self, node: Alternative) -> VisitSteps:
        self.on_enter_controlflow(f"<__{node.id}>")
        tree = self.current_tree[-1]

        if tree is not None:
            continue_exploring = True
            self.current_tree.append([tree[0]])
            tree_depth = len(self.current_tree)
            path_depth = len(self.current_path)
            collapsed_path_depth = len(self.current_path_collapsed)
            found = False
            for alt in node.alternatives:
                if (
                    not isinstance(alt, TerminalNode)
                    and alt.to_symbol() != tree[0].symbol
                ):
                    continue
                try:
                    continue_exploring = yield alt
                    found = True
                except GrammarKeyError:
                    del self.current_tree[tree_depth:]
                    del self.current_path[path_depth:]
                    del self.current_path_collapsed[collapsed_path_depth:]
            self.current_tree.pop()
            self.on_leave_controlflow()
            if not found:
                raise GrammarKeyError("Alternative mismatch")
            return continue_exploring
        else:
            continue_exploring = False
            self.current_tree.append(None)
            for alt in node.alternatives:
                continue_exploring |= yield alt
            self.current_tree.pop()
            self.on_leave_controlflow()
            return continue_exploring

    def _repetition_steps(self, node: Repetition) -> VisitSteps:
        self.on_enter_controlflow(f"<__{node.id}>")
        ret = yield from self._repetition_type_steps(node)
        self.on_leave_controlflow()
        return ret

    def _repetition_type_steps(self, node: Repetition) -> VisitSteps:
        tree = self.current_tree[-1]
        last_complete = True
        tree_len = 0
        if tree is not None and len(tree) != 0:
            tree_len = len(tree)
            self.current_tree.append([tree[-1]])
            last_complete = yield node.node
            self.current_tree.pop()

        rep_min = node.min
        rep_max = node.max
        if node.bounds_constraint:
            prefix_tree = None
            for tree_list in self.current_tree[::-1]:
                if tree_list is None or len(tree_list) != 0:
                    continue
                prefix_tree = tree_list[-1].prefix()
                prefix_tree = self.grammar.collapse(prefix_tree.get_root())
                break
            assert prefix_tree is not None
            rep_min, _ = node.bounds_constraint.min(prefix_tree)
            rep_max, _ = node.bounds_constraint.max(prefix_tree)
        if not last_complete:
            return False
        if tree_len < rep_max:
            self.current_tree.append(None)
            can_continue = yield node.node
            self.current_tree.pop()
            if can_continue:
                return True
        if tree_len >= rep_min:
            return True
        return False
