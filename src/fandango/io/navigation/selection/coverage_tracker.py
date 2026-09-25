import dataclasses
from collections.abc import Callable, Hashable
from typing import Generic, Optional, TypeVar

from fandango.io.navigation.coverage.coverage_goal import CoverageGoal
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.language.grammar.grammar import Grammar, KPath
from fandango.language.symbols import NonTerminal
from fandango.language.tree import DerivationTree

Group = TypeVar("Group", bound=Hashable)


@dataclasses.dataclass(frozen=True)
class KPathCounts:
    covered_count: int
    available_count: int


class GroupedKPathCoverage(Generic[Group]):
    def __init__(
        self,
        subtrees_by_group: Callable[
            [DerivationTree], dict[Group, list[DerivationTree]]
        ],
        extract_k_paths: Callable[[list[DerivationTree]], set[KPath]],
        history: Callable[[], DerivationTree],
    ):
        self._subtrees_by_group = subtrees_by_group
        self._extract_k_paths = extract_k_paths
        self._history = history
        self._covered_by_finished_runs: dict[Group, set[KPath]] = {}
        self._covered_by_history: Optional[dict[Group, set[KPath]]] = None

    def add_completed_tree(self, tree: DerivationTree) -> None:
        for group, subtrees in self._subtrees_by_group(tree).items():
            self._covered_by_finished_runs.setdefault(group, set()).update(
                self._extract_k_paths(subtrees)
            )

    def invalidate(self) -> None:
        self._covered_by_history = None

    def reset(self) -> None:
        self._covered_by_finished_runs.clear()
        self._covered_by_history = None

    def is_seen(self, group: Group) -> bool:
        return (
            group in self._covered_by_finished_runs or group in self._history_coverage()
        )

    def covered(self, group: Group) -> set[KPath]:
        return self._covered_by_finished_runs.get(
            group, set()
        ) | self._history_coverage().get(group, set())

    def _history_coverage(self) -> dict[Group, set[KPath]]:
        if self._covered_by_history is None:
            self._covered_by_history = {
                group: self._extract_k_paths(subtrees)
                for group, subtrees in self._subtrees_by_group(self._history()).items()
            }
        return self._covered_by_history


class CoverageTracker:
    """
    Measures reached k-path coverage of the current and past protocol runs.
    """

    def __init__(
        self,
        grammar: Grammar,
        diversity_k: int,
        model: ProtocolModel,
        start_symbol: NonTerminal,
        input_parties: Callable[[], set[str]],
        history: Callable[[], DerivationTree],
        coverage_goal: CoverageGoal,
    ):
        self._grammar = grammar
        self._diversity_k = diversity_k
        self._model = model
        self._start_symbol = start_symbol
        self._input_parties = input_parties
        self._history = history
        self._coverage_goal = coverage_goal
        self._goal_coverage: GroupedKPathCoverage[NonTerminal] = GroupedKPathCoverage(
            lambda tree: {self._start_symbol: [tree]},
            lambda trees: self._covered(
                trees,
                coverage_goal=self._coverage_goal,
                input_parties=self._input_parties(),
            ),
            history,
        )
        self._message_coverage: GroupedKPathCoverage[NonTerminal] = (
            GroupedKPathCoverage(
                self._messages_by_symbol,
                self._covered,
                history,
            )
        )
        self._packet_coverage: GroupedKPathCoverage[PacketNonTerminal] = (
            GroupedKPathCoverage(self._messages_by_packet_type, self._covered, history)
        )
        self._packet_coverage_with_context: GroupedKPathCoverage[PacketNonTerminal] = (
            GroupedKPathCoverage(
                self._messages_by_packet_type,
                lambda trees: self._covered(trees, overlap_to_root=True),
                history,
            )
        )
        self._coverage_scores: Optional[list[tuple[NonTerminal, float]]] = None

    @property
    def diversity_k(self) -> int:
        return self._diversity_k

    def add_completed_tree(self, tree: DerivationTree) -> None:
        """Fold a finished run into the coverage basis."""
        for grouped_coverage in self._grouped_coverages():
            grouped_coverage.add_completed_tree(tree)
        self._coverage_scores = None

    def reset(self) -> None:
        for grouped_coverage in self._grouped_coverages():
            grouped_coverage.reset()
        self._coverage_scores = None

    def invalidate(self) -> None:
        for grouped_coverage in self._grouped_coverages():
            grouped_coverage.invalidate()
        self._coverage_scores = None

    def set_coverage_goal(self, goal: CoverageGoal) -> None:
        # coverage_goal feeds whole-tree extraction, so the folded basis is invalid.
        self._coverage_goal = goal
        self._goal_coverage.reset()
        self._coverage_scores = None

    def uncovered_paths(self) -> list[KPath]:
        all_paths = self.all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        return list(
            all_paths.difference(self._goal_coverage.covered(self._start_symbol))
        )

    def coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        if self._coverage_scores is None:
            self._coverage_scores = self._compute_coverage_scores()
        return self._coverage_scores

    def k_path_counts(self) -> KPathCounts:
        available_paths = self.all_k_paths(
            self._start_symbol,
            coverage_goal=self._coverage_goal,
            input_parties=self._input_parties(),
        )
        covered_paths = available_paths & self._goal_coverage.covered(
            self._start_symbol
        )
        return KPathCounts(len(covered_paths), len(available_paths))

    def coverage_percent(self) -> float:
        counts = self.k_path_counts()
        if counts.available_count == 0:
            return 1.0
        return counts.covered_count / counts.available_count

    def covered_packet_k_paths(
        self, packet_type: PacketNonTerminal, overlap_to_root: bool
    ) -> set[KPath]:
        if overlap_to_root:
            return self._packet_coverage_with_context.covered(packet_type)
        return self._packet_coverage.covered(packet_type)

    def k_paths_of(self, message: DerivationTree, overlap_to_root: bool) -> set[KPath]:
        return self._covered([message], overlap_to_root=overlap_to_root)

    def _grouped_coverages(
        self,
    ) -> tuple[
        GroupedKPathCoverage[NonTerminal] | GroupedKPathCoverage[PacketNonTerminal], ...
    ]:
        return (
            self._goal_coverage,
            self._message_coverage,
            self._packet_coverage,
            self._packet_coverage_with_context,
        )

    @staticmethod
    def _messages_by_symbol(
        tree: DerivationTree,
    ) -> dict[NonTerminal, list[DerivationTree]]:
        messages: dict[NonTerminal, list[DerivationTree]] = {}
        for record in tree.protocol_msgs():
            assert isinstance(record.msg.symbol, NonTerminal)
            messages.setdefault(record.msg.symbol, []).append(record.msg)
        return messages

    @staticmethod
    def _messages_by_packet_type(
        tree: DerivationTree,
    ) -> dict[PacketNonTerminal, list[DerivationTree]]:
        messages: dict[PacketNonTerminal, list[DerivationTree]] = {}
        for record in tree.protocol_msgs():
            assert isinstance(record.msg.symbol, NonTerminal)
            packet_type = PacketNonTerminal(
                record.sender, record.recipient, record.msg.symbol
            )
            messages.setdefault(packet_type, []).append(record.msg)
        return messages

    def _covered(
        self,
        trees: list[DerivationTree],
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        """k-paths covered by the trees (union of the per-tree extraction)."""
        result: set[KPath] = set()
        for tree in trees:
            result |= self._grammar._extract_k_paths_from_tree(
                tree,
                self._diversity_k,
                overlap_to_root,
                coverage_goal,
                input_parties=input_parties,
            )
        return result

    def all_k_paths(
        self,
        non_terminal: NonTerminal,
        *,
        overlap_to_root: bool = False,
        coverage_goal: CoverageGoal = CoverageGoal.STATE_INPUTS_OUTPUTS,
        input_parties: Optional[set[str]] = None,
    ) -> set[KPath]:
        return self._grammar.generate_all_k_paths(
            k=self._diversity_k,
            non_terminal=non_terminal,
            overlap_to_root=overlap_to_root,
            coverage_goal=coverage_goal,
            input_parties=input_parties,
        )

    def _compute_coverage_scores(self) -> list[tuple[NonTerminal, float]]:
        """Per-NonTerminal coverage score: covered / total k-paths."""
        nt_coverage: dict[NonTerminal, float] = {}
        for symbol in {message.symbol for message in self._model.protocol_msg_symbols}:
            if not self._message_coverage.is_seen(symbol):
                nt_coverage[symbol] = 0.0
                continue
            covered = self._message_coverage.covered(symbol)
            all_paths = self.all_k_paths(symbol)
            if len(all_paths) == 0:
                nt_coverage[symbol] = 1.0
            else:
                nt_coverage[symbol] = len(covered) / len(all_paths)
        return list(sorted(nt_coverage.items(), key=lambda x: (x[1], x[0].name())))
