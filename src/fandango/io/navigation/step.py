from fandango.io.navigation.graph.stategrammarconverter import StateGrammarConverter
from fandango.language.symbols.non_terminal import NonTerminal

# A transition of the state grammar.
Step = tuple[NonTerminal, NonTerminal]


def to_packet_step(parent: NonTerminal, packet_symbol: NonTerminal) -> Step:
    """The step from the parent rule to the packet, as the packet appears in the state grammar."""
    packet = StateGrammarConverter.to_packet_non_terminal(packet_symbol)
    assert isinstance(packet, NonTerminal)
    return parent, packet
