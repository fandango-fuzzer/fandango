import math
from collections import Counter, deque
from collections.abc import Callable, Hashable, Sequence
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.packetnavigator import (
    Predecessor,
    SuspectPredecessors,
)
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.violation_profiler.value_features import (
    value_features,
)
from fandango.io.violation import FandangoRemoteViolation, RemoteViolationType
from fandango.language.grammar.grammar import KPath
from fandango.language.tree import DerivationTree
from fandango.logger import log_guidance_hint


class _Feature(NamedTuple):
    # "path" (a k-path), "value" (an anchored value abstraction) or "packet" (an earlier packet type)
    kind: str
    # Sender and symbol of the earlier message the feature belongs to; None stands for the message itself
    predecessor: Optional[Predecessor]
    detail: Hashable

    @property
    def source(self) -> tuple[bool, Optional[Predecessor]]:
        """Identifies the feature's source: an earlier packet type, the message's content or an earlier message's."""
        return self.kind == "packet", self.predecessor

    @property
    def complexity(self) -> int:
        """Ranks the source: 0 for a packet type, 1 for the message's content, 2 for an earlier message's."""
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


class Symptom(NamedTuple):
    error_type: RemoteViolationType
    expected_nonterminals: tuple[str, ...]
    failed_constraints: tuple[str, ...]

    @classmethod
    def of_violation(cls, violation: FandangoRemoteViolation) -> "Symptom":
        return cls(
            violation.error_type,
            tuple(
                sorted(nt.format_as_spec() for nt in violation.expected_nonterminals)
            ),
            tuple(sorted(violation.failed_constraints or [])),
        )

    def describe(self) -> str:
        text = (
            f"{self.error_type.name.lower()} {' | '.join(self.expected_nonterminals)}"
        )
        return (
            f"{text}: {'; '.join(self.failed_constraints)}"
            if self.failed_constraints
            else text
        )


class Suspicion(NamedTuple):
    packet_type: PacketNonTerminal
    symptom: Symptom


# Position in the session, sender, packet symbol and content hash: recognizes mounted copies of an answered message
_AnswerKey = tuple[int, str, str, int]

# A feature with its suspicion score
_ScoredFeature = tuple[_Feature, float]


class _FeatureCounts:
    """Counts the messages per feature and keeps the features of the last keep_last messages."""

    def __init__(self, keep_last: int = 0) -> None:
        self.message_count = 0
        self.by_feature: Counter[_Feature] = Counter()
        self.recent_features: deque[frozenset[_Feature]] = deque(maxlen=keep_last)

    def add_message(self, features: frozenset[_Feature]) -> None:
        self.message_count += 1
        self.by_feature.update(features)
        self.recent_features.append(features)


class _RetrySchedule:
    """Schedules when a suspect message of one kind may be sent again."""

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


class ViolationProfiler:
    """
    Learns which features of sent messages make the remote party violate the grammar, by comparing the messages sent
    last before a violation with messages it answered.
    """

    MIN_TRIGGERS = 3
    MIN_COUNTEREXAMPLES = 3
    MAX_COUNTEREXAMPLE_SHARE = 0.1
    MIN_SUSPICION_SCORE = 0.9
    # How many of the last triggers the suspect features are judged by
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
        """literals are the texts of the grammar's literal terminals, as literals_of collects them."""
        self._k_paths_of = k_paths_of
        self._is_fuzzer_party = is_fuzzer_party
        self._literals = literals
        self._sessions_ended = 0
        self._trigger_counts: dict[
            tuple[PacketNonTerminal, Symptom], _FeatureCounts
        ] = {}
        self._symptoms_by_packet_type: dict[PacketNonTerminal, set[Symptom]] = {}
        self._counterexample_counts: dict[PacketNonTerminal, _FeatureCounts] = {}
        self._retry_schedules: dict[
            tuple[PacketNonTerminal, Symptom], _RetrySchedule
        ] = {}
        self._suspect_cache: dict[
            PacketNonTerminal, dict[Symptom, frozenset[_Feature]]
        ] = {}
        self._last_logged_suspects: dict[tuple[PacketNonTerminal, Symptom], str] = {}
        self._last_counted_answer: Optional[_AnswerKey] = None
        self._history_features_by_prefix: dict[
            tuple[int, ...], frozenset[_Feature]
        ] = {}

    def reset(self) -> None:
        self._sessions_ended = 0
        self._trigger_counts.clear()
        self._symptoms_by_packet_type.clear()
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
        self, session_tree: DerivationTree, violation: FandangoRemoteViolation
    ) -> None:
        """Records the last message the fuzzer sent in the session as a trigger of the violation."""
        trigger = self._last_fuzzer_message(session_tree)
        if trigger is None:
            return
        packet_type, message = trigger
        symptom = Symptom.of_violation(violation)
        self._trigger_counts.setdefault(
            (packet_type, symptom),
            _FeatureCounts(keep_last=self.RECENT_TRIGGERS),
        ).add_message(self._features_in_session(message))
        self._symptoms_by_packet_type.setdefault(packet_type, set()).add(symptom)
        self._suspect_cache.pop(packet_type, None)

    def observe_answer(self, session_tree: DerivationTree) -> None:
        """Records the fuzzer's last message once as a counterexample if its packet type triggered a violation."""
        sent = self._last_fuzzer_message(session_tree)
        if sent is None:
            return
        packet_type, message = sent
        if packet_type not in self._symptoms_by_packet_type:
            return
        answer_key = self._answer_key_of(message)
        if answer_key == self._last_counted_answer:
            return
        self._last_counted_answer = answer_key
        self._counterexample_counts.setdefault(
            packet_type, _FeatureCounts()
        ).add_message(self._features_in_session(message))
        self._suspect_cache.pop(packet_type, None)

    def observe_sending(self, message: DerivationTree) -> None:
        """Logs the sending of the mounted suspect message and uses up its due retry."""
        suspicion = self.suspicion_of(message)
        if suspicion is None:
            return
        if self._is_retry_due(*suspicion):
            self._consume_retry(*suspicion)
            log_guidance_hint(
                f"Trying {suspicion.packet_type} again, suspected to cause "
                f"{suspicion.symptom.describe()}."
            )
            return
        packet_type = PacketNonTerminal.of_message(message)
        suspect = (
            "" if suspicion.packet_type == packet_type else f" {suspicion.packet_type}"
        )
        log_guidance_hint(
            f"Sending {packet_type}, suspected to cause{suspect} "
            f"{suspicion.symptom.describe()}."
        )

    def suspicion_of(self, message: DerivationTree) -> Optional[Suspicion]:
        """Finds the suspicion the mounted message confirms, about its own packet type or a later one."""
        features = self._content_features(message)
        suspicion = self._suspicion_about_own_type(message, features)
        if suspicion is not None:
            return suspicion
        return self._suspicion_about_later_types(message, features)

    def should_withhold(self, message: DerivationTree) -> bool:
        """Tells whether the mounted message confirms a suspicion whose retry is still pending."""
        suspicion = self.suspicion_of(message)
        return suspicion is not None and not self._is_retry_due(*suspicion)

    def suspect_predecessors(self) -> SuspectPredecessors:
        """Maps each packet type to the earlier packets that make all its messages suspect until the retry is due."""
        suspect_predecessors = {}
        for packet_type in self._symptoms_by_packet_type:
            predecessors: set[Predecessor] = set()
            for symptom, features in self._suspect_features(packet_type).items():
                if self._is_retry_due(packet_type, symptom):
                    continue
                for feature in features:
                    if feature.kind == "packet":
                        assert feature.predecessor is not None
                        predecessors.add(feature.predecessor)
            if predecessors:
                suspect_predecessors[packet_type] = frozenset(predecessors)
        return suspect_predecessors

    def _is_retry_due(self, packet_type: PacketNonTerminal, symptom: Symptom) -> bool:
        """Tells whether the wait for retrying the suspect is over."""
        schedule = self._retry_schedules.get((packet_type, symptom))
        return schedule is not None and schedule.is_due(self._sessions_ended)

    def _consume_retry(self, packet_type: PacketNonTerminal, symptom: Symptom) -> None:
        """Uses up the due retry of a suspect being sent and doubles its next wait."""
        self._retry_schedules[(packet_type, symptom)].postpone(
            self._sessions_ended, self.MAX_RETRY_WAIT
        )

    def _suspicion_about_own_type(
        self, message: DerivationTree, content: frozenset[_Feature]
    ) -> Optional[Suspicion]:
        """Finds the suspicion about the message's packet type that its content or history confirms."""
        packet_type = PacketNonTerminal.of_message(message)
        suspects = self._suspect_features(packet_type)
        if not suspects:
            return None
        features = content | self._history_features(self._messages_before(message))
        for symptom, suspect_features in suspects.items():
            if features & suspect_features:
                return Suspicion(packet_type, symptom)
        return None

    def _suspicion_about_later_types(
        self, message: DerivationTree, content_features: frozenset[_Feature]
    ) -> Optional[Suspicion]:
        """Finds the suspicion about a later packet type that the message's content confirms as predecessor."""
        as_predecessor = self._as_predecessor(
            content_features, self._predecessor_of(message)
        )
        for later_type in self._symptoms_by_packet_type:
            for symptom, suspect_features in self._suspect_features(later_type).items():
                if as_predecessor & suspect_features:
                    return Suspicion(later_type, symptom)
        return None

    def _features_in_session(self, message: DerivationTree) -> frozenset[_Feature]:
        """Collects the features of the message's content and of the messages before it."""
        return self._content_features(message) | self._history_features(
            self._messages_before(message)
        )

    def _content_features(self, message: DerivationTree) -> frozenset[_Feature]:
        """Collects the message's k-paths and value abstractions as features."""
        paths = frozenset(
            _Feature("path", None, path) for path in self._k_paths_of(message)
        )
        values = frozenset(
            _Feature("value", None, value)
            for value in value_features(message, self._literals)
        )
        return paths | values

    def _history_features(self, history: list[DerivationTree]) -> frozenset[_Feature]:
        hashes = tuple(hash(message) for message in history)
        features: frozenset[_Feature] = frozenset()
        for index, message in enumerate(history):
            prefix = hashes[: index + 1]
            cached = self._history_features_by_prefix.get(prefix)
            if cached is None:
                cached = features | self._predecessor_features(message)
                self._history_features_by_prefix[prefix] = cached
            features = cached
        return features

    def _predecessor_features(self, message: DerivationTree) -> frozenset[_Feature]:
        """Collects the packet type and content of a message as features of the messages after it."""
        predecessor = self._predecessor_of(message)
        return self._as_predecessor(self._content_features(message), predecessor) | {
            _Feature("packet", predecessor, None)
        }

    @staticmethod
    def _as_predecessor(
        features: frozenset[_Feature], predecessor: Predecessor
    ) -> frozenset[_Feature]:
        return frozenset(
            feature._replace(predecessor=predecessor) for feature in features
        )

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
        """Identifies the message as predecessor by its sender and symbol."""
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
    ) -> dict[Symptom, frozenset[_Feature]]:
        suspects = self._suspect_cache.get(packet_type)
        if suspects is None:
            suspects = self._compute_suspect_features(packet_type)
            self._suspect_cache[packet_type] = suspects
        return suspects

    def _compute_suspect_features(
        self, packet_type: PacketNonTerminal
    ) -> dict[Symptom, frozenset[_Feature]]:
        """Ranks the suspect features per symptom of a packet type, logs them and schedules new retries."""
        counterexamples = self._counterexample_counts.get(packet_type)
        if (
            counterexamples is None
            or counterexamples.message_count < self.MIN_COUNTEREXAMPLES
        ):
            return {}
        suspects = {}
        for symptom in self._symptoms_by_packet_type[packet_type]:
            ranked = self._ranked_suspect_features(
                self._trigger_counts[(packet_type, symptom)], counterexamples
            )
            if not ranked:
                continue
            suspects[symptom] = frozenset(feature for feature, _ in ranked)
            self._log_suspect_features(packet_type, symptom, ranked)
            self._schedule_retry_if_new(packet_type, symptom)
        return suspects

    def _schedule_retry_if_new(
        self, packet_type: PacketNonTerminal, symptom: Symptom
    ) -> None:
        if (packet_type, symptom) not in self._retry_schedules:
            self._retry_schedules[(packet_type, symptom)] = _RetrySchedule(
                self._sessions_ended, self.FIRST_RETRY_WAIT
            )

    def _log_suspect_features(
        self,
        packet_type: PacketNonTerminal,
        symptom: Symptom,
        ranked: list[_ScoredFeature],
    ) -> None:
        """Logs the strongest suspect features, whenever they change."""
        top = ", ".join(
            feature.describe() for feature, _ in ranked[: self.MAX_LOGGED_FEATURES]
        )
        more = len(ranked) - self.MAX_LOGGED_FEATURES
        text = f"{top} and {more} more" if more > 0 else top
        if self._last_logged_suspects.get((packet_type, symptom)) == text:
            return
        self._last_logged_suspects[(packet_type, symptom)] = text
        log_guidance_hint(
            f"{packet_type} is suspected to cause {symptom.describe()} by {text}. Holding back such messages."
        )

    def _ranked_suspect_features(
        self, triggers: _FeatureCounts, counterexamples: _FeatureCounts
    ) -> list[_ScoredFeature]:
        """Ranks the features of the sources that explain a recent trigger the stronger sources leave unexplained."""
        sources = self._sources_by_strength(
            self._scored_features(triggers, counterexamples)
        )
        ranked = self._explaining_features(sources, triggers.recent_features)
        ranked.sort(key=lambda scored: -scored[1])
        return ranked

    def _scored_features(
        self, triggers: _FeatureCounts, counterexamples: _FeatureCounts
    ) -> list[_ScoredFeature]:
        """Scores the features frequent in the triggers and rare in the counterexamples, keeping the suspect ones."""
        scored = []
        for feature, triggers_with_feature in triggers.by_feature.items():
            if triggers_with_feature < self.MIN_TRIGGERS:
                continue
            counterexamples_with_feature = counterexamples.by_feature[feature]
            if (
                counterexamples_with_feature
                > self.MAX_COUNTEREXAMPLE_SHARE * counterexamples.message_count
            ):
                continue
            score = self._suspicion_score(
                triggers_with_feature,
                triggers.message_count,
                counterexamples_with_feature,
            )
            if score >= self.MIN_SUSPICION_SCORE:
                scored.append((feature, score))
        return scored

    @staticmethod
    def _suspicion_score(
        triggers_with_feature: int,
        trigger_count: int,
        counterexamples_with_feature: int,
    ) -> float:
        """Computes the Ochiai coefficient of a feature and a violation."""
        return triggers_with_feature / math.sqrt(
            trigger_count * (triggers_with_feature + counterexamples_with_feature)
        )

    @staticmethod
    def _sources_by_strength(
        scored: list[_ScoredFeature],
    ) -> list[list[_ScoredFeature]]:
        """Groups the scored features by source, strongest and simplest first, dropping content of suspect packets."""
        suspect_predecessors = {
            feature.predecessor for feature, _ in scored if feature.kind == "packet"
        }
        by_source: dict[tuple[bool, Optional[Predecessor]], list[_ScoredFeature]] = {}
        for feature, score in scored:
            if feature.kind != "packet" and feature.predecessor in suspect_predecessors:
                continue
            by_source.setdefault(feature.source, []).append((feature, score))
        return sorted(
            by_source.values(),
            key=lambda features: (
                -max(score for _, score in features),
                features[0][0].complexity,
            ),
        )

    @staticmethod
    def _explaining_features(
        sources: list[list[_ScoredFeature]],
        recent_triggers: Sequence[frozenset[_Feature]],
    ) -> list[_ScoredFeature]:
        """Selects the sources that explain a recent trigger the stronger sources leave unexplained."""
        explaining = []
        explained: set[int] = set()
        for features in sources:
            covered = {
                index
                for index, trigger in enumerate(recent_triggers)
                if any(feature in trigger for feature, _ in features)
            }
            # A source absent from the recent triggers is kept
            if not covered or not covered <= explained:
                explaining.extend(features)
                explained |= covered
        return explaining
