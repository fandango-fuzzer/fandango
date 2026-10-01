from collections import Counter

from fandango.io.navigation.step import Step
from fandango.logger import log_guidance_hint


class StepRefusals:
    """
    Tracks which steps an external party refuses to take and blocks and unblocks them.
    """

    REFUSAL_LIMIT = 3
    FIRST_REFUSAL_SESSIONS = 8

    def __init__(self) -> None:
        self._session = 0
        self._refusals_in_a_row_by_step: Counter[Step] = Counter()
        self._blocked_count_by_step: Counter[Step] = Counter()
        self._blocked_until_session_by_step: dict[Step, int] = {}
        self._taken_in_session: set[Step] = set()
        self._party_by_deferred_step: dict[Step, str] = {}

    @property
    def blocked_steps(self) -> frozenset[Step]:
        return frozenset(self._blocked_until_session_by_step)

    def observe_taken(self, step: Step, party: str) -> None:
        """Records that the party took the step. Refuse counters are reset. Step is unblocked if blocked."""
        self._taken_in_session.add(step)
        self._party_by_deferred_step.pop(step, None)
        del self._refusals_in_a_row_by_step[step]
        del self._blocked_count_by_step[step]
        if step in self._blocked_until_session_by_step:
            log_guidance_hint(
                f"{party} took {step.parent} -> {step.packet}. Routing through it again."
            )
            self._unblock(step)

    def count_refusal(self, step: Step, party: str) -> None:
        """
        Counts that the party deviated from the step. Blocks the step after REFUSAL_LIMIT calls.
        A step taken in this session is blocked at its end, so the session stays derivable.
        """
        self._refusals_in_a_row_by_step[step] += 1
        if (
            self._refusals_in_a_row_by_step[step] >= self.REFUSAL_LIMIT
            and step not in self._blocked_until_session_by_step
        ):
            if step in self._taken_in_session:
                self._party_by_deferred_step[step] = party
            else:
                self._block(step, party)

    def _block(self, step: Step, party: str) -> None:
        self._blocked_count_by_step[step] += 1
        sessions = self.FIRST_REFUSAL_SESSIONS * 2 ** (
            self._blocked_count_by_step[step] - 1
        )
        log_guidance_hint(
            f"{party} refused {step.parent} -> {step.packet} {self.REFUSAL_LIMIT} times in a row. "
            f"Routing around it for {sessions} sessions."
        )
        self._blocked_until_session_by_step[step] = self._session + sessions

    def signal_session_end(self) -> None:
        """Notifies the end of a session. Expired blocks are lifted, deferred blocks are applied."""
        self._session += 1
        for step, until_session in list(self._blocked_until_session_by_step.items()):
            if until_session <= self._session:
                log_guidance_hint(f"Trying {step.parent} -> {step.packet} again.")
                self._unblock(step)
                self._refusals_in_a_row_by_step[step] = self.REFUSAL_LIMIT - 1
        for step, party in self._party_by_deferred_step.items():
            self._block(step, party)
        self._party_by_deferred_step.clear()
        self._taken_in_session.clear()

    def reset(self) -> None:
        self._session = 0
        self._refusals_in_a_row_by_step.clear()
        self._blocked_count_by_step.clear()
        self._blocked_until_session_by_step.clear()
        self._taken_in_session.clear()
        self._party_by_deferred_step.clear()

    def _unblock(self, step: Step) -> None:
        del self._blocked_until_session_by_step[step]
