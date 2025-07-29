import abc
import copy
import enum
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any
from fandango.errors import FandangoValueError
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER

if TYPE_CHECKING:
    import fandango
    from fandango.language.grammar.node_visitors.node_visitor import NodeVisitor


class NodeType(enum.Enum):
    ALTERNATIVE = "alternative"
    CONCATENATION = "concatenation"
    REPETITION = "repetition"
    STAR = "star"
    PLUS = "plus"
    OPTION = "option"
    NON_TERMINAL = "non_terminal"
    TERMINAL = "terminal"
    CHAR_SET = "char_set"

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.value


class Node(abc.ABC):
    def __init__(
        self,
        node_type: NodeType,
        grammar_settings: Sequence["HasSettings"],
        distance_to_completion: float = float("inf"),
    ):
        self._grammar_settings = grammar_settings
        self._node_type = node_type
        self.distance_to_completion = distance_to_completion
        self._settings = NodeSettings({})
        for setting in grammar_settings:
            self._settings.update(setting.settings_for(self))

    @property
    def node_type(self):
        return self._node_type

    @property
    def is_terminal(self) -> bool:
        return self.node_type == NodeType.TERMINAL

    @property
    def is_nonterminal(self) -> bool:
        return self.node_type == NodeType.NON_TERMINAL

    @property
    def settings(self) -> "NodeSettings":
        return self._settings

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ):
        return

    @abc.abstractmethod
    def accept(self, visitor: "NodeVisitor"):
        raise NotImplementedError("accept method not implemented")

    def msg_parties(self, *, include_recipients: bool = False) -> set[str]:
        parties: set[str] = set()
        for child in self.children():
            parties |= child.msg_parties(include_recipients=include_recipients)
        return parties

    def slice_parties(self, parties: list[str]) -> None:
        """Remove all nodes whose party is not in `parties`."""
        for child in self.children():
            child.slice_parties(parties)

    def in_parties(self, parties: list[str]) -> bool:
        return True

    def children(self):
        return []

    def __repr__(self):
        raise NotImplementedError(
            "__repr__ not implemented, use method specific to your usecase"
        )

    def __str__(self):
        raise NotImplementedError(
            "__str__ not implemented, use method specific to your usecase"
        )

    @abc.abstractmethod
    def format_as_spec(self) -> str:
        """
        Format as a string that can be used in a spec file.
        """

    def descendents(
        self, grammar: "fandango.language.grammar.grammar.Grammar"
    ) -> Iterator["Node"]:
        """
        Returns an iterator of the descendents of this node.

        :param grammar: The rules upon which to base non-terminal lookups.
        :return An iterator over the descendent nodes.
        """
        yield from ()


NODE_SETTINGS_DEFAULTS = {
    "havoc_probability": 0.0,
    "max_stack_pow": 7,
    "terminal_should_repeat": 0.0,
    "plus_should_return_nothing": 0.0,
    "option_should_return_multiple": 0.0,
    "alternatives_should_concatenate": 0.0,
    "invert_regex": 0.0,
    "max_out_of_regex_tries": 10000,
    "non_terminal_use_other_rule": 0.0,
}


class NodeSettings:
    def __init__(
        self,
        raw_settings: dict[str, Any] = {},
    ):
        self._settings: dict[str, Any] = {}

        for k, v in NODE_SETTINGS_DEFAULTS.items():
            if k in raw_settings:
                self._settings[k] = type(v)(raw_settings[k])

    def get(self, key: str) -> Any:
        if key not in NODE_SETTINGS_DEFAULTS:
            raise FandangoValueError(f"Grammar setting {key} not found")
        if key in self._settings:
            return self._settings[key]
        else:
            return NODE_SETTINGS_DEFAULTS[key]

    def set(self, key: str, value: Any) -> None:
        if key not in NODE_SETTINGS_DEFAULTS:
            raise FandangoValueError(f"Grammar setting {key} not found")
        self._settings[key] = type(NODE_SETTINGS_DEFAULTS[key])(value)

    def __deepcopy__(self, memo: dict[int, Any]) -> "NodeSettings":
        return NodeSettings(copy.deepcopy(self._settings))

    def update(self, other: "NodeSettings | None") -> "NodeSettings":
        if other is None:
            return self

        for k in other._settings:
            if k in self._settings:
                LOGGER.warning(f"Overriding {k} with a different value")
            self._settings[k] = other._settings[k]

        return self
