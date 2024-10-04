import abc
import random
from typing import Dict, List, Optional

from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

MAX_REPETITIONS = 50


class Node(abc.ABC):
    def fuzz(self, rules: Dict[str, "Node"]) -> List[DerivationTree]:
        return ""

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        self.alternatives = alternatives

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return random.choice(self.alternatives).fuzz(rules)

    def __repr__(self):
        return "(" + "|".join(map(repr, self.alternatives)) + ")"


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return sum([node.fuzz(rules) for node in self.nodes], [])

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

    def __repr__(self):
        return f"{self.node}*"


class Plus(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 1)

    def __repr__(self):
        return f"{self.node}+"


class Option(Repetition):
    def __init__(self, node: Node):
        super().__init__(node, 0, 1)

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

    def __repr__(self):
        return self.symbol

    def __eq__(self, other):
        return isinstance(other, NonTerminalNode) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class TerminalNode(Node):
    def __init__(self, symbol: Terminal):
        self.symbol = symbol

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return [DerivationTree(self.symbol)]

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
