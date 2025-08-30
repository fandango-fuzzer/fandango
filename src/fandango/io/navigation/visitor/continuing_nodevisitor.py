from typing import Optional

from fandango.language.tree import DerivationTree
from fandango.language import Grammar, NonTerminal
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Option, Plus, Star
from fandango.language.grammar.nodes.terminal import TerminalNode


class GrammarKeyError(KeyError):
    pass


class ContinuingNodeVisitor(NodeVisitor):
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

    def find(self, tree: Optional[DerivationTree] = None):
        if tree is None:
            self.tree = DerivationTree(NonTerminal("<start>"))
        else:
            self.tree = tree
        self.current_path = []
        self.current_tree = []
        self.current_path.append((self.tree.nonterminal, False))
        if len(self.tree.children) == 0:
            self.current_tree = [None]
        else:
            self.current_tree = [[self.tree.children[0]]]

        self.visit(self.grammar.rules[self.current_path[-1][0]])
        self.current_tree.pop()
        self.current_path.pop()

    def on_enter_controlflow(self, expected_nt: str):
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

    def on_leave_controlflow(self):
        self.current_tree.pop()
        self.current_path.pop()

    def visitNonTerminalNode(self, node: NonTerminalNode):
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
            result = self.visit(self.grammar.rules[node.symbol])
            return result
        finally:
            self.current_path.pop()
            self.current_path_collapsed.pop()
            self.current_tree.pop()

    def onNonTerminalNodeVisit(
        self, node: NonTerminalNode, is_exploring: bool
    ) -> tuple[bool, bool]:
        raise NotImplementedError()

    def onTerminalNodeVisit(self, node: TerminalNode, is_exploring: bool):
        raise NotImplementedError()

    def visitTerminalNode(self, node: TerminalNode):
        tree = self.current_tree[-1]
        return self.onTerminalNodeVisit(node, tree is None)

    def visitConcatenation(self, node: Concatenation):
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
        self.on_enter_controlflow(f"<__{node.id}>")
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
                except GrammarKeyError:
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
        self.on_enter_controlflow(f"<__{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitRepetitionType(self, node: Repetition):
        tree = self.current_tree[-1]
        continue_exploring = True
        tree_len = 0
        if tree is not None and len(tree) != 0:
            tree_len = len(tree)
            self.current_tree.append([tree[-1]])
            continue_exploring = self.visit(node.node)
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
        if continue_exploring and tree_len < rep_max:
            self.current_tree.append(None)
            continue_exploring = self.visit(node.node)
            self.current_tree.pop()
            if continue_exploring:
                return continue_exploring
        if tree_len >= rep_min:
            return True
        return continue_exploring

    def visitStar(self, node: Star):
        self.on_enter_controlflow(f"<__{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitPlus(self, node: Plus):
        self.on_enter_controlflow(f"<__{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret

    def visitOption(self, node: Option):
        self.on_enter_controlflow(f"<__{node.id}>")
        ret = self.visitRepetitionType(node)
        self.on_leave_controlflow()
        return ret
