"""Execution-feedback helpers for the FDP tutorial.

These wrap the FDP reference target so a Fandango spec can turn *execution
feedback* into an ordinary ``where`` constraint:

    where cover_count(str(<start>)) >= 8         # reward inputs that drive deep
    where reaches(str(<start>), "apply:login")   # demand a specific branch runs
    where response(str(<start>)) == "ERR_NOAUTH" # constrain on the server's reply

Feedback is *behavioural*: the message is run through the whole
``frame -> parse -> validate -> apply`` pipeline on a fresh session and we read
back what the target did, from the cheap branch trace it records about itself.
No ``sys.settrace`` is involved, so this stays fast inside Fandango's search
loop (line tracing there is orders of magnitude too slow).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fdp  # noqa: E402


def _run(message: str) -> fdp.Response:
    return fdp.process(message.encode("ascii", "replace"), fdp.Session())


def cover_count(message: str) -> int:
    """How many distinct target branches this one message drove through."""
    return len(set(_run(message).trace))


def reaches(message: str, label: str) -> bool:
    """True iff running this message executes the branch tagged `label`."""
    return label in _run(message).trace


def response(message: str) -> str:
    """The response code the target returns for this message."""
    return _run(message).code
