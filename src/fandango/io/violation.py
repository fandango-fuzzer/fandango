import enum
from typing import Optional

from fandango.errors import FandangoFailedError
from fandango.language.symbols.non_terminal import NonTerminal
from fandango.language.tree import DerivationTree


class RemoteViolationType(enum.Enum):
    SYNTAX = "SYNTAX"
    INCOMPLETE = "INCOMPLETE_PARSE"
    UNEXPECTED_PARTY = "UNEXPECTED_PARTY"
    CONSTRAINT = "CONSTRAINT"
    PARAMETER_DERIVATION = "PARAMETER_DERIVATION"
    TIMEOUT = "TIMEOUT"


class FandangoRemoteViolation(FandangoFailedError):
    """
    A message a remote party sent that does not fit the spec.
    """

    def __init__(
        self,
        message: str,
        *,
        error_type: RemoteViolationType,
        session_tree: DerivationTree,
        sender: str,
        recipient: Optional[str],
        payload_raw: str | bytes,
        expected_nonterminals: list[NonTerminal],
        failed_constraints: Optional[list[str]] = None,
        payload_tree: Optional[DerivationTree] = None,
    ):
        super().__init__(message)
        self.error_type = error_type
        self.session_tree = session_tree
        self.sender = sender
        self.recipient = recipient
        self.payload_raw = payload_raw
        self.expected_nonterminals = expected_nonterminals
        self.failed_constraints = failed_constraints or []
        self.payload_tree = payload_tree

    def __repr__(self) -> str:
        if self.error_type == RemoteViolationType.TIMEOUT:
            parts = [f"no message from {self.sender}"]
        else:
            parts = [f"{self.sender} -> {self.recipient}: {self.payload_raw!r}"]
        if self.expected_nonterminals:
            expected = " | ".join(
                nt.format_as_spec() for nt in self.expected_nonterminals
            )
            parts.append(f"expected {expected}")
        if self.failed_constraints:
            parts.append(f"violates {'; '.join(self.failed_constraints)}")
        return f"{type(self).__name__}({self.error_type.name}, {', '.join(parts)})"
