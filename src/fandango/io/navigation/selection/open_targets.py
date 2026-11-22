from collections import Counter
from collections.abc import Mapping
from typing import Optional

from fandango.io.navigation.graph.packetnavigator import PacketNavigator
from fandango.io.navigation.selection.protocol_model import ProtocolModel
from fandango.io.navigation.step import Step
from fandango.language.grammar.k_paths import KPath
from fandango.language.symbols import NonTerminal


class OpenTargets:
    """The state targets of the uncovered k-paths, and those reachable for a navigator: derivable and not marked unreachable."""

    def __init__(self, model: ProtocolModel):
        self._model = model
        self._protocol_msg_symbols = set(
            map(lambda x: x.symbol, self._model.protocol_msg_symbols)
        )
        self._state_target_by_path: dict[KPath, KPath] = {}
        self._uncovered: set[KPath] = set()
        self._uncovered_count_by_target: Counter[KPath] = Counter()
        self._unreachable: set[KPath] = set()
        self._reachable: dict[KPath, None] = {}
        self._reachable_uncovered_by_length: dict[int, dict[KPath, None]] = {}
        self._reachable_blocked_steps: Optional[frozenset[Step]] = None

    def reset(self) -> None:
        """Forget the uncovered k-paths and the targets marked unreachable, as after construction."""
        self._uncovered = set()
        self._uncovered_count_by_target = Counter()
        self._unreachable = set()
        self._reachable_blocked_steps = None

    def set_uncovered(self, uncovered: set[KPath]) -> None:
        """Takes uncovered as the uncovered k-paths. A changed set is expected as a new set object."""
        if uncovered is self._uncovered:
            return
        newly_uncovered = uncovered - self._uncovered
        newly_covered = self._uncovered - uncovered
        for path in newly_uncovered:
            target = self._state_target_of(path)
            if len(target) != 0:
                self._uncovered_count_by_target[target] += 1
        for path in newly_covered:
            self._drop_reachable_uncovered(path)
            target = self._state_target_of(path)
            if len(target) != 0:
                self._uncovered_count_by_target[target] -= 1
                if self._uncovered_count_by_target[target] == 0:
                    del self._uncovered_count_by_target[target]
                    self._drop_reachable(target)
        if newly_uncovered:
            self._reachable_blocked_steps = None
        self._uncovered = uncovered

    def mark_unreachable(self, target: KPath) -> None:
        self._unreachable.add(target)
        self._drop_reachable(target)

    def clear_unreachable(self) -> None:
        self._unreachable.clear()
        self._reachable_blocked_steps = None

    def is_reachable_message(
        self, message: NonTerminal, navigator: PacketNavigator
    ) -> bool:
        return self._is_reachable((message,), navigator)

    def is_derivable_coverage_complete(
        self, uncovered_paths: set[KPath], navigator: PacketNavigator
    ) -> bool:
        return not any(
            self._is_derivable_path(path, navigator) for path in uncovered_paths
        )

    def reachable(self, navigator: PacketNavigator) -> Mapping[KPath, None]:
        self._update_reachable(navigator)
        return self._reachable

    def reachable_uncovered_by_length(
        self, navigator: PacketNavigator
    ) -> Mapping[int, Mapping[KPath, None]]:
        """The reachable targets that are uncovered k-paths themselves, by length."""
        self._update_reachable(navigator)
        return self._reachable_uncovered_by_length

    def _is_derivable_path(self, path: KPath, navigator: PacketNavigator) -> bool:
        """True if the path trimmed to the state grammar, or else a message producing it, is derivable."""
        target = self._state_target_of(path)
        if len(target) > 0:
            return navigator.is_derivable(target)
        return any(
            navigator.is_derivable((message,))
            for message in self._model.messages_producing(path[0])
        )

    def _is_reachable(self, target: KPath, navigator: PacketNavigator) -> bool:
        return target not in self._unreachable and navigator.is_derivable(target)

    def _update_reachable(self, navigator: PacketNavigator) -> None:
        if navigator.blocked_steps == self._reachable_blocked_steps:
            return
        self._reachable = {}
        self._reachable_uncovered_by_length = {}
        for target in self._uncovered_count_by_target:
            if not self._is_reachable(target, navigator):
                continue
            self._reachable[target] = None
            if target in self._uncovered:
                self._reachable_uncovered_by_length.setdefault(len(target), {})[
                    target
                ] = None
        self._reachable_blocked_steps = navigator.blocked_steps

    def _drop_reachable(self, target: KPath) -> None:
        self._reachable.pop(target, None)
        self._drop_reachable_uncovered(target)

    def _drop_reachable_uncovered(self, target: KPath) -> None:
        targets = self._reachable_uncovered_by_length.get(len(target))
        if targets is None or target not in targets:
            return
        del targets[target]
        if not targets:
            del self._reachable_uncovered_by_length[len(target)]

    def _state_target_of(self, path: KPath) -> KPath:
        target = self._state_target_by_path.get(path)
        if target is None:
            path_last_state_cutoff = len(path) + 1
            in_state_area = True
            if len(path) > 0:
                first_symbol = path[0]
                if first_symbol not in self._model.state_grammar_symbols:
                    in_state_area = False
                    path_last_state_cutoff = 0
            if in_state_area:
                for path_idx, symbol in enumerate(path):
                    if symbol in self._protocol_msg_symbols:
                        path_last_state_cutoff = path_idx + 1
                        break
            target = path[:path_last_state_cutoff]
            self._state_target_by_path[path] = target
        return target
