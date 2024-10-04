import abc
from typing import List, Optional, Dict, Tuple, Any

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


class ItemSearch(NonTerminalSearch):
    def __init__(self, base: NonTerminalSearch, slices: Tuple[Any]):
        self.base = base
        self.slices = slices

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find(tree)
        return sum([base.__getitem__(self.slices) for base in bases], [])

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find_direct(tree)
        return sum([base.__getitem__(self.slices) for base in bases], [])

    def __repr__(self):
        slice_reprs = []
        for slice_ in self.slices:
            if isinstance(slice_, slice):
                slice_repr = ""
                if slice_.start is not None:
                    slice_repr += repr(slice_.start)
                slice_repr += ":"
                if slice_.stop is not None:
                    slice_repr += repr(slice_.stop)
                if slice_.step is not None:
                    slice_repr += ":" + repr(slice_.step)
                slice_reprs.append(slice_repr)
            else:
                slice_reprs.append(repr(slice_))
        return f"{repr(self.base)}[{', '.join(slice_reprs)}]"


class SelectiveSearch(NonTerminalSearch):
    def __init__(
        self,
        base: NonTerminalSearch,
        symbol: NonTerminal,
        slices: Optional[Tuple[Any] | Any] = None,
    ):
        self.base = base
        self.symbol = symbol
        self.slices = slices

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find(tree)
        children = [base.find_direct_trees(self.symbol) for base in bases]
        if self.slices is not None:
            result = []
            for child in children:
                items = child.__getitem__(self.slices)
                if isinstance(items, list):
                    result.extend(items)
                else:
                    result.append(items)
            return result
        return sum(children, [])

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find_direct(tree)
        children = [base.find_direct_trees(self.symbol) for base in bases]
        if self.slices is not None:
            result = []
            for child in children:
                items = child.__getitem__(self.slices)
                if isinstance(items, list):
                    result.extend(items)
                else:
                    result.append(items)
            return result
        return sum(children, [])

    def __repr__(self):
        if self.slices:
            slice_reprs = []
            for slice_ in self.slices:
                if isinstance(slice_, slice):
                    slice_repr = ""
                    if slice_.start is not None:
                        slice_repr += repr(slice_.start)
                    slice_repr += ":"
                    if slice_.stop is not None:
                        slice_repr += repr(slice_.stop)
                    if slice_.step is not None:
                        slice_repr += ":" + repr(slice_.step)
                    slice_reprs.append(slice_repr)
                else:
                    slice_reprs.append(repr(slice_))
            return f"{repr(self.base)}[{repr(self.symbol)}]{{{', '.join(slice_reprs)}}}"
        return f"{repr(self.base)}[{repr(self.symbol)}]"
