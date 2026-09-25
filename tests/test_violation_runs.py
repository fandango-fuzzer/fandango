#!/usr/bin/env pytest

import random
import threading

from fandango.api import Fandango
from fandango.evolution.algorithm.protocol import ProtocolAlgorithm
from fandango.io.violation import FandangoRemoteViolation, RemoteViolationType
from fandango.language.grammar import FuzzingMode
from fandango.language.symbols.non_terminal import NonTerminal

# The server answers the requests named in REPLIES and sends ERR; to any
# other, which the grammar does not allow, so that run ends in a violation.
# The client stops the test after MAX_SENT messages if Fandango never
# stops on its own.
SPEC = """
<start> ::= <exchange>{1,4}
<exchange> ::= <ping> | <hello> | <bye>
<ping> ::= <Client:Server:ping_request> <Server:Client:pong>
<hello> ::= <Client:Server:hello_request> <Server:Client:hi>
<bye> ::= <Client:Server:bye_request> <Server:Client:ok>
<ping_request> ::= 'PING;'
<hello_request> ::= 'HELLO;'
<bye_request> ::= 'BYE;'
<pong> ::= 'PONG;'
<hi> ::= 'HI;'
<ok> ::= 'OK;'

REPLIES = %s
MAX_SENT = 60

class Client(FandangoParty):
    sent = 0

    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.OPEN)

    def send(self, message, recipient):
        Client.sent += 1
        if Client.sent > MAX_SENT:
            raise TooManyMessages()
        reply = REPLIES.get(str(message), "ERR;")
        if reply:
            self.io_instance.add_receive("Server", "Client", reply)

    def stop(self):
        pass

class Server(FandangoParty):
    def __init__(self):
        super().__init__(connection_mode=ConnectionMode.EXTERNAL)

    def stop(self):
        pass

class TooManyMessages(Exception):
    pass
"""


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
        fandango = Fandango(spec % replies, use_stdlib=False, use_cache=False)
        fandango.init_population(mode=FuzzingMode.IO)
        algorithm = fandango.fandango
        assert isinstance(algorithm, ProtocolAlgorithm)
        algorithm.remote_response_timeout = remote_response_timeout
        algorithms.append(algorithm)
        try:
            for _ in algorithm.generate():
                pass
            ended.append("returned")
        except BaseException as error:  # noqa: BLE001
            ended.append(type(error).__name__)

    runner = threading.Thread(target=run, daemon=True)
    runner.start()
    runner.join(timeout=30)
    assert not runner.is_alive(), "generate() neither sent nor returned"
    return algorithms[0], ended[0]


def test_full_coverage_ends_generation_even_if_every_run_fails() -> None:
    algorithm, ended = run_generate({})

    assert ended == "returned"
    assert algorithm._packet_selector.coverage_percent() == 1.0
    assert len(algorithm.violations) > 0


def test_a_failed_run_does_not_steer_the_next_one() -> None:
    """Only HELLO fails. The guide target of a failed run must not carry
    over, or Fandango keeps repeating it and never reaches full coverage."""
    algorithm, ended = run_generate({"PING;": "PONG;", "BYE;": "OK;"})

    assert ended == "returned"
    assert algorithm._packet_selector.coverage_percent() == 1.0


def test_a_violation_names_the_received_message_and_what_it_should_have_been() -> None:
    algorithm, _ = run_generate({"PING;": "PONG;", "BYE;": "OK;"})

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


def test_a_violated_constraint_is_named_with_the_message() -> None:
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


def test_a_parameter_that_cannot_be_derived_is_named_with_the_message() -> None:
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


def test_a_silent_server_ends_the_run_with_a_timeout_naming_the_party() -> None:
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
