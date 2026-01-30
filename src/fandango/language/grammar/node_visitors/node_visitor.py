import abc
from typing import Generic, TypeVar, cast
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition, Star, Plus, Option
from fandango.language.grammar.nodes.terminal import TerminalNode

AggregateType = TypeVar("AggregateType")
ResultType = TypeVar("ResultType")


class NodeVisitor(abc.ABC, Generic[AggregateType, ResultType]):
    def visit(self, node: Node) -> ResultType:
        return node.accept(self)

    def default_result(self) -> AggregateType:
        return None  # type: ignore[return-value]

    def aggregate_results(
        self, aggregate: AggregateType, result: ResultType
    ) -> AggregateType:
        return aggregate

    def visitChildren(self, node: Node) -> AggregateType:
        # noinspection PyNoneFunctionAssignment
        result = self.default_result()
        for child in node.children():
            # noinspection PyNoneFunctionAssignment
            result = self.aggregate_results(result, self.visit(child))
        return result

    def visitAlternative(self, node: Alternative) -> ResultType:
        return cast(ResultType, self.visitChildren(node))

    def visitConcatenation(self, node: Concatenation) -> ResultType:
        return cast(ResultType, self.visitChildren(node))

    def visitRepetition(self, node: Repetition) -> ResultType:
        return self.visit(node.node)

    def visitStar(self, node: Star) -> ResultType:
        return self.visit(node.node)

    def visitPlus(self, node: Plus) -> ResultType:
        return self.visit(node.node)

    def visitOption(self, node: Option) -> ResultType:
        return self.visit(node.node)

    def visitNonTerminalNode(self, _node: NonTerminalNode) -> ResultType:
        return cast(ResultType, self.default_result())

    def visitTerminalNode(self, _node: TerminalNode) -> ResultType:
        return cast(ResultType, self.default_result())

    def visitCharSet(self, _node: CharSet) -> ResultType:
        return cast(ResultType, self.default_result())
