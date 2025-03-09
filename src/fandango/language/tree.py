import copy
from typing import Optional, List, Any, Union, Set, Tuple

from fandango.language.symbol import Symbol, NonTerminal, Terminal, Slice
from io import StringIO, BytesIO

from fandango.logger import LOGGER, print_exception

from fandango import FandangoValueError


class DerivationTree:
    """
    This class is used to represent a node in the derivation tree.
    """

    def __init__(
        self,
        symbol: Symbol,
        children: Optional[List["DerivationTree"]] = None,
        parent: Optional["DerivationTree"] = None,
        read_only: bool = False,
    ):
        if not isinstance(symbol, Symbol):
            raise TypeError(f"Expected Symbol, got {type(symbol)}")

        self.hash_cache = None
        self._parent: Optional["DerivationTree"] = parent
        self.symbol: Symbol = symbol
        self._children: list["DerivationTree"] = []
        self.read_only = read_only
        self._size = 1
        self.set_children(children or [])

    def __len__(self):
        return len(self._children)

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

    def get_root(self):
        if self._parent is None:
            return self
        return self._parent.get_root()

    def set_all_read_only(self, read_only: bool):
        self.read_only = read_only
        for child in self._children:
            child.set_all_read_only(read_only)

    def set_children(self, children: List["DerivationTree"]):
        self._children = children
        self._size = 1 + sum(child.size() for child in self._children)
        for child in self._children:
            child._parent = self
        self.invalidate_hash()

    def add_child(self, child: "DerivationTree"):
        self._children.append(child)
        self._size += child.size()
        child._parent = self
        self.invalidate_hash()

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

    def __getitem__(self, item) -> "DerivationTree":
        if isinstance(item, list) and len(item) == 1:
            item = item[0]
        items = self._children.__getitem__(item)
        if isinstance(items, list):
            return SliceTree(items)
        else:
            return items

    def __hash__(self):
        """
        Computes a hash of the derivation tree based on its structure and symbols.
        """
        if self.hash_cache is None:
            self.hash_cache = hash(
                (
                    self.symbol,
                    tuple(hash(child) for child in self._children),
                )
            )
        return self.hash_cache

    def __tree__(self):
        return self.symbol, [child.__tree__() for child in self._children]

    @staticmethod
    def from_tree(tree: Tuple[str, List[Tuple[str, List]]]) -> "DerivationTree":
        symbol, children = tree
        if not isinstance(symbol, str):
            raise TypeError(f"{symbol} must be a string")
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
        copied = DerivationTree(self.symbol, [], read_only=self.read_only)
        memo[id(self)] = copied

        # Deepcopy the children
        copied._children = [copy.deepcopy(child, memo) for child in self._children]

        # Set parent pointers
        for child in copied._children:
            child._parent = copied

        # Set the parent to None or update if necessary
        copied._parent = None  # or copy.deepcopy(self.parent, memo) if parent is needed

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

        if isinstance(val, int):
            # This is a bit value; convert to bytes
            val = int(val).to_bytes(val // 256 + 1)
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
        if len(self._children) == 1:
            s += ", " + self._children[0].to_tree(indent, start_indent=0)
        else:
            has_children = False
            for child in self._children:
                s += ",\n" + child.to_tree(indent + 1, start_indent=indent + 1)
                has_children = True
            if has_children:
                s += "\n" + "  " * indent
        s += ")"
        return s

    def to_repr(self, indent=0, start_indent=0) -> str:
        """
        Output the derivation tree in internal representation.
        """
        s = "  " * start_indent + "DerivationTree(" + repr(self.symbol)
        if len(self._children) == 1:
            s += ", [" + self._children[0].to_repr(indent, start_indent=0) + "])"
        elif len(self._children) >= 1:
            s += ",\n" + "  " * indent + "  [\n"
            for child in self._children:
                s += child.to_repr(indent + 2, start_indent=indent + 2)
                s += ",\n"
            s += "  " * indent + "  ]\n" + "  " * indent + ")"
        else:
            s += ")"
        return s

    def to_grammar(self, include_position=True, include_value=True) -> str:
        """
        Output the derivation tree as (specialized) grammar
        """
        bit_count = -1
        byte_count = 0

        def _to_grammar(node, indent=0, start_indent=0) -> str:
            """
            Output the derivation tree as (specialized) grammar
            """
            assert isinstance(node.symbol.symbol, str)
            nonlocal bit_count, byte_count, include_position, include_value

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
                    s += "\n" + _to_grammar(child, indent + 1, start_indent=indent + 1)
            return s

        return _to_grammar(self)

    def __repr__(self):
        return self.to_repr()

    def to_int(self, *args, **kwargs):
        try:
            return int(self.value(), *args, **kwargs)
        except ValueError:
            return None

    def to_float(self):
        try:
            return float(self.value())
        except ValueError:
            return None

    def to_complex(self, *args, **kwargs):
        try:
            return complex(self.value(), *args, **kwargs)
        except ValueError:
            return None

    def is_int(self, *args, **kwargs):
        try:
            int(self.value(), *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_float(self):
        try:
            float(self.value())
        except ValueError:
            return False
        return True

    def is_complex(self, *args, **kwargs):
        try:
            complex(self.value(), *args, **kwargs)
        except ValueError:
            return False
        return True

    def is_num(self):
        return self.is_float()

    def replace(self, tree_to_replace, new_subtree):
        """
        Replace the subtree rooted at the given node with the new subtree.
        """
        if self == tree_to_replace and not self.read_only:
            return new_subtree
        else:
            return DerivationTree(
                self.symbol,
                [
                    child.replace(tree_to_replace, new_subtree)
                    for child in self._children
                ],
                read_only=self.read_only,
            )

    def get_non_terminal_symbols(self, exclude_read_only=True) -> Set[NonTerminal]:
        """
        Retrieve all non-terminal symbols present in the derivation tree.
        """
        symbols = set()
        if self.symbol.is_non_terminal and not (exclude_read_only and self.read_only):
            symbols.add(self.symbol)
        for child in self._children:
            symbols.update(child.get_non_terminal_symbols(exclude_read_only))
        return symbols

    def find_all_nodes(
        self, symbol: NonTerminal, exclude_read_only=True
    ) -> List["DerivationTree"]:
        """
        Find all nodes in the derivation tree with the given non-terminal symbol.
        """
        nodes = []
        if self.symbol == symbol and not (exclude_read_only and self.read_only):
            nodes.append(self)
        for child in self._children:
            nodes.extend(child.find_all_nodes(symbol))
        return nodes

    @property
    def children(self) -> Optional[List["DerivationTree"]]:
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

    def children_values(self):
        """
        Return values of all direct children
        """
        return [node.value() for node in self.children()]

    def flatten(self):
        """
        Flatten the derivation tree into a list of symbols.
        """
        flat = [self]
        for child in self._children:
            flat.extend(child.flatten())
        return flat

    def descendants(self):
        """
        Return all descendants of the current node
        """
        return self.flatten()[1:]

    def descendant_values(self):
        """
        Return all descendants of the current node
        """
        values = [node.value() for node in self.descendants()]
        # LOGGER.debug(f"descendant_values(): {values}")
        return values

    def get_index(self, target):
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
                    raise FandangoValueError(f"Cannot compute {aggregate!r} + {value!r}")

            elif isinstance(aggregate, bytes):
                if isinstance(value, str):
                    aggregate += value.encode("utf-8")
                elif isinstance(value, bytes):
                    aggregate += value
                elif isinstance(value, int):
                    aggregate = aggregate + value.to_bytes()
                    bits = 0
                else:
                    raise FandangoValueError(f"Cannot compute {aggregate!r} + {value!r}")

            elif isinstance(aggregate, int):
                if isinstance(value, str):
                    aggregate = aggregate.to_bytes() + value.encode("utf-8")
                    bits = 0
                elif isinstance(value, bytes):
                    aggregate = aggregate.to_bytes() + value
                    bits = 0
                elif isinstance(value, int):
                    aggregate = (aggregate << child_bits) + value
                    bits += child_bits
                else:
                    raise FandangoValueError(f"Cannot compute {aggregate!r} + {value!r}")

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
            return self.__tree__() == other.__tree__()
        return self.value() == other

    def __le__(self, other):
        if isinstance(other, DerivationTree):
            return self.value() <= other.value()
        return self.value() <= other

    def __lt__(self, other):
        if isinstance(other, DerivationTree):
            return self.value() < other.value()
        return self.value() < other

    def __ge__(self, other):
        if isinstance(other, DerivationTree):
            return self.value() >= other.value()
        return self.value() >= other

    def __gt__(self, other):
        if isinstance(other, DerivationTree):
            return self.value() > other.value()
        return self.value() > other

    def __ne__(self, other):
        return not self.__eq__(other)

    ## Boolean operations
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
        return pow(self.value(), other, modulo)

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
        return -self.value()

    def __pos__(self):
        return +self.value()

    def __abs__(self):
        return abs(self.value())

    def __invert__(self):
        return ~self.value()

    # Converters
    def __int__(self):
        return int(self.value())

    def __float__(self):
        return float(self.value())

    def __complex__(self):
        return complex(self.value())

    def __str__(self):
        return self.to_string()

    def __bytes__(self):
        return self.to_bytes()

    ## Iterators
    def __contains__(self, other: Union["DerivationTree", Any]) -> bool:
        if isinstance(other, DerivationTree):
            return other in self._children
        return other in self.value()

    def __iter__(self):
        return iter(self._children)

    ## Everything else
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
    def __init__(self, children: List["DerivationTree"], read_only: bool = False):
        super().__init__(Slice(), children, read_only=read_only)
