import enum
from thefuzz import process as thefuzz_process


class FuzzingMode(enum.Enum):
    COMPLETE = 0
    IO = 1


def closest_match(word, candidates):
    """
    `word` raises a syntax error;
    return alternate suggestion for `word` from `candidates`
    """
    return thefuzz_process.extractOne(word, candidates)[0]


class ParsingMode(enum.Enum):
    COMPLETE = 0
    INCOMPLETE = 1
