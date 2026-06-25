from typing import Optional

from fandango.io.navigation.coverage.kpath_coverage import KPathCoverage
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class PacketCoverageFilter:
    def __init__(self, diversity_k: int, grammar: Grammar):
        self._diversity_k = diversity_k
        self._grammar = grammar
        self._coverage = KPathCoverage(grammar, diversity_k)
        self._submitted_solutions: set[int] = set()
        self.hold_back_solutions: set[DerivationTree] = set()
        self._solution_set: set[int] = set()
        self._past_trees: list[DerivationTree] = []

    def get_past_msgs(
        self, packet_type: Optional[PacketNonTerminal] = None
    ) -> set[DerivationTree]:
        msgs = []
        for tree in self._past_trees:
            msgs.extend(tree.protocol_msgs())
        msg_trees = set(map(lambda x: x.msg, msgs))
        if packet_type is None:
            return msg_trees
        return {
            msg
            for msg in msg_trees
            if isinstance(msg.symbol, NonTerminal)
            and PacketNonTerminal(msg.sender, msg.recipient, msg.symbol) == packet_type
        }

    def set_existing_derivations(self, past_trees: list[DerivationTree]) -> None:
        self._past_trees = past_trees
        self.hold_back_solutions.clear()
        self._solution_set.clear()
        for tree in past_trees:
            for msg in tree.protocol_msgs():
                tree = msg.msg
                key = (msg.sender, msg.recipient, tree)
                self._submitted_solutions.add(hash(key))

    def _is_path_start_with(self, state_path: KPath, path: KPath) -> int:
        n = len(state_path)
        m = len(path)
        max_overlap = min(n, m)
        for overlap in range(max_overlap, 0, -1):
            if state_path[-overlap:] == path[:overlap]:
                return overlap
        return 0

    def filter(self, individual: DerivationTree) -> Optional[DerivationTree]:

        if len(individual.protocol_msgs()) != 0:
            msg = individual.protocol_msgs()[-1].msg
            symbol = msg.symbol
            assert isinstance(symbol, NonTerminal)
            msg_key = PacketNonTerminal(msg.sender, msg.recipient, symbol)
            msg_hash = hash(msg)
        else:
            msg = None
            symbol = None
            msg_key = None
            msg_hash = None

        if msg is None:
            return individual

        assert msg_hash is not None and msg_key is not None
        state_path_tree = msg.get_path()
        if len(state_path_tree) > self._diversity_k:
            state_path_tree = state_path_tree[-self._diversity_k :]
        state_path = tuple(map(lambda x: x.symbol, state_path_tree))
        assert isinstance(symbol, NonTerminal)
        uncovered_paths = self._coverage.uncovered(
            list(self.get_past_msgs(msg_key)),
            symbol,
            overlap_to_root=True,
        )

        overlap_to_root = any(
            0 < self._is_path_start_with(state_path, path) < self._diversity_k
            for path in uncovered_paths
        )

        old_coverage = self._coverage.ratio(
            list(self.get_past_msgs(msg_key)),
            symbol,
            overlap_to_root=overlap_to_root,
        )
        new_coverage = self._coverage.ratio(
            list(self.get_past_msgs(msg_key)) + [msg],
            symbol,
            overlap_to_root=overlap_to_root,
        )
        if old_coverage < new_coverage or new_coverage == 1.0:
            if new_coverage < 1.0:
                self._solution_set.add(msg_hash)
            return individual
        elif (
            msg_hash not in self._submitted_solutions
            and msg_hash not in self._solution_set
            and msg_hash not in self.hold_back_solutions
        ):
            self.hold_back_solutions.add(individual)
        return None
