import abc
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from fandango.language.grammar.nodes.node import Node, NodeSettings


class HasSettings(abc.ABC):
    @abc.abstractmethod
    def settings_for(self, node: "Node") -> Optional["NodeSettings"]:
        raise NotImplementedError()
