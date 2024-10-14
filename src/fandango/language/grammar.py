import abc
import random
from typing import Dict, List, Optional

from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

MAX_REPETITIONS = 50


class Node(abc.ABC):
    def fuzz(self, rules: Dict[str, "Node"]) -> List[DerivationTree]:
        return ""

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

    def children(self):
        return []

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        self.alternatives = alternatives

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return random.choice(self.alternatives).fuzz(rules)

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitAlternative(self)

    def children(self):
        return self.alternatives

    def __getitem__(self, item):
        return self.alternatives.__getitem__(item)

    def __len__(self):
        return len(self.alternatives)

    def __repr__(self):
        return "(" + "|".join(map(repr, self.alternatives)) + ")"


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return sum([node.fuzz(rules) for node in self.nodes], [])

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


class Repetition(Node):
    def __init__(self, node: Node, min_: int = 0, max_: int = MAX_REPETITIONS):
        if min_ < 0:
            raise ValueError("Minimum repetitions must be greater than or equal to 0")
        if max_ <= 0:
            raise ValueError("Maximum repetitions must be greater than 0")
        self.node = node
        self.min = min_
        self.max = max_

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitRepetition(self)

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return sum(
            [self.node.fuzz(rules) for _ in range(random.randint(self.min, self.max))],
            [],
        )

    def __repr__(self):
        return f"{self.node}{{{self.min},{self.max}}}"


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


class NonTerminalNode(Node):
    def __init__(self, symbol: NonTerminal):
        self.symbol = symbol

    def fuzz(self, rules: Dict[NonTerminal, Node]) -> List[DerivationTree]:
        if self.symbol not in rules:
            raise ValueError(f"Symbol {self.symbol} not found in rules")
        children = rules[self.symbol].fuzz(rules)
        return [DerivationTree(self.symbol, children)]

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitNonTerminalNode(self)

    def __repr__(self):
        return self.symbol.__repr__()

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        self.symbol = symbol

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
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
        self.chars = chars

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        raise NotImplementedError("CharSet fuzzing not implemented")

    def accept(self, visitor: "NodeVisitor"):
        return visitor.visitCharSet(self)


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


class Grammar:
    def __init__(self, rules: Optional[Dict[NonTerminal, Node]] = None):
        self.rules = rules or {}

    def fuzz(self, start: str | NonTerminal = "<start>") -> DerivationTree:
        if isinstance(start, str):
            start = NonTerminal(start)
        return NonTerminalNode(start).fuzz(self.rules)[0]

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
        return "\n".join([f"{key} ::= {value};" for key, value in self.rules.items()])

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def dummy():
        return Grammar({})
