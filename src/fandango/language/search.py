import abc
from typing import List, Optional, Dict

from fandango.language.grammar import DerivationTree, Grammar, NonTerminal


class NonTerminalSearch(abc.ABC):
    def __init__(self, grammar: Grammar):
        self.grammar = grammar

    @abc.abstractmethod
    def find(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        pass

    def find_all(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        all_nodes = []
        for tree in trees:
            all_nodes.extend(self.find_all(tree.children, scope))
        all_nodes.extend(self.find(trees, scope))
        return all_nodes


class LengthSearch(NonTerminalSearch):
    def __init__(self, value: NonTerminalSearch, grammar: Grammar):
        super().__init__(grammar)
        self.value = value

    def find(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return [len(self.value.find(trees, scope=scope))]

    def find_all(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return [len(self.value.find_all(trees, scope=scope))]


class RuleSearch(NonTerminalSearch):
    def __init__(self, symbol: NonTerminal, grammar: Grammar):
        super().__init__(grammar)
        self.symbol = symbol

    def find(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        if scope and self.symbol in scope:
            return scope[self.symbol]
        return [tree for tree in trees if tree.symbol == self.symbol]


class AttributeSearch(NonTerminalSearch):
    def __init__(
        self, base: NonTerminalSearch, attribute: NonTerminalSearch, grammar: Grammar
    ):
        super().__init__(grammar)
        self.base = base
        self.attribute = attribute

    def find(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return self.attribute.find(
            [child for tree in self.base.find(trees) for child in tree.children]
        )
