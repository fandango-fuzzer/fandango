from collections.abc import Callable, Iterator
from typing import Any, Optional

from fandango.errors import FandangoValueError
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.parser.parse_state import Edge, LeoNest, ParseState
from fandango.language.grammar.parser.parser_tree import ParserDerivationTree
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

#: Which repetitions a node sits inside: (repetition id, iteration, index).
Repetitions = list[tuple[str, int, int]]


class _Choices:
    __slots__ = ("vector", "arities")

    def __init__(self, vector: list[int]) -> None:
        self.vector = vector
        self.arities: list[int] = []

    def pick(self, node: ParseState) -> Edge:
        edges = node.edges
        if len(edges) == 1:
            return edges[0]
        index = len(self.arities)
        self.arities.append(len(edges))
        return edges[self.vector[index] if index < len(self.vector) else 0]


class _Frame:
    """One state whose children `ForestBuilder.children_of` is collecting."""

    __slots__ = ("state", "chain", "children")

    def __init__(self, state: ParseState) -> None:
        self.state = state
        self.chain: Optional[list[Edge]] = None
        self.children: list[DerivationTree] = []


class ForestBuilder:
    """
    Converts a parser state into the DerivationTree it represents.
    """

    def __init__(
        self,
        rules: dict[NonTerminal, Any],
        nodes: dict[str, Node],
    ):
        self._rules = rules
        self._nodes = nodes
        self._children_cache: dict[int, list[DerivationTree]] = {}
        self._children_keepalive: list[ParseState] = []
        self._ambiguous_cache: dict[int, bool] = {}

    def reset(self) -> None:
        """Clears caches. Call when starting a new parse."""
        self._children_cache.clear()
        self._children_keepalive.clear()
        self._ambiguous_cache.clear()

    def children_of(
        self, state: ParseState, choices: Optional[_Choices] = None
    ) -> list[DerivationTree]:
        """
        The children `state` stands for, along one derivation.
        """
        if choices is None:
            cached = self._children_cache.get(id(state))
            if cached is not None:
                return cached

        built = self._children_cache if choices is None else {}
        in_progress: set[int] = set()

        def available(target: ParseState) -> bool:
            if choices is None:
                return id(target) in built
            return id(target) in built or not self._is_ambiguous(target)

        def take(target: ParseState) -> list[DerivationTree]:
            """The children of an available state; `[]` for one still open."""
            if choices is None:
                found = built.get(id(target))
                return found if found is not None else []
            found = built.pop(id(target), None)
            return found if found is not None else self.children_of(target)

        def open_frame(target: ParseState) -> None:
            pending.append(_Frame(target))
            if choices is None:
                in_progress.add(id(target))

        pending: list[_Frame] = []
        open_frame(state)
        while pending:
            frame = pending[-1]
            if frame.chain is None:
                frame.chain = self._chosen_chain(frame.state, choices, frame.children)
            chain, children = frame.chain, frame.children
            descended = False
            while chain:
                edge = chain.pop()
                filler = edge.filler
                if isinstance(filler, DerivationTree):
                    children.append(filler)
                    continue
                if isinstance(filler, list):
                    children.extend(filler)
                    continue
                if isinstance(filler, LeoNest):
                    missing = [
                        s
                        for s in filler.states()
                        if not available(s) and id(s) not in in_progress
                    ]
                    if missing:
                        # Build them all before retrying this edge, innermost
                        # first: that is the order their choices come in.
                        chain.append(edge)
                        for s in reversed(missing):
                            open_frame(s)
                        descended = True
                        break
                    children.extend(self._expand_leo(filler, take))
                    continue
                assert isinstance(filler, ParseState)
                if available(filler):
                    sub = take(filler)
                elif id(filler) in in_progress:
                    sub = []
                else:
                    # Build the nested state first, then resume here.
                    chain.append(edge)
                    open_frame(filler)
                    descended = True
                    break
                children.extend(
                    self._wrap_completed(filler.nonterminal, sub, edge.params)
                )
            if descended:
                continue
            pending.pop()
            built[id(frame.state)] = children
            if choices is None:
                in_progress.discard(id(frame.state))
                self._children_keepalive.append(frame.state)
        return take(state)

    def extra_alternatives(self, state: ParseState) -> Iterator[DerivationTree]:
        """
        The children of every derivation of `state` except the first.
        """
        if not self._is_ambiguous(state):
            return

        choices = _Choices([])
        self.children_of(state, choices)
        vector = [0] * len(choices.arities)
        while True:
            while vector and vector[-1] + 1 == choices.arities[len(vector) - 1]:
                vector.pop()
            if not vector:
                return
            vector[-1] += 1
            choices = _Choices(vector)
            yield from self.children_of(state, choices)
            vector += [0] * (len(choices.arities) - len(vector))

    def _is_ambiguous(self, state: ParseState) -> bool:
        """
        Whether any state reachable from `state` has more than one derivation.
        """
        cached = self._ambiguous_cache.get(id(state))
        if cached is not None:
            return cached

        seen: set[int] = set()
        stack: list[ParseState] = [state]
        found = False
        while stack:
            node = stack.pop()
            if id(node) in seen:
                continue
            seen.add(id(node))
            if len(node.edges) > 1:
                found = True
                break
            for edge in node.edges:
                if edge.previous is not None:
                    stack.append(edge.previous)
                filler = edge.filler
                if isinstance(filler, LeoNest):
                    stack.extend(filler.states())
                elif isinstance(filler, ParseState):
                    stack.append(filler)

        if not found:
            for node_id in seen:
                self._ambiguous_cache[node_id] = False
        self._children_keepalive.append(state)
        return found

    def _chosen_chain(
        self,
        state: ParseState,
        choices: Optional[_Choices],
        children: list[DerivationTree],
    ) -> list[Edge]:
        """
        The edges from `state` back to where its item began, leftmost last.
        """
        chain: list[Edge] = []
        node: Optional[ParseState] = state
        while node is not None and node.edges:
            if choices is None:
                edge = node.edges[0]
            elif node is not state and not self._is_ambiguous(node):
                children.extend(self.children_of(node))
                break
            else:
                edge = choices.pick(node)
            chain.append(edge)
            node = edge.previous
        return chain

    def _wrap_completed(
        self,
        nonterminal: NonTerminal,
        children: list[DerivationTree],
        params: Optional[frozenset[tuple[str, Any]]],
    ) -> list[DerivationTree]:
        """A completed non-terminal as it appears among its parent's children."""
        if nonterminal in self._rules:
            return [ParserDerivationTree(nonterminal, children, **dict(params or []))]
        return children

    def _expand_leo(
        self, nest: LeoNest, resolve: Callable[[ParseState], list[DerivationTree]]
    ) -> list[DerivationTree]:
        """
        Rebuild DerivationTrees for LeoNest optimizations.
        """
        chain = nest.chain
        params = chain.head.dot_params if chain is not None else nest.top_params
        segments = [
            self._wrap_completed(nest.inner.nonterminal, resolve(nest.inner), params)
        ]
        node = chain
        while node is not None:
            waiter, rest = node.head, node.tail
            if waiter.nonterminal in self._rules:
                children = list(resolve(waiter))
                for segment in reversed(segments):
                    children.extend(segment)
                parent_params = (
                    rest.head.dot_params if rest is not None else nest.top_params
                )
                segments = [
                    self._wrap_completed(waiter.nonterminal, children, parent_params)
                ]
            else:
                segments.append(resolve(waiter))
            node = rest
        payload: list[DerivationTree] = []
        for segment in reversed(segments):
            payload.extend(segment)
        return payload

    def to_derivation_tree(self, tree: DerivationTree) -> DerivationTree:
        """
        Converts the ParserDerivationTree to normal DerivationTrees
        """
        descent: list[tuple[DerivationTree, Repetitions]] = []
        todo: list[tuple[DerivationTree, Repetitions]] = [(tree, [])]
        while todo:
            node, reps = todo.pop()
            descent.append((node, reps))
            child_reps = self._child_repetitions(node, reps)
            todo.extend(reversed(list(zip(node.children, child_reps, strict=False))))

        built: dict[int, DerivationTree] = {}
        for node, reps in reversed(descent):
            built[id(node)] = DerivationTree(
                node.symbol,
                [built[id(child)] for child in node.children],
                parent=node.parent,
                sources=node.sources,
                sender=node.sender,
                recipient=node.recipient,
                read_only=node.read_only,
                origin_repetitions=reps,
            )
        return built[id(tree)]

    def _child_repetitions(
        self, node: DerivationTree, inherited: Repetitions
    ) -> list[Repetitions]:
        """
        The `origin_repetitions` each child of `node` inherits.
        """
        symbol = node.symbol
        if not (isinstance(symbol, NonTerminal) and symbol.name() in self._nodes):
            # Not a control-flow node: the chain restarts below it.
            return [[] for _ in node.children]

        cf_node = self._nodes[symbol.name()]
        if not isinstance(cf_node, Repetition):
            return [list(inherited) for _ in node.children]

        cf_node.iteration += 1
        return [
            inherited + [(cf_node.id, cf_node.iteration, index)]
            for index in range(len(node.children))
        ]

    def collapse(self, tree: Optional[DerivationTree]) -> Optional[DerivationTree]:
        if tree is None:
            return None
        if isinstance(tree.symbol, NonTerminal):
            if str(tree.symbol.value()).startswith("<__"):
                raise FandangoValueError(
                    "Can't collapse a tree with an implicit root node"
                )
        return self._collapse(tree)[0]

    def _collapse(self, tree: DerivationTree) -> list[DerivationTree]:
        """
        Drop control-flow nodes.
        """
        order: list[DerivationTree] = []
        stack = [tree]
        while stack:
            node = stack.pop()
            order.append(node)
            stack.extend(node.children)

        collapsed: dict[int, list[DerivationTree]] = {}
        for node in reversed(order):
            reduced: list[DerivationTree] = []
            for child in node.children:
                reduced.extend(collapsed.pop(id(child)))

            if isinstance(node.symbol, NonTerminal) and node.symbol.name().startswith(
                "<__"
            ):
                collapsed[id(node)] = reduced
            else:
                collapsed[id(node)] = [
                    DerivationTree(
                        node.symbol,
                        children=reduced,
                        sources=node.sources,
                        read_only=node.read_only,
                        recipient=node.recipient,
                        sender=node.sender,
                        origin_repetitions=node.origin_repetitions,
                    )
                ]
        return collapsed[id(tree)]
