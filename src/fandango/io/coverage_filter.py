from typing import Optional

from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.coverage_tracker import CoverageTracker
from fandango.language.grammar.grammar import KPath
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class PacketCoverageFilter:
    def __init__(self, coverage_tracker: CoverageTracker):
        self._coverage_tracker = coverage_tracker
        self._submitted_solutions: set[int] = set()
        self.hold_back_solutions: set[DerivationTree] = set()
        self._solution_set: set[int] = set()

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished run's messages into the past-message set."""
        for record in tree.protocol_msgs():
            self._submitted_solutions.add(
                hash((record.sender, record.recipient, record.msg))
            )

    def set_current_tree(self, current_tree: DerivationTree) -> None:
        """Register the in-progress tree's messages for the next generation."""
        self.hold_back_solutions.clear()
        self._solution_set.clear()
        for record in current_tree.protocol_msgs():
            self._submitted_solutions.add(
                hash((record.sender, record.recipient, record.msg))
            )

    def reset(self) -> None:
        self._submitted_solutions.clear()
        self.hold_back_solutions.clear()
        self._solution_set.clear()

    @staticmethod
    def _is_path_start_with(state_path: KPath, path: KPath) -> int:
        n = len(state_path)
        m = len(path)
        max_overlap = min(n, m)
        for overlap in range(max_overlap, 0, -1):
            if state_path[-overlap:] == path[:overlap]:
                return overlap
        return 0

    def filter(self, individual: DerivationTree) -> Optional[DerivationTree]:
        last_record = next(individual.protocol_msgs(reverse=True), None)
        if last_record is None:
            return individual
        msg = last_record.msg
        symbol = msg.symbol
        assert isinstance(symbol, NonTerminal)
        packet_type = PacketNonTerminal(msg.sender, msg.recipient, symbol)
        msg_hash = hash(msg)

        state_path_tree = msg.get_path()
        if len(state_path_tree) > self._coverage_tracker.diversity_k:
            state_path_tree = state_path_tree[-self._coverage_tracker.diversity_k :]
        state_path = tuple(map(lambda x: x.symbol, state_path_tree))
        tracker = self._coverage_tracker
        uncovered_paths = tracker.all_k_paths(
            symbol, overlap_to_root=True
        ) - tracker.covered_packet_k_paths(packet_type, overlap_to_root=True)

        overlap_to_root = any(
            0
            < self._is_path_start_with(state_path, path)
            < self._coverage_tracker.diversity_k
            for path in uncovered_paths
        )

        all_paths = tracker.all_k_paths(symbol, overlap_to_root=overlap_to_root)
        covered_paths = tracker.covered_packet_k_paths(packet_type, overlap_to_root)
        old_coverage = covered_share(covered_paths, all_paths)
        new_coverage = covered_share(
            covered_paths | tracker.k_paths_of(msg, overlap_to_root), all_paths
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


def covered_share(covered_paths: set[KPath], all_paths: set[KPath]) -> float:
    if not all_paths:
        return 1.0
    return len(covered_paths) / len(all_paths)
