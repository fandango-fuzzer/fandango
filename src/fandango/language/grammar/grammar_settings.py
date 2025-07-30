import copy
import re
from typing import Optional

from fandango.language.grammar.has_settings import HasSettings
from fandango.language.grammar.nodes.node import Node, NodeSettings
from fandango.language.grammar.nodes.non_terminal import NonTerminalNode


class GrammarSetting(HasSettings):
    ALL_WITH_TYPE_RE = re.compile(r"all_with_type\((.*?)\)")

    def __init__(self, selector: str, rules: dict[str, str]):

        self._selector = selector
        self._node_settings = NodeSettings(rules)

    def _matches(self, node: Node) -> bool:
        if self._selector == "*":
            return True
        if match := self.ALL_WITH_TYPE_RE.match(self._selector):
            if type(node).__name__ == match.group(1):
                return True
        if isinstance(node, NonTerminalNode):
            if node.symbol.name() == self._selector:
                return True
        return False

    def settings_for(self, node: "Node") -> Optional[NodeSettings]:
        if not self._matches(node):
            return None
        return copy.deepcopy(self._node_settings)
