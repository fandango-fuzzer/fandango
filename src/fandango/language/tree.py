import copy
from typing import Optional, List, Any, Union

from fandango.language.symbol import Symbol, NonTerminal


class DerivationTree:
    """
    This class is used to represent a node in the derivation tree.
    """

    def __init__(
        self,
        symbol: Symbol,
        children: Optional[List["DerivationTree"]] = None,
        parent: Optional["DerivationTree"] = None,
    ):
        self.symbol = symbol
        self._children = []
        self.set_children(children or [])
        self._parent = parent

    def set_children(self, children: List["DerivationTree"]):
        self._children = children
        for child in self._children:
            child._parent = self

    def add_child(self, child: "DerivationTree"):
        self._children.append(child)
        child._parent = self

    def find_all_trees(self, symbol: NonTerminal):
        trees = sum(
            [
                child.find_all_trees(symbol)
                for child in self._children
                if child.symbol.is_non_terminal
            ],
            [],
        )
        if self.symbol == symbol:
            trees.append(self)
        return trees

    def find_direct_trees(self, symbol: NonTerminal):
        return [child for child in self._children if child.symbol == symbol]

    def __getitem__(self, item):
        return self._children.__getitem__(item)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        """
        Computes a hash of the derivation tree based on its structure and symbols.
        """
        return hash((self.symbol, tuple(hash(child) for child in self._children)))

    def __tree__(self):
        return self.symbol, [child.__tree__() for child in self._children]

    def __deepcopy__(self, memo):
        if id(self) in memo:
            return memo[id(self)]

        # Create a new instance without copying the parent
        copied = DerivationTree(self.symbol, [])
        memo[id(self)] = copied

        # Deepcopy the children
        copied._children = [copy.deepcopy(child, memo) for child in self._children]

        # Set parent pointers
        for child in copied._children:
            child._parent = copied

        # Set the parent to None or update if necessary
        copied._parent = None  # or copy.deepcopy(self.parent, memo) if parent is needed

        return copied

    def __repr__(self):
        if self.symbol.is_non_terminal:
            return "".join([repr(child) for child in self._children])
        elif self.symbol.is_terminal:
            return self.symbol.symbol
        else:
            raise ValueError("Invalid symbol type")

    def __contains__(self, item: Union["DerivationTree", Any]) -> bool:
        if isinstance(item, DerivationTree):
            return item in self._children

    def __iter__(self):
        return iter(self._children)

    def to_int(self):
        try:
            return int(self.__repr__())
        except ValueError:
            return None

    def to_float(self):
        try:
            return int(self.__repr__())
        except ValueError:
            return None

    def to_complex(self):
        try:
            return complex(self.__repr__())
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
