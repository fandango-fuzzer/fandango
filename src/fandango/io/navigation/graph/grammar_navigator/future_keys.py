from collections.abc import Generator, Hashable
from typing import Optional

from fandango.io.navigation.graph.grammar_navigator.grammar_graph_converter import (
    GrammarGraphNode,
    LazyGrammarGraphNode,
)
from fandango.io.navigation.nested_steps import run_nested_steps
from fandango.language.grammar.nodes.repetition import Repetition


class FutureKeys:
    """
    Gives graph nodes with the same future the same key:
    the same grammar node, followed by the same nodes after its rule ends.
    """

    def __init__(self) -> None:
        self._keys: dict[GrammarGraphNode, Hashable] = {}
        # None while the key of an instance is being computed, so a rule that follows itself is noticed.
        self._continuation_keys: dict[
            GrammarGraphNode, Optional[frozenset[Hashable]]
        ] = {}

    def key(self, node: GrammarGraphNode) -> Hashable:
        return run_nested_steps(self._key_steps(node), self._key_steps)

    def _key_steps(
        self, node: GrammarGraphNode
    ) -> Generator[GrammarGraphNode, Hashable, Hashable]:
        """Computes the key of node; yields the nodes whose keys it needs first."""
        if node not in self._keys:
            instance = self._enclosing_instance(node)
            continuation = (
                None
                if instance is None
                else (yield from self._continuation_key_steps(instance))
            )
            self._keys[node] = (
                ("instance", id(node))
                if continuation is None
                else (id(node.node), continuation)
            )
        return self._keys[node]

    def _continuation_key_steps(
        self, instance: GrammarGraphNode
    ) -> Generator[GrammarGraphNode, Hashable, Optional[frozenset[Hashable]]]:
        """
        Computes the keys of the nodes that follow the rule instance; yields those nodes first.
        Returns None if the instance follows itself.
        """
        if not isinstance(instance, LazyGrammarGraphNode):
            return frozenset()
        if instance not in self._continuation_keys:
            self._continuation_keys[instance] = None
            following_keys = []
            for following in instance._pre_load_reaches:
                following_keys.append((yield following))
            self._continuation_keys[instance] = frozenset(following_keys)
        return self._continuation_keys[instance]

    @staticmethod
    def _enclosing_instance(node: GrammarGraphNode) -> Optional[GrammarGraphNode]:
        """Returns the rule instance that node lies in, or None if node lies in a repetition."""
        current = node.parent
        while current is not None and not isinstance(current, LazyGrammarGraphNode):
            if isinstance(current.node, Repetition):
                return None
            if current.parent is None:
                return current
            current = current.parent
        return current
