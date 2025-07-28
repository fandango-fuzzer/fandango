from typing import Optional
from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Star, Plus, Option
from fandango.language.grammar.nodes.terminal import TerminalNode


class NodeReplacer(NodeVisitor):
    def __init__(self, old_node: Node, new_node: Node):
        self.old_node = old_node
        self.new_node = new_node

    def replace(self, node: Node) -> Node:
        if node == self.old_node:
            return self.new_node
        return node

    def default_result(self) -> list[Node]:
        return []

    def aggregate_results(
        self, aggregate: list[Node], result: Optional[Node]
    ) -> list[Node]:
        if result is not None:
            aggregate.append(result)
        return aggregate

    def visitConcatenation(self, node: Concatenation) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Concatenation):
            replaced.nodes = self.visitChildren(replaced)
            return replaced
        else:
            return self.visit(replaced)

    def visitAlternative(self, node: Alternative) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Alternative):
            replaced.alternatives = self.visitChildren(replaced)
            return replaced
        else:
            return self.visit(replaced)

    def visitRepetition(self, node: Repetition) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Repetition):
            replaced.node = self.visit(replaced.node)
            return replaced
        else:
            return self.visit(replaced)

    def visitStar(self, node: Star) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Star):
            replaced.node = self.visit(replaced.node)
            return replaced
        else:
            return self.visit(replaced)

    def visitPlus(self, node: Plus) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Plus):
            replaced.node = self.visit(replaced.node)
            return replaced
        else:
            return self.visit(replaced)

    def visitOption(self, node: Option) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, Option):
            replaced.node = self.visit(replaced.node)
            return replaced
        else:
            return self.visit(replaced)

    def visitNonTerminalNode(self, node: NonTerminalNode) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, NonTerminalNode):
            return replaced
        else:
            return self.visit(replaced)

    def visitTerminalNode(self, node: TerminalNode) -> Node:
        replaced = self.replace(node)
        if isinstance(replaced, TerminalNode):
            return replaced
        else:
            return self.visit(replaced)
