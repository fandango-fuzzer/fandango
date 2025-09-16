from typing import Optional
from fandango.language.tree import DerivationTree
from fandango.language.symbols.symbol import Symbol


class ParserDerivationTree(DerivationTree):
    def __init__(
        self,
        symbol: Symbol,
        children: Optional[list[DerivationTree]] = None,
        *,
        parent: Optional[DerivationTree] = None,
        sender: Optional[str] = None,
        recipient=None,
        read_only: bool = False,
        origin_repetitions: list[tuple[str, int, int]] | None = None,
    ):
        super().__init__(
            symbol,
            children,
            parent=parent,
            sources=[],
            sender=sender,
            recipient=recipient,
            read_only=read_only,
            origin_repetitions=origin_repetitions,
        )

    def set_children(self, children: list[DerivationTree]):
        self._children = children
        self.invalidate_hash(update_size=False)
