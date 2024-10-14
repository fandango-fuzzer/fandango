import abc
import random
from typing import Dict, List, Optional

from fandango.language.symbol import NonTerminal, Terminal
from fandango.language.tree import DerivationTree

MAX_REPETITIONS = 50


class ParseResult:
    def __init__(
        self, trees: List[DerivationTree] | DerivationTree, remaining: str | bytes
    ):
        self.trees = trees
        self.remaining = remaining

    def append(self, tree: List[DerivationTree] | DerivationTree):
        if isinstance(self.trees, list):
            if isinstance(tree, list):
                self.trees.extend(tree)
            else:
                self.trees.append(tree)
        else:
            if isinstance(tree, list):
                self.trees = [self.trees, *tree]
            else:
                self.trees = [self.trees, tree]

    def offspring(self, tree: DerivationTree, remaining: str | bytes):
        new_result = ParseResult(self.trees, remaining)
        new_result.append(tree)
        return new_result

    def build(self, symbol: NonTerminal):
        if isinstance(self.trees, list):
            tree = DerivationTree(symbol, self.trees)
        else:
            tree = DerivationTree(symbol, [self.trees])
        return ParseResult(tree, self.remaining)

    def __repr__(self):
        return f"ParseResult({self.trees}, {self.remaining})"

    def __str__(self):
        return self.__repr__()


class Node(abc.ABC):
    def fuzz(self, rules: Dict[str, "Node"]) -> List[DerivationTree]:
        return ""

    def parse(self, s: str | bytes, rules: Dict[str, "Node"]) -> List[ParseResult]:
        raise NotImplementedError("Parsing not implemented")

    def __repr__(self):
        return ""

    def __str__(self):
        return self.__repr__()


class Alternative(Node):
    def __init__(self, alternatives: list[Node]):
        self.alternatives = alternatives

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return random.choice(self.alternatives).fuzz(rules)

    def parse(self, s: str | bytes, rules: Dict[str, Node]) -> List[ParseResult]:
        for alternative in self.alternatives:
            for result in alternative.parse(s, rules):
                yield result

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

    def _parse(
        self, s: str | bytes, rules: Dict[str, Node], nodes: List[Node]
    ) -> List[ParseResult]:
        if not nodes:
            return [ParseResult([], s)]
        for result in self._parse(s, rules, nodes[:-1]):
            for tmp_result in nodes[-1].parse(result.remaining, rules):
                yield result.offspring(tmp_result.trees, tmp_result.remaining)

    def parse(self, s: str | bytes, rules: Dict[str, Node]) -> List[ParseResult]:
        return self._parse(s, rules, self.nodes)

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

    def fuzz(self, rules: Dict[str, Node]) -> List[DerivationTree]:
        return sum(
            [self.node.fuzz(rules) for _ in range(random.randint(self.min, self.max))],
            [],
        )

    def _parse(
        self, s: str | bytes, rules: Dict[str, Node], current, min_: int, max_: int
    ) -> List[ParseResult]:
        if current == max_:
            return [ParseResult([], s)]
        for result in self.node.parse(s, rules):
            for tmp_result in self._parse(result.remaining, rules, current + 1, max_):
                yield result.offspring(tmp_result.trees, tmp_result.remaining)

    def parse(self, s: str | bytes, rules: Dict[str, Node]) -> List[ParseResult]:
        for _ in range(self.min):
            new_results = []
            for result in intermediate_results:
                tmp_results = self.node.parse(result.remaining, rules)
                new_results.extend(
                    [
                        result.offspring(tmp_result.trees, tmp_result.remaining)
                        for tmp_result in tmp_results
                    ]
                )
            intermediate_results = new_results
        for _ in range(self.min, self.max):
            new_results = []
            for result in intermediate_results:
                tmp_results = self.node.parse(result.remaining, rules)
                new_results.extend(
                    [
                        result.offspring(tmp_result.trees, tmp_result.remaining)
                        for tmp_result in tmp_results
                    ]
                )
            intermediate_results = new_results
            results.extend(intermediate_results)
        return results

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

    def parse(self, s: str | bytes, rules: Dict[str, Node]) -> List[ParseResult]:
        if self.symbol not in rules:
            raise ValueError(f"Symbol {self.symbol} not found in rules")
        results = rules[self.symbol].parse(s, rules)
        return [result.build(self.symbol) for result in results]

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

    def parse(self, s: str | bytes, rules: Dict[str, Node]) -> List[ParseResult]:
        if s.startswith(self.symbol.symbol):
            return [ParseResult(DerivationTree(self.symbol), s[len(self.symbol) :])]
        return []

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

    def parse(
        self,
        s: str | bytes,
        start: str | NonTerminal = "<start>",
        fail_on_error: bool = False,
    ) -> List[DerivationTree]:
        if isinstance(start, str):
            start = NonTerminal(start)
        parse_trees = NonTerminalNode(start).parse(s, self.rules)
        trees = [
            tree.trees
            for tree in parse_trees
            if tree.remaining == "" and isinstance(tree.trees, DerivationTree)
        ]
        if fail_on_error and not trees:
            raise ValueError(f"Could not parse {s} with start symbol {start}")
        return trees

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
