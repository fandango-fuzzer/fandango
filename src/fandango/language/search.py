import abc
from typing import List, Optional, Dict

from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


class NonTerminalSearch(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        pass

    @abc.abstractmethod
    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        pass

    def find_all(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ):
        targets = []
        for tree in trees:
            targets.extend(self.find(tree, scope=scope))
        return targets

    @abc.abstractmethod
    def __repr__(self):
        pass

    def __str__(self):
        return self.__repr__()


class LengthSearch(NonTerminalSearch):
    def __init__(self, value: NonTerminalSearch):
        self.value = value

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return [len(self.value.find(tree, scope=scope))]

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return [len(self.value.find_direct(tree, scope=scope))]

    def __repr__(self):
        return f"|{repr(self.value)}|"


class RuleSearch(NonTerminalSearch):
    def __init__(self, symbol: NonTerminal):
        self.symbol = symbol

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        if scope and self.symbol in scope:
            return [scope[self.symbol]]
        return tree.find_all_trees(self.symbol)

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        if scope and self.symbol in scope:
            return [scope[self.symbol]]
        return tree.find_direct_trees(self.symbol)

    def __repr__(self):
        return repr(self.symbol)


class AttributeSearch(NonTerminalSearch):
    def __init__(self, base: NonTerminalSearch, attribute: NonTerminalSearch):
        self.base = base
        self.attribute = attribute

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find(tree)
        targets = []
        for base in bases:
            targets.extend(self.attribute.find_direct(base, scope=scope))
        return targets

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find_direct(tree)
        targets = []
        for base in bases:
            targets.extend(self.attribute.find_direct(base, scope=scope))
        return targets

    def __repr__(self):
        return f"{repr(self.base)}.{repr(self.attribute)}"
