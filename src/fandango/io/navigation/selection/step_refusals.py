from collections import Counter, defaultdict

from fandango.io.navigation.step import Step
from fandango.logger import log_guidance_hint


class StepRefusals:
    """
    Tracks which steps an external party refuses to take and blocks and unblocks them.
    """

    REFUSAL_LIMIT = 3
    FIRST_REFUSAL_SESSIONS = 8
    REPEAT_COST = 3
    REPEAT_STEP = 10

    def __init__(self) -> None:
        self._session = 0
        self._refusals_in_a_row_by_step: Counter[Step] = Counter()
        self._blocked_count_by_step: Counter[Step] = Counter()
        self._blocked_until_session_by_step: dict[Step, int] = {}
        self._taken_in_session: set[Step] = set()
        self._party_by_deferred_step: dict[Step, str] = {}
        self._refusals_in_a_row_in_calling_rule: Counter[Step] = Counter()
        self._takes_in_calling_rule: Counter[Step] = Counter()
        self._contexts_taken_last_in_calling_rule: defaultdict[Step, set[Step]] = (
            defaultdict(set)
        )

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
        in_calling_rule = step.as_in_calling_last_rule()
        self._taken_in_session.add(in_calling_rule)
        self._party_by_deferred_step.pop(in_calling_rule, None)
        self._takes_in_calling_rule[in_calling_rule] += 1
        self._contexts_taken_last_in_calling_rule[in_calling_rule].add(step)
        del self._refusals_in_a_row_in_calling_rule[in_calling_rule]
        if in_calling_rule in self._blocked_until_session_by_step:
            log_guidance_hint(
                f"{party} took {step.parent} -> {step.packet}. Routing through it again wherever {step.parent} is used."
            )
            self._unblock(in_calling_rule)

    def repeat_costs(self) -> dict[Step, int]:
        return {
            step: min(self.REPEAT_COST, takes // self.REPEAT_STEP)
            for step, takes in self._takes_in_calling_rule.items()
            if takes >= self.REPEAT_STEP
        }

    def is_block_deferred(self, step: Step) -> bool:
        """True if the step is refused is not being blacklisted till the session ends."""
        return (
            step in self._party_by_deferred_step
            or step.as_in_calling_last_rule() in self._party_by_deferred_step
        )

    def count_refusal(self, step: Step, party: str) -> None:
        """
        Counts that the party deviated from the step. Blocks the step after REFUSAL_LIMIT calls.
        Defers blocking the rule if it was taken elsewhere in the current session.
        It the step represents a recursive call, only the recursive version of that call is blocked.
        """
        in_calling_rule = step.as_in_calling_last_rule()
        self._refusals_in_a_row_in_calling_rule[in_calling_rule] += 1
        self._refusals_in_a_row_by_step[step] += 1
        taken_last_in = self._contexts_taken_last_in_calling_rule[in_calling_rule]
        taken_last_in.discard(step)
        if in_calling_rule in self._blocked_until_session_by_step:
            return
        refused_in_rule = self._refusals_in_a_row_in_calling_rule[in_calling_rule]
        if refused_in_rule >= self.REFUSAL_LIMIT and not taken_last_in:
            log_guidance_hint(
                f"{party} does not take {step.parent} -> {step.packet}. "
                f"Routing around it wherever {step.parent} is used."
            )
            self._block_now_or_at_session_end(in_calling_rule, party)
        elif (
            self._refusals_in_a_row_by_step[step] >= self.REFUSAL_LIMIT
            and step not in self._blocked_until_session_by_step
        ):
            self._block_now_or_at_session_end(step, party)

    def _block_now_or_at_session_end(self, step: Step, party: str) -> None:
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
                if step == step.as_in_calling_last_rule():
                    self._refusals_in_a_row_in_calling_rule[step] = (
                        self.REFUSAL_LIMIT - 1
                    )
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
        self._refusals_in_a_row_in_calling_rule.clear()
        self._takes_in_calling_rule.clear()
        self._contexts_taken_last_in_calling_rule.clear()

    def _unblock(self, step: Step) -> None:
        del self._blocked_until_session_by_step[step]
