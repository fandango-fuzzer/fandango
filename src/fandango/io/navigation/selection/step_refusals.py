from collections import Counter

from fandango.io.navigation.graph.prunedstategrammarconverter import Step
from fandango.logger import log_guidance_hint


class StepRefusals:
    """
    Tracks which steps an external party refuses to take.
    """

    REFUSAL_LIMIT = 3
    FIRST_REFUSAL_SESSIONS = 8

    def __init__(self) -> None:
        self._session = 0
        self._refusals_in_a_row_by_step: Counter[Step] = Counter()
        self._blocked_count_by_step: Counter[Step] = Counter()
        self._blocked_until_session_by_step: dict[Step, int] = {}

    @property
    def blocked_steps(self) -> frozenset[Step]:
        return frozenset(self._blocked_until_session_by_step)

    def observe_taken(self, step: Step, party: str) -> None:
        """Records that the party took the step. Refuse counters are reset. Step is unblocked if blocked."""
        del self._refusals_in_a_row_by_step[step]
        del self._blocked_count_by_step[step]
        if step in self._blocked_until_session_by_step:
            log_guidance_hint(
                f"{party} took {step[0]} -> {step[1]}. Routing through it again."
            )
            self._allow(step)

    def count_refusal(self, step: Step, party: str) -> None:
        """Counts that the party deviated from the step. Blocks the step after REFUSAL_LIMIT calls."""
        self._refusals_in_a_row_by_step[step] += 1
        if (
            self._refusals_in_a_row_by_step[step] >= self.REFUSAL_LIMIT
            and step not in self._blocked_until_session_by_step
        ):
            self._blocked_count_by_step[step] += 1
            sessions = self.FIRST_REFUSAL_SESSIONS * 2 ** (
                    self._blocked_count_by_step[step] - 1
            )
            log_guidance_hint(
                f"{party} refused {step[0]} -> {step[1]} {self.REFUSAL_LIMIT} times in a row. "
                f"Routing around it for {sessions} sessions."
            )
            self._blocked_until_session_by_step[step] = self._session + sessions

    def signal_session_end(self) -> None:
        """Notifies the end of a session. Expired blocks are lifted."""
        self._session += 1
        for step, until_session in list(self._blocked_until_session_by_step.items()):
            if until_session <= self._session:
                log_guidance_hint(f"Trying {step[0]} -> {step[1]} again.")
                self._allow(step)
                self._refusals_in_a_row_by_step[step] = self.REFUSAL_LIMIT - 1

    def reset(self) -> None:
        self._session = 0
        self._refusals_in_a_row_by_step.clear()
        self._blocked_count_by_step.clear()
        self._blocked_until_session_by_step.clear()

    def _allow(self, step: Step) -> None:
        del self._blocked_until_session_by_step[step]
