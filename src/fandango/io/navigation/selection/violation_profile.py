import math
from collections import Counter
from collections.abc import Callable, Hashable
from typing import NamedTuple, Optional

from fandango.io.navigation.graph.packetnavigator import (
    Predecessor,
    RuledOutPredecessors,
)
from fandango.io.navigation.PacketNonTerminal import PacketNonTerminal
from fandango.io.navigation.selection.value_features import (
    describe_level,
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


ViolationKind = tuple[str, tuple[str, ...], tuple[str, ...]]
# Position in the session, sender, packet symbol and content hash: a message's identity across mounted copies
_MessageIdentity = tuple[int, str, str, int]


class _FeatureCounts:
    def __init__(self) -> None:
        self.messages = 0
        self.by_feature: Counter[_Feature] = Counter()

    def add(self, features: frozenset[_Feature]) -> None:
        self.messages += 1
        self.by_feature.update(features)


class _Retry:
    """When a suspect message of one kind may be sent again, to see whether it still causes the violation."""

    def __init__(self, first_wait: int) -> None:
        self.wait_sessions = first_wait
        self.due_at_session = 0


class ViolationProfile:
    """
    Learns which features of sent messages make the remote party violate the grammar, by comparing the messages sent
    last before a violation with messages it answered.
    """

    MIN_TRIGGERS = 3
    MIN_COUNTEREXAMPLES = 3
    MAX_COUNTEREXAMPLE_SHARE = 0.1
    MIN_SUSPICION_SCORE = 0.9
    EARLIER_MESSAGES_WITH_CONTENT = 10
    FIRST_RETRY_WAIT = 8
    MAX_RETRY_WAIT = 256
    LOGGED_FEATURES = 3

    def __init__(
        self,
        k_paths_of: Callable[[DerivationTree], set[KPath]],
        is_fuzzer_party: Callable[[str], bool],
    ) -> None:
        self._k_paths_of = k_paths_of
        self._is_fuzzer_party = is_fuzzer_party
        self._sessions_ended = 0
        self._trigger_counts: dict[
            tuple[PacketNonTerminal, ViolationKind], _FeatureCounts
        ] = {}
        self._violations_by_packet_type: dict[
            PacketNonTerminal, set[ViolationKind]
        ] = {}
        self._counterexample_counts: dict[PacketNonTerminal, _FeatureCounts] = {}
        self._retries: dict[tuple[PacketNonTerminal, ViolationKind], _Retry] = {}
        self._suspect_cache: dict[
            PacketNonTerminal, dict[ViolationKind, frozenset[_Feature]]
        ] = {}
        self._last_announcement: dict[tuple[PacketNonTerminal, ViolationKind], str] = {}
        self._last_counted_answer: Optional[_MessageIdentity] = None
        self._content_cache: dict[_MessageIdentity, frozenset[_Feature]] = {}

    def reset(self) -> None:
        self._sessions_ended = 0
        self._trigger_counts.clear()
        self._violations_by_packet_type.clear()
        self._counterexample_counts.clear()
        self._retries.clear()
        self._suspect_cache.clear()
        self._last_announcement.clear()
        self._last_counted_answer = None
        self._content_cache.clear()

    def signal_session_end(self) -> None:
        self._sessions_ended += 1
        self._last_counted_answer = None
        self._content_cache.clear()

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
        kind = self._violation_kind(violation)
        self._trigger_counts.setdefault((packet_type, kind), _FeatureCounts()).add(
            self._features_of(message)
        )
        self._violations_by_packet_type.setdefault(packet_type, set()).add(kind)
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
        if packet_type not in self._violations_by_packet_type:
            return
        identity = self._message_identity(message, self._messages_before(message))
        if identity == self._last_counted_answer:
            return
        self._last_counted_answer = identity
        self._counterexample_counts.setdefault(packet_type, _FeatureCounts()).add(
            self._features_of(message)
        )
        self._suspect_cache.pop(packet_type, None)

    def suspected_violation(
        self, message: DerivationTree, packet_type: PacketNonTerminal
    ) -> Optional[ViolationKind]:
        """The violation the message is suspected to cause, if any. The message must be mounted in its session."""
        suspects = self._suspects(packet_type)
        if not suspects:
            return None
        features = self._features_of(message)
        for violation, suspect_features in suspects.items():
            if features & suspect_features:
                return violation
        return None

    def retry_due(
        self, packet_type: PacketNonTerminal, violation: ViolationKind
    ) -> bool:
        """
        True once the wait for this suspect is over. The first call starts the wait; the retry is used up only by
        consume_retry, when a suspect is actually sent.
        """
        retry = self._retries.setdefault(
            (packet_type, violation), _Retry(self.FIRST_RETRY_WAIT)
        )
        if retry.due_at_session == 0:
            retry.due_at_session = self._sessions_ended + retry.wait_sessions
            return False
        return self._sessions_ended >= retry.due_at_session

    def consume_retry(
        self, packet_type: PacketNonTerminal, violation: ViolationKind
    ) -> None:
        """Uses up the due retry of a suspect that is sent now; the next wait is twice as long."""
        retry = self._retries[(packet_type, violation)]
        retry.wait_sessions = min(self.MAX_RETRY_WAIT, 2 * retry.wait_sessions)
        retry.due_at_session = self._sessions_ended + retry.wait_sessions
        log_guidance_hint(
            f"Trying {packet_type} again, suspected to cause {self.describe_violation(violation)}."
        )

    def ruled_out_predecessors(self) -> RuledOutPredecessors:
        """
        Per packet type, the earlier packets, as sender and symbol, after which every message of the type is
        suspected to cause a violation, whatever its content. Leaves out the violations whose retry is due.
        """
        ruled_out = {}
        for packet_type in self._violations_by_packet_type:
            predecessors: set[Predecessor] = set()
            for violation, features in self._suspects(packet_type).items():
                if self.retry_due(packet_type, violation):
                    continue
                for feature in features:
                    if feature.kind == "packet":
                        assert feature.predecessor is not None
                        predecessors.add(feature.predecessor)
            if predecessors:
                ruled_out[packet_type] = frozenset(predecessors)
        return ruled_out

    def _features_of(self, message: DerivationTree) -> frozenset[_Feature]:
        """The message's content, the packet types before it, and the content of the last messages before it."""
        return self._content_of(message) | self._earlier_features(
            self._messages_before(message)
        )

    def _content_of(self, message: DerivationTree) -> frozenset[_Feature]:
        """The message's k-paths and the abstractions of its values."""
        paths = frozenset(
            _Feature("path", None, path) for path in self._k_paths_of(message)
        )
        values = frozenset(
            _Feature("value", None, value) for value in value_features(message)
        )
        return paths | values

    def _earlier_features(
        self, earlier: list[tuple[str, DerivationTree]]
    ) -> frozenset[_Feature]:
        """The features of the messages before a message."""
        features: set[_Feature] = set()
        for index, (sender, earlier_message) in enumerate(earlier):
            predecessor = (sender, earlier_message.nonterminal.name())
            features.add(_Feature("packet", predecessor, None))
            if index >= len(earlier) - self.EARLIER_MESSAGES_WITH_CONTENT:
                features.update(
                    feature._replace(predecessor=predecessor)
                    for feature in self._cached_content(
                        earlier_message, earlier[:index]
                    )
                )
        return frozenset(features)

    @staticmethod
    def _violation_kind(violation: FandangoRemoteViolation) -> ViolationKind:
        return (
            violation.error_type.name,
            tuple(
                sorted(nt.format_as_spec() for nt in violation.expected_nonterminals)
            ),
            tuple(sorted(violation.failed_constraints or [])),
        )

    @staticmethod
    def describe_violation(violation: ViolationKind) -> str:
        error_type, expected, constraints = violation
        text = f"{error_type.lower()} {' | '.join(expected)}"
        return f"{text}: {'; '.join(constraints)}" if constraints else text

    @staticmethod
    def _describe_feature(feature: _Feature) -> str:
        what = None
        if feature.kind == "path":
            assert isinstance(feature.detail, tuple)
            what = ViolationProfile._describe_path(feature.detail)
        elif feature.kind == "value":
            assert isinstance(feature.detail, tuple)
            anchor, level = feature.detail
            what = f"{'/'.join(anchor)} {describe_level(level)}"
        if feature.predecessor is None:
            assert what is not None
            return what
        sender, symbol = feature.predecessor
        after = f"after {symbol} from {sender}"
        return after if what is None else f"{after} with {what}"

    @staticmethod
    def _describe_path(path: KPath) -> str:
        return "/".join(symbol.format_as_spec() for symbol in path)

    def _cached_content(
        self,
        message: DerivationTree,
        earlier: list[tuple[str, DerivationTree]],
    ) -> frozenset[_Feature]:
        identity = self._message_identity(message, earlier)
        content = self._content_cache.get(identity)
        if content is None:
            content = self._content_of(message)
            self._content_cache[identity] = content
        return content

    @staticmethod
    def _message_identity(
        message: DerivationTree, earlier: list[tuple[str, DerivationTree]]
    ) -> _MessageIdentity:
        return (
            len(earlier),
            str(message.sender),
            message.nonterminal.name(),
            hash(message),
        )

    @staticmethod
    def _messages_before(message: DerivationTree) -> list[tuple[str, DerivationTree]]:
        session = message.get_root()
        earlier = []
        for record in session.protocol_msgs():
            if record.msg is message:
                break
            earlier.append((record.sender, record.msg))
        return earlier

    def _last_fuzzer_message(
        self, session_tree: DerivationTree
    ) -> Optional[tuple[PacketNonTerminal, DerivationTree]]:
        for record in session_tree.protocol_msgs(reverse=True):
            if self._is_fuzzer_party(record.sender):
                return (
                    PacketNonTerminal(
                        record.sender, record.recipient, record.msg.nonterminal
                    ),
                    record.msg,
                )
        return None

    def _suspects(
        self, packet_type: PacketNonTerminal
    ) -> dict[ViolationKind, frozenset[_Feature]]:
        """The suspect features per violation for one packet type."""
        suspects = self._suspect_cache.get(packet_type)
        if suspects is None:
            suspects = {}
            for violation in self._violations_by_packet_type.get(packet_type, ()):
                ranked = self._ranked_suspect_features(
                    packet_type, self._trigger_counts[(packet_type, violation)]
                )
                if ranked:
                    suspects[violation] = frozenset(feature for feature, _ in ranked)
                    self._log_suspicion(packet_type, violation, ranked)
            self._suspect_cache[packet_type] = suspects
        return suspects

    def _log_suspicion(
        self,
        packet_type: PacketNonTerminal,
        violation: ViolationKind,
        ranked: list[tuple[_Feature, float]],
    ) -> None:
        """Logs the strongest suspect features, whenever they change."""
        top = ", ".join(
            self._describe_feature(feature)
            for feature, _ in ranked[: self.LOGGED_FEATURES]
        )
        more = len(ranked) - self.LOGGED_FEATURES
        text = f"{top} and {more} more" if more > 0 else top
        if self._last_announcement.get((packet_type, violation)) == text:
            return
        self._last_announcement[(packet_type, violation)] = text
        log_guidance_hint(
            f"{packet_type} is suspected to cause {self.describe_violation(violation)} by {text}. Holding back such messages."
        )

    def _ranked_suspect_features(
        self, packet_type: PacketNonTerminal, triggers: _FeatureCounts
    ) -> list[tuple[_Feature, float]]:
        """The suspect features, strongest first."""
        counterexamples = self._counterexample_counts.get(packet_type)
        if (
            counterexamples is None
            or counterexamples.messages < self.MIN_COUNTEREXAMPLES
        ):
            return []
        ranked = []
        for feature, triggers_with_feature in triggers.by_feature.items():
            if triggers_with_feature < self.MIN_TRIGGERS:
                continue
            counterexamples_with_feature = counterexamples.by_feature[feature]
            if (
                counterexamples_with_feature
                > self.MAX_COUNTEREXAMPLE_SHARE * counterexamples.messages
            ):
                continue
            score = triggers_with_feature / math.sqrt(
                triggers.messages
                * (triggers_with_feature + counterexamples_with_feature)
            )
            if score >= self.MIN_SUSPICION_SCORE:
                ranked.append((feature, score))
        ranked.sort(key=lambda ranked_feature: -ranked_feature[1])
        return ranked
