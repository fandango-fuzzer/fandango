#!/usr/bin/env pytest

import random
import threading

from fandango.api import Fandango
from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.io.violation import FandangoRemoteViolation, RemoteViolationType
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols.non_terminal import NonTerminal

from .utils import RESOURCES_ROOT

with open(RESOURCES_ROOT / "violation_io.fan") as spec_file:
    SPEC = spec_file.read()


def run_generate(
    replies: dict[str, str], spec: str = SPEC, remote_response_timeout: float = 15.0
):
    """Runs generate() to its end and returns the algorithm and how it ended."""
    ended: list[str] = []
    algorithms = []

    def run() -> None:
        # FandangoIO is bound to the context that builds the parties, so
        # everything happens on this thread.
        random.seed(1)
        fandango = Fandango(
            spec + f"\nREPLIES = {replies!r}\n", use_stdlib=False, use_cache=False
        )
        fandango.init_population(mode=FuzzingMode.IO)
        algorithm = fandango.fandango
        assert isinstance(algorithm, ProtocolAlgorithm)
        algorithm.remote_response_timeout = remote_response_timeout
        algorithms.append(algorithm)
        try:
            for _ in algorithm.generate():
                pass
            ended.append("returned")
        except Exception as error:
            ended.append(type(error).__name__)

    runner = threading.Thread(target=run, daemon=True)
    runner.start()
    runner.join(timeout=30)
    assert not runner.is_alive(), "generate() neither sent nor returned"
    return algorithms[0], ended[0]


def test_all_runs_failing() -> None:
    algorithm, ended = run_generate({})

    assert ended == "returned"
    assert algorithm._packet_selector.coverage_percent() == 1.0
    assert len(algorithm.violations) > 0


def test_syntax_violation() -> None:
    """Only HELLO fails. The guide target of a failed run must not carry
    over, or Fandango keeps repeating it and never reaches full coverage."""
    algorithm, ended = run_generate({"PING;": "PONG;", "BYE;": "OK;"})

    assert ended == "returned"
    assert algorithm._packet_selector.coverage_percent() == 1.0
    errors = [error for _, error in algorithm.violations]
    assert errors
    for error in errors:
        assert isinstance(error, FandangoRemoteViolation)
        assert error.error_type == RemoteViolationType.SYNTAX
        assert (error.sender, error.recipient, error.payload_raw) == (
            "Server",
            "Client",
            "ERR;",
        )
        assert error.expected_nonterminals == [NonTerminal("<hi>")]
        assert error.failed_constraints == []
        assert str(next(error.session_tree.protocol_msgs(reverse=True)).msg) == "HELLO;"
        assert error.payload_tree is None
        assert repr(error) == (
            "FandangoRemoteViolation(SYNTAX, Server -> Client: 'ERR;', expected <hi>)"
        )


def test_constraint_violation() -> None:
    spec = SPEC.replace(
        "<pong> ::= 'PONG;'",
        "<pong> ::= 'PONG' <counter> ';'\n<counter> ::= '1' | '7'\nwhere str(<counter>) == '1'",
    )
    algorithm, _ = run_generate(
        {"PING;": "PONG7;", "HELLO;": "HI;", "BYE;": "OK;"}, spec
    )

    errors = [error for _, error in algorithm.violations]
    assert errors
    for error in errors:
        assert isinstance(error, FandangoRemoteViolation)
        assert error.error_type == RemoteViolationType.CONSTRAINT
        assert (error.sender, error.recipient, error.payload_raw) == (
            "Server",
            "Client",
            "PONG7;",
        )
        assert error.expected_nonterminals == [NonTerminal("<pong>")]
        assert error.failed_constraints == ["str(<counter>) == '1'"]
        assert str(next(error.session_tree.protocol_msgs(reverse=True)).msg) == "PING;"
        assert error.payload_tree is not None
        assert error.payload_tree.nonterminal == NonTerminal("<pong>")
        assert error.payload_tree.to_string() == "PONG7;"
        assert repr(error) == (
            "FandangoRemoteViolation(CONSTRAINT, Server -> Client: 'PONG7;', "
            "expected <pong>, violates str(<counter>) == '1')"
        )


def test_parameter_derivation_violation() -> None:
    spec = SPEC.replace(
        "<pong> ::= 'PONG;'",
        "<pong> ::= 'PONG' <digits> ';' := 'PONG' + str(<count>) + ';'\n"
        "<digits> ::= r'[0-9]+'\n"
        "<count> ::= r'[0-9]' := str(<pong>)[4:-1]",
    )
    algorithm, _ = run_generate(
        {"PING;": "PONG42;", "HELLO;": "HI;", "BYE;": "OK;"}, spec
    )

    errors = [error for _, error in algorithm.violations]
    assert errors
    for error in errors:
        assert isinstance(error, FandangoRemoteViolation)
        assert error.error_type == RemoteViolationType.PARAMETER_DERIVATION
        assert (error.sender, error.recipient, error.payload_raw) == (
            "Server",
            "Client",
            "PONG42;",
        )
        assert error.expected_nonterminals == [NonTerminal("<pong>")]
        assert error.failed_constraints == []
        assert str(next(error.session_tree.protocol_msgs(reverse=True)).msg) == "PING;"
        assert error.payload_tree is not None
        assert error.payload_tree.nonterminal == NonTerminal("<pong>")
        assert repr(error) == (
            "FandangoRemoteViolation(PARAMETER_DERIVATION, Server -> Client: 'PONG42;', "
            "expected <pong>)"
        )


def test_timeout_violation() -> None:
    algorithm, ended = run_generate(
        {"PING;": "PONG;", "HELLO;": "", "BYE;": "OK;"}, remote_response_timeout=0.1
    )

    assert ended == "returned"
    timeouts = [
        error
        for _, error in algorithm.violations
        if isinstance(error, FandangoRemoteViolation)
        and error.error_type == RemoteViolationType.TIMEOUT
    ]
    assert timeouts
    for timeout in timeouts:
        assert (timeout.sender, timeout.recipient, timeout.payload_raw) == (
            "Server",
            None,
            "",
        )
        assert timeout.expected_nonterminals == [NonTerminal("<hi>")]
        assert (
            str(next(timeout.session_tree.protocol_msgs(reverse=True)).msg) == "HELLO;"
        )
        assert repr(timeout) == (
            "FandangoRemoteViolation(TIMEOUT, no message from Server, expected <hi>)"
        )
