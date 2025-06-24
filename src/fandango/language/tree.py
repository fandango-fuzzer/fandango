import copy
from io import BytesIO, StringIO
from typing import Any, Optional, Union, TYPE_CHECKING

from fandango.errors import FandangoValueError
from fandango.language.symbol import NonTerminal, Slice, Symbol, Terminal

if TYPE_CHECKING:
    from fandango.language.grammar import Grammar


class ProtocolMessage:
    """
    Holds information about a message in a protocol.
    """

    def __init__(self, sender: str, recipient: str | None, msg: "DerivationTree"):
        self.msg = msg
        self.sender = sender
        self.recipient = recipient

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.recipient is None:
            return f"({self.sender} -> {self.recipient}): {str(self.msg)}"
        else:
            return f"({self.sender}): {str(self.msg)}"


class StepException(Exception):
    def __init__(self, message):
        super().__init__(f"StepException: {message}")


class PathStep:
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


class SourceStep(PathStep):
    def __init__(self, index):
        self.index = index


class ChildStep(PathStep):
    def __init__(self, index):
        self.index = index


def index_by_reference(lst, target):
    for i, item in enumerate(lst):
        if item is target:
            return i
    return None


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
    ):
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

        self.hash_cache: Optional[int] = None
        self._parent: Optional["DerivationTree"] = parent
        self._sender = sender
        self._recipient = recipient
        self._symbol: Symbol = symbol
        self._children: list["DerivationTree"] = []
        self._sources: list["DerivationTree"] = []
        if sources is not None:
            self.sources = sources
        self.read_only = read_only
        self._size = 1
        self.set_children(children or [])
        self.invalidate_hash()

    def __len__(self):
        return len(self._children)

    def count_terminals(self):
        if self.symbol.is_terminal:
            return 1
        count = 0
        for child in self._children:
            count += child.count_terminals()
        return count

    def size(self):
        return self._size

    def __bytes__(self):
        return self.to_bytes()

    @property
    def symbol(self) -> Symbol:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol
        self.invalidate_hash()

    @property
    def nonterminal(self) -> NonTerminal:
        """
        Returns the non-terminal symbol of this node.
        Raises TypeError if the symbol is not a NonTerminal.
        """
        if not isinstance(self._symbol, NonTerminal):
            raise TypeError(f"Expected NonTerminal, got {type(self._symbol)}")
        return self._symbol

    @property
    def terminal(self) -> Terminal:
        """
        Returns the terminal symbol of this node.
        Raises TypeError if the symbol is not a Terminal.
        """
        if not isinstance(self._symbol, Terminal):
            raise TypeError(f"Expected Terminal, got {type(self._symbol)}")
        return self._symbol

    def is_terminal(self):
        """
        True is the node represents a terminal symbol.
        """
        return self.symbol.is_terminal

    def is_nonterminal(self):
        """
        True is the node represents a nonterminal symbol.
        """
        return self.symbol.is_non_terminal

    def is_regex(self):
        """
        True is the node represents a regex symbol.
        """
        return self.symbol.is_regex

    def sym(self):
        """
        Return the symbol
        """
        return self.symbol.symbol

    def invalidate_hash(self):
        self.hash_cache = None
        if self._parent is not None:
            self._parent.invalidate_hash()

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender: Optional[str]):
        self._sender = sender
        self.invalidate_hash()

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, recipient: Optional[str]):
        self._recipient = recipient
        self.invalidate_hash()

    def get_path(self):
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
        elif len(self.children) == 0 or str(self.children[-1].symbol) != next_nt.symbol:
            raise ValueError("Invalid hookin_path!")
        self.children[-1].append(hookin_path[1:], tree)

    def set_children(self, children: list["DerivationTree"]):
        self._children = children
        self._update_size(1 + sum(child.size() for child in self._children))
        for child in self._children:
            child._parent = self
        self.invalidate_hash()

    @property
    def sources(self) -> list["DerivationTree"]:
        return self._sources

    @sources.setter
    def sources(self, source: list["DerivationTree"]):
        if source is None:
            self._sources = []
        else:
            self._sources = source
        for param in self._sources:
            param._parent = self

    def add_child(self, child: "DerivationTree"):
        self._children.append(child)
        self._update_size(self.size() + child.size())
        child._parent = self
        self.invalidate_hash()

    def _update_size(self, new_val: int):
        if self._parent is not None:
            self._parent._update_size(self._parent.size() + new_val - self._size)
        self._size = new_val

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

    def __getitem__(self, item) -> "DerivationTree":
        if isinstance(item, list) and len(item) == 1:
            item = item[0]
        items = self._children.__getitem__(item)
        if isinstance(items, list):
            return SliceTree(items)
        else:
            return items

    def get_last_by_path(self, path: list[NonTerminal]):
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

    def __str__(self):
        return self.to_string()

    def __hash__(self):
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

    def __tree__(self):
        return self.symbol, [child.__tree__() for child in self._children]

    @staticmethod
    def from_tree(tree: tuple[str, list[tuple[str, list]]]) -> "DerivationTree":
        symbol, children = tree
        if not isinstance(symbol, str):
            raise TypeError(f"{symbol} must be a string")
        new_symbol: Symbol
        if symbol.startswith("<") and symbol.endswith(">"):
            new_symbol = NonTerminal(symbol)
        else:
            new_symbol = Terminal(symbol)
        return DerivationTree(
            new_symbol, [DerivationTree.from_tree(child) for child in children]
        )

    def deepcopy(self, *, copy_children=True, copy_params=True, copy_parent=True):
        return self.__deepcopy__(
            None,
            copy_children=copy_children,
            copy_params=copy_params,
            copy_parent=copy_parent,
        )

    def __deepcopy__(
        self, memo, copy_children=True, copy_params=True, copy_parent=True
    ):
        if memo is None:
            memo = {}
        if id(self) in memo:
            return memo[id(self)]

        # Create a new instance without copying the parent
        copied = DerivationTree(
            self.symbol,
            [],
            sender=self.sender,
            recipient=self.recipient,
            sources=[],
            read_only=self.read_only,
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

    def _write_to_stream(self, stream: BytesIO, *, encoding="utf-8"):
        """
        Write the derivation tree to a (byte) stream
        (e.g., a file or BytesIO).
        """
        if self.symbol.is_non_terminal:
            for child in self._children:
                child._write_to_stream(stream)
        elif isinstance(self.symbol.symbol, bytes):
            # Bytes get written as is
            stream.write(self.symbol.symbol)
        elif isinstance(self.symbol.symbol, str):
            # Strings get encoded
            stream.write(self.symbol.symbol.encode(encoding))
        else:
            raise FandangoValueError("Invalid symbol type")

    def _write_to_bitstream(self, stream: StringIO, *, encoding="utf-8"):
        """
        Write the derivation tree to a bit stream of 0's and 1's
        (e.g., a file or StringIO).
        """
        if self.symbol.is_non_terminal:
            for child in self._children:
                child._write_to_bitstream(stream, encoding=encoding)
        elif self.symbol.is_terminal:
            symbol = self.symbol.symbol
            if isinstance(symbol, int):
                # Append single bit
                bits = str(symbol)
            else:
                # Convert strings and bytes to bits
                elem_stream = BytesIO()
                self._write_to_stream(elem_stream, encoding=encoding)
                elem_stream.seek(0)
                elem = elem_stream.read()
                bits = "".join(format(i, "08b") for i in elem)
            stream.write(bits)
        else:
            raise FandangoValueError("Invalid symbol type")

    def contains_type(self, tp: type) -> bool:
        """
        Return true if the derivation tree contains any terminal symbols of type `tp` (say, `int` or `bytes`).
        """
        if self.symbol.is_terminal and isinstance(self.symbol.symbol, tp):
            return True
        for child in self._children:
            if child.contains_bits():
                return True
        return False  # No bits found

    def contains_bits(self) -> bool:
        """
        Return true iff the derivation tree contains any bits (0 or 1).
        """
        return self.contains_type(int)

    def contains_bytes(self) -> bool:
        """
        Return true iff the derivation tree contains any byte strings.
        """
        return self.contains_type(bytes)

    def contains_strings(self) -> bool:
        """
        Return true iff the derivation tree contains any (UTF-8) strings.
        """
        return self.contains_type(str)

    def to_string(self) -> str:
        """
        Convert the derivation tree to a string.
        """
        val: Any = self.value()

        if val is None:
            return ""

        if isinstance(val, int):
            # This is a bit value; convert to bytes
            assert (
                val >= 0
            ), "Assumption: ints are unsigned. If this does not hold, the following needs to change"
            required_bytes = (val.bit_length() + 7) // 8  # for unsigned ints
            required_bytes = max(
                1, required_bytes
            )  # ensure at least 1 byte for number 0
            val = int(val).to_bytes(required_bytes)
            assert isinstance(val, bytes)

        if isinstance(val, bytes):
            # This is a bytes string; convert to string
            # Decoding into latin-1 keeps all bytes as is
            val = val.decode("latin-1")
            assert isinstance(val, str)

        if isinstance(val, str):
            return val

        raise FandangoValueError(f"Cannot convert {val!r} to string")

    def to_bits(self, *, encoding="utf-8") -> str:
        """
        Convert the derivation tree to a sequence of bits (0s and 1s).
        """
        stream = StringIO()
        self._write_to_bitstream(stream, encoding=encoding)
        stream.seek(0)
        return stream.read()

    def to_bytes(self, encoding="utf-8") -> bytes:
        """
        Convert the derivation tree to a string.
        String elements are encoded according to `encoding`.
        """
        if self.contains_bits():
            # Encode as bit string
            bitstream = self.to_bits(encoding=encoding)

            # Decode into bytes, without further interpretation
            s = b"".join(
                int(bitstream[i : i + 8], 2).to_bytes()
                for i in range(0, len(bitstream), 8)
            )
            return s

        stream = BytesIO()
        self._write_to_stream(stream, encoding=encoding)
        stream.seek(0)
        return stream.read()

    def to_tree(self, indent=0, start_indent=0) -> str:
        """
        Pretty-print the derivation tree (for visualization).
        """
        s = "  " * start_indent + "Tree(" + repr(self.symbol.symbol)
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

    def to_repr(self, indent=0, start_indent=0) -> str:
        """
        Output the derivation tree in internal representation.
        """
        s = "  " * start_indent + "DerivationTree(" + repr(self.symbol)
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

    def to_grammar(self, include_position=True, include_value=True) -> str:
        """
        Output the derivation tree as (specialized) grammar
        """

        def _to_grammar(
            node, indent=0, start_indent=0, bit_count=-1, byte_count=0
        ) -> tuple[str, int, int]:
            """
            Output the derivation tree as (specialized) grammar
            """
            assert isinstance(node.symbol.symbol, str)
            nonlocal include_position, include_value

            s = "  " * start_indent + f"{node.symbol.symbol} ::="
            terminal_symbols = 0

            position = f"  # Position {byte_count:#06x} ({byte_count})"
            max_bit_count = bit_count - 1

            for child in node._children:
                if child.symbol.is_non_terminal:
                    s += f" {child.symbol.symbol}"
                else:
                    s += " " + repr(child.symbol.symbol)
                    terminal_symbols += 1

                    if isinstance(child.symbol.symbol, int):
                        if bit_count <= 0:
                            bit_count = 7
                            max_bit_count = 7
                        else:
                            bit_count -= 1
                            if bit_count == 0:
                                byte_count += 1
                    else:
                        byte_count += len(child.symbol.symbol)
                        bit_count = -1

                # s += f" (bit_count={bit_count}, byte_count={byte_count})"

            if len(node._sources) > 0:
                # We don't know the grammar, so we report a symbolic generator
                s += (
                    " := f("
                    + ", ".join([param.symbol.symbol for param in node._sources])
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

    def __repr__(self):
        return self.to_repr()

    def to_int(self, *args, **kwargs) -> Optional[int]:
        val = self.value()
        if val is None:
            return None
        try:
            return int(val, *args, **kwargs)
        except ValueError:
            return None

    def to_float(self) -> Optional[float]:
        val = self.value()
        if val is None:
            return None
        try:
            return float(val)
        except ValueError:
            return None

    def to_complex(self, *args, **kwargs) -> Optional[complex]:
        val = self.value()
        if val is None or isinstance(val, bytes):
            return None
        try:
            return complex(val, *args, **kwargs)
        except ValueError:
            return None

    def is_int(self, *args, **kwargs) -> bool:
        val = self.value()
        if val is None:
            return False
        try:
            int(val, *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_float(self) -> bool:
        val = self.value()
        if val is None:
            return False
        try:
            float(val)
        except ValueError:
            return False
        return True

    def is_complex(self, *args, **kwargs) -> bool:
        val = self.value()
        if val is None or isinstance(val, bytes):
            return False
        try:
            complex(val, *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_num(self) -> bool:
        return self.is_float()

    def split_end(self) -> "DerivationTree":
        cpy = copy.deepcopy(self)
        return cpy._split_end()

    def get_root(self, stop_at_argument_begin=False) -> "DerivationTree":
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
        me_idx = self.parent.children.index(self)
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
        grammar: "Grammar",
        tree_to_replace: "DerivationTree",
        new_subtree: "DerivationTree",
    ) -> "DerivationTree":
        return self.replace_multiple(grammar, {tree_to_replace: new_subtree})

    def replace_multiple(
        self,
        grammar: "Grammar",
        replacements: dict["DerivationTree", "DerivationTree"],
        path_to_replacement: Optional[dict[tuple, "DerivationTree"]] = None,
        current_path: Optional[tuple] = None,
    ) -> "DerivationTree":
        """
        Replace the subtree rooted at the given node with the new subtree.
        """
        if path_to_replacement is None:
            path_to_replacement = dict()
            for replacee, replacement in replacements.items():
                path_to_replacement[replacee.get_choices_path()] = replacement

        if current_path is None:
            current_path = self.get_choices_path()

        if current_path in path_to_replacement and not self.read_only:
            new_subtree = path_to_replacement[current_path].deepcopy(
                copy_children=True, copy_params=False, copy_parent=False
            )
            new_subtree._parent = self.parent
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
        if self.symbol == symbol and not (exclude_read_only and self.read_only):
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

    def children_values(self) -> list[int | str | bytes | None]:
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

    def descendant_values(self) -> list[int | str | bytes | None]:
        """
        Return all descendants of the current node
        """
        values = [node.value() for node in self.descendants()]
        # LOGGER.debug(f"descendant_values(): {values}")
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

    ## General purpose converters
    def _value(self) -> tuple[int | str | bytes | None, int]:
        """
        Convert the derivation tree into a standard Python value.
        Returns the value and the number of bits used.
        """
        if self.symbol.is_terminal:
            if isinstance(self.symbol.symbol, int):
                return self.symbol.symbol, 1
            else:
                return self.symbol.symbol, 0

        bits = 0
        aggregate = None
        for child in self._children:
            value, child_bits = child._value()

            if value is None:
                continue

            if aggregate is None:
                aggregate = value
                bits = child_bits

            elif isinstance(aggregate, str):
                if isinstance(value, str):
                    aggregate += value
                elif isinstance(value, bytes):
                    aggregate = aggregate.encode("utf-8") + value
                elif isinstance(value, int):
                    aggregate = aggregate + chr(value)
                    bits = 0
                else:
                    raise FandangoValueError(
                        f"Cannot compute {aggregate!r} + {value!r}"
                    )

            elif isinstance(aggregate, bytes):
                if isinstance(value, str):
                    aggregate += value.encode("utf-8")
                elif isinstance(value, bytes):
                    aggregate += value
                elif isinstance(value, int):
                    aggregate = aggregate + bytes([value])
                    bits = 0
                else:
                    raise FandangoValueError(
                        f"Cannot compute {aggregate!r} + {value!r}"
                    )

            elif isinstance(aggregate, int):
                if isinstance(value, str):
                    aggregate = bytes([aggregate]) + value.encode("utf-8")
                    bits = 0
                elif isinstance(value, bytes):
                    aggregate = bytes([aggregate]) + value
                    bits = 0
                elif isinstance(value, int):
                    aggregate = (aggregate << child_bits) + value
                    bits += child_bits
                else:
                    raise FandangoValueError(
                        f"Cannot compute {aggregate!r} + {value!r}"
                    )

        # LOGGER.debug(f"value(): {' '.join(repr(child.value()) for child in self._children)} = {aggregate!r} ({bits} bits)")

        return aggregate, bits

    def value(self) -> int | str | bytes | None:
        aggregate, bits = self._value()
        return aggregate

    def to_value(self) -> str:
        value = self.value()
        if isinstance(value, int):
            return "0b" + format(value, "b") + f" ({value})"
        return repr(self.value())

    ## Comparison operations
    def __eq__(self, other):
        if isinstance(other, DerivationTree):
            return self.__hash__() == other.__hash__()
        return self.value() == other

    def __le__(self, other):
        left = self.value()
        right = other.value() if isinstance(other, DerivationTree) else other
        return left <= right  # type: ignore[operator]

    def __lt__(self, other):
        left = self.value()
        right = other.value() if isinstance(other, DerivationTree) else other
        return left < right  # type: ignore[operator]

    def __ge__(self, other):
        left = self.value()
        right = other.value() if isinstance(other, DerivationTree) else other
        return left >= right  # type: ignore[operator]

    def __gt__(self, other):
        left = self.value()
        right = other.value() if isinstance(other, DerivationTree) else other
        return left > right  # type: ignore[operator]

    def __ne__(self, other):
        return not self.__eq__(other)  # type: ignore[operator]

    # Boolean operations
    def __bool__(self):
        return bool(self.value())

    ## Arithmetic operators
    def __add__(self, other):
        return self.value() + other

    def __sub__(self, other):
        return self.value() - other

    def __mul__(self, other):
        return self.value() * other

    def __matmul__(self, other):
        return self.value() @ other

    def __truediv__(self, other):
        return self.value() / other

    def __floordiv__(self, other):
        return self.value() // other

    def __mod__(self, other):
        return self.value() % other

    def __divmod__(self, other):
        return divmod(self.value(), other)

    def __pow__(self, other, modulo=None):
        return pow(self.value(), other, modulo)  # type: ignore[arg-type]

    def __radd__(self, other):
        return other + self.value()

    def __rsub__(self, other):
        return other - self.value()

    def __rmul__(self, other):
        return other * self.value()

    def __rmatmul__(self, other):
        return other @ self.value()

    def __rtruediv__(self, other):
        return other / self.value()

    def __rfloordiv__(self, other):
        return other // self.value()

    def __rmod__(self, other):
        return other % self.value()

    def __rdivmod__(self, other):
        return divmod(other, self.value())

    def __rpow__(self, other, modulo=None):
        return pow(other, self.value(), modulo)

    ## Bit operators
    def __lshift__(self, other):
        return self.value() << other

    def __rshift__(self, other):
        return self.value() >> other

    def __and__(self, other):
        return self.value() & other

    def __xor__(self, other):
        return self.value() ^ other

    def __or__(self, other):
        return self.value() | other

    def __rlshift__(self, other):
        return other << self.value()

    def __rrshift__(self, other):
        return other >> self.value()

    def __rand__(self, other):
        return other & self.value()

    def __rxor__(self, other):
        return other ^ self.value()

    def __ror__(self, other):
        return other | self.value()

    # Unary operators
    def __neg__(self):
        return -self.value()  # type: ignore[operator]

    def __pos__(self):
        return +self.value()  # type: ignore[operator]

    def __abs__(self):
        return abs(self.value())  # type: ignore[arg-type]

    def __invert__(self):
        return ~self.value()  # type: ignore[operator]

    # Converters
    def __int__(self):
        return int(self.value())  # type: ignore[arg-type]

    def __float__(self):
        return float(self.value())  # type: ignore[arg-type]

    def __complex__(self):
        return complex(self.value())  # type: ignore[arg-type]

    # Iterators
    def __contains__(self, other: Union["DerivationTree", Any]) -> bool:
        if isinstance(other, DerivationTree):
            return other in self._children
        return other in self.value()  # type: ignore[operator]

    def endswith(self, other: Union["DerivationTree", Any]) -> bool:
        if isinstance(other, DerivationTree):
            return self.endswith(other.value())
        return self.value().endswith(other)  # type: ignore[arg-type, union-attr]

    def startswith(self, other: Union["DerivationTree", Any]) -> bool:
        if isinstance(other, DerivationTree):
            return self.startswith(other.value())
        return self.value().startswith(other)  # type: ignore[arg-type, union-attr]

    def __iter__(self):
        return iter(self._children)

    # Everything else
    def __getattr__(self, name):
        """
        Catch-all: All other attributes and methods apply to the representation of the respective type (str, bytes, int).
        """
        value = self.value()
        tp = type(value)
        if name in tp.__dict__:

            def fn(*args, **kwargs):
                return tp.__dict__[name](value, *args, **kwargs)

            return fn

        raise AttributeError(f"{self.symbol} has no attribute {name!r}")


class SliceTree(DerivationTree):
    def __init__(self, children: list["DerivationTree"], read_only: bool = False):
        super().__init__(Slice(), children, read_only=read_only)
