"""Execution-feedback helpers for the FDP tutorial.

These wrap the FDP reference target so a Fandango spec can turn *execution
feedback* into an ordinary ``where`` constraint:

    where cover_count(str(<start>)) >= 8            # reward inputs that drive deep
    where reaches(str(<start>), "apply:login")      # demand a specific branch runs
    where response(str(<start>)) == "ERR_NOAUTH"    # constrain on the server's reply
    where covers_new(str(<start>))                  # spread coverage across the pop.

The first three judge each input on its own. ``covers_new`` is different: it
judges an input against everything generated before it, so the *population* as a
whole spreads across the target (see the section further down).

Feedback is *behavioural*: the message is run through the whole
``frame -> parse -> validate -> apply`` pipeline on a fresh session and we read
back what the target did, from the cheap branch trace it records about itself.
No ``sys.settrace`` is involved, so this stays fast inside Fandango's search
loop (line tracing there is orders of magnitude too slow).
"""

import json
import os
import sys
import tempfile

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


# ---------------------------------------------------------------------------
# Population coverage feedback: keep only inputs that cover what OTHERS do not.
#
# `cover_count` scores each message in isolation, so the search is happy to fill
# the whole population with inputs that all drive the *same* full accept path.
# A good test suite wants the opposite: every input should pull its weight by
# reaching a branch the rest of the population misses.
#
# `covers_new` turns that into a plain `where` constraint. It keeps a running
# record - in a temporary JSON file, so it survives across the whole fuzzing
# run - of which branches every input seen so far covered, and admits a message
# only if it reaches at least one branch NO other recorded input has:
#
#     covers_new(m) == True   iff m grows the population's covered-branch union
#
# So a redundant input that only retreads covered ground is rejected (punished),
# while an input that reaches a missing branch is accepted (rewarded). An
# accepted input is remembered in the record, so it keeps passing when the
# search re-checks it, while its would-be clones (same branches, nothing new)
# are turned away - the population spreads across branches instead of cloning
# one accept path.
#
# The target has only a handful of single-message branches, so the union fills
# up fast: once every reachable branch has a pioneer no further input can be
# "new", and the suite naturally caps at that minimal covering set (~5-6 here).
# Ask for a few outputs and read it as a `where` constraint:
#
#     where fdp_cover.covers_new(str(<start>))
# ---------------------------------------------------------------------------

# The shared record lives in one temporary JSON file per fuzzing run. It maps
# each ACCEPTED input to the branches it was the first to reach - i.e. the
# growing test suite and exactly what it covers. Point FDP_COVER_FILE elsewhere
# to relocate it (the coverage harness sets it per run).
_POPULATION_FILE = os.environ.get(
    "FDP_COVER_FILE",
    os.path.join(tempfile.gettempdir(), "fdp_cover_population.json"),
)

# accepted input string -> sorted branch labels it pioneered (mirrors the file)
_population: dict[str, list[str]] = {}
# every branch any accepted input has reached so far (the coverage union)
_covered: set[str] = set()


def _load() -> None:
    """Read the record back into memory (used at import and after a reset)."""
    global _population, _covered
    _population, _covered = {}, set()
    try:
        with open(_POPULATION_FILE, "r") as fh:
            _population = json.load(fh)
    except (OSError, ValueError):
        _population = {}
    for labels in _population.values():
        _covered.update(labels)


def _save() -> None:
    """Persist the record atomically so an interrupted run cannot corrupt it."""
    tmp = f"{_POPULATION_FILE}.{os.getpid()}.tmp"
    with open(tmp, "w") as fh:
        json.dump(_population, fh)
    os.replace(tmp, _POPULATION_FILE)


def reset() -> None:
    """Forget every input accepted so far and start a fresh, empty population."""
    try:
        os.remove(_POPULATION_FILE)
    except OSError:
        pass
    _load()


def covers_new(message: str) -> bool:
    """True iff `message` grows the population's coverage.

    The message is run through the target and we look at the branches it drove
    through. It is accepted only if it reaches at least one branch NO input
    already in the population has reached; a message that only retreads covered
    branches is rejected. Accepted messages are added to the shared record, so
    every later message is judged against everything accepted before it - the
    population spreads across branches instead of cloning one accept path.

    Only WELL-FORMED messages (those the target accepts all the way to its
    apply stage) count, matching the other `where` constraints: a malformed
    message is rejected here too, and never pollutes the record.
    """
    # An input already in the record was accepted before: it keeps its place,
    # so re-checking it during the search stays stable (and cheap).
    if message in _population:
        return True

    resp = _run(message)
    if resp.stage != "apply":  # not well-formed; a `where` above rejects it too
        return False

    labels = set(resp.trace)
    if labels <= _covered:  # every branch already covered -> redundant
        return False

    # First input to reach these branches: record it as part of the suite.
    _population[message] = sorted(labels)
    _covered.update(labels)
    _save()
    return True


# Fandango imports this module once per process, so resetting here starts every
# fuzzing run from an empty record: old runs never leak in, keeping generation
# reproducible.
reset()
