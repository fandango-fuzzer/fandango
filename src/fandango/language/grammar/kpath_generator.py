from __future__ import annotations

import random
from collections import deque
from typing import Optional

from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.grammar.nodes.alternative import Alternative
from fandango.language.grammar.nodes.char_set import CharSet
from fandango.language.grammar.nodes.concatenation import Concatenation
from fandango.language.grammar.nodes.node import Node
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode
from fandango.language.grammar.nodes.repetition import Repetition
from fandango.language.grammar.nodes.terminal import TerminalNode
from fandango.language.symbols import NonTerminal, Symbol, Terminal
from fandango.language.tree import DerivationTree


class KPathSession:
    """
    Stateful generator that cycles through uncovered k-paths and constructs
    derivation trees that cover one target path at a time.

    The construction works on the same collapsed-tree semantics used by
    k-path extraction in Grammar._extract_k_paths_from_tree().
    """

    def __init__(
        self,
        grammar: Grammar,
        start_symbol: str | NonTerminal = "<start>",
        *,
        k: int,
    ):
        self.grammar = grammar
        self.start_symbol = (
            start_symbol
            if isinstance(start_symbol, NonTerminal)
            else NonTerminal(start_symbol)
        )
        self.k = k
        self.all_k_paths = list(
            grammar.generate_all_k_paths(k=k, non_terminal=self.start_symbol)
        )
        self.remaining_k_paths: list[KPath] = []
        self._reshuffle_targets()

    def _reshuffle_targets(self) -> None:
        self.remaining_k_paths = list(self.all_k_paths)
        random.shuffle(self.remaining_k_paths)

    def _immediate_symbols(self, node: Node) -> list[Symbol]:
        if isinstance(node, TerminalNode):
            return [node.symbol]
        if isinstance(node, CharSet):
            return [desc.to_symbol() for desc in node.descendents(self.grammar, False)]
        if isinstance(node, NonTerminalNode):
            return [node.symbol]
        if isinstance(node, Alternative):
            symbols: list[Symbol] = []
            for child in node.alternatives:
                symbols.extend(self._immediate_symbols(child))
            return symbols
        if isinstance(node, Concatenation):
            symbols: list[Symbol] = []
            for child in node.nodes:
                symbols.extend(self._immediate_symbols(child))
            return symbols
        if isinstance(node, Repetition):
            if node.max <= 0:
                return []
            return self._immediate_symbols(node.node)
        return []

    def _can_emit_immediate_symbol(self, node: Node, symbol: Symbol) -> bool:
        return symbol in self._immediate_symbols(node)

    def _minimal_charset_terminal(self, node: CharSet) -> TerminalNode:
        return next(iter(node.descendents(self.grammar, False)))

    def _expand_minimal(
        self, parent: DerivationTree, node: Node, max_nodes: int
    ) -> None:
        if isinstance(node, TerminalNode):
            parent.add_child(DerivationTree(node.symbol))
            return

        if isinstance(node, CharSet):
            terminal = self._minimal_charset_terminal(node)
            parent.add_child(DerivationTree(terminal.symbol))
            return

        if isinstance(node, NonTerminalNode):
            dummy = DerivationTree(node.symbol)
            if self.grammar.is_use_generator(dummy):
                node.fuzz(parent, self.grammar, max_nodes)
                return

            child_tree = DerivationTree(
                node.symbol,
                [],
                sender=node.sender,
                recipient=node.recipient,
                read_only=False,
            )
            parent.add_child(child_tree)
            self._expand_minimal(child_tree, self.grammar[node.symbol], max_nodes - 1)
            return

        if isinstance(node, Alternative):
            chosen = min(
                node.alternatives, key=lambda child: child.distance_to_completion
            )
            self._expand_minimal(parent, chosen, max_nodes - 1)
            return

        if isinstance(node, Concatenation):
            for child in node.nodes:
                self._expand_minimal(parent, child, max_nodes - 1)
            return

        if isinstance(node, Repetition):
            for _ in range(node.min):
                self._expand_minimal(parent, node.node, max_nodes - 1)
            return

        node.fuzz(parent, self.grammar, max_nodes)

    def _build_symbol_subtree(
        self,
        node: NonTerminalNode,
        branch: list[Symbol],
        branch_idx: int,
        max_nodes: int,
    ) -> tuple[DerivationTree, int]:
        child_tree = DerivationTree(
            node.symbol,
            [],
            sender=node.sender,
            recipient=node.recipient,
            read_only=False,
        )
        next_idx = branch_idx + 1
        if next_idx < len(branch):
            next_idx = self._expand_for_branch(
                child_tree,
                self.grammar[node.symbol],
                branch,
                next_idx,
                max_nodes - 1,
            )
        else:
            self._expand_minimal(child_tree, self.grammar[node.symbol], max_nodes - 1)
        return child_tree, next_idx

    def _emit_target_child(
        self,
        parent: DerivationTree,
        node: Node,
        branch: list[Symbol],
        branch_idx: int,
        max_nodes: int,
    ) -> int:
        target_symbol = branch[branch_idx]

        if isinstance(node, TerminalNode):
            parent.add_child(DerivationTree(node.symbol))
            if node.symbol == target_symbol:
                return branch_idx + 1
            return branch_idx

        if isinstance(node, CharSet):
            chosen = self._minimal_charset_terminal(node)
            for candidate in node.descendents(self.grammar, False):
                if candidate.to_symbol() == target_symbol:
                    chosen = candidate
                    break
            parent.add_child(DerivationTree(chosen.symbol))
            if chosen.symbol == target_symbol:
                return branch_idx + 1
            return branch_idx

        if isinstance(node, NonTerminalNode):
            if node.symbol != target_symbol:
                self._expand_minimal(parent, node, max_nodes)
                return branch_idx
            dummy = DerivationTree(node.symbol)
            if self.grammar.is_use_generator(dummy):
                node.fuzz(parent, self.grammar, max_nodes)
                return branch_idx
            subtree, next_idx = self._build_symbol_subtree(
                node, branch, branch_idx, max_nodes
            )
            parent.add_child(subtree)
            return next_idx

        return self._expand_for_branch(parent, node, branch, branch_idx, max_nodes)

    def _expand_for_branch(
        self,
        parent: DerivationTree,
        node: Node,
        branch: list[Symbol],
        branch_idx: int,
        max_nodes: int,
    ) -> int:
        if branch_idx >= len(branch):
            self._expand_minimal(parent, node, max_nodes)
            return branch_idx

        target_symbol = branch[branch_idx]

        if isinstance(node, (TerminalNode, CharSet, NonTerminalNode)):
            return self._emit_target_child(parent, node, branch, branch_idx, max_nodes)

        if isinstance(node, Alternative):
            candidates = [
                child
                for child in node.alternatives
                if self._can_emit_immediate_symbol(child, target_symbol)
            ]
            if not candidates:
                self._expand_minimal(parent, node, max_nodes)
                return branch_idx
            chosen = min(candidates, key=lambda child: child.distance_to_completion)
            return self._expand_for_branch(
                parent, chosen, branch, branch_idx, max_nodes - 1
            )

        if isinstance(node, Concatenation):
            branch_used = False
            for child in node.nodes:
                if not branch_used and self._can_emit_immediate_symbol(
                    child, target_symbol
                ):
                    branch_idx = self._emit_target_child(
                        parent, child, branch, branch_idx, max_nodes - 1
                    )
                    branch_used = True
                else:
                    self._expand_minimal(parent, child, max_nodes - 1)
            return branch_idx

        if isinstance(node, Repetition):
            use_branch = self._can_emit_immediate_symbol(node.node, target_symbol)
            repetitions = max(node.min, 1 if use_branch else 0)
            branch_used = False
            for _ in range(repetitions):
                if not branch_used and use_branch:
                    branch_idx = self._emit_target_child(
                        parent, node.node, branch, branch_idx, max_nodes - 1
                    )
                    branch_used = True
                else:
                    self._expand_minimal(parent, node.node, max_nodes - 1)
            return branch_idx

        self._expand_minimal(parent, node, max_nodes)
        return branch_idx

    def _shortest_prefix_to(self, symbol: Symbol) -> Optional[list[Symbol]]:
        if symbol == self.start_symbol:
            return [self.start_symbol]

        queue: deque[Symbol] = deque([self.start_symbol])
        predecessor: dict[Symbol, Optional[Symbol]] = {self.start_symbol: None}

        while queue:
            current = queue.popleft()
            if (
                not isinstance(current, NonTerminal)
                or current not in self.grammar.rules
            ):
                continue

            for child_symbol in self._immediate_symbols(self.grammar[current]):
                if child_symbol in predecessor:
                    continue
                predecessor[child_symbol] = current
                if child_symbol == symbol:
                    path = [symbol]
                    prev = current
                    while prev is not None:
                        path.append(prev)
                        prev = predecessor[prev]
                    path.reverse()
                    return path
                queue.append(child_symbol)

        return None

    def _build_branch_tree(self, target: KPath, max_nodes: int) -> DerivationTree:
        prefix = self._shortest_prefix_to(target[0])
        if prefix is None:
            return self.grammar.fuzz(self.start_symbol, max_nodes)

        branch = list(prefix)
        branch.extend(target[1:])
        root_node = NonTerminalNode(self.start_symbol, self.grammar.grammar_settings)
        root_tree, _ = self._build_symbol_subtree(root_node, branch, 0, max_nodes)
        root_tree._parent = None
        return root_tree

    def next_tree(self, max_nodes: int) -> DerivationTree:
        if self.k <= 0 or len(self.all_k_paths) == 0:
            return self.grammar.fuzz(self.start_symbol, max_nodes)

        if len(self.remaining_k_paths) == 0:
            self._reshuffle_targets()

        max_attempts = max(1, len(self.all_k_paths))
        for _ in range(max_attempts):
            target = self.remaining_k_paths.pop(0)
            tree = self._build_branch_tree(target, max_nodes)
            covered_paths = self.grammar._extract_k_paths_from_tree(tree, self.k)
            if target not in covered_paths:
                self.remaining_k_paths.append(target)
                continue

            covered_set = set(covered_paths)
            self.remaining_k_paths = [
                path for path in self.remaining_k_paths if path not in covered_set
            ]
            return tree

        return self.grammar.fuzz(self.start_symbol, max_nodes)
