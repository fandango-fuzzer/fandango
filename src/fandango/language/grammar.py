import abc
import random
import copy
from typing import Dict, List, Optional

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

    def __eq__(self, other):
        return isinstance(other, NonTerminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class Terminal(Node):
    def __init__(self, symbol: str):
        self.symbol = symbol

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        return [DerivationTree(self)]

    @staticmethod
    def from_symbol(symbol: str) -> "Terminal":
        if symbol[0] == symbol[-1] == "'":
            while symbol and symbol[0] == symbol[-1] == "'":
                symbol = symbol[1:-1]
        elif symbol[0] == symbol[-1] == '"':
            while symbol and symbol[0] == symbol[-1] == '"':
                symbol = symbol[1:-1]
        return Terminal(symbol)

    def __repr__(self):
        return f'"{self.symbol}"'

    def __eq__(self, other):
        return isinstance(other, Terminal) and self.symbol == other.symbol

    def __hash__(self):
        return hash(self.symbol)


class CharSet(Node):
    def __init__(self, chars: str):
        self.chars = chars

    def fuzz(self, rules: Dict[str, "Node"]) -> List["DerivationTree"]:
        raise NotImplementedError("CharSet fuzzing not implemented")


class DerivationTree:
    """
    This class is used to represent a node in the derivation tree.
    """

    def __init__(
        self,
        symbol: NonTerminal | Terminal,
        children: Optional[List["DerivationTree"]] = None,
        parent: Optional["DerivationTree"] = None,
    ):
        self.symbol = symbol
        self.children = children or []
        self.parent = parent
        for child in self.children:
            child.parent = self

    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]

        # Create a new instance without copying the parent
        copied = DerivationTree(self.symbol, [])
        memo[id(self)] = copied

        # Deepcopy the children
        copied.children = [copy.deepcopy(child, memo) for child in self.children]

        # Set parent pointers
        for child in copied.children:
            child.parent = copied

        # Set the parent to None or update if necessary
        copied.parent = None  # or copy.deepcopy(self.parent, memo) if parent is needed

        return copied

    def __repr__(self):
        if isinstance(self.symbol, NonTerminal):
            return "".join([repr(child) for child in self.children])
        elif isinstance(self.symbol, Terminal):
            return self.symbol.symbol
        else:
            raise ValueError("Invalid symbol type")

    def to_int(self):
        try:
            int(self.__repr__())
        except ValueError:
            return None

    def to_float(self):
        try:
            int(self.__repr__())
        except ValueError:
            return None

    def to_complex(self):
        try:
            complex(self.__repr__())
        except ValueError:
            return None

    def is_int(self):
        try:
            int(self.__repr__())
        except ValueError:
            return False
        return True

    def is_float(self):
        try:
            float(self.__repr__())
        except ValueError:
            return False
        return True

    def is_complex(self):
        try:
            complex(self.__repr__())
        except ValueError:
            return False
        return True

    def is_num(self):
        return self.is_float()

    def __str__(self):
        return self.__repr__()


class Grammar:
    def __init__(self, rules: Dict[str, Node]):
        self.rules = rules

    def fuzz(self, start: str = "<start>") -> DerivationTree:
        return NonTerminal(start).fuzz(self.rules)[0]

    def __contains__(self, item: str):
        return item in self.rules

    def __getitem__(self, item: str):
        return self.rules[item]

    def __setitem__(self, key: str, value: Node):
        self.rules[key] = value

    def __delitem__(self, key: str):
        del self.rules[key]

    def __iter__(self):
        return iter(self.rules)

    def __len__(self):
        return len(self.rules)

    def __repr__(self):
        return "\n".join([f"{key} ::= {value};" for key, value in self.rules.items()])

    def __str__(self):
        return self.__repr__()
