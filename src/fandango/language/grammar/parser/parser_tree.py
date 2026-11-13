from typing import Optional

from fandango.language.symbols.symbol import Symbol
from fandango.language.tree import DerivationTree, Origin


class ParserDerivationTree(DerivationTree):
    def __init__(
        self,
        symbol: Symbol,
        children: Optional[list[DerivationTree]] = None,
        *,
        parent: Optional[DerivationTree] = None,
        sender: Optional[str] = None,
        recipient: Optional[str] = None,
        read_only: bool = False,
        origins: Optional[list[Origin]] = None,
    ):
        super().__init__(
            symbol,
            children,
            parent=parent,
            sources=[],
            sender=sender,
            recipient=recipient,
            read_only=read_only,
            origins=origins,
        )

    def set_children(self, children: list[DerivationTree]) -> None:
        self._children = children
        self.invalidate_hash(update_size=False)
