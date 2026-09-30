from collections import Counter

from fandango.io.navigation.graph.prunedstategrammarconverter import Step
from fandango.logger import log_guidance_hint


class StepRefusals:
    """
    Tracks which steps an external party refuses to take.
    """

    REFUSAL_LIMIT = 3

    def __init__(self) -> None:
        self._refusals_in_a_row_by_step: Counter[Step] = Counter()
        self._refused_steps: frozenset[Step] = frozenset()

    @property
    def refused_steps(self) -> frozenset[Step]:
        return self._refused_steps

    def observe_taken(self, step: Step, party: str) -> None:
        """Records that the party took the step: its refusals start over, and it is allowed again if it was refused."""
        del self._refusals_in_a_row_by_step[step]
        if step in self._refused_steps:
            log_guidance_hint(
                f"{party} took {step[0]} -> {step[1]}. Routing through it again."
            )
            self._refused_steps = self._refused_steps - {step}

    def count_refusal(self, step: Step, party: str) -> None:
        """Counts that the party deviated from the step; refuses the step after REFUSAL_LIMIT deviations in a row."""
        self._refusals_in_a_row_by_step[step] += 1
        if (
            self._refusals_in_a_row_by_step[step] >= self.REFUSAL_LIMIT
            and step not in self._refused_steps
        ):
            log_guidance_hint(
                f"{party} refused {step[0]} -> {step[1]} {self.REFUSAL_LIMIT} times in a row. Routing around it."
            )
            self._refused_steps = self._refused_steps | {step}

    def reset(self) -> None:
        self._refusals_in_a_row_by_step.clear()
        self._refused_steps = frozenset()
