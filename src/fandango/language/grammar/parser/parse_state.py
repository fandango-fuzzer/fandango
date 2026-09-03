from collections.abc import Iterator
from typing import Any, Optional, Union

from fandango.language.symbols import NonTerminal, Symbol
from fandango.language.tree import DerivationTree

#: One symbol of a rule, with its parameters (e.g. sender/recipient).
RuleSymbol = tuple[Symbol, frozenset[tuple[str, Any]]]

#: One alternative of a compiled rule: the symbols to match, in order.
RuleAlternative = tuple[RuleSymbol, ...]

#: What can occupy one symbol along a derivation; see `Edge.filler`.
Filler = Union[DerivationTree, "ParseState", "LeoNest", list[DerivationTree]]


class Edge:
    """
    Pointer to the previous ParseState.
    `filler` holds the parsed value between the previous and the current parse state.
    """

    __slots__ = ("previous", "filler", "params")

    def __init__(
        self,
        previous: Optional["ParseState"],
        filler: Filler,
        params: Optional[frozenset[tuple[str, Any]]] = None,
    ):
        self.previous = previous
        self.filler = filler
        self.params = params

    def __repr__(self) -> str:
        return f"Edge({self.filler!r})"


class ReductionChain:
    """
    Stores the nodes Leo's shortcut jumped over. `head` is the innermost node,
    starting from the completed symbol.
    `tail` are further reduction chains going up the tree towards the direction
    of the root node, ending one below `LeoEntry.top`.
    """

    __slots__ = ("head", "tail")

    def __init__(self, head: "ParseState", tail: Optional["ReductionChain"] = None):
        self.head = head
        self.tail = tail

    def __iter__(self) -> Iterator["ParseState"]:
        link: Optional[ReductionChain] = self
        while link is not None:
            yield link.head
            link = link.tail

    def __repr__(self) -> str:
        return f"ReductionChain({list(self)!r})"


class LeoEntry:
    """
    Stores the shortcut for one Leo reduction path. `top` is the item that
    gets advanced in place of the whole path. `chain` is the path between the
    completed symbol (in the table's column) and `top`, both ends excluded.
    If both are neighbors, `chain` is None.
    """

    __slots__ = ("top", "chain")

    def __init__(self, top: "ParseState", chain: Optional[ReductionChain] = None):
        self.top = top
        self.chain = chain

    def push(self, waiter: "ParseState") -> "LeoEntry":
        """The same top, with `waiter` prepended to the skipped chain."""
        return LeoEntry(self.top, ReductionChain(waiter, self.chain))

    def __repr__(self) -> str:
        return f"LeoEntry(top={self.top!r})"


class LeoNest:
    """
    Stands in for the completions Leo's shortcut skipped, as one edge filler.
    `inner` is the item that completed, `chain` the skipped nodes above it, and
    `top_params` the parameters of the symbol being filled.
    The `top` field (towards which) `top_params` applies to is the symbol of its Edge.previous.
    """

    __slots__ = ("chain", "inner", "top_params")

    def __init__(
        self,
        chain: Optional[ReductionChain],
        inner: "ParseState",
        top_params: Optional[frozenset[tuple[str, Any]]],
    ):
        self.chain = chain
        self.inner = inner
        self.top_params = top_params

    def states(self) -> list["ParseState"]:
        """Every state whose children the nest needs, innermost first."""
        needed = [self.inner]
        if self.chain is not None:
            needed.extend(self.chain)
        return needed

    def __repr__(self) -> str:
        return f"LeoNest({self.inner!r})"


class ParseState:
    __slots__ = (
        "nonterminal",
        "position",
        "symbols",
        "dot",
        "matched_length",
        "force_completed",
        "edges",
        "_hash",
    )

    # Beartype type-definition
    edges: list[Edge]

    def __init__(
        self,
        nonterminal: NonTerminal,
        position: int,
        symbols: RuleAlternative,
        dot: int = 0,
        children: Optional[list[DerivationTree]] = None,
        matched_length: int = 0,
        force_completed: bool = False,
    ):
        self.nonterminal = nonterminal
        self.position = position
        self.symbols = symbols
        self.dot = dot
        self.matched_length = matched_length
        # Completed although its rule was not matched to the end; only an
        # incomplete parse does that, to see how the input could go on.
        self.force_completed = force_completed
        self.edges = []
        if children:
            self.edges.append(Edge(None, list(children), None))
        self._hash: Optional[int] = None

    def add_edge(
        self,
        previous: Optional["ParseState"],
        filler: Filler,
        params: Optional[frozenset[tuple[str, Any]]] = None,
    ) -> None:
        """Record that this state is reachable from `previous` via `filler`."""
        self.edges.append(Edge(previous, filler, params))

    def predecessor(self) -> Optional["ParseState"]:
        """The state one symbol back along the first derivation, if any."""
        return self.edges[0].previous if self.edges else None

    def last_filler(self) -> Optional[Filler]:
        """What filled the most recent symbol along the first derivation."""
        return self.edges[0].filler if self.edges else None

    def set_edge(
        self,
        previous: Optional["ParseState"],
        filler: Filler,
        params: Optional[frozenset[tuple[str, Any]]] = None,
    ) -> None:
        self.edges = [Edge(previous, filler, params)]

    def has_children(self) -> bool:
        """
        Whether this state has any children.
        """
        current: Optional[ParseState] = self
        while current is not None and current.edges:
            edge = current.edges[0]
            filler = edge.filler
            if isinstance(filler, list):
                if filler:
                    return True
            else:
                # A tree, a state, or a Leo nest each fill one symbol, and so
                # become one child even when what they matched is empty.
                return True
            current = edge.previous
        return False

    @property
    def next_symbol(self) -> Optional[Symbol]:
        return self.symbols[self.dot][0] if self.dot < len(self.symbols) else None

    @property
    def next_params(self) -> Optional[frozenset[tuple[str, Any]]]:
        return self.symbols[self.dot][1] if self.dot < len(self.symbols) else None

    @property
    def is_terminal_partial_match(self) -> bool:
        """
        Whether the terminal under the dot is only partially matched.
        """
        return self.matched_length > 0

    @property
    def is_finished(self) -> bool:
        return (
            self.dot >= len(self.symbols)
            and not self.is_terminal_partial_match
            and not self.force_completed
        )

    def next_symbol_is_nonterminal(self) -> bool:
        return (
            self.dot < len(self.symbols) and self.symbols[self.dot][0].is_non_terminal
        )

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(
                (
                    self.nonterminal,
                    self.position,
                    self.dot,
                    len(self.symbols),
                    self.symbols[0][0] if self.symbols else None,
                    self.force_completed,
                )
            )
        return self._hash

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, ParseState)
            and self.nonterminal == other.nonterminal
            and self.position == other.position
            and self.symbols == other.symbols
            and self.dot == other.dot
            and self.force_completed == other.force_completed
        )

    def __repr__(self) -> str:
        return (
            f"({self.nonterminal.format_as_spec()} -> "
            + "".join(
                [
                    f"{'•' if i == self.dot else ''}{s[0]!s}"
                    for i, s in enumerate(self.symbols)
                ]
            )
            + ("•" if self.is_finished else "")
            + f", column {self.position}"
            + (", force_completed" if self.force_completed else "")
            + ")"
        )

    def next(self, force_completed: bool = False) -> "ParseState":
        """Returns self rule, with 'dot' advanced by one position. (edges not copied)"""
        return ParseState(
            self.nonterminal,
            self.position,
            self.symbols,
            self.dot + 1,
            None,
            self.matched_length,
            self.force_completed or force_completed,
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> "ParseState":
        """
        Copy self, by value. Only copies edges by reference.
        """
        copied = ParseState(
            self.nonterminal,
            self.position,
            self.symbols,
            self.dot,
            None,
            self.matched_length,
            self.force_completed,
        )
        copied.edges = list(self.edges)
        memo[id(self)] = copied
        return copied

    def copy(self) -> "ParseState":
        return self.__deepcopy__(dict())
