import copy
from typing import Optional, List, Any, Union, Set, Tuple

from fandango.language.symbol import Symbol, NonTerminal, Terminal


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
        self._size = 1
        self.set_children(children or [])
        self._parent = parent

    def __len__(self):
        return len(self._children)

    def size(self):
        return self._size

    def set_children(self, children: List["DerivationTree"]):
        self._children = children
        self._size = 1 + sum(child.size() for child in self._children)
        for child in self._children:
            child._parent = self

    def add_child(self, child: "DerivationTree"):
        self._children.append(child)
        self._size += child.size()
        child._parent = self

    def find_all_trees(self, symbol: NonTerminal) -> List["DerivationTree"]:
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

    def find_direct_trees(self, symbol: NonTerminal) -> List["DerivationTree"]:
        return [child for child in self._children if child.symbol == symbol]

    def __getitem__(
        self, item, as_list=False
    ) -> Union["DerivationTree", List["DerivationTree"]]:
        if isinstance(item, list) and len(item) == 1:
            item = item[0]
        items = self._children.__getitem__(item)
        if as_list and not isinstance(items, list):
            items = [items]
        return items

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        """
        Computes a hash of the derivation tree based on its structure and symbols.
        """
        return hash((self.symbol, tuple(hash(child) for child in self._children)))

    def __tree__(self):
        return self.symbol, [child.__tree__() for child in self._children]

    @staticmethod
    def from_tree(tree: Tuple[str, List[Tuple[str, List]]]) -> "DerivationTree":
        symbol, children = tree
        if not isinstance(symbol, str):
            raise TypeError(f"{symbol} must be string")
        if symbol.startswith("<") and symbol.endswith(">"):
            symbol = NonTerminal(symbol)
        else:
            symbol = Terminal(symbol)
        return DerivationTree(
            symbol, [DerivationTree.from_tree(child) for child in children]
        )

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

    def __contains__(self, other: Union["DerivationTree", Any]) -> bool:
        if isinstance(other, DerivationTree):
            return other in self._children
        return other in str(self)

    def __iter__(self):
        return iter(self._children)

    def to_int(self, *args, **kwargs):
        try:
            return int(self.__repr__(), *args, **kwargs)
        except ValueError:
            return None

    def to_float(self):
        try:
            return float(self.__repr__())
        except ValueError:
            return None

    def to_complex(self, *args, **kwargs):
        try:
            return complex(self.__repr__(), *args, **kwargs)
        except ValueError:
            return None

    def is_int(self, *args, **kwargs):
        try:
            int(self.__repr__(), *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_float(self):
        try:
            float(self.__repr__())
        except ValueError:
            return False
        return True

    def is_complex(self, *args, **kwargs):
        try:
            complex(self.__repr__(), *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_num(self):
        return self.is_float()

    def __eq__(self, other):
        if isinstance(other, DerivationTree):
            return self.__tree__() == other.__tree__()
        return str(self) == other

    def __le__(self, other):
        if isinstance(other, DerivationTree):
            return str(self) <= str(other)
        return str(self) <= other

    def __lt__(self, other):
        if isinstance(other, DerivationTree):
            return str(self) < str(other)
        return str(self) < other

    def __ge__(self, other):
        if isinstance(other, DerivationTree):
            return str(self) >= str(other)
        return str(self) >= other

    def __gt__(self, other):
        if isinstance(other, DerivationTree):
            return str(self) > str(other)
        return str(self) > other

    def __ne__(self, other):
        return not self.__eq__(other)

    def replace(self, tree_to_replace, new_subtree):
        """
        Replace the subtree rooted at the given node with the new subtree.
        """
        if self == tree_to_replace:
            return new_subtree
        else:
            return DerivationTree(
                self.symbol,
                [
                    child.replace(tree_to_replace, new_subtree)
                    for child in self._children
                ],
            )

    def get_non_terminal_symbols(self) -> Set[NonTerminal]:
        """
        Retrieve all non-terminal symbols present in the derivation tree.
        """
        symbols = set()
        if self.symbol.is_non_terminal:
            symbols.add(self.symbol)
        for child in self._children:
            symbols.update(child.get_non_terminal_symbols())
        return symbols

    def find_all_nodes(self, symbol: NonTerminal) -> List["DerivationTree"]:
        """
        Find all nodes in the derivation tree with the given non-terminal symbol.
        """
        nodes = []
        if self.symbol == symbol:
            nodes.append(self)
        for child in self._children:
            nodes.extend(child.find_all_nodes(symbol))
        return nodes

    @property
    def children(self):
        return self._children

    def flatten(self):
        """
        Flatten the derivation tree into a list of symbols.
        """
        flat = [self]
        for child in self._children:
            flat.extend(child.flatten())
        return flat

    def get_index(self, target):
        """
        Get the index of the target node in the tree.
        """
        flat = self.flatten()
        try:
            return flat.index(target)
        except ValueError:
            return -1

    def __getattr__(self, name):
        """
        Catch-all: All other attributes and methods apply to the string representation
        """
        if name in str.__dict__:

            def fn(*args, **kwargs):
                return str.__dict__[name](str(self), *args, **kwargs)

            return fn

        raise AttributeError(f"{self.symbol} has no attribute {repr(name)}")
