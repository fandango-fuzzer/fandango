import copy
from typing import Any, Optional, TYPE_CHECKING, TypeVar, cast
from collections.abc import Iterable, Iterator
import warnings

from fandango.language.symbols import NonTerminal, Slice, Symbol, Terminal
from fandango.language.tree_value import (
    BYTES_TO_STRING_ENCODING,
    DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE,
    DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE,
    STRING_TO_BYTES_ENCODING,
    TreeValue,
    TreeValueType,
)

if TYPE_CHECKING:
    import fandango


# Recursive type for tree structure
T = TypeVar("T")
if TYPE_CHECKING:
    TreeTuple = tuple[T, list["TreeTuple[T]"]]
else:
    TreeTuple = tuple[T, list]  # beartype falls over with recursive types


class ProtocolMessage:
    """
    Holds information about a message in a protocol.
    """

    def __init__(
        self, sender: str, recipient: str | None, msg: "DerivationTree"
    ) -> None:
        self.msg = msg
        self.sender = sender
        self.recipient = recipient

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.recipient is None:
            return f"({self.sender} -> {self.recipient}): {str(self.msg)}"
        else:
            return f"({self.sender}): {str(self.msg)}"


class StepException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(f"StepException: {message}")


class PathStep:
    def __init__(self, index: int):
        self.index = index

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(sorted(self.__dict__.items())))


class SourceStep(PathStep):
    def __init__(self, index: int) -> None:
        super().__init__(index)


class ChildStep(PathStep):
    def __init__(self, index: int) -> None:
        super().__init__(index)


def index_by_reference(lst: Iterable[T], target: T) -> Optional[int]:
    for i, item in enumerate(lst):
        if item is target:  # compare reference, not data
            return i
    return None


def forward_to_tree_value_methods(
    function_names: list[str],
):
    """
    Decorator to add methods to a class, delegating to the result of `value().method(self)`.
    """

    def make_method(name):
        def method(self, *args, **kwargs):
            return getattr(self.value(), name)(*args, **kwargs)

        return method

    def decorator(cls):
        for name in function_names:
            # Check if the method is actually implemented on the class itself, not inherited
            if name in cls.__dict__:
                warnings.warn(
                    f"Method {name} already exists on {cls.__name__}, skipping",
                    Warning,
                )
            else:
                setattr(cls, name, make_method(name))
        return cls

    return decorator


@forward_to_tree_value_methods(DIRECT_ACCESS_METHODS_BASE_TO_FIRST_ARG_TYPE)
@forward_to_tree_value_methods(DIRECT_ACCESS_METHODS_BASE_TO_UNDERLYING_TYPE)
class DerivationTree:
    """
    This class is used to represent a node in the derivation tree.
    """

    def __init__(
        self,
        symbol: Symbol,
        children: Optional[list["DerivationTree"]] = None,
        *,
        parent: Optional["DerivationTree"] = None,
        sources: Optional[list["DerivationTree"]] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        read_only: Optional[bool] = False,
        origin_repetitions: Optional[list[tuple[str, int, int]]] = None,
    ) -> None:
        """
        Create a new derivation tree node.
        :param symbol: The symbol for this node (type Symbol)
        :param children: The children of this node (a list of DerivationTree)
        :param parent: (optional) The parent of this node (a DerivationTree node)
        :param sources: (optional) The sources of this node (a list of DerivationTrees used in generators to produce this node)
        :param read_only: If True, the node is read-only and cannot be modified (default: False)
        """
        if not isinstance(symbol, Symbol):
            raise TypeError(f"Expected Symbol, got {type(symbol)}")
        assert isinstance(
            symbol, (Terminal, NonTerminal, Slice)
        ), f"Received symbol of type {type(symbol)}"

        self.hash_cache: Optional[int] = None
        self._parent = parent
        self._sender = sender
        self._recipient = recipient
        self._symbol = symbol
        self._children: list[DerivationTree] = []
        self._sources: list[DerivationTree] = []  # init first
        if sources is not None:
            self.sources = sources  # use setter
        if origin_repetitions is None:
            origin_repetitions = []
        self.origin_repetitions: list[tuple[str, int, int]] = origin_repetitions
        self.read_only = read_only
        self._size: int  # no need to set it, it will be set in invalidate_hash, which is called in set_children
        self.set_children(children or [])

    def __len__(self) -> int:
        return len(self._children)

    def count_terminals(self) -> int:
        if self.symbol.is_terminal:
            return 1
        count = 0
        for child in self._children:
            count += child.count_terminals()
        return count

    def size(self) -> int:
        return self._size

    @property
    def symbol(self) -> Terminal | NonTerminal | Slice:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol) -> None:
        assert isinstance(
            symbol, (Terminal, NonTerminal, Slice)
        ), f"Received symbol of type {type(symbol)}"
        self._symbol = symbol
        self.invalidate_hash()

    @property
    def nonterminal(self) -> NonTerminal:
        """
        Returns the non-terminal symbol of this node.
        Raises TypeError if the symbol is not a NonTerminal.
        """
        if not self._symbol.is_non_terminal:
            raise TypeError(f"Symbol {self._symbol} is not a nonterminal")
        return cast(NonTerminal, self._symbol)

    @property
    def terminal(self) -> Terminal:
        """
        Returns the terminal symbol of this node.
        Raises TypeError if the symbol is not a Terminal.
        """
        if not self._symbol.is_terminal:
            raise TypeError(f"Symbol {self._symbol} is not a terminal")
        return cast(Terminal, self._symbol)

    @property
    def is_terminal(self) -> bool:
        """
        True is the node represents a terminal symbol.
        """
        return self.symbol.is_terminal

    @property
    def is_non_terminal(self) -> bool:
        """
        True is the node represents a nonterminal symbol.
        """
        return self.symbol.is_non_terminal

    def invalidate_hash(self, update_size: bool = True) -> None:
        self.hash_cache = None
        if update_size:
            self._size = 1 + sum(child.size() for child in self._children)
        if self._parent is not None:
            self._parent.invalidate_hash()

    @property
    def sender(self) -> Optional[str]:
        return self._sender

    @sender.setter
    def sender(self, sender: Optional[str]) -> None:
        self._sender = sender
        self.invalidate_hash()

    @property
    def recipient(self) -> Optional[str]:
        return self._recipient

    @recipient.setter
    def recipient(self, recipient: Optional[str]) -> None:
        self._recipient = recipient
        self.invalidate_hash()

    def get_path(self) -> list["DerivationTree"]:
        path: list[DerivationTree] = []
        current: Optional[DerivationTree] = self
        while current is not None:
            path.insert(0, current)
            current = current.parent
        return path

    def set_all_read_only(self, read_only: bool) -> None:
        """
        Sets self as well as all children and sources to read-only.
        This signals other classes, that this subtree should not be modified.
        """
        self.read_only = read_only
        for child in self._children:
            child.set_all_read_only(read_only)
        for child in self._sources:
            child.set_all_read_only(read_only)

    def protocol_msgs(self) -> list[ProtocolMessage]:
        """
        Returns a list of all protocol messages present in the current DerivationTree and children.
        """
        if not isinstance(self.symbol, NonTerminal):
            return []
        if self.sender is not None:
            return [ProtocolMessage(self.sender, self.recipient, self)]
        subtrees = []
        for child in self._children:
            subtrees.extend(child.protocol_msgs())
        return subtrees

    def append(
        self, hookin_path: tuple[tuple[NonTerminal, bool], ...], tree: "DerivationTree"
    ) -> None:
        """
        Appends a given DerivationTree to the current subtree at the specified hookin_path.

        :param hookin_path: A tuple of (NonTerminal, bool) pairs indicating the path to append the tree. If the bool
        is set to true, a new node is created for the NonTerminal.
        :param tree: The DerivationTree to append.
        """
        if len(hookin_path) == 0:
            self.add_child(tree)
            return
        next_nt, add_new_node = hookin_path[0]
        if add_new_node:
            self.add_child(DerivationTree(next_nt))
        elif (
            len(self.children) == 0
            or not isinstance(self.children[-1].symbol, NonTerminal)
            or self.children[-1].symbol.name() != next_nt.name()
        ):
            raise ValueError("Invalid hookin_path!")
        self.children[-1].append(hookin_path[1:], tree)

    def set_children(self, children: list["DerivationTree"]) -> None:
        self._children = children
        for child in self._children:
            child._parent = self
        self.invalidate_hash()

    @property
    def sources(self) -> list["DerivationTree"]:
        return self._sources

    @sources.setter
    def sources(self, source: list["DerivationTree"]) -> None:
        if source is None:
            self._sources = []
        else:
            self._sources = source
        for param in self._sources:
            param._parent = self

    def add_child(self, child: "DerivationTree") -> None:
        self._children.append(child)
        child._parent = self
        self.invalidate_hash()

    def find_all_trees(self, symbol: NonTerminal) -> list["DerivationTree"]:
        trees = sum(
            [
                child.find_all_trees(symbol)
                for child in [*self._children, *self._sources]
                if child.symbol.is_non_terminal
            ],
            [],
        )
        if self.symbol == symbol:
            trees.append(self)
        return trees

    def find_direct_trees(self, symbol: NonTerminal) -> list["DerivationTree"]:
        return [
            child
            for child in [*self._children, *self._sources]
            if child.symbol == symbol
        ]

    def find_by_origin(self, node_id: str) -> list["DerivationTree"]:
        trees = sum(
            [
                child.find_by_origin(node_id)
                for child in [*self._children, *self._sources]
                if child.symbol.is_non_terminal
            ],
            [],
        )
        for o_node_id, o_iter_id, rep in self.origin_repetitions:
            if o_node_id == node_id:
                trees.append(self)
                break
        return trees

    def __getitem__(self, item: Any) -> "DerivationTree":
        if isinstance(item, list) and len(item) == 1:
            item = item[0]
        items = self._children.__getitem__(item)
        if isinstance(items, list):
            return SliceTree(items)
        else:
            return items

    def get_last_by_path(self, path: list[NonTerminal]) -> "DerivationTree":
        symbol = path[0]
        if self.symbol == symbol:
            if len(path) == 1:
                return self
            else:
                return self._get_last_by_path(path[1:])
        raise IndexError(f"No such path in tree: {path} Tree: {self}")

    def _get_last_by_path(self, path: list[NonTerminal]) -> "DerivationTree":
        symbol = path[0]
        for child in self._children[::-1]:
            if child.symbol == symbol:
                if len(path) == 1:
                    return child
                else:
                    return child._get_last_by_path(path[1:])
        raise IndexError(
            f"No such path in tree: {path} Tree: {self.get_root(stop_at_argument_begin=True)}"
        )

    def __str__(self) -> str:
        return str(self.value())

    def __int__(self) -> int:
        return int(self.value())

    def __bytes__(self) -> bytes:
        return bytes(self.value())

    def __hash__(self) -> int:
        """
        Computes a hash of the derivation tree based on its structure and symbols.
        """
        if self.hash_cache is None:
            self.hash_cache = hash(
                (
                    self.symbol,
                    self.sender,
                    self.recipient,
                    tuple(hash(child) for child in self._children),
                )
            )
        return self.hash_cache

    def __tree__(self) -> TreeTuple[Symbol]:
        return self.symbol, [child.__tree__() for child in self._children]

    @staticmethod
    def from_tree(tree: TreeTuple[str]) -> "DerivationTree":
        symbol, children = tree
        new_symbol: Symbol
        if symbol.startswith("<") and symbol.endswith(">"):
            new_symbol = NonTerminal(symbol)
        else:
            new_symbol = Terminal(symbol)
        parsed_children = [DerivationTree.from_tree(child) for child in children]
        return DerivationTree(new_symbol, parsed_children)

    def deepcopy(
        self,
        *,
        copy_children: bool = True,
        copy_params: bool = True,
        copy_parent: bool = True,
    ) -> "DerivationTree":
        return self.__deepcopy__(
            None,
            copy_children=copy_children,
            copy_params=copy_params,
            copy_parent=copy_parent,
        )

    def __deepcopy__(
        self,
        memo: Optional[dict[int, Any]],
        copy_children: bool = True,
        copy_params: bool = True,
        copy_parent: bool = True,
    ) -> "DerivationTree":
        if memo is None:
            memo = {}
        if id(self) in memo:
            res = memo[id(self)]
            assert isinstance(res, DerivationTree)
            return res

        # Create a new instance without copying the parent
        copied = DerivationTree(
            self.symbol,
            [],
            sender=self.sender,
            recipient=self.recipient,
            sources=[],
            read_only=self.read_only,
            origin_repetitions=list(self.origin_repetitions),
        )
        memo[id(self)] = copied

        # Deepcopy the children
        if copy_children:
            copied.set_children(
                [copy.deepcopy(child, memo) for child in self._children]
            )

        # Set the parent to None or update if necessary
        if copy_parent:
            copied._parent = copy.deepcopy(self.parent, memo)
        if copy_params:
            copied.sources = copy.deepcopy(self.sources, memo)

        return copied

    def should_be_serialized_to_bytes(self) -> bool:
        """
        Return true if the derivation tree should be serialized to bytes.
        """
        return self._contains_type(
            TreeValueType.TRAILING_BITS_ONLY
        ) or self._contains_type(TreeValueType.BYTES)

    def _contains_type(self, tp: TreeValueType) -> bool:
        """
        Return true if the derivation tree contains any terminal symbols of type `tp` (say, `int` or `bytes`).
        """
        if self.symbol.is_terminal and self.symbol.is_type(tp):
            return True
        return any(child._contains_type(tp) for child in self._children)

    def contains_bits(self) -> bool:
        """
        Return true iff the derivation tree contains any bits (0 or 1).
        """
        return self._contains_type(TreeValueType.TRAILING_BITS_ONLY)

    def contains_bytes(self) -> bool:
        """
        Return true iff the derivation tree contains any byte strings.
        """
        return self._contains_type(TreeValueType.BYTES)

    def to_string(self, *, encoding: str = BYTES_TO_STRING_ENCODING) -> str:
        """
        Convert the derivation tree to a string.
        """
        return self.value().to_string(bytes_to_str_encoding=encoding)

    def to_bits(self, *, encoding: str = STRING_TO_BYTES_ENCODING) -> str:
        """
        Convert the derivation tree to a sequence of bits (0s and 1s).

        """
        return self.value().to_bits(str_to_bytes_encoding=encoding)

    def to_bytes(self, encoding: str = STRING_TO_BYTES_ENCODING) -> bytes:
        """
        Convert the derivation tree to a sequence of bytes.
        String elements are encoded according to `encoding`.
        """
        return self.value().to_bytes(str_to_bytes_encoding=encoding)

    def to_int(self, encoding: str = STRING_TO_BYTES_ENCODING) -> Optional[int]:
        return self.value().to_int(str_to_bytes_encoding=encoding)

    def to_tree(self, indent: int = 0, start_indent: int = 0) -> str:
        """
        Pretty-print the derivation tree (for visualization).
        """
        s = "  " * start_indent + "Tree(" + self.symbol.format_as_spec()
        if len(self._children) == 1 and len(self._sources) == 0:
            s += ", " + self._children[0].to_tree(indent, start_indent=0)
        else:
            has_children = False
            for child in self._children:
                s += ",\n" + child.to_tree(indent + 1, start_indent=indent + 1)
                has_children = True
            if len(self._sources) > 0:
                s += ",\n" + "  " * (indent + 1) + "sources=[\n"
                for child in self._sources:
                    s += child.to_tree(indent + 2, start_indent=indent + 2) + ",\n"
                    has_children = True
                s += "  " * (indent + 1) + "]"
            if has_children:
                s += "\n" + "  " * indent
        s += ")"
        return s

    def to_repr(self, indent: int = 0, start_indent: int = 0) -> str:
        """
        Output the derivation tree in internal representation.
        """
        s = "  " * start_indent + "DerivationTree(" + self.symbol.format_as_spec()
        if len(self._children) == 1 and len(self._sources) == 0:
            s += ", [" + self._children[0].to_repr(indent, start_indent=0) + "])"
        elif len(self._children + self._sources) >= 1:
            s += ",\n" + "  " * indent + "  [\n"
            for child in self._children:
                s += child.to_repr(indent + 2, start_indent=indent + 2)
                s += ",\n"
            s += "  " * indent + "  ]\n" + "  " * indent + ")"

            if len(self._sources) > 0:
                s += ",\n" + "  " * (indent + 1) + "sources=[\n"
                for source in self._sources:
                    s += source.to_repr(indent + 2, start_indent=indent + 2)
                    s += ",\n"
                s += "  " * indent + "  ]\n" + "  " * indent + ")"
        else:
            s += ")"
        return s

    def to_grammar(
        self, include_position: bool = True, include_value: bool = True
    ) -> str:
        """
        Output the derivation tree as (specialized) grammar
        """

        def _to_grammar(
            node: "DerivationTree",
            indent: int = 0,
            start_indent: int = 0,
            bit_count: int = -1,
            byte_count: int = 0,
        ) -> tuple[str, int, int]:
            """
            Output the derivation tree as (specialized) grammar
            """
            nonlocal include_position, include_value
            assert isinstance(node.symbol, NonTerminal)

            s = "  " * start_indent + f"{node.symbol.name()} ::="
            terminal_symbols = 0

            position = f"  # Position {byte_count:#06x} ({byte_count})"
            max_bit_count = bit_count - 1

            for child in node._children:
                assert not isinstance(child.symbol, Slice)
                if child.symbol.is_non_terminal:
                    s += f" {child.symbol.format_as_spec()}"
                else:
                    terminal = cast(Terminal, child.symbol)
                    s += " " + terminal.format_as_spec()
                    terminal_symbols += 1
                    if terminal.is_type(TreeValueType.TRAILING_BITS_ONLY):
                        if bit_count <= 0:
                            bit_count = 7
                            max_bit_count = 7
                        else:
                            bit_count -= 1
                            if bit_count == 0:
                                byte_count += 1
                    else:
                        byte_count += terminal.count_bytes()
                        bit_count = -1

                # s += f" (bit_count={bit_count}, byte_count={byte_count})"

            if len(node._sources) > 0:
                # We don't know the grammar, so we report a symbolic generator
                s += (
                    " := f("
                    + ", ".join(
                        [param.symbol.format_as_spec() for param in node._sources]
                    )
                    + ")"
                )

            have_position = False
            if include_position and terminal_symbols > 0:
                have_position = True
                s += position
                if bit_count >= 0:
                    if max_bit_count != bit_count:
                        s += f", bits {max_bit_count}-{bit_count}"
                    else:
                        s += f", bit {bit_count}"

            if include_value and len(node._children) >= 2:
                s += "  # " if not have_position else "; "
                s += node.to_value()

            for child in node._children:
                if child.symbol.is_non_terminal:
                    child_str, bit_count, byte_count = _to_grammar(
                        child,
                        indent + 1,
                        start_indent=indent + 1,
                        bit_count=bit_count,
                        byte_count=byte_count,
                    )
                    s += "\n" + child_str

                for param in child._sources:
                    child_str, _, _ = _to_grammar(
                        param, indent + 2, start_indent=indent + 1
                    )
                    s += "\n  " + child_str

            return s, bit_count, byte_count

        return _to_grammar(self)[0]

    def __repr__(self) -> str:
        return self.to_repr()

    def split_end(self, copy_tree: bool = True) -> "DerivationTree":
        inst = self
        if copy_tree:
            inst = copy.deepcopy(self)
        return inst._split_end()

    def prefix(self, copy_tree: bool = True) -> "DerivationTree":
        ref_tree = self.split_end(copy_tree)
        assert ref_tree.parent is not None
        ref_tree = ref_tree.parent
        ref_tree.set_children(ref_tree.children[:-1])
        return ref_tree

    def get_root(self, stop_at_argument_begin: bool = False) -> "DerivationTree":
        root = self
        while root.parent is not None and not (
            root in root.parent.sources and stop_at_argument_begin
        ):
            root = root.parent
        return root

    def _split_end(self) -> "DerivationTree":
        if self.parent is None or self in self.parent.sources:
            if self.parent is not None:
                self._parent = None
            return self
        me_idx = index_by_reference(self.parent.children, self)
        if me_idx is None:
            # Handle error or fallback — for example:
            raise ValueError("self not found in parent's children")
        keep_children = self.parent.children[: (me_idx + 1)]
        parent = self.parent._split_end()
        parent.set_children(keep_children)
        return self

    def get_choices_path(self) -> tuple[PathStep, ...]:
        current = self
        path: list[PathStep] = []
        while current.parent is not None:
            parent = current.parent
            child_idx = index_by_reference(parent.children, current)
            if child_idx is not None:
                path.append(ChildStep(child_idx))
            else:
                source_idx = index_by_reference(parent.sources, current)
                if source_idx is None:
                    try:
                        # Fallback: If current node reference is not in parent.sources, try to get it by value.
                        source_idx = parent.sources.index(current)
                    except ValueError:
                        raise StepException(
                            f"Cannot find {current.to_repr()} in parent.children: {parent.children} or parent.sources: {parent.sources}"
                        )
                else:
                    path.append(SourceStep(source_idx))
            current = parent
        return tuple(path[::-1])

    def replace(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",  # has to be full path, otherwise beartype complains because of a circular import with grammar
        tree_to_replace: "DerivationTree",
        new_subtree: "DerivationTree",
    ) -> "DerivationTree":
        return self.replace_multiple(grammar, [(tree_to_replace, new_subtree)])

    def replace_multiple(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",  # full path to avoid circular import
        replacements: list[tuple["DerivationTree", "DerivationTree"]],
        path_to_replacement: Optional[dict[tuple, "DerivationTree"]] = None,
        current_path: Optional[tuple] = None,
    ) -> "DerivationTree":
        """
        Replace the subtree rooted at the given node with the new subtree.
        """
        if path_to_replacement is None:
            path_to_replacement = dict()
            for replacee, replacement in replacements:
                path_to_replacement[replacee.get_choices_path()] = replacement

        if current_path is None:
            current_path = self.get_choices_path()

        if (
            current_path in path_to_replacement
            and self.symbol == path_to_replacement[current_path].symbol
            and not self.read_only
        ):
            new_subtree = path_to_replacement[current_path].deepcopy(
                copy_children=True, copy_params=False, copy_parent=False
            )
            new_subtree._parent = self.parent
            new_subtree.origin_repetitions = list(self.origin_repetitions)
            new_children = []
            for i, child in enumerate(new_subtree._children):
                new_children.append(
                    child.replace_multiple(
                        grammar,
                        replacements,
                        path_to_replacement,
                        current_path + (ChildStep(i),),
                    )
                )
            new_subtree.set_children(new_children)
            grammar.populate_sources(new_subtree)
            return new_subtree

        regen_children = False
        regen_params = False
        new_children = []
        sources = []
        for i, param in enumerate(self._sources):
            new_param = param.replace_multiple(
                grammar,
                replacements,
                path_to_replacement,
                current_path + (SourceStep(i),),
            )
            sources.append(new_param)
            if new_param != param:
                regen_children = True
        for i, child in enumerate(self._children):
            new_child = child.replace_multiple(
                grammar,
                replacements,
                path_to_replacement,
                current_path + (ChildStep(i),),
            )
            new_children.append(new_child)
            if new_child != child:
                regen_params = True

        new_tree = DerivationTree(
            self.symbol,
            new_children,
            parent=self.parent,
            sender=self.sender,
            recipient=self.recipient,
            sources=sources,
            read_only=self.read_only,
            origin_repetitions=list(self.origin_repetitions),
        )

        # Update children match generator parameters, if parameters updated
        if new_tree.symbol not in grammar.generators:
            new_tree.sources = []
            return new_tree

        if regen_children:
            self_is_generator_child = False
            current = self
            current_parent = self.parent
            while current_parent is not None:
                if current in current_parent.sources:
                    break
                elif current in current_parent.children and grammar.is_use_generator(
                    current_parent
                ):
                    self_is_generator_child = True
                    break
                current = current_parent
                current_parent = current_parent.parent

            # Trees generated by generators don't contain children generated with other generators.
            if self_is_generator_child:
                new_tree.sources = []
            else:
                new_tree.set_children(grammar.derive_generator_output(new_tree))
        elif regen_params:
            new_tree.sources = grammar.derive_sources(new_tree)

        return new_tree

    def get_non_terminal_symbols(
        self, exclude_read_only: bool = True
    ) -> set[NonTerminal]:
        """
        Retrieve all non-terminal symbols present in the derivation tree.
        """
        symbols = set()
        if self.symbol.is_non_terminal and not (exclude_read_only and self.read_only):
            symbols.add(self.nonterminal)
        for child in self._children:
            symbols.update(child.get_non_terminal_symbols(exclude_read_only))
        for param in self._sources:
            symbols.update(param.get_non_terminal_symbols(exclude_read_only))
        return symbols

    def find_all_nodes(
        self, symbol: NonTerminal, exclude_read_only: bool = True
    ) -> list["DerivationTree"]:
        """
        Find all nodes in the derivation tree with the given non-terminal symbol.
        """
        if isinstance(symbol, str):
            symbol = NonTerminal(symbol)
        nodes = []
        if self.symbol.is_non_terminal:
            nt = cast(NonTerminal, self.symbol)
            if nt == symbol and not (exclude_read_only and self.read_only):
                nodes.append(self)
            for child in self._children:
                nodes.extend(child.find_all_nodes(symbol, exclude_read_only))
            for param in self._sources:
                nodes.extend(param.find_all_nodes(symbol, exclude_read_only))
        return nodes

    @property
    def children(self) -> list["DerivationTree"]:
        """
        Return the children of the current node.
        """
        return self._children

    @property
    def parent(self) -> Optional["DerivationTree"]:
        """
        Return the parent node of the current node.
        """
        return self._parent

    def children_values(self) -> list[TreeValue]:
        """
        Return values of all direct children
        """
        return [node.value() for node in self.children]

    def flatten(self) -> list["DerivationTree"]:
        """
        Flatten the derivation tree into a list of DerivationTrees.
        """
        flat = [self]
        for child in self._children:
            flat.extend(child.flatten())
        return flat

    def descendants(self) -> list["DerivationTree"]:
        """
        Return all descendants of the current node
        """
        return self.flatten()[1:]

    def descendant_values(self) -> list[TreeValue]:
        """
        Return all descendants of the current node
        """
        values = [node.value() for node in self.descendants()]
        return values

    def get_index(self, target: "DerivationTree") -> int:
        """
        Get the index of the target node in the tree.
        """
        flat = self.flatten()
        try:
            return flat.index(target)
        except ValueError:
            return -1

    def value(self) -> TreeValue:
        if self.symbol.is_terminal:
            return self.symbol.value()

        aggregate = TreeValue.empty()
        for child in self._children:
            aggregate = aggregate.append(child.value())
        return aggregate

    def to_value(self) -> str:
        value = self.value()
        if value.is_type(TreeValueType.EMPTY):
            return ""
        elif value.is_type(TreeValueType.TRAILING_BITS_ONLY):
            return "0b" + value.to_bits()
        elif value.is_type(TreeValueType.STRING):
            return str(value)
        elif value.is_type(TreeValueType.BYTES):
            return str(bytes(value))
        else:
            raise ValueError(f"Invalid value type: {value.type_}")

    ## Comparison operations
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, DerivationTree):
            return hash(self) == hash(other)
        else:
            return self.value() == other

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __iter__(self) -> Iterator["DerivationTree"]:
        return iter(self._children)


class SliceTree(DerivationTree):
    def __init__(self, children: list[DerivationTree], read_only: bool = False) -> None:
        super().__init__(Slice(), children, read_only=read_only)
