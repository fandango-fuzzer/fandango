import math
from collections import Counter, deque
from collections.abc import Callable, Hashable
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.packetnavigator import (
    Predecessor,
    RuledOutPredecessors,
)
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.violation_profiler.value_features import (
    value_features,
)
from fandango.io.violation import FandangoRemoteViolation
from fandango.language.grammar.grammar import KPath
from fandango.language.tree import DerivationTree
from fandango.logger import log_guidance_hint


class _Feature(NamedTuple):
    # "path" (a k-path), "value" (anchor and abstraction of a value) or "packet"
    kind: str
    # Sender and symbol of the earlier message the feature is of, or None for the message itself
    predecessor: Optional[Predecessor]
    detail: Hashable

    @property
    def source(self) -> tuple[bool, Optional[Predecessor]]:
        """What the feature tells about: an earlier packet type, the message's own content or an earlier message's."""
        return self.kind == "packet", self.predecessor

    @property
    def complexity(self) -> int:
        """0 for a packet type, 1 for the message's own content, 2 for the content of an earlier message."""
        if self.kind == "packet":
            return 0
        return 1 if self.predecessor is None else 2

    def describe(self) -> str:
        what = None
        if self.kind == "path":
            assert isinstance(self.detail, tuple)
            what = "/".join(symbol.format_as_spec() for symbol in self.detail)
        elif self.kind == "value":
            assert isinstance(self.detail, tuple)
            anchor, abstraction = self.detail
            what = f"{'/'.join(anchor)} {abstraction.describe()}"
        if self.predecessor is None:
            assert what is not None
            return what
        sender, symbol = self.predecessor
        after = f"after {symbol} from {sender}"
        return after if what is None else f"{after} with {what}"


class ViolationKind(NamedTuple):
    error_type: str
    expected_nonterminals: tuple[str, ...]
    failed_constraints: tuple[str, ...]

    @classmethod
    def from_remote_violation(
        cls, violation: FandangoRemoteViolation
    ) -> "ViolationKind":
        return ViolationKind(
            violation.error_type.name,
            tuple(
                sorted(nt.format_as_spec() for nt in violation.expected_nonterminals)
            ),
            tuple(sorted(violation.failed_constraints or [])),
        )

    def describe(self) -> str:
        text = f"{self.error_type.lower()} {' | '.join(self.expected_nonterminals)}"
        return (
            f"{text}: {'; '.join(self.failed_constraints)}"
            if self.failed_constraints
            else text
        )


class Suspicion(NamedTuple):
    packet_type: PacketNonTerminal
    violation_kind: ViolationKind


# Position in the session, sender, packet symbol and content hash.
# Tells mounted copies of the same answered message apart from other messages
_AnswerKey = tuple[int, str, str, int]


class _FeatureCounts:
    """How many messages have each feature, and the features of the last keep_last messages."""

    def __init__(self, keep_last: int = 0) -> None:
        self.message_count = 0
        self.by_feature: Counter[_Feature] = Counter()
        self.recent_features: deque[frozenset[_Feature]] = deque(maxlen=keep_last)

    def add_message(self, features: frozenset[_Feature]) -> None:
        self.message_count += 1
        self.by_feature.update(features)
        if self.recent_features.maxlen:
            self.recent_features.append(features)


class _RetrySchedule:
    """When a suspect message of one kind may be sent again, to see whether it still causes the violation."""

    def __init__(self, now: int, first_wait: int) -> None:
        """now is the number of sessions ended so far."""
        self.wait_sessions = first_wait
        self.due_at_session = now + first_wait

    def is_due(self, now: int) -> bool:
        return now >= self.due_at_session

    def postpone(self, now: int, max_wait: int) -> None:
        """Doubles the wait, up to max_wait, and starts it now."""
        self.wait_sessions = min(max_wait, 2 * self.wait_sessions)
        self.due_at_session = now + self.wait_sessions


class ViolationProfile:
    """
    Learns which features of sent messages make the remote party violate the grammar, by comparing the messages sent
    last before a violation with messages it answered.
    """

    MIN_TRIGGERS = 3
    MIN_COUNTEREXAMPLES = 3
    MAX_COUNTEREXAMPLE_SHARE = 0.1
    MIN_SUSPICION_SCORE = 0.9
    # How many of the last triggers are checked for what a suspect feature explains
    RECENT_TRIGGERS = 32
    FIRST_RETRY_WAIT = 8
    MAX_RETRY_WAIT = 256
    MAX_LOGGED_FEATURES = 3

    def __init__(
        self,
        k_paths_of: Callable[[DerivationTree], set[KPath]],
        is_fuzzer_party: Callable[[str], bool],
        literals: frozenset[str],
    ) -> None:
        """literals are the texts of the grammar's terminals that are not regular expressions."""
        self._k_paths_of = k_paths_of
        self._is_fuzzer_party = is_fuzzer_party
        self._literals = literals
        self._sessions_ended = 0
        self._trigger_counts: dict[
            tuple[PacketNonTerminal, ViolationKind], _FeatureCounts
        ] = {}
        self._violation_kinds_by_packet_type: dict[
            PacketNonTerminal, set[ViolationKind]
        ] = {}
        self._counterexample_counts: dict[PacketNonTerminal, _FeatureCounts] = {}
        self._retry_schedules: dict[
            tuple[PacketNonTerminal, ViolationKind], _RetrySchedule
        ] = {}
        self._suspect_cache: dict[
            PacketNonTerminal, dict[ViolationKind, frozenset[_Feature]]
        ] = {}
        self._last_logged_suspects: dict[
            tuple[PacketNonTerminal, ViolationKind], str
        ] = {}
        self._last_counted_answer: Optional[_AnswerKey] = None
        # The features of the messages before a message, per prefix of the session
        self._history_features_by_prefix: dict[
            tuple[int, ...], frozenset[_Feature]
        ] = {}

    def reset(self) -> None:
        self._sessions_ended = 0
        self._trigger_counts.clear()
        self._violation_kinds_by_packet_type.clear()
        self._counterexample_counts.clear()
        self._retry_schedules.clear()
        self._suspect_cache.clear()
        self._last_logged_suspects.clear()
        self._last_counted_answer = None
        self._history_features_by_prefix.clear()

    def signal_session_end(self) -> None:
        self._sessions_ended += 1
        self._last_counted_answer = None
        self._history_features_by_prefix.clear()

    def observe_violation(
        self, session_tree: DerivationTree, violation: Exception
    ) -> None:
        """Records the last message the fuzzer sent in the session as a trigger of the violation."""
        if not isinstance(violation, FandangoRemoteViolation):
            return
        trigger = self._last_fuzzer_message(session_tree)
        if trigger is None:
            return
        packet_type, message = trigger
        violation_kind = ViolationKind.from_remote_violation(violation)
        self._trigger_counts.setdefault(
            (packet_type, violation_kind),
            _FeatureCounts(keep_last=self.RECENT_TRIGGERS),
        ).add_message(self._features_in_session(message))
        self._violation_kinds_by_packet_type.setdefault(packet_type, set()).add(
            violation_kind
        )
        self._suspect_cache.pop(packet_type, None)

    def observe_answer(self, session_tree: DerivationTree) -> None:
        """
        Records the last message the fuzzer sent as a counterexample, as the remote party answered it within the
        grammar. Ignores packet types never triggered a violation before.
        """
        sent = self._last_fuzzer_message(session_tree)
        if sent is None:
            return
        packet_type, message = sent
        if packet_type not in self._violation_kinds_by_packet_type:
            return
        answer_key = self._answer_key_of(message)
        if answer_key == self._last_counted_answer:
            return
        self._last_counted_answer = answer_key
        self._counterexample_counts.setdefault(
            packet_type, _FeatureCounts()
        ).add_message(self._features_in_session(message))
        self._suspect_cache.pop(packet_type, None)

    def suspicion_of(self, message: DerivationTree) -> Optional[Suspicion]:
        """
        The suspicion the message confirms, if any: one about its own packet type, or one about a later packet type
        whose suspect features name the message as predecessor with its content. The message must be mounted in its
        session.
        """
        packet_type = PacketNonTerminal.of_message(message)
        content = self._content_features(message)
        suspects = self._suspect_features(packet_type)
        if suspects:
            features = content | self._history_features(self._messages_before(message))
            for violation_kind, suspect_features in suspects.items():
                if features & suspect_features:
                    return Suspicion(packet_type, violation_kind)
        predecessor = self._predecessor_of(message)
        as_predecessor = frozenset(
            feature._replace(predecessor=predecessor) for feature in content
        )
        for later_type in self._violation_kinds_by_packet_type:
            for violation_kind, suspect_features in self._suspect_features(
                later_type
            ).items():
                if as_predecessor & suspect_features:
                    return Suspicion(later_type, violation_kind)
        return None

    def should_withhold(self, message: DerivationTree) -> bool:
        """
        True if the message confirms a suspicion whose retry is not due. The message must be mounted in its session.
        """
        suspicion = self.suspicion_of(message)
        return suspicion is not None and not self.is_retry_due(*suspicion)

    def is_retry_due(
        self, packet_type: PacketNonTerminal, violation_kind: ViolationKind
    ) -> bool:
        """
        True once the wait for this suspect is over, which starts when the suspicion arises. False for what was never
        suspected. The retry is used up only by consume_retry, when a suspect is actually sent.
        """
        schedule = self._retry_schedules.get((packet_type, violation_kind))
        return schedule is not None and schedule.is_due(self._sessions_ended)

    def consume_retry(
        self, packet_type: PacketNonTerminal, violation_kind: ViolationKind
    ) -> None:
        """Uses up the due retry of a suspect that is sent now; the next wait is twice as long."""
        self._retry_schedules[(packet_type, violation_kind)].postpone(
            self._sessions_ended, self.MAX_RETRY_WAIT
        )
        log_guidance_hint(
            f"Trying {packet_type} again, suspected to cause {violation_kind.describe()}."
        )

    def ruled_out_predecessors(self) -> RuledOutPredecessors:
        """
        Per packet type, the earlier packets, as sender and symbol, after which every message of the type is
        suspected to cause a violation, whatever its content. Leaves out the violations whose retry is due.
        """
        ruled_out = {}
        for packet_type in self._violation_kinds_by_packet_type:
            predecessors: set[Predecessor] = set()
            for violation_kind, features in self._suspect_features(packet_type).items():
                if self.is_retry_due(packet_type, violation_kind):
                    continue
                for feature in features:
                    if feature.kind == "packet":
                        assert feature.predecessor is not None
                        predecessors.add(feature.predecessor)
            if predecessors:
                ruled_out[packet_type] = frozenset(predecessors)
        return ruled_out

    def _features_in_session(self, message: DerivationTree) -> frozenset[_Feature]:
        """The message's content, the packet types before it, and the content of the last messages before it."""
        return self._content_features(message) | self._history_features(
            self._messages_before(message)
        )

    def _content_features(self, message: DerivationTree) -> frozenset[_Feature]:
        """The message's k-paths and the abstractions of its values."""
        paths = frozenset(
            _Feature("path", None, path) for path in self._k_paths_of(message)
        )
        values = frozenset(
            _Feature("value", None, value)
            for value in value_features(message, self._literals)
        )
        return paths | values

    def _history_features(self, history: list[DerivationTree]) -> frozenset[_Feature]:
        """The features of the messages before a message: their packet types and their content."""
        hashes = tuple(hash(message) for message in history)
        features: frozenset[_Feature] = frozenset()
        for index, message in enumerate(history):
            prefix = hashes[: index + 1]
            cached = self._history_features_by_prefix.get(prefix)
            if cached is None:
                predecessor = self._predecessor_of(message)
                cached = (
                    features
                    | {_Feature("packet", predecessor, None)}
                    | {
                        feature._replace(predecessor=predecessor)
                        for feature in self._content_features(message)
                    }
                )
                self._history_features_by_prefix[prefix] = cached
            features = cached
        return features

    @classmethod
    def _answer_key_of(cls, message: DerivationTree) -> _AnswerKey:
        return (
            len(cls._messages_before(message)),
            str(message.sender),
            message.nonterminal.name(),
            hash(message),
        )

    @staticmethod
    def _messages_before(message: DerivationTree) -> list[DerivationTree]:
        session = message.get_root()
        earlier = []
        for record in session.protocol_msgs():
            if record.msg is message:
                break
            earlier.append(record.msg)
        return earlier

    @staticmethod
    def _predecessor_of(message: DerivationTree) -> Predecessor:
        """The message as an earlier packet of a later one: its sender and symbol."""
        assert message.sender is not None
        return message.sender, message.nonterminal.name()

    def _last_fuzzer_message(
        self, session_tree: DerivationTree
    ) -> Optional[tuple[PacketNonTerminal, DerivationTree]]:
        for record in session_tree.protocol_msgs(reverse=True):
            if self._is_fuzzer_party(record.sender):
                return PacketNonTerminal.of_message(record.msg), record.msg
        return None

    def _suspect_features(
        self, packet_type: PacketNonTerminal
    ) -> dict[ViolationKind, frozenset[_Feature]]:
        """The suspect features per violation for one packet type."""
        suspects = self._suspect_cache.get(packet_type)
        if suspects is None:
            suspects = {}
            for violation_kind in self._violation_kinds_by_packet_type.get(
                packet_type, ()
            ):
                ranked = self._ranked_suspect_features(
                    packet_type, self._trigger_counts[(packet_type, violation_kind)]
                )
                if ranked:
                    suspects[violation_kind] = frozenset(
                        feature for feature, _ in ranked
                    )
                    self._log_suspect_features(packet_type, violation_kind, ranked)
                    if (packet_type, violation_kind) not in self._retry_schedules:
                        self._retry_schedules[(packet_type, violation_kind)] = (
                            _RetrySchedule(self._sessions_ended, self.FIRST_RETRY_WAIT)
                        )
            self._suspect_cache[packet_type] = suspects
        return suspects

    def _log_suspect_features(
        self,
        packet_type: PacketNonTerminal,
        violation_kind: ViolationKind,
        ranked: list[tuple[_Feature, float]],
    ) -> None:
        """Logs the strongest suspect features, whenever they change."""
        top = ", ".join(
            feature.describe() for feature, _ in ranked[: self.MAX_LOGGED_FEATURES]
        )
        more = len(ranked) - self.MAX_LOGGED_FEATURES
        text = f"{top} and {more} more" if more > 0 else top
        if self._last_logged_suspects.get((packet_type, violation_kind)) == text:
            return
        self._last_logged_suspects[(packet_type, violation_kind)] = text
        log_guidance_hint(
            f"{packet_type} is suspected to cause {violation_kind.describe()} by {text}. Holding back such messages."
        )

    def _ranked_suspect_features(
        self, packet_type: PacketNonTerminal, triggers: _FeatureCounts
    ) -> list[tuple[_Feature, float]]:
        """
        The suspect features, strongest first. Features of the same source, an earlier packet type, the message's
        content or an earlier message's content, are kept only if they explain one of the last triggers that
        stronger sources do not. Without the content of earlier packets suspect by themselves.
        """
        counterexamples = self._counterexample_counts.get(packet_type)
        if (
            counterexamples is None
            or counterexamples.message_count < self.MIN_COUNTEREXAMPLES
        ):
            return []
        ranked = []
        for feature, triggers_with_feature in triggers.by_feature.items():
            if triggers_with_feature < self.MIN_TRIGGERS:
                continue
            counterexamples_with_feature = counterexamples.by_feature[feature]
            if (
                counterexamples_with_feature
                > self.MAX_COUNTEREXAMPLE_SHARE * counterexamples.message_count
            ):
                continue
            score = triggers_with_feature / math.sqrt(
                triggers.message_count
                * (triggers_with_feature + counterexamples_with_feature)
            )
            if score >= self.MIN_SUSPICION_SCORE:
                ranked.append((feature, score))
        suspect_predecessors = {
            feature.predecessor for feature, _ in ranked if feature.kind == "packet"
        }
        by_source: dict[
            tuple[bool, Optional[Predecessor]], list[tuple[_Feature, float]]
        ] = {}
        for feature, score in ranked:
            if feature.kind != "packet" and feature.predecessor in suspect_predecessors:
                continue
            by_source.setdefault(feature.source, []).append((feature, score))
        sources = sorted(
            by_source.values(),
            key=lambda features: (
                -max(score for _, score in features),
                features[0][0].complexity,
            ),
        )
        explaining = []
        explained: set[int] = set()
        for features in sources:
            covered = {
                index
                for index, trigger in enumerate(triggers.recent_features)
                if any(feature in trigger for feature, _ in features)
            }
            # A source absent from the last triggers is not judged by them
            if not covered or not covered <= explained:
                explaining.extend(features)
                explained |= covered
        explaining.sort(key=lambda ranked_feature: -ranked_feature[1])
        return explaining
