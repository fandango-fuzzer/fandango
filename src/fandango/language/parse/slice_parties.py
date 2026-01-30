from fandango.errors import FandangoValueError
from fandango.language.grammar import closest_match
from fandango.language.grammar.grammar import Grammar


def slice_parties(grammar: Grammar, parties: list[str]) -> None:
    """
    Slice the given parties from the grammar.
    :param grammar: The grammar to check
    :param parties: List of party names to check
    :raises FandangoValueError: If a party is not defined in the grammar
    """
    if not parties:
        return

    defined_parties = set(grammar.msg_parties(include_recipients=True))
    for party in parties:
        if party not in defined_parties:
            closest = closest_match(party, defined_parties)
            raise FandangoValueError(
                f"Party {party!r} not defined in the grammar. Did you mean {closest!r}?"
            )

    grammar.slice_parties(parties)
