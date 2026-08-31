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

    def children_of(self, state: ParseState) -> list[DerivationTree]:
        """
        Constructs the DerivationTree parsed up to the given state
        """
        cached = self._children_cache.get(id(state))
        if cached is not None:
            return cached

        # States whose construction has started but not finished.
        in_progress: set[int] = set()
        pending: list[tuple[ParseState, list[Edge], list[DerivationTree]]] = [
            (state, state.edge_chain(), [])
        ]
        in_progress.add(id(state))

        def resolve(target: ParseState) -> list[DerivationTree]:
            found = self._children_cache.get(id(target))
            return found if found is not None else []

        while pending:
            current, edge_chain, collected_children = pending[-1]
            descended = False
            while edge_chain:
                edge = edge_chain.pop()
                filler = edge.filler
                if isinstance(filler, DerivationTree):
                    collected_children.append(filler)
                    continue
                if isinstance(filler, list):
                    collected_children.extend(filler)
                    continue
                if isinstance(filler, LeoNest):
                    needed = filler.states()
                    missing = [
                        s
                        for s in needed
                        if id(s) not in self._children_cache
                        and id(s) not in in_progress
                    ]
                    if missing:
                        # Queue them all at once, so this chunk is retried
                        # once rather than once per chain element.
                        edge_chain.append(edge)
                        for missing_state in reversed(missing):
                            pending.append(
                                (missing_state, missing_state.edge_chain(), [])
                            )
                            in_progress.add(id(missing_state))
                        descended = True
                        break
                    collected_children.extend(self._expand_leo(filler, resolve))
                    continue
                assert isinstance(filler, ParseState)
                sub = self._children_cache.get(id(filler))
                if sub is None:
                    if id(filler) not in in_progress:
                        # Build the nested state first, then resume here.
                        edge_chain.append(edge)
                        pending.append((filler, filler.edge_chain(), []))
                        in_progress.add(id(filler))
                        descended = True
                        break
                    sub = []
                if filler.nonterminal in self._rules:
                    collected_children.append(
                        ParserDerivationTree(
                            filler.nonterminal, sub, **dict(edge.params or [])
                        )
                    )
                else:
                    collected_children.extend(sub)
            if descended:
                continue
            pending.pop()
            in_progress.discard(id(current))
            self._children_cache[id(current)] = collected_children
            self._children_keepalive.append(current)
        return self._children_cache[id(state)]

    def extra_alternatives(self, state: ParseState) -> Iterator[DerivationTree]:
        """
        The children of every derivation of `state` *except* the first.

        The first one is what `children_of` returns, so callers yield that and
        come back here only if someone asks for more. Nothing below is touched
        until then -- a caller that stops after one tree pays nothing for this.
        """
        alternatives = self._enumerate_children(state)
        next(alternatives, None)
        for children in alternatives:
            yield from children

    def _is_ambiguous(self, state: ParseState) -> bool:
        """
        Whether any state reachable from `state` has more than one derivation.

        Iterative, because the reachable set is as deep as the derivation and
        this runs on arbitrary input.
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
            # Safe to cache: a state only gains edges while its own column is
            # being processed, and enumeration starts once that column is done.
            # Everything reachable from `state` points backwards, into columns
            # that are already closed.
            for node_id in seen:
                self._ambiguous_cache[node_id] = False
        self._children_keepalive.append(state)
        return found

    def _enumerate_children(self, state: ParseState) -> Iterator[list[DerivationTree]]:
        """
        Every children list `state` can stand for, first one first.

        Unambiguous states short-circuit to `children_of`, so the recursion
        only ever follows the spine along which derivations actually branch.
        """
        if not self._is_ambiguous(state):
            yield self.children_of(state)
            return
        if not state.edges:
            yield []
            return
        for edge in state.edges:
            if edge.previous is None:
                prefixes: Iterator[list[DerivationTree]] = iter(([],))
            else:
                prefixes = self._enumerate_children(edge.previous)
            for prefix in prefixes:
                for tail in self._enumerate_filler(edge):
                    yield prefix + tail

    def _enumerate_filler(self, edge: Edge) -> Iterator[list[DerivationTree]]:
        """What one filled symbol can contribute to its parent's children."""
        filler = edge.filler
        if isinstance(filler, DerivationTree):
            yield [filler]
        elif isinstance(filler, list):
            yield list(filler)
        elif isinstance(filler, LeoNest):
            yield from self._enumerate_leo(filler)
        else:
            for sub in self._enumerate_children(filler):
                yield self._wrap_completed(filler.nonterminal, sub, edge.params)

    def _enumerate_leo(self, nest: LeoNest) -> Iterator[list[DerivationTree]]:
        """`_expand_leo`, branching wherever a nested state is ambiguous."""
        chain = list(nest.chain) if nest.chain is not None else []
        params = chain[0].dot_params if chain else nest.top_params
        for inner in self._enumerate_children(nest.inner):
            payload = self._wrap_completed(nest.inner.nonterminal, inner, params)
            yield from self._unwind_leo(chain, 0, payload, nest.top_params)

    def _unwind_leo(
        self,
        chain: list[ParseState],
        index: int,
        payload: list[DerivationTree],
        top_params: Optional[frozenset[tuple[str, Any]]],
    ) -> Iterator[list[DerivationTree]]:
        """
        Wrap `payload` in the skipped chain from `index` outwards.

        Loops while the chain stays unambiguous -- right recursion makes it one
        entry per input position, so recursing per entry would overflow.
        """
        while index < len(chain):
            waiter = chain[index]
            rest_params = (
                chain[index + 1].dot_params if index + 1 < len(chain) else top_params
            )
            if self._is_ambiguous(waiter):
                for waiter_children in self._enumerate_children(waiter):
                    children = list(waiter_children)
                    children.extend(payload)
                    yield from self._unwind_leo(
                        chain,
                        index + 1,
                        self._wrap_completed(waiter.nonterminal, children, rest_params),
                        top_params,
                    )
                return
            children = list(self.children_of(waiter))
            children.extend(payload)
            payload = self._wrap_completed(waiter.nonterminal, children, rest_params)
            index += 1
        yield payload

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
        payload = self._wrap_completed(
            nest.inner.nonterminal, resolve(nest.inner), params
        )
        node = chain
        while node is not None:
            waiter, rest = node.head, node.tail
            children = list(resolve(waiter))
            children.extend(payload)
            parent_params = (
                rest.head.dot_params if rest is not None else nest.top_params
            )
            payload = self._wrap_completed(waiter.nonterminal, children, parent_params)
            node = rest
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
