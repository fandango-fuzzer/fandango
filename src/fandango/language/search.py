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

    @abc.abstractmethod
    def get_access_points(self) -> List[NonTerminal]:
        pass


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

    def get_access_points(self):
        return self.value.get_access_points()


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

    def get_access_points(self):
        return [self.symbol]


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

    def get_access_points(self):
        return self.attribute.get_access_points()


class StarAttributeSearch(NonTerminalSearch):
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
            targets.extend(self.attribute.find(base, scope=scope))
        return targets

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find_direct(tree)
        targets = []
        for base in bases:
            targets.extend(self.attribute.find(base, scope=scope))
        return targets

    def __repr__(self):
        return f"{repr(self.base)}*{repr(self.attribute)}"

    def get_access_points(self):
        return self.attribute.get_access_points()


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
        return sum([base.__getitem__(self.slices, as_list=True) for base in bases], [])

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        bases = self.base.find_direct(tree)
        return sum([base.__getitem__(self.slices, as_list=True) for base in bases], [])

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

    def get_access_points(self):
        return self.base.get_access_points()


class SelectiveSearch(NonTerminalSearch):
    def __init__(
        self,
        base: NonTerminalSearch,
        symbols: List[Tuple[NonTerminal, bool]],
        slices: List[Optional[Any]] = None,
    ):
        self.base = base
        self.symbols = symbols
        self.slices = slices or [None] * len(symbols)

    def _find(self, bases: List[DerivationTree]):
        result = []
        for symbol, is_direct, items in zip(*zip(*self.symbols), self.slices):
            if is_direct:
                children = [base.find_direct_trees(symbol) for base in bases]
            else:
                children = [base.find_all_trees(symbol) for base in bases]
            if items is not None:
                for index, child in enumerate(children):
                    values = child.__getitem__(items)
                    children[index] = values if isinstance(values, list) else [values]
            result.extend(sum(children, []))
        return result

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return self._find(self.base.find(tree))

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[DerivationTree]:
        return self._find(self.base.find_direct(tree))

    def __repr__(self):
        slice_reprs = []
        for symbol, is_direct, items in zip(*self.symbols, self.slices):
            slice_repr = f"{'' if is_direct else '*'}{repr(symbol)}"
            if items is not None:
                slice_repr += ": "
                if isinstance(items, slice):
                    if items.start is not None:
                        slice_repr += repr(items.start)
                    slice_repr += ":"
                    if items.stop is not None:
                        slice_repr += repr(items.stop)
                    if items.step is not None:
                        slice_repr += ":" + repr(items.step)
                else:
                    slice_reprs += repr(items)
            slice_reprs.append(slice_repr)
        return f"{repr(self.base)}{{{', '.join(slice_reprs)}}}"

    def get_access_points(self):
        return [symbol for symbol, _ in self.symbols]
