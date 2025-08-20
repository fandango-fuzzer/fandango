from typing import Optional

from fandango.language import NonTerminal


class PacketNonTerminal:

    def __init__(self, sender: Optional[str], recipient: Optional[str], symbol: NonTerminal):
        self.sender = sender
        self.recipient = recipient
        self.symbol = symbol

    def __repr__(self):
        non_terminal_str = str(self.symbol)
        if self.sender is not None:
            sender_str = self.sender
        else:
            sender_str = ""
        if self.recipient is not None:
            recipient_str = self.recipient
        else:
            recipient_str = ""
        return f"<{sender_str}:{recipient_str}:{non_terminal_str[1:-1]}>"

    def __hash__(self):
        return hash((self.sender, self.recipient, self.symbol.name()))

    def __eq__(self, other):
        if not isinstance(other, PacketNonTerminal):
            return False
        return (
            self.sender == other.sender
            and self.recipient == other.recipient
            and self.symbol == other.symbol
        )