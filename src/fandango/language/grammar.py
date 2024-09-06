import abc
import random
from typing import Dict, List


MAX_REPETITIONS = 20


class Node(abc.ABC):
    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        return ""

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        self.alternatives = alternatives

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        return random.choice(self.alternatives).fuzz(rules)

    def __repr__(self):
        return "(" + "|".join(map(repr, self.alternatives)) + ")"


class Concatenation(Node):
    def __init__(self, nodes: list[Node]):
        self.nodes = nodes

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
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

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        return sum([self.node.fuzz(rules) for _ in range(random.randint(self.min, self.max))], [])

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


class NonTerminal(Node):
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        if self.symbol not in rules:
            raise ValueError(f"Symbol {self.symbol} not found in rules")
        children = rules[self.symbol].fuzz(rules)
        return [DerivationTree(self, children)]

    def __repr__(self):
        return self.symbol


class Terminal(Node):
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        return [DerivationTree(self)]

    @staticmethod
    def from_symbol(symbol: str) -> "Terminal":
        if symbol[0] == symbol[-1] == "'":
            while symbol[0] == symbol[-1] == "'":
                symbol = symbol[1:-1]
        elif symbol[0] == symbol[-1] == '"':
            while symbol[0] == symbol[-1] == '"':
                symbol = symbol[1:-1]
        return Terminal(symbol)

    def __repr__(self):
        return f'"{self.symbol}"'


class CharSet(Node):
    def __init__(self, chars: str):
        self.chars = chars

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        raise NotImplementedError("CharSet fuzzing not implemented")


class DerivationTree:
    """
    This class is used to represent a node in the derivation tree.
    """

    def __init__(self, symbol: NonTerminal|Terminal, children: List["DerivationTree"] = None):
        self.symbol = symbol
        self.children = children or []

    def __repr__(self):
        if isinstance(self.symbol, NonTerminal):
            return "".join([repr(child) for child in self.children])
        elif isinstance(self.symbol, Terminal):
            return self.symbol.symbol
        else:
            raise ValueError("Invalid symbol type")

    def __str__(self):
        return self.__repr__()
    

class Grammar:
    def __init__(self, rules: Dict[str, Node]):
        self.rules = rules

    def fuzz(self, start: str = "<start>") -> DerivationTree:
        return NonTerminal(start).fuzz(self.rules)[0]