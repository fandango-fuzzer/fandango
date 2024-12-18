import abc
from typing import List, Optional, Dict, Tuple, Any

from fandango.language.symbol import NonTerminal
from fandango.language.tree import DerivationTree


class Container(abc.ABC):
    @abc.abstractmethod
    def get_trees(self) -> List[DerivationTree]:
        pass

    @abc.abstractmethod
    def evaluate(self):
        pass


class Tree(Container):
    def __init__(self, tree: DerivationTree):
        self.tree = tree

    def get_trees(self) -> List[DerivationTree]:
        return [self.tree]

    def evaluate(self):
        return self.tree


class Length(Container):
    def __init__(self, trees: List[DerivationTree]):
        self.trees = trees

    def get_trees(self) -> List[DerivationTree]:
        return self.trees

    def evaluate(self):
        return len(self.trees)


class NonTerminalSearch(abc.ABC):
    @abc.abstractmethod
    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        pass

    @abc.abstractmethod
    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        pass

    def find_all(
        self,
        trees: List[DerivationTree],
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[List[Container]]:
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
    ) -> List[Container]:
        return [
            Length(
                sum(
                    [
                        container.get_trees()
                        for container in self.value.find(tree, scope=scope)
                    ],
                    [],
                )
            )
        ]

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        return [
            Length(
                sum(
                    [
                        container.get_trees()
                        for container in self.value.find_direct(tree, scope=scope)
                    ],
                    [],
                )
            )
        ]

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
    ) -> List[Container]:
        if scope and self.symbol in scope:
            return [Tree(scope[self.symbol])]
        return list(map(Tree, tree.find_all_trees(self.symbol)))

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        if scope and self.symbol in scope:
            return [Tree(scope[self.symbol])]
        return list(map(Tree, tree.find_direct_trees(self.symbol)))

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
    ) -> List[Container]:
        bases = self.base.find(tree, scope=scope)
        targets = []
        for base in bases:
            for t in base.get_trees():
                targets.extend(self.attribute.find_direct(t, scope=scope))
        return targets

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        bases = self.base.find_direct(tree, scope=scope)
        targets = []
        for base in bases:
            for t in base.get_trees():
                targets.extend(self.attribute.find_direct(t, scope=scope))
        return targets

    def __repr__(self):
        return f"{repr(self.base)}.{repr(self.attribute)}"

    def get_access_points(self):
        return self.attribute.get_access_points()


class DescendantAttributeSearch(NonTerminalSearch):
    def __init__(self, base: NonTerminalSearch, attribute: NonTerminalSearch):
        self.base = base
        self.attribute = attribute

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        bases = self.base.find(tree, scope=scope)
        targets = []
        for base in bases:
            for t in base.get_trees():
                targets.extend(self.attribute.find(t, scope=scope))
        return targets

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        bases = self.base.find_direct(tree, scope=scope)
        targets = []
        for base in bases:
            for t in base.get_trees():
                targets.extend(self.attribute.find(t, scope=scope))
        return targets

    def __repr__(self):
        return f"{repr(self.base)}..{repr(self.attribute)}"

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
    ) -> List[Container]:
        bases = self.base.find(tree, scope=scope)
        return list(
            map(
                Tree,
                sum(
                    [
                        t.__getitem__(self.slices, as_list=True)
                        for base in bases
                        for t in base.get_trees()
                    ],
                    [],
                ),
            )
        )

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        bases = self.base.find_direct(tree, scope=scope)
        return list(
            map(
                Tree,
                sum(
                    [
                        t.__getitem__(self.slices, as_list=True)
                        for base in bases
                        for t in base.get_trees()
                    ],
                    [],
                ),
            )
        )

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

    def _find(self, bases: List[Container]):
        result = []
        for symbol, is_direct, items in zip(*zip(*self.symbols), self.slices):
            if is_direct:
                children = [
                    t.find_direct_trees(symbol)
                    for base in bases
                    for t in base.get_trees()
                ]
            else:
                children = [
                    t.find_all_trees(symbol) for base in bases for t in base.get_trees()
                ]
            if items is not None:
                for index, child in enumerate(children):
                    values = child.__getitem__(items)
                    children[index] = values if isinstance(values, list) else [values]
            result.extend(sum(children, []))
        return list(map(Tree, result))

    def find(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        return self._find(self.base.find(tree, scope=scope))

    def find_direct(
        self,
        tree: DerivationTree,
        scope: Optional[Dict[NonTerminal, List[DerivationTree]]] = None,
    ) -> List[Container]:
        return self._find(self.base.find_direct(tree, scope=scope))

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
