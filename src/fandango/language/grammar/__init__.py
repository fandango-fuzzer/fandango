from collections.abc import Collection
import enum
from thefuzz import process as thefuzz_process


class FuzzingMode(enum.Enum):
    COMPLETE = 0
    IO = 1


def closest_match(word: str, candidates: Collection[str]) -> str:
    """
    `word` raises a syntax error;
    return alternate suggestion for `word` from `candidates`
    """
    res = thefuzz_process.extractOne(word, candidates)[0]  # type: ignore[no-untyped-call] # thefuzz doesn't provide types
    assert isinstance(res, str)
    return res


class ParsingMode(enum.Enum):
    COMPLETE = 0
    INCOMPLETE = 1
