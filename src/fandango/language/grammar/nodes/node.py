import abc
import copy
import enum
from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any, Optional
import warnings
from fandango.errors import FandangoValueError
from fandango.language.symbols import Symbol
from fandango.language.grammar.has_settings import HasSettings
from fandango.language.tree import DerivationTree
from fandango.logger import LOGGER

if TYPE_CHECKING:
    import fandango.language.grammar.node_visitors.node_visitor


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

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
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
    def node_type(self) -> NodeType:
        return self._node_type

    @property
    def is_terminal(self) -> bool:
        return self.node_type == NodeType.TERMINAL

    @property
    def is_nonterminal(self) -> bool:
        return self.node_type == NodeType.NON_TERMINAL

    @abc.abstractmethod
    def to_symbol(self) -> Symbol:
        """
        Convert the node to a symbol representation.
        Controlflow nodes are converted to Nonterminal-Symbols with the form <__type:id>
        """
        raise NotImplementedError("to_symbol method not implemented")

    @property
    def is_controlflow(self) -> bool:
        """
        Returns True if the node is a control flow node (i.e., not terminal or non-terminal).
        Controlflow nodes are nodes that affect the structure of the derivation tree, such as alternatives, concatenations, and repetitions...
        """
        return self.node_type not in {
            NodeType.TERMINAL,
            NodeType.NON_TERMINAL,
        }

    @property
    def settings(self) -> "NodeSettings":
        return self._settings

    def fuzz(
        self,
        parent: DerivationTree,
        grammar: "fandango.language.grammar.grammar.Grammar",
        max_nodes: int = 100,
        in_message: bool = False,
    ) -> None:
        return

    @abc.abstractmethod
    def accept(
        self,
        visitor: "fandango.language.grammar.node_visitors.node_visitor.NodeVisitor[fandango.language.grammar.node_visitors.node_visitor.AggregateType, fandango.language.grammar.node_visitors.node_visitor.ResultType]",
    ) -> "fandango.language.grammar.node_visitors.node_visitor.ResultType":
        raise NotImplementedError("accept method not implemented")

    def msg_parties(
        self,
        *,
        grammar: "fandango.language.grammar.grammar.Grammar",
        seen_nts: Optional[set[tuple[Optional[str], Optional[str], Symbol]]] = None,
        include_recipients: bool = False,
    ) -> set[str]:
        if seen_nts is None:
            seen_nts = set()
        parties: set[str] = set()
        for child in self.children():
            parties |= child.msg_parties(
                grammar=grammar,
                seen_nts=seen_nts,
                include_recipients=include_recipients,
            )
        return parties

    def in_parties(self, parties: list[str]) -> bool:
        return True

    def children(self) -> list["Node"]:
        return []

    def __repr__(self) -> str:
        warnings.filterwarnings("ignore",
            message=f"Don't rely on the __repr__ impl on {self.__class__.__name__}. Use a method specific to your usecase, such as format_as_spec(). Report this as a bug if this is called from within Fandango."
        )
        return f"{self.__class__.__name__}({self.format_as_spec()})"

    def __str__(self) -> str:
        warnings.warn(
            f"Don't rely on the __str__ impl on {self.__class__.__name__}. Use a method specific to your usecase, such as format_as_spec(). Report this as a bug if this is called from within Fandango."
        )
        return self.format_as_spec()

    @abc.abstractmethod
    def format_as_spec(self) -> str:
        """
        Format as a string that can be used in a spec file.
        """

    def descendents(
        self,
        grammar: "fandango.language.grammar.grammar.Grammar",
        filter_controlflow: bool = False,
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

    def update(self, other: Optional["NodeSettings"]) -> "NodeSettings":
        if other is None:
            return self

        for k in other._settings:
            if k in self._settings:
                LOGGER.warning(f"Overriding {k} with a different value")
            self._settings[k] = other._settings[k]

        return self
