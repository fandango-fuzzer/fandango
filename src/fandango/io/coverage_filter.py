from typing import Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class PacketCoverageFilter:
    def __init__(self, diversity_k: int, grammar: Grammar):
        self._diversity_k = diversity_k
        self._grammar = grammar
        self._submitted_solutions: set[int] = set()
        self.hold_back_solutions: set[DerivationTree] = set()
        self._solution_set: set[int] = set()
        self._past_msgs: set[DerivationTree] = set()
        self._current_msgs: set[DerivationTree] = set()

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished run's messages into the past-message set."""
        for record in tree.protocol_msgs():
            self._past_msgs.add(record.msg)
            self._submitted_solutions.add(
                hash((record.sender, record.recipient, record.msg))
            )

    def set_current_tree(self, current_tree: DerivationTree) -> None:
        """Register the in-progress tree's messages for the next generation."""
        self.hold_back_solutions.clear()
        self._solution_set.clear()
        self._current_msgs = set()
        for record in current_tree.protocol_msgs():
            self._current_msgs.add(record.msg)
            self._submitted_solutions.add(
                hash((record.sender, record.recipient, record.msg))
            )

    def reset(self) -> None:
        self._submitted_solutions.clear()
        self.hold_back_solutions.clear()
        self._solution_set.clear()
        self._past_msgs.clear()
        self._current_msgs.clear()

    def get_past_msgs(
        self, packet_type: Optional[PacketNonTerminal] = None
    ) -> set[DerivationTree]:
        msg_trees = self._past_msgs | self._current_msgs
        if packet_type is None:
            return msg_trees
        return {
            msg
            for msg in msg_trees
            if isinstance(msg.symbol, NonTerminal)
            and PacketNonTerminal(msg.sender, msg.recipient, msg.symbol) == packet_type
        }

    def _is_path_start_with(self, state_path: KPath, path: KPath) -> int:
        n = len(state_path)
        m = len(path)
        max_overlap = min(n, m)
        for overlap in range(max_overlap, 0, -1):
            if state_path[-overlap:] == path[:overlap]:
                return overlap
        return 0

    def filter(self, individual: DerivationTree) -> Optional[DerivationTree]:
        protocol_records = individual.protocol_msgs()
        if len(protocol_records) != 0:
            record = max(
                protocol_records,
                key=lambda r: (
                    r.msg.arrival_index if r.msg.arrival_index is not None else -1
                ),
            )
            msg = record.msg
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
        uncovered_paths = self._grammar.get_uncovered_k_paths(
            list(self.get_past_msgs(msg_key)),
            self._diversity_k,
            symbol,
            overlap_to_root=True,
        )

        overlap_to_root = any(
            0 < self._is_path_start_with(state_path, path) < self._diversity_k
            for path in uncovered_paths
        )

        old_coverage = self._grammar.compute_kpath_coverage(
            list(self.get_past_msgs(msg_key)),
            self._diversity_k,
            symbol,
            overlap_to_root=overlap_to_root,
        )
        new_coverage = self._grammar.compute_kpath_coverage(
            list(self.get_past_msgs(msg_key)) + [msg],
            self._diversity_k,
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
